# 📄 Remove Lines from Text Files (Python CLI Tool)

## Overview
A lightweight and flexible Python command-line tool for removing specific lines or ranges of lines from text files.

This utility is designed for scientific computing, data preprocessing, and reproducible workflows, where structured text outputs (e.g., MD logs, simulation outputs, CSV files) often require precise cleaning before analysis.

✨ Features

- Remove:
  - Individual lines → `1,5,10`
  - Ranges → `3-8`
  - Mixed selections → `1,3-5,10`
*   Human-friendly 1-based indexing
*   Memory-efficient (stream-based processing)
*   Optional in-place editing
*   Robust error handling
*   Cross-platform (Linux, macOS, HPC environments)


## ⚙️ Usage

### Basic Syntax
```python
python remove_lines.py INPUT OUTPUT --remove "SPEC"
```

### Arguments

| Argument     |	Description                                     | 
|--------------|----------------------------------------------------|
| `INPUT`	   | Path to input file                                 |
| `OUTPUT`     | Path to output file (optional if using `--inplace)`|
| `--remove`   | Line specification (e.g., `"1,3-5,10"`)            | 
| `--inplace`  | Modify the file directly                           |

## 🧪 Examples

### Remove specific lines
```python
python remove_lines.py data.txt cleaned.txt --remove "1,5,10"
```

### Remove a range of lines
```python
python remove_lines.py data.txt cleaned.txt --remove "3-8"
```

### Mixed removal (recommended)
```python
python remove_lines.py data.txt cleaned.txt --remove "1,3-5,10"
```

### In-place modification
```python
python remove_lines.py data.txt --remove "1-10" --inplace
```

### 📌 Line Specification Format

The `--remove` argument accepts:

| Format        |	Meaning                                      |
|---------------|------------------------------------------------|
| `5`	        | Remove line 5                                  |
| `3-7`	        | Remove lines 3 through 7                       |
| `1,4,10`	    | Remove lines 1, 4, and 10                      |
| `1,3-6,9`	    | Combination of both                            |

*   ⚠️ Line numbering starts at 1 (not 0)

## 🧠 Design Principles
This tool is built with reproducibility and scalability in mind:

### 1. Streaming I/O
*   Processes files line-by-line
*   Suitable for large files (GB-scale)
### 2. Deterministic Behavior
*   Explicit line control
*   No hidden transformations
### 3. HPC-Friendly
*   Easily integrated into Slurm pipelines
*   No external dependencies

## 🔬 Example Use Cases
*   Cleaning molecular dynamics output files (e.g., NAMD, GROMACS logs)
*   Removing headers or corrupted segments from datasets
*   Preprocessing input files for machine learning pipelines
*   Standardizing simulation outputs before analysis

## 🛠️ Integration Example (HPC / Slurm)
```bash
srun python remove_lines.py simulation.log --remove "1-50" --inplace
```

## 📂 Project Structure
```
remove-lines-tool/
│── remove_lines.py
│── README.md
```

## 📈 Future Improvements
Planned extensions:
*   Keep-only mode (`--keep`)
*   Regex-based filtering (`--pattern`)
*   Batch processing across directories
*   CSV column extraction
*   Integration with scientific data pipelines

## 🤝 Contributing

Contributions are welcome. Please open an issue or submit a pull request for improvements.

