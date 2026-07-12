---
description: Create an INVEST-oriented product backlog from an increment PRD for user review
agent: plan
---

Run the `check-handoff` skill for the `create-backlog` command, then use the `workflow-state` skill and the `create-backlog` skill.

Require the increment PRD. Create `.scratch/<increment>/backlog.md` as the status/order/blocker source of truth and story files under `.scratch/<increment>/backlog/`. Stories should be reasonably INVEST, small, testable, and able to demonstrate value; do not require a rigid vertical slice.

Arguments: optional increment name or PRD path.

$ARGUMENTS
