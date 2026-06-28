---
description: Two-axis review (Standards + Spec) since a fixed point
agent: build
subtask: true
---

Use the `/review` skill to review changes since a fixed point (commit, branch, or tag).

Two parallel sub-agents report separately:

- **Standards** — does the code follow documented coding standards?
- **Spec** — does the code match the originating issue/PRD?

A change can pass one axis and fail the other — they are deliberately separate.

Arguments: <fixed-point> (e.g., main, HEAD~5, commit SHA)

$ARGUMENTS
