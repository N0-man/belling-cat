---
name: preflight
description: Run the repository's non-mutating CI-equivalent verification checks, including workflow consistency when configured, and fail on workspace mutation.
compatibility: opencode
metadata:
  workflow: verification
---

# Preflight

## Discover the gate

Prefer `make preflight` or the repository's documented CI-equivalent target. The Makefile or CI configuration owns executable verification commands; do not maintain contradictory copies in agent instructions.

Otherwise reproduce non-mutating checks from workflow/config files: lint check, format check, type/static analysis, tests, coverage only when configured, architecture/import checks when present, and `workflow-lint` when this OpenCode workflow is stored in the repository.

Do not claim a check exists merely because a generic workflow mentions it.

## Non-mutation guarantee

Capture `git status --short` before and after. Preflight commands must use check modes, never auto-fix or rewrite. If verification changes files, preflight fails and reports the mutation.

Baseline-preserved unrelated changes may remain, but the before/after delta from preflight itself must be empty.

## Result

Report each executed check, command, exit status, and concise failure evidence. Overall success requires:

- every required check passed;
- no unexpected warnings treated as errors by project policy;
- workflow consistency passed when configured;
- workspace delta after preflight is empty relative to its starting state.

Suggest `/lint --fix <paths>` for fixable style/format failures, but do not run it automatically during preflight.
