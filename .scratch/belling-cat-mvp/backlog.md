# Backlog: Belling Cat MVP

## Overview

This backlog tracks the implementation of the Belling Cat fact-checking terminal application. Each item is a vertical slice that delivers end-to-end functionality.

## Backlog Items

| Item ID | Title | Status | Blocked by | PRD | Item file |
|---------|-------|--------|-----------|-----|-----------|
| Item 00 | Scaffolding & Tech Stack Setup | done | None - can start immediately | .scratch/belling-cat-mvp/PRD.md | .scratch/belling-cat-mvp/backlog/00-scaffolding-tech-stack.md |
| Item 01 | CLI Foundation & Command Parsing | done | Item 00 | .scratch/belling-cat-mvp/PRD.md | .scratch/belling-cat-mvp/backlog/01-cli-foundation.md |
| Item 02 | Claim Decomposition Agent | done | Item 01 | .scratch/belling-cat-mvp/PRD.md | .scratch/belling-cat-mvp/backlog/02-claim-decomposition.md |
| Item 03 | Investigation & Evidence Gathering | done | Item 02 | .scratch/belling-cat-mvp/PRD.md | .scratch/belling-cat-mvp/backlog/03-investigation-evidence.md |
| Item 04 | Verifier Agent & Verdict Display with User Approval | doing | Item 03 | .scratch/belling-cat-mvp/PRD.md | .scratch/belling-cat-mvp/backlog/04-verifier-verdict.md |
| Item 05 | Report Generation via /save Command | to-do | Item 04 | .scratch/belling-cat-mvp/PRD.md | .scratch/belling-cat-mvp/backlog/05-report-generation.md |
| Item 06 | Session Loop & Error Handling | to-do | Item 05 | .scratch/belling-cat-mvp/PRD.md | .scratch/belling-cat-mvp/backlog/06-session-loop.md |
| Item 07 | Session Persistence & Recovery | to-do | Item 06 | .scratch/belling-cat-mvp/PRD.md | .scratch/belling-cat-mvp/backlog/07-session-persistence.md |

## Status Legend

- **to-do**: Not started
- **doing**: Currently in progress
- **done**: Completed and verified

## Notes

- Items should be completed in dependency order (Item 00 → Item 07)
- Each item includes integration tests that verify end-to-end behavior
- The MVP excludes `/interview me` mode, historical session retrieval, and multi-user support
