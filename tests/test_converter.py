"""Tests for MSG to EML converter."""

import pytest
from pathlib import Path
import tempfile
import os

from msg_to_eml.converter import convert_msg_to_eml, batch_convert


class TestConverter:
    """Test cases for the MSG to EML converter."""

    def test_convert_msg_to_eml_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent MSG file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            msg_path = Path(temp_dir) / "nonexistent.msg"
            eml_path = Path(temp_dir) / "output.eml"

            with pytest.raises(FileNotFoundError):
                convert_msg_to_eml(msg_path, eml_path)

    def test_convert_msg_to_eml_invalid_extension(self):
        """Test that ValueError is raised for non-MSG files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a file with wrong extension
            wrong_file = Path(temp_dir) / "test.txt"
            wrong_file.write_text("test content")
            eml_path = Path(temp_dir) / "output.eml"

            with pytest.raises(ValueError):
                convert_msg_to_eml(wrong_file, eml_path)

    def test_convert_msg_to_eml_success(self):
        """Test successful conversion (placeholder implementation)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a mock MSG file (this will fail conversion, but we'll test error handling)
            msg_path = Path(temp_dir) / "test.msg"
            msg_path.write_text("mock msg content")
            eml_path = Path(temp_dir) / "output.eml"

            # This should raise a ValueError due to invalid MSG format
            with pytest.raises(ValueError, match="Failed to convert MSG file"):
                convert_msg_to_eml(msg_path, eml_path)

    def test_batch_convert_no_msg_files(self, capsys):
        """Test batch conversion with no MSG files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "input"
            output_dir = Path(temp_dir) / "output"
            input_dir.mkdir()

            batch_convert(input_dir, output_dir)

            captured = capsys.readouterr()
            assert "No MSG files found" in captured.out

    def test_batch_convert_with_msg_files(self):
        """Test batch conversion with MSG files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "input"
            output_dir = Path(temp_dir) / "output"
            input_dir.mkdir()

            # Create mock MSG files (these will fail conversion)
            (input_dir / "test1.msg").write_text("msg1 content")
            (input_dir / "test2.msg").write_text("msg2 content")

            # This should complete without raising exceptions, but no files will be converted
            batch_convert(input_dir, output_dir)

            # Output directory should be created even if no conversions succeed
            assert output_dir.exists()

    def test_batch_convert_input_dir_not_found(self):
        """Test that FileNotFoundError is raised for non-existent input directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "nonexistent"
            output_dir = Path(temp_dir) / "output"

            with pytest.raises(FileNotFoundError):
                batch_convert(input_dir, output_dir)
