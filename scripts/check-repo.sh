#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "README.md"
  "PROOF-OF-WORK.md"
  "GOALS.md"
  "HOW-IT-WORKS.md"
  "CLAUDE.md"
  "Tools/gate-check.sh"
  "_Registry/reviewer-verdict-schema.md"
  "_Registry/voice-map.md"
  "_Registry/artifact-log.md"
  "Artifacts/README.md"
  "Workflows/regeval-run.md"
  "Evals/regeval/regeval-suite.md"
  "Evals/run-log.md"
  "Projects/ralph/brief.md"
)

missing=0
for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required file: $file" >&2
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

# External-facing docs must carry no unresolved identity placeholders.
placeholder_files=(
  "README.md"
  "PROOF-OF-WORK.md"
  "GOALS.md"
  "HOW-IT-WORKS.md"
)

if rg --fixed-strings "[Your name]" "${placeholder_files[@]}"; then
  echo "Unresolved placeholder found: [Your name]" >&2
  exit 1
fi

# No day-job / employer / sibling-repo residue anywhere in tracked files.
# (Case-insensitive; excludes this script itself.)
residue_pattern='kpay|dayjob-active|cdp-feature|martech-cdp|Product-Management_OS|Anthropic Singapore|Microsoft Singapore'
if rg -i --glob '!scripts/check-repo.sh' "$residue_pattern" .; then
  echo "Residue found matching: $residue_pattern" >&2
  exit 1
fi

echo "Repo proof-of-work checks passed."
