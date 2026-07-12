---
description: Validate an active story or exact committed range against intent, review, traceability, and preflight gates
agent: build
---

Use the `validate-change` skill.

With an active story, resolve the exact range and intent packet from the tracker and handoff. Without one, require an explicit base/range and intent or specification; never guess the fixed point.

Default mode is read-only. Pass `--repair` only when the user wants safe, in-intent repairs committed. Findings that change product intent, contracts, scope, dependencies, or material architecture must be escalated to the user.

Arguments: optional exact base/range, intent/specification path, and `--repair`.

$ARGUMENTS
