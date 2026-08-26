---
name: subpowers-review
description: >
  Use before finishing significant work — scans the diff for correctness bugs,
  simplifications, and violations of this project's own conventions. Optional
  for one-liners. Trigger on: "review", "check my code", "before committing",
  "before PR", "looks good?".
---

# Review

## How to use

Read `git diff HEAD` (or `git diff main..HEAD` for a branch).
Work through the checklist. Report findings by severity.

**If the diff belongs to a plan** (the project contract's `## Plans` `dir`),
read that plan's frontmatter and `## Corrections` section first — per
`subpowers-plan`'s "State block" section. Don't raise a finding over something
already recorded there as a deliberate decision (a `[~]` deferred item, a
documented reslice); that's not a defect this diff introduced. Do raise one if
the diff contradicts what the frontmatter or `## Corrections` say should be
true — that's a real defect the plan's own record makes cheap to catch.

## Checklist

### Correctness
- [ ] Edge cases: empty list, None/null, zero, negative, overflow?
- [ ] Async operations properly awaited?
- [ ] Off-by-one in loops or date ranges?
- [ ] Error paths handled or explicitly ignored?
- [ ] No SQL injection, XSS, or command injection?

### Simplicity
- [ ] Any function doing two distinct things? Flag it.
- [ ] Any logic block copy-pasted? Flag it.
- [ ] Any dead code added? Delete it.
- [ ] Any new abstraction that isn't used in at least 2 places? Remove it.

### Project specifics
Apply the project contract's `## Project rules` section to the diff —
`.claude/subpowers.md`, resolved per `subpowers-check`'s "The project contract".
That file owns the single condensed copy of this project's conventions; don't
keep a second one here and don't invent rules it doesn't state.

Its Consistency item reads as a build-time question ("did you check sibling
spots?") — read it here as a diff-audit one instead: does the diff make one spot
consistent while leaving an adjacent, equally-applicable spot untouched? That's
a fresh bug, not a partial fix.

Also check the contract's `## Reindex / regeneration triggers`: if the diff
touches one of those, the out-of-band step has to be announced, and a diff that
silently skips it is an Important finding.

**No contract in this repo?** Read `CLAUDE.md`/`AGENTS.md` (or the project's
style guide) directly for this pass, and say in your report that you reviewed
against that instead — so nobody reads a clean result as "the project's rules
were checked" when there was no checkable list.

## Output format

```
Critical  — would crash or corrupt data; fix before committing
Important — correctness issue or violated project rule; fix before PR
Minor     — simplification or style; note for later
```

Skip severity levels with no findings. Zero findings is a valid result — say so.
