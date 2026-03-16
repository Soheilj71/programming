# Backup Folder Script

A simple Bash script that creates a timestamped backup copy of a folder.

## What this script does

This script takes a folder as input, makes a full copy of it, and adds the current date and time to the backup folder name.

This is useful when you want to:

- save a copy of important files before editing them
- keep snapshots of project folders
- create quick manual backups from the terminal

---

## Script name

```bash
backup_folder.sh
```

# Usage

Run the script like this:

```bash
bash backup_folder.sh path/to/folder
```

Example:

```bash
bash backup_folder.sh data
```

# Example

Suppose you have a folder named:

```bash
data
```

and you run:

```bash
bash backup_folder.sh data
```

The script may create a backup folder like:

```bash
data_backup_20260316_154210
```

This means the original folder data was copied into a new folder whose name includes the backup time.

# How it works

The script does the following:

1.  reads the folder path from the command line

2.  checks whether the folder path was provided

3.  checks whether the folder exists

4.  creates a timestamp using the current date and time

5.  builds a backup folder name

6.  copies the folder recursively

7.  prints a success message

# Output format

The backup folder name follows this pattern:

```bash
originalFolder_backup_YYYYMMDD_HHMMSS
```

Example:

```bash
results_backup_20260316_154210
```
# Requirements

*   Bash

*   Standard Unix tools such as:
       *   cp
       *   date
       *   basename

This script is suitable for Linux and macOS.

# Notes

*   The backup is created in the current working directory.

*   The original folder is not modified.

*   The script stops immediately if an error happens.

# Exit behavior

The script will stop with an error if:

*   no folder path is provided

*   the folder does not exist

# Example terminal output

Successful run:
```bash
Backup created: data_backup_20260316_154210
```

Missing folder argument:
```bash
Usage: bash backup_folder.sh path/to/folder
```

Folder not found:
```bash
Error: folder not found: myfolder
```
