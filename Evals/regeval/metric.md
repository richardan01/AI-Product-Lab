# RegEval metric — Cohen's κ for judge-alignment

**Single optimized metric.** Everything else in the log is diagnostic.

> **2026-06-28 — BINARY as of the discovery pass.** The `unclear` class failed inter-annotator
> agreement (κ=0.48, 2/18 — see [[Evals/regeval/discovery-pass-2026-06-28]]). The optimized task is
> now **binary: compliant vs non-compliant**. `unclear` is no longer a gold class; it is quarantined
> pending human re-adjudication. Abstention, if reintroduced, will be a *separately measured
> calibrated-confidence flag*, NOT a gold label.
>
> **Pinned judge model.** Cite κ only with the judge model id + harness. Numbers are not comparable
> across either. Reproducible demo harness = **Sonnet subagent, forced-commit, shuffled order**
> (the 2026-06-04 κ=0.820 was Sonnet-4-5 API one-call and does **not** reproduce on this harness —
> FM-10, ~0.25 shift). Always log `model_id` + `harness` on every row of `results.tsv`.
>
> **Held-out is real now.** Use `inputs/heldout_v2.jsonl` (net-new, 20 regimes). The old
> `gold_expansion.jsonl` is DEPRECATED — it was a duplicate slice of the tuning set (FM-11).

## Definition

For each item `i` in the gold dataset:
- `g_i` ∈ {accept, reject, abstain} — human gold label
- `j_i` ∈ {accept, reject, abstain} — LLM-as-judge label produced by the scaffold under test

Compute Cohen's κ over the full gold set:

```
κ = (p_o − p_e) / (1 − p_e)
```

where `p_o` is observed agreement and `p_e` is expected agreement under independence (per-class marginal product summed across classes).

## Interpretation bands

| κ | Band | Action |
|---|---|---|
| ≥ 0.80 | Substantial / near-perfect | Candidate to overwrite `scaffolds/current.md` |
| 0.60 – 0.79 | Moderate | Directional; log and continue varying |
| 0.40 – 0.59 | Fair | Do not promote; record as "negative result" |
| < 0.40 | Poor | Discard; consider whether the scaffold change was confounded |

The 0.80 bar is the published convention for "substantial agreement" (Landis & Koch). It is not a vibe.

## Required diagnostics (logged with every run)

These are not optimized but must be logged to detect κ-gaming:

| Diagnostic | What it catches |
|---|---|
| **TPR** (recall on accept) | Judge that always-rejects |
| **TNR** (recall on reject) | Judge that always-accepts |
| **Abstention rate** | Judge that abstains its way to apparent calibration |
| **Per-class κ** (one-vs-rest for each of accept/reject/abstain) | Class collapse hidden in the macro number |
| **N** (gold set size used) | Stat power — flag any run with N < 30 |
| **Confidence interval** (bootstrap, 1000 resamples, 95%) | Is the κ estimate stable? |

Any run where abstention rate > 50% **and** κ ≥ 0.80 is flagged "suspicious" and excluded from Keep decisions until inspected.

## Edge cases

- **Tied items in gold.** If two annotators disagreed and the gold label is "tied", exclude from κ; log under `excluded_n`.
- **Judge produces a 4th class** (e.g. "uncertain"). Map to abstain. Log the rate so we can see scaffold drift.
- **Gold set rebalancing.** If you add/remove gold items, you reset `current.md` and start a new experiment lineage. Old κ numbers are not comparable.
- **κ paradox.** If marginal distributions are extreme (e.g. 95% accept), κ deflates even with high agreement. Always read κ alongside per-class TPR/TNR — never alone.

## Computation

Use `scipy.stats.cohen_kappa_score` or the inline implementation below. Either is acceptable; both must produce identical output on the test fixture.

```python
def cohen_kappa(gold, pred):
    from collections import Counter
    classes = sorted(set(gold) | set(pred))
    n = len(gold)
    p_o = sum(g == p for g, p in zip(gold, pred)) / n
    g_marg = Counter(gold); p_marg = Counter(pred)
    p_e = sum((g_marg[c]/n) * (p_marg[c]/n) for c in classes)
    return (p_o - p_e) / (1 - p_e) if p_e < 1 else 1.0
```

Test fixture: `inputs/test_kappa.jsonl` (planted disagreements) must produce κ = 0.40 ± 0.01.

## Why κ and not accuracy

Accuracy is misleading on imbalanced gold sets (which RegEval will be — refusal cases are rare and high-stakes). κ corrects for chance agreement. Riddler will block any scaffold report that quotes accuracy without κ.
