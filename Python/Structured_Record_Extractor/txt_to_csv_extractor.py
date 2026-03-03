# Purpose: Extract structured data from a text file into a CSV table using user-provided regex patterns.  # Goal.

import argparse  # For command-line options (easy to use from terminal).
import csv  # To write a CSV output file.
import re  # Regex engine: lets us search text patterns like "Temperature: 300".
import sys  # For exiting with error codes.
from pathlib import Path  # Safe file path handling.


def fail(message: str, code: int = 1) -> None:  # Helper to stop with an error message.
    print(f"[ERROR] {message}", file=sys.stderr)  # Print error message.
    sys.exit(code)  # Exit script.


def parse_field(arg: str) -> tuple[str, re.Pattern]:  # Parse a --field argument like NAME=REGEX.
    if "=" not in arg:  # Ensure it has the expected format.
        fail(f'Bad --field "{arg}". Expected format: NAME=REGEX')  # Show user the correct format.

    name, pattern = arg.split("=", 1)  # Split only on the first '=' so regex can contain '=' later.
    name = name.strip()  # Remove spaces around the name.

    if not name:  # Field name cannot be empty.
        fail(f'Bad --field "{arg}". NAME is empty.')  # Explain.

    try:  # Try compiling the regex pattern.
        compiled = re.compile(pattern)  # Compile regex for faster repeated searching.
    except re.error as e:  # If regex is invalid, re.compile throws an error.
        fail(f'Regex error in "{arg}": {e}')  # Explain regex error.

    return name, compiled  # Return (field_name, compiled_regex).


def split_records(text: str, record_sep: str) -> list[str]:  # Split the text into "records" (blocks).
    if record_sep == "blank":  # If user wants blank-line separation...
        # We split on one or more blank lines.  # Common for logs where each job prints a block.
        parts = re.split(r"\n\s*\n+", text.strip())  # Split into blocks.
        return [p for p in parts if p.strip()]  # Remove empty blocks.
    else:  # Otherwise user gave a literal separator string.
        parts = text.split(record_sep)  # Split on the separator string.
        return [p for p in parts if p.strip()]  # Remove empty pieces.


def extract_one_record(record: str, fields: list[tuple[str, re.Pattern]]) -> dict:  # Extract all fields from one record.
    row = {}  # Start an empty dictionary for this record’s extracted values.

    for name, pat in fields:  # Loop over each requested field.
        m = pat.search(record)  # Search the record text for the pattern.
        if m is None:  # If not found...
            row[name] = ""  # Store empty string (so CSV still has a column).
            continue  # Move to next field.

        # If the regex has a capturing group ( ... ), we prefer group(1).  # Example: r"Temp:\s*([0-9.]+)"
        if m.lastindex and m.lastindex >= 1:  # lastindex tells us if there are capture groups.
            row[name] = m.group(1)  # Use the first captured group.
        else:  # If no capturing groups exist...
            row[name] = m.group(0)  # Use the full matched text.

    return row  # Return extracted data for this record.


def write_csv(out_csv: Path, rows: list[dict], field_order: list[str]) -> None:  # Write rows to CSV.
    out_csv.parent.mkdir(parents=True, exist_ok=True)  # Create output folder if needed.

    with out_csv.open("w", newline="", encoding="utf-8") as f:  # Open CSV file.
        writer = csv.DictWriter(f, fieldnames=field_order)  # Create CSV writer with fixed column order.
        writer.writeheader()  # Write header row.
        for row in rows:  # Write each extracted row.
            writer.writerow(row)  # Write row.


def main() -> None:  # Main entry point.
    parser = argparse.ArgumentParser(  # Create the CLI parser.
        description="Extract values from a text file into a CSV using regex patterns."
    )  # Description for --help.

    parser.add_argument("--infile", required=True, help="Input text file (log, output, etc.).")
    parser.add_argument("--out_csv", required=True, help="Output CSV file path.")

    parser.add_argument(  # Add field option (can be repeated).
        "--field",
        action="append",
        default=[],
        help='Field definition in format NAME=REGEX. If REGEX has a capture group, group(1) is saved. '
             'Example: --field temp="Temp:\\s*([0-9.]+)"',
    )

    parser.add_argument(  # How to split file into records.
        "--record_sep",
        default="blank",
        help='How to split file into records: "blank" (default) splits on blank lines, '
             'or provide a literal separator string like "====".',
    )

    args = parser.parse_args()  # Parse arguments.

    infile = Path(args.infile)  # Convert input file path.
    out_csv = Path(args.out_csv)  # Convert output CSV path.

    if not infile.exists():  # Validate input file exists.
        fail(f"Input file not found: {infile}")  # Explain.

    if not args.field:  # Require at least one field.
        fail("You must provide at least one --field NAME=REGEX.")  # Explain.

    fields = [parse_field(x) for x in args.field]  # Compile all field regex patterns.
    field_order = [name for name, _ in fields]  # CSV columns follow the same order user gave.

    text = infile.read_text(encoding="utf-8", errors="replace")  # Read the entire file safely.
    records = split_records(text, args.record_sep)  # Split into records (blocks).

    rows = []  # List to store all extracted rows.
    for rec in records:  # Loop through each record.
        row = extract_one_record(rec, fields)  # Extract requested fields from this record.
        rows.append(row)  # Add row.

    write_csv(out_csv, rows, field_order)  # Save extracted table.

    print(f"Read records: {len(records)}")  # Show how many records were found.
    print(f"Wrote CSV: {out_csv}")  # Confirm output.


if __name__ == "__main__":  # Only run main when executed directly.
    main()  # Run main.
