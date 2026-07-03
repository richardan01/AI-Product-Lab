# AI Product Lab — Gemini CLI Entry Point

This file is the entry point for **Gemini CLI**. The lab is harness-neutral — Claude Code reads `CLAUDE.md` and Gemini CLI reads this file. Both route to the same configuration surface and the same workflows.

## Configuration surface

- **`CLAUDE.md`** — user identity, persona, tone, routing, cadence, privacy boundaries, quality gates. Filename is historical; the contents apply to every harness. Read this on session start and respect what's there.
- **`GOALS.md`** — strategic outcomes and metrics.
- **`Tasks/active.md`** — current sprint focus.
- **`Knowledge/`** — durable reference context (stakeholder profiles under `Knowledge/People/` are gitignored/private).
- **`Projects/`** — per-project briefs and artifacts.
- **`Workflows/`** — repeatable interactive workflows.
- **`Templates/`** — document templates.
- **`Evals/`** — eval suites, run log, severity taxonomy, freshness sentinels. See `AGENTIC-EVAL-FRAMEWORK.md` for the loop design.

## Onboarding mode

When the user says `Computer, onboard me into this OS`, `set up this template`, or similar:

1. Run `Workflows/interactive-onboarding.md` phase by phase.
2. Ask the user — never invent — for identity, purpose, persona, cadence, current tasks, goals, stakeholders, and privacy boundaries.
3. Confirm each phase's read-back before moving on. Do not batch-propose tasks or stakeholders.
4. Show the final summary in full before asking for write approval.
5. Write files one at a time, asking explicitly per file. Polite acknowledgements ("ok", "sounds good") do not count as approval — require an explicit "yes" per file.
6. On re-run, re-confirm persona / tone / quality gates even if previously set.

## Operating contract (after onboarding)

Once `CLAUDE.md` is filled, treat it as the source of truth for how to respond — persona, tone, pushback level, review style, decision style, privacy boundaries. The principles, routing rules, quality gates, and DO-NOT list there apply regardless of harness.

## DO NOT

- Commit, push, or delete files without explicit approval.
- Write setup files during onboarding before the user confirms the summary.
- Replace placeholders (`[YOUR_NAME]`, `[YOUR_COMPANY]`, etc.) with invented values — ask the user.
- Create new top-level folders — extend existing structure.
- Store credentials or sensitive customer/company data in the repo. Sensitive people/company facts require explicit approval; keep private context in a private fork.
- Ship any public artifact without the Riddler + Vale reviewer gates (`Workflows/gate-dispatch.md`).

## Trigger phrases

- `Computer, onboard me into this OS` → `Workflows/interactive-onboarding.md`
- `Computer, what should I focus on today?` → daily brief workflow
- `/today`, `/eod`, `/peer-review`, `/prd-readiness`, `/go-nogo`, `/eval-review`, `/build-review`, `/test-plan` → corresponding skill or workflow under `Workflows/` or `.claude/skills/`.

## Core daily loop

- `/today` — morning brief from `Tasks/active.md` + `GOALS.md`.
- `/eod` — end-of-day update to `Tasks/active.md`, follow-ups, and current context.
- `/weekly-update` and `/retro` — close the week.

Stale task files weaken the OS. Running `/eod` daily is the highest-leverage habit.

Full skill catalog: `.claude/skills/`.
