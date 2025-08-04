#!/bin/bash
# 
# Written by: Soheil Jamali
# Email: sjamali@uark.edu, soheil.jamali.dev@gmail.com
# University of Arkansas
#
# This script is designed to open images in a specified folder based on a user-defined pattern. 
# Open Images Script
# -------------------
# This script allows the user to:
#   1. Enter any folder path (supports ~ for home directory).
#   2. Enter any image pattern (e.g. *.png, *.jpeg, Heatmap_*.jpg).
#   3. Open the matching images using the default image viewer.
#   4. On macOS, it waits for Preview to fully close before continuing.
#   5. On Linux, it asks the user to press Enter to continue for each image.
#
# Supported OS: macOS and Linux
#
#

# Detect the operating system and set the image viewer command
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: Use Preview
    IMAGE_VIEWER="open -a Preview"
    VIEWER_PROCESS="Preview"
else
    # Linux: Use xdg-open (works with default image viewer)
    IMAGE_VIEWER="xdg-open"
fi

# Infinite loop until the user types "done"
while true; do
    # Ask user for the folder path
    read -p "Enter the folder path (or type 'done' to exit): " folder_path

    # If user types "done", exit the script
    if [[ "$folder_path" == "done" ]]; then
        echo "Exiting script."
        break
    fi

    # Expand ~ to $HOME if used
    folder_path="${folder_path/#\~/$HOME}"

    # Check if the folder exists
    if [[ ! -d "$folder_path" ]]; then
        echo "Folder '$folder_path' does not exist."
        continue
    fi

    # Ask user for the image pattern
    read -p "Enter the image pattern (e.g. *.png, Heatmap_*.jpg): " img_pattern

    # Find matching files safely using 'find' (handles spaces in filenames)
    images=()
    while IFS= read -r file; do
        images+=("$file")
    done < <(find "$folder_path" -maxdepth 1 -type f -name "$img_pattern" | sort -V)

    # If no images are found, prompt again
    if [[ ${#images[@]} -eq 0 ]]; then
        echo "No images found matching '$img_pattern' in '$folder_path'."
        continue
    fi

    # Loop through each image and open it
    for img in "${images[@]}"; do
        echo "Opening: $img"

        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS: Open in Preview and wait until it's closed
            $IMAGE_VIEWER "$img"
            while pgrep -x "$VIEWER_PROCESS" > /dev/null; do
                sleep 2
            done
        else
            # Linux: Open in default viewer and ask for manual confirmation
            $IMAGE_VIEWER "$img"
            echo "Press Enter after closing the image viewer..."
            read
        fi
    done

    echo "✅ All images in '$folder_path' have been opened."
done
