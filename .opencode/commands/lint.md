---
description: Check repository lint and formatting; pass --fix to apply scoped fixes
agent: build
---

Use the `lint` skill. Without `--fix`, run non-mutating lint and format checks. With `--fix`, establish scope protection and apply fixes only to explicit paths or the active story scope; do not sweep unrelated files.

Arguments: optional paths and `--fix`.

$ARGUMENTS
