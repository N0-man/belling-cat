# Session Persistence and Recovery

**Status:** Accepted
**Related PRD:** [belling-cat-mvp](../../.scratch/belling-cat-mvp/PRD.md)

## Decision

Implement continuous auto-save to file-based session storage with:

- Storage location: `.session/` directory in user's workspace
- File naming: `session-{id}-{timestamp}.json` (metadata) + `session-{id}-{timestamp}.pkl` (LangGraph state)
- Format: JSON for human-readable metadata, Python pickle for LangGraph workflow state objects
- Persistence frequency: After each agent node completion
- Recovery flow: On startup, detect incomplete sessions and prompt user to resume or archive
- Cleanup: Completed sessions archived or deleted after successful report generation

## Why

PRD requires continuous auto-save of session state for crash recovery (PRD Requirements 27-31). System must persist claim, sub-claims, findings, agent state, and streaming log. On restart, detect incomplete session and offer to resume or start fresh.
