---
name: subpowers-design
description: >
  Use for visual design on a canvas: a new page, a redesign, options for a
  component or an icon, or a round of canvas comments. Runs page layout MVP →
  components → page layout finalization; every board is created, selected,
  rejected or approved, and a finished canvas holds approved boards only.
  Trigger on: "design", "redesign", "draw options", "mockup", "canvas",
  "board", "/design". The what and why of a feature, and backend design,
  route to `subpowers-spec`; building an approved design routes to
  `subpowers-plan` or `subpowers-implement`.
---

# Design

<directives>
A canvas records decisions; it is not a scrapbook. Every board has exactly one state, and a finished canvas holds only approved boards. Design the page, never a component alone. Primitives come from the primitives table and icons from the icons board first; a missing one is announced in chat and on the canvas.
</directives>

## 1. Ground the round

* **Contract:** Read `.claude/subpowers.md`'s `## Design` section: `source:` (where each page's canvas lives),
  `preferences:` (the owner's confirmed taste), `decisions:` (where a page's decisions are recorded), `primitives:` (the
  table of shared components), `icons:` (the shared icons board) and `labels:` (badge text per state). With no contract, find them in the repo, state
  them, and get them confirmed once before the first round.
* **Read before drawing:** the preferences file in full, the page's decisions record, the canvas's current boards, and
  every open comment thread on it. All comments first, then the work.
* **User first:** Write down who opens the page, what they want to learn there, and in what order. Every block answers
  one item on that list. The data the backend happens to have, or the shape it arrives in (laps, splits, files, calendar
  weeks), is never the starting point.
* **Grill the idea:** Unless a signed-off spec already covers it, grill it with `subpowers-spec` Step 2 before the
  first board. The goal it settles is the yardstick the finished page is judged by.
* **Real data:** Draw on the owner's real data, read through the contract's `## Inspect` commands. Placeholder data
  hides the layout problems real values cause.

## 2. Canvas structure

* **One page, one canvas.** Everything designed for a page lives on that page's canvas. A component never gets a canvas
  of its own; the only shared canvas is the icons board. Primitives are a table, and a table never goes on a canvas.
* **Areas:** a page canvas has the page layout (desktop and phone), approved components grouped together, and a work
  area holding the current round and the board it builds on. Sticky notes explain each round.
* **A board is a pair:** a desktop board and its phone board share one name, one state and one badge.
* **Never overwrite:** a new iteration is a new board with its own numbered name beside the one it builds on, never an
  edit over it. A new round runs across the previous round's direction: a round laid out top to bottom gets its next
  round in a row to the right of the selected board, and a row gets its next round in a column under it. The one board
  edited in place is the approved page layout, filled with each component as it is approved.
* **The repo copy is the source of truth:** export the canvas to the repository in the same change that creates or
  updates it. When a published canvas link does not open, publish the repo copy at once and continue there.

## 3. Board lifecycle

| State | Badge | Set by | On the canvas |
|-------|-------|--------|---------------|
| created | pending | drawing it | sits in the work area beside the board it builds on |
| selected | best, not approved | the owner picking it for more work | its round's other boards and the unapproved board it built on are deleted; it stays as the reference for the next round |
| rejected | none | the owner turning it down, or any hesitant comment | deleted in the same change |
| approved | approved | the owner's explicit approval only | moves to the approved area; every other unapproved board answering the same question is deleted; the page layout is filled with it in the same change |

* **A pick is not an approval.** "Go with C", "B is better", "best of these" select a board. Only an explicit approval
  approves it. Any hesitant comment is a no.
* **Harvest before deleting:** what the owner liked in a board about to be deleted is written into the page's
  decisions record as a carried detail, in the same change. Deleting a board never loses a liked part.
* **Threads first:** a board is deleted only after every thread on it has a reply. Threads stay open; the owner
  resolves them.
* **One approved page layout.** Two approved layout pairs coexist only during finalization's micro-adjustments, until
  the owner approves one of them.
* **Badges everywhere:** every board carries its state badge in the contract's `labels:` text, updated in the same
  change as the state.

## 4. Primitives and icons

* **What a primitive is:** a reusable component that more than one board builds on (a marker, a pill, a band, a row),
  with one target file in code. The primitives table has one row per file: what it is, the page canvases that draw it,
  notes. It lives in a file made for tables (Markdown, CSV), never on a canvas: a table on a canvas is a misuse of the
  tool. Rendered copies stay on the page canvases the table names.
