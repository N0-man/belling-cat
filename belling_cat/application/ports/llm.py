"""LLM adapter port interface."""

from dataclasses import dataclass
from typing import Protocol


@dataclass
class RawEvidence:
    """Raw evidence structure returned by LLM adapters."""

    source_url: str
    publication_date: str
    credibility: str
    quote: str


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
