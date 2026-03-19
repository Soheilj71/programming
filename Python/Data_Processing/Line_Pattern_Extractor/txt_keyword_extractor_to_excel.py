"""
GOAL 
---------------------------
This program takes ANY text file (.txt, .log, etc.), asks you what words or patterns
you want to search for, finds every line that contains them, and then saves the results
into an Excel file (or CSV if Excel writing is not possible).

You can use it for:
- Searching logs for "ERROR", "WARNING", "finished", "nan", etc.
- Extracting lines that contain specific phrases
- Extracting lines that match a pattern (regex)

IMPORTANT NOTE about "keywords"
-------------------------------
This script treats every "keyword" you enter as a REGULAR EXPRESSION (regex) pattern.

- If you type a simple word like: ERROR
  it works like a normal keyword search.

- If you type a regex like: time\\s*=\\s*(\\d+\\.\\d+)
  it can match complex patterns.

If you do not want regex behavior, you can still safely type plain words.
"""

import argparse   # Helps us read command-line options like --in and --out
import os         # Helps us work with files/folders (paths, checking if file exists)
import re         # Regular expressions (pattern matching)
import sys        # For exiting with error codes and printing errors cleanly


# -----------------------------
# 1) Ask the user for keywords
# -----------------------------
def prompt_user_keywords() -> list[str]:
    """
    Ask the user to type keywords/patterns in the terminal.

    The user will type one keyword per line.
    When the user presses ENTER on an empty line, we stop collecting keywords.

    Returns:
        A list of strings (each string is one keyword/pattern).
    """
    print("\n============================================================")
    print("KEYWORD / PATTERN INPUT")
    print("============================================================")
    print("Enter keywords or regex patterns to extract from the file.")
    print("Type ONE per line.")
    print("When you are done, press ENTER on an empty line.\n")
    print("Examples:")
    print("  ERROR")
    print("  WARNING")
    print("  KL\\(P_real")
    print("  time\\s*=\\s*(?P<value>[0-9.+\\-eE]+)")
    print("============================================================\n")

    keywords: list[str] = []

    while True:
        user_text = input("keyword/regex> ").strip()

        # If the user enters nothing, that means "I'm done"
        if user_text == "":
            break

        keywords.append(user_text)

    return keywords


# ------------------------------------
# 2) Convert keywords to regex patterns
# ------------------------------------
def compile_patterns(keywords: list[str], ignore_case: bool) -> list[tuple[str, re.Pattern]]:
    """
    Turn each user keyword into a compiled regex pattern.

    Why compile?
    - Compiled regex patterns run faster
    - Compiling also checks if a regex is valid

    Args:
        keywords: list of user-provided patterns (strings)
        ignore_case: if True, match without caring about upper/lowercase

    Returns:
        A list of (keyword_string, compiled_regex_pattern)
    """
    # Regex flags control matching options.
    # IGNORECASE makes "error" match "ERROR", "Error", etc.
    flags = re.IGNORECASE if ignore_case else 0

    compiled: list[tuple[str, re.Pattern]] = []

    for kw in keywords:
        try:
            pattern = re.compile(kw, flags)
        except re.error as e:
            # This happens if the user types an invalid regex like "("
            raise ValueError(f"Invalid regex pattern: {kw}\nRegex error: {e}")

        compiled.append((kw, pattern))

    return compiled


# --------------------------------------------
# 3) Search the file line-by-line for patterns
# --------------------------------------------
def extract_matches(lines: list[str],
                    patterns: list[tuple[str, re.Pattern]],
                    context_lines: int) -> list[dict]:
    """
    Look through each line of the file.
    If a line matches any keyword/pattern, record that match as a row in a table.

    Args:
        lines: list of lines from the input file (each line includes newline char usually)
        patterns: list of (keyword_text, compiled_regex_pattern)
        context_lines: number of lines to include before and after the match for context

    Returns:
        rows: list of dictionaries, each dictionary is one "row" for the output table
    """
    rows: list[dict] = []
    match_id = 0  # we will count matches starting from 1

    total_lines = len(lines)

    # Enumerate gives us both index and line content.
    # i is 0-based index (first line has i=0), but humans prefer 1-based line numbers.
    for i, line in enumerate(lines):
        # For each line, try every pattern
        for keyword_text, pattern in patterns:
            # pattern.search(line) checks if the pattern appears anywhere in the line
            if pattern.search(line):
                match_id += 1

                # Decide context window bounds safely (do not go below 0 or above total_lines)
                before_start = max(0, i - context_lines)
                after_end = min(total_lines, i + context_lines + 1)

                # Join the context lines into a single multi-line string
                context_before = "".join(lines[before_start:i]).rstrip("\n")
                context_after = "".join(lines[i + 1:after_end]).rstrip("\n")

                # Save one row (dictionary) for this match
                rows.append({
                    "match_id": match_id,
                    "keyword": keyword_text,      # the keyword/pattern that matched
                    "line_number": i + 1,         # convert 0-based index to 1-based line number
                    "line_text": line.rstrip("\n"),
                    "context_before": context_before,
                    "context_after": context_after,
                })

                # NOTE:
                # If a line matches multiple patterns, you will get multiple rows,
                # one per (line, keyword) match. That is usually what you want.

    return rows


