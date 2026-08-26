---
name: subpowers-debug
description: >
  Use when a test fails, behavior is wrong, or the cause of a bug is unclear.
  Enforces root-cause-first debugging: reproduce → investigate → hypothesis →
  failing test → fix → verify. Trigger on: "test fails", "broken", "error",
  "unexpected behavior", "bug", "doesn't work", "why is".
---

# Debug

## The Rule

**Find the root cause before attempting any fix.**
Guessing wastes more time than investigating.

## Phase 1 — Reproduce and investigate

1. **Read the full error** — stack trace, line numbers, exact message. Don't skim.
2. **Reproduce consistently** — what exact steps trigger it every time?
3. **Check recent changes** — `git diff HEAD~3` — what could have caused this?
4. **Multi-layer systems** (API → service → datastore, or client → server):
   Add a log/print at each boundary, run once to find *where* it breaks before
   touching anything.
5. **Prefer direct checks over the browser to find *where* it breaks.** Use the
   project contract's `## Inspect` commands — `.claude/subpowers.md`, resolved
   per `subpowers-check`'s "The project contract" — to confirm the actual state
   the bug depends on: what the endpoint really returns, whether the row is
   really there, whether the cache key is stale, what the index really holds.

   Reserve the browser for bugs that are actually about rendering — layout,
   theme, chart drawing — where a direct check can't tell you anything.

Only proceed when you can state: **"I know what's wrong and where."**

## Phase 2 — Form one hypothesis

Write it down: _"The root cause is X because Y."_

One hypothesis. Be specific.

## Phase 3 — Write a failing test

Write a test that reproduces the bug before fixing anything, in this project's
own test framework and layout:

```
Arrange — the exact state that triggers the bug
Act     — call the thing that should work
Assert  — what it should return instead
```

Run it with the contract's `test-one` command. Confirm it fails for the exact
right reason — the missing behavior, not a missing import or a typo in the
fixture.

## Phase 4 — Fix and verify

- Make **one** change targeting the root cause
- Run the failing test → it must pass
- Run the full suite → nothing else must break. That means every applicable
  command in the contract's `## Commands`, per `subpowers-check` — not just the
  new test

Read the output. Only then declare it fixed.

**If this bug surfaced while executing a plan task**, the fix gets a dated entry
in that plan's `## Corrections` section — what changed and why — so the next
session doesn't read tasks that contradict the code.

## If the fix doesn't work

Return to Phase 1 with the new information you just learned.

After **3 failed attempts**: stop. The architecture might be the problem — discuss before trying more fixes.

On a plan task, stopping means recording it: set the plan's `status: blocked`
with a one-sentence `blocker` naming what's stuck, per `subpowers-plan`'s
"State block" section, before yielding. A silent stop leaves the next session
resuming into a wall it can't see.

## Red flags

| Thought | Action |
|--------|--------|
| "Probably X, let me just change it" | Phase 1 first |
| "I'll change a few things and see" | One change at a time |
| "It should work now" | Run the tests |
| "I've tried 3 things, let me try one more" | Stop — question the design |
