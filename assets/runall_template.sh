#!/usr/bin/env bash
#
# runall — driver script for the <YYYY-MM-DD topic> experiment.
#
# Reference skeleton for a compbio driver script. Adapt language/tooling to whatever the
# project actually uses (Python, R, Snakemake, Nextflow, ...) — what matters is that the
# resulting script follows the same rules this one demonstrates:
#   1. records every operation
#   2. is commented well enough to follow without reading called scripts
#   3. never requires hand-editing intermediate files
#   4. centralizes file/directory names here and passes them to sub-scripts
#   5. uses only relative paths within the project
#   6. is restartable: re-run this script and only the missing outputs get recomputed
#
# Abort immediately on any error or unset variable, and on failures inside a pipeline.
set -euo pipefail

# --- centralize every path used by this experiment (rule 4) -----------------------------------
PROJECT_ROOT="../../.."                 # relative to this script's directory (rule 5)
DATA_DIR="$PROJECT_ROOT/data/<YYYY-MM-DD>"
BIN_DIR="$PROJECT_ROOT/bin"
OUT_DIR="."                             # this experiment's own results/<YYYY-MM-DD>/ directory

SPLIT_DIRS=(split1 split2 split3)

# --- restartable step: skip work whose output already exists (rule 6) -------------------------
run_step () {
  local output="$1"; shift
  if [[ -e "$output" ]]; then
    echo "[skip] $output already exists"
    return 0
  fi
  echo "[run]  $*  ->  $output"
  local tmp="${output}.tmp"
  "$@" > "$tmp"                          # write to a temp name first (atomic output, see SKILL.md)
  mv "$tmp" "$output"
}

# --- example pipeline steps --------------------------------------------------------------------
for split in "${SPLIT_DIRS[@]}"; do
  mkdir -p "$OUT_DIR/$split"
  run_step "$OUT_DIR/$split/result.tsv" \
    "$BIN_DIR/analyze.py" --input "$DATA_DIR/input.tsv" --split "$split"
done

# --- always finish by summarizing progress, even on a partial run -----------------------------
"$(dirname "$0")/summarize"
