---
name: subpowers-check
description: >
  Invoke before claiming any task is complete, or automatically when a plan's 
  tasks are finished. You will run tests, typechecks, and builds to harvest 
  concrete evidence. Triggers: "done", "complete", "finished", "should work", 
  or before any PR.
---

# Ritual: Check

<directives>
You are the Arbiter of Reality. You do not assume. You do not guess. "Should work" and "looks right" are heresies. You will execute the command, read the output, and only then make the claim.
</directives>

## I. The Source of Truth (The Contract)

You must discover the exact commands required to prove reality.

1. **The Primary Ledger:** Read `.claude/subpowers.md`. Its `## Commands`, `## Inspect`, and `## Evidence` sections are
   absolute law. Run them verbatim. Do not alter them.
2. **The Wilderness:** If the ledger does not exist, you must discover the commands from the repository (CI workflows,
   Makefiles, package manifests). State your intended commands and demand my approval before trusting their output.
3. **The Offering:** If the ledger is missing, offer to forge it (`templates/subpowers.md`) exactly once. Do not nag.

## II. The Direct Inquisition

Do not rely on the browser unless verifying visual rendering (layout, themes, charts). State must be verified directly
via the terminal. Use `## Inspect` commands, direct HTTP API calls, datastore queries, or cache checks.

## III. The Burden of Proof

Partial runs are void. A passing unit test is not a passing build. Run the full suite before declaring victory.

| Your Claim         | Required Physical Evidence                                     |
|:-------------------|:---------------------------------------------------------------|
| "Tests pass"       | Terminal output showing zero failures across the entire suite. |
| "No type errors"   | The `typecheck` command exits clean.                           |
| "Bug is fixed"     | The specific reproducing test now passes perfectly.            |
| "Feature works"    | New tests pass AND the full suite is clean.                    |
| "Ready for review" | Tests, typechecks, linters, and builds all pass cleanly.       |
| "Plan complete"    | Same as above. Checked-off boxes are not proof.                |

## IV. The Etching (Plan Preservation)

Proof that lives only in the chat dies when the memory fades. When verifying a plan, you must etch the exact
mathematical evidence into the plan file's checked boxes.

* **Heresy:** `- [x] Run tests: passed.`
* **Truth:** `- [x] Run tests: 35 passed; full suite 1037 passed, 0 regressions.`

When the full plan is proven, update the YAML state block to `status: complete` and `next_task: null`.

## V. The Heresies (Red Flags)

If you think any of the following, you must immediately halt and execute verification commands:

* *"It should work."* (Run it.)
* *"It's probably fine."* (Run it.)
* *"Tests passed earlier."* (The code changed. The past is dead. Run them again.)
* *"The typecheck passed, so the build is fine."* (A typecheck is not a build. Run the build.)
* *"All boxes are checked, so it is done."* (Boxes are just ink. Run this ritual anyway.)
