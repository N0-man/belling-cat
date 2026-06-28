---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification - "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" - treating RED as "write all tests" and GREEN as "write all code."

This produces **crap tests**:

- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes - they pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle. Because you just wrote the code, you know exactly what behavior matters and how to verify it.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## Workflow

### 1. Planning

When exploring the codebase, read `CONTEXT.md` (if it exists) so that test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

Before writing any code:

- [ ] Identify the behaviors to test (not implementation steps)
- [ ] Identify opportunities for deep modules (small interface, deep implementation) by reviewing existing module boundaries and keeping interfaces minimal

**If a backlog item was provided** (i.e., you were invoked from `/implement`): derive the interface and behaviors directly from the backlog item's acceptance criteria. Do not ask the user for confirmation unless it's ambiguous or incomplete — proceed to the Tracer Bullet step.

**If no backlog item was provided** (i.e., direct `/tdd` invocation): ask the user to confirm the interface and prioritize behaviors before proceeding:
- Confirm what interface changes are needed
- Confirm which behaviors to test (prioritize)
- Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors are most important to test?"

**testing scope** Focus testing effort on all critical paths, behaviors and various edge cases.

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet - proves the path works end-to-end.

### 3. Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior

### 4. Refactor

After all tests pass, refactor with two goals: clean code **and** correct layer placement.

**Layer placement (check first):**

Read `CONTEXT.md` and `docs/00-repo-structure.md` to confirm the expected layer boundaries for this project, then apply the Clean Architecture dependency rule: **dependencies must only point inward** — outer layers depend on inner layers, never the reverse.

The standard layers from innermost to outermost:

| Layer | Contains | Must not depend on |
|---|---|---|
| **Domain** | Entities, value objects, domain services, aggregates | Everything outside itself |
| **Application** | Use cases, application services, port interfaces | Infrastructure, delivery |
| **Adapters** | Concrete implementations of ports (LLM, DB, search, etc.) | Delivery layer |
| **Delivery** | Entry points (CLI, API, UI) — wiring and I/O formatting only | Nothing domain-internal |

For each piece of new code, ask:

- **Which layer does it belong in?** Business rules → domain. Orchestration → application. External I/O → adapter. Entry point → delivery.
- **Is the dependency rule satisfied?** If an inner layer imports from an outer layer, that is a violation — extract an interface (port) and invert the dependency.
- **Is domain logic pure?** Domain objects must have zero I/O, no framework imports, no LLM calls.
- **Are external concerns behind ports?** Any call to an LLM, database, file system, or network should cross an interface defined in the application layer and implemented in an adapter.
- **Is the delivery layer thin?** It should only wire components together and translate between user I/O and application layer calls — no business logic.

**Then apply standard refactors:**

- [ ] Extract duplication
- [ ] Deepen modules — small interface, deep implementation
- [ ] Apply SOLID principles where natural
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```
