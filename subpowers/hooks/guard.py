#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

RULE = re.compile(r"^\s*[-*]\s+(deny|ask|allow)\s+`([^`]+)`\s+`([^`]+)`\s+(?:—|--?)\s+(.+?)\s*$")
PLACEHOLDER = re.compile(r"<[^>]*>")
DEFAULTS = Path(__file__).resolve().parent / "guards.md"
PLAN_PATH = re.compile(r"^\s*[-*]\s+`(dir|archive):`\s+`([^`]+)`", re.MULTILINE)


class Guard(NamedTuple):
    decision: str
    tool: str
    pattern: str
    reason: str


def repo_root(start: str) -> Path | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], cwd=start, check=True, capture_output=True, text=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, NotADirectoryError):
        return None
    return Path(out)


def section(text: str, name: str) -> str:
    found = re.search(rf"^## {name}\s*$(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return found.group(1) if found else ""


def parse(text: str) -> list[Guard]:
    parsed = [Guard(*match.groups()) for line in text.splitlines() if (match := RULE.match(line))]
    return [guard for guard in parsed if not PLACEHOLDER.fullmatch(guard.tool)]


def plan_paths(plans: str) -> dict[str, str]:
    found = dict(PLAN_PATH.findall(plans))
    paths = {}
    if found.get("dir", "none") != "none":
        paths["plans"] = re.escape(found["dir"].rstrip("/"))
    archive = re.split(r"<|YYYY", found.get("archive", ""))[0]
    if "/" in archive:
        paths["archive"] = re.escape(archive[: archive.rindex("/")])
    return paths


def defaults(paths: dict[str, str]) -> list[Guard]:
    filled = []
    for guard in parse(DEFAULTS.read_text()):
        needed = re.findall(r"\{(plans|archive)\}", guard.pattern)
        if all(key in paths for key in needed):
            pattern = re.sub(r"\{(plans|archive)\}", lambda match: paths[match.group(1)], guard.pattern)
            filled.append(guard._replace(pattern=pattern))
    return filled


def guards(root: Path) -> list[Guard]:
    path = root / ".claude" / "subpowers.md"
    text = path.read_text() if path.is_file() else ""
    return parse(section(text, "Guards")) + defaults(plan_paths(section(text, "Plans")))


def matching(rules: list[Guard], tool: str, inputs: dict) -> Guard | None:
    flat = json.dumps(inputs, ensure_ascii=False)
    for guard in rules:
        if re.fullmatch(guard.tool, tool) and re.search(guard.pattern, flat):
            return guard
    return None


def approvals(session: str) -> Path:
    base = Path(os.environ.get("SUBPOWERS_STATE_DIR") or Path(tempfile.gettempdir()) / "subpowers-approvals")
    return base / f"{re.sub(r'[^A-Za-z0-9_-]', '_', session)}.json"


def approved(session: str) -> set[str]:
    path = approvals(session)
    return set(json.loads(path.read_text())) if session and path.is_file() else set()


def remember(session: str, guard: Guard) -> None:
    path = approvals(session)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted(approved(session) | {guard.pattern})))


def main() -> int:
    payload = json.loads(sys.stdin.read() or "{}")
    root = repo_root(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())
    if root is None:
        return 0
    guard = matching(guards(root), payload.get("tool_name", ""), payload.get("tool_input") or {})
    if guard is None or guard.decision == "allow":
        return 0
    session = payload.get("session_id") or ""
    if payload.get("hook_event_name") == "PostToolUse":
        if guard.decision == "ask" and session:
            remember(session, guard)
        return 0
    if guard.decision == "ask" and guard.pattern in approved(session):
        decision = {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": f"subpowers guard: approved earlier this session ({guard.reason})",
        }
    else:
        decision = {
            "hookEventName": "PreToolUse",
            "permissionDecision": guard.decision,
            "permissionDecisionReason": f"subpowers guard: {guard.reason}",
        }
    print(json.dumps({"hookSpecificOutput": decision}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
