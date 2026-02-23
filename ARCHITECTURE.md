# py-mono Architecture

## Overview

`py-mono` is a Python monorepo inspired by [pi-mono](https://github.com/badlogic/pi-mono), designed to provide a unified toolkit for building AI agents and LLM applications.

## Design Principles

1. **Modular Design**: Each package is independently usable
2. **Provider Agnostic**: Unified interface across LLM providers
3. **Type Safety**: Full type hints and mypy compliance
4. **Async Support**: Both sync and async APIs
5. **Developer Experience**: Clear APIs and comprehensive docs

## Package Structure

### py-ai (Core LLM API)

**Purpose**: Unified multi-provider LLM API

**Key Components**:
- `LLM`: Main client class
- `Config`: Configuration management
- `Provider`: Base provider interface
- Provider implementations: OpenAI, Anthropic, Google

**Design Pattern**: Strategy pattern for providers

```python
# Usage
llm = LLM(provider="openai", api_key="...")
response = llm.complete("Hello")
```

### py-agent-core (Coming Soon)

**Purpose**: Agent runtime with tool calling

**Planned Features**:
- Tool/function calling
- State management
- Multi-turn conversations
- Memory/context handling

### py-coding-agent (Coming Soon)

**Purpose**: Interactive coding agent CLI

**Planned Features**:
- File system operations
- Code generation and editing
- Shell command execution
- Interactive chat interface

### py-tui (Coming Soon)

**Purpose**: Terminal UI library

**Planned Features**:
- Differential rendering
- Rich text support
- Interactive components
- Event handling

### py-web-ui (Coming Soon)

**Purpose**: Web components for AI interfaces

**Planned Features**:
- Chat interface components
- Streaming support
- Markdown rendering
- Code highlighting

## Data Flow

```
User Input
    ↓
LLM Client (py-ai)
    ↓
Provider (OpenAI/Anthropic/Google)
    ↓
API Request
    ↓
Response/Stream
    ↓
Parsed Response
    ↓
User Output
```

## Technology Stack

- **Python**: 3.10+
- **HTTP Client**: httpx
- **Validation**: pydantic
- **Async**: asyncio
- **Testing**: pytest
- **Linting**: ruff
- **Type Checking**: mypy

## Comparison with pi-mono

| Feature | pi-mono (TypeScript) | py-mono (Python) |
|---------|---------------------|------------------|
| Language | TypeScript/Node.js | Python |
| Package Manager | npm workspaces | pip + local packages |
| Type System | TypeScript | Type hints + mypy |
| Async | Native async/await | asyncio |
| Build | tsc | hatchling |
| Testing | Jest/Vitest | pytest |

## Future Roadmap

### Phase 1 (Current)
- ✅ Basic project structure
- ✅ py-ai package with OpenAI support
- 🚧 Additional provider implementations
- 🚧 Comprehensive tests

### Phase 2
- py-agent-core with tool calling
- py-coding-agent CLI
- Integration examples

### Phase 3
- py-tui for terminal interfaces
- py-web-ui for web interfaces
- Advanced agent capabilities

### Phase 4
- Community contributions
- Plugin system
- Performance optimizations
- Production-ready releases

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
