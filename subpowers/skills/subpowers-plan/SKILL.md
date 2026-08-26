---
name: subpowers-plan
description: >
  Use before implementing a change that touches multiple files or systems
  (client + server, several services, a schema change plus its callers),
  once a clear spec (goal + acceptance criteria) already exists. Produces a
  task-broken-down plan written to the project's plans directory and gets a
  thumbs-up before code moves.
  Trigger on: "plan this out", "write a plan", "how would you approach", or
  subpowers-implement's Step 1 landing on "multiple files/systems". Ambiguous
  goal/criteria → use `subpowers-spec` first. Skip for 1-2 file changes with
  a clear purpose — go straight to subpowers-implement.
---

# Plan

## The Rule

**Scope and sequence multi-file work in writing before touching code.**
A plan turns a signed-off spec into a checklist someone else could execute —
it answers "how", not "what" or "why".

A plan file is also the **handoff record** for its work: the one artifact a
session that has lost its context can re-enter execution from.

## Where plans live

The project contract's `## Plans` section — `.claude/subpowers.md`, resolved per
`subpowers-check`'s "The project contract" — gives `dir` (where plan files are
written) and `archive` (where Step 4 moves them). With no contract, default to
`docs/subpowers/plans/` and `docs/subpowers/plans/archive/YYYY-MM-DD-<slug>/`,
and mention that you're doing so.

If the contract says `dir: none`, this project has opted out of plan files: keep
the plan in the conversation, and say plainly that the handoff record is off —
a compacted or restarted session will have nothing to resume from.

## State block

Every plan file opens with YAML frontmatter. It is the resume contract — the
only part of a plan another session must read before doing anything.

```yaml
---
status: planned | in_progress | blocked | complete
current_task: <task id>       # or [<ids>] when independent tasks run in parallel; null if idle
next_task: <task id>          # the task to start next, or null when complete
blocker: <one sentence>       # or null
suite_expected: green | red   # red = known-red mid-slice, not a regression to chase
deps:                         # files current_task + next_task touch, not the whole plan
  - path/to/file
updated: YYYY-MM-DD
---
```

`status: blocked` requires a non-null `blocker`. `suite_expected: red` is how a
deliberately-red mid-slice state is distinguished from a regression, so nobody
resumes and starts chasing failures that the plan already expects.

**Checkbox vocabulary:** `[ ]` todo · `[x]` done · `[~]` deferred by a decision
or blocked on something external, reason inline. Task-level progress lives in
`current_task`, never as a token on the task heading — one marker, so the two
can't drift.

An item merely gated by task **ordering** (`[after E2]`, `depends on F1`) stays
`[ ]`. It will be actioned normally when its turn comes, and `[~]` would force a
future session to ask permission for ordinary sequenced work.

**`next_task` is authoritative. Never infer position by grepping for the first
`[ ]`.** Plans do not progress linearly: a deferred item stays behind on
purpose while later tasks complete, so the first unchecked box is routinely
*behind* the real frontier. Never action a `[~]` item without asking — it is
unchecked because someone decided so.

This schema is defined here and nowhere else. Other skills cite this section by
name instead of restating it.

## Step 0 — Confirm a spec exists, then ground the plan in the codebase

**0a. Verify a spec exists.** A plan translates acceptance criteria into
file paths and tasks — it needs those criteria to translate. A spec counts
as existing if any of:
- `subpowers-spec` already produced one earlier in this conversation, or
- a plan file already exists carrying a `## Spec` section (`subpowers-spec`
  writes one there for plan-routed specs) — if it also already has tasks, you
  are resuming: go to **Step R**, not Step 0, or
- the user's own request already states a clear goal and what "done" looks
  like (a well-scoped bug fix or small feature usually qualifies on its
  own).

If the goal or "done" state is still ambiguous — the request is broad,
or touches undefined business logic, data shape, or edge-case behavior —
**stop here and hand off to `subpowers-spec` first.** Don't guess at
requirements to keep momentum; a plan built on a guessed spec just moves
the rework downstream.

