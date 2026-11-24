---
name: subpowers-spec
description: >
  Use when a message brings a new idea, the goal is unclear, or business logic
  must be defined before any file is changed. Grills the idea in rounds of at
  most 3 yes-default questions until nothing is left open. Trigger on: a new
  idea, "grill", "design a feature", "write a spec", "define requirements".
  Produces the "what" and "why", not the "how". If the user is only asking how
  existing code works without requesting a change, DO NOT invoke this — route
  to `subpowers-explore` instead.
---

# Spec

<directives>
Establish the "what" and the "why" before a single file is touched. Do not decide the "how" — file paths, functions, tasks. Grill every new idea until no decision is left open. Do not guess; define.
</directives>

## 1. Ground the spec

* **Read the codebase first:** Read the existing models, schemas, and adjacent features — the spans that matter
  (`offset`/`limit`), not whole files. The spec must fit the reality of this codebase, not a generic guess.
* **Find the design:** If a design covers this work — named in the contract's `## Design` section, linked by the
  user, or attached to the conversation — read it before writing anything. It is the spec for whatever it shows:
  derive the acceptance criteria from it, not from memory or taste. Anything the work needs that the design does not
  show (a state, a screen, a breakpoint, a field) goes under **Additions to the design**, and each one is settled with
  the user — drawn into the design first, or explicitly approved — before sign-off. Never fill a gap yourself.

## 2. Grill the idea

A new idea is a change to what something does or shows, or to an agreed design, decision or rule. Every one is grilled
before work starts. A direct question, a bug report, or a clear change whose purpose is settled is not.

1. **Map the design tree:** Every decision branches into the decisions that hang off it. The frontier is every
   decision whose prerequisites are settled: the questions you can ask now without guessing answers not yet heard.
2. **Ask in rounds:** At most 3 frontier questions a round, ranked by how many later decisions each unblocks; the
   rest wait for the next round. A question that depends on one still open belongs to a later round. Wait for the
   answers, then recompute the frontier.
3. **Open with the approach:** Round 1, Q1 is how to approach the idea. Ground it in what the idea means to the
   people who use the product: what they come for, what they already get elsewhere in it, what it changes for them.
   A good idea is made better; a weak one is explained (what it costs, what it breaks) and replaced. Offer the
   recommended approach, two alternatives and one unexpected (a different form, model or interaction, not a
   variation). Approaches to the given idea only, never extra features.
4. **Make "yes" the answer:** Word each question so "yes" accepts the recommendation. "yes" alone accepts the whole
   round; "Qn: …" overrides one. Do not ask about file layouts or library choices; those belong to `subpowers-plan`.
5. **Find facts yourself:** Facts come from the codebase and tools, never from the user. Look them up yourself. A
   sweep over many files goes to a sub-agent on a cheap model (Claude Code: `Agent` with `model: "sonnet"`; Codex:
   `spawn_agent` with `gpt-6-luna`) that returns `file:line` citations, not contents; reread the load-bearing spans
   before relying on them. A running lookup holds back only the questions downstream of it.
6. **Keep the tree on disk:** Track settled answers and the open frontier in a file in the session scratchpad.
   Update it after every answer and reread it before every round, so context compaction loses nothing. Nothing of it
   reaches the repository before sign-off.
7. **When no one can answer:** In an unattended or overnight run, take each recommended answer, mark it
   `assumed (unattended)` in the tree, and list every assumed answer under **Assumed** in the spec.
8. **Stop when the frontier is empty:** Every branch visited, nothing silently assumed. The chosen approach's goal is
   the yardstick the built result is reassessed against.

Format a round like so:

```markdown
❓ **Q1** - **<question title>**: <question body, as long as it needs, including the choices>

➡️ <recommended answer>

---

❓ **Q2** - **<question title>**: <question body>

➡️ <recommended answer>
```

## 3. Write the spec

Present it directly in the chat. **Write nothing to disk at this stage.** A rejected spec must never reach the file
system.

```markdown
# <Feature Name> Spec

**Goal:** <One sentence — the defining objective.>
**Approaches:** <The chosen one and why; the others considered, one line each.>
**Assumed:** <Each answer taken unattended under §2, for the user to confirm — omit if none.>

**Design:** <Source and version, and which part covers which criterion — or "none".>
**Additions to the design:** <Each gap, and how the user settled it — omit if none.>

**Acceptance Criteria:**

- [ ] <Concrete, checkable condition>
- [ ] ...

**Data Models / State:**
<The full contract for every new or changed type.>
```

### Showing signatures

When altering an existing type, show the **entire type** in a fenced code block, explicitly marking what is new. Do not
show only the delta. The reader must never need to search the codebase to understand the final shape.

```python
class RateLimiter:
    def __init__(self, limit: int, window_seconds: int): ...  # existing

    def check(self, key: str) -> bool: ...  # existing

    def retry_after(self, key: str) -> float: ...  # NEW
```

*(Exception: if the type is very large, show the new members and state `# + X other existing methods, unrelated` so the
partial view reads as deliberate.)*

### Flow and edge cases

* **Flow diagram:** Render a minimal Mermaid diagram. Collapse redundant nodes. If the flow is a straight line, say so
  instead of drawing a useless diagram.
* **Edge cases:** Define error conditions, empty and boundary states, and the exact expected behavior of each.

## 4. Sign-off

Present the spec and require explicit approval. Do not route to planning or implementation on the strength of your own
spec. If it is rejected, revise it in the chat and ask again.

## 5. Routing

Once the spec is approved, route it by scope:

* **Needs drawing first (a page or a component with no approved design):** route to `subpowers-design`, carrying the
  spec's goal as its yardstick. Once the design is finished it routes on to plan or implement, below.
* **Complex (multiple files or systems):**
    1. Write the spec to `<plans_dir>/<slug>.md` — the directory named by `.claude/subpowers.md`'s `## Plans` section,
       defaulting to `docs/subpowers/plans/`.
    2. Write the frontmatter required by `subpowers-plan`'s state block (`status: planned`, `current_task: null`,
       `next_task: null`, today's date).
    3. Place the approved text under a `## Spec` heading. That section is the record of decisions carried in from this
       conversation — what implementation reads instead of re-litigating them.
    4. Route to `subpowers-plan`.
* **Simple (1-2 files):**
    1. **Write nothing to disk.** The spec is ephemeral; a file would outlive its usefulness as a stale artifact.
    2. Carry the acceptance criteria forward and route to `subpowers-implement`.
