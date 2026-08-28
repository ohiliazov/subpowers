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
by area. `subpowers-implement`'s self-review applies this section verbatim, so
this is the single copy.

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
