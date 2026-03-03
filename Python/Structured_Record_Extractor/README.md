# 📄 TXT to CSV Extractor
Convert structured or semi-structured text files (logs, simulation outputs, reports) into clean CSV tables using user-defined regular expressions.
This tool is lightweight, dependency-free, and designed for reproducible data extraction workflows.


# 🚀 Features
*   Extract multiple fields using custom regex patterns
*   Split large text files into logical records
*   Automatically generate structured CSV output
*   No third-party dependencies
*   Works on macOS, Linux, and Windows


# 📦 Requirements
*   Python 3.8 or newer
*   No external libraries required


# 🛠 Installation
Clone your repository:
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

Or simply download `txt_to_csv_extractor.py`.

# ▶️ Usage
Basic syntax:

```bash
python3 txt_to_csv_extractor.py \
  --infile input.txt \
  --out_csv output.csv \
  --field NAME=REGEX \
  --field NAME2=REGEX2
```


# 🔍 Arguments
## Required

| Argument	| Description                                                       |
|---------|---------------------------------------------------------------------|
| --infile	| Input text file (log, report, etc.)                               |
| --out_csv	| Output CSV file path                                              |
| --field	| Field definition in the form COLUMN_NAME=REGEX (can be repeated)  |


## Optional
| Argument	    | Default    |	Description                                                                                               |
|---------------|------------|------------------------------------------------------------------------------------------------------------|
| --record_sep	| blank	     |   How to split records. `blank` splits on empty lines, or provide a literal separator string like `"===="` |

# 🧠 How It Works
1. The script reads the entire input text file.
2. It splits the file into records:
        *   By default, records are separated by blank lines.
        *   You can define a custom separator string.
3. For each record, it applies your regex patterns.
4. Extracted values are written as rows in a CSV file.

Each record becomes one row in the output CSV.


# 📘 Regex Behavior
If your regex contains a capturing group:
```regex
Temperature:\s*([0-9.]+)
```

The script saves the first captured group (`group(1)`).
If there is *no capturing group*, the full match is saved.

# 🧪 Example
## Example Input (`example.txt`)
```
Job ID: 101
Temperature: 300
Pressure: 1.2

Job ID: 102
Temperature: 350
Pressure: 1.5
```

## Run:
```bash
python3 txt_to_csv_extractor.py \
  --infile example.txt \
  --out_csv results.csv \
  --field job_id="Job ID:\s*([0-9]+)" \
  --field temp="Temperature:\s*([0-9.]+)" \
  --field pressure="Pressure:\s*([0-9.]+)"
```

## Output (`results.csv`)
```
job_id,temp,pressure
101,300,1.2
102,350,1.5
```

# 🧩 Custom Record Separator Example
If your file looks like:
```
==== RUN ====
...
==== RUN ====
...
```

Run:
``` bash
python3 txt_to_csv_extractor.py \
  --infile input.txt \
  --out_csv output.csv \
  --record_sep "==== RUN ====" \
  --field value="Energy:\s*([0-9.]+)"
```

# ⚠️ Error Handling
The script will:
*   Stop if the input file does not exist
*   Stop if no `--field` is provided
*   Validate regex patterns before execution
*   Leave empty cells if a field is not found in a record

# 📁 Suggested Repository Structure
```
txt-to-csv-extractor/
│
├── txt_to_csv_extractor.py
├── README.md
└── examples/
    └── example.txt
```

# 🎯 Use Cases
*   Simulation log parsing (MD, ML, HPC jobs)
*   Scientific output extraction
*   Batch result aggregation
*   Converting legacy text reports to CSV
*   Research reproducibility workflows

