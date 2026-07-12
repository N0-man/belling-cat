---
name: check-handoff
description: Load and reconcile active workflow recovery state against the product backlog tracker without deleting history or guessing current work.
compatibility: opencode
metadata:
  workflow: state-management
---

# Check Handoff

Use at the beginning of user-triggered workflow commands.

## Read both state sources

1. Locate the relevant `.scratch/<increment>/backlog.md` tracker when one can be resolved.
2. Read `.scratch/handoff-context.md` when it exists.
3. Compare tracker active story, handoff story, and current Git HEAD.

## Consistency rules

- Matching tracker `doing` story and handoff work ID: current work is resumable.
- Tracker has one `doing` story but no handoff: recovery information is incomplete; reconstruct cautiously and use `reconcile` phase.
- Handoff exists but tracker has no matching `doing` story: mismatch; do not mutate product code until reconciled.
- More than one `doing` story: invalid tracker state.
- No active story and no handoff: no recovery state; continue normally.

Compare `current_head` with repository `HEAD`:

- equal: current;
- recorded HEAD is an ancestor: repository advanced; inspect commits and refresh only when they belong to the same work;
- recorded HEAD is not an ancestor: divergent/stale; surface the conflict and reconcile.

Never delete a handoff because the user declines to resume. Deletion requires explicit `/handoff discard`.

## Command behaviour

- `/implement` targeting the matching active story: resume automatically and state story, cycle, and phase.
- `/workflow-status`, `/handoff`, `/review`, `/preflight`, `/test-affected`: load tracker and handoff as context without asking.
- `/discover`, `/create-prd`, or `/create-backlog` while implementation is active: preserve the handoff; ask one question only if the new planning work risks conflicting with active changes.
- Divergence or tracker/handoff mismatch: recommend `/handoff reconcile`; do not guess.

The handoff is recovery state, not a conversation lock.
