---
name: create-backlog
description: Turn an increment PRD into an ordered, INVEST-oriented product backlog whose stories preserve intent, are testable, and can demonstrate value.
compatibility: opencode
metadata:
  workflow: planning
---

# Create Product Backlog

## Gate

Use the `workflow-state` skill. Require `.scratch/<increment>/PRD.md`. Read relevant context, design decisions, ADRs, code, and tests.

## Story quality

Use INVEST as a heuristic, not dogma.

Each story should:

- have one coherent outcome;
- preserve the relevant part of the user's original intent and deliberate constraints;
- minimize dependencies while declaring genuine blockers;
- remain negotiable about implementation unless an accepted decision constrains it;
- demonstrate value to a user, stakeholder, operator, or delivery team;
- be small and understood enough for one focused implementation/validation cycle;
- have observable acceptance and demonstration evidence;
- reference relevant PRD requirements and decisions.

A strict vertical slice is not mandatory. Technical enablers are acceptable when they unlock, de-risk, or visibly prove a useful capability. Avoid stories that merely create one layer or component without a demonstrable outcome.

## Process

1. Read the PRD and decision records.
2. Draft stories in a sensible delivery order.
3. For each story state intent, outcome, value/demo, accepted constraints, exclusions, acceptance criteria, and requirement/decision references. Record blockers only in the tracker.
4. Check the story set against INVEST and split or merge where that improves delivery.
5. Verify that later reviewers can distinguish deliberate choices from mistakes without reading the original chat.
6. Write deterministic draft story files using `ITEM-FORMAT.md`.
7. Write `.scratch/<increment>/backlog.md` using `BACKLOG-FORMAT.md`.
8. Present the proposed scope, granularity, value, and dependency order and ask one approval question.
9. New stories start `to-do` in the tracker. Do not put mutable status in story files.
10. Do not begin implementation until the user has accepted the backlog or explicitly requested `/implement`.
11. On rerun, preserve IDs, order, and existing statuses. Never silently delete or renumber `doing` or `done` stories; record supersession explicitly.

The backlog tracker is authoritative for status, order, and blockers. Story files are authoritative for intent, scope, value, criteria, evidence, and references.
