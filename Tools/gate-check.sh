#!/usr/bin/env bash
# gate-check.sh — PreToolUse publish gate for public artifacts.
#
# Wired in .claude/settings.json as a PreToolUse hook on
# Write|Edit|MultiEdit|NotebookEdit|Bash.
#
# Gates any write that resolves under Artifacts/, or whose filename contains
# -essay, -post, or -thread, on BOTH global gate markers being present, fresh
# (mtime within GATE_TTL_SECONDS, default and maximum 6h), and VALID:
#   _Registry/.riddler-passed   (written by /riddler on PASS/CONDITIONAL)
#   _Registry/.vicki-passed     (written by /vale on PASS/CONDITIONAL)
#
# Marker validity (per _Registry/reviewer-verdict-schema.md): the marker must
# be non-empty, carry `Verdict: PASS` or `Verdict: CONDITIONAL`, and its
# `File:` line must name the same basename as the file being written — so a
# review of artifact A can never ship artifact B, and an empty forged marker
# never arms the gate. The staged artifact must keep the reviewed filename.
#
# Bash coverage: commands that combine a write indicator (redirection, tee,
# cp, mv, touch, sed -i, …) with a gated path are held to the same marker
# check, and commands that create or modify the _Registry/ markers themselves
# are always blocked (rm for the gate-merge disarm is allowed). This is drift
# protection against shortcutting the review flow, not an adversarial
# security boundary — shell parsing is heuristic by nature.
#
# Failure posture: ANY internal error fails CLOSED (exit 2). Claude Code
# treats other non-zero exits as non-blocking, so an error path that exits 1
# would silently let the write through.
#
# Markers are disarmed by Workflows/gate-merge.md Step 6 after the artifact
# is staged. They are gitignored — a committed marker would get a fresh mtime
# on every checkout and permanently arm the gate.
#
# Hook contract: reads the tool-call JSON on stdin; exit 0 = allow,
# exit 2 = block (stderr is shown to the model so it knows why).

set -Eeuo pipefail
trap 'echo "PUBLISH GATE ERROR: Tools/gate-check.sh failed internally — failing closed (call blocked). Fix the hook before retrying." >&2; exit 2' ERR

ROOT_RAW="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"

# TTL: env-tunable downward only. Clamp so the freshness window can never be
# extended past 6h from the environment.
TTL_SECONDS="${GATE_TTL_SECONDS:-21600}"
case "$TTL_SECONDS" in
  ''|*[!0-9]*) TTL_SECONDS=21600 ;;
esac
if [ "$TTL_SECONDS" -gt 21600 ]; then
  TTL_SECONDS=21600
fi

# ---------------------------------------------------------------------------
# Decision: ALLOW (exit 0 now), BLOCK (unconditional), or GATE (needs markers).
# DETAIL carries the block reason, or the target basename for marker binding.
# ---------------------------------------------------------------------------

if command -v python3 >/dev/null 2>&1; then
  ROOT="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$ROOT_RAW")"

  # NOTE: must use `python3 -c '...' "$ROOT"`, not `python3 - <<EOF`.
  # A heredoc-to-stdin script source consumes this process's own stdin as the
  # program text, leaving nothing for json.load(sys.stdin) to read below — the
  # hook's JSON payload arrives on stdin, so the script body must come via -c.
  PARSED="$(python3 -c '
import json, os, re, sys

root = sys.argv[1]
WRITE_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")

def out(decision, extra=""):
    print(decision)
    print(extra)
    sys.exit(0)

try:
    data = json.load(sys.stdin)
except Exception:
    out("BLOCK", "malformed hook payload (stdin was not valid JSON) — failing closed")

tool = data.get("tool_name") or ""
ti = data.get("tool_input") or {}

