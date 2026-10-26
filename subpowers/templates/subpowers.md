# Subpowers contract

<!--
Copy this file to `.claude/subpowers.md` in a project root and fill it in.
The subpowers-* skills read it instead of hardcoding any stack. Every command
below is run verbatim, so paste commands you have actually run in this repo.
Delete any section that doesn't apply — an absent section is handled; a wrong
command is not.
-->

## Commands

Run from the repo root unless the command itself cds.

If this repo has a canonical dev-ops entry point — a `Makefile`, a `justfile`, a
`scripts/` wrapper — point every row at that instead of at raw `docker`/`curl`/
`psql` invocations, and add a missing subcommand there rather than pasting a raw
command here. A wrapper follows the repo when ports, container names, or auth
change; a raw command pasted into this file silently goes stale.

| Key | Command | Notes |
|-----|---------|-------|
| `test` | `<full test suite>` | The bar for "tests pass" |
| `test-one` | `<single test, with a placeholder>` | Used in the TDD red step |
| `typecheck` | `<static type check>` | Omit the row if the stack has none |
| `lint` | `<linter/formatter check>` | |
| `build` | `<production build>` | |
| `run` | `<start the app locally>` | |

Add a row for any check that is **load-bearing but not implied** by the others —
a build step that catches what the typechecker can't, a migration check, a
codegen freshness check. If a claim can only be verified by that command, it
belongs here, with a note saying which claim it backs.

## Gates

Commands the plugin's Stop hook runs before a turn may end, one backticked
command per bullet, run from the repo root in order. They run only when the
working tree's content differs from the last green run, so keep them to checks
that are fast enough to run on every changed turn. A failing gate blocks the
turn with the command's last 40 lines, once per tree state: stopping again on
the same failing tree is allowed with a warning. The hook times out after 600 s.
Gitignore `.claude/.gate-green` and `.claude/.gate-red`, where the hook keeps
its state. Replace the placeholder below; an unfilled `<...>` bullet is skipped.

- `<lint command>`

## Inspect

Direct, read-only ways to confirm real state in this project — preferred over
clicking through a UI or guessing. Fill in the ones that exist here.

```bash
# HTTP API — confirm a request/response shape or a computed value
# Datastore — confirm rows/columns/keys (read-only; schema changes go through migrations)
# Cache — confirm a key or its TTL
# Search index / queue / other backing service
# Logs
```

## Plans

- `dir:` `docs/subpowers/plans/`
- `archive:` `docs/subpowers/plans/archive/YYYY-MM-DD-<slug>/`

Where `subpowers-plan` writes plan files and where it moves them once complete.
If this project does not want plan files on disk, say so here instead:
`dir: none` — plans then stay in the conversation and `subpowers-plan`'s
handoff-record guarantee is off.

## Design

- `source:` `<link or path: a Figma file, a design canvas, mockups under docs/design/>`
- `covers:` `<which pages, screens or components it defines, and at which widths>`

Designs listed here are binding specs, not inspiration. The skills read the
relevant part before touching anything it covers, build it as drawn (structure,
styles, copy, order), and ask before any deviation. Delete this section if the
project has no designs.

## Evidence

Extra claim → evidence rows specific to this project, appended to
`subpowers-check`'s table. One row per claim that a passing test suite does
*not* actually establish here.

| Claim | Required |
|-------|----------|
| | |

## Project rules

The condensed, checkable form of this project's own conventions — whatever
`CLAUDE.md`/`AGENTS.md`/the style guide says that a reviewer would flag. Group
by area. `subpowers-implement`'s self-review applies this section verbatim.

When the rule already lives in a file the agent reads anyway, point at it
instead of copying it: a line `See <file> §<heading>` stands for that whole
section, read in full wherever this section is applied. A copy drifts from its
source; a reference cannot. Keep checklist items here only for rules that have
no other home.

- See `CLAUDE.md` §Rules

### Consistency

- [ ] Checked sibling components/modules for the same category of issue — not
      just the specific spot pointed at — before calling it done? A pattern
      that holds in one place holds everywhere it logically applies.

### <Area, e.g. Frontend>

- [ ] ...

### <Area, e.g. Backend>

- [ ] ...

## Reindex / regeneration triggers

Changes that require an out-of-band step someone must be told about — a search
reindex, a cache flush, a client regeneration, a data backfill. Name the
trigger and the step.

- Changed `<function/schema/mapping>` → `<step to announce>`
