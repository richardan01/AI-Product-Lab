#!/usr/bin/env bash
# gate-check.sh — PreToolUse publish gate for public artifacts.
#
# Wired in .claude/settings.json as a PreToolUse hook on Write|Edit.
# Gates any write that resolves under Artifacts/, or whose filename contains
# -essay, -post, or -thread, on BOTH global gate markers being present AND
# fresh (mtime within GATE_TTL_SECONDS, default 6h):
#   _Registry/.riddler-passed   (written by /riddler on PASS/CONDITIONAL)
#   _Registry/.vicki-passed     (written by /vale on PASS/CONDITIONAL)
# Markers are disarmed by Workflows/gate-merge.md after the artifact is staged,
# so a stale pass can never ship the next artifact — and an expired-but-present
# marker is treated the same as missing.
#
# Hook contract: reads the tool-call JSON on stdin; exit 0 = allow, exit 2 = block
# (stderr is shown to the model so it knows why).

set -euo pipefail

if command -v python3 >/dev/null 2>&1; then
  ROOT="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' \
    "${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}")"

  # NOTE: must use `python3 -c '...' "$ROOT"`, not `python3 - <<EOF`.
  # A heredoc-to-stdin script source consumes this process's own stdin as the
  # program text, leaving nothing for json.load(sys.stdin) to read below — the
  # hook's JSON payload arrives on stdin, so the script body must come via -c.
  DECISION="$(python3 -c '
import json, os, sys

root = sys.argv[1]

try:
    data = json.load(sys.stdin)
except Exception:
    print("ALLOW")
    sys.exit(0)

ti = data.get("tool_input") or {}
file_path = ti.get("file_path") or ti.get("notebook_path") or ""
if not file_path:
    print("ALLOW")
    sys.exit(0)

abs_path = file_path if os.path.isabs(file_path) else os.path.join(root, file_path)
real_path = os.path.realpath(abs_path)

artifacts_dir = os.path.realpath(os.path.join(root, "Artifacts"))
basename = os.path.basename(real_path)

under_artifacts = real_path == artifacts_dir or real_path.startswith(artifacts_dir + os.sep)
publishable_name = any(tag in basename for tag in ("-essay", "-post", "-thread"))

print("GATE" if (under_artifacts or publishable_name) else "ALLOW")
' "$ROOT")"
else
  # Fail-closed shell fallback for environments without python3. If this
  # branch errored out instead, Claude Code would treat the hook failure as
  # non-blocking and perform the write — silently bypassing the gate.
  ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
  RAW="$(cat 2>/dev/null || true)"
  FILE_PATH="$(printf '%s' "$RAW" | tr -d '\n' \
    | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
  if [ -z "$FILE_PATH" ]; then
    FILE_PATH="$(printf '%s' "$RAW" | tr -d '\n' \
      | sed -n 's/.*"notebook_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
  fi

  if [ -z "$FILE_PATH" ]; then
    DECISION="ALLOW"
  elif printf '%s' "$FILE_PATH" | grep -q '\.\.'; then
    # Cannot canonicalize safely without python3 — fail closed.
    DECISION="GATE"
  else
    # Squash /./ segments and duplicate slashes before matching.
    NORM="$(printf '%s' "$FILE_PATH" | sed 's#/\./#/#g; s#//*#/#g')"
    BASE="${NORM##*/}"
    case "$NORM" in
      "$ROOT"/Artifacts/*|Artifacts/*) DECISION="GATE" ;;
      *)
        case "$BASE" in
          *-essay*|*-post*|*-thread*) DECISION="GATE" ;;
          *) DECISION="ALLOW" ;;
        esac
        ;;
    esac
  fi
fi

[ "$DECISION" = "ALLOW" ] && exit 0

TTL_SECONDS="${GATE_TTL_SECONDS:-21600}"  # 6 hours

marker_status() {
  # Uses find -mmin (portable across GNU/BSD, no python3 needed) so the TTL
  # check works in the shell-fallback path too. Granularity: minutes.
  local marker="$1"
  if [ ! -f "$marker" ]; then
    echo "missing"
    return
  fi
  local ttl_min=$(( (TTL_SECONDS + 59) / 60 ))
  if [ -n "$(find "$marker" -mmin +"$ttl_min" 2>/dev/null)" ]; then
    echo "expired"
  else
    echo "ok"
  fi
}

RIDDLER_STATUS="$(marker_status "$ROOT/_Registry/.riddler-passed")"
VALE_STATUS="$(marker_status "$ROOT/_Registry/.vicki-passed")"

if [ "$RIDDLER_STATUS" != "ok" ] || [ "$VALE_STATUS" != "ok" ]; then
  echo "PUBLISH GATE BLOCKED: this write requires both gate markers present and fresh (TTL ${TTL_SECONDS}s)." >&2
  echo "  riddler: $RIDDLER_STATUS   vale: $VALE_STATUS" >&2
  echo "Run /riddler and /vale on the artifact (via Workflows/gate-dispatch.md). Both must PASS before staging." >&2
  exit 2
fi

exit 0
