#!/usr/bin/env bash
#written by: Soheil Jamali
#Email: sjamali@uark.edu, soheil.jamali.dev@gmail.com

# change_any_line.sh — replace lines in many files (exact/contains/regex).
# Portable: uses awk + temp files (safe on Linux/macOS). Git-friendly backups.
# Exit codes: 0 OK, 1 bad args, 2 no files matched, 3 no changes made.

set -euo pipefail

# ---------- defaults ----------
MODE="exact"             # exact | contains | regex
SEARCH=""                # text or regex to match (by MODE)
REPLACE=""               # full replacement line
ALL=false                # replace all matches in a file (default: only first)
DRY_RUN=false
BACKUP_EXT=".bak"        # set "" to disable backups

# File selection (choose one style):
GLOB_DIR="*"             # scan these top-level dirs (e.g., max_*), used with --file
REL_PATH=""              # relative path within each dir (e.g., src/slurm.sh)
NAME_PATTERN=""          # alternatively: recursive search by -name (e.g., "*.sh")
ROOT_DIR="."             # base dir for recursive mode

usage() {
  cat <<EOF
Usage:
  $(basename "$0") -s SEARCH -t REPLACE [options]

Match mode (choose one; default: exact):
  -M, --mode MODE        exact | contains | regex   (default: exact)

What to change:
  -s, --search TEXT      The line to match (text or regex depending on MODE)
  -t, --to TEXT          Replacement line

How many:
  -a, --all              Replace all matches per file (default: only first)

Safety:
  -n, --dry-run          Show changes without writing
  -b, --backup EXT       Backup extension (default: .bak, set "" to disable)

File selection (choose ONE style):
  (A) Dir+relpath:
      -g, --glob GLOB        Top-level directory glob (default: *)
      -f, --file RELPATH     Relative file path in each dir (e.g., src/slurm.sh)

  (B) Recursive by name:
      -r, --root DIR         Root directory to search from (default: .)
      -N, --name PATTERN     Filename pattern, e.g. "*.sh" or "slurm.sh"

Examples:
  # Exact line to exact line (Slurm time)
  $(basename "$0") -s "#SBATCH --time=72:00:00" -t "#SBATCH --time=48:00:00" \
    -g "max_*" -f "src/slurm.sh"

  # Regex mode: replace any time with 48h
  $(basename "$0") -M regex -s '^#SBATCH[[:space:]]+--time=.*$' \
    -t '#SBATCH --time=48:00:00' -g "max_*" -f "src/slurm.sh"

  # Contains mode: any line containing 'gpus-per-node' -> set to 4
  $(basename "$0") -M contains -s "--gpus-per-node" \
    -t "#SBATCH --gpus-per-node=4" -g "max_*" -f "src/slurm.sh"

  # Recursive: all .sh files under repo
  $(basename "$0") -s "module load python/miniforge" \
    -t "module load python/miniforge-24.3.0" -r . -N "*.sh"
EOF
}

# ---------- parse args ----------
while [[ $# -gt 0 ]]; do
  case "$1" in
    -M|--mode)        MODE="${2:?}"; shift 2;;
    -s|--search)      SEARCH="${2:?}"; shift 2;;
    -t|--to)          REPLACE="${2:?}"; shift 2;;
    -a|--all)         ALL=true; shift;;
    -n|--dry-run)     DRY_RUN=true; shift;;
    -b|--backup)      BACKUP_EXT="${2:-}"; shift 2;;
    -g|--glob)        GLOB_DIR="${2:?}"; shift 2;;
    -f|--file)        REL_PATH="${2:?}"; shift 2;;
    -r|--root)        ROOT_DIR="${2:?}"; shift 2;;
    -N|--name)        NAME_PATTERN="${2:?}"; shift 2;;
    -h|--help)        usage; exit 0;;
    *) echo "Unknown option: $1" >&2; usage; exit 1;;
  esac || true
done

# Basic validation
if [[ -z "$SEARCH" || -z "$REPLACE" ]]; then
  echo "Error: --search and --to are required." >&2
  usage; exit 1
fi
if [[ "$MODE" != "exact" && "$MODE" != "contains" && "$MODE" != "regex" ]]; then
  echo "Error: --mode must be one of: exact | contains | regex" >&2
  exit 1
fi

# Collect files
files=()
if [[ -n "$REL_PATH" ]]; then
  shopt -s nullglob
  for d in ${GLOB_DIR}; do
    [[ -d "$d" && -f "$d/$REL_PATH" ]] && files+=("$d/$REL_PATH")
  done
elif [[ -n "$NAME_PATTERN" ]]; then
  while IFS= read -r -d '' f; do files+=("$f"); done < <(find "$ROOT_DIR" -type f -name "$NAME_PATTERN" -print0)
else
  echo "Error: choose one file selection method: (-g with -f) OR (-r with -N)" >&2
  usage; exit 1
fi

if [[ ${#files[@]} -eq 0 ]]; then
  echo "No files matched selection." >&2
  exit 2
fi

# ---------- worker ----------
changed_files=0

for file in "${files[@]}"; do
  tmp="${file}.tmp.$$"
  status=0

  case "$MODE" in
    exact)
      awk -v s="$SEARCH" -v rep="$REPLACE" -v all="$ALL" '
        BEGIN {changed=0; done=0}
        {
          if ($0==s) {
            if (all=="true") { print rep; changed=1; next }
            else if (done==0){ print rep; changed=1; done=1; next }
          }
          print $0
        }
        END { if (!changed) exit 3 }
      ' "$file" > "$tmp" || status=$?
      ;;
    contains)
      awk -v s="$SEARCH" -v rep="$REPLACE" -v all="$ALL" '
        BEGIN {changed=0; done=0}
        {
          if (index($0, s)>0) {
            if (all=="true") { print rep; changed=1; next }
            else if (done==0){ print rep; changed=1; done=1; next }
          }
          print $0
        }
        END { if (!changed) exit 3 }
      ' "$file" > "$tmp" || status=$?
      ;;
    regex)
      awk -v re="$SEARCH" -v rep="$REPLACE" -v all="$ALL" '
        BEGIN {changed=0; done=0}
        {
          if ($0 ~ re) {
            if (all=="true") { print rep; changed=1; next }
            else if (done==0){ print rep; changed=1; done=1; next }
          }
          print $0
        }
        END { if (!changed) exit 3 }
      ' "$file" > "$tmp" || status=$?
      ;;
  esac

  if [[ ${status:-0} -eq 3 ]]; then
    echo "[skip]  No match in: $file"
    rm -f "$tmp"
    continue
  fi

  if $DRY_RUN; then
    echo "[plan]  Would update: $file"
    if command -v diff >/dev/null 2>&1; then
      diff -u --label "before:$file" --label "after:$file" "$file" "$tmp" || true
    fi
    rm -f "$tmp"
  else
    [[ -n "$BACKUP_EXT" ]] && cp -p "$file" "${file}${BACKUP_EXT}"
    mv "$tmp" "$file"
    echo "[done]  Updated: $file"
    changed_files=$((changed_files+1))
  fi
done

if ! $DRY_RUN && [[ $changed_files -eq 0 ]]; then
  echo "No files changed." >&2
  exit 3
fi
