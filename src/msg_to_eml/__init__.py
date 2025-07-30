"""MSG to EML Converter Package

A professional CLI/GUI application for converting Microsoft Outlook MSG files
to standard EML format that can be opened by any email client.
"""

__version__ = "1.0.0"

from .converter import convert_msg_to_eml, batch_convert

__all__ = ["convert_msg_to_eml", "batch_convert"]
