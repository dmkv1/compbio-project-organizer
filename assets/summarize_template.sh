#!/usr/bin/env bash
#
# summarize — reports progress on the <YYYY-MM-DD topic> experiment.
#
# Called by runall as its final step, and safe to run standalone at any time, including
# mid-run: it should degrade gracefully and report on whatever outputs exist so far rather
# than failing outright, so a long job can be checked in on without waiting for it to finish.
set -uo pipefail

# Run from this script's own directory so relative paths resolve from anywhere.
cd "$(dirname "$0")"

OUT_DIR="."
SPLIT_DIRS=(split1 split2 split3)

echo "=== progress: $(date) ==="
for split in "${SPLIT_DIRS[@]}"; do
  result="$OUT_DIR/$split/result.tsv"
  if [[ -e "$result" ]]; then
    echo "[done]    $split  ($(wc -l < "$result") lines)"
  else
    echo "[pending] $split"
  fi
done
