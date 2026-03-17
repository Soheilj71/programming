# 🔍 Find Large Files (Bash Script)

## 📌 Overview

This script helps you quickly identify the **largest files** inside a folder.

It is especially useful for:
- Cleaning up disk space
- Debugging large data usage
- Managing simulation outputs (e.g., MD trajectories, logs, checkpoints)

---

## ⚙️ Features

- Works on any Unix-based system (Linux / macOS)
- Handles filenames with spaces safely
- Sorts files by size (largest → smallest)
- User-defined number of results
- Beginner-friendly and easy to modify

---

## 🚀 Usage

```bash
bash find_large_files.sh [folder_path] [number_of_files]
```

### Default behavior:

*   `folder_path` → current directory (`.`)
*   `number_of_files` → 20

---
## 📌 Examples
### 1. Search current directory
```bash
bash find_large_files.sh
```

### 2. Search a specific folder
```bash
bash find_large_files.sh /home/user/data
```

### 3. Show top 50 largest files
```bash
bash find_large_files.sh /home/user/data 50
```
---

## 🧠 How It Works

The script uses a pipeline of standard Unix tools:
1.  `find` → locates all files
2.  `du -h` → calculates file sizes (human-readable)
3. `sort -hr` → sorts by size (largest first)
4. `head` → limits output to top N files

## 📂 Example Output
```
Searching in: /home/user/data
Showing top 5 largest files...
----------------------------------------
2.1G    ./trajectory_01.xtc
1.8G    ./trajectory_02.xtc
900M    ./checkpoint.pt
500M    ./log.txt
120M    ./results.npy
----------------------------------------
Done.
```
---
## ⚠️ Notes

*   Large directories may take time to scan
*   Requires standard Unix tools (`find`, `du`, `sort`, `head`)
*   Works best on local filesystems

---

## 🛠️ Possible Improvements
*   Add file type filtering (e.g., only `.xtc`, `.npy`)
*   Export results to CSV
*   Add progress indicator for large directories
