---
name: subpowers-spec
description: >
  Use before any file-level planning or implementation when a request is
  broad, ambiguous, or needs business logic, data models, or acceptance
  criteria defined first. Trigger on: "design a feature", "write a spec",
  "define requirements", or any request whose goal or "done" state isn't
  clear yet. Produces a spec (what/why) that `subpowers-plan` or
  `subpowers-implement` then turns into the how. Skip when the goal and
  acceptance criteria are already obvious — go straight to `subpowers-plan`
  or `subpowers-implement`.
---

# Spec

## The Rule

**Lock in the "what" and "why" before anything touches files or code.**
A spec turns "build me a usage dashboard" into a concrete goal, acceptance
criteria, data shape, and edge cases someone else could scope and build from —
without yet deciding which files change.

This is a business-logic checkpoint, not a file-level one. It never names
files, functions, or a task checklist — that's `subpowers-plan`'s job once
the spec is signed off.

## Step 0 — Understand the domain, then clarify

1. **Read relevant codebase context first.** Look at existing models,
   schemas, and adjacent features to understand how this domain already
   works here — so the spec's data model and edge cases fit reality instead
   of a generic guess.
2. **Batch clarifying questions.** Resolve requirements ambiguity in one
   round: up to 3 highly targeted questions (each a single decision, 2-4
   options, multiple-choice or yes/no) in a single `AskUserQuestion` call —
   covering things like ambiguous business rules, edge-case handling, or
   UX intent that would change what "done" means.
   - Don't ask about implementation details (file layout, library choice) —
     that belongs to `subpowers-plan`, not here.
   - If the goal and "done" state are already unambiguous, skip this step
     and go straight to Step 1.

## Step 1 — Write the spec

Present directly in chat (or as an ephemeral artifact for something visual,
e.g. a UI mockup). Nothing is written to disk at this stage — whether the
spec ends up in a repo file at all is Step 2's routing decision, made only
after sign-off, so a rejected spec never hits disk:

```markdown
# <Feature Name> Spec

**Goal:** One sentence — the primary objective.

**Acceptance Criteria:**
- [ ] Concrete, checkable condition that must hold for this to be "done"
- [ ] ...

**Data Models / State:**
- New or changed structures, fields, enums, or state transitions this
  feature requires — not exact file paths (that's `subpowers-plan`'s job to
  place), but the full contract for every new or changed type and
  method/function. Keep the signature and its description visually
  separate — a fenced code block for the signature, then prose below it —
  never inline a signature into a sentence.
- When a type already exists and the spec adds to it, show the **complete**
  type in the code block — every existing member plus the new one(s),
  marked so it's clear which is which — not just the delta. A reader
  shouldn't have to go check the current source to know the full shape of
  what they're building against; showing only the new method leaves them
  unable to tell how many methods it has or what else is already there.
  For example:

  ```python
  class RateLimiter:
      def __init__(self, limit: int, window_seconds: int): ...   # existing
      def check(self, key: str) -> bool: ...                     # existing
      def reset(self, key: str) -> None: ...                     # existing
      def retry_after(self, key: str) -> float: ...              # NEW
  ```
  `retry_after` returns the seconds until `key` would next pass `check`,
  or `0.0` if it would pass now.

  A signature is unambiguous in a way prose isn't; leaving it out just
  defers that ambiguity to `subpowers-plan` or implementation, where it's
  more expensive to resolve.
- Exception: for a large pre-existing type where most members are
  unrelated to this feature (e.g. a shared infrastructure class with
  dozens of methods), showing all of them would bury the new ones in noise
  — the opposite problem. There, show only the new/changed members, but
  say so explicitly (e.g. `# + 39 other existing methods, unrelated to
  this feature`) so it reads as a deliberate partial view instead of
  looking like the whole type.

**Flow Diagram:**
A Mermaid diagram of the feature's flow — as few nodes and edges as the
flow can be reduced to while staying accurate. Collapse steps that always
happen together into one node; drop nodes/edges that don't change the
outcome. If the flow is a straight line with no branches or actors worth
distinguishing, state that instead of drawing a diagram.

**Edge Cases:**
- Error conditions, unexpected inputs, empty/boundary states, and how each
  should behave.
```

## Step 2 — Sign-off and routing

Ask for a thumbs-up before routing onward. Do not let planning or
implementation start on the strength of your own spec.

**If the user rejects or requests changes:** revise the spec in place in
chat and ask again. Repeat until approved.

**Once approved, route by scope:**

- **Complex (multiple files/systems)** — **persist the spec, then** hand off
  to `subpowers-plan`, which turns these acceptance criteria into a
  file-by-file task checklist.

  Write `<plans dir>/<slug>.md`, where `<plans dir>` is the project
  contract's `## Plans` `dir` — `.claude/subpowers.md`, resolved per
  `subpowers-check`'s "The project contract"; default
  `docs/subpowers/plans/` when the repo has no contract. The file opens with
  the state-block frontmatter — schema per `subpowers-plan`'s "State block"
  section, with `status: planned`, `current_task: null`, `next_task: null` (no
  tasks exist yet), and today's date — followed by the signed-off spec verbatim
  under a `## Spec` heading. `subpowers-plan` appends Goal / Architecture /
  Tasks below it and takes over the frontmatter from there.

  That `## Spec` section **is** the record of decisions carried in from the
  spec conversation, and the thing implementation reads instead of
  re-litigating them. Nobody retypes spec content into the plan by hand, and
  nothing is lost when this conversation's context is.

  If the contract says `dir: none`, the spec stays in the conversation and
  gets handed to `subpowers-plan` inline — say so explicitly when handing off,
  because the handoff-record guarantee is then off.

- **Simple (1-2 files, clear purpose)** — skip planning; hand off directly
  to `subpowers-implement`, carrying the acceptance criteria forward as the
  definition of done for the TDD cycle. **Nothing goes to disk** — the work
  finishes inside this session, so a spec file would be pure overhead that
  outlives its own usefulness as a stale artifact.
