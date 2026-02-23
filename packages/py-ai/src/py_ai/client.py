"""Main LLM client."""

from typing import Iterator, Optional

from .config import Config
from .models import Message, Response, StreamChunk


class LLM:
    """Unified LLM client supporting multiple providers."""

    def __init__(
        self,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        config: Optional[Config] = None,
        **kwargs,
    ):
        """Initialize LLM client.

        Args:
            provider: Provider name (openai, anthropic, google)
            api_key: API key for the provider
            config: Configuration object
            **kwargs: Additional config parameters
        """
        if config is None:
            config_dict = {"provider": provider or "openai"}
            if api_key:
                config_dict["api_key"] = api_key
            config_dict.update(kwargs)
            config = Config(**config_dict)

        self.config = config
        self._provider = self._init_provider()

    def _init_provider(self):
        """Initialize the provider client."""
        # Import providers here to avoid circular imports
        from .providers.openai import OpenAIProvider
        from .providers.anthropic import AnthropicProvider
        from .providers.google import GoogleProvider
        from .providers.azure import AzureOpenAIProvider
        from .providers.groq import GroqProvider
        from .providers.mistral import MistralProvider
        from .providers.openrouter import OpenRouterProvider
        from .providers.bedrock import BedrockProvider
        from .providers.xai import XAIProvider
        from .providers.cerebras import CerebrasProvider
        from .providers.cohere import CohereProvider
        from .providers.perplexity import PerplexityProvider
        from .providers.deepseek import DeepSeekProvider
        from .providers.together import TogetherProvider

        provider_map = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "google": GoogleProvider,
            "azure": AzureOpenAIProvider,
            "groq": GroqProvider,
            "mistral": MistralProvider,
            "openrouter": OpenRouterProvider,
            "bedrock": BedrockProvider,
            "xai": XAIProvider,
            "cerebras": CerebrasProvider,
            "cohere": CohereProvider,
            "perplexity": PerplexityProvider,
            "deepseek": DeepSeekProvider,
            "together": TogetherProvider,
        }

        provider_class = provider_map.get(self.config.provider)
        if not provider_class:
            raise ValueError(f"Unknown provider: {self.config.provider}")

        return provider_class(self.config)

    def complete(
        self,
        prompt: str,
        system: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """Generate a completion.

        Args:
            prompt: User prompt
            system: Optional system message
            **kwargs: Additional parameters

        Returns:
            Response object with content and metadata
        """
        messages = []
        if system:
            messages.append(Message(role="system", content=system))
        messages.append(Message(role="user", content=prompt))

        return self._provider.complete(
            messages=messages,
            model=kwargs.get("model", self.config.model),
            temperature=kwargs.get("temperature", self.config.temperature),
            max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
            **kwargs,
        )

    def stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        **kwargs,
    ) -> Iterator[StreamChunk]:
        """Stream a completion.

        Args:
            prompt: User prompt
            system: Optional system message
            **kwargs: Additional parameters

        Yields:
            StreamChunk objects with content
        """
        messages = []
        if system:
            messages.append(Message(role="system", content=system))
        messages.append(Message(role="user", content=prompt))

        yield from self._provider.stream(
            messages=messages,
            model=kwargs.get("model", self.config.model),
            temperature=kwargs.get("temperature", self.config.temperature),
            max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
            **kwargs,
        )

    def chat(
        self,
        messages: list[Message],
        **kwargs,
    ) -> Response:
        """Generate a chat completion with full message history.

        Args:
            messages: List of Message objects
            **kwargs: Additional parameters

        Returns:
            Response object with content and metadata
        """
        return self._provider.complete(
            messages=messages,
            model=kwargs.get("model", self.config.model),
            temperature=kwargs.get("temperature", self.config.temperature),
            max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
            **kwargs,
        )
