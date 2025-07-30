#!/bin/bash
# Check if Python files need formatting with Black (without changing them)
echo "🔍 Checking Python file formatting..."
.venv/bin/python -m black --check src/ tests/ gui_app.py build_app.py example.py
if [ $? -eq 0 ]; then
    echo "✅ All files are properly formatted!"
else
    echo "❌ Some files need formatting. Run './scripts/format.sh' to fix them."
fi
