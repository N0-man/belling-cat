---
name: test-affected
description: Select and run tests affected by explicit paths or changes since a fixed commit, with safe fallback when repository-specific mapping is unavailable.
compatibility: opencode
metadata:
  workflow: verification
---

# Test Affected

## Determine changed paths

Priority:
1. explicit paths;
2. `--since <commit>`;
3. active handoff `story_base_sha`;
4. uncommitted paths from `git diff --name-only` and `git diff --cached --name-only`.

For committed story cycles, do not default to `git diff --name-only HEAD`, which is empty by design.

## Select tests

Use the repository's existing affected-test script or build target when present. Do not assume `scripts/affected_tests.py` or a parser exists.

Otherwise map conservatively using repository conventions:
- directly changed tests;
- tests mirroring changed modules;
- package/module test directories;
- integration/contract tests for changed public interfaces.

If impact cannot be mapped reliably, run the relevant package suite or full suite. “No mapped tests” is not evidence that no tests are affected.

## Run and report

Use the configured test runner. Report commands, pass/fail counts, failing test names, and selection rationale. Return failure when any selected check fails.
