# Research summary — SMB merchant churn drivers (Q2 2026)

**Author:** Research Analyst · **Status:** For decision input · **Last updated:** 2026-05-28
**Intended use:** Input to the H2 retention business case — should we fund an onboarding-rework bet?
**Research brief questions:** (1) What drives first-90-day SMB churn? (2) Is it concentrated by segment? (3) Would onboarding changes move it?

## Findings

- **F1 — Activation gap drives early churn.** SMB merchants who do not complete a first payout within 14 days churn at 3.1x the 90-day rate of those who do (n=4,200 cohort, internal billing export, May 2026). *Confidence: high* — large internal cohort, consistent across two prior quarters.
- **F2 — Churn concentrates in the sub-10-employee segment.** 71% of first-90-day churn comes from merchants with <10 employees, who are 54% of new signups (internal cohort, May 2026). *Confidence: high* — direct internal segmentation.
- **F3 — Onboarding friction is the top cited reason.** In 18 win/loss interviews (Gong, Apr–May 2026), "setup took too long / unclear" was the most-cited churn reason (11 of 18). *Confidence: medium* — qualitative, modest n, interviewer-selected sample.
- **F4 — Competitors ship guided onboarding.** Stripe and Square both moved to checklist-style guided activation in 2025–26 (their public changelogs + G2 reviews, Mar 2026). *Confidence: medium* — public sources, directionally clear but not a controlled comparison.

## [YOUR_COMPANY] relevance
- All findings tie to [YOUR_COMPANY]'s SMB-heavy book (sub-10-employee merchants are the majority segment) and the H2 retention goal. Activation-to-payout is a metric we already instrument.

## Gaps acknowledged
- No causal test that faster onboarding *reduces* churn — F1 is correlational. An A/B is the missing piece.
- Win/loss sample (F3) skews to merchants who answered outreach; non-responders may differ.
- No EU-segment breakdown; cohort is US-only.

## Sources
- Internal billing + cohort export, May 2026 (F1, F2)
- 18 Gong win/loss interviews, Apr–May 2026 (F3)
- Stripe/Square public changelogs + G2 reviews, Mar 2026 (F4)

## Recommendation
- Fund a scoped onboarding-rework A/B (guided activation checklist) on the sub-10-employee segment. Treat the churn-reduction effect as a hypothesis to be measured by the A/B, not as proven. Decision input is sufficient to justify the test, not to claim the outcome.
