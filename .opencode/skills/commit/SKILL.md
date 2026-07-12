---
name: commit
description: Create one focused, verified commit for a completed green TDD, refactoring, or documentation repair cycle without staging unrelated or sensitive files.
compatibility: opencode
metadata:
  workflow: version-control
---

# Commit One Focused Cycle

## Preconditions

- active cycle phase is VERIFY, or the change is an explicitly verified documentation/decision repair;
- focused and affected checks passed;
- intended file set is known;
- `scope-guard` baseline exists or has just been established;
- unrelated workspace changes are identified and excluded.

Do not run full preflight for every cycle unless required by the repository; full preflight is mandatory at story/refactor completion.

## Process

1. Inspect `git status --short`, relevant diffs, and staged state.
2. Abort if secrets, credentials, certificates, private keys, local environment files, generated bulk artifacts, or unexplained files are in scope.
3. Stage specific intended paths only. Broad all-workspace staging is prohibited.
4. Inspect `git diff --cached` and confirm it represents one complete green or documentation repair cycle.
5. Derive the message from active work unless explicitly supplied:
   - `ITEM-03 Cycle 02: reject an empty claim`
   - `REFACTOR-AUD-004 Cycle 01: isolate search adapter`
   - `ITEM-03 Docs: synchronize investigation guidance`
6. Commit without amend, force, or hook bypass.
7. Report SHA, title, and files; update the handoff COMMITTED checkpoint after the commit.
8. Recheck the scope baseline and confirm unrelated changes remain outside the commit.

Do not push.
