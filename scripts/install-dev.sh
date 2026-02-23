#!/bin/bash
# Install all packages in development mode

set -e

echo "Installing py-mono packages in development mode..."

# Get the script directory and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$REPO_ROOT"

# Install each package in editable mode
for pkg in packages/*/; do
    if [ -f "$pkg/pyproject.toml" ]; then
        echo "Installing $(basename "$pkg")..."
        pip install -e "$pkg"
    fi
done

echo "✓ All packages installed successfully!"
