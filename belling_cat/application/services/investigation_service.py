"""Investigation service for evidence gathering."""

from datetime import UTC, datetime

from belling_cat.application.ports.llm import LLMPort
from belling_cat.domain.value_objects import Evidence, Finding, Source


class InvestigationService:
    """Orchestrates evidence gathering using an LLM adapter.

    Application service that coordinates the process of investigating
    sub-claims and gathering evidence from authoritative sources.
    """

    def __init__(self, llm_adapter: LLMPort) -> None:
        """Initialize the investigation service.

        Args:
            llm_adapter: LLM adapter implementing LLMPort protocol
        """
        self._llm_adapter = llm_adapter

    def investigate(self, subclaim: str) -> list[Evidence]:
        """Investigate a sub-claim and gather evidence.

        Args:
            subclaim: The sub-claim text to investigate

        Returns:
            List of Evidence value objects with sources
        """
        raw_evidence, _findings = self._llm_adapter.investigate_subclaim(subclaim)

        # Get current timestamp for investigation
        timestamp = datetime.now(UTC).isoformat()

        # Convert raw evidence to domain Evidence objects
        evidence_list = []
        for raw in raw_evidence:
            source = Source(
                url=raw.source_url,
                authority_level=raw.credibility,
                publication_date=raw.publication_date,
            )
            evidence = Evidence(source=source, quote=raw.quote, timestamp=timestamp)
            evidence_list.append(evidence)

        return evidence_list

    def investigate_with_findings(self, subclaim: str) -> tuple[list[Evidence], list[Finding]]:
        """Investigate a sub-claim and return evidence with progress findings.

        Args:
            subclaim: The sub-claim text to investigate

        Returns:
            Tuple of (evidence_list, findings_list) where findings contains
            real-time progress updates
        """
        raw_evidence, finding_messages = self._llm_adapter.investigate_subclaim(subclaim)

        # Get current timestamp for investigation
        timestamp = datetime.now(UTC).isoformat()

        # Convert raw evidence to domain Evidence objects
        evidence_list = []
        for raw in raw_evidence:
            source = Source(
                url=raw.source_url,
                authority_level=raw.credibility,
                publication_date=raw.publication_date,
            )
            evidence = Evidence(source=source, quote=raw.quote, timestamp=timestamp)
            evidence_list.append(evidence)

        # Convert finding messages to Finding objects
        findings = [Finding(message=msg) for msg in finding_messages]

        return evidence_list, findings
