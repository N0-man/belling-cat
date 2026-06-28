# Item 06: Session Loop & Error Handling

## Status

to-do

## Parent

.scratch/belling-cat-mvp/PRD.md

## What to build

Complete the session lifecycle: idle → investigate → display verdict → save → return to idle → new investigation. This slice adds error handling for invalid inputs, graceful degradation for LLM failures, and help text for users.

The terminal should handle multiple investigations in one session without requiring restart, and errors should be user-friendly.

## Acceptance criteria

- [ ] Session state machine implemented: idle → investigating → displaying → ready for new investigation
- [ ] After `/save`, terminal returns to idle state automatically
- [ ] User can start a new `/investigate` without restarting the application
- [ ] Invalid commands display helpful error messages with usage examples
- [ ] LLM API failures handled gracefully with retry logic or user-friendly error messages
- [ ] Help text available (e.g., `/help` command or startup instructions)
- [ ] Ctrl+C during investigation handled gracefully (prompt to save partial work or exit)
- [ ] Integration test verifies full session loop: investigate → verdict → save → new investigation
- [ ] Error handling tests cover invalid commands, API failures, and network issues

## Blocked by

Item 05
