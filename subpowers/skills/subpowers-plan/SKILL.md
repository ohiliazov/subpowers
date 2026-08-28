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
Translate the spec into a file-by-file plan before code moves. This file becomes the source of truth for the work, and the handoff record a session that has lost its context can resume from.
</directives>

## 1. Preconditions

* **A spec must exist.** A plan cannot exist without a goal. If the acceptance criteria are missing or ambiguous, stop
  and route to `subpowers-spec`.
* **Re-check scope.** If the work collapses to 1-2 files, abandon this skill and route to `subpowers-implement`.
* **Read before planning.** Read the actual files, interfaces, and callers *before* writing tasks. Do not plan against
  assumed architecture.
* **Batch your questions.** If architectural decisions remain open, ask up to 3 targeted questions in one tool call.

## 2. Where plans live

* **Location:** The directory defined by `.claude/subpowers.md`'s `## Plans` section, defaulting to
  `docs/subpowers/plans/`.
* **Opt-out (`dir: none`):** If the contract specifies `dir: none`, plan files are forbidden. Keep the plan in the chat
  context and state plainly that handoff persistence is disabled.
* **Append, never overwrite:** If `subpowers-spec` already created the plan file with frontmatter and a `## Spec`
  section, **do not overwrite it**. Append your Goal, Architecture, and Task sections below the existing `## Spec`
  heading, and update the frontmatter.

## 3. State block

Every plan begins with this frontmatter. It is the resume contract. Parse it, trust it, and update it exactly.

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

* **Vocabulary:** `[ ]` pending · `[x]` done · `[~]` deferred by a decision, reason inline.
* **Ordering is not deferral:** an item merely gated by task order (`[after E2]`, `depends on F1`) stays `[ ]`. It will
  be actioned normally when its turn comes; marking it `[~]` forces a future session to ask permission for ordinary
  sequenced work.
* **`next_task` is authoritative:** never infer position by grepping for the first `[ ]` — deferred tasks stay behind on
  purpose, so the first unchecked box is routinely behind the real frontier. Never action a `[~]` item without asking.

This schema is defined here and nowhere else. Other skills cite this section rather than restating it.

## 4. Write the plan

Write it to `<plans_dir>/<slug>.md`, and show it in the chat for review.

* **Traceability:** Every task must cite the acceptance criteria it fulfills.
* **Tagging:** Mark every task `[independent]` or `[sequential]`. A task is `independent` only if it shares ZERO files
  and ZERO runtime state with any other task. Do not guess; if unsure, it is `sequential`.
* **Commands:** Write the exact, executable test commands into the file. No placeholders.

```markdown
# <Feature Name> Implementation Plan

## Spec

<!-- Present only when `subpowers-spec` created this file: the signed-off spec, verbatim.
     Append below it; never overwrite it. Absent when the plan was written directly. -->

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

Write the **real** command into that first box — the contract's `test-one` with this task's test path substituted in. A
placeholder is a command the next session has to reconstruct.

When the approach changes mid-execution — a task resliced, a dependency discovered, an item deferred — add a dated
`## Corrections` entry saying what changed and why. Without a defined home, corrections land wherever the writer
happened to be, and the next session reads a plan whose tasks contradict its own prose.

## 5. Sign-off

Present the plan and require explicit approval. Do not move code until it is given. If it is rejected, revise the file
in place and ask again.

## 6. Resume an existing plan

When entering a session with a plan already written, start here, not at step 1. Steps 1-5 already happened; redoing
them re-litigates an approved plan.

1. Read only the first 15 lines (the frontmatter).
2. Read `## Spec` and `## Corrections` — settled decisions, and where the plan's prose has been overtaken.
3. Read the specific task named by `next_task`, not the whole plan.
4. **Do not re-verify `[x]` items** unless a failure implicates them.
5. If `status: blocked`, address the blocker or report it and stop. Never route around a recorded blocker silently.

## 7. Execute

* **Sequential tasks:** Execute inline. Hand off to `subpowers-implement` step 2 (TDD). Update the frontmatter and the
  checkboxes *in the same edit pass* — updated separately is how they end up disagreeing, and the frontmatter is what
  the next session trusts.
* **Independent tasks:** Dispatch to sub-agents, in parallel where several are ready. If several would touch a shared
  file (an i18n file, a route table, a barrel export), run those sequentially instead.
    * *Dispatch payload:* the task section, the frontmatter (`suite_expected`, `deps`), the relevant `## Spec` and
      `## Corrections` entries, and the exact test commands. A sub-agent that guesses at the test command reports a
      result you cannot trust.
    * *Return contract:* require touched files, the exact command run, and its real output — not "tests pass". Treat a
      report missing any of these as incomplete rather than filling the gap by assumption.
    * *Plan-file ownership:* **the sub-agent is forbidden from editing the plan file.** The main thread writes state on
      its return, so two agents cannot clobber each other.
    * *Review the diff, not the report:* you did not write this code and you do not share the sub-agent's reasoning, so
      review its actual diff against the contract's `## Project rules` before you tick the boxes. A report describes
      what the sub-agent believes it did. Accepting the report in place of the diff is how a task closes green on work
      nobody read.
* **Phase close:** Before checking off a phase whose tasks you executed inline yourself, get eyes that are not yours on
  the accumulated diff. Dispatch one sub-agent with `git diff` for the phase and the contract's `## Project rules`,
  withholding your reasoning. This is the only pass that sees the whole phase at once, which is where cross-task
  inconsistency lives — each task looked correct in isolation, and the seam between them is what no single task's
  review covered.
* **When an approach breaks down:** halt immediately. Do not improvise around it. Set `status: blocked`, define the
  `blocker`, log the reslice in `## Corrections`, and report before yielding.

## 8. Archive

When the work is complete (`status: complete`, `next_task: null`, and `subpowers-check`'s evidence bar met — not just
boxes ticked), move the plan to the `archive` directory under a `YYYY-MM-DD-<slug>` folder, dated by archival. Move any
companion files with it. Leave no completed plans in the active directory.
