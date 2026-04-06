# 🧹 Transcript Cleaner

A robust Python tool for cleaning raw transcripts by removing timestamps and formatting text for downstream analysis (NLP, ML, documentation, etc.).

---

## 🚀 Features

- Removes timestamps:
  - `MM:SS` → `0:06`
  - `HH:MM:SS` → `1:30:08`
- Handles:
  - timestamps at the start of lines
  - timestamps embedded within sentences
- Cleans:
  - extra whitespace
  - empty lines after removal
  - unicode artifacts (non-breaking spaces, dashes)
- Supports:
  - single file processing
  - batch processing (entire folder)

---

## 📂 Example

### Input (raw transcript)
```
0:00
Welcome to the podcast
1:30:08
This is an example transcript
```

### Output (cleaned)
```
Welcome to the podcast
This is an example transcript
```
---

## ⚙️ Installation

No external dependencies required.

```bash
python3 --version
```

## ▶️ Usage
### 1. Single File
```python
python3 transcript_cleaner.py input.txt output.txt
```

### 2. Batch Mode (Folder)
```python
python3 transcript_cleaner.py raw_folder cleaned_folder
```

*   All `.txt` files in `raw_folder` will be processed
*   Cleaned files will be saved in `cleaned_folder`

## 📁 Recommended Structure
```
Data_Processing/
└── transcript_cleaning/
    ├── transcript_cleaner.py
    ├── README.md
    └── examples/
        ├── raw.txt
        └── cleaned.txt
```
## 🧠 Use Cases
*   Preparing transcripts for:
        *   NLP pipelines
        *   Embedding models
        *   Diffusion / generative models
*   Cleaning lecture recordings
*   Preprocessing YouTube / podcast transcripts
*   Converting transcripts into readable text

## ⚠️ Notes
*   Only `.txt` files are processed in batch mode
*   Input files must be UTF-8 encoded
*   Designed for noisy real-world transcript data

