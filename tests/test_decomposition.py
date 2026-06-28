"""Tests for claim decomposition functionality."""


class MockLLMAdapter:
    """Mock LLM adapter for testing decomposition."""

    def __init__(self, responses: dict[str, list[str]]) -> None:
        """Initialize mock with predefined responses.

        Args:
            responses: Mapping of claim patterns to sub-claim lists
        """
        self._responses = responses

    def decompose_claim(self, claim: str) -> list[str]:
        """Return predefined sub-claims for known patterns, or echo for unknown."""
        for pattern, subclaims in self._responses.items():
            if pattern in claim:
                return subclaims
        return [claim]  # Echo simple claims


class TestClaimDecomposition:
    """Test claim decomposition behaviors."""

    def test_simple_claim_returns_single_subclaim(self) -> None:
        """Given a simple claim, decomposition should return a single sub-claim."""
        from belling_cat.application.services.decomposition_service import (
            DecompositionService,
        )

        # Mock adapter that echoes simple claims
        adapter = MockLLMAdapter(responses={})
        service = DecompositionService(llm_adapter=adapter)
        claim = "The sky is blue"

        result = service.decompose(claim)

        assert len(result) == 1
        assert result[0].text == "The sky is blue"

    def test_complex_claim_returns_multiple_subclaims(self) -> None:
        """Given a complex multi-faceted claim, decomposition should return multiple sub-claims."""
        from belling_cat.application.services.decomposition_service import (
            DecompositionService,
        )

        # Mock adapter with predefined decomposition
        adapter = MockLLMAdapter(
            responses={
                "elephant": [
                    "An elephant was seen",
                    "The elephant was flying",
                    "The sighting was near Changi Airport",
                    "The sighting occurred yesterday",
                ]
            }
        )
        service = DecompositionService(llm_adapter=adapter)
        claim = "elephant was seen flying near Changi Airport yesterday"

        result = service.decompose(claim)

        assert len(result) == 4
        assert result[0].text == "An elephant was seen"
        assert result[1].text == "The elephant was flying"
        assert result[2].text == "The sighting was near Changi Airport"
        assert result[3].text == "The sighting occurred yesterday"
