---
name: subpowers-implement
description: >
  Use ONLY for small, precise changes (1-2 files, purpose already clear).
  Ambiguity or larger scope routes to `subpowers-spec` or `subpowers-plan`.
  Unexplained behavior routes to `subpowers-debug`. Read-only discovery
  routes to `subpowers-explore`. Trigger on: "add", "build", "implement",
  "fix", "change", "refactor", "update".
---

# Implement

<directives>
This skill enacts swift, localized change. Do not design architecture here. It is for precise, known, tightly scoped execution.
</directives>

## I. The Scope Gate

Do not invoke heavy ceremony for a two-line fix, and do not bypass ceremony when the scope grows past your control.

* **The Ledger Check:** If this work is bound to an existing plan, read its frontmatter first. Plans live in the
  directory named by `.claude/subpowers.md`'s `## Plans` section — the contract names the location, it is not itself the
  plan. Your entry point is `next_task`, never the first unchecked box. Do not re-verify the past.
* **The Scale Test:**
    * *Is the goal unclear?* Halt. Route to `subpowers-spec`.
    * *Does it span multiple files or systems?* Halt. Route to `subpowers-plan`.
    * *Is it contained to 1-2 files?* Proceed directly to The Trial of TDD.

## II. The Trial of TDD

Execute this cycle per task. Match the surrounding test architecture — the project's framework, assertions, fixtures.

* **RED:** Write the smallest test for the new behavior. Run `test-one`. Confirm it fails for the right reason.
* **GREEN:** Write the minimum code to pass. Confirm no neighboring tests broke.
* **REFACTOR:** Clean names. Remove duplication. Stay green.
* **The Red Clause:** If the ledger says `suite_expected: red`, the suite is known-red mid-slice and those failures are
  not yours to chase. Ensure only your own slice is green. The full suite must be green before the phase closes.

## III. The Inquisition (Self-Review)

Before declaring victory, judge your own work against these standards:

* **Correctness:** Are edge cases (`null`, zero, negative, overflow) handled? Are async operations awaited? Is the logic
  immune to injection?
* **Simplicity:** Does any function serve two masters? Is any logic copy-pasted? Delete dead code. If a new abstraction
  is used in fewer than 2 places, remove it.
* **Consistency:** Check the ledger's `## Project rules`. If you made one location consistent but left an adjacent,
  equally applicable location untouched, you have created a fresh bug. Fix it.
* **The Out-of-Band Cry:** Check `## Reindex / regeneration triggers`. If your change requires a cache flush, a search
  reindex, a client regeneration, or a backfill, announce it.

**What this pass can and cannot establish.** You are reviewing your own work in the context that produced it, so you
already believe the design decisions. That is fine for the checklist items above — a missing `await`, a hardcoded
color, an untranslated string are mechanical, and you either find them on the list or you do not. It is worthless for
judgment: whether the abstraction is right, whether a function does two things, whether an adjacent spot was left
inconsistent. On those you will agree with yourself.

**The escalation.** When the change turns on judgment rather than the checklist — a new abstraction, a refactor, a
consistency call across several files — do not settle for this pass. Dispatch a sub-agent with the diff
(`git diff HEAD`), the ledger's `## Project rules`, and nothing else: no reasoning, no justification, no summary of
what you were trying to achieve. Context is what compromises a reviewer, so withhold it. Require findings ranked
Critical / Important / Minor, and act on them before the Final Seal.

## IV. The Final Seal

* Run the verification commands required by `subpowers-check`.
* Execute them for real. Read the output.
* Fix anything you introduced.
* Do not declare the task done until the terminal proves it.
