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
Observe the codebase, trace the logic, and report what is actually there today. Change nothing during this pass. Look, but do not touch.
</directives>

## I. The Vow of Stasis

* **No Creation:** Do not write specs to disk. Do not create plans. Do not modify code.
* **No Testing:** Do not run the test suite or build commands unless explicitly asked to observe a runtime state.
* **The Pivot:** If the inquiry shifts from "how does this work?" to "let's change how this works", halt this skill
  immediately and route to `subpowers-spec`, `subpowers-plan`, or `subpowers-implement`.

## II. The Scrying (Investigation)

Do not answer from memory or inference. Prove every claim by reading the files.

1. **Deep Tracing:** Do not `grep` and guess from function names. Follow the call stack — read the interfaces, then read
   the implementations.
2. **State the Boundaries:** Identify where the logic begins (the entry point) and where it ends (the datastore, the
   return payload, the UI render).

## III. The Revelation (Output)

* **The Map:** Cite exact file paths and function names for every claim.
* **The Flow:** For a complex sequence — an auth flow, a data pipeline — render a minimal Mermaid diagram.
* **The Verbatim Truth:** If a specific block is the source of confusion, quote those exact lines in a fenced block.

## IV. The Yield

End by asking whether the inquiry is answered, or whether changing this architecture should now route to
`subpowers-spec`, `subpowers-plan`, or `subpowers-implement`.
