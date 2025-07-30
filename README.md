# MSG to EML Converter

A Python application for converting Microsoft Outlook MSG files to standard EML format, featuring both command-line and graphical interfaces.

*Created by Carlo & Alex (AI Assistant)*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Dual Interface**: Both CLI and GUI applications
- **Batch Processing**: Convert multiple files at once
- **Flexible Output**: Choose output location or place next to originals
- **Cross-Platform**: Works on macOS, Linux, and Windows
- **Homebrew Ready**: Easy installation via Homebrew (coming soon)

## Installation

### From Source

1. Clone this repository:

   ```bash
   git clone https://github.com/carlo-nomes/msg-to-eml.git
   cd msg-to-eml
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or .venv\Scripts\activate on Windows
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

### Via Homebrew (Coming Soon)

```bash
brew install msg-to-eml
```

## Usage

### Command Line Interface

The CLI provides comprehensive options for converting MSG files with flexible output control.

#### Basic Usage

```bash
# Convert a single MSG file
msg-to-eml email.msg email.eml

# Batch convert all MSG files in a directory to separate output folder
msg-to-eml input_folder/ output_folder/ --batch

# Batch convert with EML files created next to original MSG files
msg-to-eml input_folder/ --batch --next-to-original
```

#### Advanced Options

```bash
# Convert without searching subdirectories
msg-to-eml input_folder/ output_folder/ --batch --no-recursive

# Quiet mode (suppress progress output)
msg-to-eml input_folder/ output_folder/ --batch --quiet

# View all available options
msg-to-eml --help
```

### Graphical User Interface

Launch the GUI application:

```bash
msg-to-eml-gui
```

The GUI provides:

- **Simple Interface**: Drag-and-drop or browse for files
- **Batch Processing**: Select directories for bulk conversion
- **Output Options**: Choose between separate folder or next-to-original placement
- **Real-time Progress**: Visual feedback during conversion
- **Detailed Results**: Summary of converted, failed, and ignored files

### Python API

```python
from msg_to_eml import convert_msg_to_eml, batch_convert

# Convert a single MSG file
convert_msg_to_eml('input.msg', 'output.eml')

# Batch convert with options
stats = batch_convert(
    input_dir='msg_files/',
    output_dir='eml_files/',
    recursive=True,
    output_next_to_original=False
)

print(f"Converted {stats['files_converted']} files")
```

## Development

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Running Tests

```bash
python -m pytest
```

### Code Formatting

This project uses [Black](https://black.readthedocs.io/) for code formatting with pre-commit hooks.

```bash
# Check if files need formatting
./scripts/check-format.sh

# Format all Python files
./scripts/format.sh
```

### Building for Distribution

```bash
./scripts/build.sh
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and formatting checks
5. Submit a pull request

## Authors

- **Carlo** - Project lead and implementation
- **Alex** - AI Assistant for development and documentation

## License

MIT License - see the [LICENSE](LICENSE) file for details.
