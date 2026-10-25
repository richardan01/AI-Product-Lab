# From agent traces to research-quality human evaluation

**Status:** Proposed product direction and evidence-based gap assessment; not a claim of completed research-user validation.

## Problem
A final answer can look plausible even when an agent chose the wrong tool, invented arguments, forgot context, or recovered badly. Researchers and product owners need traceable signals connecting failures to fixes, rather than a single opaque quality score.

## Current evidence
The [agent-harness suite](../../evals/agent-harness/README.md) tests seven dimensions: task success, tool choice, parameter extraction, error recovery, context retention, efficiency, and goal alignment. Published examples document grader provenance and distinguish synthetic traces from a controlled real tool-use run. The [RegEval discovery](../../evals/regeval/discovery-pass-2026-06-28.md) explicitly invalidated a contaminated held-out claim.

These artifacts demonstrate a methodology and its limits, **not** a representative reliability rate across production agents.

## Product decision and trade-offs
Prioritize **human-auditable failure classification and provenance** ahead of a hosted dashboard or broad provider integrations. This sacrifices integration breadth and rapid visual polish in favor of the ability to inspect how a judgment was produced.

## Human-data platform requirements to explore
- **Sampling:** representative and risk-targeted traces, plus untouched holdouts; track inclusion criteria and distribution shifts.
- **Annotation instructions:** explicit failure definitions and examples distinguishing bad (trust blocking), sad (friction), and ambiguous cases; avoid conflating labels with model-generated rationale.
- **Review workflow:** independent annotation, disagreement detection, expert adjudication, and label versioning.
- **Provenance:** trace ID, source version, task definition, reviewer, grader, rubric version, run date, and model identifier.
- **Measurement:** inter-reviewer agreement, judge vs human performance per class, confidence intervals, tool-trajectory error rates, review throughput, and cost per usable label.
- **Product loop:** failure cluster → prioritized intervention → paired rerun → regression and slice review → human release decision.

## Next experiment (not yet run)
1. Interview or observe at least three people who actually build, review, or evaluate agents. Record where annotation and debugging take time; confirm whether the proposed workflow addresses a real problem.
2. Collect a consented or synthetic, well-documented trace sample across multiple failure types. Keep privacy-sensitive traces private.
3. Have two reviewers independently label a stratified subset using a draft annotation manual. Record disagreement and adjudication, then revise the manual.
4. Compare model graders with adjudicated human decisions, separately by failure class; include uncertainty and missing-provenance rates.
5. Ship a small read-only review surface only after demonstrating that it shortens investigation time or improves agreement without masking important failures.

## Proposed success criteria
**North star:** Number of evidence-backed agent product decisions enabled by independently reviewed trace evidence (requires user validation before adoption).

Supporting: adjudicated labels per reviewer-hour, median investigation time, percentage of traces with complete provenance, and time from failure discovery to validated regression fix.

Guardrails: critical false-pass rate, unresolved label disputes, private-trace exposure, reviewer anchoring, and cost per accepted label.

These are **candidate metrics**, not reported outcomes. A limited synthetic run is not proof of real-world safety or product-market fit.

## Frontier-AI PM positioning
This work is intended to demonstrate judgment about human-data quality, researcher workflows, evaluation measurement, and responsible release. The missing evidence is equally important: real researcher interviews, independent labels at useful scale, deployment integration, and measurable user outcomes. Those should guide the next iteration rather than be implied as already achieved.
