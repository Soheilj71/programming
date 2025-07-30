# 🖥️ Interactive File Opener Script

## 📌 Overview
This script allows you to:
- Interactively select a folder by number (e.g., `simulation_1`, `simulation_2`, etc.).
- Automatically open files in that folder matching a defined pattern (e.g., `Heatmap_lag*_full.png`).
- **(macOS only)** Wait until the application closes before continuing.
- Repeat this process until you type `done`.
  
It is designed for **macOS** and **Linux**, and can easily be customized for other purposes.

---

## 🚀 Features
- Works on macOS (Darwin) and Linux (Ubuntu, Fedora, etc.).
- Supports wildcard patterns to match multiple files (e.g., `*.png`, `*.pdf`).
- Automatically sorts files in natural order (1, 2, 10 instead of 1, 10, 2).
- Interactive loop — process as many folders as you want until you type `done`.
- Hides errors if no files are found.
- **(macOS)** Waits until Preview or the chosen application is closed before moving to the next folder.

---

## 🛠️ How It Works
The script follows these steps:
1. **Prompt for folder number**  
   Asks the user to enter a number (e.g. `1`) or type `done` to exit.
2. **Build folder path**  
   Combines the base directory and folder prefix (e.g. `./simulation_1`).
3. **Check if folder exists**  
   If it does not exist, the script prints a warning and asks again.
4. **Find and sort files**  
   Searches for files matching the pattern (e.g. `Heatmap_lag*_full.png`) and sorts them in natural order.
5. **Open files**  
   - On macOS: Uses `open -a Preview` to open all files in Preview.  
   - On Linux: Uses `xdg-open` to open each file in its default application.
6. **Wait for application (macOS only)**  
   Waits until the application is closed before continuing.
7. **Repeat or exit**  
   Loop continues until you type `done`.

---

## 📂 Folder Structure Example
project/

│
├── script.sh

├── simulation_1/

│ ├── Heatmap_lag1_full.png

│ ├── Heatmap_lag2_full.png

│

├── simulation_2/

│ ├── Heatmap_lag1_full.png

│ ├── Heatmap_lag2_full.png


---

## ⚙️ Configuration
You can modify the following variables inside the script:

| Variable       | Description                                   | Example                    |
|----------------|-----------------------------------------------|----------------------------|
| `base_dir`     | Base directory where folders are stored       | `.` (current directory)    |
| `folder_prefix`| Prefix for folder names                       | `simulation_`             |
| `file_pattern` | Pattern of files to open (wildcards allowed)  | `Heatmap_lag*_full.png`    |
| `app_name`     | Application to open files with (macOS only)   | `Preview`                  |

---

## 💻 Usage
1. Make the script executable:  
   ```bash
   chmod +x script.sh

2. Run the script:
   ```bash
   ./script.sh

3. Example session:
```bash
Enter the folder number (or type 'done' to exit): 1
Opening files in ./simulation_1
Waiting for Preview to close...
Closed Preview for folder 1.

Enter the folder number (or type 'done' to exit): 2
Opening files in ./simulation_2
Waiting for Preview to close...
Closed Preview for folder 2.

Enter the folder number (or type 'done' to exit): done
Exiting script.
```

## 🖥️ OS Detection
The script uses `$OSTYPE` to detect the operating system:

- `darwin*` → macOS (Darwin kernel is the underlying Unix-based OS for macOS).

- `linux-gnu*` → Linux.

This allows the script to decide whether to use open -a (macOS) or xdg-open (Linux).

## 🔑 Key Bash Commands Explained
|   Command	   |                Purpose                                 |      
|--------------|--------------------------------------------------------|
|while true	   | Creates an infinite loop.                              |
|read -p	     | Displays a prompt and waits for input.                 |
|if [[ ... ]]  | Conditional test in Bash.                              |
|-d	           | True if a directory exists.                            |
|-z	           | True if a variable is empty.                           |
|ls	           | Lists files in a directory.                            |
|sort -V	     | Sorts files in natural number order.                   |
|pgrep -x	     | Checks if a process is running by its exact name.      |
|sleep 2	     | Pauses the script for 2 seconds.                       |
|continue	     | Skips to the next loop iteration.                      |
|break	       | Exits the loop entirely.                               |
|2>/dev/null	 | Redirects errors to nowhere (hides "file not found").  |

## 🔄 Customization Ideas##

- Change `file_pattern` to `"*.pdf"` to open PDFs instead of images.
- Use `app_name="Google Chrome"` to open files in Chrome on macOS.
- Modify `folder_prefix` to `"experiment_"` if your folders follow a different naming scheme.
- Add delete or move functionality to manage files interactively.
