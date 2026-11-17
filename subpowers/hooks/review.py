#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

TURN_LIMIT = 40_000
TOOL_LIMIT = 4_000
TIMEOUT = 240
DEFAULT_MODEL = "sonnet"
CHILD = "SUBPOWERS_REVIEW_CHILD"
INSTRUCTIONS = """You are a strict reviewer. Judge ONLY the assistant's last turn below against the rules below.
A violation is something the turn says or writes that a rule forbids, or something a rule requires that the turn
skipped. Check the logic of what was written too: a plan must read as a plan and an actual timeline as what happened,
and every statement must make sense in its own frame. Ignore rules the turn had no occasion to apply. Do not invent
rules. Reply with JSON only, no prose: {"ok": true, "violations": []} or
{"ok": false, "violations": [{"rule": "<the rule, quoted or numbered>", "where": "<message or file>", "why": "<what
in the turn breaks it>"}]}."""


def repo_root(start: str) -> Path | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], cwd=start, check=True, capture_output=True, text=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, NotADirectoryError):
        return None
    return Path(out)


def section(root: Path) -> list[str] | None:
    path = root / ".claude" / "subpowers.md"
    if not path.is_file():
        return None
    found = re.search(r"^## Review\s*$(.*?)(?=^## |\Z)", path.read_text(), re.MULTILINE | re.DOTALL)
    if not found:
        return None
    return [item.strip() for item in re.findall(r"^\s*[-*]\s+`([^`]+)`", found.group(1), re.MULTILINE)]


def settings(items: list[str]) -> tuple[list[str], str]:
    files, model = [], DEFAULT_MODEL
    for item in items:
        if item.startswith("model:"):
            model = item.split(":", 1)[1].strip() or DEFAULT_MODEL
        elif not re.fullmatch(r"<[^>]*>", item):
            files.append(item)
    return files, model


def rule_files(root: Path, listed: list[str]) -> list[Path]:
    home = Path(os.environ.get("HOME", str(Path.home())))
    found = [Path(item).expanduser() if item.startswith("~") else root / item for item in listed]
    parent = root.parent
    while parent != home and parent != parent.parent:
        found.append(parent / "CLAUDE.md")
        parent = parent.parent
    found += [home / "CLAUDE.md", home / ".claude" / "CLAUDE.md"]
    unique: dict[Path, Path] = {}
    for path in found:
        if path.is_file():
            unique.setdefault(path.resolve(), path)
    return list(unique.values())


def blocks(entry: dict) -> list:
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return content if isinstance(content, list) else []


def real_user(entry: dict) -> bool:
    if entry.get("type") != "user":
        return False
    return any(isinstance(block, dict) and block.get("type") == "text" for block in blocks(entry))


def render(block: dict) -> str | None:
    if block.get("type") == "text":
        return f"[assistant message]\n{block.get('text', '')}"
    if block.get("type") == "tool_use":
        inputs = json.dumps(block.get("input", {}), ensure_ascii=False)[:TOOL_LIMIT]
        return f"[tool {block.get('name')}]\n{inputs}"
    return None


def last_turn(transcript: Path) -> str:
    entries = []
    for line in transcript.read_text(errors="replace").splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    start = max((i for i, entry in enumerate(entries) if real_user(entry)), default=-1)
    parts = [
        rendered
        for entry in entries[start + 1 :]
        if entry.get("type") == "assistant"
        for block in blocks(entry)
        if isinstance(block, dict) and (rendered := render(block))
    ]
    return "\n\n".join(parts)[-TURN_LIMIT:]


def judge_command(model: str) -> list[str]:
    override = os.environ.get("SUBPOWERS_REVIEW_JUDGE")
    if override:
        return shlex.split(override)
    return [
        "claude",
        "-p",
        "--model",
        model,
        "--tools",
        "",
        "--no-session-persistence",
        "--settings",
        json.dumps({"disableAllHooks": True}),
        "--output-format",
        "json",
    ]


def verdict(raw: str) -> dict:
    outer = json.loads(raw)
    inner = outer.get("structured_output") or outer.get("result", outer)
    if isinstance(inner, str):
        match = re.search(r"\{.*\}", inner, re.DOTALL)
        inner = json.loads(match.group(0)) if match else {}
    return inner if isinstance(inner, dict) else {}


def report(violations: list[dict]) -> str:
    lines = [f"- {v.get('rule', '?')} — {v.get('where', '?')}: {v.get('why', '?')}" for v in violations]
    head = f"subpowers review: {len(violations)} rule violation(s) in this turn; fix them before stopping"
    return "\n".join([head, *lines])


def main() -> int:
    if os.environ.get(CHILD):
        return 0
    payload = json.loads(sys.stdin.read() or "{}")
    if payload.get("stop_hook_active"):
        return 0
    root = repo_root(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())
    items = section(root) if root else None
    if items is None:
        return 0
    transcript = Path(payload.get("transcript_path") or "")
    turn = last_turn(transcript) if transcript.is_file() else ""
    if not turn.strip():
        return 0
    listed, model = settings(items)
    rules = "\n\n".join(f"### {path}\n{path.read_text(errors='replace')}" for path in rule_files(root, listed))
    prompt = f"{INSTRUCTIONS}\n\n## Rules\n\n{rules}\n\n## The assistant's last turn\n\n{turn}\n"
    try:
        result = subprocess.run(
            judge_command(model),
            check=True,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            cwd=root,
            env={**os.environ, CHILD: "1"},
        )
        decided = verdict(result.stdout)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"subpowers review not run: {type(exc).__name__}", file=sys.stderr)
        return 0
    violations = [v for v in decided.get("violations") or [] if isinstance(v, dict)]
    if not violations:
        return 0
    print(report(violations), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
