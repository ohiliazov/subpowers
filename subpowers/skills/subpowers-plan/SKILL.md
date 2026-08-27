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

## II. The Realm & Opt-Out (Where Plans Live)

* **Location:** Plans live in the directory defined by `.claude/subpowers.md` (`## Plans` section, defaulting to
  `docs/subpowers/plans/`).
* **The Opt-Out Law (`dir: none`):** If the project contract specifies `dir: none`, plan files are forbidden. Keep the
  plan strictly in the chat context and announce plainly that handoff persistence is disabled.
* **The Append Law:** If `subpowers-spec` already created the plan file with frontmatter and a `## Spec` section, **do
  not overwrite it**. Append your Goal, Architecture, and Task sections below the existing `## Spec` heading and update
  the frontmatter.

## III. The Ledger (State Block)

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
```

* **Vocabulary:** `[ ]` pending · `[x]` executed · `[~]` deferred.
* **The Absolute Truth:** `next_task` dictates your reality. Never infer position by grepping for the first `[ ]`.
  Deferred tasks stay behind on purpose.

## IV. Forging the Blueprint (Step 1)

Write the plan to `<plans_dir>/<slug>.md`.

* **Traceability:** Every task must cite the specific acceptance criteria it fulfills.
* **Tagging:** Mark every task `[independent]` or `[sequential]`. A task is only `independent` if it shares ZERO files
  and ZERO runtime state with others. Do not guess; if unsure, it is `sequential`.
* **Commands:** Write the *exact, executable* test commands into the file. No placeholders.

```markdown
# <Feature Name> Implementation Plan

**Goal:** <One from sentence spec>
**Architecture:** <2-3 sentences>
**Tech Stack:** <Key libs>

---

### Task 1: <Name> [independent | sequential]

**Satisfies:** <Spec items>
**Files:** Create `path/file`, Modify `path/file`

- [ ] Test: `<exact_test_command>` → expect FAIL
- [ ] Implement code
- [ ] Verify: expect PASS

## Corrections

<!-- Append-only log of mid-flight course corrections -->
```

## V. The Oath (Step 2)

Present the blueprint. Demand my validation (a thumbs-up). Do not move code until the decree is given.

## VI. Resurrection (Step R - Resuming a Plan)

When waking into a session with an existing plan:

1. Read only the first 15 lines (the Frontmatter).
2. Read `## Spec` and `## Corrections`.
3. Read the specific task marked by `next_task`.
4. **Do not re-verify `[x]` items.** The past is sealed.
5. If `status: blocked`, read the blocker and halt.

## VII. Execution (Step 3)

* **Sequential Tasks:** Execute inline. Transition to `subpowers-implement` Step 3 (TDD). You must update the
  frontmatter and the checkboxes *in the exact same edit pass*.
* **Independent Tasks:** Dispatch them to sub-agents.
    * *The Summoning:* Feed the sub-agent the task section, the frontmatter (`suite_expected`), and the exact test
      commands.
    * *The Return:* The sub-agent must report touched files and exact test outputs. **The sub-agent is forbidden from
      editing the plan file.** You, the main thread, will write the state upon their successful return.
* **The Wall:** If an approach shatters, halt immediately. Do not improvise. Set `status: blocked`, define the
  `blocker`, log it in `## Corrections`, and await new orders.

## VIII. The Archive (Step 4)

When victory is absolute (`status: complete`, `next_task: null`, and `subpowers-check` verified), banish the blueprint.
Move the file (and its companions) to the `archive` directory under a `YYYY-MM-DD-<slug>` folder. Leave no completed
plans in the active directory.
