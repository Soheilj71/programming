#!/bin/bash
# ============================================
# General Interactive File Opener Script
# Written by: Soheil Jamali
# University of Arkansas
# Email: sjamali@uark.edu, soheil.jamali.dev@gmail.com
# ============================================
# This script allows a user to:
#   1. Repeatedly select a folder based on a numeric identifier.
#   2. Open files (matching a pattern) with a chosen application.
#   3. Wait until the application is closed before proceeding.
#
# Works on macOS (open) and Linux (xdg-open).
# ============================================

# -------- CONFIGURATION --------
base_dir="."                          # Base directory where folders exist
folder_prefix="simulation_"           # Prefix for the folder names, e.g., "simulation_"
file_pattern="Heatmap_lag*_full.png"  # File pattern to open
app_name="Preview"                    # Application to open files (macOS: Preview, Linux: eog, etc.)

# Detect OS for file opening command
if [[ "$OSTYPE" == "darwin"* ]]; then
    open_cmd="open -a"    # macOS
else
    open_cmd="xdg-open"   # Linux
fi

# -------- MAIN LOOP --------
while true; do
    # Ask user for folder number or exit
    read -p "Enter the folder number (or type 'done' to exit): " folder_num

    # Exit condition
    if [[ "$folder_num" == "done" ]]; then
        echo "Exiting script."
        break
    fi

    # Construct the folder path
    folder="${base_dir}/${folder_prefix}${folder_num}"

    # Check if the folder exists
    if [[ -d "$folder" ]]; then
        echo "Opening files in $folder"

        # Find and sort files matching the pattern
        files=$(ls "$folder"/$file_pattern 2>/dev/null | sort -V)

        if [[ -z "$files" ]]; then
            echo "No files found matching pattern '$file_pattern' in $folder."
            continue
        fi

        # Open the files
        if [[ "$OSTYPE" == "darwin"* ]]; then
            $open_cmd "$app_name" $files
        else
            for f in $files; do
                $open_cmd "$f"
            done
        fi

        # Wait until the application closes (macOS only)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "Waiting for $app_name to close..."
            while pgrep -x "$app_name" > /dev/null; do
                sleep 2
            done
            echo "$app_name closed for folder $folder_num."
        else
            echo "Opened files. (Linux does not block until close)"
        fi
    else
        echo "Folder $folder does not exist."
    fi
done

