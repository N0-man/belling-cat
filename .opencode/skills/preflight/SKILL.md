---
name: preflight
description: Run full CI-equivalent preflight checks (lint, format, tests, coverage)
disable-model-invocation: true
---

# /preflight

Run the full CI-equivalent preflight check suite and report results.

## Steps

1. Run `make preflight` with output redirected:
   ```bash
   make preflight > /tmp/preflight-output.txt 2>&1; echo "EXIT CODE: $?" >> /tmp/preflight-output.txt
   ```

2. Check the exit code at the end of the output file.

3. If exit code is 0: Report success with a summary of what passed.

4. If exit code is non-zero: Read the output file, identify which check(s) failed, and provide actionable fix suggestions:
   - Lint failures → `make lint-fix`
   - Format failures → `uv run ruff format`
   - Test failures → show failing tests, suggest running them individually
   - Coverage failures → identify uncovered lines, suggest adding tests
   - Frontend failures → `cd frontend && npx next lint --fix` or `npx tsc --noEmit`

5. Show a concise pass/fail summary.
