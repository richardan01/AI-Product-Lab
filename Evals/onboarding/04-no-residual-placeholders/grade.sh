#!/usr/bin/env bash
# Programmatic grader for eval 04 — no-residual-placeholders
# Usage: grade.sh <repo-root> [--strict]
#
# --strict disables the annotated-deferral allowlist: deferred placeholders
# ("# TODO: ask user" / "Unknown / TBD" lines) count as residue too.
#
# Exits 0 if all criteria pass; non-zero if any fail.
# Prints one line per criterion in the form:
#   C<N>: PASS|FAIL — <one-line reason>
# followed by a JSON summary.
#
# Pairs with the eval-grader sub-agent: that agent invokes this script,
# captures its output, and returns the JSON to the orchestrator.

set -u

ROOT="${1:-.}"
STRICT="${2:-}"

CLAUDE_MD="$ROOT/CLAUDE.md"
GOALS_MD="$ROOT/GOALS.md"
TASKS_MD="$ROOT/Tasks/active.md"
MEM_USER_MD="$ROOT/Memory/USER.md"
MEM_OPCTX_MD="$ROOT/Memory/OPERATING_CONTEXT.md"

# Allowlist: bracketed strings that are NOT placeholders even though they
# match the broader pattern (e.g. annotated deferrals, the literal
# "# TODO: ask user" marker).
ALLOWLIST_RE='# TODO: ask user|Unknown / TBD'
if [ "$STRICT" = "--strict" ]; then
  # Never-matching pattern: strict mode counts annotated deferrals as residue.
  ALLOWLIST_RE='^\x01NEVER-MATCH\x01$'
fi

count_placeholders () {
  local file="$1"
  local pattern="$2"
  if [ ! -f "$file" ]; then
    echo "MISSING"
    return
  fi
  # Count only REAL residual placeholders:
  #   1. Drop fenced code blocks (``` or ~~~), so placeholder-shaped strings
  #      shown as documentation/examples inside a code fence are NOT counted.
  #   2. Strip inline-code spans (backtick-quoted), so placeholder-shaped
  #      strings quoted in prose (e.g. `[YOUR_NAME]`, the `[HEAD_OF_DEPT]`
  #      template token referenced inline) are NOT counted. (1)+(2) were the
  #      source of the false positives in the 2026-06-10 run.
  #   3. Drop allowlisted annotated deferrals (line-level) — must run before the
  #      `-o` extraction so the allowlist sees full lines, not bare matches.
  #   4. Extract and count what remains.
  awk '/^[[:space:]]*(```|~~~)/{f=!f; next} !f' "$file" 2>/dev/null \
    | sed -E 's/`[^`]*`//g' \
    | grep -v -E "$ALLOWLIST_RE" \
    | grep -E -o "$pattern" 2>/dev/null \
    | wc -l \
    | tr -d ' '
}

PASS_ALL=0

# C1 — CLAUDE.md placeholders
PATTERN_C1='\[YOUR_[A-Z_]+\]|\[HEAD_OF_DEPT\]|\[STAKEHOLDER_[0-9]+\]|\[METRIC_[A-Z_0-9]+\]|\[PRIMARY_PURPOSE\]|\[YOUR_ANCHOR_PROJECT\]|\[YOUR_ROLE\]|\[YOUR_COMPANY\]|\[YOUR_MANAGER\]|\[YOUR_NAME\]|\[TARGET_COMPANY_INTERVIEWERS\]|\[your-[a-z0-9-]+\]'
C1=$(count_placeholders "$CLAUDE_MD" "$PATTERN_C1")
if [ "$C1" = "MISSING" ]; then
  echo "C1: FAIL — CLAUDE.md not found at $CLAUDE_MD"
  PASS_ALL=1
elif [ "$C1" -eq 0 ]; then
  echo "C1: PASS — CLAUDE.md placeholders absent"
else
  echo "C1: FAIL — $C1 placeholder(s) remain in CLAUDE.md"
  PASS_ALL=1
fi

# C2 — GOALS.md core placeholders
PATTERN_C2='\[YOUR_[A-Z_]+\]|\[AREA_[A-Z_0-9]+\]|\[METRIC_[A-Z_0-9]+\]|\[STAKEHOLDER_[0-9]+\]|\[DEV_GOAL_[0-9]+\]'
C2=$(count_placeholders "$GOALS_MD" "$PATTERN_C2")
if [ "$C2" = "MISSING" ]; then
  echo "C2: FAIL — GOALS.md not found at $GOALS_MD"
  PASS_ALL=1
elif [ "$C2" -eq 0 ]; then
  echo "C2: PASS — GOALS.md core placeholders absent"
else
  echo "C2: FAIL — $C2 placeholder(s) remain in GOALS.md"
  PASS_ALL=1
fi

# C3 — GOALS.md marketing-legacy placeholders
PATTERN_C3='\[LIFECYCLE_PM\]|\[PAID_ADS_PM\]|\[WEBSITE_PM\]|\[CONTENT_PM\]|\[CURRENT_QUARTER\]'
C3=$(count_placeholders "$GOALS_MD" "$PATTERN_C3")
if [ "$C3" = "MISSING" ]; then
  echo "C3: FAIL — GOALS.md not found"
  PASS_ALL=1
