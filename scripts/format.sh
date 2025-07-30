#!/bin/bash
# Format all Python files with Black
echo "🎨 Formatting Python files with Black..."
.venv/bin/python -m black src/ tests/ build_app.py example.py
echo "✅ Formatting complete!"
