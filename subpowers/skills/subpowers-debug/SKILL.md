---
name: subpowers-debug
description: >
  Use when a test fails, behavior is wrong, or the root cause is unclear.
  Enforces root-cause-first investigation before any fix. Trigger on: "test
  fails", "broken", "error", "bug", "doesn't work", "why is".
---

# Debug

<directives>
Do not flail in the dark. Dissect the anomaly, establish its root cause, and only then change code.
</directives>

## I. The Dissection (Investigation)

Do not proceed until you can state: **"I know what is wrong and exactly where it lives."**

1. **Read the Trail:** Parse the full error — stack trace, line numbers, exact message. Do not skim.
2. **Reproduce It:** Identify the exact trigger, and confirm it fires every time.
3. **Consult the Past:** Run `git diff HEAD~3`.
4. **Isolate the Layers:** Inject logs at each boundary (API → service → datastore). Run once to find which layer
   breaks before changing anything.
5. **Direct Inquisition:** Confirm state through terminal commands and datastore queries — the ledger's `## Inspect`
   section. Reserve the browser for failures that are genuinely visual.

## II. The Decree (Hypothesis)

Form exactly one hypothesis: *"The root cause is [X] because [Y]."* Be specific.

## III. The Trap (The Failing Test)

Write a test in the project's own framework and idiom. Run `test-one`. It must fail for the exact reason you
hypothesized — not a missing import, not a broken fixture.

## IV. The Fix

* **One Change:** Make a single precise change targeting the root cause.
* **The Proof:** Run the trap — it must pass. Then run the full suite via `subpowers-check`.
* **The Ledger:** If bound to a plan, record the fix in `## Corrections`.

## V. The Wall (The 3-Strike Law)

If the fix fails, return to Phase I with what you just learned.

* **The Limit:** After **3 failed attempts**, halt. The architecture itself is likely at fault.
* **The Retreat:** Do not reset the working tree. `git restore .` and `git reset --hard` are forbidden here: both act on
  the whole repository, the tree may hold staged or unstaged work that is not yours, and neither command can tell the
  difference. Name the files you changed during this investigation and offer exactly two scoped options —
  `git restore -- <those paths>` to discard them, or `git stash push -m "debug: <hypothesis>" -- <those paths>` to
  shelve them for inspection. Wait for an answer before running either. Yielding a littered tree is a lesser failure
  than destroying work you did not create.
* **The Blockade:** Set `status: blocked` in the plan with a one-sentence `blocker`, and report back before yielding.
