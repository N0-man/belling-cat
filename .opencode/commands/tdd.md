---
description: Test-driven development using tracer bullet approach
agent: build
subtask: true
---

Use the `/tdd` skill for test-driven development.

Core principles:
- Tests verify behavior through public interfaces, not implementation details
- ONE test at a time — tracer bullet approach (RED → GREEN → repeat)
- NO horizontal slicing — never write all tests first, then all code
- Only refactor after GREEN, never while RED

Workflow:
1. Plan: Confirm interface changes and which behaviors to test
2. Tracer bullet: Write ONE test → minimal code to pass
3. Incremental loop: For each remaining behavior, write next test → minimal code
4. Refactor: Extract duplication, deepen modules, apply SOLID (only after GREEN)

Read CONTEXT.md (if it exists) so test names match domain language.

$ARGUMENTS
