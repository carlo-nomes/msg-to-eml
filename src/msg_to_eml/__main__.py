"""Main entry point for the MSG to EML converter."""

import argparse
from pathlib import Path
from msg_to_eml import convert_msg_to_eml, batch_convert


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Convert MSG files to EML format")
    parser.add_argument("input", help="Input MSG file or directory containing MSG files")
    parser.add_argument("output", help="Output EML file or directory for EML files")
    parser.add_argument("--batch", action="store_true", help="Batch convert all MSG files in input directory")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    try:
        if args.batch or input_path.is_dir():
            print(f"Batch converting MSG files from {input_path} to {output_path}")
            batch_convert(input_path, output_path)
        else:
            print(f"Converting {input_path} to {output_path}")
            convert_msg_to_eml(input_path, output_path)

        print("Conversion completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
