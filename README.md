# Subpowers

A workflow for coding agents that refuses to skip steps: **explore → spec → plan →
implement → debug → check**. Six skills, one rule each, and a hard line between "I think this works"
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
| `subpowers-explore`   | Read-only. No writes, no code changes.                     | You need to know "how X works" without triggering code changes or plans. |
| `subpowers-spec`      | Lock the *what* and *why* before anything touches files.   | The goal or the definition of "done" is still fuzzy.                     |
| `subpowers-plan`      | Scope and sequence multi-file work in writing before code. | The change spans several files or systems.                               |
| `subpowers-implement` | Red → green → refactor, then review.                       | 1–2 files, purpose already clear.                                        |
| `subpowers-debug`     | Expose the root cause before changing code. 3-strike limit. | A test fails or behavior is wrong and you don't know why.                |
| `subpowers-check`     | Run the command, read the output, *then* make the claim.   | Before saying "done" — and automatically after a plan's last task.       |

They cross-reference each other deliberately to prevent AI scope-creep. The plan state-block schema lives only in
`subpowers-plan`; the evidence bar lives only in `subpowers-check`; a project's own conventions live only in that
project's contract (below).

There is deliberately no separate review skill. Independence in review comes from **context isolation**, not from which
file the instructions live in — an author reviewing their own work agrees with themselves whether the checklist sits in
a skill of its own or inline. So mechanical checks run inline (`implement` §3), and anything turning on judgment is
dispatched to a sub-agent that receives the diff and the project rules and none of the author's reasoning.

## The Project Contract

The skills dictate the process. Your repo dictates the commands. The seam between them is one file: **
`.claude/subpowers.md`** in the project root.

```bash
cp <marketplace>/subpowers/templates/subpowers.md <your-repo>/.claude/subpowers.md
```

Fill in what applies and delete the rest:

| Section                              | How the skills use it                                                                                          |
|:-------------------------------------|:----------------------------------------------------------------------------------------------------------------|
| `## Commands`                        | `test`, `test-one`, `typecheck`, `lint`, `build` — run verbatim by Check, Implement, and Debug.                 |
| `## Gates`                           | Commands the Stop hook runs before a turn may end, whenever the tree changed since the last green run.          |
| `## Inspect`                         | Direct read-only state checks, strictly preferred over guessing or clicking through a UI.                       |
| `## Plans`                           | Where plans are written and archived (`dir: none` opts out).                                          |
| `## Design`                          | Binding designs and what they cover — read before building, built as drawn, deviations asked first.             |
| `## Evidence`                        | Extra claim → evidence rows that a standard green suite doesn't cover.                                          |
| `## Project rules`                   | Checklist items, or `See <file> §<heading>` references to the rules where they already live — applied during Implement's self-review. |
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

## The Gate Hook

The skills can only ask for evidence; the plugin's Stop hook enforces it. When a turn ends, `hooks/gate.py` reads the
contract's `## Gates`, fingerprints the working tree's content (tracked and untracked non-ignored files, independent of commits), and runs the
gates only if that fingerprint differs from the last green one. A failure blocks the turn and hands the agent the
command and its last 40 lines. Each failing tree is reported once: stopping again on it, including on a turn that
changed nothing, is allowed with a warning rather than looping. The repo is `CLAUDE_PROJECT_DIR`, so a `cd` elsewhere
does not move the gate. The hook times out after 600 s. No contract, or no `## Gates`, and the hook does nothing.

The gates are shell commands from the repo's own contract and run at every changed Stop with no prompt, like any
project hook: enable the plugin only in repos whose contract you trust.

## Validating changes

```bash
uvx prek install          # once: run the hooks on every commit
uvx prek run --all-files  # on demand
```

The hooks run file hygiene, `ruff` on the scripts, and `scripts/validate.py`, which also runs alone as
`python3 scripts/validate.py`. The gate hook's tests run with `uvx --with pytest pytest tests` locally and in CI. The
validator checks the manifests parse and agree with `VERSION`, that the hooks manifest parses and every script it
runs exists, that each skill's
frontmatter `name` matches its directory, that every `subpowers-<name>` mention resolves to a skill that exists, that
cross-skill `Step N` citations point at real sections, that every `## Section` a skill cites is defined in the contract
template or the plan layout, that the template documents `## Project rules` references and every skill applying that
section resolves them, that every template path a skill cites resolves inside the installed plugin, that
whole-repo destructive git commands appear only as prohibitions, and that no skill file carries trailing whitespace or
tabs.

CI runs the same hooks on every push and pull request via
[`.github/workflows/validate.yml`](.github/workflows/validate.yml).

## License

MIT — see [LICENSE](LICENSE).
