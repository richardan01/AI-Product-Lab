#!/usr/bin/env bash
# check-eval-freshness.sh — remote replay of the eval-ci sentinel.
#
# The /eval-ci skill blocks /peer-review and /go-nogo from citing a suite whose
# source changed but wasn't re-run. This is its GitHub-side counterpart:
#
#   HARD FAIL  — any uncleared `pending` row in Evals/_pending-reruns.md
#   WARN only  — a suite whose newest run in Evals/run-log.md is >60 days old
#                (the 60-day cadence in Evals/index.md). Never changes exit code,
#                so a known-stale suite can't wedge unrelated PRs.
#
# Exit 0 = no uncleared pending rows; exit 1 = at least one.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LEDGER="$ROOT/Evals/_pending-reruns.md"
RUN_LOG="$ROOT/Evals/run-log.md"

pending=0

if [[ -f "$LEDGER" ]]; then
  # A row is an uncleared pending re-run if it is a table data row that mentions
  # "pending" and does NOT mention "cleared" (case-insensitive). This is robust
  # to the ledger's two row shapes (clean 6-column rows and the shorter
  # hardening-batch rows) without relying on a fixed column index.
  while IFS= read -r line; do
    # table data rows only: start with "|", not a header/separator row
    [[ "$line" == \|* ]] || continue
    case "$line" in
      *---*) continue ;;                 # |---|---| separator
      *Suite*Source*) continue ;;        # header row
    esac
    lc="$(printf '%s' "$line" | tr '[:upper:]' '[:lower:]')"
    if [[ "$lc" == *pending* && "$lc" != *cleared* ]]; then
      suite="$(printf '%s' "$line" | sed -E 's/^\|[[:space:]]*//; s/[[:space:]]*\|.*$//')"
      echo "PENDING RE-RUN: suite '$suite' has an uncleared row in Evals/_pending-reruns.md" >&2
      pending=$((pending + 1))
    fi
  done < "$LEDGER"
else
  echo "WARN: $LEDGER not found — skipping pending-rerun check." >&2
fi

# --- Non-blocking staleness warning (best-effort; never affects exit code) ---
if [[ -f "$RUN_LOG" ]]; then
  newest="$(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$RUN_LOG" | sort | tail -1 || true)"
  if [[ -n "$newest" ]]; then
    newest_s="$(date -j -f '%Y-%m-%d' "$newest" +%s 2>/dev/null \
      || date -d "$newest" +%s 2>/dev/null || echo '')"
    now_s="$(date +%s)"
    if [[ -n "$newest_s" ]]; then
      age_days=$(( (now_s - newest_s) / 86400 ))
      if [[ "$age_days" -gt 60 ]]; then
        echo "WARN: newest eval run in run-log.md is ${age_days}d old (>60d cadence in Evals/index.md)." >&2
      fi
    fi
  fi
fi

if [[ "$pending" -ne 0 ]]; then
  echo "" >&2
  echo "Eval freshness FAILED: $pending uncleared pending re-run(s)." >&2
  echo "Run the affected suite and clear its row in Evals/_pending-reruns.md before merge." >&2
  exit 1
fi

echo "Eval freshness passed: no uncleared pending re-runs."
exit 0
