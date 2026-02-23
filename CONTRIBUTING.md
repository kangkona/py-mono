# Contributing to py-mono

Thank you for your interest in contributing to py-mono!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Install development dependencies: `pip install -e ".[dev]"`
4. Install packages: `./scripts/install-dev.sh`

## Development Workflow

### Making Changes

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `./scripts/test.sh`
4. Run linting: `./scripts/lint.sh`
5. Commit your changes: `git commit -m "Description"`
6. Push to your fork: `git push origin feature/your-feature`
7. Create a Pull Request

### Code Style

- Use `ruff` for linting and formatting
- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Write docstrings for all public functions and classes

### Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage

### Running Tests

```bash
# Run all tests
./scripts/test.sh

# Run specific test file
pytest tests/test_py_ai.py

# Run with coverage
pytest --cov=packages --cov-report=html
```

### Code Quality

```bash
# Format code
ruff format packages/

# Lint code
ruff check packages/

# Type check
mypy packages/
```

## Project Structure

```
py-mono/
├── packages/          # Monorepo packages
│   ├── py-ai/        # LLM API wrapper
│   ├── py-agent-core/ # Agent runtime
│   └── ...
├── scripts/          # Build and utility scripts
├── tests/            # Integration tests
└── pyproject.toml    # Project configuration
```

## Adding a New Package

1. Create package directory: `packages/your-package/`
2. Add `pyproject.toml` with package metadata
3. Create `src/your_package/` for source code
4. Add README.md with usage examples
5. Add tests in `tests/test_your_package.py`

## Questions?

Feel free to open an issue for any questions or concerns!
