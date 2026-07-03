# Calibration data plan — eval 05 (goals-specific-not-generic)

This is the first eval in AI Product Lab to receive a calibrated LLM-as-judge. The criterion is the most subjective in the onboarding suite (highest grading variance), so calibration pays off most here.

## Target corpus
- **30 Pass** labeled examples (30/60/90 outcomes that are specific, deliverable-named, derived from user input)
- **30 Fail** labeled examples (outcomes that are generic, themed, or fabricated despite user uncertainty)
- Total: 60 minimum to satisfy `/judge-calibration` (20% train, 40% dev, 40% test)

## Sources

| Source | Target count | Notes |
|---|---|---|
| Real traces from `Evals/onboarding/_traces/` (captured by `trace-collector`) | 20 | Highest-quality signal. Mix of Executive / Builder / Minimalist personas. |
| Adversarial synthetic generation | 20 | Use a prompt that deliberately generates generic outcomes for diverse personas. Document the generation prompt in `_labeled/_synthetic-prompts.md` once created. |
| Expansions of `sample-pass.md` + `sample-fail.md` | 20 | Take each anchor and vary the persona, deferral state, or domain. Document the expansion logic. |

## Current count

| Class | Count | Source breakdown |
|---|---|---|
| Pass | 0 | — (corpus is generated in a working copy; kept local, gitignored) |
| Fail | 0 | — (corpus is generated in a working copy; kept local, gitignored) |

The labeled corpus lives under `_labeled/` in a working copy and is **gitignored** (run evidence, not template scaffolding). Run `/judge-calibration` to build/split it and produce the calibration report under `_calibration/` (also gitignored).

## Owner & timeline

- **Owner:** [YOUR_NAME]
- **Target completion:** end of Week 4 (per `/root/.claude/plans/on-evals-can-you-reactive-beaver.md`)
- **Status:** `gathering` (flips to `split` once corpus hits 60, then `calibrated` after `/judge-calibration` PASSes, then `deployed` once `judge-prompt.md` is promoted — all tracked in the local working copy, not the public template)

## TPR/TNR targets

- TPR_test ≥ 0.90
- TNR_test ≥ 0.90
- Re-validation: every 90 days OR on Claude model version change

## What "Pass" and "Fail" mean for this corpus

**Pass example shape:** A 30/60/90 outcome that names a deliverable, decision point, or measurable evidence, and traces back to a user statement during onboarding. E.g. "Ship the activation funnel discovery readout; align Priya on top 3 hypotheses" (from a user who said they're working on activation).

**Fail example shape:** A generic outcome that would fit any PM at any company at any quarter. E.g. "Learn the product", "Build relationships with stakeholders", "Ship something meaningful". Also Fail: a specific-sounding outcome the user did NOT state — fabricated specificity is worse than generic blandness.

**Borderline (label carefully):** Outcomes that are specific but only marginally derived from user input. These belong in the dev/train splits with explicit borderline notes — they teach the judge where the line is.

## Files this plan governs

- `_labeled/pass-NNNN.md` and `_labeled/fail-NNNN.md` — the corpus
- `_labeled/_synthetic-prompts.md` — generation prompts for the synthetic 20
- `_calibration/<date>_*.md` — written by `/judge-calibration`
- `judge-prompt.md` — written by `/judge-calibration` when status flips to `deployed`

## Note

Until status is `deployed`, eval 05 is graded manually by the `eval-grader` sub-agent. The judge is **not** live in production grading until the calibration final report passes test.
