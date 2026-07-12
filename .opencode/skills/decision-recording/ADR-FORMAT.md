# ADR format

ADRs live in `docs/adr/NNNN-<slug>.md`. Each file records exactly one accepted architecture decision.

## Required structure

```md
# <Decision title>

**Status:** Accepted
**Related PRD:** [<increment>](link to `.scratch/<increment>/PRD.md`)
**Related stories:** `ITEM-01` <!-- optional metadata; omit when not useful -->

## Decision

<What was explicitly agreed.>

## Why

<Why it was explicitly chosen.>
```

This is the complete default record. Do not add more sections for completeness.

## Optional blocks

Append **Considered options** only when the options were actually discussed with or presented to the user:

```md
## Considered options

- <Option actually discussed>
- <Option actually discussed>
```

Append **Consequences** only when the consequences were explicitly acknowledged or accepted by the user:

```md
## Consequences

- <Consequence explicitly accepted>
```

Do not infer alternatives, advantages, disadvantages, trade-offs, or consequences from general knowledge, code, or the selected technology.

Optional lifecycle metadata may be added when applicable:

```md
**Supersedes:** `docs/adr/0001-<slug>.md`
**Superseded by:** `docs/adr/0003-<slug>.md`
```

Create an ADR only for an accepted decision that is cross-cutting, long-lived, expensive to reverse, or materially affects future architecture. Routine and local choices belong in an individual design-decision file or require no durable record.
