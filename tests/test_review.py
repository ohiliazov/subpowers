from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REVIEW = Path(__file__).resolve().parent.parent / "subpowers" / "hooks" / "review.py"


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def contract(repo: Path, review: str | None) -> None:
    (repo / ".claude").mkdir(exist_ok=True)
    section = f"## Review\n\n{review}\n\n" if review is not None else ""
    (repo / ".claude" / "subpowers.md").write_text(f"# Contract\n\n{section}## Plans\n\n- `dir:` none\n")


def transcript(path: Path, *entries: dict) -> Path:
    path.write_text("".join(json.dumps(entry) + "\n" for entry in entries))
    return path


def user(text: str) -> dict:
    return {"type": "user", "message": {"role": "user", "content": text}}


def assistant(*blocks: dict) -> dict:
    return {"type": "assistant", "message": {"role": "assistant", "content": list(blocks)}}


def text(value: str) -> dict:
    return {"type": "text", "text": value}


def tool(name: str, **inputs: str) -> dict:
    return {"type": "tool_use", "name": name, "input": inputs}


def judge(tmp: Path, verdict: dict) -> str:
    seen = tmp / "seen.txt"
    script = tmp / "judge.py"
    script.write_text(
        "import json, sys\n"
        f"open({str(seen)!r}, 'w').write(sys.stdin.read())\n"
        f"print(json.dumps({{'result': json.dumps({verdict!r})}}))\n"
    )
    return f"{sys.executable} {script}"


def stop(repo: Path, log: Path, judge_cmd: str, active: bool = False) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"cwd": str(repo), "stop_hook_active": active, "transcript_path": str(log)})
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(repo), "SUBPOWERS_REVIEW_JUDGE": judge_cmd, "HOME": str(repo)}
    return subprocess.run(
        [sys.executable, str(REVIEW)], check=False, input=payload, capture_output=True, text=True, env=env
    )


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    (root / "CLAUDE.md").write_text("1. Never write «same again» in a plan.\n")
    return root


@pytest.fixture
def log(tmp_path: Path) -> Path:
    return transcript(
        tmp_path / "t.jsonl",
        user("old request"),
        assistant(text("old answer")),
        user("draw the plan"),
        assistant(text("Drawing."), tool("Write", file_path="plan.html", content="Кінець кола, далі таке саме")),
        assistant(text("Done: the plan is on the canvas.")),
    )


def test_without_review_section_allows_without_judging(repo: Path, log: Path, tmp_path: Path) -> None:
    contract(repo, None)

    result = stop(repo, log, judge(tmp_path, {"ok": True, "violations": []}))

    assert result.returncode == 0
    assert not (tmp_path / "seen.txt").exists()


def test_clean_verdict_allows(repo: Path, log: Path, tmp_path: Path) -> None:
    contract(repo, "- `CLAUDE.md`")

    result = stop(repo, log, judge(tmp_path, {"ok": True, "violations": []}))

    assert result.returncode == 0


def test_violation_blocks_with_rule_and_reason(repo: Path, log: Path, tmp_path: Path) -> None:
    contract(repo, "- `CLAUDE.md`")
    verdict = {
        "ok": False,
        "violations": [{"rule": "Never write «same again»", "where": "plan.html", "why": "says далі таке саме"}],
    }

    result = stop(repo, log, judge(tmp_path, verdict))

    assert result.returncode == 2
    assert "Never write «same again»" in result.stderr
    assert "says далі таке саме" in result.stderr


def test_judge_sees_rules_and_only_the_last_turn(repo: Path, log: Path, tmp_path: Path) -> None:
    contract(repo, "- `CLAUDE.md`")

    stop(repo, log, judge(tmp_path, {"ok": True, "violations": []}))

    seen = (tmp_path / "seen.txt").read_text()
    assert "Never write «same again» in a plan." in seen
    assert "Done: the plan is on the canvas." in seen
    assert "Кінець кола, далі таке саме" in seen
    assert "old answer" not in seen


def test_repeat_stop_after_a_block_allows_without_judging(repo: Path, log: Path, tmp_path: Path) -> None:
    contract(repo, "- `CLAUDE.md`")

    result = stop(
        repo, log, judge(tmp_path, {"ok": False, "violations": [{"rule": "r", "where": "w", "why": "y"}]}), active=True
    )

    assert result.returncode == 0
    assert not (tmp_path / "seen.txt").exists()


def test_broken_judge_warns_and_allows(repo: Path, log: Path, tmp_path: Path) -> None:
    contract(repo, "- `CLAUDE.md`")

    result = stop(repo, log, f"{sys.executable} -c 'import sys; sys.exit(5)'")

    assert result.returncode == 0
    assert "review not run" in result.stderr
