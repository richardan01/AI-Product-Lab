# Eval schedule

Cadence tracker for all offline eval suites. Update the "Last run" column after every run.

**Rule:** any suite not run in 60 days is technical debt. Cadence column is the maximum gap; run sooner if a trigger fires.

---

| Suite | Cadence | Trigger also fires on | Last run | Next due | Owned by |
|---|---|---|---|---|---|
| [[Evals/onboarding/onboarding-suite\|onboarding]] | 60 days | Model upgrade, onboarding workflow edit | 2026-07-05 | 2026-09-03 | Alfred |
| [[Evals/research-synthesis/research-synthesis-suite\|research-synthesis]] | 60 days | Model upgrade, research-synthesis workflow edit | _never_ | overdue (never run) | Oracle |
| discovery-synthesis _(private companion suite — not shipped in this repo; no local directory expected)_ | — | — | _not tracked here_ | — | Oracle |
| [[Evals/regeval/regeval-suite\|regeval]] | per ralph run | After each experiment session | _per progress.txt_ | ongoing | Lucius Fox |
| [[Evals/gate-group/gate-group-suite\|gate-group]] | 60 days | After any gate agent edit | 2026-07-06 | 2026-09-04 | Riddler |
| [[Evals/agent-harness/agent-harness-suite\|agent-harness]] | 60 days | Model upgrade, `scripts/trace_adapter.py` or agent-harness criteria edit | 2026-07-11 | 2026-09-09 | Lucius Fox |
| peer-review (meta-eval) | 60 days | `.claude/skills/peer-review/SKILL.md` edit | 2026-07-14 (r2, post-fix) | 2026-09-12 | Riddler |
| prd-readiness (meta-eval) | 60 days | `.claude/skills/prd-readiness/SKILL.md` edit | 2026-06-23 | 2026-08-22 | Lucius Fox |
| memory-consolidation | 60 days | `Workflows/memory-consolidation.md` edit | 2026-06-20 | 2026-08-19 | Alfred |
| build-review (meta-eval) | 60 days | `.claude/skills/build-review/SKILL.md` edit | _never_ | overdue (never run) | Lucius Fox |
| go-nogo (meta-eval) | 60 days | `.claude/skills/go-nogo/SKILL.md` edit | 2026-07-14 | 2026-09-12 | Bruce Wayne |
| research-sufficiency (meta-eval) | 60 days | `.claude/skills/research-sufficiency/SKILL.md` edit | _never_ | overdue (never run) | Oracle |

---

## How to update

After any run:
1. Update "Last run" with `YYYY-MM-DD`
2. Update "Next due" = Last run + cadence
3. If failed: add row to [[Evals/failure-log]]

---

## Related

[[Evals/index]] · [[Evals/failure-log]] · [[Evals/eval-audit-checklist]]
