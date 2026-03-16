#!/usr/bin/env bash
# =============================================================================
# backup_folder.sh
# -----------------------------------------------------------------------------
# A simple Bash script that creates a timestamped backup of a folder.
#
# Example:
#   bash backup_folder.sh data
#
# Result:
#   data_backup_20260316_154210
#
# The script copies the entire folder and adds the current date and time
# to the backup folder name so multiple backups do not overwrite each other.
# =============================================================================


# -----------------------------------------------------------------------------
# Safety settings
# -----------------------------------------------------------------------------
# -e  : stop the script immediately if any command fails
# -u  : stop if we try to use a variable that was not defined
# pipefail : if a pipeline fails, the whole script fails
set -euo pipefail


# -----------------------------------------------------------------------------
# Read the first command-line argument
# -----------------------------------------------------------------------------
# $1 means "the first argument provided to the script"
# Example:
#   bash backup_folder.sh data
#
# In this case:
#   source_dir = "data"
#
# The syntax "${1:-}" means:
#   if $1 exists → use it
#   if not → set the variable to empty
source_dir="${1:-}"


# -----------------------------------------------------------------------------
# Check if the user provided a folder path
# -----------------------------------------------------------------------------
# -z checks if a string is empty
if [[ -z "${source_dir}" ]]; then
    echo "Usage: bash backup_folder.sh path/to/folder"
    exit 1
fi


# -----------------------------------------------------------------------------
# Check if the folder actually exists
# -----------------------------------------------------------------------------
# -d checks if something is a directory
if [[ ! -d "${source_dir}" ]]; then
    echo "Error: folder not found: ${source_dir}"
    exit 1
fi


# -----------------------------------------------------------------------------
# Create a timestamp
# -----------------------------------------------------------------------------
# date command generates the current date/time
# Format used:
#
#   %Y = year
#   %m = month
#   %d = day
#   %H = hour
#   %M = minute
#   %S = second
#
# Example output:
#   20260316_154210
timestamp="$(date +%Y%m%d_%H%M%S)"


# -----------------------------------------------------------------------------
# Extract the folder name only (remove path)
# -----------------------------------------------------------------------------
# Example:
#
#   source_dir="/Users/soheil/data"
#
# basename returns:
#
#   data
base_name="$(basename "${source_dir}")"


# -----------------------------------------------------------------------------
# Create the backup folder name
# -----------------------------------------------------------------------------
# The new folder name will look like this:
#
#   data_backup_20260316_154210
backup_name="${base_name}_backup_${timestamp}"


# -----------------------------------------------------------------------------
# Copy the folder
# -----------------------------------------------------------------------------
# cp = copy
# -R = recursive (copy everything inside the folder)
#
# This duplicates the entire folder and its contents.
cp -R "${source_dir}" "${backup_name}"


# -----------------------------------------------------------------------------
# Print confirmation message
# -----------------------------------------------------------------------------
echo "Backup created: ${backup_name}"
