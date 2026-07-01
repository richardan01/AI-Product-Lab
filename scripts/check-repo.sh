#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "README.md"
  "PROOF-OF-WORK.md"
  "REPO-RELATIONSHIP.md"
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

placeholder_files=(
  "README.md"
  "PROOF-OF-WORK.md"
  "REPO-RELATIONSHIP.md"
)

if rg --fixed-strings "[Your name]" "${placeholder_files[@]}"; then
  echo "Unresolved placeholder found: [Your name]" >&2
  exit 1
fi

echo "Repo proof-of-work checks passed."