# Shell commands: screen for writes into gated paths and marker tampering.
if tool == "Bash" or ("command" in ti and tool not in WRITE_TOOLS):
    cmd = ti.get("command") or ""
    write_re = re.compile(
        r"(>"                                                  # any redirection
        r"|(^|[;&|`(\s])(tee|cp|mv|touch|rsync|truncate|dd|install|ln)(\s|$)"
        r"|\bsed\b[^;|&]*\s-i)"                                # sed in-place
    )
    marker_re = re.compile(r"_Registry/\.(riddler-passed|vicki-passed|vicki-bounced)")
    gated_re = re.compile(r"(\bartifacts/|-(essay|post|thread))", re.IGNORECASE)
    if marker_re.search(cmd) and write_re.search(cmd):
        out("BLOCK",
            "gate markers are armed only by /riddler and /vale (Write tool, verdict-schema header) "
            "and disarmed with rm (gate-merge Step 6). Bash must not create or modify them.")
    if gated_re.search(cmd) and write_re.search(cmd):
        out("GATE", "")  # no single target file — marker freshness/validity only
    out("ALLOW")

file_path = ti.get("file_path") or ti.get("notebook_path") or ""
if not file_path:
    if tool in WRITE_TOOLS:
        out("BLOCK", "write-tool payload missing file_path — failing closed")
    out("ALLOW")

abs_path = file_path if os.path.isabs(file_path) else os.path.join(root, file_path)
norm_path = os.path.normpath(abs_path)   # lexical target (what the tool writes)
real_path = os.path.realpath(abs_path)   # symlink-resolved target

artifacts_lex = os.path.join(root, "Artifacts")
artifacts_real = os.path.realpath(artifacts_lex)

def under(path, d):
    # Case-insensitive: on case-insensitive filesystems (macOS default),
    # artifacts/x.md and Artifacts/x.md are the same directory.
    p, dl = path.lower(), d.lower()
    return p == dl or p.startswith(dl + os.sep)

# Gate if EITHER the lexical path or its resolved target lands in Artifacts/ —
# a symlink pointing in or out of Artifacts/ must not change the answer.
under_artifacts = (under(norm_path, artifacts_lex) or under(real_path, artifacts_real))
names = (os.path.basename(norm_path), os.path.basename(real_path))
publishable_name = any(tag in b for b in names for tag in ("-essay", "-post", "-thread"))

if under_artifacts or publishable_name:
    out("GATE", os.path.basename(norm_path))
out("ALLOW")
' "$ROOT")"
  DECISION="$(printf '%s\n' "$PARSED" | sed -n '1p')"
  DETAIL="$(printf '%s\n' "$PARSED" | sed -n '2p')"
