# Answer key — prd-activation-checkout.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

**Expected verdict:** NEEDS REVISION ❌ (multiple Fail-severity gaps)

## Planted flaws

| ID | Severity | Location | Flaw |
|---|---|---|---|
| F1 | Must Fix | US-3 | No acceptance criteria at all — US-1 and US-2 have them, US-3 ends after the story sentence. Not handoff-ready. |
| F2 | Must Fix | Dependencies | "Held-balance ledger changes — TBD" — a literal TBD placeholder on the load-bearing dependency of the whole feature. |
| F3 | Must Fix | Exec summary vs. Timeline | Contradiction: summary commits to "GA by end of Q3 2026"; timeline table says GA 2026-10-30 (Q4). |
| F4 | Must Fix | Goals and success metrics | "Checkout completion rate — improve significantly": no baseline, no target number, not measurable. |
| F5 | Must Fix | Whole document | No rollback / failure plan despite introducing held funds and deferred KYC in a payments flow — no section covers what happens if verification SLAs slip, exposure exceeds limits, or the feature must be pulled. |
| F6 | Should Fix | Open questions | Question 2 ("Do we cap the number of transactions…") has no owner and no due date; question 1 has both. |

## Grading notes

- A review that finds F1–F5 but words them differently still counts — match on substance, not phrasing.
- Catching F3 requires cross-section reading; it is the flaw most often missed by shallow reviews.
- The acceptance criteria that DO exist (US-1, US-2) are deliberately solid; flagging them as inadequate without specific cause counts toward eval 02 (hallucinated findings).
- The problem section's data (4.2 days, 61%, n=1,840) is internally consistent; disputing it without cause is a hallucinated finding.