# -----------------------------------------
# 4) Write results to Excel, or fallback CSV
# -----------------------------------------
def write_excel_or_csv(rows: list[dict], out_path: str):
    """
    Try to save rows to an Excel file first (requires pandas + openpyxl).
    If that fails, save as CSV (built-in Python, no extra packages required).

    Args:
        rows: list of row dictionaries (from extract_matches)
        out_path: output file path requested by user, usually ends with .xlsx
    """
    # Create the output directory if it doesn't exist.
    # Example: if out_path is "results/output.xlsx", ensure "results/" exists.
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)

    # Define a stable column order for the output table
    columns = ["match_id", "keyword", "line_number", "line_text", "context_before", "context_after"]

    # First try Excel using pandas.
    try:
        import pandas as pd  # Only available if user installed pandas

        df = pd.DataFrame(rows, columns=columns)

        # ExcelWriter chooses the correct engine automatically in many cases.
        # Typically it uses "openpyxl" for .xlsx.
        with pd.ExcelWriter(out_path) as writer:
            df.to_excel(writer, index=False, sheet_name="Extracted")

        print(f"[OK] Wrote Excel: {out_path}")
        print(f"     Sheet name: Extracted")
        print(f"     Number of matches: {len(df)}")
        return

    except Exception as excel_error:
        # If Excel output fails (pandas missing, openpyxl missing, permission issue, etc.)
        # we create a CSV instead.
        base, _ = os.path.splitext(out_path)
        csv_path = base + ".csv"

        try:
            import csv

            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)

            print(f"[WARN] Excel write failed. Reason: {excel_error}")
            print(f"[OK] Wrote CSV instead: {csv_path}")
            print(f"     Number of matches: {len(rows)}")
            return

        except Exception as csv_error:
            print(f"[ERROR] Could not write Excel or CSV.", file=sys.stderr)
            print(f"        Excel error: {excel_error}", file=sys.stderr)
            print(f"        CSV error:   {csv_error}", file=sys.stderr)
            sys.exit(1)


# -----------------------
# 5) The main() function
# -----------------------
def main():
    """
    This is the main controller of the program.

    Steps:
    1) Read command line arguments
    2) Load the input file
    3) Ask user for keywords/patterns (or read them from CLI)
    4) Extract matches
    5) Write results to Excel/CSV
    """

    # argparse makes a friendly command-line interface
    ap = argparse.ArgumentParser(
        description="Extract lines matching user keywords/regex patterns from any text file and export to Excel/CSV."
    )

    # --in : input file path
    ap.add_argument(
        "--in",
        dest="infile",
        required=True,
        help="Input text file (any .txt / .log file)"
    )

    # --out : output file path (Excel preferred)
    ap.add_argument(
        "--out",
        dest="outfile",
        default="extracted.xlsx",
        help="Output Excel file (.xlsx). If Excel fails, a CSV will be written instead."
    )

    # --ignore-case : case-insensitive matching
    ap.add_argument(
        "--ignore-case",
        action="store_true",
        help="Match keywords without case sensitivity (error == ERROR == Error)"
    )

    # --context : include some lines before/after each match for context
    ap.add_argument(
        "--context",
        type=int,
        default=0,
        help="Number of lines before/after a match to include as context (default: 0)"
    )

    # --keywords : optionally supply keywords directly (no interactive prompt)
    ap.add_argument(
        "--keywords",
        nargs="*",
        default=None,
        help="Optional: provide keywords/regex patterns directly. If not given, program will ask interactively."
    )

    args = ap.parse_args()

    # Validate the input file exists
    if not os.path.isfile(args.infile):
        print(f"[ERROR] Input file not found: {args.infile}", file=sys.stderr)
        sys.exit(1)

    # Read the whole file into memory as a list of lines
    # errors="replace" prevents crashes if the file contains weird characters
    with open(args.infile, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    # Decide where keywords come from:
    # - If user passed --keywords ..., use those
    # - Otherwise, ask interactively
    if args.keywords is not None and len(args.keywords) > 0:
        keywords = args.keywords
    else:
        keywords = prompt_user_keywords()

    # If user did not provide anything, we cannot extract anything
    if not keywords:
        print("[ERROR] No keywords provided. Nothing to extract.", file=sys.stderr)
        sys.exit(2)

    # Compile user patterns
    try:
        patterns = compile_patterns(keywords, ignore_case=args.ignore_case)
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(3)

    # Extract matches
    rows = extract_matches(lines, patterns, context_lines=args.context)

    # If there are no matches, we still can write an empty file, but it's useful to warn the user
    if not rows:
        print("[WARN] No matches found for your keywords/patterns.")
        print("       You may want to check spelling, case sensitivity, or regex syntax.")

    # Write output
    write_excel_or_csv(rows, args.outfile)


# This means: "if this file is executed directly, run main()"
# If someone imports this file as a module, main() will NOT run automatically.
if __name__ == "__main__":
    main()
