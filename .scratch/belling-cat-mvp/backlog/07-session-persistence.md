# Item 07: Session Persistence & Recovery

## Status

to-do

## Parent

.scratch/belling-cat-mvp/PRD.md

## What to build

Implement continuous auto-save of session state to enable crash recovery and resumption. The system should persist the entire investigation context (claim, sub-claims, findings, agent state, streaming logs) to `.session/session-{id}-{timestamp}.json` (or pickle format).

On startup, if an incomplete session is detected, prompt the user to resume or archive it. If resumed, the investigation continues from the last checkpoint without losing context.

## Acceptance criteria

- [ ] Session state continuously auto-saved during investigation
- [ ] Persisted state includes: original claim, decomposed sub-claims, investigation findings (partial or complete), current agent/phase, streaming output buffer
- [ ] Session files saved to `.session/session-{id}-{timestamp}.json` (or `.pkl` for complex objects)
- [ ] On application startup, detect incomplete sessions in `.session/`
- [ ] User prompted: "Resume incomplete session from [timestamp]? (yes/no)"
- [ ] If user resumes, LangGraph workflow state restored and investigation continues
- [ ] If user declines, incomplete session archived or moved to `.session/archive/`
- [ ] Completed investigations clean up session files or mark them as complete
- [ ] Integration test verifies auto-save during investigation
- [ ] Recovery test: simulate crash, restart app, verify resume functionality
- [ ] Edge case: multiple incomplete sessions handled (show list, let user choose)

## Blocked by

Item 06
