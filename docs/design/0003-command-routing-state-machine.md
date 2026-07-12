# Command Routing and State Machine

**Status:** Accepted
**Related PRD:** [belling-cat-mvp](../../.scratch/belling-cat-mvp/PRD.md)

## Decision

Implement commands: `/investigate <claim>`, `/save <report-name>` (optional), `/help`, `/quit` or `/exit`

Linear state machine: idle → investigating → displaying results → idle

## Why

PRD defines `/investigate <claim>` command pattern (PRD Requirement 3) and session flow from idle to investigation to save and return to idle (PRD Requirements 24-26).