**0b. Re-check scope.** Once the spec's shape is clear, confirm this still
needs a plan at all: if it turns out to only touch 1-2 files with a clear
purpose, skip `subpowers-plan` entirely and hand off directly to
`subpowers-implement` — carrying the acceptance criteria forward as-is.

**0c. Read before you plan.** Search and read the files this change will
actually touch — the modules, interfaces, and callers involved — so the
plan cites real paths, real function signatures, and real existing patterns
instead of guessed ones. A plan built on assumptions costs more to fix
later than the minute spent reading now.

**0d. Batch clarifying questions.** Same batching rule as `subpowers-spec`
Step 0 (up to 3 targeted questions, one `AskUserQuestion` call, most
significant first) — but scoped to file-layout/architecture decisions, not
requirements (those belong to Step 0a's handoff to `subpowers-spec`). Skip
entirely if everything is already unambiguous.

## Step 1 — Write the plan

Assume this project's global constraints (stack conventions, testing rules,
etc.) apply — they're already established context in `CLAUDE.md`/`AGENTS.md`
and the contract's `## Project rules`; don't spend tokens re-copying them into
the plan. Write only what's specific to this change.

Each task's checklist should trace back to the spec: name which acceptance
criterion it satisfies, so the plan reads as a translation of the spec into
files and tests rather than a fresh re-derivation of scope.

**Tag each task `independent` or `sequential`.** A task is `independent` only
if it shares no files and no runtime state with any other task in the plan —
it doesn't read a model/function/type another task introduces, and no other
task reads anything it introduces. Everything else, including "probably
fine but touches an adjacent file," is `sequential`. This tag decides
execution mode in Step 3 — get it right, don't default to `independent` to
look parallelizable.

Write the plan to `<plans dir>/<slug>.md`, and also show it in chat for review.
**If `subpowers-spec` already created that file** with frontmatter and a
`## Spec` section, append below it and update the frontmatter — don't overwrite;
that section carries the signed-off decisions and is the reason nobody has to
re-derive them later.

```markdown
---
status: planned
current_task: null
next_task: 1
blocker: null
suite_expected: green
deps:
  - path/to/file
updated: YYYY-MM-DD
---

# <Feature Name> Implementation Plan

**Goal:** One sentence (from the spec).
**Architecture:** 2–3 sentences on approach.
**Tech Stack:** Key libs/layers touched.

---

### Task 1: <Name> [independent | sequential]

**Satisfies acceptance criteria:** <which spec item(s) this task delivers>

**Files:**
- Create: `exact/path/to/new/file`
- Modify: `exact/path/to/existing/file`
- Test: `exact/path/to/test/file`

**Interfaces:**
- Produces: `function_name(arg: Type) -> ReturnType`

- [ ] Write failing test: `<contract test-one command, filled in>` → expect FAIL
- [ ] Implement minimal code
- [ ] Run test: expect PASS, no other failures

### Task 2: ...

---

## Corrections

<!-- Append-only. One dated entry per mid-flight change of approach. -->
```

Write the **real** command into that first box — the contract's `test-one` with
this task's test path substituted in. A placeholder is a command the next
session has to reconstruct.

When the approach changes mid-execution — a task resliced, a dependency
discovered, an item deferred — it gets a dated `## Corrections` entry saying what
changed and why. Without a defined home, corrections land wherever the writer
happened to be, and the next session reads a plan whose tasks contradict its own
prose.

## Step 2 — Get sign-off

After writing: ask for a thumbs-up before executing. Do not start implementing
on the strength of your own plan — the point is a checkpoint before code
moves.

