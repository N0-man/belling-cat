---
name: lint
description: Auto-fix lint and formatting issues for Python and frontend
disable-model-invocation: true
---

# /lint

Run auto-fix linting and formatting across Python and frontend, then show what changed.

## Steps

1. Run `make lint-fix` (covers Python via ruff):
   ```bash
   make lint-fix
   ```

2. Run frontend lint auto-fix:
   ```bash
   cd frontend && npx next lint --fix > /tmp/frontend-lint.txt 2>&1; echo "EXIT CODE: $?" >> /tmp/frontend-lint.txt
   ```

3. Verify Python formatting is clean:
   ```bash
   make format-check > /tmp/format-check.txt 2>&1; echo "EXIT CODE: $?" >> /tmp/format-check.txt
   ```

4. Show what files changed:
   ```bash
   git diff --stat
   ```

5. Report remaining issues for any check that still fails. Otherwise confirm all clean.
