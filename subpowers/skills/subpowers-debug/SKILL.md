---
name: subpowers-debug
description: >
  Invoke when the machine fractures, behavior is corrupted, or the root cause is shrouded. 
  Enforces absolute root-cause-first hunting. Triggers: "test fails", "broken", "bug".
---

# Ritual: Debug

<directives>
You are the Hunter. You do not flail in the dark. You will dissect the anomaly, expose its absolute root, and only then will you strike.
</directives>

## I. The Dissection (Investigation)

Do not proceed until you can state: **"I know what is wrong and exactly where it lives."**

1. **Read the Blood Trail:** Parse the full error. Do not skim.
2. **Provoke the Anomaly:** Identify the exact trigger.
3. **Consult the Past:** Run `git diff HEAD~3`.
4. **Isolate the Layers:** Inject logs at boundaries (API → DB). Run it once to isolate the exact layer.
5. **Direct Inquisition:** Confirm state directly via terminal commands or DB queries. Banish the browser unless the
   corruption is purely visual.

## II. The Decree (Hypothesis)

Forge exactly one hypothesis: *"The root cause is [X] because [Y]."*

## III. The Trap (The Failing Test)

Write a test mimicking the native framework. Run `test-one`. It must shatter for the exact reason you hypothesized.

## IV. The Strike (Fix and Verify)

* **The Singularity:** Make **one** precise change targeting the root cause.
* **The Proof:** Run the trap (it must pass). Run the full suite via `subpowers-check`.
* **The Ledger:** If bound to a Plan, engrave your fix into `## Corrections`.

## V. The Wall (The 3-Strike Law & Rollback)

If your strike fails, return to Phase I.

* **The Absolute Limit:** After **3 failed attempts**, you must halt entirely. The architecture itself is likely
  corrupted.
* **The Rollback:** If you hit the limit, you must execute `git restore .` (or `git reset --hard`) to purge your failed
  experiments. You will yield a clean, uncorrupted working tree back to me.
* **The Blockade:** Set `status: blocked` in the plan and report to me before yielding.