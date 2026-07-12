---
name: workflow-state
description: Validate and report increment state by reconciling the product backlog tracker, story files, Git, scope baseline, intent packet, and active handoff.
compatibility: opencode
metadata:
  workflow: gate
---

# Workflow State

## Canonical artifacts

```text
.scratch/<increment>/PRD.md
.scratch/<increment>/backlog.md
.scratch/<increment>/backlog/NN-<slug>.md
.scratch/handoff-context.md
docs/design/<increment>.md
docs/adr/
```

There is no mandatory discovery-state artifact.

## State authority

The product backlog tracker is authoritative for:

- story order;
- story status (`to-do`, `doing`, `done`);
- blockers;
- active story selection.

The story file is authoritative for scope, acceptance criteria, value/demo, intent, and references.

The handoff is authoritative for the active story's exact execution state: base SHA, current HEAD, scope baseline, intent packet, cycle, phase, evidence, commits, findings, validation, and blockers.

## Gates

- `/create-backlog`: require the increment PRD.
- `/implement`: require PRD, backlog tracker, one resolvable story, and all blockers done.
- `/review` during a story: require exact base SHA, intent packet, story path, PRD path, and tracker path from the handoff.
- `/validate`: require an active-story handoff or an explicit committed range plus intent/specification.
- `/refactor`: require an audit report or explicitly bounded behaviour-preserving target.

When a gate fails, name the missing or conflicting artifact and the next corrective action. Do not silently create downstream product scope.

## Resolve active story

Read the tracker and handoff together.

1. If exactly one story is `doing` and the handoff matches it, resume the handoff's cycle and phase.
2. If exactly one story is `doing` but no handoff exists, inspect Git history, working changes, tests, and story evidence. Create a handoff in `reconcile` phase and report ambiguity before code changes.
3. If a handoff exists but its story is not the tracker’s `doing` story, report a mismatch and require reconciliation.
4. If no story is `doing` and no handoff exists, choose the explicit story or the lowest ordered ready `to-do` story.
5. If more than one story is `doing`, stop: the tracker is invalid.
6. If no ready story exists, report blockers or completion.

Never infer active status from a story file.

## Starting a story

Before any workflow or production mutation:

- invoke the `scope-guard` skill and record baseline changes;
- record current HEAD as `story_base_sha`;
- set the selected tracker row from `to-do` to `doing`;
- create the handoff referencing tracker, story, and PRD;
- build an intent packet from approved sources;
- surface any overlapping or unexplained workspace change.

## Completing a story

Only after candidate acceptance/demo evidence is recorded and `validate-change` returns `PASS`:

- set the tracker row from `doing` to `done`;
- update acceptance/evidence in the story file;
- finalize and archive the handoff.

## Report mode

Show:

- discovered increments and PRD/backlog availability;
- backlog counts by status;
- the one active story or next ready story;
- blockers;
- handoff cycle, phase, base SHA, current HEAD, and staleness;
- intent packet completeness;
- scope baseline and unexpected changes;
- open findings and whether they are repairable or awaiting user decision;
- validation and preflight state;
- tracker/handoff consistency;
- exact next valid command.

Do not modify files in report mode.
