# Subpowers — The Binding

A workflow for coding agents that refuses to skip steps: **explore → spec → plan →
implement → debug → check**. Six skills, one binding rule each, and a hard line between "I think this works"
and "I ran the command and read the output".

Installable as a Claude Code plugin marketplace, so it follows you across machines and projects instead of living in one
repo's `.claude/skills/`.

## Install

```bash
claude plugin marketplace add ohiliazov/subpowers
claude plugin install subpowers@subpowers
```

Install at **user scope** to get the skills in every project.

## The Six Skills

| Skill                 | The Rule                                                   | Invoke when...                                                           |
|:----------------------|:-----------------------------------------------------------|:-------------------------------------------------------------------------|
| `subpowers-explore`   | Look, but do not touch. Pure read-only discovery.          | You need to know "how X works" without triggering code changes or plans. |
| `subpowers-spec`      | Lock the *what* and *why* before anything touches files.   | The goal or the definition of "done" is still fuzzy.                     |
| `subpowers-plan`      | Scope and sequence multi-file work in writing before code. | The change spans several files or systems.                               |
| `subpowers-implement` | Red → green → refactor, followed by strict self-review.    | 1–2 files, purpose already clear.                                        |
| `subpowers-debug`     | Expose the root cause before changing code. 3-strike limit. | A test fails or behavior is wrong and you don't know why.                |
| `subpowers-check`     | Run the command, read the output, *then* make the claim.   | Before saying "done" — and automatically after a plan's last task.       |

They cross-reference each other deliberately to prevent AI scope-creep. The plan state-block schema lives only in
`subpowers-plan`; the evidence bar lives only in `subpowers-check`; a project's own conventions live only in that
project's contract (below).

## The Project Contract

The skills dictate the process. Your repo dictates the commands. The seam between them is one file: **
`.claude/subpowers.md`** in the project root.

```bash
cp <marketplace>/templates/subpowers.md <your-repo>/.claude/subpowers.md
```

Fill in what applies and delete the rest:

| Section                              | How the skills use it                                                                                          |
|:-------------------------------------|:----------------------------------------------------------------------------------------------------------------|
| `## Commands`                        | `test`, `test-one`, `typecheck`, `lint`, `build` — run verbatim by Check, Implement, and Debug.                 |
| `## Inspect`                         | Direct read-only state checks, strictly preferred over guessing or clicking through a UI.                       |
| `## Plans`                           | Where plan blueprints are written and archived (`dir: none` opts out).                                          |
| `## Evidence`                        | Extra claim → evidence rows that a standard green suite doesn't cover.                                          |
| `## Project rules`                   | The condensed, checkable form of your `CLAUDE.md` — applied during Implement's self-review. |
| `## Reindex / regeneration triggers` | Changes that demand an out-of-band step someone must be told about.                                             |

Without a contract, the skills still function: they discover commands from the package manifest, `Makefile`, and CI
workflow, then **demand confirmation from you before treating any output as proof**. They will offer to write the
contract so the next session skips that round-trip.

This is the exact reason the skillset is portable. A hardcoded `docker compose exec db psql -d myapp` is not slightly
wrong in a Go repo; it's an instruction that's actively corrupted. Commands live in the repo that owns them.

## Per-Project Overrides

A project-level `.claude/skills/subpowers-plan/` shadows nothing — plugin skills are namespaced — but two skills
answering to the same purpose is confusion, not flexibility. Prefer changing the contract. Fork a skill into a repo only
when that project's *process* genuinely differs, not just its commands.

## License

MIT — see [LICENSE](LICENSE).