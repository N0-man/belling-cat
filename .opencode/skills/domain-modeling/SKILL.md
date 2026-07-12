---
name: domain-modeling
description: Improve ubiquitous language, responsibility ownership, and module boundaries when domain-oriented reasoning materially reduces ambiguity.
compatibility: opencode
metadata:
  workflow: domain-design
---

# Pragmatic Domain Modeling

Use when language, ownership, or boundaries are genuinely unclear or changing. Do not invoke merely to decorate ordinary code with DDD terminology.

## Sources of truth

- `CONTEXT.md`: useful ubiquitous language for the current domain or context.
- `CONTEXT-MAP.md`: relationships between genuinely distinct contexts, only when needed.
- `docs/00-repo-structure.md`: module ownership and dependency rules.
- design decisions and ADRs: rationale for technical or architecture choices, managed through `decision-recording`.

## Language discipline

Challenge fuzzy, overloaded, or conflicting terms. Define what a term means to users and the business, and list misleading synonyms where useful.

Do not put APIs, frameworks, persistence details, prompts, streaming mechanics, or implementation recipes in the glossary.

Tactical labels such as Entity, Value Object, Aggregate Root, Domain Event, Policy, or Read Model are optional. Add one only when it clarifies identity, lifecycle, ownership, or invariants. `Domain Concept` or no label is valid.

Do not create bounded contexts, aggregates, repositories, services, or ports as ceremony.

## During discovery

- update language only as terms become stable;
- identify responsibility and lifecycle ownership when it affects behaviour or design;
- update repository structure when module boundaries become clear;
- delegate technical decision classification to `decision-recording`.

## During implementation/refactoring

After GREEN, ask proportionately:

- Did the code reveal a better term or responsibility owner?
- Is a business rule leaking into delivery or infrastructure code?
- Is an external dependency difficult to test or replace enough to justify a boundary?
- Did a module/dependency rule change?
- Is the existing glossary or structure document now misleading?

Update only the artifacts that genuinely changed. New product behaviour or scope returns to `/discover`; do not smuggle it into refactoring.

Use the bundled context format when a glossary update is warranted.
