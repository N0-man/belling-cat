# Item 04: Verifier Service Layer Implementation

## Status

done

## Parent

.scratch/belling-cat-mvp/PRD.md

## What to build

Implement the Verifier Agent service layer that assesses source credibility, detects contradictions, and generates a verdict for each sub-claim. The verdict categorizes claims as Supported, Contradicted, or Unsupported based on evidence quality.

This story covers the domain, application, and infrastructure layers for verification, including LangGraph workflow integration and CLI display functions (not yet integrated into the user-facing workflow).

## Acceptance criteria

- [x] LangGraph workflow node created for Verifier Agent
- [x] Agent uses GPT-4o (strong reasoning model) for nuanced credibility assessment
- [x] Source credibility assessed using hierarchy: government > academic > news > other
- [x] Contradictions between sources detected and flagged with explanations
- [x] Verdict generated for each sub-claim: Supported / Contradicted / Unsupported
- [x] Unsupported claims marked as "lacking evidence" (not proven false)
- [x] Verdict display functions implemented with Rich panels/tables (not yet integrated)
- [x] Contradiction highlighting functions implemented (not yet integrated)
- [x] User approval prompt functions implemented (not yet integrated)
- [x] Integration test verifies verdict generation logic with mocked evidence
- [ ] **Deferred to Item 04.1:** End-to-end CLI integration and workflow improvements

## Demonstration evidence

**Commit:** 7e6af8b "Item 04: Verifier Agent & Verdict Display with User Approval"

**Domain layer:**
- `belling_cat/domain/value_objects.py:50-61` - Verdict value object (immutable, frozen dataclass)

**Application layer:**
- `belling_cat/application/services/verifier_service.py` - VerifierService with verify() and verify_with_contradictions()
- `belling_cat/application/ports/llm.py:20-26` - RawVerdict DTO and verify_claim() port method

**Infrastructure layer:**
- `belling_cat/infrastructure/llm/openai_adapter.py:125-212` - GPT-4o verification implementation
- `belling_cat/infrastructure/langgraph/workflow.py:79-107` - Verification node

**CLI layer:**
- `belling_cat/cli.py:70-120` - display_verdicts() and prompt_for_approval() functions

**Tests:**
- `tests/test_verification.py` - 4 tests covering all verdict categories and contradiction detection
- `tests/test_openai_adapter.py:108-151` - GPT-4o adapter verification test
- `tests/test_langgraph_workflow.py:105-174` - Workflow integration test
- `tests/test_cli.py:238-312` - Display and approval function tests

## Scope clarification (2026-07-12)

After validation, it was determined that the original Item 04 scope was too large. This story is now scoped as "service layer implementation" and marked complete. The following items are deferred to Item 04.1:

**Deferred to Item 04.1:**
- CLI integration (wiring display functions to investigate_handler)
- Evidence-to-subclaim association in workflow state
- Confidence field in Verdict domain model
- Contradiction propagation fix in workflow
- End-to-end integration test

## Blocked by

Item 03
