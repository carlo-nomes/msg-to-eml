"""MSG to EML converter functionality.

This module provides functionality to convert Microsoft Outlook MSG files
to standard EML format that can be opened by any email client.
"""

from email.message import EmailMessage
from pathlib import Path
from typing import Dict, List, Optional, Union
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


def _get_output_path(msg_file: Path, input_path: Path, output_path: Optional[Path], recursive: bool, output_next_to_original: bool) -> Path:
    """Determine the output path for a given MSG file."""
    if output_next_to_original:
        return msg_file.with_suffix(".eml")

    assert output_path is not None, "output_path must be provided when not outputting next to original"

    if recursive:
        relative_path = msg_file.relative_to(input_path)
        eml_file = output_path / relative_path.with_suffix(".eml")
        # Create subdirectories if needed
        eml_file.parent.mkdir(parents=True, exist_ok=True)
        return eml_file
    else:
        return output_path / f"{msg_file.stem}.eml"


def _filter_non_msg_files(all_files: List[Path]) -> List[Path]:
    """Filter out non-MSG files, excluding hidden and system files."""
    non_msg_files = []
    for file_path in all_files:
        if file_path.is_file() and file_path.suffix.lower() != ".msg" and not file_path.name.startswith(".") and not file_path.name.startswith("~"):
            non_msg_files.append(file_path)
    return non_msg_files


def batch_convert(
    input_dir: Union[str, Path], output_dir: Optional[Union[str, Path]] = None, recursive: bool = True, output_next_to_original: bool = False
) -> Dict[str, Union[int, List[str], bool]]:
    """
    Convert all MSG files in a directory to EML format.

    Args:
        input_dir: Directory containing MSG files
        output_dir: Directory to save EML files (ignored if output_next_to_original=True)
        recursive: Whether to search subdirectories recursively
        output_next_to_original: If True, create EML files next to original MSG files

    Returns:
        Dictionary with conversion statistics including:
        - msg_files_found: Number of MSG files found
        - files_converted: Number of files successfully converted
        - files_failed: Number of files that failed conversion
        - files_ignored: Number of non-MSG files ignored
        - failed_files: List of failed file paths
        - ignored_files: List of ignored file paths
        - recursive: Whether recursive search was used

    Raises:
        FileNotFoundError: If input directory doesn't exist
        ValueError: If output_dir is required but not provided
    """
    input_path = Path(input_dir)

    if not output_next_to_original:
        if output_dir is None:
            raise ValueError("output_dir must be provided when output_next_to_original=False")
        output_path = Path(output_dir)
    else:
        output_path = None  # Will be set for each file individually

    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_path}")

    # Create output directory only if we're using a separate output directory
    if output_path is not None:
        output_path.mkdir(parents=True, exist_ok=True)

    # Find all MSG files (recursively or just in current directory)
    file_pattern = "*.msg"
    if recursive:
        msg_files = list(input_path.rglob(file_pattern))
        all_files = list(input_path.rglob("*"))
    else:
        msg_files = list(input_path.glob(file_pattern))
        all_files = list(input_path.glob("*"))

    # Count non-MSG files (excluding directories and system files)
    non_msg_files = _filter_non_msg_files(all_files)
    ignored_count = len(non_msg_files)

    if not msg_files:
        stats = {
            "msg_files_found": 0,
            "files_converted": 0,
            "files_failed": 0,
            "files_ignored": ignored_count,
            "ignored_files": [str(f) for f in non_msg_files],
            "recursive": recursive,
        }
        print(f"No MSG files found in {input_path}")
        if ignored_count > 0:
            print(f"⚠️  {ignored_count} non-MSG files ignored")
        return stats

    success_count = 0
    failed_files = []

    for msg_file in msg_files:
        try:
            eml_file = _get_output_path(msg_file, input_path, output_path, recursive, output_next_to_original)
            convert_msg_to_eml(msg_file, eml_file)
            success_count += 1
        except Exception as e:
            print(f"Failed to convert {msg_file}: {e}")
            failed_files.append(str(msg_file))

    # Print summary
    print(f"Successfully converted {success_count}/{len(msg_files)} MSG files to EML format")
    if ignored_count > 0:
        print(f"⚠️  {ignored_count} non-MSG files ignored")
    if recursive:
        print(f"📁 Searched recursively in subdirectories")

    return {
        "msg_files_found": len(msg_files),
        "files_converted": success_count,
        "files_failed": len(failed_files),
        "files_ignored": ignored_count,
        "failed_files": failed_files,
        "ignored_files": [str(f) for f in non_msg_files],
        "recursive": recursive,
    }
