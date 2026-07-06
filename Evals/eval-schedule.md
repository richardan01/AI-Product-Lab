# Eval schedule

Cadence tracker for all offline eval suites. Update the "Last run" column after every run.

**Rule:** any suite not run in 60 days is technical debt. Cadence column is the maximum gap; run sooner if a trigger fires.

---

| Suite | Cadence | Trigger also fires on | Last run | Next due | Owned by |
|---|---|---|---|---|---|
| [[Evals/onboarding/onboarding-suite\|onboarding]] | 60 days | Model upgrade, onboarding workflow edit | _never_ | 2026-07-28 | Alfred |
| [[Evals/research-synthesis/research-synthesis-suite\|research-synthesis]] | 60 days | Model upgrade, research-synthesis workflow edit | _never_ | 2026-07-28 | Oracle |
| [[Evals/discovery-synthesis/discovery-synthesis-suite\|discovery-synthesis]] | 60 days | Model upgrade, discovery workflow edit | _never_ | 2026-07-28 | Oracle |
| [[Evals/regeval/regeval-suite\|regeval]] | per ralph run | After each experiment session | _per progress.txt_ | ongoing | Lucius Fox |
| [[Evals/gate-group/gate-group-suite\|gate-group]] | 60 days | After any gate agent edit | 2026-07-06 | 2026-09-04 | Riddler |

---

## How to update

After any run:
1. Update "Last run" with `YYYY-MM-DD`
2. Update "Next due" = Last run + cadence
3. If failed: add row to [[Evals/failure-log]]

---

## Related

[[Evals/index]] · [[Evals/failure-log]] · [[Evals/eval-audit-checklist]]
