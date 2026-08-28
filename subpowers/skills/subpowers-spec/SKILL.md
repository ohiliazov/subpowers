---
name: subpowers-spec
description: >
  Use when the goal is unclear, or business logic must be defined before any
  file is changed. Trigger on: "design a feature", "write a spec", "define
  requirements". Produces the "what" and "why", not the "how". If the user is
  only asking how existing code works without requesting a change, DO NOT
  invoke this — route to `subpowers-explore` instead.
---

# Spec

<directives>
Establish the "what" and the "why" before a single file is touched. Do not decide the "how" — file paths, functions, tasks. Lock in the business logic. Do not guess; define.
</directives>

## 1. Ground the spec

* **Read the codebase first:** Read the existing models, schemas, and adjacent features. The spec must fit the reality
  of this codebase, not a generic guess.
* **Batch your questions:** If requirements are ambiguous, resolve them in one round — up to 3 targeted,
  multiple-choice or yes/no questions in a single tool call. Do not ask about file layouts or library choices; those
  belong to `subpowers-plan`.

## 2. Write the spec

Present it directly in the chat. **Write nothing to disk at this stage.** A rejected spec must never reach the file
system.

```markdown
# <Feature Name> Spec

**Goal:** <One sentence — the defining objective.>

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

## 3. Sign-off

Present the spec and require explicit approval. Do not route to planning or implementation on the strength of your own
spec. If it is rejected, revise it in the chat and ask again.

## 4. Routing

Once the spec is approved, route it by scope:

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
