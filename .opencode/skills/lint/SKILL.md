---
name: lint
description: Run repository-native lint and formatting checks by default, or apply explicitly authorized scoped fixes with --fix.
compatibility: opencode
metadata:
  workflow: verification
---

# Lint and Format

Inspect `Makefile`, task-runner files, package manifests, and CI configuration. Do not assume a language or framework that the repository does not use.

## Default check mode

Without `--fix`, run non-mutating lint and format checks, preferring:

```bash
make lint
make format-check
```

Report commands, exit status, and concise failures. Do not edit files.

## Explicit fix mode

Only use fix mode when the user passes `--fix` or an active repair workflow explicitly authorizes it.

1. Invoke the `scope-guard` skill.
2. Resolve explicit paths from arguments or the active story scope.
3. Prefer repository targets such as:

```bash
make lint-fix PATHS="<explicit paths>"
make format PATHS="<explicit paths>"
```

4. Never run a repository-wide style sweep while unrelated baseline changes exist unless the user explicitly requests it.
5. Re-run non-mutating checks for the same scope.
6. Show changed paths and `git diff --stat`; report remaining failures.

`/preflight` must never use fix mode.
