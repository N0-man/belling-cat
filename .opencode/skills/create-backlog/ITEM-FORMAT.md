# Story file format

```md
---
id: ITEM-01
requirements:
  - REQ-001
decisions:
  - DD-001
  - ADR-0001
prd: .scratch/<increment>/PRD.md
---

# ITEM-01: <Title>

## Intent

What the user or stakeholder set out to accomplish, in outcome terms. Preserve relevant deliberate constraints and trade-offs; do not describe only files or implementation tasks.

## Outcome

The observable result this story contributes.

## Value and showcase

Who benefits, why this matters now, and what can be demonstrated when complete.

## Deliberate constraints and exclusions

Accepted constraints, ruled-out approaches, and explicit out-of-scope matters relevant to this story. Link decision records instead of copying their full rationale.

## Scope

### Included

### Excluded

## Acceptance criteria

- [ ] AC-01: <Observable criterion>
- [ ] AC-02: <Failure or edge criterion>

## Test and demonstration evidence

Tests, commands, screenshots, reports, or observable behaviour required to call the story done.

## Design constraints and references

Only already accepted constraints. Link design decisions and ADRs rather than restating their rationale.

## Implementation notes

Optional discoveries or hints. These are negotiable and must not silently expand scope.
```

Mutable status and blockers belong only in the product backlog tracker.
