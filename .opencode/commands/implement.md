---
description: Implement a single backlog item using TDD and self-review
agent: build
---

Implement a single backlog item using test-driven development and self-review.

**Resolving the target item:**

- **Argument provided:** Use the specified backlog item. Check its `Blocked by:` field — if any listed item is not `done`, tell the user which blocker must be implemented first and stop.
- **No argument:** Scan the backlog and pick the lowest-numbered item whose `Status:` is `to-do` or `doing` and whose `Blocked by:` dependencies are all `done`. If no such item exists, report the blockers and stop.

Do not ask the user to choose once the item is resolved.

Process:

1. Read the backlog item and the PRD
2. Run `/handoff` once to bootstrap the handoff file for this item before writing any code
3. Use `/tdd` skill — one test → minimal code → pass → next test; after each GREEN cycle append a one-line log entry to `.scratch/handoff-context.md` under a `## TDD Log` section (format: `- [<timestamp>] GREEN: <test name or behaviour confirmed>`) — do not regenerate the file
4. Run typechecking regularly, single test files during loop, full suite at end
5. Self-review with `/review` — use `main` as the fixed point (or `HEAD~1` if on main)
6. Run `/preflight` — do not commit until it passes
7. Commit to current branch

TDD discipline:

- Tests verify behavior through public interfaces, not implementation
- One test at a time — tracer bullet approach
- No speculative features added
- Refactor only after GREEN, never while RED

Arguments: path to backlog item file (e.g., .scratch/<feature-name>/backlog/01-<slug>.md)

$ARGUMENTS
