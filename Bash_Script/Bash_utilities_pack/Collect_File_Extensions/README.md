# Collect File Extensions

A simple Bash script that counts how many files of each extension exist inside a folder and its subfolders.

This can be useful when:

- auditing project file types
- cleaning large datasets
- exploring unknown directories
- preparing repositories for GitHub

---

# Features

- Works recursively through subfolders
- Counts every file extension
- Detects files without extensions
- Simple command line usage
- No external dependencies

---

# Example Output

```
txt 12
csv 4
png 8
no_extension 3
```


This means:

| Extension | Count |
|----------|------|
| txt | 12 |
| csv | 4 |
| png | 8 |
| no_extension | 3 |

---

# Requirements

- macOS or Linux
- Bash
- Standard Unix tools (`find`, `awk`, `sort`)

---

# Usage

Run inside terminal.

### Count extensions in the current folder
```bash
bash collect_file_extensions.sh
```
### Count extensions in a specific folder
```bash
bash collect_file_extensions.sh /path/to/folder
```

# Examples

```bash
bash collect_file_extensions.sh ~/Documents
```


---

# How It Works

The script performs three main steps:

1. **Find files**

```bash
find folder -type f
```


This lists every file in the folder tree.

2. **Extract file extensions**

The script splits filenames using `.` and keeps the last part.

Example:
```bash
report.pdf → pdf
image.png → png
README → no_extension
```


3. **Count extensions**

AWK stores counts in a dictionary and prints the result.

---

# Example

Directory:
```
project/
│
├── data.csv
├── script.py
├── notes.txt
├── image.png
└── README
```

Run:

```bash
bash collect_file_extensions.sh project
```

Output:
```
csv 1
png 1
py 1
txt 1
no_extension 1
```


---

# Make Script Executable (Optional)

You can make the script runnable directly:

```bash
chmod +x collect_file_extensions.sh
```


