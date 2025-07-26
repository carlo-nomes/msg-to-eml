"""MSG to EML converter functionality."""

import os
from email.message import EmailMessage
from pathlib import Path
from typing import Union
import extract_msg


def convert_msg_to_eml(msg_path: Union[str, Path], eml_path: Union[str, Path]) -> None:
    """
    Convert a MSG file to EML format.

    Args:
        msg_path: Path to the input MSG file
        eml_path: Path to the output EML file

    Raises:
        FileNotFoundError: If the MSG file doesn't exist
        ValueError: If the MSG file is invalid
    """
    msg_path = Path(msg_path)
    eml_path = Path(eml_path)

    if not msg_path.exists():
        raise FileNotFoundError(f"MSG file not found: {msg_path}")

    if not msg_path.suffix.lower() == ".msg":
        raise ValueError(f"File is not a MSG file: {msg_path}")

    # Create output directory if it doesn't exist
    eml_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Parse the MSG file
        msg = extract_msg.Message(str(msg_path))

        # Create email message
        eml_msg = EmailMessage()

        # Set basic headers
        if hasattr(msg, "sender") and msg.sender:
            eml_msg["From"] = msg.sender
        if hasattr(msg, "to") and msg.to:
            eml_msg["To"] = msg.to
        if hasattr(msg, "cc") and msg.cc:
            eml_msg["Cc"] = msg.cc
        if hasattr(msg, "bcc") and msg.bcc:
            eml_msg["Bcc"] = msg.bcc
        if hasattr(msg, "subject") and msg.subject:
            eml_msg["Subject"] = msg.subject
        if hasattr(msg, "date") and msg.date:
            eml_msg["Date"] = msg.date.strftime("%a, %d %b %Y %H:%M:%S %z")

        # Set message body
        if hasattr(msg, "body") and msg.body:
            eml_msg.set_content(msg.body)
        elif hasattr(msg, "htmlBody") and msg.htmlBody:
            eml_msg.set_content(msg.htmlBody, subtype="html")

        # Handle attachments
        if hasattr(msg, "attachments") and msg.attachments:
            for attachment in msg.attachments:
                if hasattr(attachment, "data") and hasattr(attachment, "longFilename"):
                    eml_msg.add_attachment(
                        attachment.data, maintype="application", subtype="octet-stream", filename=attachment.longFilename or "attachment"
                    )

        # Close the MSG file
        msg.close()

        # Write EML file
        with open(eml_path, "w", encoding="utf-8") as f:
            f.write(str(eml_msg))

        print(f"Successfully converted {msg_path} to {eml_path}")

    except Exception as e:
        raise ValueError(f"Failed to convert MSG file: {e}")


def batch_convert(input_dir: Union[str, Path], output_dir: Union[str, Path]) -> None:
    """
    Convert all MSG files in a directory to EML format.

    Args:
        input_dir: Directory containing MSG files
        output_dir: Directory to save EML files
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_path}")

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all MSG files
    msg_files = list(input_path.glob("*.msg"))

    if not msg_files:
        print(f"No MSG files found in {input_path}")
        return

    success_count = 0
    for msg_file in msg_files:
        eml_file = output_path / f"{msg_file.stem}.eml"
        try:
            convert_msg_to_eml(msg_file, eml_file)
            success_count += 1
        except Exception as e:
            print(f"Failed to convert {msg_file}: {e}")

    print(f"Successfully converted {success_count}/{len(msg_files)} MSG files to EML format")
