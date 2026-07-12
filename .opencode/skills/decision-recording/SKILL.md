---
name: decision-recording
description: Classify technical and architecture choices and record them as product requirements, lightweight design decisions, ADRs, repository rules, open decisions, or routine implementation details.
compatibility: opencode
metadata:
  workflow: decision-management
---

# Decision Recording

Use during discovery, PRD cleanup, implementation, review, validation, or audit whenever a choice needs durable rationale.

## Classify before writing

Choose exactly one primary destination.

### Product requirement

Use when the decision states observable behaviour, a user constraint, or a product policy. Record it in the PRD. Do not disguise it as architecture.

### Design decision

Use when the choice is local to one increment, reasonably reversible, or primarily guides implementation. Record it in:

```text
docs/design/<increment>.md
```

Examples: persistence representation for this increment, terminal rendering approach, retry strategy, testing seam, local concurrency model.

### ADR

Use when the choice is cross-cutting, long-lived, costly to reverse, or surprising without its trade-off rationale. Record it in:

```text
docs/adr/NNNN-<slug>.md
```

Examples: workflow/orchestration platform, provider-coupling strategy, tenancy model, eventing architecture, system-wide persistence boundary.

### Repository structure rule

Use when the choice defines module ownership or dependency direction. Record it in `docs/00-repo-structure.md`, linking a design decision or ADR when rationale matters.

### Open decision

Use when alternatives remain unresolved. Record candidates, decision deadline/blocking stories, and status in the increment design document or PRD open-decisions section. Never write alternatives joined by “or” as though they were accepted.

### No durable record

Use when the choice is routine, obvious from code/tests, easily reversible, and has no meaningful future rationale. Do not create documentation for ceremony.

## One owner per fact

Every durable fact or rationale has one primary owner. Other artifacts link to it and add only context specific to their purpose.

- PRD owns product behaviour and constraints.
- Design record owns local technical rationale.
- ADR owns significant architecture trade-offs.
- Repository structure owns current module/dependency rules.
- `CONTEXT.md` owns business-language definitions.
- Makefile or CI configuration owns executable verification commands.

Avoid copying full requirement text, decision rationale, configuration tables, or command lists into multiple documents where they can drift.

## Process

1. Identify the actual decision—not just the chosen technology name.
2. Capture context, decision, rationale, consequences, and meaningful alternatives.
3. Confirm material choices with the user before marking them accepted.
4. Create or update the correct record using the bundled format. Preserve existing IDs: allocate the next unused zero-padded ADR number after inspecting `docs/adr/`, and append the next unused `DD-NNN` within an increment design record. Never renumber accepted or superseded records.
5. Replace duplicated rationale in the PRD or other docs with a concise reference.
6. Link related PRD requirements, stories, code boundaries, and superseded records where useful.
7. When superseding a record, preserve history and point to the replacement.
8. During validation, classify missing but already-approved rationale as `record-decision`; unresolved choices belong to `ask-user`.

## Migration from mixed PRDs

When a PRD contains an implementation-decisions section:

- move accepted architecture trade-offs to ADRs;
- move local/reversible choices to the increment design record;
- keep observable product behaviour in the PRD;
- mark unresolved alternatives as open decisions;
- leave a `Decision references` section in the PRD.

Do not silently invent the selected alternative while migrating.
