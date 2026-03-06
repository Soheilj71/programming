# Purpose: Run a command inside many subfolders and save stdout/stderr logs + a summary CSV.  # Goal.

import argparse  # Command-line interface.
import csv  # For summary output.
import subprocess  # To run external commands (like python script.py).
import sys  # For exit codes.
import time  # For timing runs.
from pathlib import Path  # Safer file paths.
from typing import List  # For type hints.


def fail(message: str, code: int = 1) -> None:  # Helper to exit with an error.
    print(f"[ERROR] {message}", file=sys.stderr)  # Print error.
    sys.exit(code)  # Exit.


def list_target_folders(parent: Path) -> List[Path]:  # Find subfolders to run in.
    if not parent.exists():  # Ensure parent exists.
        fail(f"Parent folder not found: {parent}")  # Explain.
    if not parent.is_dir():  # Ensure parent is a directory.
        fail(f"Parent path is not a folder: {parent}")  # Explain.

    folders = [p for p in sorted(parent.iterdir()) if p.is_dir()]  # Get all direct subfolders.
    if not folders:  # If none found...
        fail(f"No subfolders found inside: {parent}")  # Explain.

    return folders  # Return list of folder Paths.


def run_in_folder(folder: Path, command: List[str], timeout: int) -> dict:  # Run the command in one folder.
    start = time.time()  # Record start time.

    # We run the command and capture stdout and stderr.  # This helps debugging and record keeping.
    try:  # Try running the external command.
        result = subprocess.run(  # Run the command.
            command,  # Example: ["python", "script.py", "--arg", "10"]
            cwd=str(folder),  # Run *inside* this folder.
            capture_output=True,  # Capture stdout and stderr in memory.
            text=True,  # Decode output as text.
            timeout=timeout if timeout > 0 else None,  # Timeout in seconds (or None for no timeout).
        )
        code = result.returncode  # 0 means success, non-zero means error.
        out = result.stdout  # Standard output text.
        err = result.stderr  # Error output text.
    except subprocess.TimeoutExpired:  # If the command took too long...
        code = 124  # Common timeout code in Unix.
        out = ""  # No output guaranteed.
        err = f"TimeoutExpired: command exceeded {timeout} seconds"  # Store a clear message.
    except FileNotFoundError:  # If command executable not found (e.g., "python" not found).
        fail(f"Command not found: {command[0]} (is it installed and on PATH?)")  # Explain and exit.
    except Exception as e:  # Any other unexpected error.
        code = 1  # Generic failure code.
        out = ""  # Empty output.
        err = f"Unexpected error: {e}"  # Save error message.

    elapsed = time.time() - start  # Measure runtime.

    return {  # Return structured info for summary + logs.
        "folder": str(folder),  # Which folder we ran in.
        "returncode": int(code),  # Exit code.
        "seconds": float(elapsed),  # Runtime.
        "stdout": out,  # Captured stdout.
        "stderr": err,  # Captured stderr.
    }


def write_text(path: Path, text: str) -> None:  # Write a text file safely.
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists.
    path.write_text(text, encoding="utf-8", errors="replace")  # Write text.


def write_summary_csv(path: Path, rows: list[dict]) -> None:  # Write CSV summary.
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensure output folder exists.

    # Define columns in a fixed order.  # Keeps CSV consistent.
    cols = ["folder", "returncode", "seconds", "stdout_file", "stderr_file"]  # Chosen summary columns.

    with path.open("w", newline="", encoding="utf-8") as f:  # Open output CSV file.
        writer = csv.DictWriter(f, fieldnames=cols)  # Create writer with the column list.
        writer.writeheader()  # Write header row.
        for r in rows:  # Write each row.
            writer.writerow(r)  # Write row.


def main() -> None:  # Main program.
    parser = argparse.ArgumentParser(  # Create CLI.
        description="Run the same command inside each subfolder and save logs + summary."
    )  # Description shown in --help.

    parser.add_argument("--parent", required=True, help="Parent folder containing many subfolders (e.g., runs/).")
    parser.add_argument("--out_dir", required=True, help="Where to save logs and summary CSV.")
    parser.add_argument("--timeout", type=int, default=0, help="Timeout seconds per folder (0 means no timeout).")

    # We accept the command after a double-dash separator.  # Example:
    # python folder_runner.py --parent runs --out_dir logs -- python script.py --arg 5
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to run after '--'.")

    args = parser.parse_args()  # Parse args.

    parent = Path(args.parent)  # Convert to Path.
    out_dir = Path(args.out_dir)  # Convert to Path.

    if not args.command:  # Ensure command exists.
        fail("No command provided. Example: folder_runner.py --parent X --out_dir Y -- python script.py")  # Explain.

    # If the first token is '--', argparse may include it; we remove it.  # Makes command clean.
    command = args.command  # Get raw command tokens.
    if command and command[0] == "--":  # If leading separator is present...
        command = command[1:]  # Remove it.

    folders = list_target_folders(parent)  # Gather subfolders.

    rows_for_csv = []  # CSV summary rows.
    logs_dir = out_dir / "logs"  # Folder where stdout/stderr files will go.
    logs_dir.mkdir(parents=True, exist_ok=True)  # Create logs directory.

    for folder in folders:  # Loop through each folder.
        result = run_in_folder(folder, command, timeout=args.timeout)  # Run the command.

        # Create safe filenames based on folder name.  # So each folder gets its own log files.
        tag = folder.name  # Use folder name as identifier.
        stdout_path = logs_dir / f"{tag}.stdout.txt"  # Stdout file path.
        stderr_path = logs_dir / f"{tag}.stderr.txt"  # Stderr file path.

        write_text(stdout_path, result["stdout"])  # Save stdout.
        write_text(stderr_path, result["stderr"])  # Save stderr.

        # Add one row to summary CSV.  # Keeps CSV small and readable.
        rows_for_csv.append(
            {
                "folder": result["folder"],  # Folder path.
                "returncode": result["returncode"],  # Exit code.
                "seconds": f"{result['seconds']:.3f}",  # Runtime with 3 decimals.
                "stdout_file": str(stdout_path),  # Where stdout was saved.
                "stderr_file": str(stderr_path),  # Where stderr was saved.
            }
        )

        # Print progress line so user sees what is happening.  # Helpful feedback.
        print(f"{folder} -> returncode={result['returncode']} time={result['seconds']:.2f}s")  # Progress.

    summary_csv = out_dir / "summary.csv"  # Summary CSV path.
    write_summary_csv(summary_csv, rows_for_csv)  # Write summary CSV.

    print(f"Wrote summary: {summary_csv}")  # Final message.


if __name__ == "__main__":  # Only run main if executed directly.
    main()  # Start the program.
