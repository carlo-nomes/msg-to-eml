"""Main entry point for the MSG to EML converter."""

import argparse
import sys
from pathlib import Path
from msg_to_eml import convert_msg_to_eml, batch_convert


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Convert MSG files to EML format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single file
  python -m msg_to_eml email.msg email.eml

  # Batch convert to separate folder
  python -m msg_to_eml input_folder/ output_folder/ --batch

  # Batch convert next to original files
  python -m msg_to_eml input_folder/ --batch --next-to-original

  # Batch convert without recursion
  python -m msg_to_eml input_folder/ output_folder/ --batch --no-recursive
        """,
    )

    parser.add_argument(
        "input", help="Input MSG file or directory containing MSG files"
    )
    parser.add_argument(
        "output",
        nargs="?",
        help="Output EML file or directory for EML files (optional when using --next-to-original)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Batch convert all MSG files in input directory",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        default=True,
        help="Search subdirectories recursively (default: True)",
    )
    parser.add_argument(
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Do not search subdirectories recursively",
    )
    parser.add_argument(
        "--next-to-original",
        action="store_true",
        help="Create EML files next to original MSG files (ignores output path)",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress progress output"
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    # Validate input
    if not input_path.exists():
        print(f"Error: Input path '{input_path}' does not exist", file=sys.stderr)
        return 1

    # Determine if this is batch mode
    is_batch = args.batch or input_path.is_dir()

    # Validate output requirements
    if not args.next_to_original and not args.output:
        if is_batch:
            print(
                "Error: Output directory is required for batch conversion unless using --next-to-original",
                file=sys.stderr,
            )
        else:
            print(
                "Error: Output file path is required for single file conversion",
                file=sys.stderr,
            )
        return 1

    output_path = Path(args.output) if args.output else None

    try:
        if is_batch:
            if not args.quiet:
                if args.next_to_original:
                    print(f"📁 Batch converting MSG files from {input_path}")
                    print("📍 Creating EML files next to original MSG files")
                else:
                    print(
                        f"📁 Batch converting MSG files from {input_path} to {output_path}"
                    )

                if args.recursive:
                    print("🔍 Searching subdirectories recursively...")
                else:
                    print("📂 Searching only in the main directory...")

            stats = batch_convert(
                input_path,
                output_path,
                recursive=args.recursive,
                output_next_to_original=args.next_to_original,
            )

            if not args.quiet:
                _print_batch_results(stats)
        else:
            if not args.quiet:
                print(f"📄 Converting {input_path} to {output_path}")
            assert (
                output_path is not None
            ), "Output path is required for single file conversion"
            convert_msg_to_eml(input_path, output_path)
            if not args.quiet:
                print("✅ Conversion completed successfully!")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

    return 0


def _print_batch_results(stats):
    """Print detailed batch conversion results."""
    print(f"\n📊 Conversion Results:")
    print(f"   MSG files found: {stats['msg_files_found']}")
    print(f"   Successfully converted: {stats['files_converted']}")

    if stats["files_failed"] > 0:
        print(f"   Failed conversions: {stats['files_failed']}")
        if stats.get("failed_files"):
            print("   Failed files:")
            for failed_file in stats["failed_files"][:5]:  # Show max 5
                print(f"     • {Path(failed_file).name}")
            if len(stats["failed_files"]) > 5:
                print(f"     ... and {len(stats['failed_files']) - 5} more")

    if stats["files_ignored"] > 0:
        print(f"   Non-MSG files ignored: {stats['files_ignored']}")

    if stats["files_converted"] > 0:
        print(
            f"\n🎉 Successfully converted {stats['files_converted']} MSG files to EML format!"
        )
    else:
        print(f"\n⚠️  No files were converted.")


if __name__ == "__main__":
    exit(main())
