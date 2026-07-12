---
description: Create a PRD from the confirmed discovery interaction and durable decision records
agent: plan
---

Run the `check-handoff` skill for the `create-prd` command, then use the `create-prd` skill to create or update `.scratch/<increment>/PRD.md`.

Use the current discovery conversation and repository artifacts. If the interaction does not yet contain sufficient confirmed requirements, route back to `/discover` rather than fabricating scope. Ensure accepted technical choices are recorded as design decisions or ADRs and referenced by the PRD.

Arguments: optional increment name.

$ARGUMENTS
