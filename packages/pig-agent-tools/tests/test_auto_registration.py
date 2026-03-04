"""Integration tests for tool auto-registration."""

import pytest
from pig_agent_core.tools import _global_registry
from pig_agent_tools.web import register_tools


def test_register_tools_with_global_registry():
    """Test registering web tools with global registry."""
    # Clear global registry first
    with _global_registry._lock:
        _global_registry._handlers.clear()
        _global_registry._schemas.clear()
        _global_registry._core_tools.clear()
        _global_registry._discovered.clear()

    # Register web tools
    registered = register_tools()

    # Verify tools were registered
    assert "search_web" in registered
    assert "read_webpage" in registered
    assert len(registered) == 2

    # Verify tools are in global registry
    with _global_registry._lock:
        assert "search_web" in _global_registry._handlers
        assert "read_webpage" in _global_registry._handlers
        assert "search_web" in _global_registry._schemas
        assert "read_webpage" in _global_registry._schemas


def test_register_tools_with_new_registry():
    """Test registering web tools with new ToolRegistry."""
    from pig_agent_core.tools.registry import ToolRegistry

    new_registry = ToolRegistry()

    # Register web tools with new registry
    registered = register_tools(new_registry)

    # Verify tools were registered
    assert "search_web" in registered
    assert "read_webpage" in registered

    # Verify tools are in new registry
    with new_registry._lock:
        assert "search_web" in new_registry._handlers
        assert "read_webpage" in new_registry._handlers


def test_register_tools_with_old_registry_raises_error():
    """Test that registering with old ToolRegistry raises helpful error."""
    from pig_agent_core.registry import ToolRegistry as OldToolRegistry

    old_registry = OldToolRegistry()

    # Should raise TypeError with helpful message
    with pytest.raises(TypeError, match="old ToolRegistry API"):
        register_tools(old_registry)


def test_register_tools_idempotent():
    """Test that registering tools multiple times is safe."""
    from pig_agent_core.tools.registry import ToolRegistry

    registry = ToolRegistry()

    # Register tools twice
    registered1 = register_tools(registry)
    registered2 = register_tools(registry)

    # Both should return the same tools
    assert registered1 == registered2

    # Registry should still have correct tools
    with registry._lock:
        assert "search_web" in registry._handlers
        assert "read_webpage" in registry._handlers


def test_handlers_can_be_called_directly():
    """Test that handlers can be used without registration."""
    import asyncio
    from unittest.mock import Mock, patch

    from pig_agent_tools.web import handle_search_web

    # Mock Tavily API
    mock_response = {
        "results": [
            {
                "title": "Test Result",
                "url": "https://example.com",
                "content": "Test content",
            }
        ]
    }

    with patch("tavily.TavilyClient") as mock_client_class:
        mock_client = Mock()
        mock_client.search.return_value = mock_response
        mock_client_class.return_value = mock_client

        with patch.dict("os.environ", {"TAVILY_API_KEY": "test-key"}):
            result = asyncio.run(
                handle_search_web(
                    {"query": "test", "max_results": 1},
                    user_id="test_user",
                    meta={},
                )
            )

    # Verify result
    assert result.ok
    assert "Test Result" in result.data
