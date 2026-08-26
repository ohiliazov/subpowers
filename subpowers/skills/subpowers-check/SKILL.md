---
name: subpowers-check
description: >
  Use before claiming any work is complete, and automatically as the final
  step once a `subpowers-plan` change finishes checking off its tasks.
  Runs tests and typecheck, provides concrete evidence. Trigger on: "done",
  "complete", "finished", "should work", before any PR or merge, or right
  after a plan's tasks are all checked off.
---

# Check

## The Rule

**Run the command. Read the output. Only then make the claim.**

"Should pass" and "looks right" are not verification.

## The project contract

Subpowers carries the process; the project carries the commands. Every
subpowers skill that needs to run something reads **`.claude/subpowers.md`** in
the repo root. This section defines how that file is resolved — other subpowers
skills cite it by name rather than restating it.

**Resolution order:**

1. **`.claude/subpowers.md` exists** — use it. Its `## Commands` table, its
   `## Inspect` block, its `## Plans` paths, its `## Evidence` rows, and its
   `## Project rules` are authoritative. Run those commands verbatim; don't
   "improve" them.
2. **It doesn't exist** — discover the commands from the repo before running
   anything: the package manifest's script section, the `Makefile`/`justfile`
   targets, the CI workflow (the most reliable source — it lists what actually
   has to pass), the test config, the container compose file. Then **state the
   commands you intend to run and get a yes before treating their output as
   the bar.** A suite you invoked the wrong way exits 0 and proves nothing.
3. **Once confirmed, offer to write the contract** — the plugin ships
   `templates/subpowers.md`; filling it in means the next session, and every
   other subpowers skill, skips this discovery. Offer once; don't nag.

A missing contract is a slower first run, not a blocker. A *stale* contract is
worse than none: if a command in it fails because it no longer matches the repo,
fix the contract in the same pass, don't route around it.

## Direct checks first — prefer these over the browser

Reach for the contract's `## Inspect` commands before opening a browser tab —
confirming state directly beats clicking through a UI or guessing. Reserve the
browser for claims that are actually about rendering (layout, theme, chart
drawing), where a direct check can't tell you anything.

If the contract has no `## Inspect` section, the equivalents are still usually
one command away — an HTTP call against the local API, a shell into the
datastore container, a cache `GET`/`TTL`, a query against the search index. Find
them once and write them into the contract.

## Commands

Run the contract's `test`, `typecheck`, `lint`, and `build` commands — plus any
extra row the contract marks as load-bearing. Two rules about which to run:

- **A passing unit suite is not a passing build.** Where a project has a build
  or bundle step, run it whenever a changed file is reachable from it; some
  whole classes of error surface *only* there and never in dev mode or a
  typecheck. That's exactly what the contract's extra rows exist to name.
- **Partial runs don't close a claim.** Run the single test during the TDD
  cycle; run the full suite before saying anything is done.

## Evidence required before each claim

| Claim | Required |
|-------|----------|
| "Tests pass" | The `test` command's own output showing zero failures, per suite that exists |
| "No type errors" | The `typecheck` command exits clean |
| "Bug is fixed" | The specific test that reproduced the bug now passes |
| "Feature works" | New tests pass + full suite clean |
| "Ready for review" | Every command in the contract's `## Commands` that applies to the changed surface — tests, typecheck, lint, build — passing |
| "Plan ready to close out" | Same full bar as "Ready for review" — neither checked-off boxes nor a `status: complete` state block is evidence on its own |

Plus every row in the contract's `## Evidence` section. Those exist because a
green suite doesn't establish them; treat them as non-optional.

## Write the evidence into the plan file

Evidence that only lands in chat dies with the context window. When checking work
against a plan (the contract's `## Plans` `dir`), put the real command-output
summary inline in that task's checked box — actual numbers, not "tests pass":

- `- [x] Run tests: 35 passed; full suite 1037 passed, no regressions`
- `- [x] ... predicted 14 rows (3+3+3+2+3), got 14; downgrade path restored all 3 originals`

A resuming agent can trust a number it can re-run and compare against; it cannot
trust the word "pass".

On a full pass, update the plan's state block (`subpowers-plan`'s "State block"
section) to `status: complete` with `next_task: null` — `subpowers-plan` Step 4
then archives the file.

## Red flags

- "Should work" — run it
- "Probably fine" — run it
- Tests passed earlier — run them again; code changed since then
- "The typecheck passed, so it's fine" — a typecheck is not a build and not a
  test; run what the contract says backs this claim
- Partial run (only the new test) — run the full suite too
- Ran a command you guessed at, with no contract and no confirmation — the exit
  code means nothing yet
- "All tasks are checked off", or a state block reading `status: complete` — that's
  task-tracking, not verification; run this skill anyway. Only inline evidence in the
  checked boxes carries a prior run forward
