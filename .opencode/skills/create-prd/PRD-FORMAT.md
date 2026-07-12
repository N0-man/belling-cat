# PRD format

```md
---
increment: <kebab-case-name>
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
---

# PRD: <Increment title>

## Intent and outcome

What the user or stakeholder set out to accomplish, who benefits, and the observable outcome. This is not a diff or implementation summary.

## Actors and journey

## Deliberate constraints and trade-offs

Accepted product/delivery constraints, ruled-out approaches, and decisions that a reviewer must know to distinguish intent from mistakes. Reference technical rationale owned by design records or ADRs.

## Requirements

### REQ-001 — <Observable requirement>

Use concise GIVEN/WHEN/THEN examples or decision tables only where they clarify behaviour.

## Failure behaviour and edge cases

## Quality attributes

### NFR-001 — <Measurable or verifiable quality constraint>

## Product constraints

Only product or delivery constraints. Do not duplicate architecture rationale.

## Decision references

- DD-001 — `docs/design/<increment>.md`
- ADR-0001 — `docs/adr/0001-<slug>.md`

## Domain language references

Reference only glossary terms relevant to this increment.

## Acceptance and demonstration evidence

Describe how the increment can be tested and showcased.

## Out of scope

## Deferred and open decisions

Each unresolved decision states what it blocks and where it is tracked.

## Traceability

Optional mapping from source conversation themes to requirement IDs.
```
