---
name: commit
description: Create a single commit from the current reviewed changes.
argument-hint: "Commit message (optional)."
disable-model-invocation: true
---

# Commit

Create one commit for the current reviewed changes.

## Process

1. Confirm scope

- Use `git status --short` and `git diff --stat` to confirm what will be committed.
- If unrelated changes are present, ask the user whether to exclude them before committing.

2. Build commit message

- If the user passed a message argument, use it.
- Otherwise derive a concise message from the reviewed issue/slice.
- Prefer issue-linked format when available: `Issue NN: <concise summary>`.

3. Stage and commit

- Stage only the intended files for this change.
- Create a single non-amended commit with the message from step 2.

4. Report result

- Return commit hash, title line, and changed files summary.

## Rules

- Do not amend previous commits unless explicitly requested.
- Do not include unrelated files without user confirmation.
- Do not push.
- Never use `git add -A` or `git add .` — stage specific files only.
- Never use `--no-verify`.
- Never commit `.env`, keys, credentials, tokens, certs, or secrets — abort if any staged file contains them.
- Run `/preflight` (or at minimum `/test-affected`) before committing unless the user explicitly overrides.
