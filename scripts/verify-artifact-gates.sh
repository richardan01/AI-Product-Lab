#!/usr/bin/env bash
# verify-artifact-gates.sh — remote replay of the publish gate.
#
# The local PreToolUse hook (Tools/gate-check.sh) blocks *writing* an ungated
# artifact inside Claude Code. This script is its GitHub-side counterpart: it
# fails CI if any committed artifact under Artifacts/ was shipped without a
# valid Riddler + Vicki Vale verdict, so a commit that bypasses the local hook
# still can't land on main.
#
# For each content artifact under Artifacts/ it requires:
#   1. Both sidecars exist:  <artifact>.riddler-passed  and  <artifact>.vicki-passed
#      (reviewer-verdict-schema.md rule 5 — sidecars committed alongside the artifact)
#   2. Each sidecar's Verdict is PASS or CONDITIONAL
#   3. Each sidecar's Hash matches the current sha256 of the artifact
#      (schema rule 4 — content changed after review => verdict void => re-run gate)
#
# Content artifact = anything under Artifacts/ that is NOT README.md, .gitkeep,
# a verdict sidecar (*-passed), or a block record (*-blocked-*.md). This mirrors
# the publishable-file detection in Tools/gate-check.sh so local and CI agree on
# what counts as an artifact.
#
# Exit 0 = all artifacts gated and hashes fresh; exit 1 = at least one violation.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ARTIFACTS_DIR="$ROOT/Artifacts"

if [[ ! -d "$ARTIFACTS_DIR" ]]; then
  echo "No Artifacts/ directory — nothing to gate."
  exit 0
fi

# First 12 chars of the sha256 of a file (schema format). Prefer sha256sum
# (Linux/CI); fall back to shasum -a 256 (macOS).
sha12_of() {
  local f="$1" hash
  if command -v sha256sum >/dev/null 2>&1; then
    hash="$(sha256sum "$f" | awk '{print $1}')"
  else
    hash="$(shasum -a 256 "$f" | awk '{print $1}')"
  fi
  printf '%s' "${hash:0:12}"
}

# Value of a header field ("Field:  value") from a verdict file, trimmed.
field_of() {
  local file="$1" key="$2"
  grep -E "^${key}:" "$file" | head -1 \
    | sed -E "s/^${key}:[[:space:]]*//" \
    | sed -E 's/[[:space:]]+$//'
}

failures=0
checked=0

# Walk every file under Artifacts/, skip the non-artifact classes.
while IFS= read -r -d '' art; do
  base="$(basename "$art")"
  case "$base" in
    README.md|.gitkeep) continue ;;
    *-passed) continue ;;                 # verdict sidecars (any gate)
    *-blocked-*.md) continue ;;           # block records
    .*) continue ;;                       # other dotfiles
  esac

  checked=$((checked + 1))
  rel="${art#"$ROOT"/}"
  riddler="${art}.riddler-passed"
  vale="${art}.vicki-passed"

  # 1. Both sidecars must exist.
  if [[ ! -f "$riddler" ]]; then
    echo "UNGATED: $rel — missing $(basename "$riddler") (no Riddler pass)" >&2
    failures=$((failures + 1))
    continue
  fi
  if [[ ! -f "$vale" ]]; then
    echo "UNGATED: $rel — missing $(basename "$vale") (no Vicki Vale pass)" >&2
    failures=$((failures + 1))
    continue
  fi

  actual_hash="$(sha12_of "$art")"

  # 2 + 3. Verdict valid and hash fresh, for each sidecar.
  for sidecar in "$riddler" "$vale"; do
    verdict="$(field_of "$sidecar" "Verdict")"
    stored_hash="$(field_of "$sidecar" "Hash")"
    stored_hash="${stored_hash:0:12}"

    case "$verdict" in
      PASS|CONDITIONAL) ;;
      *)
        echo "BAD VERDICT: $rel — $(basename "$sidecar") has Verdict='${verdict:-<empty>}' (need PASS or CONDITIONAL)" >&2
        failures=$((failures + 1))
        ;;
    esac

    if [[ -z "$stored_hash" ]]; then
      echo "NO HASH: $rel — $(basename "$sidecar") has no Hash field" >&2
      failures=$((failures + 1))
    elif [[ "$stored_hash" != "$actual_hash" ]]; then
      echo "STALE VERDICT: $rel — $(basename "$sidecar") Hash=$stored_hash but artifact is $actual_hash (content changed after review; re-run the gate)" >&2
      failures=$((failures + 1))
    fi
  done
done < <(find "$ARTIFACTS_DIR" -type f -print0)

if [[ "$failures" -ne 0 ]]; then
  echo "" >&2
  echo "Artifact gate FAILED: $failures violation(s) across $checked artifact(s)." >&2
  echo "Every file under Artifacts/ must ship with fresh .riddler-passed + .vicki-passed sidecars." >&2
  exit 1
fi

echo "Artifact gate passed: $checked content artifact(s) checked, all gated with fresh verdicts."
exit 0
