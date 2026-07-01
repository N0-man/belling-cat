"""OpenAI LLM adapter implementation."""

import json
from typing import TYPE_CHECKING

from openai import OpenAI

from belling_cat.application.ports.llm import RawEvidence, RawVerdict

if TYPE_CHECKING:
    from belling_cat.domain.value_objects import Evidence, SubClaim


class OpenAIAdapter:
    """Adapter for OpenAI's GPT models implementing LLMPort protocol.

    Translates application-level decomposition requests into OpenAI API calls.
    """

    def __init__(self, client: OpenAI | None = None) -> None:
        """Initialize the OpenAI adapter.

        Args:
            client: Optional OpenAI client instance (creates default if not provided)
        """
        self._client = client if client is not None else OpenAI()

    def decompose_claim(self, claim: str) -> list[str]:
        """Decompose a claim into sub-claims using GPT-4o mini.

        Args:
            claim: The claim text to decompose

        Returns:
            List of sub-claim text strings
        """
        system_prompt = (
            "You are a fact-checking assistant. Break down the given claim into "
            "discrete, independently verifiable sub-claims. Each sub-claim should be "
            "a single fact that can be verified separately. Return ONLY a JSON array "
            "of strings, where each string is a sub-claim. For simple single-fact "
            "claims, return an array with one element."
        )

        user_prompt = f"Decompose this claim into verifiable sub-claims: {claim}"

        response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,  # Deterministic for testing
        )

        content = response.choices[0].message.content
        if content is None:
            return [claim]  # Fallback to original claim if no response

        try:
            subclaims = json.loads(content)
            if isinstance(subclaims, list) and all(isinstance(s, str) for s in subclaims):
                return subclaims
        except json.JSONDecodeError:
            pass

        # Fallback: return original claim if parsing fails
        return [claim]

    def investigate_subclaim(self, subclaim: str) -> tuple[list[RawEvidence], list[str]]:
        """Investigate a sub-claim and gather evidence using GPT-4 Turbo.

        Args:
            subclaim: The sub-claim text to investigate

        Returns:
            Tuple of (evidence_list, findings_list) where evidence contains
            RawEvidence objects and findings contains progress messages
        """
        system_prompt = (
            "You are a fact-checking investigator. For the given sub-claim, "
            "search for evidence from authoritative sources. Return ONLY a JSON object with:\n"
            '{\n  "evidence": [\n    {\n      "source_url": "URL of the source",\n'
            '      "publication_date": "YYYY-MM-DD",\n'
            '      "credibility": "government" or "academic" or "news" or "other",\n'
            '      "quote": "specific quote or fact from the source"\n    }\n  ],\n'
            '  "findings": ["progress message 1", "progress message 2"]\n}\n'
            "Include multiple evidence items from different authority levels if available."
        )

        user_prompt = f"Investigate this sub-claim and find evidence: {subclaim}"

        response = self._client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,  # Deterministic for testing
        )

        content = response.choices[0].message.content
        if content is None:
            return ([], ["No evidence found"])

        try:
            data = json.loads(content)
            if isinstance(data, dict) and "evidence" in data and "findings" in data:
                evidence_list = [
                    RawEvidence(
                        source_url=e["source_url"],
                        publication_date=e["publication_date"],
                        credibility=e["credibility"],
                        quote=e["quote"],
                    )
                    for e in data["evidence"]
                ]
                findings = data["findings"]
                return (evidence_list, findings)
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

        # Fallback: return empty evidence if parsing fails
        return ([], ["No evidence found"])

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
        # Prepare evidence summary for the prompt
        evidence_summary = []
        for i, ev in enumerate(evidence, 1):
            evidence_summary.append(
                f"Source {i}: {ev.source.url} ({ev.source.authority_level}, "
                f"{ev.source.publication_date})\nQuote: {ev.quote}"
            )
        evidence_text = "\n\n".join(evidence_summary)

        system_prompt = (
            "You are a fact-checking verifier. Assess the credibility of evidence "
            "and generate a verdict for the given sub-claim. Use the authority hierarchy: "
            "government > academic > established news > other. "
            "Detect contradictions between sources and explain them. "
            "Return ONLY a JSON object with:\n"
            '{\n  "verdict": {\n'
            '    "category": "Supported" or "Contradicted" or "Unsupported",\n'
            '    "explanation": "explanation of the verdict",\n'
            '    "confidence": "high" or "medium" or "low"\n  },\n'
            '  "contradictions": ["contradiction explanation 1", ...]\n}\n'
            "Categories:\n"
            "- Supported: Multiple authoritative sources agree with the claim\n"
            "- Contradicted: Authoritative sources directly refute the claim\n"
            "- Unsupported: Insufficient authoritative evidence (not proven false)"
        )

        user_prompt = (
            f"Sub-claim: {subclaim.text}\n\nEvidence:\n{evidence_text}\n\n"
            "Assess the credibility and generate a verdict."
        )

        response = self._client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,  # Deterministic for testing
        )

        content = response.choices[0].message.content
        if content is None:
            return (
                RawVerdict(
                    category="Unsupported",
                    explanation="Unable to verify claim",
                    confidence="low",
                ),
                [],
            )

        try:
            data = json.loads(content)
            if isinstance(data, dict) and "verdict" in data and "contradictions" in data:
                verdict_data = data["verdict"]
                verdict = RawVerdict(
                    category=verdict_data["category"],
                    explanation=verdict_data["explanation"],
                    confidence=verdict_data["confidence"],
                )
                contradictions = data["contradictions"]
                return (verdict, contradictions)
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

        # Fallback: return Unsupported verdict if parsing fails
        return (
            RawVerdict(
                category="Unsupported",
                explanation="Unable to verify claim",
                confidence="low",
            ),
            [],
        )
