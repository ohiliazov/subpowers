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
* **Check for a design:** If the plan, the contract's `## Design` section, or the user names a design for what you
  are touching, read that part before writing code. Build exactly what it shows — structure, styles, copy, order —
  and change only what binds it to real data and logic. Add, drop, restyle or "improve" nothing it does not show. If
  it is missing something you need, conflicts with the code, or cannot be built as drawn, stop and ask the user.
  Never invent the answer. If the work belongs to a plan, record the approved deviation in its `## Corrections`.
* **Route by scope:**
    * *Goal unclear?* Stop. Route to `subpowers-spec`.
    * *Spans multiple files or systems?* Stop. Route to `subpowers-plan`.
    * *Contained to 1-2 files?* Go to step 2.

## 2. TDD cycle

Run this per task. Match the surrounding test architecture — the project's framework, assertions, fixtures.

* **RED:** Write the smallest test for the new behavior. Run `test-one`. Confirm it fails for the right reason. Run
  commands with `subpowers-check`'s §2 bounded output.
* **GREEN:** Write the minimum code to pass. Confirm no neighboring tests broke.
* **REFACTOR:** Clean names. Remove duplication. Stay green.
* **Known-red suites:** If the plan's frontmatter says `suite_expected: red`, the suite is known-red mid-slice and
  those failures are not yours to chase. Ensure only your own slice is green. The full suite must be green before the
  phase closes.

## 3. Self-review

Before declaring the work done, check it against these standards:

* **Correctness:** Are edge cases (`null`, zero, negative, overflow) handled? Are async operations awaited? Is the
  logic immune to injection?
* **Simplicity:** Does any function do two things? Delete dead code. If a new abstraction is used in fewer than 2
  places, remove it.
* **Duplication:** Search the codebase, not just the diff, for logic your change repeats: an existing helper that
  already does what you wrote, a sibling block you copied or paralleled, the same pattern recurring across the files
  you touched. Duplication contained in your own diff is yours: remove it in REFACTOR. Duplication reaching outside
  the diff is not: do not fix it silently. In your final report, list each instance — locations, what they share, the
  proposed extraction and where it would live — and offer the deduplication. Act only on an explicit yes; if it spans
  more than 2 files, route to `subpowers-plan`.
* **Design fidelity:** If a design covers the change, compare the rendered result with it side by side. Every
  difference is either fixed or approved by the user — none is explained away.
* **Consistency:** Check the contract's `## Project rules`, reading every section it references in full. If you made
  one location consistent but left an adjacent, equally applicable location untouched, you have created a fresh bug.
  Fix it.
* **Out-of-band steps:** Check `## Reindex / regeneration triggers`. If your change requires a cache flush, a search
  reindex, a client regeneration, or a backfill, announce it.

**What this pass can and cannot establish.** You are reviewing your own work in the context that produced it, so you
already believe the design decisions. That is fine for the checklist items above — a missing `await`, a hardcoded
color, an untranslated string are mechanical, and you either find them on the list or you do not. It is worthless for
judgment: whether the abstraction is right, whether a function does two things, whether an adjacent spot was left
inconsistent. On those you will agree with yourself.

**Escalation.** When the change turns on judgment rather than the checklist — a new abstraction, a refactor, a
consistency call across several files — do not settle for this pass. Dispatch a sub-agent with the diff
(`git diff HEAD`), the contract's `## Project rules` with the sections it references pasted in, and nothing else: no
reasoning, no justification, no summary of what you were trying to achieve. Context is what compromises a reviewer, so withhold it. Require findings ranked
Critical / Important / Minor, and act on them before step 4.

## 4. Final verification

* Run the verification commands required by `subpowers-check`.
* Execute them for real. Read the output.
* Fix anything you introduced.
* Do not declare the task done until the terminal proves it.
