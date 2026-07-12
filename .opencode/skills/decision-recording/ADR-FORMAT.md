# ADR format

ADRs live in `docs/adr/NNNN-<slug>.md` and are created lazily.

```md
---
status: proposed | accepted | deprecated | superseded
increment: <increment name when applicable>
related_decisions:
  - DD-001
---

# <Decision title>

## Context

## Decision

## Rationale

## Consequences

## Considered alternatives

## Superseded by

Omit when not applicable.
```

Create an ADR when one or more of these are materially true:

- the decision affects several modules, increments, or teams;
- reversal would be expensive, risky, or migration-heavy;
- the choice is long-lived or constrains future architecture;
- the decision is surprising without its trade-off rationale;
- several credible alternatives existed with meaningful consequences.

Routine library choices, local implementation details, and small reversible refactors belong in the increment design record or code—not an ADR.
