from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

GATE = Path(__file__).resolve().parent.parent / "subpowers" / "hooks" / "gate.py"


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def contract(repo: Path, *commands: str) -> None:
    gates = "\n".join(f"- `{c}`" for c in commands)
    (repo / ".claude").mkdir(exist_ok=True)
    (repo / ".claude" / "subpowers.md").write_text(f"# Contract\n\n## Gates\n\n{gates}\n\n## Plans\n\n- `dir:` none\n")


def stop(repo: Path, active: bool = False) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"cwd": str(repo), "stop_hook_active": active, "hook_event_name": "Stop"})
    return subprocess.run([sys.executable, str(GATE)], check=False, input=payload, capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    (tmp_path / ".gitignore").write_text(".claude/.gate-green\n.claude/.gate-red\nran.log\n")
    (tmp_path / "app.txt").write_text("one\n")
    return tmp_path


def test_without_gates_allows(repo: Path) -> None:
    result = stop(repo)

    assert result.returncode == 0


def test_passing_gate_writes_stamp(repo: Path) -> None:
    contract(repo, "echo ran >> ran.log")

    result = stop(repo)

    assert result.returncode == 0
    assert (repo / ".claude" / ".gate-green").read_text().strip()


def test_unchanged_tree_skips_gates(repo: Path) -> None:
    contract(repo, "echo ran >> ran.log")
    stop(repo)

    stop(repo)

    assert (repo / "ran.log").read_text().count("ran") == 1


def test_changed_tree_reruns_gates(repo: Path) -> None:
    contract(repo, "echo ran >> ran.log")
    stop(repo)
    (repo / "app.txt").write_text("two\n")

    stop(repo)

    assert (repo / "ran.log").read_text().count("ran") == 2


def test_failing_gate_blocks_with_output(repo: Path) -> None:
    contract(repo, "echo boom && exit 3")

    result = stop(repo)

    assert result.returncode == 2
    assert "echo boom && exit 3" in result.stderr
    assert "boom" in result.stderr


def test_reported_failure_on_unchanged_tree_allows(repo: Path) -> None:
    contract(repo, "exit 1")
    stop(repo)

    result = stop(repo)

    assert result.returncode == 0
    assert "still failing" in result.stderr


def test_project_dir_wins_over_cwd(repo: Path, tmp_path_factory: pytest.TempPathFactory) -> None:
    contract(repo, "exit 1")
    elsewhere = tmp_path_factory.mktemp("elsewhere")

    result = subprocess.run(
        [sys.executable, str(GATE)],
        check=False,
        input=json.dumps({"cwd": str(elsewhere), "stop_hook_active": False}),
        capture_output=True,
        text=True,
        env={**os.environ, "CLAUDE_PROJECT_DIR": str(repo)},
    )

    assert result.returncode == 2
