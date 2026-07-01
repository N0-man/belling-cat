"""Tests for OpenAI LLM adapter."""

import json
import os
from dataclasses import dataclass
from unittest.mock import Mock

import pytest


@dataclass
class RawEvidence:
    """Raw evidence structure from OpenAI adapter."""

    source_url: str
    publication_date: str
    credibility: str
    quote: str


class TestOpenAIAdapter:
    """Test OpenAI adapter integration."""

    def test_adapter_calls_openai_with_correct_model(self) -> None:
        """OpenAI adapter should use GPT-4o mini model for decomposition."""
        from belling_cat.infrastructure.llm.openai_adapter import OpenAIAdapter

        # Mock the OpenAI client
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [
            Mock(message=Mock(content=json.dumps(["sub-claim 1", "sub-claim 2"])))
        ]
        mock_client.chat.completions.create.return_value = mock_response

        adapter = OpenAIAdapter(client=mock_client)
        claim = "Test claim"

        result = adapter.decompose_claim(claim)

        # Verify the adapter called OpenAI with correct model
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == "gpt-4o-mini"
        assert len(result) == 2
        assert result[0] == "sub-claim 1"
        assert result[1] == "sub-claim 2"

    def test_adapter_sends_decomposition_prompt(self) -> None:
        """OpenAI adapter should send appropriate prompt for claim decomposition."""
        from belling_cat.infrastructure.llm.openai_adapter import OpenAIAdapter

        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=json.dumps(["sub-claim"])))]
        mock_client.chat.completions.create.return_value = mock_response

        adapter = OpenAIAdapter(client=mock_client)
        claim = "elephant was seen flying"

        adapter.decompose_claim(claim)

        # Verify prompt mentions decomposition and the claim
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        messages = call_kwargs["messages"]
        assert len(messages) >= 1
        prompt_content = " ".join(msg["content"] for msg in messages)
        assert "decompose" in prompt_content.lower() or "break" in prompt_content.lower()
        assert "elephant was seen flying" in prompt_content

    def test_adapter_investigates_subclaim_with_gpt4(self) -> None:
        """OpenAI adapter should use GPT-4 Turbo for investigation with evidence gathering."""
        from belling_cat.infrastructure.llm.openai_adapter import OpenAIAdapter

        # Mock the OpenAI client
        mock_client = Mock()
        mock_response = Mock()
        evidence_json = json.dumps(
            {
                "evidence": [
                    {
                        "source_url": "https://example.com/article",
                        "publication_date": "2024-01-01",
                        "credibility": "news",
                        "quote": "The sky is blue due to Rayleigh scattering",
                    }
                ],
                "findings": ["Searching for evidence...", "Found 1 authoritative source"],
            }
        )
        mock_response.choices = [Mock(message=Mock(content=evidence_json))]
        mock_client.chat.completions.create.return_value = mock_response

        adapter = OpenAIAdapter(client=mock_client)
        subclaim = "The sky is blue"

        evidence, findings = adapter.investigate_subclaim(subclaim)

        # Verify the adapter called OpenAI with GPT-4 Turbo
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == "gpt-4-turbo"
        assert len(evidence) == 1
        assert evidence[0].source_url == "https://example.com/article"
        assert evidence[0].credibility == "news"
        assert len(findings) == 2


class TestOpenAIAdapterIntegration:
    """End-to-end integration tests with real OpenAI API."""

    @pytest.mark.slow
    @pytest.mark.integration
    @pytest.mark.skipif(
        "OPENAI_API_KEY" not in os.environ,
        reason="Requires OPENAI_API_KEY environment variable",
    )
    def test_real_openai_call_decomposes_claim(self) -> None:
        """End-to-end test: real OpenAI API call decomposes a claim.

        This test makes an actual API call to OpenAI and should only run
        when explicitly enabled (requires OPENAI_API_KEY environment variable).
        """
        from belling_cat.infrastructure.llm.openai_adapter import OpenAIAdapter

        # Use real OpenAI client (requires OPENAI_API_KEY env var)
        adapter = OpenAIAdapter()
        claim = "The Eiffel Tower is in Paris and was completed in 1889"

        result = adapter.decompose_claim(claim)

        # Verify we get a list of sub-claims
        assert isinstance(result, list)
        assert len(result) >= 1
        assert all(isinstance(subclaim, str) for subclaim in result)
        # For this claim, we expect at least 2 sub-claims
        # (location and completion date are separate facts)
        assert len(result) >= 2

    @pytest.mark.slow
    @pytest.mark.integration
    @pytest.mark.skipif(
        "OPENAI_API_KEY" not in os.environ,
        reason="Requires OPENAI_API_KEY environment variable",
    )
    def test_real_openai_call_investigates_subclaim(self) -> None:
        """End-to-end test: real OpenAI API call investigates a sub-claim.

        This test makes an actual API call to OpenAI and should only run
        when explicitly enabled (requires OPENAI_API_KEY environment variable).
        """
        from belling_cat.infrastructure.llm.openai_adapter import OpenAIAdapter

        # Use real OpenAI client
        adapter = OpenAIAdapter()
        subclaim = "The Eiffel Tower is in Paris"

        evidence, findings = adapter.investigate_subclaim(subclaim)

        # Verify we get evidence and findings
        assert isinstance(evidence, list)
        assert isinstance(findings, list)
        assert len(evidence) >= 1
        assert len(findings) >= 1
        # Verify evidence structure
        assert all(hasattr(e, "source_url") for e in evidence)
        assert all(hasattr(e, "credibility") for e in evidence)
        assert all(hasattr(e, "quote") for e in evidence)
