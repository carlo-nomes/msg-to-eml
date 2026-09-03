#!/bin/bash
# Build script for msg-to-eml application

set -e

echo "🔨 Building msg-to-eml..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ src/msg_to_eml.egg-info/

# Install in development mode for testing
echo "📦 Installing in development mode..."
.venv/bin/pip install -e .

# Run tests
echo "🧪 Running tests..."
.venv/bin/python -m pytest tests/ -v

# Build wheel for distribution
echo "🏗️  Building distribution packages..."
.venv/bin/python -m build

echo "✅ Build complete!"
echo "📦 Distribution files:"
ls -la dist/
