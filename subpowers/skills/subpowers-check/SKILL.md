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
Do not assume. Do not guess. "Should work" and "looks right" are not verification. Run the command, read the output, and only then make the claim.
</directives>

## 1. Project contract

Find the exact commands that establish the claim.

1. **Contract present:** Read `.claude/subpowers.md`. Its `## Commands`, `## Inspect`, and `## Evidence` sections are
   binding. Run them verbatim. Do not alter them.
2. **No contract:** Discover the commands from the repository — CI workflows, Makefiles, package manifests. State the
   commands you intend to run and get approval before trusting their output.
3. **Offer to write one:** If the contract is missing, offer exactly once to create it from the template shipped with
   this plugin (`templates/subpowers.md` in the subpowers marketplace repo, not a path in this project). Do not nag.
4. **Stale contract:** A wrong command is worse than a missing one — a suite invoked the wrong way exits 0 and proves
   nothing. If a contract command fails because it no longer matches the repo, or names a port, path, or entry point
   that has since moved, fix the contract in the same pass. Do not route around it with a command of your own while
   leaving the contract wrong for the next session.

## 2. Direct checks

Verify state through the terminal, not the browser. Use the contract's `## Inspect` commands, direct HTTP calls,
datastore queries, or cache checks. Reserve the browser for claims that are genuinely about rendering — layout, theme,
chart drawing.

## 3. Evidence required

Partial runs do not count. A passing unit test is not a passing build. Run the full suite before you claim anything.

| Claim              | Required evidence                                              |
|:-------------------|:---------------------------------------------------------------|
| "Tests pass"       | Terminal output showing zero failures across the entire suite. |
| "No type errors"   | The `typecheck` command exits clean.                           |
| "Bug is fixed"     | The specific reproducing test now passes.                      |
| "Feature works"    | New tests pass AND the full suite is clean.                    |
| "Ready for review" | Tests, typechecks, linters, and builds all pass.                |
| "Plan complete"    | Same as above. Checked-off boxes are not evidence.             |

## 4. Write evidence into the plan

Evidence that lives only in the chat is lost when the context is. When verifying a plan, write the exact numbers into
the plan file's checked boxes.

* **Not evidence:** `- [x] Run tests: passed.`
* **Evidence:** `- [x] Run tests: 35 passed; full suite 1037 passed, 0 regressions.`

When the whole plan is verified, update the YAML state block to `status: complete` and `next_task: null`.

## 5. Stop conditions

Each thought below is a hard stop. Do not keep reasoning — run the command.

* *"It should work."* → run it
* *"It's probably fine."* → run it
* *"Tests passed earlier."* → the code changed. Run them again.
* *"The typecheck passed, so the build is fine."* → a typecheck is not a build. Run the build.
* *"All boxes are checked, so it is done."* → checked boxes are not evidence. Run this skill anyway.
