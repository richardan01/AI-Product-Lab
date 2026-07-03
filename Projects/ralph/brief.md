# Project Brief: Ralph — RegEval autonomous build loop

**Owner:** [Your Name] (Lucius Fox, build lead)
**Status:** Active — bootstrap phase complete (REV-001/002/003 done)
**Started:** 2026-05-23
**Target:** Drive RegEval to MVP for the Day 60 gate (2026-06-30)
**Last updated:** 2026-05-28

---

## What this is

Ralph is the **outer build loop** that drives the RegEval flagship. It reads stories from `prd.json`, invokes Claude Code per story, checks quality gates after exit, and only marks a story `done` when all gates pass. `ralph.sh` is the loop; `/regeval-run` is the inner experiment loop that takes over once the first experiment (REV-003) completes.

This is build infrastructure for Q3 thesis Pillar 1 (RegEval), not a standalone product. It lives in `Projects/` because it carries its own PRD, progress log, and discovered-pattern memory.

---

## Why it exists

RegEval has a fixed weekly build budget and a hard Day 60 invalidation gate. Hand-driving every build story burns that budget on orchestration overhead. Ralph automates the bootstrap and scaffold-variant stories so the scarce human hours go to judgment calls (labelling, gate review, kill/continue) rather than loop-running.

---

## How it works

- **`prd.json`** — 7 stories (REV-001 … REV-007). Bootstrap: REV-001 gold dataset → REV-002 baseline scaffold → REV-003 first experiment. Then scaffold variants REV-004/006/007.
- **`ralph.sh`** — the loop: reset stale `in-progress`, pick next pending story, invoke `claude` under `timeout 30m`, check gates after exit, mark done + commit (with approval) or fail.
- **`progress.txt`** — append-only run log, one entry per run, session-stamped. Never edited retroactively.
- **`AGENTS.md`** — patterns Ralph discovers per resolved story; feeds future prompts so the loop avoids repeating mistakes.

---

## Human-in-the-loop triggers (immutable)

1. `blocked` after 3 consecutive (session-scoped) failures → resize story
2. Eval runner gate fails → check the harness, not the story
3. `agent_hint` mentions essay/post/thread/demo → Riddler + Vale FIRST
4. Git commit prompt → always pauses, never auto-pushes
5. Day 60 date reached (2026-06-30) → Bruce Wayne kill/continue decision
6. Story size = `large` → break before running

---

## Current state

| Story | Status | Note |
|-------|--------|------|
| REV-001 | ✅ Done (2026-05-23) | Gold dataset — 30 labelled items |
| REV-002 | ✅ Done (2026-05-23) | Day-1 baseline scaffold |
| REV-003 | ✅ Done (2026-05-23) | First experiment — κ baseline established |
| REV-004/006/007 | Pending | Scaffold variants — next Ralph stories |

---

## Scope

### In scope
- Outer build-loop orchestration for RegEval bootstrap + scaffold-variant stories
- Quality-gate enforcement after each Claude Code exit
- Session-scoped failure counting, orphan recovery, model-invocation timeout
- Narrow, approval-gated git commits (Ralph-owned paths + `Evals/regeval/` only)

### Out of scope
- The inner experiment loop (`/regeval-run` owns continuous experiment cycling)
- Publishing artifacts (essay/demo) — those route through Riddler + Vale gates manually
- Auto-push or blanket `git add .`

### Deferred (next pass)
- `Tasks/active.md` sync as single source of truth
- `_Registry/` registration of Ralph for discoverability
- Riddler/Vale verdict-file checking inside the loop
- Stronger experiment gates (actual κ values, not just row counts)
- Webhook notifications on loop completion

---

## Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Story exceeds one context window | Medium | Medium | Sizing rule: `large` ships BLOCKED; break before re-running |
| Loop hangs on a stuck `claude` session | Low | High | `timeout 30m` (gtimeout on macOS); exit 124 = story failure |
| Gates pass on incomplete artifacts | Medium | High | Gates must enumerate every artifact in `acceptance` |
| Day 60 gate slips | Medium | High | HITL trigger 5 forces a Bruce Wayne kill/continue decision on 2026-06-30 |

---

## Links & resources

- `Evals/regeval/` — the flagship build target
- `prd.json` — story backlog (Ralph-owned)
- `progress.txt` — append-only run log
- `AGENTS.md` — discovered build patterns
- `Agents/Gotham/thesis-q3-2026.md` — Pillar 1 context and the Day 60 invalidation gate
