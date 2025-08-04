# 🖼️ Open Images Script

A simple and interactive Bash script that allows you to open images from any folder, using any pattern you define.

Supports macOS and Linux, handles file names with spaces, and provides a smooth experience for opening images one-by-one.

## Features
- Open any folder: Type a folder path (supports ~ for your home directory).
- Filter images by pattern: e.g. *.png, *.jpeg, Heatmap_*.jpg.
- Cross-platform: Works on both macOS (Preview) and Linux (xdg-open).
- Wait behavior:
- macOS: Waits until Preview is closed before continuing.
- Linux: Asks you to press Enter after closing each image.
- Handles spaces in file names properly.
- Repeatable: After viewing, you can enter a new folder or exit.

## Installation
Clone or download this repository, then make the script executable:
```bash
chmod +x open_images.sh
```

# Usage
Run the script from the terminal:
```bash
./open_images.sh
```

Follow the prompts:
<pre>
  Enter the folder path (or type 'done' to exit): ~/Pictures
  Enter the image pattern (e.g. *.png, Heatmap_*.jpg): *.jpeg
  Opening: image1.jpeg
  (wait until Preview closes or press Enter on Linux)
  ✅ All images in the folder have been opened.
</pre>


Type done anytime to exit.

# Example

Example 1: Open PNG images on macOS
<pre>
Enter the folder path (or type 'done' to exit): ~/Pictures
Enter the image pattern (e.g. *.png, Heatmap_*.jpg): *.png
</pre>

Example 2: Open specific images on Linux
<pre>
Enter the folder path (or type 'done' to exit): ~/Downloads
Enter the image pattern (e.g. *.png, Heatmap_*.jpg): Heatmap_*.jpg
</pre>

# Requirements
- macOS: Preview (built-in)
- Linux: xdg-open (available by default in most distros)
- Bash: v4 or later

# Notes
- On macOS, all images will open in Preview. The script waits until Preview closes before proceeding.
- On Linux, you will be asked to press Enter to move to the next image because most image viewers do not block the terminal.
- File names with spaces are fully supported.
