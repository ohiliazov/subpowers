---
name: subpowers-plan
description: >
  Use for multi-file or multi-system changes, once a clear spec exists.
  Produces a task-broken-down plan written to the project's plans directory,
  and gets approval before code moves. Trigger on: "plan this out", "write a
  plan", "how would you approach". If the scope is 1-2 files, route directly
  to `subpowers-implement`. For read-only discovery or architectural tracing,
  route to `subpowers-explore`.
---

# Plan

<directives>
Do not execute blindly. Translate the requirements (the Spec) into a file-by-file blueprint. This file becomes the source of truth for the work, and the handoff record a session that has lost its context can re-enter from.
</directives>

## I. The Anchoring (Step 0)

* **The Spec Check:** A plan cannot exist without a goal. If the acceptance criteria are missing or ambiguous, halt.
  Route to `subpowers-spec`.
* **The Scale Check:** If the scope collapses to 1-2 files, abandon this skill and route to `subpowers-implement`.
* **The Reality Read:** Read the actual files, interfaces, and callers *before* planning. Do not build blueprints on
  assumed architecture.
* **Interrogation:** If architectural decisions remain open, ask up to 3 targeted questions in one tool call.

## II. The Realm & Opt-Out (Where Plans Live)

* **Location:** Plans live in the directory defined by `.claude/subpowers.md` (`## Plans` section, defaulting to
  `docs/subpowers/plans/`).
* **The Opt-Out Law (`dir: none`):** If the contract specifies `dir: none`, plan files are forbidden. Keep the plan in
  the chat context and state plainly that handoff persistence is disabled.
* **The Append Law:** If `subpowers-spec` already created the plan file with frontmatter and a `## Spec` section, **do
  not overwrite it**. Append your Goal, Architecture, and Task sections below the existing `## Spec` heading, and update
  the frontmatter.

## III. The Ledger (State Block)

Every blueprint begins with this frontmatter. It is the resume contract. Parse it, trust it, and update it exactly.

```yaml
---
status: planned | in_progress | blocked | complete
current_task: <task id>       # or [<ids>] for parallel; null if idle
next_task: <task id>          # the authority on what happens next
blocker: <one sentence>       # or null
suite_expected: green | red   # red = known-red mid-slice, not a regression
deps:                         # files current_task + next_task touch
  - path/to/file
updated: YYYY-MM-DD
---
```

* **Vocabulary:** `[ ]` pending · `[x]` executed · `[~]` deferred by a decision, reason inline.
* **Ordering Is Not Deferral:** an item merely gated by task order (`[after E2]`, `depends on F1`) stays `[ ]`. It will
  be actioned normally when its turn comes; marking it `[~]` forces a future session to ask permission for ordinary
  sequenced work.
* **The Governing Rule:** `next_task` dictates position. Never infer it by grepping for the first `[ ]` — deferred tasks
  stay behind on purpose, so the first unchecked box is routinely behind the real frontier. Never action a `[~]` item
  without asking.

This schema is defined here and nowhere else. Other skills cite this section rather than restating it.

## IV. Forging the Blueprint (Step 1)

Write the plan to `<plans_dir>/<slug>.md`, and show it in the chat for review.

* **Traceability:** Every task must cite the acceptance criteria it fulfills.
* **Tagging:** Mark every task `[independent]` or `[sequential]`. A task is `independent` only if it shares ZERO files
  and ZERO runtime state with any other task. Do not guess; if unsure, it is `sequential`.
* **Commands:** Write the exact, executable test commands into the file. No placeholders.

```markdown
# <Feature Name> Implementation Plan

**Goal:** <One sentence, carried from the spec>
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

When the approach changes mid-execution — a task resliced, a dependency discovered, an item deferred — it gets a dated
`## Corrections` entry saying what changed and why. Without a defined home, corrections land wherever the writer
happened to be, and the next session reads a plan whose tasks contradict its own prose.

## V. The Oath (Step 2)

Present the blueprint and require explicit approval. Do not move code until it is given. If it is rejected, revise the
file in place and ask again.

## VI. Resurrection (Step R — Resuming a Plan)

When entering a session with an existing plan, start here, not at Step 0. Steps 0-2 already happened; redoing them
re-litigates an approved plan.

1. Read only the first 15 lines (the frontmatter).
2. Read `## Spec` and `## Corrections` — settled decisions, and where the plan's prose has been overtaken.
3. Read the specific task named by `next_task`, not the whole plan.
4. **Do not re-verify `[x]` items** unless a failure implicates them.
5. If `status: blocked`, address the blocker or report it and halt. Never route around a recorded blocker silently.

## VII. Execution (Step 3)

* **Sequential Tasks:** Execute inline. Transition to `subpowers-implement` Step II (TDD). Update the frontmatter and
  the checkboxes *in the same edit pass* — updated separately is how they end up disagreeing, and the frontmatter is
  what the next session trusts.
* **Independent Tasks:** Dispatch to sub-agents, in parallel where several are ready. If several would touch a shared
  file (an i18n file, a route table, a barrel export), run those sequentially instead.
    * *The Dispatch:* Feed the sub-agent the task section, the frontmatter (`suite_expected`, `deps`), the relevant
      `## Spec` and `## Corrections` entries, and the exact test commands. A sub-agent that guesses at the test command
      reports a result you cannot trust.
    * *The Return:* Require touched files, the exact command run, and its real output — not "tests pass". Treat a report
      missing any of these as incomplete rather than filling the gap by assumption.
    * *The Boundary:* **The sub-agent is forbidden from editing the plan file.** The main thread writes state on its
      return, so two agents cannot clobber each other.
* **The Wall:** If an approach breaks down, halt immediately. Do not improvise around it. Set `status: blocked`, define
  the `blocker`, log the reslice in `## Corrections`, and report before yielding.

## VIII. The Archive (Step 4)

When the work is complete (`status: complete`, `next_task: null`, and `subpowers-check`'s evidence bar met — not just
boxes ticked), retire the blueprint. Move the file, and any companions, to the `archive` directory under a
`YYYY-MM-DD-<slug>` folder, dated by archival. Leave no completed plans in the active directory.
