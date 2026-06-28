"""Tests for OpenAI LLM adapter."""

import json
import os
from unittest.mock import Mock

import pytest


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
