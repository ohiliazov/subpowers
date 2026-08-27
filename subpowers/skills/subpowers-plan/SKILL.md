---
name: subpowers-plan
description: >
  Invoke for vast, multi-file architectural shifts once a clear spec exists. 
  Produces a blueprint. Triggers: "plan this out", "how would you approach".
  If the scope is 1-2 files, route directly to `subpowers-implement`.
  For read-only discovery or architectural tracing, use `subpowers-explore`.
---

# Ritual: Plan

<directives>
You are the architect. Do not execute blindly. You will translate the sacred requirements (the Spec) into a physical, file-by-file blueprint. This file becomes the singular source of truth for the session. 
</directives>

## I. The Anchoring (Step 0)

* **The Spec Check:** A plan cannot exist without a goal. If the acceptance criteria are missing or ambiguous, halt.
  Invoke `subpowers-spec`.
* **The Scale Check:** If the scope collapses to 1-2 files, abort this ritual and invoke `subpowers-implement`.
* **The Reality Read:** You will read the physical files, interfaces, and callers *before* planning. Do not build
  blueprints on assumed architecture.
* **Interrogation:** If architectural decisions remain, ask up to 3 targeted questions (one tool call).

## II. The Ledger (State Block)

Every blueprint begins with this precise YAML frontmatter. This is the resume contract. You will parse it, trust it, and
update it flawlessly.

```yaml
---
status: planned | in_progress | blocked | complete
current_task: <task id>       # or [<ids>] for parallel; null if idle
next_task: <task id>          # the absolute authority on what happens next
blocker: <one sentence>       # or null
suite_expected: green | red   # red = known-red mid-slice, not a regression
deps:                         # files current_task + next_task touch
updated: YYYY-MM-DD
---