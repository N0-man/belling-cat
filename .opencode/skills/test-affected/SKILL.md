---
name: test-affected
description: Find and run tests affected by recent changes
disable-model-invocation: true
---

# /test-affected

Find tests affected by current changes and run them.

## Arguments

- Optional: specific file path(s) to find affected tests for
- If no argument given, uses `git diff --name-only HEAD` to detect changed files

## Steps

1. Find affected tests:
   ```bash
   # If file argument provided:
   python scripts/affected_tests.py <file_args>
   # Otherwise, from git diff:
   git diff --name-only HEAD | python scripts/affected_tests.py
   ```

2. If no affected tests found, report that and exit.

3. Run the affected tests with output redirect:
   ```bash
   uv run pytest <affected_test_files> --tb=short -q > /tmp/pytest-output.txt 2>&1; echo "EXIT CODE: $?" >> /tmp/pytest-output.txt
   ```

4. Parse results:
   ```bash
   python scripts/parse_test_results.py
   ```

5. Report pass/fail counts. If failures, show the failing test names and suggest running them individually for debugging.
