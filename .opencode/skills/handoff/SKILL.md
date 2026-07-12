---
name: handoff
description: Maintain durable active-story recovery state, reconcile it with the product backlog tracker, and preserve scope, intent, per-cycle evidence, findings, validation, and commits.
compatibility: opencode
metadata:
  workflow: state-management
---

# Handoff

The active file is `.scratch/handoff-context.md`. It complements, but does not replace, the product backlog tracker.

## Bootstrap

At story start:

- require the tracker row to be `doing`;
- create the handoff using `HANDOFF-FORMAT.md` if none exists;
- if a handoff describes the same story, resume without overwriting history;
- if it describes different work, surface the conflict;
- record tracker, story, PRD, `story_base_sha`, current HEAD, scope baseline, and intent packet before production changes.

The scope baseline lists pre-existing staged, modified, and untracked files. The intent packet records the user's objective, accepted constraints/trade-offs, exclusions, and demonstration outcome.

## Checkpoint

After every material phase, update metadata and append evidence:

- scope changes and their relationship to intent;
- RED observed with expected failure;
- GREEN focused test passed;
- REFACTOR completed and context/decision records checked;
- VERIFY affected or broader tests passed;
- COMMIT created with SHA;
- REVIEW/TRACEABILITY findings and triage action;
- repair or user-decision status;
- PREFLIGHT result;
- VALIDATION outcome and risk assessment.

Use cycle/phase identity to avoid duplicate log entries after retries. Never claim a phase without evidence. Never delete old finding or repair history; mark its status and resolution.

## Reconcile

Use when tracker, handoff, Git, or scope baseline disagree.

1. Read the tracker, story, Git status/log/diff, tests, and handoff history.
2. Determine what can be established from evidence.
3. Preserve uncertain history explicitly; do not rewrite it as fact.
4. Repair tracker or handoff metadata only when evidence is sufficient.
5. Confirm pre-existing unrelated changes were not absorbed into story commits.
6. If ambiguity affects scope, intent, or code ownership, stop and ask one focused question.

## Close

Only after the tracker story is `done` and validation passes:

- set phase `done`;
- update final HEAD and summary;
- record whether the workspace is clean or unrelated baseline changes remain preserved;
- copy the handoff to `.scratch/<increment>/handoffs/<story-id>.md`;
- remove `.scratch/handoff-context.md`.

## Discard

Require explicit user confirmation. Discarding recovery state must never change tracker status, reset code, or remove commits automatically.

## Staleness

Equal HEAD is current. An ancestor may be refreshable after inspecting intervening commits. Non-ancestor history is divergent and requires reconciliation.
