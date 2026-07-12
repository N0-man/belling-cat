---
description: Resolve approved behaviour-preserving audit findings through scoped committed TDD refactoring
agent: build
---

Use the `finding-triage` skill, the `scope-guard` skill, and the `refactor` skill.

Only findings classified as in-intent behaviour-preserving repairs are eligible. If a finding requires a product, contract, dependency, or material architecture decision, route it through `/discover`, `/record-decision`, or a focused user decision instead.

Arguments: audit report path plus one or more finding IDs, or a narrowly defined refactoring target.

$ARGUMENTS
