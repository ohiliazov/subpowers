---
name: subpowers-implement
description: >
  Use ONLY for small changes (roughly 1-2 files, purpose and root cause
  already known) — bigger or ambiguous work should go through
  `subpowers-spec`/`subpowers-plan` instead, since a full spec+plan+sign-off
  cycle is needless back-and-forth for something this small. Not a mystery —
  for unexplained/broken behavior use subpowers-debug first. Covers TDD,
  project-specific checks, and final verification. Trigger on: "add",
  "build", "implement", "fix" (once the fix is understood), "change",
  "refactor", "update" — but only when the change is small; a larger
  code-writing request should route to `subpowers-spec`/`subpowers-plan`.
---

# Implement

## Step 1 — Scope check

**This skill is reserved for small changes only — it keeps small work fast
for the user, not just cheap.** A full spec + plan (business logic locked in
chat, then a file-by-file task checklist written to disk, each with its own
sign-off) is real ceremony — extra round-trips and reading for something the
user just wants fixed. That structure earns its keep on real scope, not on a
two-line fix. So don't reach for it when it isn't warranted — but don't skip
it just to avoid the extra step on something that isn't actually small.

**First: does this work belong to an existing plan?** Check the project
contract's `## Plans` `dir` — `.claude/subpowers.md`, resolved per
`subpowers-check`'s "The project contract". If a plan covers this work, read its
frontmatter before anything else and take `next_task` as the entry point — never
the first unchecked box. Follow `subpowers-plan`'s "Step R — Resume" for what to
read and what not to re-verify, then come back here for that task's TDD cycle.

| Scope | Action |
|-------|--------|
| Goal/requirements still ambiguous | Use `subpowers-spec` first to lock in the "what" and "why" |
| Requirements clear but multiple files/systems involved | Use `subpowers-plan`, which turns the spec's acceptance criteria into a file-by-file task checklist, then drives Step 3 onward here per task |
| Small: roughly 1–2 files, purpose (and acceptance criteria) already clear | Skip to **Step 3** (TDD directly) — no spec/plan needed |

## Step 2 — (handled by subpowers-spec/subpowers-plan for anything non-trivial)

Ambiguous requirements get locked in via `subpowers-spec` (goal, acceptance
criteria, data shape, edge cases — signed off in chat). Once acceptance
criteria are clear and the work spans multiple files/systems, `subpowers-plan`
turns them into a task checklist and drives Step 3 onward here, inline, for
each task in order. Only skip both entirely for genuinely small work.

## Step 3 — TDD cycle (per task)

**RED** — Write the smallest test for the new behavior. Run it with the
contract's `test-one` command. Confirm it fails for the right reason — not a
missing import, the actual missing behavior.

**GREEN** — Write the minimal code to pass. Nothing extra.
Run again. Confirm it passes and no existing tests broke.

**REFACTOR** — Clean names, remove duplication. Stay green.

Match the surrounding code: this project's test framework, its assertion style,
its fixture conventions. A test written in the house style gets maintained; one
that isn't gets deleted.

**When the plan's frontmatter says `suite_expected: red`**, the suite is
*known* red mid-slice and those failures are not yours to chase. The
green-suite boundary is the phase, not the task: inside a phase, "no existing
tests broke" is scoped to the slice you're touching; when the phase closes, the
full suite must be green before it's checked off. Don't widen a task to fix
pre-existing red, and don't declare a phase done while it's still red — see
`subpowers-plan`'s "State block" section for what the flag means.

## Step 4 — Project rules (before final verify)

Apply the project contract's `## Project rules` section as a checklist against
what you just wrote — the condensed, checkable form of this project's own
conventions. That file is the **single** copy: `subpowers-review` applies the
same section to the diff rather than keeping its own, and if a rule changes in
`CLAUDE.md`/`AGENTS.md`, the contract is what gets updated.

Then check the contract's `## Reindex / regeneration triggers`: if this change
hit one, **announce the out-of-band step** — a search reindex, a cache flush, a
client regeneration, a backfill. A change that silently needs one is a change
that breaks in someone else's environment.

**No contract in this repo?** Read `CLAUDE.md`/`AGENTS.md` for this pass and say
which rules you checked against — an unstated project convention is the single
most common source of "works but gets sent back in review".

## Step 5 — Final verification

Run `subpowers-check`'s commands — every applicable command in the contract's
`## Commands`, not just the test you were iterating on. Read the output. Fix
anything. Only then say done.

On a plan task mid-phase, apply the expected-red rule from Step 3 when reading
that output: known-red failures the plan already expects don't block the task,
but they do block closing the phase.
