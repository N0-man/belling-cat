---
name: create-prd
description: Synthesize the confirmed discovery interaction and durable decision records into a concise, traceable product requirements document that preserves user intent.
compatibility: opencode
metadata:
  workflow: planning
---

# Create PRD

## Gate

Use the confirmed discovery interaction as the primary source. Also read relevant code, tests, `CONTEXT.md`, repository structure, increment design records, and ADRs.

If the available conversation does not establish the outcome, scope, important behaviours, deliberate constraints, and acceptance evidence, stop and recommend `/discover`. Do not infer product intent from code or fabricate a discovery artifact merely to satisfy a gate.

## Process

1. Resolve the increment name and `.scratch/<increment>/PRD.md` path.
2. Capture the user's objective in outcome terms, not as a list of files or implementation tasks.
3. Extract product behaviour, constraints, failure behaviour, quality attributes, exclusions, deliberate trade-offs, ruled-out approaches, and deferred scope from the confirmed interaction.
4. Inspect implementation decisions embedded in source notes or an existing PRD.
5. Invoke the `decision-recording` skill to move accepted technical choices to `docs/design/<increment>.md`, ADRs, or repository structure as appropriate.
6. Keep unresolved alternatives as explicit open decisions; do not choose silently.
7. Assign stable requirement IDs such as `REQ-001` and quality IDs such as `NFR-001`.
8. Prefer observable requirements and concise examples over implementation recipes.
9. Record the highest useful public test/demo seams.
10. Ensure each durable fact has one primary owner; use references rather than duplicating full rationale across PRD, design, ADR, README, and context.
11. Write the PRD using `PRD-FORMAT.md`.
12. Present a concise summary and ask one approval question before treating it as ready for backlog creation.

Do not create backlog stories in this skill.
