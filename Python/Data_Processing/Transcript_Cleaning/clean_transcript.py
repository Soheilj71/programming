#!/usr/bin/env python3
"""
===============================================================================
TRANSCRIPT CLEANER (ROBUST PREPROCESSING TOOL)
-------------------------------------------------------------------------------
Author: Soheil Jamali

Description:
    Cleans raw transcripts by removing timestamps and formatting text.

Features:
    - Removes timestamps (MM:SS and HH:MM:SS)
    - Handles timestamps at line start and inline
    - Fixes unicode artifacts (NBSP, dashes)
    - Removes empty lines after cleaning
    - Works on single file or batch folders

Usage:
    python transcript_cleaner.py input.txt output.txt

    OR

    python transcript_cleaner.py input_folder output_folder
===============================================================================
"""

import re
import sys
import os


def fail(msg):
    print(f"[ERROR] {msg}")
    sys.exit(1)


def normalize_text(text):
    """Fix common unicode issues"""
    text = re.sub(r'\xa0', ' ', text)  # non-breaking space
    text = text.replace('\u2013', '-')  # en dash
    text = text.replace('\u2014', '-')  # em dash
    return text


def clean_text(text):
    """Remove timestamps and clean transcript"""

    text = normalize_text(text)

    # Matches MM:SS and HH:MM:SS
    time_pattern = r'\b\d{1,2}:\d{2}(?::\d{2})?\b'

    # Remove timestamps at start of line
    text = re.sub(
        r'^\s*' + time_pattern + r'(\s*[-–—]?\s*)?',
        '',
        text,
        flags=re.MULTILINE
    )

    # Remove timestamps anywhere else
    text = re.sub(time_pattern, '', text)

    # Normalize spacing
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove empty lines
    lines = []
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned != "":
            lines.append(cleaned)

    return "\n".join(lines) + "\n"


def process_file(input_path, output_path):
    if not os.path.exists(input_path):
        fail(f"File not found: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    cleaned = clean_text(text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    print(f"[✔] {input_path} → {output_path}")


def process_folder(input_dir, output_dir):
    if not os.path.isdir(input_dir):
        fail(f"Folder not found: {input_dir}")

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            in_path = os.path.join(input_dir, filename)
            out_path = os.path.join(output_dir, filename)
            process_file(in_path, out_path)


def main():
    if len(sys.argv) != 3:
        print("\nUsage:")
        print("  python transcript_cleaner.py input.txt output.txt")
        print("  OR")
        print("  python transcript_cleaner.py input_folder output_folder\n")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if os.path.isfile(input_path):
        process_file(input_path, output_path)
    elif os.path.isdir(input_path):
        process_folder(input_path, output_path)
    else:
        fail("Input must be a file or folder")


if __name__ == "__main__":
    main()
