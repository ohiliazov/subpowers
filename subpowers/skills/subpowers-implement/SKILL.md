---
name: subpowers-implement
description: >
  Invoke ONLY for minor, precise alterations (1-2 files, purpose absolute). 
  Ambiguity or vast scope demands `subpowers-spec` or `subpowers-plan`. 
  Unknown anomalies demand `subpowers-debug`. For read-only discovery, 
  use `subpowers-explore`. Triggers: "add", "build", "implement", "fix".
---

# Ritual: Implement

<directives>
You are invoked to enact swift, localized change. Do not conjure vast architecture here. This ritual is for precise, known, and highly scoped execution.
</directives>

## I. The Scope Gate

Do not invoke heavy ceremony for microscopic fixes, but do not bypass the ceremony if the scope bleeds beyond your
control.

* **The Ledger Check:** If this work is bound to an existing plan (found in `.claude/subpowers.md`), read the
  frontmatter first. Your entry point is `next_task`. Do not re-verify the past.
* **The Scale Test:**
    * *Is the goal cloudy?* Halt. Invoke `subpowers-spec`.
    * *Does it span multiple systems?* Halt. Invoke `subpowers-plan`.
    * *Is it strictly contained (1-2 files)?* Proceed directly to The Trial of TDD.

## II. The Trial of TDD

Execute this cycle relentlessly per task. Mimic the surrounding test architecture.

* **Blood (RED):** Write the smallest test. Run `test-one`. Confirm it shatters correctly.
* **Life (GREEN):** Write the absolute minimum syntax to pass. Ensure no neighboring tests fracture.
* **Purity (REFACTOR):** Cleanse names. Obliterate duplication. Remain green.
* **The Red Clause:** If the ledger dictates `suite_expected: red`, you are inside a fractured phase. You must only
  ensure your specific slice is green.

## III. The Inquisition (Self-Review)

Before you declare victory, you must judge your own creation against these absolute standards:

* **Correctness:** Are edge cases (`null`, zero, overflow) handled? Are async operations awaited? Is the logic immune to
  injection?
* **Simplicity:** Does any function serve two masters? Is any logic copy-pasted? Purge dead code. If a new abstraction
  is used in fewer than 2 places, obliterate it.
* **Consistency:** Check the `## Project rules`. If you fixed consistency in one location but left an adjacent,
  identical location untouched, you have created a fresh bug. Fix it.
* **The Out-of-Band Cry:** Check `## Reindex / regeneration triggers`. If your syntax demands a cache flush or search
  reindex, announce it out-of-band.

## IV. The Final Seal

* Invoke the verification commands required by `subpowers-check`.
* Execute them physically. Read the output.
* Fix any anomaly you introduced.
* You are absolutely forbidden from declaring the task "done" until the terminal proves your victory.