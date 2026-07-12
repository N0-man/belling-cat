---
name: scope-guard
description: Capture the repository baseline before agent work, preserve unrelated changes, and prevent story, refactor, validation, or commit scope from drifting.
compatibility: opencode
metadata:
  workflow: safety
---

# Scope Guard

Use before `/implement`, `/refactor`, repair-enabled `/validate`, and any standalone commit.

## Establish the baseline

Inspect and record:

```bash
git rev-parse HEAD
git status --short
git diff --name-status
git diff --cached --name-status
```

When an active handoff exists, store the baseline there. Record:

- starting HEAD;
- tracked modifications;
- staged files;
- untracked files;
- whether each pre-existing change is related, unrelated, or uncertain;
- the intended story/refactor/validation scope.

Do not stash, reset, clean, delete, or rewrite pre-existing work merely to obtain a clean tree.

## Scope rules

- Preserve unrelated pre-existing changes byte-for-byte where practical.
- Never stage broad paths merely because they are convenient.
- Stage explicit intended files only.
- Do not absorb an unrelated cleanup, dependency update, formatting sweep, generated artifact, or refactor into the current work.
- If an existing change overlaps the same lines or files and ownership cannot be established safely, stop and ask one focused question.
- A newly discovered problem outside the current intent becomes an audit finding, backlog candidate, or separate discovery topic; it is not silently fixed.

## During work

After every cycle commit or validation repair:

1. compare the current workspace with the recorded baseline;
2. confirm unrelated files remain uncommitted and unmodified by the agent;
3. update the handoff with intended files added to scope and why;
4. flag unexpected files immediately.

Scope may evolve when implementation legitimately reveals another required file, but the reason must trace to the approved story, finding, test, or decision record.

## Before commit or completion

Confirm:

- the staged diff contains only the current cycle or approved documentation repair;
- pre-existing unrelated changes remain outside the commit;
- no secrets or local-only files entered scope;
- every changed file has a stated relationship to the active intent.

Do not claim a clean workspace when unrelated baseline changes intentionally remain. Report it as `baseline-preserved` instead.
