#!/usr/bin/env python3
"""
Build script to create a Mac app bundle for the MSG to EML converter.
This script uses PyInstaller to create a standalone .app file.
"""

import subprocess
import sys
import os
from pathlib import Path


def build_mac_app():
    """Build the Mac app using PyInstaller."""

    print("🏗️  Building MSG to EML Converter Mac App...")
    print("=" * 50)

    # Get the current directory
    project_dir = Path(__file__).parent

    # PyInstaller command
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=MSG to EML Converter",
        "--windowed",  # No console window
        "--onedir",  # Create a directory bundle
        "--clean",  # Clean cache
        "--noconfirm",  # Overwrite without asking
        f"--distpath={project_dir}/dist",
        f"--workpath={project_dir}/build",
        f"--specpath={project_dir}",
        str(project_dir / "gui_app.py"),
    ]

    print(f"Running: {' '.join(cmd)}")
    print()

    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        print("✅ Build successful!")
        print(f"📱 App created at: {project_dir}/dist/MSG to EML Converter.app")
        print()
        print("🎉 Your dad can now use the app by:")
        print("1. Double-clicking 'MSG to EML Converter.app'")
        print("2. Using the simple drag-and-drop interface")
        print("3. No need to install Python or any dependencies!")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Main function."""
    if not build_mac_app():
        sys.exit(1)

    print("\n" + "=" * 50)
    print("🚀 Ready to share with your dad!")


if __name__ == "__main__":
    main()
