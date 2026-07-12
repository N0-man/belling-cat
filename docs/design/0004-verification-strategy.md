# Verification Strategy

**Status:** Accepted
**Related PRD:** [belling-cat-mvp](../../.scratch/belling-cat-mvp/PRD.md)

## Decision

Use LLM-based credibility assessment with hierarchy (government > academic > established news > other).

Associate evidence with specific sub-claims during investigation. Each sub-claim verified independently with its relevant evidence.

Include confidence levels (high, medium, low) in verdicts.

## Why

PRD requires credibility hierarchy for source assessment and contradiction detection (PRD Requirements 14-16).

Evidence association and confidence added per validation findings (F-002, F-004) to ensure independent verification of sub-claims and transparency about verdict certainty.
