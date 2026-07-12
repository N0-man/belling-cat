---
name: tdd
description: Execute one behavioural Red-Green-Refactor cycle at a time, checkpoint every phase, preserve scope, and leave each cycle in a committed green state.
compatibility: opencode
metadata:
  workflow: implementation
---

# Test-Driven Development

## Core rule

Do not change production behaviour before observing a test fail for the intended missing or incorrect behaviour.

One cycle covers one named behaviour and ends with a green commit:

```text
RED -> GREEN -> REFACTOR -> VERIFY -> COMMIT
```

Do not commit RED separately.

For a pure structural refactor, use existing behavioural protection or add characterization coverage. When the new test passes immediately, demonstrate that it can detect the relevant breakage through a controlled mutation or another credible safety signal rather than manufacturing a fake failure.

## Before a cycle

Read the active story/refactor, PRD or audit report, product backlog, handoff, intent packet, scope baseline, relevant context, design records, ADRs, tests, and code. Confirm:

- the next acceptance criterion, finding, or protected behaviour;
- the value/demo outcome it contributes to;
- the public seam to test;
- current cycle number and workspace state;
- that unrelated baseline changes will not be touched.

## RED

Write the smallest behavioural test. Run the narrowest command and confirm it fails for the expected reason—not syntax, import, fixture, environment, or collection failure. Checkpoint the test, command, and failure evidence.

A test that passes immediately does not establish RED. Determine whether behaviour already exists, the assertion is weak, or the wrong seam was chosen.

## GREEN

Implement only enough code to pass the focused test. Do not anticipate later behaviours. Run the focused test and checkpoint GREEN evidence.

Fix forward within approved intent. Do not delete or revert deliberate functionality merely to make a finding disappear.

## REFACTOR

While green:

- remove duplication and improve names/cohesion;
- keep important business rules separate from delivery and external I/O where practical;
- avoid abstractions, ports, layers, or DDD patterns without a concrete need;
- prefer the smallest root-cause improvement over a line-level patch when the same defect class would otherwise remain;
- preserve accepted structure and decision records;
- check whether implementation revealed a new technical decision or useful domain-language change.

Invoke the `decision-recording` skill when a choice deserves durable rationale. Invoke the `domain-modeling` skill only when language or ownership genuinely changed. A newly discovered product behaviour or scope decision returns to `/discover`.

Run focused tests after meaningful refactoring and checkpoint the result.

## VERIFY

Run focused tests, `test-affected`, and proportionate type/lint/architecture checks. Record commands and results. Full preflight is required at story end, not necessarily every cycle.

Invoke the `scope-guard` skill before commit and confirm the diff contains only the current behaviour or approved repair.

## COMMIT

Use the `commit` skill to create one commit for the complete green cycle, for example:

```text
ITEM-03 Cycle 02: reject an empty claim
```

Checkpoint the commit SHA and update `current_head`. Confirm unrelated baseline changes remain outside the commit. Only then begin the next cycle.

## Completion evidence

Never claim TDD was followed unless each changed behaviour has RED or credible safety evidence, GREEN evidence, refactor consideration, verification evidence, a scoped green commit, and a handoff checkpoint.
