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
This skill makes small, localized changes. Do not design architecture here.
</directives>

## 1. Scope check

Do not run heavy process for a two-line fix, and do not skip it when the scope grows past 1-2 files.

* **Check for an existing plan:** If this work belongs to one, read its frontmatter first. Plans live in the directory
  named by `.claude/subpowers.md`'s `## Plans` section — the contract names the location, it is not itself the plan.
  Your entry point is `next_task`, never the first unchecked box. Do not re-verify completed work.
* **Route by scope:**
    * *Goal unclear?* Stop. Route to `subpowers-spec`.
    * *Spans multiple files or systems?* Stop. Route to `subpowers-plan`.
    * *Contained to 1-2 files?* Go to step 2.

## 2. TDD cycle

Run this per task. Match the surrounding test architecture — the project's framework, assertions, fixtures.

* **RED:** Write the smallest test for the new behavior. Run `test-one`. Confirm it fails for the right reason.
* **GREEN:** Write the minimum code to pass. Confirm no neighboring tests broke.
* **REFACTOR:** Clean names. Remove duplication. Stay green.
* **Known-red suites:** If the contract says `suite_expected: red`, the suite is known-red mid-slice and those failures
  are not yours to chase. Ensure only your own slice is green. The full suite must be green before the phase closes.

## 3. Self-review

Before declaring the work done, check it against these standards:

* **Correctness:** Are edge cases (`null`, zero, negative, overflow) handled? Are async operations awaited? Is the
  logic immune to injection?
* **Simplicity:** Does any function do two things? Is any logic copy-pasted? Delete dead code. If a new abstraction is
  used in fewer than 2 places, remove it.
* **Consistency:** Check the contract's `## Project rules`. If you made one location consistent but left an adjacent,
  equally applicable location untouched, you have created a fresh bug. Fix it.
* **Out-of-band steps:** Check `## Reindex / regeneration triggers`. If your change requires a cache flush, a search
  reindex, a client regeneration, or a backfill, announce it.

**What this pass can and cannot establish.** You are reviewing your own work in the context that produced it, so you
already believe the design decisions. That is fine for the checklist items above — a missing `await`, a hardcoded
color, an untranslated string are mechanical, and you either find them on the list or you do not. It is worthless for
judgment: whether the abstraction is right, whether a function does two things, whether an adjacent spot was left
inconsistent. On those you will agree with yourself.

**Escalation.** When the change turns on judgment rather than the checklist — a new abstraction, a refactor, a
consistency call across several files — do not settle for this pass. Dispatch a sub-agent with the diff
(`git diff HEAD`), the contract's `## Project rules`, and nothing else: no reasoning, no justification, no summary of
what you were trying to achieve. Context is what compromises a reviewer, so withhold it. Require findings ranked
Critical / Important / Minor, and act on them before step 4.

## 4. Final verification

* Run the verification commands required by `subpowers-check`.
* Execute them for real. Read the output.
* Fix anything you introduced.
* Do not declare the task done until the terminal proves it.
