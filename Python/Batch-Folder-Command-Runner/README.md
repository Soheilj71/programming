# Batch Folder Command Runner

A simple Python utility that runs the **same command inside multiple subfolders** and automatically collects logs and a summary report.

This tool is useful when you have many experiment folders, simulation runs, or datasets and need to execute the same script in each folder.

The script will:

1. Find all subfolders inside a parent directory
2. Run a command inside each subfolder
3. Capture both **stdout** and **stderr**
4. Save logs for each folder
5. Generate a **summary CSV report**

This makes it easy to monitor large batches of experiments.

---

# Why This Tool Is Useful

Many workflows require running the same script across many folders, such as:

- Running simulations in many directories
- Processing datasets stored in separate folders
- Executing analysis scripts for multiple experiments
- Running machine learning evaluations on multiple runs
- Automating repetitive command line tasks

Instead of manually entering each folder and running commands, this tool automates the entire process.

---

# Features

- Runs any command in **all subfolders**
- Captures **standard output (stdout)**
- Captures **error output (stderr)**
- Saves logs automatically
- Creates a **summary CSV report**
- Optional **timeout protection**
- Works on **Linux / macOS / Windows**

---

# Installation

No external dependencies are required.

The script only uses Python standard libraries.

Requirements:

- Python 3.8+

Clone the repository:

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
```

# Basic Usage
```bash
python folder_runner.py --parent PARENT_FOLDER --out_dir OUTPUT_FOLDER -- COMMAND
```

Important: the command must appear after `--`

# Example
Directory structure:
```
runs/
 ├── run1/
 │   └── data.txt
 ├── run2/
 │   └── data.txt
 ├── run3/
 │   └── data.txt
```

Example command:
```bash
python folder_runner.py \
--parent runs \
--out_dir results \
-- python analyze.py
```

What happens:
The script will execute:

```
cd runs/run1
python analyze.py

cd runs/run2
python analyze.py

cd runs/run3
python analyze.py
```

# Output Structure
After execution, the output folder will contain:

```
results/

summary.csv

logs/
 ├── run1.stdout.txt
 ├── run1.stderr.txt
 ├── run2.stdout.txt
 ├── run2.stderr.txt
 ├── run3.stdout.txt
 └── run3.stderr.txt
```

# Summary CSV
The summary file contains one row per folder.

Example:
```
folder,returncode,seconds,stdout_file,stderr_file
runs/run1,0,1.25,logs/run1.stdout.txt,logs/run1.stderr.txt
runs/run2,0,1.10,logs/run2.stdout.txt,logs/run2.stderr.txt
runs/run3,1,0.85,logs/run3.stdout.txt,logs/run3.stderr.txt
```

Columns:

|Column      |Meaning                                    |
|------------|-------------------------------------------|
|folder	     | Folder where the command was executed     |
|returncode	 | Exit status of the command (0 = success)  |
|seconds	 | Execution time                            |
|stdout_file |	Saved standard output                    |
|stderr_file |	Saved error output                       |

# Timeout Option
You can limit how long a command runs in each folder.

Example:
```bash
python folder_runner.py \
--parent runs \
--out_dir results \
--timeout 300 \
-- python analyze.py
```

This stops any command that runs longer than 300 seconds.

# Common Use Cases
## Running simulations

``` bash
python folder_runner.py \
--parent simulations \
--out_dir logs \
-- python run_simulation.py
```

## Running analysis scripts
```bash
python folder_runner.py \
--parent experiments \
--out_dir analysis_logs \
-- python analyze_results.py
```

## Running shell commands
```bash
python folder_runner.py \
--parent datasets \
--out_dir logs \
-- ls
```


# Example Workflow
Suppose you have 100 simulation folders.
Instead of manually doing:
```bash
cd run1
python analyze.py

cd run2
python analyze.py
...
```

You run one command:
```bash
python folder_runner.py --parent runs --out_dir logs -- python analyze.py
And everything runs automatically.
```