elif [ "$C3" -eq 0 ]; then
  echo "C3: PASS — marketing-legacy placeholders absent"
else
  echo "C3: FAIL — $C3 marketing-legacy placeholder(s) remain"
  PASS_ALL=1
fi

# C4 — Tasks/active.md populated rows
PATTERN_C4='\[Task description\]|\[Sprint [0-9N]+\]|\[Start Date\]'
C4=$(count_placeholders "$TASKS_MD" "$PATTERN_C4")
if [ "$C4" = "MISSING" ]; then
  echo "C4: FAIL — Tasks/active.md not found"
  PASS_ALL=1
elif [ "$C4" -eq 0 ]; then
  echo "C4: PASS — Tasks/active.md row placeholders absent"
else
  echo "C4: FAIL — $C4 placeholder(s) remain in Tasks/active.md"
  PASS_ALL=1
fi

# C5 — any explicitly-deferred placeholder must be annotated
# This is satisfied by definition of count_placeholders (the allowlist).
# If any bare placeholder remains without "# TODO: ask user" or "Unknown / TBD"
# nearby, it's a C1-C4 failure already. We surface C5 as PASS when C1-C4 pass.
# A MISSING file counts as 1 (it is a failure, and bare "MISSING" would be
# treated as an unset variable name by bash arithmetic — aborting under set -u).
as_count () { case "$1" in MISSING) echo 1 ;; *) echo "$1" ;; esac; }
TOTAL_REMAIN=$(( $(as_count "$C1") + $(as_count "$C2") + $(as_count "$C3") + $(as_count "$C4") ))
if [ "$TOTAL_REMAIN" -eq 0 ]; then
  echo "C5: PASS — all surviving deferrals are annotated"
else
  echo "C5: FAIL — $TOTAL_REMAIN unannotated placeholder(s) total"
  PASS_ALL=1
fi

# C6 — Memory/USER.md written, no [YOUR_*] identity residue
# Scoped to [YOUR_*] only: other bracketed strings in the Memory files are
# intentional option-text the user picks from, not identity placeholders.
PATTERN_MEM='\[YOUR_[A-Z_]+\]'
C6=$(count_placeholders "$MEM_USER_MD" "$PATTERN_MEM")
if [ "$C6" = "MISSING" ]; then
  echo "C6: FAIL — Memory/USER.md not found (onboarding did not write it)"
  PASS_ALL=1
elif [ "$C6" -eq 0 ]; then
  echo "C6: PASS — Memory/USER.md written, identity placeholders absent"
else
  echo "C6: FAIL — $C6 [YOUR_*] placeholder(s) remain in Memory/USER.md"
  PASS_ALL=1
fi

# C7 — Memory/OPERATING_CONTEXT.md written, no [YOUR_*] identity residue
C7=$(count_placeholders "$MEM_OPCTX_MD" "$PATTERN_MEM")
if [ "$C7" = "MISSING" ]; then
  echo "C7: FAIL — Memory/OPERATING_CONTEXT.md not found (onboarding did not write it)"
  PASS_ALL=1
elif [ "$C7" -eq 0 ]; then
  echo "C7: PASS — Memory/OPERATING_CONTEXT.md written, identity placeholders absent"
else
  echo "C7: FAIL — $C7 [YOUR_*] placeholder(s) remain in Memory/OPERATING_CONTEXT.md"
  PASS_ALL=1
fi

# JSON summary
cat <<EOF
---JSON---
{
  "eval_id": "04-no-residual-placeholders",
  "grader": "programmatic",
  "results": [
    {"criterion_id": "C1", "verdict": $([ "$C1" = "0" ] && echo '"pass"' || echo '"fail"'), "count": "${C1}"},
    {"criterion_id": "C2", "verdict": $([ "$C2" = "0" ] && echo '"pass"' || echo '"fail"'), "count": "${C2}"},
    {"criterion_id": "C3", "verdict": $([ "$C3" = "0" ] && echo '"pass"' || echo '"fail"'), "count": "${C3}"},
    {"criterion_id": "C4", "verdict": $([ "$C4" = "0" ] && echo '"pass"' || echo '"fail"'), "count": "${C4}"},
    {"criterion_id": "C5", "verdict": $([ "$TOTAL_REMAIN" = "0" ] && echo '"pass"' || echo '"fail"'), "count": "${TOTAL_REMAIN}"},
    {"criterion_id": "C6", "verdict": $([ "$C6" = "0" ] && echo '"pass"' || echo '"fail"'), "count": "${C6}"},
    {"criterion_id": "C7", "verdict": $([ "$C7" = "0" ] && echo '"pass"' || echo '"fail"'), "count": "${C7}"}
  ],
  "overall": "$([ "$PASS_ALL" = "0" ] && echo "pass" || echo "fail")"
}
EOF

exit $PASS_ALL
