"""Tests for web tool handlers."""

import sys
from types import ModuleType
from unittest.mock import AsyncMock, Mock, patch

import pytest
from pig_agent_tools.web.handlers import handle_read_webpage, handle_search_web


def _install_fake_tavily():
    """Inject a fake tavily module into sys.modules so patch() can target it."""
    fake_tavily = ModuleType("tavily")
    fake_tavily.TavilyClient = Mock()
    sys.modules["tavily"] = fake_tavily
    return fake_tavily


@pytest.mark.asyncio
async def test_search_web_success():
    """Test successful web search."""
    mock_response = {
        "results": [
            {
                "title": "Python Tutorial",
                "url": "https://example.com/python",
                "content": "Learn Python programming",
            },
            {
                "title": "Python Docs",
                "url": "https://docs.python.org",
                "content": "Official Python documentation",
            },
        ]
    }

    fake_tavily = _install_fake_tavily()
    try:
        mock_client = Mock()
        mock_client.search.return_value = mock_response
        fake_tavily.TavilyClient.return_value = mock_client

        with patch.dict("os.environ", {"TAVILY_API_KEY": "test-key"}):
            result = await handle_search_web({"query": "Python tutorials", "max_results": 2})

        assert result.ok
        assert "Python Tutorial" in result.data
        assert "https://example.com/python" in result.data
        assert "Learn Python programming" in result.data
    finally:
        sys.modules.pop("tavily", None)


@pytest.mark.asyncio
async def test_search_web_missing_query():
    """Test search with missing query parameter."""
    result = await handle_search_web({})

    assert not result.ok
    assert "Query parameter is required" in result.error


@pytest.mark.asyncio
async def test_search_web_no_api_key():
    """Test search without API key — when tavily is not installed, expect import error."""
    sys.modules.pop("tavily", None)
    with patch.dict("os.environ", {}, clear=True):
        result = await handle_search_web({"query": "test"})

    assert not result.ok
    assert "TAVILY_API_KEY" in result.error or "Tavily" in result.error


@pytest.mark.asyncio
async def test_search_web_no_api_key_with_tavily():
    """Test search without API key when tavily is installed."""
    _install_fake_tavily()
    try:
        with patch.dict("os.environ", {}, clear=True):
            result = await handle_search_web({"query": "test"})

        assert not result.ok
        assert "TAVILY_API_KEY" in result.error
    finally:
        sys.modules.pop("tavily", None)


@pytest.mark.asyncio
async def test_search_web_no_results():
    """Test search with no results."""
    mock_response = {"results": []}

    fake_tavily = _install_fake_tavily()
    try:
        mock_client = Mock()
        mock_client.search.return_value = mock_response
        fake_tavily.TavilyClient.return_value = mock_client

        with patch.dict("os.environ", {"TAVILY_API_KEY": "test-key"}):
            result = await handle_search_web({"query": "nonexistent query"})

        assert result.ok
        assert "No results found" in result.data
    finally:
        sys.modules.pop("tavily", None)


@pytest.mark.asyncio
async def test_search_web_exception():
    """Test search with exception."""
    fake_tavily = _install_fake_tavily()
    try:
        mock_client = Mock()
        mock_client.search.side_effect = Exception("API error")
        fake_tavily.TavilyClient.return_value = mock_client

        with patch.dict("os.environ", {"TAVILY_API_KEY": "test-key"}):
            result = await handle_search_web({"query": "test"})

        assert not result.ok
        assert "Search failed" in result.error
    finally:
        sys.modules.pop("tavily", None)


@pytest.mark.asyncio
async def test_read_webpage_success():
    """Test successful webpage reading."""
    mock_html = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <nav>Navigation</nav>
            <h1>Main Title</h1>
            <p>This is the main content.</p>
            <script>console.log('test');</script>
            <footer>Footer content</footer>
        </body>
    </html>
    """

    mock_response = Mock()
    mock_response.text = mock_html
    mock_response.raise_for_status = Mock()

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        result = await handle_read_webpage({"url": "https://example.com"})

    assert result.ok
    assert "Main Title" in result.data
    assert "main content" in result.data
    assert "Navigation" not in result.data
    assert "Footer content" not in result.data
    assert "console.log" not in result.data


@pytest.mark.asyncio
async def test_read_webpage_missing_url():
    """Test webpage reading with missing URL."""
    result = await handle_read_webpage({})

    assert not result.ok
    assert "URL parameter is required" in result.error


@pytest.mark.asyncio
async def test_read_webpage_invalid_url():
    """Test webpage reading with invalid URL."""
    result = await handle_read_webpage({"url": "not-a-url"})

    assert not result.ok
    assert "must start with http" in result.error


@pytest.mark.asyncio
async def test_read_webpage_http_error():
    """Test webpage reading with HTTP error."""
    import httpx

    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.reason_phrase = "Not Found"

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get.side_effect = httpx.HTTPStatusError(
            "404", request=Mock(), response=mock_response
        )
        mock_client_class.return_value = mock_client

        result = await handle_read_webpage({"url": "https://example.com/notfound"})

    assert not result.ok
    assert "404" in result.error


@pytest.mark.asyncio
async def test_read_webpage_timeout():
    """Test webpage reading with timeout."""
    import httpx

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get.side_effect = httpx.TimeoutException("Timeout")
        mock_client_class.return_value = mock_client

        result = await handle_read_webpage({"url": "https://example.com"})

    assert not result.ok
    assert "timed out" in result.error


@pytest.mark.asyncio
async def test_read_webpage_content_truncation():
    """Test webpage content truncation for long content."""
    long_content = "A" * 15000
    mock_html = f"<html><body><p>{long_content}</p></body></html>"

    mock_response = Mock()
    mock_response.text = mock_html
    mock_response.raise_for_status = Mock()

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        result = await handle_read_webpage({"url": "https://example.com"})

    assert result.ok
    assert "[Content truncated...]" in result.data
    assert len(result.data) <= 10050
