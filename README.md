# MSG to EML Converter

A Python project for converting MSG files to EML format.

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```python
from msg_to_eml import convert_msg_to_eml

# Convert a single MSG file
convert_msg_to_eml('input.msg', 'output.eml')
```

## Development

Run tests:

```bash
python -m pytest
```

## License

MIT License
