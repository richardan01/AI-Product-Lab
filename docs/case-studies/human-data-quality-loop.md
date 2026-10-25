# Human data quality: from agent traces to defensible decisions

**Status:** Proposed next-step design; the repository does not demonstrate a production human-data platform.

## Product question
How can an AI product or research team turn messy agent failures into a trustworthy set of human judgments that informs model, product, and release decisions?

The existing [agent-harness](../../evals/agent-harness/README.md) evaluates task success and six trajectory dimensions. The [RegEval discovery](../../evals/regeval/discovery-pass-2026-06-28.md) shows why falsely held-out evaluation evidence must be invalidated, not quietly reused.

## Decision
Prioritize provenance, independent annotation, and disagreement resolution **before** building a broader judge dashboard. The alternative—a larger automated evaluation surface first—would increase apparent coverage without establishing trustworthy labels.

## Proposed research-to-product loop
1. **Select traces:** Stratify by critical failures, uncertainty, tool choice, error recovery, model version, and user workflow. Record the source and sampling rationale.
2. **Specify labels:** Define one narrow judgment per rubric item, explicit abstention and ambiguous cases, severity, and the policy or task evidence required.
3. **Collect independent judgments:** Keep human raters blind to the agent version and model-generated grades where feasible; track reviewer identity pseudonymously, rubric version, annotation time, and confidence.
4. **Adjudicate disagreement:** Preserve original labels; capture consensus, adjudicator rationale, and reasons for disagreement instead of overwriting history.
5. **Validate automation:** Compare each proposed LLM judge against adjudicated human data by failure slice; report false accepts, false rejects, uncertainty intervals, costs, and drift. Do not use uncalibrated judge scores as release gates.
6. **Make a product decision:** Create prioritized error clusters, propose a system change, rerun a locked test set, and document regressions and the launch decision.
7. **Close the loop:** Track whether fixes improve real user workflows, not only an offline score.

## Evidence boundaries
- Existing real-run records and synthetic examples have different provenance; do not combine them into an advertised reliability rate.
- Historical RegEval held-out scores are not independently reproducible from the public repository.
- This document is a proposed operating model, **not** proof of real annotator operations or collaboration with model researchers.

## MVP artifacts to publish next
- A versioned annotation guideline with positive, negative, and ambiguous exemplars.
- A small *independently labeled* sample and disagreement/adjudication log with permitted public data.
- A dataset manifest recording train/dev/held-out partition, version, lineage, contamination checks, and label provenance.
- A baseline-vs-candidate decision memo with error slices, uncertainty, latency, cost, and explicit release guardrails.
- A usability study with target evaluators or researchers and a written product decision influenced by the findings.

## North star and guardrails
**Candidate north star:** Percentage of consequential product/research decisions supported by an auditable, sufficiently reliable evaluation package. Validate this with target users before adoption.

**Supporting measures:** time to adjudicated label, coverage of critical failure slices, labeling throughput, researcher reuse, and turnaround from failure discovery to verified fix.

**Guardrails:** disagreement rates, false-pass rates on critical failures, leakage/contamination, privacy exposure, reviewer burden, and judge calibration drift.

**Trade-off to test:** More annotators and richer provenance improve trust but increase cost and decision latency. Optimize for decision quality, not raw label count.

## Learning
Human data is not merely a dataset: it is a versioned decision process. To position this work for human-data product roles, the next proof must be actual independent labeling and researcher/customer feedback—not another unvalidated automation layer.
