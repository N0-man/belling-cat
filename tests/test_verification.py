"""Tests for verdict verification functionality."""

from dataclasses import dataclass

from belling_cat.domain.value_objects import Evidence, Source, SubClaim


@dataclass(frozen=True)
class MockVerdict:
    """Mock verdict structure returned by LLM adapters."""

    category: str  # "Supported", "Contradicted", or "Unsupported"
    explanation: str
    confidence: str  # "high", "medium", "low"


class MockLLMAdapter:
    """Mock LLM adapter for testing verification."""

    def __init__(self, verdict: MockVerdict, contradictions: list[str] | None = None) -> None:
        """Initialize mock with predefined verdict.

        Args:
            verdict: The verdict to return for verification
            contradictions: Optional list of contradiction explanations
        """
        self._verdict = verdict
        self._contradictions = contradictions or []

    def decompose_claim(self, claim: str) -> list[str]:
        """Required by LLMPort protocol (from decomposition)."""
        return [claim]

    def investigate_subclaim(self, subclaim: str) -> tuple[list, list[str]]:
        """Required by LLMPort protocol (from investigation)."""
        return ([], [])

    def verify_claim(
        self, subclaim: SubClaim, evidence: list[Evidence]
    ) -> tuple[MockVerdict, list[str]]:
        """Return predefined verdict.

        Args:
            subclaim: The sub-claim to verify
            evidence: Evidence gathered for the sub-claim

        Returns:
            Tuple of (verdict, contradictions)
        """
        return (self._verdict, self._contradictions)


class TestVerification:
    """Test verdict verification behaviors."""

    def test_supported_claim_returns_supported_verdict(self) -> None:
        """Given a sub-claim with supporting evidence, verifier should return Supported verdict."""
        from belling_cat.application.services.verifier_service import VerifierService

        # Create sub-claim and supporting evidence
        subclaim = SubClaim(text="The sky is blue")
        evidence = [
            Evidence(
                source=Source(
                    url="https://nasa.gov/earth-sky-color",
                    authority_level="government",
                    publication_date="2024-01-01",
                ),
                quote="Atmospheric scattering causes sky to appear blue",
                timestamp="2024-01-01T12:00:00Z",
            )
        ]

        # Mock adapter with Supported verdict
        mock_verdict = MockVerdict(
            category="Supported",
            explanation="Multiple authoritative sources confirm this claim",
            confidence="high",
        )
        adapter = MockLLMAdapter(verdict=mock_verdict)
        service = VerifierService(llm_adapter=adapter)

        # Verify claim
        result = service.verify(subclaim, evidence)

        assert result.category == "Supported"
        assert result.explanation == "Multiple authoritative sources confirm this claim"
        assert result.subclaim == subclaim

    def test_contradicted_claim_returns_contradicted_verdict(self) -> None:
        """Given a sub-claim with contradicting evidence, verifier should return Contradicted verdict."""
        from belling_cat.application.services.verifier_service import VerifierService

        # Create sub-claim and contradicting evidence
        subclaim = SubClaim(text="The moon landing was faked")
        evidence = [
            Evidence(
                source=Source(
                    url="https://nasa.gov/apollo-missions",
                    authority_level="government",
                    publication_date="2024-01-01",
                ),
                quote="Apollo 11 successfully landed on the moon in 1969",
                timestamp="2024-01-01T12:00:00Z",
            ),
            Evidence(
                source=Source(
                    url="https://science.edu/moon-landing-evidence",
                    authority_level="academic",
                    publication_date="2024-01-02",
                ),
                quote="Physical evidence confirms moon landing authenticity",
                timestamp="2024-01-01T12:00:00Z",
            ),
        ]

        # Mock adapter with Contradicted verdict
        mock_verdict = MockVerdict(
            category="Contradicted",
            explanation="Authoritative sources directly contradict this claim",
            confidence="high",
        )
        adapter = MockLLMAdapter(verdict=mock_verdict)
        service = VerifierService(llm_adapter=adapter)

        # Verify claim
        result = service.verify(subclaim, evidence)

        assert result.category == "Contradicted"
        assert result.explanation == "Authoritative sources directly contradict this claim"
        assert result.subclaim == subclaim

    def test_unsupported_claim_returns_unsupported_verdict(self) -> None:
        """Given a sub-claim with insufficient evidence, verifier should return Unsupported verdict."""
        from belling_cat.application.services.verifier_service import VerifierService

        # Create sub-claim with weak/insufficient evidence
        subclaim = SubClaim(text="Ancient aliens built the pyramids")
        evidence = [
            Evidence(
                source=Source(
                    url="https://blog.example.com/ancient-aliens",
                    authority_level="other",
                    publication_date="2024-01-01",
                ),
                quote="Some theorists suggest alien involvement",
                timestamp="2024-01-01T12:00:00Z",
            )
        ]

        # Mock adapter with Unsupported verdict
        mock_verdict = MockVerdict(
            category="Unsupported",
            explanation="Insufficient authoritative evidence to verify this claim",
            confidence="low",
        )
        adapter = MockLLMAdapter(verdict=mock_verdict)
        service = VerifierService(llm_adapter=adapter)

        # Verify claim
        result = service.verify(subclaim, evidence)

        assert result.category == "Unsupported"
        assert result.explanation == "Insufficient authoritative evidence to verify this claim"
        assert result.subclaim == subclaim

    def test_contradicting_sources_detected_and_flagged(self) -> None:
        """Given evidence with contradicting sources, verifier should detect contradictions."""
        from belling_cat.application.services.verifier_service import VerifierService

        # Create sub-claim with contradicting evidence from different sources
        subclaim = SubClaim(text="Coffee is unhealthy")
        evidence = [
            Evidence(
                source=Source(
                    url="https://health.gov/coffee-study-1",
                    authority_level="government",
                    publication_date="2024-01-01",
                ),
                quote="Coffee consumption linked to health benefits",
                timestamp="2024-01-01T12:00:00Z",
            ),
            Evidence(
                source=Source(
                    url="https://health.gov/coffee-study-2",
                    authority_level="government",
                    publication_date="2024-01-02",
                ),
                quote="Excessive coffee consumption may have negative effects",
                timestamp="2024-01-01T12:00:00Z",
            ),
        ]

        # Mock adapter with contradictions
        contradictions = [
            "Source 1 (health.gov/coffee-study-1) states coffee has health benefits, "
            "while Source 2 (health.gov/coffee-study-2) suggests negative effects"
        ]
        mock_verdict = MockVerdict(
            category="Unsupported",
            explanation="Sources contradict each other, claim is ambiguous",
            confidence="low",
        )
        adapter = MockLLMAdapter(verdict=mock_verdict, contradictions=contradictions)
        service = VerifierService(llm_adapter=adapter)

        # Verify claim and get contradictions
        result, detected_contradictions = service.verify_with_contradictions(subclaim, evidence)

        assert result.category == "Unsupported"
        assert len(detected_contradictions) == 1
        assert "health.gov/coffee-study-1" in detected_contradictions[0]
        assert "health.gov/coffee-study-2" in detected_contradictions[0]
