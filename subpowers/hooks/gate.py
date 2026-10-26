#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GREEN = ".claude/.gate-green"
RED = ".claude/.gate-red"
TAIL = 40


def git(root: Path, *args: str, env: dict[str, str] | None = None) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, env=env, check=True, capture_output=True, text=True, errors="replace"
    ).stdout.strip()


def repo_root(start: str) -> Path | None:
    try:
        return Path(git(Path(start), "rev-parse", "--show-toplevel"))
    except (subprocess.CalledProcessError, FileNotFoundError, NotADirectoryError):
        return None


def gates(root: Path) -> list[str]:
    path = root / ".claude" / "subpowers.md"
    if not path.is_file():
        return []
    section = re.search(r"^## Gates\s*$(.*?)(?=^## |\Z)", path.read_text(), re.MULTILINE | re.DOTALL)
    if not section:
        return []
    commands = re.findall(r"^\s*[-*]\s+`([^`]+)`", section.group(1), re.MULTILINE)
    return [c for c in commands if not re.fullmatch(r"<[^>]*>", c.strip())]


def fingerprint(root: Path) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        index = Path(tmp) / "index"
        real = root / git(root, "rev-parse", "--git-path", "index")
        if real.is_file():
            shutil.copyfile(real, index)
        env = {**os.environ, "GIT_INDEX_FILE": str(index)}
        git(root, "add", "-A", env=env)
        git(root, "rm", "-q", "--cached", "--ignore-unmatch", "--", GREEN, RED, env=env)
        return git(root, "write-tree", env=env)


def read(root: Path, name: str) -> str:
    path = root / name
    return path.read_text().strip() if path.is_file() else ""


def write(root: Path, name: str, value: str) -> None:
    path = root / name
    path.parent.mkdir(exist_ok=True)
    path.write_text(value + "\n")


def run(root: Path, command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, shell=True, cwd=root, capture_output=True, text=True, errors="replace")


def main() -> int:
    payload = json.loads(sys.stdin.read() or "{}")
    root = repo_root(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())
    if root is None:
        return 0
    commands = gates(root)
    if not commands:
        return 0
    try:
        tree = fingerprint(root)
    except subprocess.CalledProcessError as exc:
        print(f"subpowers gate: cannot fingerprint the tree, gates not run\n{exc.stderr}", file=sys.stderr)
        return 0 if payload.get("stop_hook_active") else 2
    if tree == read(root, GREEN):
        return 0
    if tree == read(root, RED):
        print("subpowers gate: still failing on an unchanged tree; stopping without a green gate", file=sys.stderr)
        return 0
    for command in commands:
        result = run(root, command)
        if result.returncode != 0:
            write(root, RED, tree)
            output = "\n".join((result.stdout + result.stderr).splitlines()[-TAIL:])
            print(f"subpowers gate failed: `{command}` exited {result.returncode}\n{output}", file=sys.stderr)
            return 2
    write(root, GREEN, tree)
    return 0


if __name__ == "__main__":
    sys.exit(main())
