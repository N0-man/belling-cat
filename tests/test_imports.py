"""Smoke tests to verify core dependencies are installed and importable."""


def test_can_import_rich():
    """Verify Rich library can be imported."""
    import rich  # noqa: F401


def test_can_import_yachalk():
    """Verify Yachalk library can be imported."""
    import yachalk  # noqa: F401


def test_can_import_openai():
    """Verify OpenAI SDK can be imported."""
    import openai  # noqa: F401


def test_can_import_langgraph():
    """Verify LangGraph library can be imported."""
    import langgraph  # noqa: F401


def test_can_import_pytest():
    """Verify pytest can be imported."""
    import pytest  # noqa: F401


def test_can_import_pytest_asyncio():
    """Verify pytest-asyncio can be imported."""
    import pytest_asyncio  # noqa: F401
