#!/usr/bin/env bash
# gate-check.sh — PreToolUse publish gate for public artifacts.
#
# Wired in .claude/settings.json as a PreToolUse hook on Write|Edit.
# Blocks any write into Artifacts/ unless BOTH global gate markers are armed:
#   _Registry/.riddler-passed   (written by /riddler on PASS/CONDITIONAL)
#   _Registry/.vicki-passed     (written by /vale on PASS/CONDITIONAL)
# Markers are disarmed by Workflows/gate-merge.md after the artifact is staged,
# so a stale pass can never ship the next artifact.
#
# Hook contract: reads the tool-call JSON on stdin; exit 0 = allow, exit 2 = block
# (stderr is shown to the model so it knows why).

set -euo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"

FILE_PATH="$(python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
ti = data.get("tool_input") or {}
print(ti.get("file_path") or ti.get("notebook_path") or "")
' 2>/dev/null || true)"

# Not a file write we can evaluate — allow.
[ -z "$FILE_PATH" ] && exit 0

# Normalize to a repo-relative path for matching.
REL="${FILE_PATH#"$ROOT"/}"

case "$REL" in
  Artifacts/*) ;;
  *) exit 0 ;;  # gate only guards the public-artifact staging area
esac

MISSING=""
[ -f "$ROOT/_Registry/.riddler-passed" ] || MISSING="_Registry/.riddler-passed"
[ -f "$ROOT/_Registry/.vicki-passed" ] || MISSING="${MISSING:+$MISSING + }_Registry/.vicki-passed"

if [ -n "$MISSING" ]; then
  echo "PUBLISH GATE BLOCKED: writing to Artifacts/ requires both gate markers; missing: $MISSING." >&2
  echo "Run /riddler and /vale on the artifact (via Workflows/gate-dispatch.md). Both must PASS before staging." >&2
  exit 2
fi

exit 0
