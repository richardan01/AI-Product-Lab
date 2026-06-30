# Answer key — sufficient-research.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

**Research type:** Decision-input research (feeds the H2 retention business case → all 7 gates apply)
**Expected verdict:** SUFFICIENT ✅ (CONDITIONAL ⚠️ acceptable only if the gate flags the acknowledged correlational/causality gap as a downstream caveat — but every gate has genuine supporting content, so no gate should be marked Fail)

## Planted flaws
None. This is the false-positive control.

The summary is deliberately decision-ready: it answers all three brief questions (coverage); cites three distinct source types — internal cohort data, win/loss interviews, public competitor sources (source diversity); every source is dated within ≤3 months (recency, well inside the 6-month bar); findings are contextualized to [YOUR_COMPANY]'s SMB-heavy book and the H2 retention goal ([YOUR_COMPANY] relevance); each finding F1–F4 carries an explicit confidence level (confidence levels); a Gaps-acknowledged section names the correlation-vs-causation limit, the win/loss sampling bias, and the missing EU segment (gaps acknowledged); and the recommendation is scoped and actionable — fund a measurable A/B, do not claim the outcome (actionability).

## Grading notes
- **Eval 01 (verdict-correct):** correct verdict is SUFFICIENT (or CONDITIONAL citing only the acknowledged causality gap, which the summary itself already flags and proposes to resolve via A/B). INSUFFICIENT here is a P0 false-positive failure.
- **Eval 02 (no-hallucinated-gaps):** any gate marked **Fail** is a hallucinated gap — every one of the 7 gates has genuine supporting content. Marking "Confidence levels — Fail" or "Source diversity — Fail" etc. is a fabricated finding.
- **Eval 03 (clean-not-flunked):** passes only if the verdict is SUFFICIENT/CONDITIONAL with **zero Fail gates** and no fabricated blocking gap. Demanding a causal proof the summary already names as a known gap (and correctly defers to an A/B) is not a Fail — the gate scores whether the research is sufficient *for the stated decision* (fund a test), which it is.
- A gate legitimately marked **CONDITIONAL** solely on the correlational nature of F1 is acceptable, because the recommendation already treats churn-reduction as a hypothesis to measure, not a proven claim.
