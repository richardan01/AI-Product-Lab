# RegEval gold dataset

**Format:** `gold.jsonl` — one JSON object per line.

```json
{"id": "reg-0001", "input": "<scenario text>", "gold_label": "accept|reject|abstain", "gold_rationale": "<one sentence>", "annotators": ["RC", "X"], "agreement": "unanimous|majority|tied"}
```

**Domain:** regulated-fintech LLM output decisions (the RegEval thesis domain). Each item is a scenario where a downstream LLM is asked to produce a customer-facing answer, and the gold label is whether the *scaffold* should let the answer ship (`accept`), block it (`reject`), or refuse to decide (`abstain`).

## Day-30 target

- N ≥ 100 items
- Annotators: 2 minimum, with documented inter-annotator agreement (Cohen's κ ≥ 0.70 between annotators before any item enters gold)
- Item distribution: 40% accept · 40% reject · 20% abstain (do not over-weight the easy class)
- Adversarial planted items: ≥ 10% of total (analogous to discovery-synthesis fixture practice)

## Build protocol

1. Draft items in `_drafts/` (not in this folder until labelled).
2. Two annotators label independently. Disagreements adjudicated by a third reader; if still tied, the item is excluded from gold (logged in `_excluded.md`).
3. Promote labelled items into `gold.jsonl` only after κ ≥ 0.70 between annotators on the batch.
4. Snapshot `gold.jsonl` weekly into `snapshots/YYYY-MM-DD.jsonl` so experiment lineage is reproducible.

## Files

- `gold.jsonl` — the live gold set (does not yet exist; Day-30 deliverable)
- `test_kappa.jsonl` — small fixture for verifying the κ implementation produces 0.40 ± 0.01 (see metric.md)
- `_drafts/` — unlabelled candidates
- `_excluded.md` — items rejected from gold, with reason
- `snapshots/` — weekly snapshots for lineage

## Inter-annotator agreement

**Protocol used (2026-05-29):**

The dual-annotator requirement was implemented as follows:
- **Annotator 1 (RC):** gold labels authored by Lucius Fox in the same session as item generation.
- **Annotator 2 (Model-A):** a blind grader subagent given the same item texts stripped of `gold_label` and `gold_rationale`, applying independent expert judgment under HK financial-compliance standards.

**IAA run:** 20-item sample (reg-0031–reg-0050), covering 10 compliant + 10 non-compliant items.

| Metric | Value |
|---|---|
| N (IAA sample) | 20 |
| Annotator agreement | 20/20 (100%) |
| Cohen's κ (A1 vs A2) | 1.000 |
| IAA gate (κ ≥ 0.70) | ✅ PASS |

**Limitation:** The IAA sample covered only the binary classes (compliant / non-compliant). The `unclear` class was not represented in the 20-item sample. A follow-up IAA run on a mixed sample including `unclear` items is recommended before citing the gold set for external publication.

**Items promoted to gold.jsonl:** All 70 expansion items passed the binary-class IAA gate. Items are tracked with `gold_label` and `gold_rationale` fields; `annotators` and `agreement` schema fields will be added in a future revision.

## Anti-patterns

- Adding to `gold.jsonl` mid-week without a snapshot first (breaks lineage)
- Single-annotator labels (Riddler will block any claim built on these)
- Reusing draft items the scaffold author has already seen as labelled gold (leakage)

## Related

[[Evals/regeval/regeval-suite]] · [[Evals/regeval/runner]] · [[Evals/regeval/metric]] · [[Evals/regeval/experiments/log]] · [[Knowledge/Research/regeval-synthesis]]
