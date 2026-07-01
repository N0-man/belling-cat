# Item 04: Verifier Agent & Verdict Display with User Approval

## Status

doing

## Parent

.scratch/belling-cat-mvp/PRD.md

## What to build

Implement the Verifier Agent that assesses source credibility, detects contradictions, and generates a verdict for each sub-claim. The verdict categorizes claims as Supported, Contradicted, or Unsupported based on evidence quality.

After generating the verdict, the system displays findings to the user, highlights ambiguous claims or contradictions, and asks for user approval or review before proceeding to save.

## Acceptance criteria

- [ ] LangGraph workflow node created for Verifier Agent
- [ ] Agent uses GPT-4o (strong reasoning model) for nuanced credibility assessment
- [ ] Source credibility assessed using hierarchy: government > academic > news > other
- [ ] Contradictions between sources detected and flagged with explanations
- [ ] Verdict generated for each sub-claim: Supported / Contradicted / Unsupported
- [ ] Unsupported claims marked as "lacking evidence" (not proven false)
- [ ] Verdict displayed to user with clear formatting (Rich panels/tables)
- [ ] Ambiguous claims or contradictions highlighted for user review
- [ ] User prompted for approval/acknowledgment before proceeding
- [ ] Integration test verifies verdict generation logic with mocked evidence
- [ ] End-to-end test verifies user prompt and approval flow

## Blocked by

Item 03
