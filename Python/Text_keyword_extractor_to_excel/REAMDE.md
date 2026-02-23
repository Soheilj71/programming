# TXT Keyword Extractor → Excel

This tool reads **any text file** (`.txt`, `.log`, etc.), searches for user-provided **keywords or regex patterns**, and exports every match into a **table** (Excel `.xlsx` preferred, or CSV fallback).

---

## What it does

- Reads an input text file line-by-line
- Searches for one or more keywords / regex patterns
- For each match, saves a row containing:
  - `match_id` (1, 2, 3, ...)
  - `keyword` (which keyword/pattern matched)
  - `line_number`
  - `line_text` (the full line)
  - `context_before` (optional lines before the match)
  - `context_after` (optional lines after the match)
- Writes output to:
  - Excel (`.xlsx`) if `pandas` + `openpyxl` are available
  - Otherwise CSV (`.csv`) automatically

---

## Requirements

### Minimal (CSV only)
- Python 3.9+ (CSV output uses only the standard library)

### Recommended (Excel output)
Install:
- `pandas`
- `openpyxl`

```bash
pip install pandas openpyxl
```

# Usage
## 1) Interactive mode (recommended)
You run the script and it will ask you to type keywords/patterns.
``` bash
python txt_keyword_extractor_to_excel.py --in result_KL.txt --out extracted.xlsx
```

Then type one keyword per line, for example:
```
ERROR
WARNING
KL\(P_real
```

Press ENTER on an empty line to finish.

## 2) Non-interactive mode (keywords from command line)
This is useful for scripts and automation:
```bash
python txt_keyword_extractor_to_excel.py \
  --in result_KL.txt \
  --out extracted.xlsx \
  --keywords ERROR WARNING "KL\\(P_real"
```
# Options

## Case-insensitive matching

```bash
python txt_keyword_extractor_to_excel.py --in mylog.txt --ignore-case
```

## Include context lines (before/after each match)
Example: include 2 lines before and 2 lines after each match:

```bash
python txt_keyword_extractor_to_excel.py --in mylog.txt --context 2
```

# Notes about keywords (IMPORTANT)
This script treats every keyword you enter as a regular expression (regex) pattern.
    * If you type a plain word like `ERROR`, it works like normal keyword searching.
    * If you type special regex characters like `(` or `*`, they affect matching.

If you want to search for characters like parentheses literally, you should escape them:
    * Literal `(` in regex becomes `\(`

Example:
    * Search for `KL(P_real || Q_muller)` literally:
```code 
KL\(P_real \|\| Q_muller\)
```

# Output
## Excel

If Excel writing succeeds, you get:
    * `extracted.xlsx`
    * Sheet name: `Extracted`

## CSV fallback

If Excel writing fails (missing packages), you get:
    * `extracted.csv`

# Troubleshooting
## No matches found
    * Check spelling
    * Try `--ignore-case`
    * If using regex, make sure your regex is correct

## Invalid regex pattern
You entered a regex that Python cannot compile. Common mistakes:
    * Unclosed parentheses: `(`
    * Unescaped special characters

Try using a plain word first to confirm the tool works.


