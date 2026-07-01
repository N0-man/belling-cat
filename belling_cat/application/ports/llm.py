"""LLM adapter port interface."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from belling_cat.domain.value_objects import Evidence, SubClaim


@dataclass
class RawEvidence:
    """Raw evidence structure returned by LLM adapters."""

    source_url: str
    publication_date: str
    credibility: str
    quote: str


@dataclass
class RawVerdict:
    """Raw verdict structure returned by LLM adapters."""

    category: str  # "Supported", "Contradicted", or "Unsupported"
    explanation: str
    confidence: str  # "high", "medium", "low"


class LLMPort(Protocol):
    """Interface for LLM adapters used in claim decomposition and investigation.

    Implementations should integrate with specific LLM providers (OpenAI, etc.)
    """

    def decompose_claim(self, claim: str) -> list[str]:
        """Decompose a claim into independently verifiable sub-claims.

        Args:
            claim: The claim text to decompose

        Returns:
            List of sub-claim text strings
        """
        ...

    def investigate_subclaim(self, subclaim: str) -> tuple[list[RawEvidence], list[str]]:
        """Investigate a sub-claim and gather evidence from authoritative sources.

        Args:
            subclaim: The sub-claim text to investigate

        Returns:
            Tuple of (evidence_list, findings_list) where evidence contains
            RawEvidence objects and findings contains progress messages
        """
        ...

    def verify_claim(
        self, subclaim: "SubClaim", evidence: list["Evidence"]
    ) -> tuple[RawVerdict, list[str]]:
        """Verify a sub-claim using gathered evidence and assess credibility.

        Args:
            subclaim: The sub-claim to verify
            evidence: Evidence gathered for the sub-claim

        Returns:
            Tuple of (verdict, contradictions) where verdict is a RawVerdict
            and contradictions is a list of contradiction explanations
        """
        ...
