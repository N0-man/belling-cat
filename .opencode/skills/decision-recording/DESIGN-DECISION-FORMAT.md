# Design decision format

Design decisions live in `docs/design/NNNN-<slug>.md`. Each file records exactly one accepted, local or reasonably reversible design choice.

## Required structure

```md
# <Decision title>

**Status:** Accepted
**Related PRD:** `.scratch/<increment>/PRD.md`
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

Do not infer alternatives, pros/cons, trade-offs, or consequences from code, conventions, or general best practice.

Optional lifecycle metadata may be added when applicable:

```md
**Supersedes:** `docs/design/0001-<slug>.md`
**Superseded by:** `docs/design/0003-<slug>.md`
```

Do not combine several decisions into one increment-level document. The related PRD links the individual decision files relevant to the increment.