**If the user rejects or requests changes:** revise the plan file in place
(don't restart from scratch unless the rejection is fundamental) and ask for
sign-off again. Repeat until approved.

## Step R — Resume (entry point when the plan already exists)

When work resumes on a plan this session didn't write — a new session, a
compacted context, someone else's plan — start here, not at Step 0. Steps 0-2
already happened; redoing them re-litigates a signed-off plan.

1. **Read the frontmatter only** — `Read` with `limit=15`: status, position,
   blocker, and `deps` for the cost of a few lines.
2. **Read `## Spec`** (if present) and `## Corrections` — settled decisions not
   to re-litigate, and where the plan's prose has been overtaken.
3. **Read `next_task`'s section**, not the whole plan. A large plan is mostly
   finished work, and reading it invites re-verifying it.
4. **Don't re-verify `[x]` items** unless a failure implicates them, and don't
   action `[~]` items without asking.
5. **If `status: blocked`**, address the `blocker` or report it and stop — never
   route around a recorded blocker silently.

Then continue into Step 3 for `next_task`.

## Step 3 — Execute

**`sequential` tasks:** execute inline in this session, in order, handing off
to `subpowers-implement` Step 3 onward (TDD cycle) for each. Check off each
task's boxes in the plan file as it completes, so the file stays an accurate
record of progress if the session is interrupted.

**Write state in the same edit pass that ticks the boxes** — `current_task`,
`next_task`, `updated`, and `suite_expected` if the slice's expected suite state
changed. Boxes and frontmatter updated separately is how they end up disagreeing,
and the frontmatter is what the next session trusts.

**`independent` tasks:** dispatch each via the Agent tool (in parallel where
several are ready at once). If several independent tasks are likely to touch a
shared file (e.g. a shared translations/i18n file, a route table, a barrel
export), run those ones sequentially instead of in parallel to avoid one
overwriting another's edits.

**Dispatch payload** — the agent starts with no context, so send all of:
- the task's full section: files, interfaces, checklist, acceptance criteria
- the plan's frontmatter, so it knows `suite_expected` (whether a red suite is
  expected) and which `deps` matter
- any `## Spec` decisions and `## Corrections` entries bearing on this task
- the commands it should run, or a pointer to `.claude/subpowers.md` — an agent
  that guesses at the test command reports a result you can't trust
- the checkbox vocabulary, and: **do not edit the plan file** — the main thread
  owns it, so two agents can't clobber each other's state writes

**Return contract** — require the agent to report back, and treat a report
missing any of these as incomplete rather than filling the gap by assumption:
- files actually touched (created / modified / deleted)
- the exact test or verification command run, and its real output — not "tests
  pass"
- deviations from the task as written, and why
- any blocker hit, stated plainly rather than worked around

**Then write state yourself** from that report: tick the boxes, update
`current_task` / `next_task` / `updated`, and add a `## Corrections` entry if the
agent deviated. The agent never writes state; if you skip this after it reports,
progress-tracking silently stalls at the last thing you did by hand.

Don't default to inline-everything just because it's simpler to drive — the
whole point of tagging tasks in Step 1 is to let independent ones run off
the main thread. But don't force `independent` dispatch on a task that
turns out to be coupled after all; if the dispatched agent reports back that
a task actually depended on another task's output, treat that task as
`sequential` from then on and finish it inline yourself.

**If a task proves impossible or the approach breaks down mid-implementation:**
stop immediately — don't improvise around it. **Before yielding, set
`status: blocked` and a one-sentence `blocker`**, and record the reslice in
`## Corrections` if the approach itself changed. Then report what happened and
why to the user, and propose a revised plan (updated tasks, or a different
approach for the blocked one) before resuming. A session that ends without
writing state leaves the next one to guess, which is the failure this file
exists to prevent.

## Step 4 — Archive the plan once fully implemented

Once every task is implemented and verified — with `subpowers-check`'s evidence
bar met, not just boxes ticked — set `status: complete` and `next_task: null`,
then move the plan to the contract's `archive` path (default
`docs/subpowers/plans/archive/YYYY-MM-DD-<slug>/<slug>.md`; date = archival
date, not creation date). Nothing should linger checked-off in the top level of
the plans directory.

A plan is normally a single file, so archiving means creating that dated
directory and moving the file into it. If a plan accumulated companion files,
move the whole set together.
