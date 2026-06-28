---
name: create-backlog
description: Break the PRD into independently-grabbable backlog items as tracer-bullet vertical slices and track them locally per feature.
disable-model-invocation: true
---

# Create Backlog

Break the PRD into independently-grabbable backlog items using vertical slices (tracer bullets).

## Process

### 1. Gather context

Work from the recent PRD document from the conversation context. If the user passes a different PRD reference as an argument, load that PRD from local workspace paths (typically `.scratch/<feature-name>/PRD.md`) and read it fully.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Backlog item titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the plan into **tracer bullet** backlog items. Each backlog item is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

<vertical-slice-rules>

- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Any prefactoring should be done first

</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?

Iterate until the user approves the breakdown.

### 5. Publish backlog items to local files

For each approved slice, create a local backlog item file under `.scratch/<feature-name>/backlog/` using the template below.

Publish items in dependency order (blockers first) so each item can reference earlier local item identifiers in the "Blocked by" field.

Use deterministic naming so reruns update existing files instead of creating duplicates:

- File name format: `NN-short-kebab-title.md` (example: `01-query-intake.md`)
- In-file title format: `# Item NN: <Title>`
- Initial status for all new backlog items: `to-do`

### 6. Update the per-feature backlog tracker

Maintain a per-feature tracker at `.scratch/<feature-name>/backlog.md`.

- If the file does not exist, create it.
- Add one row per backlog item in the same dependency order used above.
- Track status using only: `to-do`, `doing`, `done`.
- On rerun, update existing rows in place (match by `Item file`) and do not duplicate rows.
- Rerun ordering rule: preserve the current tracker row order for existing items; append only newly introduced items at the end in dependency order.

Use this tracker table format:

| Item ID | Title        | Status | Blocked by                   | PRD                            | Item file                                          |
| ------- | ------------ | ------ | ---------------------------- | ------------------------------ | -------------------------------------------------- |
| Item 01 | Query intake | to-do  | None - can start immediately | .scratch/<feature-name>/PRD.md | .scratch/<feature-name>/backlog/01-query-intake.md |

<item-template>
# Item NN: <Title>

## Status

to-do

## Parent

A reference to the parent PRD or source backlog item (if the source was an existing item, otherwise omit this section).

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- Local backlog item references only (for example: `Item 01` or `.scratch/<feature-name>/backlog/01-query-intake.md`)

Or "None - can start immediately" if no blockers.

</item-template>

Do NOT close or modify any parent backlog item.
