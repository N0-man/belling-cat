---
description: Run a surprise codebase audit for correctness, structure, architecture, tests, intent drift, and undocumented decisions
agent: build
---

Use the `audit` skill and `finding-triage` skill. This command is read-only: inspect the requested scope, invoke the configured audit subagents in parallel, and write a finding report under `.scratch/audits/` without changing production code.

Arguments: optional path, module, exact diff range, or `--all`. With no argument, audit the current working changes and the architecture around them.

$ARGUMENTS
