# RegEval gold dataset

**Format:** `gold.jsonl` — one JSON object per line.

```json
{"id": "reg-0001", "input": "<scenario text>", "gold_label": "compliant|non-compliant|unclear", "gold_rationale": "<one sentence>"}
```

**Domain:** regulated-fintech LLM output decisions (the RegEval thesis domain). Each item is a scenario where a downstream LLM is asked to produce a customer-facing answer, and the gold label is whether the answer complies (`compliant`), violates (`non-compliant`), or cannot be decided from the scenario (`unclear`).

> **Label-vocabulary note:** the original Day-30 spec used `accept|reject|abstain`. The build settled on `compliant|non-compliant|unclear` (see experiments REV-006/REV-007); all shipped snapshots, the scorer, and the run log use the current vocabulary.

## Status (post-build — current as of 2026-06-28)

- **Gold set exists since 2026-06-04** at N=100 (40 compliant / 40 non-compliant / 20 unclear), expanded via REV-007 from the original 30-item seed.
- **Binary split (2026-06-28):** the 18 reconciled `unclear` items are quarantined by `score.py --binary`, leaving **82 binary in-sample items**; a separate **36-item author-constructed held-out set** (`heldout_v2.jsonl`, 20 unseen regimes) gates out-of-sample claims.
- **What ships in this public repo:** the snapshots under `snapshots/` (including the full 100-item `2026-06-28_gold_pre-split.jsonl`) and the IAA sample under `iaa/`. The live working files (`gold.jsonl`, `heldout_v2.jsonl`) are local working copies — predictions against them ship in `experiments/.preds/`.

## Build protocol (as executed)

1. Items drafted and labelled per batch; disagreements adjudicated (see `corrections-log.md` for the gold-cal-v1 relabels).
2. IAA gate before promotion: Cohen's κ ≥ 0.70 between annotators on the batch.
3. `gold.jsonl` snapshotted into `snapshots/YYYY-MM-DD*.jsonl` before any mid-week change, so experiment lineage stays reproducible.
4. Held-out integrity: `heldout_v2` verified disjoint from the tuning set by item ID **and** text before any out-of-sample κ is cited (the FM-11 lesson — see `Evals/regeval/regeval-suite.md`).

## Files

- `snapshots/` — dated gold snapshots for lineage (**shipped**; `2026-06-28_gold_pre-split.jsonl` is the full 100-item set)
- `iaa/` — inter-annotator agreement sample + protocol (**shipped**)
- `corrections-log.md` — gold relabels with adjudication reasoning (**shipped**)
- `gold.jsonl` — 100-item in-sample gold set (**shipped**; identical content to `snapshots/2026-06-28_gold_pre-split.jsonl` — the shipped file is the canonical working copy)
- `heldout_v2.jsonl` — 36-item genuine held-out set (**local, not shipped**; labels stay local to prevent contamination; predictions ship in `experiments/.preds/`)

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

## Anti-patterns

- Adding to `gold.jsonl` mid-week without a snapshot first (breaks lineage)
- Single-annotator labels (Riddler will block any claim built on these)
- Reusing draft items the scaffold author has already seen as labelled gold (leakage)
- Citing out-of-sample κ before verifying held-out/tuning disjointness by ID + text (FM-11)

## Related

[[Evals/regeval/regeval-suite]] · [[Evals/regeval/runner]] · [[Evals/regeval/metric]] · [[Evals/regeval/experiments/log]] · [[Knowledge/Research/regeval-synthesis]]
