---
name: check-handoff
description: Gate check at the start of any user-triggered command. If a handoff file exists, ask the user whether to resume from it. Declining deletes the file; accepting loads the context.
disable-model-invocation: true
---

# Check Handoff

Run this at the very start of a command, before doing anything else.

## Steps

### 1. Detect handoff file

Check whether `.scratch/handoff-context.md` exists.

- If it does **not** exist: do nothing. Skip the rest of this skill entirely and proceed with the command.

### 2. Surface the handoff summary

Read `.scratch/handoff-context.md` and extract the one-line focus or summary from its metadata section (typically the "next session focus" or last backlog item in progress).

Ask the user **exactly this one question** — do not ask anything else:

> A handoff file exists from a previous session: **<one-line summary>**
> Resume from it? (yes / no)

### 3. Handle the response

**If yes:**
- Read the full contents of `.scratch/handoff-context.md` into your working context.
- Note the commit hash and timestamp recorded in the file; flag if the current `HEAD` has advanced past that commit (stale context).
- Proceed with the current command using the handoff context as background.

**If no:**
- Delete `.scratch/handoff-context.md`.
- Proceed with the current command as if no handoff existed.
