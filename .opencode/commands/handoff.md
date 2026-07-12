---
description: Inspect, checkpoint, reconcile, close, or discard active scope, intent, cycle, finding, and validation state
agent: build
---

Use the `handoff` skill and always compare it with the product backlog tracker and Git scope baseline.

Supported intents:
- no argument or `status`: show combined tracker/handoff, intent, scope, finding, and validation state;
- `checkpoint <note>`: preserve history and update the current phase;
- `reconcile`: repair a tracker/handoff/Git mismatch using evidence;
- `close`: archive a completed handoff and remove the active file;
- `discard`: remove the active handoff only after explicit confirmation, without changing code or tracker state.

$ARGUMENTS
