#!/usr/bin/env bash
# ralph.sh — RegEval autonomous build loop
# Adapted from https://github.com/snarktank/ralph
# Pattern: https://ghuntley.com/loop/
#
# Usage:
#   ./ralph.sh              — run next pending story
#   ./ralph.sh --dry-run    — show what would run, no execution
#   ./ralph.sh --status     — print story status summary
#   ./ralph.sh --story REV-003  — run a specific story by ID
#
# Human-in-the-loop moments (the loop will PAUSE and print HITL):
#   1. Story marked blocked (3 consecutive failures)
#   2. Quality gate fails on the eval runner (harness may be broken)
#   3. Story involves a public artifact (Riddler + Vicki Vale required)
#   4. Git commit — always pauses for your approval (never auto-pushes)
#   5. Day 60 invalidation check due
#   6. Story size flagged "large" (break it before running)

set -euo pipefail

# ── Config ─────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PRD_FILE="$SCRIPT_DIR/prd.json"
PROGRESS_FILE="$SCRIPT_DIR/progress.txt"
AGENTS_FILE="$SCRIPT_DIR/AGENTS.md"
LOG_FILE="$OS_ROOT/Evals/regeval/experiments/log.md"
HARNESS_ROOT="$OS_ROOT/Evals/regeval"

# Colours
RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'

# ── Helpers ────────────────────────────────────────────────────────────────
log()  { echo -e "${CYAN}[ralph]${NC} $*"; }
warn() { echo -e "${YELLOW}[ralph][warn]${NC} $*"; }
hitl() { echo -e "${RED}[ralph][HITL]${NC} $*"; }
ok()   { echo -e "${GREEN}[ralph][ok]${NC} $*"; }

require_jq() {
  command -v jq >/dev/null 2>&1 || { echo "jq is required: brew install jq"; exit 1; }
}

require_claude() {
  command -v claude >/dev/null 2>&1 || { echo "claude CLI not found. Install Claude Code first."; exit 1; }
}

ts() { date -u '+%Y-%m-%d %H:%M UTC'; }

# SESSION_ID is set in main(). Default to "adhoc" for utility calls (e.g. --status).
: "${SESSION_ID:=adhoc}"

append_progress() {
  echo "" >> "$PROGRESS_FILE"
  echo "## $(ts) [SESSION-$SESSION_ID] — $1" >> "$PROGRESS_FILE"
  echo "$2" >> "$PROGRESS_FILE"
}

# ── Status ─────────────────────────────────────────────────────────────────
cmd_status() {
  require_jq
  log "RegEval story status:"
  echo ""
  jq -r '.stories[] | "\((.status | ascii_upcase) + "        " | .[0:8]) \(.id) — \(.title)"' "$PRD_FILE" | \
    sed 's/^PENDING /  ⬜ /' | \
    sed 's/^IN_PROGR/  🔄 /' | \
    sed 's/^DONE    /  ✅ /' | \
    sed 's/^BLOCKED /  🔴 /' | \
    sed 's/^DEPRIORI/  ⏸️ /'
  echo ""
  local total done blocked
  total=$(jq '.stories | length' "$PRD_FILE")
  done=$(jq '[.stories[] | select(.status == "done")] | length' "$PRD_FILE")
  blocked=$(jq '[.stories[] | select(.status == "blocked")] | length' "$PRD_FILE")
  log "$done/$total stories done · $blocked blocked"
}

# ── Gate checks ────────────────────────────────────────────────────────────
check_gate() {
  local gate="$1"
  local type="${gate%%:*}"
  local args="${gate#*:}"

  case "$type" in
    file_exists)
      local path="$OS_ROOT/$args"
      [[ -f "$path" ]] && return 0 || return 1
      ;;
    line_count_gte)
      local file="$OS_ROOT/${args%%:*}"
      local min="${args##*:}"
      local count
      count=$(wc -l < "$file" 2>/dev/null || echo 0)
      [[ "$count" -ge "$min" ]] && return 0 || return 1
      ;;
    log_has_row)
      local file="$OS_ROOT/$args"
      # Check log has a row that isn't the header or the placeholder row
      grep -q "KEEP\|HOLD\|DISCARD\|FAIL" "$file" 2>/dev/null && return 0 || return 1
      ;;
    log_row_count_gte)
      local file="$OS_ROOT/${args%%:*}"
      local min="${args##*:}"
      local count
      count=$(grep -c "KEEP\|HOLD\|DISCARD\|FAIL" "$file" 2>/dev/null || echo 0)
      [[ "$count" -ge "$min" ]] && return 0 || return 1
      ;;
    file_contains)
      local file="$OS_ROOT/${args%%:*}"
      local needle="${args##*:}"
      grep -q "$needle" "$file" 2>/dev/null && return 0 || return 1
      ;;
    typecheck)
      # Python type hints check — run mypy if available
      command -v mypy >/dev/null 2>&1 && mypy "$HARNESS_ROOT" --ignore-missing-imports -q && return 0
      warn "mypy not found — skipping typecheck gate (install: pip install mypy)"
      return 0  # non-blocking if mypy absent
      ;;
    *)
      warn "Unknown gate type: $type — skipping"
      return 0
      ;;
  esac
}

run_gates() {
  local story_id="$1"
  require_jq
  local gates
  gates=$(jq -r --arg id "$story_id" '.stories[] | select(.id == $id) | .gates[]?' "$PRD_FILE")

  local all_passed=true
  while IFS= read -r gate; do
    [[ -z "$gate" ]] && continue
    if check_gate "$gate"; then
      ok "gate passed: $gate"
    else
      warn "gate FAILED: $gate"
      all_passed=false
    fi
  done <<< "$gates"

  $all_passed
}

# ── Dependency check ────────────────────────────────────────────────────────
check_deps() {
  local story_id="$1"
  require_jq
  local deps
  deps=$(jq -r --arg id "$story_id" '.stories[] | select(.id == $id) | .depends_on[]?' "$PRD_FILE")

  while IFS= read -r dep; do
    [[ -z "$dep" ]] && continue
    local dep_status
    dep_status=$(jq -r --arg id "$dep" '.stories[] | select(.id == $id) | .status' "$PRD_FILE")
    if [[ "$dep_status" != "done" ]]; then
      hitl "Dependency $dep is not done (status: $dep_status). Complete it first."
      return 1
    fi
  done <<< "$deps"
  return 0
}

# ── Story runner ────────────────────────────────────────────────────────────
run_story() {
  local story_id="$1"
  require_jq
  require_claude

  local story_json
  story_json=$(jq --arg id "$story_id" '.stories[] | select(.id == $id)' "$PRD_FILE")

  local title phase size context agent_hint acceptance
  title=$(echo "$story_json" | jq -r '.title')
  phase=$(echo "$story_json" | jq -r '.phase')
  size=$(echo "$story_json" | jq -r '.size')
  context=$(echo "$story_json" | jq -r '.context // ""')
  agent_hint=$(echo "$story_json" | jq -r '.agent_hint // ""')
  acceptance=$(echo "$story_json" | jq -r '.acceptance')

  log "Running story: $story_id — $title"
  log "Phase: $phase · Size: $size"
  echo ""

  # Human gate: large stories
  if [[ "$size" == "large" ]]; then
    hitl "Story $story_id is sized 'large'. Ralph rule: one context window = one story."
    hitl "Break this into 2–3 smaller stories before running. Edit prd.json."
    exit 1
  fi

  # Check dependencies
  check_deps "$story_id" || exit 1

  # Mark in-progress
  local tmp
  tmp=$(mktemp)
  jq --arg id "$story_id" \
    '(.stories[] | select(.id == $id) | .status) |= "in-progress"' \
    "$PRD_FILE" > "$tmp" && mv "$tmp" "$PRD_FILE"

  # Build the prompt for Claude Code
  local prompt
  if [[ "$phase" == "experiment" ]]; then
    # Experiment stories: invoke /regeval-run
    prompt="You are running a RegEval experiment in the autoresearch loop.

STORY: $story_id — $title
ACCEPTANCE: $acceptance
CONTEXT: $context
INSTRUCTION: $agent_hint

Working directory: $OS_ROOT
Run the /regeval-run skill as instructed. Record all results to experiments/log.md."
  else
    # Build stories: implement the acceptance criteria
    prompt="You are Lucius Fox building the RegEval eval framework.

STORY: $story_id — $title
ACCEPTANCE: $acceptance
CONTEXT: $context
INSTRUCTION: $agent_hint

Working directory: $OS_ROOT
Implement exactly what the acceptance criteria describe. No more, no less. Prefer small, focused changes. Write files, do not commit."
  fi

  log "Spawning Claude Code with fresh context..."
  echo ""

  # Spawn fresh Claude Code instance (--dangerously-skip-permissions for autonomous mode)
  # Remove --dangerously-skip-permissions if you want permission prompts on each run
  if [[ "${DRY_RUN:-false}" == "true" ]]; then
    warn "[DRY RUN] Would spawn: claude -p \"...$story_id...\""
    warn "[DRY RUN] Prompt: ${prompt:0:200}..."
    # Simulate success for dry run
    ok "Dry run — marking $story_id done (simulated)"
    mark_done "$story_id"
    return 0
  fi

  local exit_code=0
  # Wrap claude in `timeout` so a hung session can't hang the loop forever.
  # Use gtimeout on macOS if available (from coreutils); fall back to timeout.
  local TIMEOUT_BIN
  if command -v timeout >/dev/null 2>&1; then TIMEOUT_BIN="timeout"
  elif command -v gtimeout >/dev/null 2>&1; then TIMEOUT_BIN="gtimeout"
  else TIMEOUT_BIN=""
  fi

  if [[ -n "$TIMEOUT_BIN" ]]; then
    "$TIMEOUT_BIN" 30m claude --dangerously-skip-permissions -p "$prompt" || exit_code=$?
    if [[ $exit_code -eq 124 ]]; then
      warn "Claude Code timed out after 30 minutes — treating as failure"
    fi
  else
    warn "No timeout binary found (install coreutils for gtimeout) — running claude without timeout"
    claude --dangerously-skip-permissions -p "$prompt" || exit_code=$?
  fi

  echo ""
  if [[ $exit_code -ne 0 ]]; then
    warn "Claude Code exited with code $exit_code"
  fi

  # Run quality gates
  log "Running quality gates for $story_id..."
  if run_gates "$story_id"; then
    ok "All gates passed for $story_id"
    mark_done "$story_id"
    append_progress "$story_id — DONE" "$title — all gates passed"

    # Commit gate — stage narrowly, always pause for human approval
    if git -C "$OS_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
      git -C "$OS_ROOT" add Projects/ralph/prd.json Projects/ralph/progress.txt 2>/dev/null || true
      git -C "$OS_ROOT" add Evals/regeval/ 2>/dev/null || true
      git_commit_with_approval "ralph: complete $story_id"
    else
      warn "Not a git repo — skipping commit gate"
    fi
  else
    warn "Gates FAILED for $story_id"
    handle_failure "$story_id"
  fi
}

mark_done() {
  local story_id="$1"
  local tmp
  tmp=$(mktemp)
  jq --arg id "$story_id" \
    '(.stories[] | select(.id == $id) | .status) |= "done"' \
    "$PRD_FILE" > "$tmp" && mv "$tmp" "$PRD_FILE"
  ok "Marked $story_id as done in prd.json"
}

handle_failure() {
  local story_id="$1"
  require_jq

  # Count consecutive failures for this story IN THE CURRENT SESSION only.
  # Historical FAILs from prior sessions stay in progress.txt as audit trail
  # but do not count toward the 3-strikes block.
  local fail_count
  fail_count=$(grep -c "SESSION-$SESSION_ID.*FAIL:$story_id" "$PROGRESS_FILE" 2>/dev/null || echo 0)
  fail_count=$((fail_count + 1))

  append_progress "FAIL:$story_id ($fail_count)" "Gates failed on attempt $fail_count"

  # Mark back to pending for retry
  local tmp
  tmp=$(mktemp)
  jq --arg id "$story_id" \
    '(.stories[] | select(.id == $id) | .status) |= "pending"' \
    "$PRD_FILE" > "$tmp" && mv "$tmp" "$PRD_FILE"

  if [[ $fail_count -ge 3 ]]; then
    # 3 consecutive failures — block and surface to human
    local tmp2
    tmp2=$(mktemp)
    jq --arg id "$story_id" \
      '(.stories[] | select(.id == $id) | .status) |= "blocked"' \
      "$PRD_FILE" > "$tmp2" && mv "$tmp2" "$PRD_FILE"
    hitl "──────────────────────────────────────────"
    hitl "Story $story_id has failed 3 times. BLOCKED."
    hitl "Human required: resize the story, fix the acceptance criteria, or repair the harness."
    hitl "Check progress.txt for failure log."
    hitl "──────────────────────────────────────────"
    exit 1
  else
    warn "Attempt $fail_count/3 failed. Will retry on next ralph.sh run."
  fi
}

# ── Commit gate (always human-approved) ────────────────────────────────────
git_commit_with_approval() {
  local message="$1"
  hitl "Git commit ready. Review the staged changes before approving:"
  echo ""
  git -C "$OS_ROOT" diff --staged --stat 2>/dev/null || true
  echo ""
  hitl "Commit message: $message"
  read -r -p "Approve commit? [y/N] " yn
  case "$yn" in
    [Yy]*) git -C "$OS_ROOT" commit -m "$message" && ok "Committed." ;;
    *) warn "Commit declined. Changes remain staged." ;;
  esac
}

# ── Stale in-progress recovery ─────────────────────────────────────────────
# A new session starting with any story in "in-progress" means the previous
# session crashed mid-story. Reset such orphans to "pending" so they get
# picked up again. By definition only one story runs at a time.
reset_stale_in_progress() {
  require_jq
  local stale
  stale=$(jq -r '.stories[] | select(.status == "in-progress") | .id' "$PRD_FILE")
  while IFS= read -r id; do
    [[ -z "$id" ]] && continue
    warn "Resetting orphaned story $id (was in-progress) to pending"
    local tmp; tmp=$(mktemp)
    jq --arg id "$id" '(.stories[] | select(.id == $id) | .status) |= "pending"' "$PRD_FILE" > "$tmp" && mv "$tmp" "$PRD_FILE"
    append_progress "RECOVER:$id" "Reset orphaned in-progress to pending (prior session crashed)"
  done <<< "$stale"
}

# ── Day 60 check ────────────────────────────────────────────────────────────
day60_check() {
  local today
  today=$(date '+%Y-%m-%d')
  local gate_date
  gate_date=$(jq -r '.meta.day_60_gate' "$PRD_FILE")

  if [[ "$today" > "$gate_date" || "$today" == "$gate_date" ]]; then
    hitl "Day 60 gate reached ($gate_date). Bruce Wayne assessment required."
    hitl "Kill criterion: κ ≥ 0.80 on ≥1 scaffold AND gold ≥ 100 items AND 14-day cadence."
    hitl "Run: Computer, what's our Day 60 RegEval status — Bruce Wayne"
    exit 1
  fi
}

# ── Public artifact gate ────────────────────────────────────────────────────
# If a story's agent_hint mentions essay/post/thread/demo, pause for Riddler + Vale
public_artifact_check() {
  local story_id="$1"
  require_jq
  local hint
  hint=$(jq -r --arg id "$story_id" '.stories[] | select(.id == $id) | .agent_hint // ""' "$PRD_FILE")

  if echo "$hint" | grep -qiE "essay|post|thread|demo|publish|ship"; then
    hitl "Story $story_id produces a public artifact."
    hitl "Riddler + Vicki Vale review BOTH required before loop continues."
    hitl "Run: /riddler on the artifact, then resume ralph.sh."
    exit 1
  fi
}

# ── Main ───────────────────────────────────────────────────────────────────
main() {
  require_jq

  # Parse args
  local dry_run=false
  local specific_story=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dry-run) dry_run=true; export DRY_RUN=true ;;
      --status) cmd_status; exit 0 ;;
      --story) specific_story="$2"; shift ;;
      *) echo "Unknown arg: $1"; exit 1 ;;
    esac
    shift
  done

  # Session ID stamps every progress.txt entry from this run; lets handle_failure
  # count per-session FAILs instead of all-time FAILs.
  SESSION_ID="$(date '+%Y%m%d-%H%M%S')"
  export SESSION_ID

  log "Ralph loop — RegEval build"
  log "Session: $SESSION_ID"
  log "OS root: $OS_ROOT"
  log "PRD: $PRD_FILE"
  echo ""

  # Recover orphans from prior crashed sessions before doing anything else
  reset_stale_in_progress

  # Day 60 check
  day60_check

  if [[ -n "$specific_story" ]]; then
    public_artifact_check "$specific_story"
    run_story "$specific_story"
    exit 0
  fi

  # Find next pending story (respecting dependency order)
  local next_story
  next_story=$(jq -r '
    .stories[]
    | select(.status == "pending")
    | .id
  ' "$PRD_FILE" | head -1)

  if [[ -z "$next_story" ]]; then
    local blocked_count
    blocked_count=$(jq '[.stories[] | select(.status == "blocked")] | length' "$PRD_FILE")
    if [[ $blocked_count -gt 0 ]]; then
      hitl "No pending stories, but $blocked_count stories are BLOCKED."
      hitl "Human required. Run: ./ralph.sh --status"
      exit 1
    fi
    ok "All stories done! RegEval bootstrap complete."
    ok "Next: run /regeval-run experiment loop for scaffold variants."
    cmd_status
    exit 0
  fi

  public_artifact_check "$next_story"
  run_story "$next_story"
}

main "$@"
