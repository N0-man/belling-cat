# Handoff format

```md
---
workflow_version: 5
kind: backlog-story | refactor
increment: <increment or null>
backlog: .scratch/<increment>/backlog.md
work_id: ITEM-01 | REFACTOR-...
work_file: <story or refactor record path>
prd: <path or null>
story_base_sha: <SHA>
current_head: <SHA>
cycle: 1
phase: reconcile | red | green | refactor | verify | committed | review | traceability | repair | preflight | validate | awaiting-user | done
updated_at: <UTC timestamp>
---

# Active Handoff

## State reconciliation

- Tracker status:
- Tracker active story:
- Handoff story:
- Git status:
- Consistency: consistent | needs-reconcile | divergent

## Scope baseline

- Starting HEAD:
- Pre-existing staged files:
- Pre-existing modified files:
- Pre-existing untracked files:
- Related changes:
- Unrelated changes to preserve:
- Uncertain overlaps:
- Current intended files and rationale:

## Intent packet

- Objective and beneficiary:
- Observable outcome:
- Demonstration evidence:
- Accepted constraints and quality attributes:
- Deliberate technical/design choices:
- Ruled-out or deferred approaches:
- Explicit out of scope:
- Completeness: complete | partial

## Current objective

## Current cycle

- Behaviour or repair finding:
- Test or safety signal:
- Expected RED:
- Current phase:

## Cycle history

### Cycle 01 — <Behaviour>

- RED: <timestamp, command, expected failure evidence>
- GREEN: <timestamp, command, pass evidence>
- REFACTOR: <timestamp, code/design/context changes or none>
- VERIFY: <timestamp, commands and results>
- COMMIT: <timestamp, SHA, title>
- SCOPE CHECK: <baseline-preserved or explained delta>

## Acceptance and demo progress

## Finding queue

| ID | Axis | Severity | Action | Status | Evidence | Resolution |
|---|---|---|---|---|---|---|

## Review and traceability state

- Reviewed range:
- Risk level and rationale:
- Axes completed:
- Open repair findings:
- Awaiting-user findings:
- Decision records required:

## Preflight and validation state

- Preflight:
- Validation outcome:
- Workspace delta:

## Open blockers and discoveries

## References

- Product backlog:
- Story:
- PRD:
- Design decisions:
- ADRs:
```
