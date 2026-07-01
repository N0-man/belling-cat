"""Verifier service for verdict generation."""

from belling_cat.application.ports.llm import LLMPort
from belling_cat.domain.value_objects import Evidence, SubClaim, Verdict


class VerifierService:
    """Orchestrates verdict generation using an LLM adapter.

    Application service that coordinates the process of verifying
    sub-claims and generating verdicts based on evidence credibility.
    """

    def __init__(self, llm_adapter: LLMPort) -> None:
        """Initialize the verifier service.

        Args:
            llm_adapter: LLM adapter implementing LLMPort protocol
        """
        self._llm_adapter = llm_adapter

    def verify(self, subclaim: SubClaim, evidence: list[Evidence]) -> Verdict:
        """Verify a sub-claim and generate a verdict.

        Args:
            subclaim: The sub-claim to verify
            evidence: Evidence gathered for the sub-claim

        Returns:
            Verdict value object categorizing the claim as
            Supported/Contradicted/Unsupported
        """
        verdict, _contradictions = self.verify_with_contradictions(subclaim, evidence)
        return verdict

    def verify_with_contradictions(
        self, subclaim: SubClaim, evidence: list[Evidence]
    ) -> tuple[Verdict, list[str]]:
        """Verify a sub-claim and return verdict with detected contradictions.

        Args:
            subclaim: The sub-claim to verify
            evidence: Evidence gathered for the sub-claim

        Returns:
            Tuple of (verdict, contradictions) where contradictions is a list
            of contradiction explanations between sources
        """
        raw_verdict, contradictions = self._llm_adapter.verify_claim(subclaim, evidence)

        verdict = Verdict(
            subclaim=subclaim,
            category=raw_verdict.category,
            explanation=raw_verdict.explanation,
        )

        return verdict, contradictions
