#!/usr/bin/env bash
# =============================================================================
# RENAME SPACES TO UNDERSCORES
# =============================================================================
# Author: Your Name
# Description:
#   This script recursively finds files and folders with spaces in their names
#   and replaces spaces with underscores (_).
#
# Why this is useful:
#   - Avoid issues in scripts (spaces break many commands)
#   - Clean file naming for pipelines (HPC, ML, MD simulations)
#   - Standardize datasets before processing
#
# Usage:
#   bash rename_spaces_to_underscores.sh [folder_path]
#
# Examples:
#   bash rename_spaces_to_underscores.sh
#   bash rename_spaces_to_underscores.sh /home/user/data
# =============================================================================

set -euo pipefail  # Exit on error, undefined variable, or pipeline failure

# -----------------------------------------------------------------------------
# INPUT ARGUMENT
# -----------------------------------------------------------------------------

# Default: current directory
target_dir="${1:-.}"

# -----------------------------------------------------------------------------
# VALIDATION
# -----------------------------------------------------------------------------

if [[ ! -d "${target_dir}" ]]; then
    echo "[ERROR] Folder not found: ${target_dir}"
    exit 1
fi

# -----------------------------------------------------------------------------
# CORE LOGIC
# -----------------------------------------------------------------------------

# Explanation:
# - find ... -depth:
#     Process deeper paths first (important for renaming directories safely)
# - -name '* *':
#     Select files/directories that contain spaces
# - while read:
#     Iterate through each matched path safely
# - ${var// /_}:
#     Replace ALL spaces with underscores

echo "Scanning directory: ${target_dir}"
echo "Renaming files and folders..."
echo "----------------------------------------"

find "${target_dir}" -depth -name '* *' | while IFS= read -r old_name; do

    # Replace spaces with underscores
    new_name="${old_name// /_}"

    # Only rename if the name actually changes
    if [[ "${old_name}" != "${new_name}" ]]; then
        mv "${old_name}" "${new_name}"
        echo "Renamed:"
        echo "  OLD: ${old_name}"
        echo "  NEW: ${new_name}"
        echo "----------------------------------------"
    fi

done

echo "Done."
