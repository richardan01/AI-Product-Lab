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

# Generic residue guard (non-revealing patterns only — the private term list
# lives in scripts/residue-terms.local, which is gitignored and never ships).
# Note: "Day-job PM" personas in onboarding eval fixtures are intentional
# fictional test data, so the pattern targets the private-layer file names,
# not the generic phrase.
generic_pattern='dayjob-active|cdp-implementation|cdp-specialist'
if rg -i --glob '!scripts/*' "$generic_pattern" .; then
  echo "Generic residue found matching: $generic_pattern" >&2
  exit 1
fi

# Private residue terms (optional, local-only): one extended-regex pattern per
# line; blank lines and #-comments ignored. See scripts/residue-terms.local.example.
local_terms_file="scripts/residue-terms.local"
if [[ -f "$local_terms_file" ]]; then
  local_pattern="$(grep -Ev '^\s*(#|$)' "$local_terms_file" | paste -sd'|' -)"
  if [[ -n "$local_pattern" ]] && rg -i --glob '!scripts/*' "$local_pattern" .; then
    echo "Private residue term matched (see $local_terms_file)." >&2
    exit 1
  fi
fi

echo "Repo proof-of-work checks passed."
