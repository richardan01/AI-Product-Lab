# Human evaluation as product infrastructure: learning from agent trajectory tests

**Status:** A product-management interpretation of existing experiment evidence, not a new production experiment.

## User problem
Researchers and agent product teams cannot safely infer success from a plausible final response. They need to understand tool choice, parameter grounding, context retention, error recovery, efficiency, and goal completion—then trace failures back to actionable examples.

## Evidence already available
The [agent harness](../../evals/agent-harness/README.md) evaluates seven dimensions against normalized Claude Code and Codex traces. The [September 19 sample report](../../evals/agent-harness/evidence/2026-09-19_sample-coding-retry.md) is synthetic; six of seven dimensions reproduced an earlier run and the divergent dimension was documented. The [controlled real-run report](../../evals/agent-harness/evidence/controlled-real-run/README.md) explicitly lacks recorded grader provenance and independent author/grader separation, so it **cannot** support a reliability claim. [RegEval's discovery report](../../evals/regeval/discovery-pass-2026-06-28.md) documents contaminated held-out evidence and withdrawal of the earlier claim.

## Product decision
Prefer inspectable, provenance-aware evaluations that expose uncertainty over a single overall quality score. This sacrifices a simple headline metric but makes it possible to identify meaningful failures and avoid invalid release claims.

## Human data platform roadmap (proposed)
1. **Collection contract:** Every trace includes task, inputs, model and tool versions, timestamps, outcome, and data-access classification. Redact confidential context before review.
2. **Sampling:** Define task and failure strata, with a locked held-out set. Oversample rare but consequential errors without reporting the oversampled rates as population prevalence.
3. **Annotation specification:** Define each dimension, positive and negative examples, abstain rules, and criteria for adjudicating borderline cases.
4. **Reviewer operations:** Independent blind labels, reviewer qualifications, calibration rounds, disagreement queue, adjudication audit trail, and versioned gold labels.
5. **Measurement:** Report per-dimension confusion matrices, agreement and uncertainty, failure-severity slices, annotation throughput, adjudication latency, and label freshness.
6. **Model/product feedback:** Map repeated failures to hypotheses, interventions, regression fixtures, and launch decisions. Keep test sets independent of prompt development.

## Product metrics
- **North star (proposed):** Percentage of consequential product or model decisions supported by timely, independently validated evaluation evidence.
- **Supporting:** Gold-label coverage by failure slice; inter-reviewer agreement; time to adjudicate; confirmed failures converted into regressions; decision turnaround.
- **Guardrails:** Leaked private traces; labeling rework; uncalibrated judge used for a release gate; stale source policies; evaluator cost and latency.

These metrics are proposals and have no current observed baselines.

## Next falsifiable experiment
Run blind double-labeling on a stratified set of redacted agent trajectories. Compare human-to-human agreement before calibrating an automated judge. Publish an annotation guide, adjudication log, confidence intervals, and one decision that changed as a result. Ask participating reviewers which evidence is missing from the workflow.

## What remains unproven
No demonstrated research-team adoption, scaled human-labeling operation, or production impact. The strength of the existing work is its transparent experimental provenance and documented limitations—not a claim of frontier-model evaluation experience at scale.
