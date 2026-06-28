"""LLM adapter port interface."""

from typing import Protocol


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
