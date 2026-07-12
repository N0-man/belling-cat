---
description: Run the repository's non-mutating CI-equivalent and agent-workflow verification suite
agent: build
---

Use the `preflight` skill. Verification must not rewrite files. Run `workflow-lint` when this workflow is stored in the repository, and fail if any check mutates the workspace or leaves unexplained generated changes.

$ARGUMENTS
