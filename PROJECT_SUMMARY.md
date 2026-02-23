# py-mono Project Summary

## 📦 What is py-mono?

`py-mono` is a Python monorepo toolkit for building AI agents and LLM applications, inspired by [badlogic/pi-mono](https://github.com/badlogic/pi-mono).

## 🎯 Project Goals

1. Provide a unified, Pythonic interface for multiple LLM providers
2. Enable rapid development of AI agents and tools
3. Offer reusable components for terminal and web UIs
4. Maintain clean, type-safe, well-tested code

## 📁 Project Structure

```
py-mono/
├── packages/                    # Monorepo packages
│   ├── py-ai/                  # ✅ LLM API wrapper (READY)
│   │   ├── src/py_ai/
│   │   │   ├── __init__.py
│   │   │   ├── client.py       # Main LLM client
│   │   │   ├── config.py       # Configuration
│   │   │   ├── models.py       # Data models
│   │   │   ├── providers.py    # Provider interface
│   │   │   └── providers/      # Provider implementations
│   │   │       ├── openai.py   # ✅ OpenAI (complete)
│   │   │       ├── anthropic.py # 🚧 Anthropic (placeholder)
│   │   │       └── google.py   # 🚧 Google (placeholder)
│   │   ├── tests/
│   │   ├── README.md
│   │   └── pyproject.toml
│   ├── py-agent-core/          # 🚧 Agent runtime (TODO)
│   ├── py-coding-agent/        # 🚧 Coding agent CLI (TODO)
│   ├── py-tui/                 # 🚧 Terminal UI (TODO)
│   └── py-web-ui/              # 🚧 Web UI components (TODO)
├── scripts/                    # Build and utility scripts
│   ├── install-dev.sh         # Install all packages
│   ├── test.sh                # Run tests
│   └── lint.sh                # Run linting
├── tests/                      # Integration tests
├── examples/                   # Usage examples
│   └── basic_usage.py
├── docs/                       # Documentation
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── ARCHITECTURE.md
│   └── CONTRIBUTING.md
├── pyproject.toml             # Root project config
├── LICENSE                    # MIT License
└── .gitignore
```

## ✅ Current Status

### Completed (Phase 1a)

- ✅ Project structure and configuration
- ✅ `py-ai` package with:
  - Unified LLM client interface
  - OpenAI provider (complete)
  - Sync and async support
  - Streaming support
  - Type hints throughout
- ✅ Development tooling:
  - pytest for testing
  - ruff for linting/formatting
  - mypy for type checking
- ✅ Documentation:
  - README with overview
  - QUICKSTART guide
  - ARCHITECTURE documentation
  - CONTRIBUTING guidelines
- ✅ Build scripts:
  - `install-dev.sh` - Install packages
  - `test.sh` - Run tests
  - `lint.sh` - Code quality checks
- ✅ Example code

### In Progress (Phase 1b)

- 🚧 Anthropic provider implementation
- 🚧 Google provider implementation
- 🚧 Comprehensive test coverage
- 🚧 Error handling and retries

### Planned (Phase 2+)

- 📋 `py-agent-core`: Agent runtime with tool calling
- 📋 `py-coding-agent`: Interactive coding agent CLI
- 📋 `py-tui`: Terminal UI library
- 📋 `py-web-ui`: Web UI components
- 📋 Integration examples
- 📋 CI/CD pipeline
- 📋 Package publishing to PyPI

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd py-mono
pip install -e ".[dev]"
./scripts/install-dev.sh

# Try it out
export OPENAI_API_KEY="your-key"
python examples/basic_usage.py

# Run tests
./scripts/test.sh

# Check code quality
./scripts/lint.sh
```

## 💡 Usage Example

```python
from py_ai import LLM

# Initialize
llm = LLM(provider="openai", api_key="sk-...")

# Simple completion
response = llm.complete("What is Python?")
print(response.content)

# Streaming
for chunk in llm.stream("Tell me a story"):
    print(chunk.content, end="")
```

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Type Checking | mypy |
| Linting | ruff |
| Testing | pytest |
| Validation | pydantic |
| HTTP Client | httpx |
| Build Tool | hatchling |
| Async | asyncio |

## 📊 Comparison: pi-mono vs py-mono

| Feature | pi-mono | py-mono |
|---------|---------|---------|
| Language | TypeScript | Python |
| Runtime | Node.js | Python |
| Package Manager | npm workspaces | pip + editable installs |
| Type System | TypeScript | Type hints + mypy |
| Build System | tsc + esbuild | hatchling |
| Testing | Jest/Vitest | pytest |
| Linting | Biome | ruff |
| Async Pattern | async/await | asyncio |

## 📈 Roadmap

### Phase 1: Foundation (Current)
- [x] Project setup
- [x] py-ai package structure
- [x] OpenAI provider
- [ ] Additional providers
- [ ] Comprehensive tests

### Phase 2: Core Features
- [ ] py-agent-core with tool calling
- [ ] State management
- [ ] Memory/context handling
- [ ] Multi-turn conversations

### Phase 3: User Interfaces
- [ ] py-coding-agent CLI
- [ ] py-tui terminal library
- [ ] py-web-ui components
- [ ] Interactive examples

### Phase 4: Production Ready
- [ ] CI/CD pipeline
- [ ] PyPI publishing
- [ ] Performance optimizations
- [ ] Comprehensive documentation
- [ ] Community contributions

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Testing requirements
- PR process

## 📝 Key Design Decisions

1. **Monorepo Structure**: Easier development and sharing of common code
2. **Provider Abstraction**: Unified interface across LLM providers
3. **Type Safety**: Full type hints for better IDE support and fewer bugs
4. **Async First**: Both sync and async APIs for flexibility
5. **Pydantic Models**: Runtime validation and great developer experience

## 🔗 Resources

- **Inspiration**: [pi-mono](https://github.com/badlogic/pi-mono)
- **Documentation**: See `docs/` directory
- **Examples**: See `examples/` directory
- **Tests**: See `tests/` directory

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

**Built with ❤️ for the Python AI community**
