#!/usr/bin/env python3
"""
===============================================================================
REMOVE SELECTED LINES FROM TEXT FILE
-------------------------------------------------------------------------------
Purpose:
    Remove specific lines or ranges of lines from a text file.

Supports:
    - Single lines:        1,5,10
    - Ranges:              3-8
    - Mixed:               1,3-5,10

Usage:
    python remove_lines.py input.txt output.txt --remove "1,3-5,10"

    # In-place modification
    python remove_lines.py input.txt --remove "1,3-5,10" --inplace

Notes:
    - Line numbering starts at 1 (human-friendly)
    - Large files supported (stream processing)
===============================================================================
"""

import argparse
from pathlib import Path
import sys


def parse_line_spec(spec):
    """
    Convert string like "1,3-5,10" into a set of line numbers.
    """
    lines_to_remove = set()

    for part in spec.split(","):
        part = part.strip()

        if "-" in part:
            start, end = part.split("-")
            start, end = int(start), int(end)

            if start > end:
                raise ValueError(f"Invalid range: {part}")

            lines_to_remove.update(range(start, end + 1))
        else:
            lines_to_remove.add(int(part))

    return lines_to_remove


def remove_lines(input_path, output_path, lines_to_remove):
    """
    Remove selected lines from file using streaming (memory efficient).
    """
    with input_path.open("r") as fin, output_path.open("w") as fout:
        for i, line in enumerate(fin, start=1):
            if i not in lines_to_remove:
                fout.write(line)


def main():
    parser = argparse.ArgumentParser(
        description="Remove specific lines or ranges from a text file."
    )

    parser.add_argument("input", type=Path, help="Input file path")
    parser.add_argument("output", type=Path, nargs="?", help="Output file path")
    parser.add_argument(
        "--remove",
        required=True,
        help='Lines to remove (e.g. "1,3-5,10")',
    )
    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Modify file in place",
    )

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    try:
        lines_to_remove = parse_line_spec(args.remove)
    except Exception as e:
        print(f"Error parsing line specification: {e}")
        sys.exit(1)

    if args.inplace:
        temp_path = args.input.with_suffix(".tmp")

        try:
            remove_lines(args.input, temp_path, lines_to_remove)
            temp_path.replace(args.input)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    else:
        if args.output is None:
            print("Error: Provide output file or use --inplace.")
            sys.exit(1)

        try:
            remove_lines(args.input, args.output, lines_to_remove)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    print("Done.")


if __name__ == "__main__":
    main()
