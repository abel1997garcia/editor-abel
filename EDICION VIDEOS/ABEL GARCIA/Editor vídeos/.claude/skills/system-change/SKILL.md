---
name: system-change
description: Rewrite a changed reusable system into its simplest equivalent form and keep its active callers consistent. Use when the user asks to change, replace, redesign, or permanently improve a recurring workflow, skill, SOP, integration, automation, source of truth, schema, prompt, or operating rule. Do not use for ordinary execution, one-record edits, supported parameter choices, or fixes that only restore the existing contract.
---

# System Change

## Scope

- If the user explicitly makes the change future/routine, it is permanent. If they explicitly limit it to this case, it is one-off.
- If duration is ambiguous, ask: `¿Quieres que esto sustituya al sistema habitual y actualice todo el contexto, o es una excepción puntual para esta tarea?`
- A reviewer, failure, or successful experiment may propose a permanent change but cannot authorize one.

For a one-off, leave the durable system unchanged. Use the smallest task-local override; persist it only if resuming requires it, with an exit condition; validate and clean it up.

## Permanent Change

1. Implement the requested behavior by rewriting the complete active system—canonical implementation, instructions, and callers—into the smallest version that preserves its required output and non-negotiable safety, privacy, and authorization constraints. Delete or merge anything whose removal changes neither; replace old rules instead of appending feedback, and prefer tests or code when they express a repeated guard more simply than prose.
2. Validate the output and constraints with appropriate tests, dry-runs, or readbacks and remove competing active instructions. Leave clear history historical.
3. Spawn one fresh independent reviewer with only the output, constraints, rewritten system, and validation evidence. It must try to make the system smaller and return `PASS` or an equivalent version created only by deleting, merging, or shortening. It may not add requirements, edge cases, features, explanations, agents, or review rounds. Apply valid reductions and revalidate once; do not spawn a resolver or another reviewer.

Complete only when validation passes and every reviewer-proven reduction has been applied.
