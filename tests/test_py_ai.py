"""Tests for py-ai package."""

import pytest

from py_ai import LLM, Config, Message


def test_config_creation():
    """Test config creation."""
    config = Config(provider="openai", model="gpt-4")
    assert config.provider == "openai"
    assert config.model == "gpt-4"
    assert config.temperature == 0.7


def test_llm_initialization():
    """Test LLM initialization."""
    llm = LLM(provider="openai", api_key="test-key")
    assert llm.config.provider == "openai"
    assert llm.config.api_key == "test-key"


def test_message_creation():
    """Test message creation."""
    msg = Message(role="user", content="Hello")
    assert msg.role == "user"
    assert msg.content == "Hello"


@pytest.mark.skip(reason="Requires API key")
def test_llm_complete():
    """Test LLM completion (integration test)."""
    llm = LLM(provider="openai")
    response = llm.complete("Say hello")
    assert response.content
    assert response.model
