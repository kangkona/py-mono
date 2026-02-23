#!/bin/bash
# Run tests for all packages

set -e

echo "Running tests..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$REPO_ROOT"

# Run pytest with coverage
pytest tests/ -v --cov=packages --cov-report=term-missing

echo "✓ All tests passed!"