else
  # Fail-closed shell fallback for environments without python3. Coarser than
  # the python path: no realpath canonicalization, pattern checks run over the
  # raw JSON payload. Ambiguity resolves toward GATE, never toward ALLOW.
  ROOT="$ROOT_RAW"
  RAW="$(cat 2>/dev/null || true)"
  FLAT="$(printf '%s' "$RAW" | tr -d '\n')"
  FILE_PATH="$(printf '%s' "$FLAT" \
    | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
  if [ -z "$FILE_PATH" ]; then
    FILE_PATH="$(printf '%s' "$FLAT" \
      | sed -n 's/.*"notebook_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
  fi

  DECISION="ALLOW"
  DETAIL=""
  # Match write indicators against the extracted command string (not the raw
  # JSON): in JSON a leading `touch`/`cp`/… is preceded by a `"` quote, which
  # is not a shell word boundary, so matching the raw payload misses them.
  WRITE_IND='(>|(^|[;&|`( ])(tee|cp|mv|touch|rsync|truncate|dd|install|ln)( |$)|sed[^;|&]* -i)'

  if printf '%s' "$FLAT" | grep -q '"command"'; then
    # Bash-style payload — extract the command value.
    CMD="$(printf '%s' "$FLAT" \
      | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\(.*\)".*/\1/p')"
    if printf '%s' "$CMD" | grep -q '_Registry/\.\(riddler-passed\|vicki-passed\|vicki-bounced\)' \
       && printf '%s' "$CMD" | grep -Eq "$WRITE_IND"; then
      DECISION="BLOCK"
      DETAIL="gate markers are armed only by /riddler and /vale (Write tool) and disarmed with rm — Bash must not create or modify them"
    elif printf '%s' "$CMD" | grep -iq '\(artifacts/\|-essay\|-post\|-thread\)' \
       && printf '%s' "$CMD" | grep -Eq "$WRITE_IND"; then
      DECISION="GATE"
    fi
  elif [ -z "$FILE_PATH" ]; then
    if printf '%s' "$FLAT" | grep -q '"tool_name"[[:space:]]*:[[:space:]]*"\(Write\|Edit\|MultiEdit\|NotebookEdit\)"'; then
      DECISION="BLOCK"
      DETAIL="write-tool payload missing file_path — failing closed"
    fi
  elif printf '%s' "$FILE_PATH" | grep -q '\.\.'; then
    # Cannot canonicalize safely without python3 — fail closed.
    DECISION="GATE"
    DETAIL="${FILE_PATH##*/}"
  else
    # Squash /./ segments and duplicate slashes, lowercase for the dir match.
    NORM="$(printf '%s' "$FILE_PATH" | sed 's#/\./#/#g; s#//*#/#g')"
    BASE="${NORM##*/}"
    NORM_L="$(printf '%s' "$NORM" | tr '[:upper:]' '[:lower:]')"
    ROOT_L="$(printf '%s' "$ROOT" | tr '[:upper:]' '[:lower:]')"
    case "$NORM_L" in
      "$ROOT_L"/artifacts/*|artifacts/*) DECISION="GATE"; DETAIL="$BASE" ;;
      *)
        case "$BASE" in
          *-essay*|*-post*|*-thread*) DECISION="GATE"; DETAIL="$BASE" ;;
        esac
        ;;
    esac
  fi
fi

case "$DECISION" in
  ALLOW)
    exit 0
    ;;
  BLOCK)
    echo "PUBLISH GATE BLOCKED: ${DETAIL:-call blocked by publish gate}" >&2
    exit 2
    ;;
  GATE)
    ;;
  *)
    echo "PUBLISH GATE ERROR: unknown gate decision '${DECISION}' — failing closed." >&2
    exit 2
    ;;
esac

TARGET_BASE="$DETAIL"

# ---------------------------------------------------------------------------
# Marker checks: freshness (mtime within TTL) + content validity.
# ---------------------------------------------------------------------------

marker_status() {
  # $1 = marker path, $2 = target basename ("" = skip file binding)
  # Prints: missing | expired | empty | no-pass-verdict | file-mismatch | ok
  local marker="$1" target_base="$2"

  if [ ! -f "$marker" ]; then
    echo "missing"
    return
  fi

  # Freshness via find -mmin (portable GNU/BSD, works without python3).
  # A find failure counts as expired — never as fresh.
  local ttl_min=$(( (TTL_SECONDS + 59) / 60 ))
  local stale
  if ! stale="$(find "$marker" -mmin +"$ttl_min" 2>/dev/null)"; then
    echo "expired"
    return
  fi
  if [ -n "$stale" ]; then
    echo "expired"
    return
  fi

  # Content validity per _Registry/reviewer-verdict-schema.md.
  if [ ! -s "$marker" ]; then
    echo "empty"
    return
  fi
  if ! grep -Eq '^Verdict:[[:space:]]*(PASS|CONDITIONAL)([[:space:]]|$)' "$marker"; then
    echo "no-pass-verdict"
    return
  fi
  if [ -n "$target_base" ]; then
    local file_line reviewed_base
    file_line="$(sed -n 's/^File:[[:space:]]*//p' "$marker" | sed -n '1p')"
    reviewed_base="$(printf '%s' "${file_line##*/}" | sed 's/[[:space:]]*$//')"
    if [ "$reviewed_base" != "$target_base" ]; then
      echo "file-mismatch (marker reviewed: ${reviewed_base:-nothing})"
      return
    fi
  fi

  echo "ok"
}

RIDDLER_STATUS="$(marker_status "$ROOT/_Registry/.riddler-passed" "$TARGET_BASE")"
VALE_STATUS="$(marker_status "$ROOT/_Registry/.vicki-passed" "$TARGET_BASE")"

if [ "$RIDDLER_STATUS" != "ok" ] || [ "$VALE_STATUS" != "ok" ]; then
  echo "PUBLISH GATE BLOCKED: this write requires both gate markers present, fresh (TTL ${TTL_SECONDS}s), and valid for this artifact." >&2
  echo "  riddler: $RIDDLER_STATUS   vale: $VALE_STATUS" >&2
  echo "Run /riddler and /vale on the artifact (via Workflows/gate-dispatch.md). Both must PASS, and the staged filename must match the reviewed filename." >&2
  exit 2
fi

exit 0
