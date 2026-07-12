---
name: refactor
description: Resolve selected audit findings through scoped behaviour-preserving characterization and committed TDD cycles, then repeat audit, validation, and preflight.
compatibility: opencode
metadata:
  workflow: implementation
---

# Refactor from Audit Findings

## Eligibility

Read the audit report and selected findings. Use the `finding-triage` skill before starting.

Work is eligible only for findings classified `repair` whose intended observable behaviour and approved contracts remain unchanged.

Route to `/discover` or ask the user when the change alters product behaviour, contracts, data semantics, scope, or a material architecture/dependency choice. Use `/record-decision` when code may remain unchanged but rationale is missing.

## Scope and work record

Invoke the `scope-guard` skill.

Create `.scratch/refactors/<timestamp>-<slug>.md` with selected finding IDs, protected behaviours, acceptance evidence, intent boundaries, and status. Record current HEAD as base and bootstrap a handoff with `kind: refactor`.

Do not overwrite an unrelated active story handoff; preserve and surface the conflict. Record pre-existing workspace changes and exclude them from refactor commits.

## Execution

1. Establish characterization protection where behaviour is not sufficiently covered.
2. Use one TDD/safety cycle for one refactoring outcome at a time.
3. Preserve behaviour and keep each cycle green and committed.
4. Prefer a bounded root-cause improvement over a superficial line patch when the same audited defect class would remain.
5. Apply DDD or architectural patterns only where they solve the audited problem.
6. Invoke the `decision-recording` skill for material clarified choices and the `domain-modeling` skill for genuinely improved language/ownership.
7. Commit every verified cycle as `REFACTOR-<id> Cycle NN: ...`.
8. Preserve prior repair commits; never restart by resetting away completed work.

## Final gate

Rerun the audit against the original scope and selected findings, then invoke the `validate-change` skill on the exact refactor base..HEAD range with the protected-behaviour intent packet.

Mark the refactor done and close handoff only when findings are resolved, no regression appears, decisions are current, preflight passes, and unrelated baseline changes remain outside the commits.
