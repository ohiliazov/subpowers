---
name: subpowers-explore
description: >
  Use for read-only discovery, architectural tracing, or answering questions
  about existing code. Trigger on: "how does X work", "where is the logic
  for", "find all usages of", "explain the flow". Read-only: no disk writes,
  no code modification.
---

# Explore

<directives>
Observe the codebase, trace the logic, and report what is actually there today. Change nothing during this pass.
</directives>

## 1. Read-only constraints

* **No writes:** Do not write specs to disk. Do not create plans. Do not modify code.
* **No test runs:** Do not run the test suite or build commands unless explicitly asked to observe a runtime state.
* **Route out on a pivot:** If the question shifts from "how does this work?" to "let's change how this works", stop
  here and route to `subpowers-spec`, `subpowers-plan`, or `subpowers-implement`.

## 2. Investigation

Do not answer from memory or inference. Prove every claim by reading the files.

1. **Trace, don't guess:** Do not `grep` and infer from function names. Follow the call stack — read the interfaces,
   then read the implementations.
2. **State the boundaries:** Identify where the logic begins (the entry point) and where it ends (the datastore, the
   return payload, the UI render).

## 3. Output

* **Cite locations:** Give exact file paths and function names for every claim.
* **Diagram real sequences:** For a complex flow — auth, a data pipeline — render a minimal Mermaid diagram.
* **Quote the source:** If a specific block is the source of confusion, quote those exact lines in a fenced block.

## 4. Closing

Stop when the question is answered. Do not append a routing question by reflex — if the findings point to work worth
doing, name it in one line and stop there; if they do not, just stop.