* **Look there first:** before drawing any element, find it in the primitives table and copy its rendered markup from a
  canvas the table names, or convert it from its code file when no canvas draws it; before drawing any icon, look on
  the icons board. Reuse it exactly (same paths, tokens, sizes), copying everything it depends on (hidden definitions,
  colour classes), and render it once before showing it.
* **Missing primitive:** draw it on the board that needs it, put a warning on that board naming the missing primitive,
  and say so in chat in the same message that links the board. Both, every time.
* **Missing icon:** the same, with the warning on the icons canvas as well as on the board that needs it. A new icon is
  derived from the closest approved icon family, never drawn from nothing.
* **Recorded on approval:** when the board that introduced a primitive is approved, its row goes into the primitives
  table in the same change, named by its target in code with the canvas that draws it; an approved icon is copied onto
  the icons board. Its warnings are removed. The table and the icons board hold approved items only.

## 5. Phases

A page moves through three phases in order. A phase is finished only when its exit holds.

### 5.1 Page layout MVP

* The general layout and the basic idea of each block's data representation: which block answers which question, its
  width and its place on desktop and phone. No concrete visuals, animation, units or data detail yet.
* Where a block repeats for several items (days, sports, legs), one skeleton is designed first: its parts, which part
  applies to which item and why, and its desktop and phone layout. Every item fills the same skeleton.
* 2–4 layouts, at least one unexpected: a different form, model or interaction, not a variation.
* **Exit:** one approved layout pair.

### 5.2 Components

* Each block of the approved layout gets its concrete form, unless the owner explicitly approved that block as it
  stands.
* **Reasons before drawing:** for every option write down the question it answers, the unit it judges by, and why that
  unit is the reader's own. An option without its reasons is not drawn.
* 3–4 options on real data, at least one unexpected. Each is drawn twice: alone, and in place in the assembled page at
  its real width, desktop and phone, next to the blocks approved so far.
* **Sibling audit before showing:** same parts, same form, same width as its siblings; no number repeated elsewhere on
  the page; one signature visual per page, the other blocks in the form native to their data. The round's notes state
  the audit's result.
* **Exit:** every block approved and already filled into the page layout.

### 5.3 Page layout finalization

* The assembled page is judged as a whole at desktop and phone width: proportions, repeated numbers, consistency across
  repeated items, every state the page can be in. Interactions are built as working interactive boards, not described.
* Micro-adjustments are drawn as variants of the approved layout; the approved one stays, the rest are deleted.
* **Exit, the design is finished:** the canvas holds only approved boards: the page layout pair and its approved
  components. No pending or selected board, no warning, no open question.

## 6. Running a round

* **Self-regulate:** keep your own worklist in the session scratchpad and run the round end to end. No plan file, no
  sign-off, no "is it ready?" question. Plans are the owner's.
* **Comments as a batch:** assess a round's comments together, against the page's job, never one by one. A complaint
  about an element is about its existence or job first and its style last. A liked detail is one ingredient, not the
  new concept for every block. A comment on one item is applied to every sibling it holds for, in the same round.
* **Picks and approvals come from the canvas,** or from the owner's own words in chat. Never put a design pick to the
  owner as a terminal question.
* **Novelty:** every round carries at least one approach that breaks your habits. Reaching for the form you used last
  time is the habit.
* **Show, don't tell:** an idea worth proposing is drawn. Answer a design question with a board, not a paragraph.
* **Build only what was agreed:** once a block is approved, a tweak is allowed only when it improves the block without
  changing its idea. A new block, number, unit or view is proposed in chat first and drawn only after the owner agrees.
* **Look before publishing:** render every changed board at its real width and look at it, then check it against the
  preferences file. The round's message names the rules it was checked against.
* **Follow-ups:** when a block is approved, every board that embeds the block it replaces is updated in the same
  change. A defect that already has a design answer is fixed without asking.
* **Taste goes home:** a preference the owner confirms goes into the preferences file; a page's decisions go into its
  decisions record. Neither lives only in the canvas or in memory.
* **Link it:** every message that shows or changes a canvas carries its link. Never link a canvas the turn did not
  touch.

## 7. Routing

* **Finished:** route to `subpowers-plan` with the approved boards as the plan's design, or to `subpowers-implement` for
  a change of 1–2 files. The design is built from its own markup, as drawn.
* **Built:** `subpowers-check` compares the result with the approved boards side by side and judges it on real data
  against the goal from §1. A gap goes back into a round on the same canvas.
