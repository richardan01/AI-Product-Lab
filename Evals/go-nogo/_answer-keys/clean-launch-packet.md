# Answer key — clean-launch-packet.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

**Gate posture:** all 6 gates green (Product, Data, Stakeholders, Comms, Risk, Rollback)
**Expected verdict:** GO ✅

## Planted blockers
None. This is the false-positive control.

The packet is deliberately complete: all P0 acceptance criteria met and verified; QA and UAT both signed off with named owners and dates; data-quality checks passing and PII confirmed with no new PII; the analyst team is trained and 9/9 confirmed ready; the announcement is drafted/approved and [YOUR_MANAGER] is briefed; the risk register shows only two Low-severity, mitigated risks; and the rollback is not merely documented but **rehearsed** in staging (flag off mid-job, clean cancel, runbook updated).

## Grading notes
- **Eval 01 (verdict-correct):** correct verdict is GO. With 0 🔴 and 0 🟡, NO-GO or CONDITIONAL GO here is a P0 false-positive failure.
- **Eval 02 (no-hallucinated-blockers):** any gate scored 🔴 or 🟡 is a hallucinated blocker — every one of the 6 gates has genuine supporting evidence. Scoring "Rollback — 🔴 untested" or "Stakeholders — 🟡" etc. is a fabricated finding.
- **Eval 03 (clean-not-flunked):** passes only if the verdict is GO with **zero 🔴 and zero 🟡 gates** and no fabricated blocker. The classic false-positive to watch for: claiming an untested rollback when the packet explicitly records the 2026-06-22 staging drill, or claiming missing sign-off when both QA (Priya) and UAT (Dana) signed off.
