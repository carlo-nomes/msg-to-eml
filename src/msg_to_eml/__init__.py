"""MSG to EML Converter Package"""

__version__ = "0.1.0"

from .converter import convert_msg_to_eml, batch_convert

__all__ = ["convert_msg_to_eml", "batch_convert"]
