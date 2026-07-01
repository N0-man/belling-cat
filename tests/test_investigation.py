"""Tests for evidence investigation functionality."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MockEvidence:
    """Mock evidence for testing."""

    source_url: str
    publication_date: str
    credibility: str
    quote: str


class MockLLMAdapter:
    """Mock LLM adapter for testing investigation."""

    def __init__(self, responses: dict[str, list[MockEvidence]]) -> None:
        """Initialize mock with predefined responses.

        Args:
            responses: Mapping of sub-claim patterns to evidence lists
        """
        self._responses = responses

    def decompose_claim(self, claim: str) -> list[str]:
        """Required by LLMPort protocol (from decomposition)."""
        return [claim]

    def investigate_subclaim(self, subclaim: str) -> tuple[list[MockEvidence], list[str]]:
        """Return predefined evidence for known patterns.

        Returns:
            Tuple of (evidence_list, findings_list)
        """
        for pattern, evidence in self._responses.items():
            if pattern in subclaim:
                findings = [f"Searching for {subclaim}...", f"Found {len(evidence)} sources"]
                return (evidence, findings)
        return ([], ["No evidence found"])


class TestInvestigation:
    """Test evidence investigation behaviors."""

    def test_simple_subclaim_returns_evidence_with_source(self) -> None:
        """Given a sub-claim, investigation should return evidence with source URL."""
        from belling_cat.application.services.investigation_service import (
            InvestigationService,
        )

        # Mock adapter with predefined evidence
        mock_evidence = MockEvidence(
            source_url="https://example.com/article",
            publication_date="2024-01-01",
            credibility="news",
            quote="The sky appears blue due to Rayleigh scattering",
        )
        adapter = MockLLMAdapter(responses={"sky is blue": [mock_evidence]})
        service = InvestigationService(llm_adapter=adapter)

        result = service.investigate("The sky is blue")

        assert len(result) == 1
        assert result[0].source.url == "https://example.com/article"
        assert result[0].source.publication_date == "2024-01-01"
        assert result[0].quote == "The sky appears blue due to Rayleigh scattering"
        assert result[0].timestamp is not None  # Verify timestamp exists

    def test_multiple_sources_with_different_authority_levels(self) -> None:
        """Given a sub-claim with multiple sources, investigation returns multiple evidence with authority levels."""
        from belling_cat.application.services.investigation_service import (
            InvestigationService,
        )

        # Mock adapter with multiple sources at different authority levels
        mock_evidence = [
            MockEvidence(
                source_url="https://nasa.gov/earth-sky-color",
                publication_date="2024-01-01",
                credibility="government",
                quote="Atmospheric scattering causes sky to appear blue",
            ),
            MockEvidence(
                source_url="https://nature.com/rayleigh-scattering",
                publication_date="2024-01-02",
                credibility="academic",
                quote="Rayleigh scattering explains blue sky phenomenon",
            ),
            MockEvidence(
                source_url="https://news.example.com/why-sky-blue",
                publication_date="2024-01-03",
                credibility="news",
                quote="Scientists explain why sky appears blue",
            ),
        ]
        adapter = MockLLMAdapter(responses={"sky is blue": mock_evidence})
        service = InvestigationService(llm_adapter=adapter)

        result = service.investigate("The sky is blue")

        assert len(result) == 3
        assert result[0].source.authority_level == "government"
        assert result[1].source.authority_level == "academic"
        assert result[2].source.authority_level == "news"
        assert result[0].source.url == "https://nasa.gov/earth-sky-color"
        assert result[1].source.url == "https://nature.com/rayleigh-scattering"
        assert result[2].source.url == "https://news.example.com/why-sky-blue"

    def test_investigation_returns_findings_during_search(self) -> None:
        """Given an investigation, service returns real-time findings (progress messages)."""
        from belling_cat.application.services.investigation_service import (
            InvestigationService,
        )

        # Mock adapter with predefined evidence and findings
        mock_evidence = MockEvidence(
            source_url="https://example.com/article",
            publication_date="2024-01-01",
            credibility="news",
            quote="The sky appears blue",
        )
        adapter = MockLLMAdapter(responses={"sky is blue": [mock_evidence]})
        service = InvestigationService(llm_adapter=adapter)

        evidence, findings = service.investigate_with_findings("The sky is blue")

        assert len(evidence) == 1
        assert len(findings) == 2
        assert findings[0].message == "Searching for The sky is blue..."
        assert findings[1].message == "Found 1 sources"
