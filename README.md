# Subpowers

A workflow for coding agents that refuses to skip steps: **spec → plan →
implement → debug → check → review**. Six skills, one rule each, and a hard
line between "I think this works" and "I ran the command and read the output".

Installable as a Claude Code plugin marketplace, so it follows you across
machines and projects instead of living in one repo's `.claude/skills/`.

## Install

```bash
claude plugin marketplace add ohiliazov/subpowers
```

```bash
claude plugin install subpowers@subpowers
```

Install at **user scope** to get the skills in every project.

## The six skills

| Skill | Rule | Reach for it when |
|-------|------|-------------------|
| `subpowers-spec` | Lock the *what* and *why* before anything touches files | The goal or the definition of "done" is still fuzzy |
| `subpowers-plan` | Scope and sequence multi-file work in writing before code | The change spans several files or systems |
| `subpowers-implement` | Red → green → refactor, one small change at a time | 1–2 files, purpose already clear |
| `subpowers-debug` | Find the root cause before attempting any fix | A test fails or behavior is wrong and you don't know why |
| `subpowers-check` | Run the command, read the output, *then* make the claim | Before saying "done" — and automatically after a plan's last task |
| `subpowers-review` | Audit the diff for correctness, simplicity, house rules | Before committing or opening a PR |

They cross-reference each other deliberately: each rule is defined in exactly
one place. The plan state-block schema lives only in `subpowers-plan`; the
evidence bar lives only in `subpowers-check`; a project's own conventions live
only in that project's contract (below).

## The project contract

The skills carry process. Your repo carries commands. The seam between them is
one file: **`.claude/subpowers.md`** in the project root.

```
cp <marketplace>/templates/subpowers.md <your-repo>/.claude/subpowers.md
```

Fill in what applies and delete the rest:

| Section | What the skills do with it |
|---------|----------------------------|
| `## Commands` | `test`, `test-one`, `typecheck`, `lint`, `build`, `run` — run verbatim by check, implement, debug |
| `## Inspect` | Direct read-only state checks, preferred over clicking through a UI |
| `## Plans` | Where plan files are written and archived (`dir: none` opts out) |
| `## Evidence` | Extra claim → evidence rows a green suite doesn't establish here |
| `## Project rules` | The condensed, checkable form of your `CLAUDE.md` — the single copy, applied by implement Step 4 and review |
| `## Reindex / regeneration triggers` | Changes that need an out-of-band step someone must be told about |

Without a contract the skills still work: they discover commands from the
package manifest, `Makefile`, and CI workflow, then **confirm with you before
treating any output as the bar** — and offer to write the contract so the next
session skips that round-trip.

This is the whole reason the skillset is portable. A hardcoded
`docker compose exec db psql -d myapp` is not slightly wrong in a Go repo; it's
an instruction that's actively wrong. Commands live in the repo that owns them.

## Per-project overrides

A project-level `.claude/skills/subpowers-plan/` shadows nothing — plugin skills
are namespaced — but two skills answering to the same purpose is confusion, not
flexibility. Prefer changing the contract. Fork a skill into a repo only when
that project's *process* genuinely differs, not just its commands.

## License

MIT — see [LICENSE](LICENSE).
