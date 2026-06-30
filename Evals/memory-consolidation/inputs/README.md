# Fixtures — memory-consolidation

A fixture is a dated source window plus a gold expectation.

Structure per fixture:
- `window/` — the in-range `*.jsonl` transcripts + a `git log --since` excerpt + relevant `Decisions/` and `Tasks/` files for `[LASTRUN → TODAY]`
- `gold.md` — the facts a correct consolidation **should** write, and a **should-NOT-write** list (traps: a plausible-but-unsourced fact; a fact that contradicts a `Knowledge/` canon page)

Build incrementally — gold sets grow over time, per the RegEval doctrine (`Evals/regeval/`). Planned fixtures:

| Fixture | Scenario | Stresses |
|---|---|---|
| `normal-day` | one ordinary session | baseline faithfulness (01) + freshness (05) |
| `heavy-day` | many long sessions (like 2026-06-18) | recall under volume (03) + completeness (05) | ✅ built: `2026-06-20-heavy-day/` (first measured run) |
| `conflicting-facts` | window contradicts a `Knowledge/` canon page | canonicality (04) + drift (01) |
| `empty-day` | no durable content | must still bump date (05); must invent nothing (02) |

To snapshot a real window as a fixture: copy the in-range `*.jsonl` + a `git log --since` excerpt into `window/`, then hand-author `gold.md`.
