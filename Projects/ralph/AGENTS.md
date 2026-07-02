# Ralph AGENTS.md — Patterns discovered per iteration
**Current project:** RegEval (Evals/regeval/)

Ralph writes patterns here when a story resolves (DONE or BLOCKED).
Patterns feed future story prompts and help the loop avoid repeating mistakes.

**Format:** `## <date> — <pattern-slug>`

---

## 2026-05-23 — initial-setup

**Source:** Initial design
**Pattern:** Ralph is the outer build loop. `/regeval-run` is the inner experiment loop.
- Ralph drives bootstrap stories (gold dataset, scaffold creation) via `prd.json`
- Once REV-003 completes (first experiment), `/regeval-run` takes over for continuous experiment cycling
- Ralph resumes for new scaffold variant stories (REV-004, REV-006, REV-007)

**Sizing rule:** If a story takes > 1 context window, it ships BLOCKED. Break it before re-running.

**Gate discipline:** Quality gates are checked AFTER Claude Code exits. A story is only marked `done` when all gates pass — not when Claude Code says it's done.

**Human-in-the-loop triggers (immutable):**
1. `blocked` after 3 consecutive failures → resize story
2. Eval runner gate fails → check harness, not story
3. `agent_hint` mentions essay/post/thread/demo → Riddler + Vale FIRST
4. Git commit prompt → always pauses, never auto-pushes
5. Day 60 date reached → Bruce Wayne kill/continue decision
6. Story size = `large` → break before running

---

<!-- Ralph appends new patterns below as the loop runs -->

## 2026-05-23 — pre-flight-audit-fixes

**Source:** Independent audit before first real run (24 findings, 3 blockers).

**Patterns codified into the loop:**

1. **Commit gate must be wired, not just defined.** `git_commit_with_approval()` existed but was never called — Ralph mutated `prd.json` in place without committing. Lesson: every HITL gate function needs a call site review. Now invoked after `mark_done`, with narrow staging (Ralph-owned paths + `Evals/regeval/` only — never blanket `git add .`).

2. **Failure counters must be session-scoped.** Original `grep -c "FAIL:$story_id"` counted historical failures across all time. A story that failed 3× last week would instantly block today. Fix: stamp every `progress.txt` entry with `SESSION_ID` (timestamp) and grep within session only. Historical FAILs remain as audit trail; they don't block retries.

3. **Orphaned `in-progress` stories happen.** Status is flipped to `in-progress` before Claude runs; if Claude crashes, status is stuck. By definition only one story can be in-progress, so any `in-progress` found at session start is an orphan. `reset_stale_in_progress` runs first thing in `main()` and resets them to `pending`.

4. **Timeout the model invocation.** A hung `claude` session would hang Ralph indefinitely. Wrap in `timeout 30m` (or `gtimeout` from coreutils on macOS). Exit code 124 = timeout = treat as story failure.

5. **Gate definitions must match acceptance criteria.** REV-006 declared three files in `acceptance` but only checked one in `gates`. Whenever acceptance lists multiple artifacts, gates must enumerate all of them.

6. **Story dependencies must follow agent_hint logic.** REV-006 said "vary from current champion after REV-005" but depended on REV-003. The dependency graph must match the narrative.

**Deferred for next pass:**
- `Tasks/active.md` sync (single source of truth)
- `_Registry/` registration of Ralph for discoverability
- Riddler/Vale verdict file checking (currently the loop just exits and tells the human to run them)
- Stronger gates on experiment stories — check actual κ values, not just row counts
- Webhook notifications on loop completion

## Related

[[Projects/ralph/brief]] · [[Evals/regeval/regeval-suite]] · [[Evals/regeval/runner]] · [[Evals/regeval/experiments/log]] · [[Agents/Gotham/Computer/lucius-fox]]
