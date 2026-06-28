"""Tests for LangGraph workflow integration."""


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
