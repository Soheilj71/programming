#!/usr/bin/env bash
# =============================================================================
# collect_file_extensions.sh
# =============================================================================
# Purpose
# -----------------------------------------------------------------------------
# Count how many files of each extension exist inside a folder and all of its
# subfolders.
#
# Example
# -----------------------------------------------------------------------------
# bash collect_file_extensions.sh
#
# or
#
# bash collect_file_extensions.sh /Users/username/Documents
#
# Output Example
# -----------------------------------------------------------------------------
# txt 12
# csv 4
# png 8
# no_extension 3
#
# =============================================================================

# Exit immediately if a command fails
# -e : stop if a command fails
# -u : stop if a variable is not defined
# -o pipefail : detect failures inside pipelines
set -euo pipefail

# If user does not provide a folder, use the current folder
target_dir="${1:-.}"

# Check that the folder exists
if [[ ! -d "${target_dir}" ]]; then
    echo "Error: folder not found: ${target_dir}"
    exit 1
fi

# Find all files and extract their extensions
find "${target_dir}" -type f | awk '
{
    # Split the file name using "." as separator
    n = split($0, parts, ".")

    # If the file has an extension
    if (n > 1) {
        ext = parts[n]
    }
    else {
        ext = "no_extension"
    }

    # Count occurrences
    count[ext]++
}

# After processing all files
END {
    for (e in count) {
        print e, count[e]
    }
}
' | sort
