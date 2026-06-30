# Pass criteria — Goals specific, not generic

**Type:** Generalization Failure — workflow Phase 5 prompts for specific outcomes; model defaults to generic PM-textbook outcomes when user input is sparse. Highest grading variance of any eval → **first target for LLM-as-judge calibration** (see `/judge-calibration`). Until calibrated, graded manually.
**Grader:** eval-grader sub-agent (manual); judge in calibration per `calibration-data-plan.md` (to be written).

The 30-60-90 outcomes should name a deliverable, decision, or evidence — not a theme.

## Criteria (binary)

1. ✅ / ❌ Each of the three phases (30 / 60 / 90) has at least 2 outcomes derived from the user's stated answers (anchor project: "Activation funnel redesign", manager: Priya Shah, stakeholders named).
2. ✅ / ❌ At least 50% of outcomes name a deliverable (doc, dashboard, test, decision) — not a generic verb like "understand" or "learn."
3. ✅ / ❌ The 30-day section contains the user's stated 30-day outcome ("Ship activation funnel discovery readout; align Priya on top 3 hypotheses") in recognizable form.
4. ✅ / ❌ The 60-day section contains the user's stated 60-day outcome (A/B test + baseline dashboard) in recognizable form.
5. ✅ / ❌ The 90-day section contains the user's stated 90-day outcome (measurable activation lift + v1 roadmap to skip).
6. ✅ / ❌ No outcome was auto-generated that wasn't traceable to the user's input (no hallucinated metrics, targets, or stakeholder names).

## Failure modes this catches

- Assistant fills 30-60-90 with generic PM-onboarding outcomes ("stakeholder mapping," "audit existing tools") regardless of user role.
- Assistant invents a numeric target ("increase activation by 20%") the user never said.
- Assistant collapses Jordan's three outcomes into one generic outcome.
- Assistant preserves template scaffolding bullets ("[Outcome 1 — specific, observable]") in the final file.
