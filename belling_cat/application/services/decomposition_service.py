"""Claim decomposition service."""

from belling_cat.application.ports.llm import LLMPort
from belling_cat.domain.value_objects import SubClaim


class DecompositionService:
    """Orchestrates claim decomposition using an LLM adapter.

    Application service that coordinates the process of breaking down
    claims into independently verifiable sub-claims.
    """

    def __init__(self, llm_adapter: LLMPort) -> None:
        """Initialize the decomposition service.

        Args:
            llm_adapter: LLM adapter implementing LLMPort protocol
        """
        self._llm_adapter = llm_adapter

    def decompose(self, claim: str) -> list[SubClaim]:
        """Decompose a claim into sub-claims.

        Args:
            claim: The claim text to decompose

        Returns:
            List of SubClaim value objects
        """
        subclaim_texts = self._llm_adapter.decompose_claim(claim)
        return [SubClaim(text=text) for text in subclaim_texts]
