#!/usr/bin/env python3
"""Structural checks for the subpowers marketplace. No third-party deps.

Run from the repo root:  python3 scripts/validate.py
Exits non-zero on the first category of problem found, listing every instance.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "subpowers"
SKILLS = PLUGIN / "skills"
TEMPLATE = ROOT / "templates" / "subpowers.md"

ROMAN = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"}
# Scoped forms are fine; whole-repo forms must be presented as prohibitions.
DESTRUCTIVE = ("git reset --hard", "git restore .", "git clean -fd", "git checkout -- .")

errors: list[str] = []
checks = 0


def fail(msg: str) -> None:
    errors.append(msg)


def check(label: str) -> None:
    global checks
    checks += 1
    print(f"  {label}")


def frontmatter(text: str) -> str | None:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else None


def headings(text: str) -> list[str]:
    """H2 headings outside fenced code blocks."""
    out, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            out.append(line[3:].strip())
    return out


def main() -> int:
    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir()) if SKILLS.is_dir() else []
    if not skill_dirs:
        fail(f"no skill directories under {SKILLS.relative_to(ROOT)}")
        print("\n".join(errors))
        return 1
    names = {p.name for p in skill_dirs}
    docs = {p: p.read_text() for p in ROOT.rglob("*.md") if ".git" not in p.parts}
    skill_docs = {p: t for p, t in docs.items() if p.name == "SKILL.md"}

    # 1. manifests parse, carry required keys, and point at real directories
    check("manifests: JSON valid, required keys, sources exist")
    mp_path = ROOT / ".claude-plugin" / "marketplace.json"
    pl_path = PLUGIN / ".claude-plugin" / "plugin.json"
    mp = pl = None
    for path in (mp_path, pl_path):
        if not path.exists():
            fail(f"{path.relative_to(ROOT)}: missing")
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            fail(f"{path.relative_to(ROOT)}: invalid JSON — {exc}")
            continue
        if path == mp_path:
            mp = data
        else:
            pl = data
    if mp is not None:
        for key in ("name", "description", "plugins"):
            if key not in mp:
                fail(f"marketplace.json: missing required key {key!r}")
        for entry in mp.get("plugins", []):
            src = entry.get("source")
            if not src:
                fail(f"marketplace.json: plugin {entry.get('name')!r} has no source")
            elif not (ROOT / src).is_dir():
                fail(f"marketplace.json: source {src!r} is not a directory")
    if pl is not None:
        for key in ("name", "description", "version"):
            if key not in pl:
                fail(f"plugin.json: missing required key {key!r}")

    # 2. VERSION agrees with plugin.json
    check("version: VERSION file agrees with plugin.json")
    vfile = ROOT / "VERSION"
    if not vfile.exists():
        fail("VERSION: missing")
    elif pl is not None and vfile.read_text().strip() != pl.get("version"):
        fail(f"VERSION ({vfile.read_text().strip()!r}) != plugin.json version ({pl.get('version')!r})")

    # 3. every skill has frontmatter whose name matches its directory
    check("skills: frontmatter present, name matches directory, description non-empty")
    for path, text in sorted(skill_docs.items()):
        rel, dirname = path.relative_to(ROOT), path.parent.name
        fm = frontmatter(text)
        if fm is None:
            fail(f"{rel}: no YAML frontmatter")
            continue
        m = re.search(r"^name:\s*(\S+)", fm, re.M)
        if not m:
            fail(f"{rel}: frontmatter has no name:")
        elif m.group(1) != dirname:
            fail(f"{rel}: name {m.group(1)!r} != directory {dirname!r}")
        d = re.search(r"^description:\s*>?\s*\n?((?:.|\n)*?)(?=^\w+:|\Z)", fm, re.M)
        if not d or not d.group(1).strip():
            fail(f"{rel}: frontmatter has no description:")
    for d in skill_dirs:
        if not (d / "SKILL.md").exists():
            fail(f"{d.relative_to(ROOT)}: directory has no SKILL.md")

    # 4. no reference to a skill that does not exist
    check("references: every `subpowers-<name>` mention resolves to a real skill")
    for path, text in sorted(docs.items()):
        for ref in sorted(set(re.findall(r"\bsubpowers-[a-z][a-z-]*", text))):
            if ref not in names:
                fail(f"{path.relative_to(ROOT)}: references unknown skill {ref!r}")

    # 5. cross-skill section citations resolve in the cited skill
    check("citations: `skill` Step N / §N point at a section that exists")
    for path, text in sorted(skill_docs.items()):
        for ref, num in re.findall(r"`(subpowers-[a-z-]+)`(?:'s)?\s+(?:[Ss]tep|§)\s*([IVX]+|\d+)", text):
            if ref not in names:
                continue  # already reported by check 4
            target = SKILLS / ref / "SKILL.md"
            if not target.exists():
                continue
            heads = headings(target.read_text())
            token = num if num in ROMAN else num
            if not any(h.startswith(f"{token}.") or f"Step {token}" in h for h in heads):
                fail(f"{path.relative_to(ROOT)}: cites {ref} Step/§ {num}, which has no such section")

    # 6. contract/plan sections cited by skills exist in the template or in plan's own layout
    check("contract: every `## Section` cited by a skill is defined somewhere")
    defined = set(headings(TEMPLATE.read_text())) if TEMPLATE.exists() else set()
    if not TEMPLATE.exists():
        fail(f"{TEMPLATE.relative_to(ROOT)}: missing")
    plan_text = (SKILLS / "subpowers-plan" / "SKILL.md")
    plan_body = plan_text.read_text() if plan_text.exists() else ""
    for path, text in sorted(skill_docs.items()):
        for sec in sorted(set(re.findall(r"`##\s+([^`]+)`", text))):
            sec = sec.strip()
            if sec in defined:
                continue
            if re.search(rf"^##\s+{re.escape(sec)}\s*$", plan_body, re.M):
                continue  # a plan-file section, defined by the plan template
            fail(f"{path.relative_to(ROOT)}: cites `## {sec}`, absent from the contract template and plan layout")

    # 7. whole-repo destructive git commands only ever appear as prohibitions
    check("safety: whole-repo destructive git commands appear only as prohibitions")
    for path, text in sorted(docs.items()):
        for lineno, line in enumerate(text.splitlines(), 1):
            for cmd in DESTRUCTIVE:
                if cmd in line and "forbidden" not in line.lower():
                    fail(
                        f"{path.relative_to(ROOT)}:{lineno}: {cmd!r} present without being marked forbidden"
                    )

    # 8. hygiene
    check("hygiene: no trailing whitespace or tabs in skill files")
    for path, text in sorted(skill_docs.items()):
        for lineno, line in enumerate(text.splitlines(), 1):
            if line != line.rstrip():
                fail(f"{path.relative_to(ROOT)}:{lineno}: trailing whitespace")
            if "\t" in line:
                fail(f"{path.relative_to(ROOT)}:{lineno}: tab character")

    print()
    if errors:
        print(f"FAILED — {len(errors)} problem(s) across {checks} checks:\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK — {checks} checks passed across {len(skill_docs)} skills, {len(docs)} markdown files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
