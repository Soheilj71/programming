
# Change Any Line (Portable)

A tiny, portable Bash tool to replace **any line → any line** across many files.
- Works on **Linux & macOS** (no brittle `sed -i` flags).
- Supports **exact**, **contains**, and **regex** matching.
- Safe: writes via temp files, optional **.bak** backups, and **dry-run** diff.

## Quick Start

```bash
chmod +x change_any_line.sh
```
# Exact line → exact line (example: Slurm walltime)
```bash
./change_any_line.sh \
  -s "#SBATCH --time=72:00:00" \
  -t "#SBATCH --time=48:00:00" \
  -g "max_*" -f "src/slurm.sh"
```

# Modes
-  exact (default): line must match exactly.
-  contains: line contains the given text.
-   egex: POSIX ERE (e.g., ^#SBATCH[[:space:]]+--time=.*$).
```bash
 # Regex: normalize any --time to 48h
./change_any_line.sh -M regex \
  -s '^#SBATCH[[:space:]]+--time=.*$' \
  -t '#SBATCH --time=48:00:00' \
  -g 'max_*' -f 'src/slurm.sh'
```

# File Selection (choose one style)

# A) Directory glob + relative file path

```bash
# Edit 'src/slurm.sh' inside each 'max_*' directory
./change_any_line.sh -s "old" -t "new" -g 'max_*' -f 'src/slurm.sh'
```

# B) Recursive search from a root by filename

```bash
# Edit all .sh files under the repo
./change_any_line.sh -s "old" -t "new" -r . -N '*.sh'
```

# Replace all matches per file

```bash
./change_any_line.sh -a -M contains -s 'module load' \
  -t 'module load python/miniforge-24.3.0' \
  -r . -N '*.sh'
```

# Dry-run (recommended first)

```bash
./change_any_line.sh -n -M contains -s '--gpus-per-node' \
  -t '#SBATCH --gpus-per-node=4' \
  -g 'max_*' -f 'src/slurm.sh'
```

# Options

```
Required:
  -s, --search TEXT      The line to match (text/regex per mode)
  -t, --to TEXT          Replacement line

Match mode:
  -M, --mode MODE        exact | contains | regex  (default: exact)
  -a, --all              Replace all matches per file (default: only first)

Safety:
  -n, --dry-run          Show planned changes with unified diff
  -b, --backup EXT       Backup extension (default: .bak; set "" to disable)

File selection (choose one style):
  A) -g, --glob GLOB     Top-level directory glob (default: *)
     -f, --file RELPATH  Relative file path within each dir
  B) -r, --root DIR      Root directory for recursive search (default: .)
     -N, --name PATTERN  Filename pattern for find (e.g., "*.sh")
```

# Tips
-  Regex is POSIX ERE: use `[[:space:]]` instead of `\s`, etc.
-  Backups appear as filename.ext.bak. Restore with `git checkout -- .` (tracked) or rename.
-  Output shows `[skip]` if no matching line is found in a file.
-  Commit the script + README to your repo’s tools/ or scripts/ directory.
