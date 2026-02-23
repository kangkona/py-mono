# Py-Mono

> Python monorepo toolkit for AI agents and LLM applications

Python equivalent of [pi-mono](https://github.com/badlogic/pi-mono), providing tools for building AI agents and managing LLM deployments.

## Packages

| Package | Status | Description |
|---------|--------|-------------|
| **[py-ai](packages/py-ai)** | ✅ Ready | Unified multi-provider LLM API (OpenAI, Anthropic, Google, etc.) |
| **[py-agent-core](packages/py-agent-core)** | ✅ Ready | Agent runtime with tool calling and state management |
| **[py-coding-agent](packages/py-coding-agent)** | ✅ Ready | Interactive coding agent CLI |
| **[py-tui](packages/py-tui)** | ✅ Ready | Terminal UI library with rich formatting |
| **[py-web-ui](packages/py-web-ui)** | ✅ Ready | Web UI components with FastAPI backend |

## Quick Demo

### Coding Agent with Full Features! 🚀
```bash
# Install and run
export OPENAI_API_KEY=your-key
py-code

# New features:
/session    - Show session info (tree, branches, stats)
/tree       - View conversation tree
/fork name  - Fork session to new branch
/compact    - Compact old messages
/skills     - List available skills
/skill:name - Invoke a skill
```

### Session Management
```python
from py_agent_core import Session

session = Session(name="my-work")
session.add_message("user", "Question 1")
session.add_message("assistant", "Answer 1")

# Branch to earlier point
session.branch_to(earlier_id)
session.add_message("user", "Different question")

# Fork to new session
fork = session.fork(point_id, "alt-approach")
fork.save()
```

### Extensions
```python
# my_extension.py
def extension(api):
    @api.tool(description="Custom tool")
    def my_tool(x: str) -> str:
        return x.upper()
    
    @api.command("stats")
    def stats():
        return "Statistics..."

# Auto-loaded from .agents/extensions/
```

### Skills
```markdown
<!-- .agents/skills/my-skill/SKILL.md -->
# My Skill

Use when user asks about X.

## Steps
1. Do this
2. Then that
```

### Web UI
```bash
py-webui --port 8000
# Open http://localhost:8000
```

## Installation

```bash
# Install from source
git clone <repo-url>
cd py-mono
pip install -e ".[dev]"

# Install all packages
./scripts/install-dev.sh

# Or install specific package
pip install -e packages/py-ai
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install all packages in editable mode
./scripts/install-dev.sh

# Run tests
pytest

# Run linting and formatting
ruff check .
ruff format .

# Type checking
mypy packages/
```

## Project Structure

```
py-mono/
├── packages/
│   ├── py-ai/              # LLM API wrapper
│   ├── py-agent-core/      # Agent runtime
│   ├── py-coding-agent/    # Coding agent CLI
│   ├── py-tui/             # Terminal UI
│   └── py-web-ui/          # Web UI components
├── scripts/                # Build and utility scripts
├── tests/                  # Integration tests
├── pyproject.toml          # Project configuration
└── README.md
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT
