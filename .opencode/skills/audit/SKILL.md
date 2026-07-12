---
name: audit
description: Perform a read-only surprise audit for correctness, maintainability, test health, proportionate architecture, stale artifacts, undocumented decisions, and intent drift.
compatibility: opencode
metadata:
  workflow: quality
---

# Surprise Audit

Audit is independent of a planned story and may run at any time. It does not modify production code.

## Scope

- explicit path/module/range: audit that target and relevant dependencies;
- `--all`: repository-wide audit, prioritizing high-risk boundaries;
- no argument: inspect working-tree changes and surrounding architecture; if clean, inspect recent commits and structural hotspots.

Record exact scope, HEAD, and whether uncommitted changes are included. Invoke the `scope-guard` skill in observation mode so pre-existing work is not mistaken for audit-generated work.

## Sources

Read code, tests, standards, product backlog/PRDs, active intent packet when relevant, context, repository structure, increment design decisions, and ADRs. Missing documentation is evidence only when the choice is material enough to warrant it.

## Parallel axes

Invoke:

- the `code-auditor` subagent for correctness, security, resilience, performance hazards, maintainability, cohesion, coupling, and error handling;
- the `architecture-reviewer` subagent for proportionate boundaries, dependency direction, ownership, and decision compliance;
- the `traceability-auditor` subagent for undocumented decisions, stale PRDs/backlogs/design records, intent drift, and weak behavioural protection.

## Findings

Use stable IDs `AUD-001`, `AUD-002`, ... Each finding includes severity, evidence, impact, suggested action, and:

- `behaviour_change: yes | no | uncertain`;
- `discovery_required: yes | no`;
- `record_destination: none | PRD | design | ADR | repo-structure | context`.

Invoke the `finding-triage` skill to assign `repair`, `ask-user`, `record-decision`, or `no-op`. Preserve uncertainty rather than forcing a behaviour-preserving classification.

Write `.scratch/audits/<UTC timestamp>-<scope-slug>.md`. Do not auto-fix findings.

Conclude with:

- prioritized behaviour-preserving findings eligible for `/refactor`;
- missing rationale eligible for `/record-decision`;
- product or architecture choices requiring `/discover` or direct user decision;
- observations requiring no action.
