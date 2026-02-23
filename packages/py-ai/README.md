# py-ai

Unified multi-provider LLM API for Python.

## Features

- 🔌 **Multi-provider support**: OpenAI, Anthropic, Google, and more
- 🎯 **Unified interface**: Same API across all providers
- 🔄 **Streaming support**: Real-time token streaming
- 🛡️ **Error handling**: Automatic retries and fallbacks
- 📊 **Usage tracking**: Token counting and cost estimation

## Installation

```bash
pip install py-ai
```

## Quick Start

```python
from py_ai import LLM

# Initialize with API key
llm = LLM(provider="openai", api_key="sk-...")

# Simple completion
response = llm.complete("What is the meaning of life?")
print(response.content)

# Streaming
for chunk in llm.stream("Tell me a story"):
    print(chunk.content, end="", flush=True)

# With system message
response = llm.complete(
    "Translate to Spanish",
    system="You are a helpful translator",
)
```

## Supported Providers

- OpenAI (GPT-4, GPT-3.5, etc.)
- Anthropic (Claude 3, Claude 2)
- Google (Gemini Pro)
- More coming soon...

## Configuration

```python
from py_ai import LLM, Config

config = Config(
    provider="openai",
    model="gpt-4",
    temperature=0.7,
    max_tokens=1000,
    timeout=30,
)

llm = LLM(config=config)
```

## License

MIT
