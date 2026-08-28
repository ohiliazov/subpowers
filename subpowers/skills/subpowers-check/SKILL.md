---
name: subpowers-check
description: >
  Use before claiming any task is complete, and automatically once a plan's
  tasks are finished. Runs tests, typechecks, and builds to gather concrete
  evidence. Trigger on: "done", "complete", "finished", "should work", or
  before any PR.
---

# Check

<directives>
Do not assume. Do not guess. "Should work" and "looks right" are not verification. Execute the command, read the output, and only then make the claim.
</directives>

## I. The Source of Truth (The Contract)

Discover the exact commands that prove reality.

1. **The Primary Ledger:** Read `.claude/subpowers.md`. Its `## Commands`, `## Inspect`, and `## Evidence` sections are
   binding. Run them verbatim. Do not alter them.
2. **The Wilderness:** If the ledger does not exist, discover the commands from the repository (CI workflows, Makefiles,
   package manifests). State your intended commands and get approval before trusting their output.
3. **The Offering:** If the ledger is missing, offer to write it exactly once, from the template shipped with this
   plugin (`templates/subpowers.md` in the subpowers marketplace repo, not a path in this project). Do not nag.
4. **The Stale Ledger:** A wrong command is worse than a missing one — a suite invoked the wrong way exits 0 and proves
   nothing. If a ledger command fails because it no longer matches the repo, or names a port, path, or entry point that
   has since moved, fix the ledger in the same pass. Do not route around it with a command of your own while leaving the
   ledger wrong for the next session.

## II. The Direct Inquisition

Verify state through the terminal, not the browser. Use `## Inspect` commands, direct HTTP calls, datastore queries, or
cache checks. Reserve the browser for claims that are genuinely about rendering — layout, theme, chart drawing.

## III. The Burden of Proof

Partial runs are void. A passing unit test is not a passing build. Run the full suite before you claim anything.

| Your claim         | Required evidence                                              |
|:-------------------|:---------------------------------------------------------------|
| "Tests pass"       | Terminal output showing zero failures across the entire suite. |
| "No type errors"   | The `typecheck` command exits clean.                           |
| "Bug is fixed"     | The specific reproducing test now passes.                      |
| "Feature works"    | New tests pass AND the full suite is clean.                    |
| "Ready for review" | Tests, typechecks, linters, and builds all pass.                |
| "Plan complete"    | Same as above. Checked-off boxes are not proof.                |

## IV. The Etching (Plan Preservation)

Proof that lives only in the chat dies when the context does. When verifying a plan, write the exact numbers into the
plan file's checked boxes.

* **Not proof:** `- [x] Run tests: passed.`
* **Proof:** `- [x] Run tests: 35 passed; full suite 1037 passed, 0 regressions.`

When the full plan is proven, update the YAML state block to `status: complete` and `next_task: null`.

## V. The Stop Conditions

Each thought below is a hard stop. Do not keep reasoning — run the command.

* *"It should work."* → run it
* *"It's probably fine."* → run it
* *"Tests passed earlier."* → the code changed. Run them again.
* *"The typecheck passed, so the build is fine."* → a typecheck is not a build. Run the build.
* *"All boxes are checked, so it is done."* → boxes are ink, not evidence. Run this skill anyway.
