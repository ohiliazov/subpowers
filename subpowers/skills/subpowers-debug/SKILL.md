---
name: subpowers-debug
description: >
  Use when a test fails, behavior is wrong, or the root cause is unclear.
  Enforces root-cause-first investigation before any fix. Trigger on: "test
  fails", "broken", "error", "bug", "doesn't work", "why is".
---

# Debug

<directives>
Do not guess at fixes. Establish the root cause first, then change exactly one thing.
</directives>

## 1. Investigation

Do not proceed until you can state: **"I know what is wrong and exactly where it lives."**

1. **Read the error:** Parse it in full — stack trace, line numbers, exact message. Do not skim.
2. **Reproduce it:** Identify the exact trigger, and confirm it fires every time.
3. **Check recent changes:** Run `git diff HEAD~3`.
4. **Isolate the layer:** Log at each boundary (API → service → datastore). Run once to find which layer breaks before
   changing anything.
5. **Check state directly:** Confirm state through terminal commands and datastore queries — the contract's
   `## Inspect` section. Reserve the browser for failures that are genuinely visual.

## 2. Hypothesis

Form exactly one: *"The root cause is [X] because [Y]."* Be specific.

## 3. Failing test

Write a test in the project's own framework and idiom. Run `test-one`. It must fail for the exact reason you
hypothesized — not a missing import, not a broken fixture.

## 4. Fix and verify

* **One change:** A single precise change targeting the root cause.
* **Verify:** Run the failing test — it must pass. Then run the full suite via `subpowers-check`.
* **Record:** If bound to a plan, record the fix in `## Corrections`.

## 5. Three-strike limit

If the fix fails, return to step 1 with what you just learned.

* **Limit:** After **3 failed attempts**, halt. The architecture itself is likely at fault.
* **Rollback:** Do not reset the working tree. `git restore .` and `git reset --hard` are forbidden here: both act on
  the whole repository, the tree may hold staged or unstaged work that is not yours, and neither command can tell the
  difference. Name the files you changed during this investigation and offer exactly two scoped options —
  `git restore -- <those paths>` to discard them, or `git stash push -m "debug: <hypothesis>" -- <those paths>` to
  shelve them for inspection. Wait for an answer before running either. Leaving a littered tree is a lesser failure
  than destroying work you did not create.
* **Blocked plans:** Set `status: blocked` in the plan with a one-sentence `blocker`, and report back before yielding.
