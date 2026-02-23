"""Anthropic provider implementation (placeholder)."""

from typing import AsyncIterator, Iterator, Optional

from ..config import Config
from ..models import Message, Response, StreamChunk
from ..providers import Provider


class AnthropicProvider(Provider):
    """Anthropic provider implementation."""

    def __init__(self, config: Config):
        """Initialize Anthropic provider."""
        self.config = config
        # TODO: Initialize Anthropic client
        raise NotImplementedError("Anthropic provider not yet implemented")

    def complete(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Response:
        """Generate a completion."""
        raise NotImplementedError("Anthropic provider not yet implemented")

    def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Iterator[StreamChunk]:
        """Stream a completion."""
        raise NotImplementedError("Anthropic provider not yet implemented")
        yield  # Make this a generator

    async def acomplete(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> Response:
        """Async generate a completion."""
        raise NotImplementedError("Anthropic provider not yet implemented")

    async def astream(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> AsyncIterator[StreamChunk]:
        """Async stream a completion."""
        raise NotImplementedError("Anthropic provider not yet implemented")
        yield  # Make this an async generator
