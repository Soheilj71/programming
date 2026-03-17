# 🔤 Rename Spaces to Underscores (Bash Script)

## 📌 Overview

This script recursively scans a folder and replaces **spaces in file and directory names** with underscores (`_`).

It helps prevent issues in command-line workflows and improves compatibility with scripts and pipelines.

---

## ⚙️ Features

- Recursively processes all files and folders
- Safely handles nested directories
- Avoids renaming errors using depth-first traversal
- Beginner-friendly and easy to modify

---

## 🚀 Usage

```bash
bash rename_spaces_to_underscores.sh [folder_path]
```

### Default behavior:
*   If no folder is provided → uses current directory (`.`)

---
## 📌 Examples

### 1. Run in current directory
```bash
bash rename_spaces_to_underscores.sh
```

### 2. Run on a specific folder
```bash
bash rename_spaces_to_underscores.sh /home/user/data
```

---
## 🧠 How It Works

The script uses:
1.  `find` → locates files/folders with spaces
2.  `-depth` → ensures safe renaming of nested directories
3.  Bash string replacement:

   ```bash
   ${name// /_}
   ```
        
 replaces all spaces with underscores

5.  `mv` → renames the file/folder

---
## 📂 Example

### Before:
```bash
my folder/file name.txt
```

### After:
```bash
my_folder/file_name.txt
```
---
## ⚠️ Important Notes
*   This operation modifies filenames permanently
*   Avoid running on system directories
*   Make backups if working on critical data

---

🛠️ Possible Improvements

*   Add dry-run mode (preview changes without renaming)
*   Add file type filtering (e.g., only `.txt`, `.xtc`)
*   Log renamed files into a report file
*   Add undo functionality
