---
description: Three-axis review (Standards + Spec + Architecture) since a fixed point
agent: build
subtask: true
---

Use the `/review` skill to review changes since a fixed point (commit, branch, or tag).

Three parallel sub-agents report separately:

- **Standards** — does the code follow documented coding standards?
- **Spec** — does the code match the originating issue/PRD?
- **Architecture** — does the code respect the domain model, DDD layer boundaries, and ADRs?

A change can pass one axis and fail the others — they are deliberately separate.

Arguments: <fixed-point> (e.g., main, HEAD~5, commit SHA)

$ARGUMENTS
