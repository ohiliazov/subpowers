from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parent.parent / "subpowers" / "hooks" / "guard.py"

GUARDS = """- deny `Bash` `git push\\s+(-f|--force)` — Never force-push.
- ask `Bash` `\\bgit push\\b` — Every push to main is a release.
- deny `.*ArtifactComments` `"action": "resolve"` — The owner resolves threads.
- deny `Read` `^(?!.*"limit").*docs/plans/[^/"]+\\.md` — Read the outline first.
- ask `<tool>` `<pattern>` — placeholder"""


def contract(repo: Path, guards: str | None) -> None:
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / ".claude").mkdir(exist_ok=True)
    section = f"## Guards\n\n{guards}\n\n" if guards is not None else ""
    (repo / ".claude" / "subpowers.md").write_text(f"# Contract\n\n{section}## Plans\n\n- `dir:` none\n")


def call(repo: Path, tool: str, **inputs: object) -> dict | None:
    payload = json.dumps({"cwd": str(repo), "tool_name": tool, "tool_input": inputs})
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(repo)}
    result = subprocess.run(
        [sys.executable, str(GUARD)], check=True, input=payload, capture_output=True, text=True, env=env
    )
    return json.loads(result.stdout)["hookSpecificOutput"] if result.stdout.strip() else None


def test_deny_names_the_rule(tmp_path: Path) -> None:
    contract(tmp_path, GUARDS)
    decision = call(tmp_path, "Bash", command="git push --force origin main")
    assert decision == {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "subpowers guard: Never force-push.",
    }


def test_first_matching_guard_wins_and_ask_prompts(tmp_path: Path) -> None:
    contract(tmp_path, GUARDS)
    assert call(tmp_path, "Bash", command="git push origin main")["permissionDecision"] == "ask"


def test_tool_name_is_a_full_match_regex(tmp_path: Path) -> None:
    contract(tmp_path, GUARDS)
    assert call(tmp_path, "mcp__x__ArtifactComments", action="resolve")["permissionDecision"] == "deny"
    assert call(tmp_path, "BashOutput", command="git push --force") is None


def test_pattern_sees_the_whole_input(tmp_path: Path) -> None:
    contract(tmp_path, GUARDS)
    assert call(tmp_path, "Read", file_path="/r/docs/plans/a.md")["permissionDecision"] == "deny"
    assert call(tmp_path, "Read", file_path="/r/docs/plans/a.md", offset=1, limit=40) is None


def test_no_match_and_placeholders_allow(tmp_path: Path) -> None:
    contract(tmp_path, GUARDS)
    assert call(tmp_path, "Bash", command="git status") is None


def plain_contract(repo: Path, body: str) -> None:
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / ".claude").mkdir(exist_ok=True)
    (repo / ".claude" / "subpowers.md").write_text(f"# Contract\n\n{body}")


def test_defaults_apply_without_a_guards_section(tmp_path: Path) -> None:
    plain_contract(tmp_path, "## Plans\n\n- `dir:` none\n")
    assert call(tmp_path, "Bash", command="git push origin main --force")["permissionDecision"] == "deny"
    assert call(tmp_path, "Bash", command="git reset --hard HEAD~1")["permissionDecision"] == "deny"
    assert call(tmp_path, "Bash", command="git clean -fdx")["permissionDecision"] == "deny"
    assert call(tmp_path, "Bash", command="uv add httpx")["permissionDecision"] == "ask"
    assert call(tmp_path, "Bash", command="npm install -D vitest")["permissionDecision"] == "ask"
    assert call(tmp_path, "Bash", command="npm ci && npm install") is None


def test_contract_allow_overrides_a_default(tmp_path: Path) -> None:
    plain_contract(tmp_path, "## Guards\n\n- allow `Bash` `uv add` — Dependencies are free here.\n")
    assert call(tmp_path, "Bash", command="uv add httpx") is None


def test_plan_guards_follow_the_plans_dir(tmp_path: Path) -> None:
    plain_contract(tmp_path, "## Plans\n\n- `dir:` `docs/plans/`\n- `archive:` `docs/plans/archive/<slug>/`\n")
    assert call(tmp_path, "Read", file_path=f"{tmp_path}/docs/plans/a.md")["permissionDecision"] == "deny"
    assert call(tmp_path, "Read", file_path=f"{tmp_path}/docs/plans/a.md", offset=1, limit=15) is None
    assert call(tmp_path, "Grep", pattern="x", path="docs/plans/archive")["permissionDecision"] == "ask"


def test_no_contract_still_gets_defaults(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    assert call(tmp_path, "Bash", command="git push -f")["permissionDecision"] == "deny"
