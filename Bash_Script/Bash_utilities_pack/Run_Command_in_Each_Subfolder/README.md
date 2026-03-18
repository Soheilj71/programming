# Run Command in Each Subfolder

A simple Bash script that runs the same command inside each immediate subfolder of a parent directory.

This is useful when you have many project folders, simulation folders, or job folders and want to execute the same command in each one without entering them manually.

---

## What this script does

Given a parent folder, the script:

1. Finds all immediate subfolders inside it
2. Enters each subfolder one by one
3. Runs the command you provide
4. Prints the folder name before executing the command

It only checks the **first level** of subfolders, not deeper nested folders.

---

## File

- `run_command_in_each_subfolder.sh`

---

## Usage

```bash
bash run_command_in_each_subfolder.sh parent_folder "command"
```

## Examples

Print the current directory inside each subfolder:
```bash
bash run_command_in_each_subfolder.sh simulations "pwd"
```

List files in each subfolder:

```bash
bash run_command_in_each_subfolder.sh simulations "ls -lh"
```

Run a Python script inside each subfolder:

```bash
bash run_command_in_each_subfolder.sh projects "python run.py"
```

Run a shell script inside each subfolder:

```bash
bash run_command_in_each_subfolder.sh jobs "bash submit.sh"
```

## Example folder structure

```
simulations/
├── run1/
├── run2/
├── run3/
```

Command:

```bash
bash run_command_in_each_subfolder.sh simulations "pwd"
```

Possible output:
```
==================================================
Folder: simulations/run1
Command: pwd
--------------------------------------------------
/full/path/to/simulations/run1

==================================================
Folder: simulations/run2
Command: pwd
--------------------------------------------------
/full/path/to/simulations/run2

==================================================
Folder: simulations/run3
Command: pwd
--------------------------------------------------
/full/path/to/simulations/run3
```

## Requirements
*   Bash
*   Standard Unix tools such as `find`

This script works on Linux and macOS.

## Important note about safety

This script uses:
```bash
eval "${command_to_run}"
```

That means the command is interpreted by the shell exactly as you provide it.

Use only trusted commands. Do not pass unsafe or unknown input into this script.

## Why use quotes around the command?
If your command contains spaces, it must be wrapped in quotes.

Correct:
```bash
bash run_command_in_each_subfolder.sh simulations "ls -lh"
```

Incorrect:

```bash
bash run_command_in_each_subfolder.sh simulations ls -lh
```

Without quotes, Bash will treat `ls` and `-lh` as separate arguments instead of one command string.

## Behavior notes
*   Only immediate subfolders are processed
*   Files directly inside the parent folder are ignored
*   If no subfolders are found, the script prints a message
*   The script stops on errors because it uses strict Bash settings:

```bash
set -euo pipefail
```

## Make the script executable
You can make it executable with:
```bash
chmod +x run_command_in_each_subfolder.sh
```

Then run it as:
```bash
./run_command_in_each_subfolder.sh simulations "pwd"
```
