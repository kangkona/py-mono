"""Web tool handlers."""

from typing import Any

from pig_agent_core.tools.base import ToolResult


async def handle_search_web(
    args: dict[str, Any],
    user_id: str | None = None,
    meta: dict[str, Any] | None = None,
    cancel: Any = None,
) -> ToolResult:
    """Handle web search using Tavily API.

    Args:
        args: Tool arguments containing 'query' and optional 'max_results'
        user_id: Optional user identifier
        meta: Optional metadata
        cancel: Optional cancellation token

    Returns:
        ToolResult with search results
    """
    query = args.get("query", "")
    max_results = args.get("max_results", 5)

    if not query:
        return ToolResult(
            ok=False,
            error="Query parameter is required",
        )

    try:
        # Import here to avoid requiring tavily for package installation
        import os

        try:
            from tavily import TavilyClient
        except ImportError:
            return ToolResult(
                ok=False,
                error="Tavily package not installed. Install with: pip install tavily-python",
            )

        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return ToolResult(
                ok=False,
                error="TAVILY_API_KEY environment variable not set",
            )

        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=max_results)

        # Format results
        results = response.get("results", [])
        if not results:
            return ToolResult(ok=True, data="No results found")

        formatted_results = []
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("url", "")
            snippet = result.get("content", "")
            formatted_results.append(f"{i}. {title}\n   URL: {url}\n   {snippet}\n")

        return ToolResult(ok=True, data="\n".join(formatted_results))

    except Exception as e:
        return ToolResult(
            ok=False,
            error=f"Search failed: {str(e)}",
        )


async def handle_read_webpage(
    args: dict[str, Any],
    user_id: str | None = None,
    meta: dict[str, Any] | None = None,
    cancel: Any = None,
) -> ToolResult:
    """Handle webpage reading and content extraction.

    Args:
        args: Tool arguments containing 'url'
        user_id: Optional user identifier
        meta: Optional metadata
        cancel: Optional cancellation token

    Returns:
        ToolResult with extracted webpage content
    """
    url = args.get("url", "")

    if not url:
        return ToolResult(
            ok=False,
            error="URL parameter is required",
        )

    # Basic URL validation
    if not url.startswith(("http://", "https://")):
        return ToolResult(
            ok=False,
            error="URL must start with http:// or https://",
        )

    try:
        # Import here to avoid requiring httpx/bs4 for package installation
        try:
            import httpx
            from bs4 import BeautifulSoup
        except ImportError:
            return ToolResult(
                ok=False,
                error="Required packages not installed. Install with: pip install httpx beautifulsoup4",  # noqa: E501
            )

        # Fetch webpage
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()

        # Parse HTML and extract text
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Get text content
        text = soup.get_text(separator="\n", strip=True)

        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        content = "\n".join(lines)

        if not content:
            return ToolResult(
                ok=False,
                error="No text content found on webpage",
            )

        # Limit content length to avoid overwhelming context
        max_length = 10000
        if len(content) > max_length:
            content = content[:max_length] + "\n\n[Content truncated...]"

        return ToolResult(ok=True, data=content)

    except httpx.HTTPStatusError as e:
        return ToolResult(
            ok=False,
            error=f"HTTP error {e.response.status_code}: {e.response.reason_phrase}",
        )
    except httpx.TimeoutException:
        return ToolResult(
            ok=False,
            error="Request timed out after 30 seconds",
        )
    except Exception as e:
        return ToolResult(
            ok=False,
            error=f"Failed to read webpage: {str(e)}",
        )


# Handler registry
HANDLERS = {
    "search_web": handle_search_web,
    "read_webpage": handle_read_webpage,
}
