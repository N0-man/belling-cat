---
description: Implement a single backlog item using TDD and self-review
agent: build
---

Run the `/check-handoff` skill first.

Implement a single backlog item using test-driven development and self-review.

Process:

1. Read the backlog item (passed as argument) and the PRD
2. Use `/tdd` skill — one test → minimal code → pass → next test
3. Run typechecking regularly, single test files during loop, full suite at end
4. Self-review with `/review` when done
5. Run `/preflight` — do not commit until it passes
6. Commit to current branch

TDD discipline:

- Tests verify behavior through public interfaces, not implementation
- One test at a time — tracer bullet approach
- No speculative features added
- Refactor only after GREEN, never while RED

Arguments: path to backlog item file (e.g., .scratch/nlq-agent/backlog/01-<slug>.md)

$ARGUMENTS
