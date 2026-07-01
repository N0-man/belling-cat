"""Tests for LangGraph workflow integration."""

import os

import pytest


class TestLangGraphWorkflow:
    """Test LangGraph workflow orchestration."""

    def test_decomposition_node_exists_in_workflow(self) -> None:
        """Workflow should include a claim decomposition node."""
        from belling_cat.application.services.decomposition_service import (
            DecompositionService,
        )
        from belling_cat.infrastructure.langgraph.workflow import create_workflow

        # Create workflow with mock adapter
        class MockAdapter:
            def decompose_claim(self, claim: str) -> list[str]:
                return [claim]

        service = DecompositionService(llm_adapter=MockAdapter())
        workflow = create_workflow(decomposition_service=service)

        # Verify workflow was created successfully
        assert workflow is not None
        # Verify workflow can be invoked (has correct structure)
        result = workflow.invoke({"claim": "test"})
        assert "subclaims" in result

    def test_workflow_executes_decomposition(self) -> None:
        """Workflow should execute claim decomposition when invoked."""
        from belling_cat.application.services.decomposition_service import (
            DecompositionService,
        )
        from belling_cat.infrastructure.langgraph.workflow import create_workflow

        # Mock adapter that returns known sub-claims
        class MockAdapter:
            def decompose_claim(self, claim: str) -> list[str]:
                return ["sub-claim 1", "sub-claim 2"]

        service = DecompositionService(llm_adapter=MockAdapter())
        workflow = create_workflow(decomposition_service=service)
        result = workflow.invoke({"claim": "test claim"})

        # Verify decomposition ran and returned SubClaim domain objects
        assert "subclaims" in result
        assert len(result["subclaims"]) == 2
        # SubClaim value objects, not raw strings
        assert result["subclaims"][0].text == "sub-claim 1"
        assert result["subclaims"][1].text == "sub-claim 2"

    def test_workflow_includes_investigation_node(self) -> None:
        """Workflow should include an investigation node that gathers evidence for sub-claims."""
        from dataclasses import dataclass

        from belling_cat.application.services.decomposition_service import (
            DecompositionService,
        )
        from belling_cat.application.services.investigation_service import (
            InvestigationService,
        )
        from belling_cat.infrastructure.langgraph.workflow import create_workflow

        @dataclass
        class MockEvidence:
            source_url: str
            publication_date: str
            credibility: str
            quote: str

        # Mock adapter
        class MockAdapter:
            def decompose_claim(self, claim: str) -> list[str]:
                return ["sub-claim 1"]

            def investigate_subclaim(self, subclaim: str) -> tuple[list[MockEvidence], list[str]]:
                evidence = [
                    MockEvidence(
                        source_url="https://example.com",
                        publication_date="2024-01-01",
                        credibility="news",
                        quote="Test evidence",
                    )
                ]
                findings = ["Searching...", "Found 1 source"]
                return (evidence, findings)

        decomp_service = DecompositionService(llm_adapter=MockAdapter())
        inv_service = InvestigationService(llm_adapter=MockAdapter())
        workflow = create_workflow(
            decomposition_service=decomp_service, investigation_service=inv_service
        )

        result = workflow.invoke({"claim": "test claim"})

        # Verify investigation ran and returned evidence
        assert "evidence" in result
        assert len(result["evidence"]) >= 1
        assert result["evidence"][0].source.url == "https://example.com"
        assert result["evidence"][0].quote == "Test evidence"

    def test_workflow_includes_verification_node(self) -> None:
        """Workflow should include a verification node that generates verdicts for sub-claims."""
        from dataclasses import dataclass

        from belling_cat.application.services.decomposition_service import (
            DecompositionService,
        )
        from belling_cat.application.services.investigation_service import (
            InvestigationService,
        )
        from belling_cat.application.services.verifier_service import VerifierService
        from belling_cat.domain.value_objects import Evidence, SubClaim
        from belling_cat.infrastructure.langgraph.workflow import create_workflow

        @dataclass
        class MockEvidence:
            source_url: str
            publication_date: str
            credibility: str
            quote: str

        @dataclass
        class MockVerdict:
            category: str
            explanation: str
            confidence: str

        # Mock adapter
        class MockAdapter:
            def decompose_claim(self, claim: str) -> list[str]:
                return ["sub-claim 1"]

            def investigate_subclaim(self, subclaim: str) -> tuple[list[MockEvidence], list[str]]:
                evidence = [
                    MockEvidence(
                        source_url="https://example.com",
                        publication_date="2024-01-01",
                        credibility="government",
                        quote="Test evidence",
                    )
                ]
                findings = ["Searching...", "Found 1 source"]
                return (evidence, findings)

            def verify_claim(
                self, subclaim: SubClaim, evidence: list[Evidence]
            ) -> tuple[MockVerdict, list[str]]:
                verdict = MockVerdict(
                    category="Supported",
                    explanation="Evidence supports this claim",
                    confidence="high",
                )
                return (verdict, [])

        decomp_service = DecompositionService(llm_adapter=MockAdapter())
        inv_service = InvestigationService(llm_adapter=MockAdapter())
        ver_service = VerifierService(llm_adapter=MockAdapter())
        workflow = create_workflow(
            decomposition_service=decomp_service,
            investigation_service=inv_service,
            verifier_service=ver_service,
        )

        result = workflow.invoke({"claim": "test claim"})

        # Verify verification ran and returned verdicts
        assert "verdicts" in result
        assert len(result["verdicts"]) >= 1
        assert result["verdicts"][0].category == "Supported"
        assert result["verdicts"][0].explanation == "Evidence supports this claim"


class TestLangGraphWorkflowIntegration:
    """End-to-end integration tests with real OpenAI API."""

    @pytest.mark.slow
    @pytest.mark.integration
    @pytest.mark.skipif(
        "OPENAI_API_KEY" not in os.environ,
        reason="Requires OPENAI_API_KEY environment variable",
    )
    def test_real_openai_investigation_workflow(self) -> None:
        """End-to-end test: real OpenAI API investigates a claim through the full workflow.

        This test makes actual API calls to OpenAI and should only run
        when explicitly enabled (requires OPENAI_API_KEY environment variable).
        """
        from belling_cat.application.services.decomposition_service import (
            DecompositionService,
        )
        from belling_cat.application.services.investigation_service import (
            InvestigationService,
        )
        from belling_cat.infrastructure.langgraph.workflow import create_workflow
        from belling_cat.infrastructure.llm.openai_adapter import OpenAIAdapter

        # Use real OpenAI adapter
        adapter = OpenAIAdapter()
        decomp_service = DecompositionService(llm_adapter=adapter)
        inv_service = InvestigationService(llm_adapter=adapter)

        workflow = create_workflow(
            decomposition_service=decomp_service, investigation_service=inv_service
        )

        # Test with a simple verifiable claim
        result = workflow.invoke({"claim": "The Eiffel Tower is in Paris"})

        # Verify workflow executed successfully
        assert "subclaims" in result
        assert "evidence" in result
        assert len(result["subclaims"]) >= 1
        assert len(result["evidence"]) >= 1

        # Verify evidence structure
        for evidence in result["evidence"]:
            assert hasattr(evidence, "source")
            assert hasattr(evidence.source, "url")
            assert hasattr(evidence.source, "authority_level")
            assert hasattr(evidence, "quote")
            # Verify authority level is one of expected values
            assert evidence.source.authority_level in [
                "government",
                "academic",
                "news",
                "other",
            ]
