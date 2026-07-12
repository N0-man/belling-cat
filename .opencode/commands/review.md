---
description: Review an exact committed range for standards, intent/specification, and proportionate architecture
agent: build
---

Use the `review` skill and then the `finding-triage` skill. Invoke the `standards-reviewer` subagent, the `spec-reviewer` subagent, and the `architecture-reviewer` subagent in parallel.

Arguments may include an exact fixed point and explicit story/specification path. During implementation, use the active handoff's story base SHA, intent packet, story file, PRD, and referenced design/ADR records. Review is read-only; do not repair findings in this command.

$ARGUMENTS
