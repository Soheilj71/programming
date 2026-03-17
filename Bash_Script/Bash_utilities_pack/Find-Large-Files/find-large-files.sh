#!/usr/bin/env bash
# =============================================================================
# FIND LARGE FILES SCRIPT
# =============================================================================
# Author: Your Name
# Description:
#   This script finds and displays the largest files inside a directory.
#
# Why this is useful:
#   - Quickly identify large files taking up disk space
#   - Clean up storage
#   - Debug storage-heavy workflows (e.g., MD trajectories, logs, checkpoints)
#
# Usage:
#   bash find_large_files.sh [folder_path] [number_of_files]
#
# Examples:
#   bash find_large_files.sh
#   bash find_large_files.sh /home/user/data
#   bash find_large_files.sh /home/user/data 50
# =============================================================================

set -euo pipefail  # Safe scripting: exit on error, undefined vars, pipe failures

# -----------------------------------------------------------------------------
# INPUT ARGUMENTS
# -----------------------------------------------------------------------------

# If user does not provide a folder, default is current directory (.)
search_dir="${1:-.}"

# If user does not provide count, default is 20 files
count="${2:-20}"

# -----------------------------------------------------------------------------
# VALIDATION
# -----------------------------------------------------------------------------

# Check if the provided folder exists
if [[ ! -d "${search_dir}" ]]; then
    echo "[ERROR] Folder not found: ${search_dir}"
    exit 1
fi

# -----------------------------------------------------------------------------
# CORE LOGIC
# -----------------------------------------------------------------------------

# Step 1: find all files (-type f)
# Step 2: use -print0 to safely handle spaces in filenames
# Step 3: pass results to 'du -h' to get human-readable sizes
# Step 4: sort files by size (largest first)
# Step 5: show top N results

echo "Searching in: ${search_dir}"
echo "Showing top ${count} largest files..."
echo "----------------------------------------"

find "${search_dir}" -type f -print0 \
  | xargs -0 du -h \
  | sort -hr \
  | head -n "${count}"

echo "----------------------------------------"
echo "Done."
