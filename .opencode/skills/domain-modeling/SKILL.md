---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the _active_ discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely _reading_ `CONTEXT.md` for vocabulary is not this skill — that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Single context: `CONTEXT.md` at root + `docs/adr/`. Multi-context: `CONTEXT-MAP.md` at root pointing to each bounded context's own `CONTEXT.md`. Create files lazily — only when you have something to write.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Classify each term into a DDD building block

When a term is added to `CONTEXT.md`, also identify which tactical DDD pattern it maps to:

| Building block | Characteristic |
|---|---|
| **Entity** | Has identity that persists over time; two instances with the same attributes are still distinct if their IDs differ |
| **Value Object** | Defined entirely by its attributes; immutable; interchangeable if attributes match |
| **Aggregate** | Cluster of entities/VOs treated as a unit; has a single Aggregate Root that controls access |
| **Domain Service** | Stateless operation that belongs to the domain but doesn't naturally fit on an entity |
| **Repository** | Abstraction over persistence for an aggregate — defined in the domain/application layer, implemented in infrastructure |
| **Port** | Interface defined by the application layer for any external dependency (LLM, search, storage); concrete implementation lives in adapters |
| **Application Service** | Orchestrates domain objects to fulfil a use case; no business logic of its own |

Record the building block type alongside each term in `CONTEXT.md` (e.g., `**Claim** _(Aggregate Root)_:`).

### Establish layer structure in docs/00-repo-structure.md

When the domain model is sufficiently clear (aggregates, services, and ports identified), write or update `docs/00-repo-structure.md` to document:

- The module layout that reflects the Clean Architecture layers for this project
- Which layer each building block lives in
- The dependency rule in force: inner layers must not import from outer layers

Create this file lazily — only once there is enough model to make it meaningful. Update it whenever a new boundary, module, or port is introduced.

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

Also check layer violations: if a domain term's implementation lives in the wrong layer (e.g., a Value Object method making an HTTP call), flag it.

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

## When to stop

End the session when the user signals they're done — "done", "looks good", "that's enough", or similar. Summarize: (1) terms added or changed in `CONTEXT.md` with their building block types, (2) any updates to `docs/00-repo-structure.md`, (3) any ADRs created. Then stop.
