---
name: handoff
description: Write or refresh a workspace handoff document at .scratch/handoff-context.md for the next session.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarizing the current conversation so a fresh agent can continue the work.

Save to `.scratch/handoff-context.md` in the workspace.

Always overwrite the file on each `/handoff` run.

Map each handoff to the current commit:

- Resolve current `HEAD` commit hash.
- Record it in the handoff file under a metadata section.
- Record UTC timestamp for when the handoff was generated.

Detect stale handoff context before overwrite:

- If `.scratch/handoff-context.md` already exists, read its previously recorded commit hash.
- Compare previous hash with current `HEAD` hash.
- If they differ, include a `Stale context detected` note in the new file explaining that the previous handoff belonged to an older commit.
- If they match, state `No stale context detected`.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

Use this structure:

```md
# Handoff Context

## Metadata

- Generated at (UTC): <timestamp>
- Current HEAD: <full-or-short-sha>
- Previous handoff HEAD: <sha or none>
- Stale context detected: <yes/no>

## Next-session focus

<derived from /handoff arguments if provided>

## Current status

<brief snapshot of where the workflow currently is>

## Open decisions and blockers

- ...

## Suggested next actions

1. ...
2. ...

## Suggested skills

- /create-prd
- /create-backlog
- /implement
- /review

## References

- <paths to PRD, issues, tracker, ADRs, relevant commits>
```
