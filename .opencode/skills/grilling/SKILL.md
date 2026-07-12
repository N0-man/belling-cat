---
name: grilling
description: Resolve a design or discovery tree one dependency-aware question at a time while continually restating shared understanding and a recommended default.
compatibility: opencode
metadata:
  workflow: discovery
---

# Grilling

Ask exactly one question per response.

Use this shape:

```text
What I understand:
<brief, cumulative understanding>

My recommendation:
<the preferred default and why>

Question:
<one question only>
```

Then stop.

## Question order

Resolve the highest-impact uncertainty whose answer influences later decisions. Usually move through:
1. intended outcome and actor;
2. observable behaviour and boundaries;
3. failures and edge cases;
4. domain concepts and ownership;
5. integration and data contracts;
6. architecture, stack, deployment, security, and NFRs;
7. testing seam and acceptance evidence;
8. deferred scope.

The order is adaptive, not a questionnaire.

## Rules

- Inspect the codebase instead of asking codebase-answerable questions.
- Challenge contradictions and overloaded language immediately.
- Offer a concrete recommendation; do not outsource every decision to the user.
- Ask architecture questions when they materially shape this increment, even when they do not block the very next behaviour question.
- Keep the increment small, but do not split away behaviour required for a coherent user outcome.
- Record confirmed product understanding for PRD synthesis, and use the `decision-recording` skill or the `domain-modeling` skill for durable decisions and language.
- When the user signals completion, evaluate the discovery Definition of Ready. If a blocker remains, ask the single blocking question; otherwise present the approval summary and one approval question.
