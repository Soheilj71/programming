#!/usr/bin/env bash
# =============================================================================
# run_command_in_each_subfolder.sh
# -----------------------------------------------------------------------------
# Purpose:
#   Run the same shell command inside each immediate subfolder of a parent
#   directory.
#
# Description:
#   - Looks only at the first level of subfolders inside the given parent folder
#   - Enters each subfolder one by one
#   - Runs the command you provide
#   - Prints the folder name before running the command
#
# Usage:
#   bash run_command_in_each_subfolder.sh parent_folder "command"
#
# Examples:
#   bash run_command_in_each_subfolder.sh simulations "pwd"
#   bash run_command_in_each_subfolder.sh simulations "ls -lh"
#   bash run_command_in_each_subfolder.sh projects "python run.py"
#
# Notes:
#   - The command must be passed inside quotes if it contains spaces
#   - The script uses 'eval', so only run trusted commands
# =============================================================================

set -euo pipefail

# ---------------------------
# Read input arguments
# ---------------------------
parent_dir="${1:-}"
command_to_run="${2:-}"

# ---------------------------
# Show help message
# ---------------------------
show_usage() {
    cat <<EOF
Usage:
  bash run_command_in_each_subfolder.sh parent_folder "command"

Description:
  Run the same command inside each immediate subfolder of a parent directory.

Examples:
  bash run_command_in_each_subfolder.sh simulations "pwd"
  bash run_command_in_each_subfolder.sh simulations "ls -lh"
  bash run_command_in_each_subfolder.sh projects "python run.py"
EOF
}

# ---------------------------
# Validate input
# ---------------------------
if [[ -z "${parent_dir}" || -z "${command_to_run}" ]]; then
    echo "Error: missing required arguments."
    echo
    show_usage
    exit 1
fi

if [[ ! -d "${parent_dir}" ]]; then
    echo "Error: folder not found: ${parent_dir}"
    exit 1
fi

# ---------------------------
# Track whether any subfolder exists
# ---------------------------
found_subfolder=false

# ---------------------------
# Loop through immediate subfolders
# ---------------------------
while IFS= read -r -d '' folder; do
    found_subfolder=true

    echo "=================================================="
    echo "Folder: ${folder}"
    echo "Command: ${command_to_run}"
    echo "--------------------------------------------------"

    (
        cd "${folder}" || exit 1
        eval "${command_to_run}"
    )

    echo
done < <(find "${parent_dir}" -mindepth 1 -maxdepth 1 -type d -print0)

# ---------------------------
# Warn if no subfolders found
# ---------------------------
if [[ "${found_subfolder}" == false ]]; then
    echo "No immediate subfolders were found inside: ${parent_dir}"
fi
