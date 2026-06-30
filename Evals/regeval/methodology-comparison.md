# Methodology comparison — Shreya's error-discovery vs RegEval

**The purpose of the eval is to map both what we KNOW and what we DON'T KNOW about
RegEval's failure modes and edge cases.** That goal has two halves, and the two
methodologies below are the two engines that serve them — they are not rivals, they are
opposite ends of the same pipeline.

- **Unknown-engine** — Shreya Shankar / Hamel Husain's error analysis
  (`shreyashankar/error-discovery-skill`). *Discovers* failure modes we haven't seen.
- **Known-engine** — RegEval's κ loop. *Measures and guards* failure modes we already have.

A complete eval needs both. RegEval today is a strong known-engine with **no unknown-engine** —
that is the one real gap (deferred build; see [[Evals/regeval/failure-taxonomy]]).

## Side-by-side

| Dimension | Shreya's `error-discovery-skill` (unknown-engine) | RegEval (known-engine) |
|---|---|---|
| **Job** | **Discovery** — surface unknown failure modes | **Optimization** — align a judge to κ≥0.80 and hold it |
| **Lifecycle stage** | Front-end: "what should I even build evals for?" | Back-end: "is my judge right, and improving?" |
| **Target of analysis** | The **system under test** | The **judge** (meta-eval) |
| **Sampling** | **Clustered + diverse** (≈60–70% cluster reps, 30–40% random) — built to find unknowns | **Sliced**: abstains + confident-wrong — surfaces *known* failure directions |
| **Annotation** | Single-file HTML app, free-text **open coding**, agent suggests/categorizes | Markdown queue + `inputs/corrections-log.md` + `failure-taxonomy.md` |
| **Saturation tracking** | **Yes** — coverage gaps; pushes new samples until saturated | **No** |
| **Measurement** | **None** — explicitly "not estimating how common they are" | **Cohen's κ + bootstrap CI + per-class κ + TPR/TNR/abstention** + κ-gaming guards |
| **Anti-overfit / held-out** | No | **Now real (2026-06-28).** ⚠️ The original "70-item held-out gate" was a **phantom** — `gold_expansion.jsonl` was a duplicate of the tuning set (FM-11). Replaced by genuine net-new `heldout_v2.jsonl` (36 items, 20 unseen regimes). See [[Evals/regeval/discovery-pass-2026-06-28]]. |
| **Regression / model-upgrade audit** | No | **Yes** — cross-model runs (Fable 0.677, Opus 0.768) |
| **Provenance** | Light (annotated dataset) | **Strong** — append-only log, snapshots, reconciliation (Δ=0.0002), trace records |
| **End artifact** | Web app + categorized taxonomy | κ verdict + experiment log + taxonomy + adjudication CLI |

## Where each wins

**Shreya's is stronger at finding what you don't know.** The clustered diverse sample + saturation
loop is built to surface modes you never imagined. RegEval's loop cannot do this — it only ever sees
failures that already showed up as judge-vs-gold disagreements.

**RegEval is stronger at everything downstream of "we know the failure."** Shreya's skill stops at a
categorized taxonomy: **no κ, no CI, no held-out gate, no regression audit, no reproducibility
envelope.** Once you know what to measure, RegEval is the far more rigorous instrument — and that
measurement rigor is the rarer, more interview-defensible signal.

## The blind spot each has

- **Shreya's:** discovers modes but **can't prove a fix worked or guard against regression** — no metric.
- **RegEval's:** measures rigorously but **never ran the forward discovery pass** — so it is blind to
  modes that don't manifest as disagreements, and it analyzes the *judge*, not the *system*. The
  sharpest version was the confident-wrong blind spot (the loop only watched where the judge *hedged*,
  never where it was *confidently wrong*) — now closed by the confident-mismatch slice in `score.py`.

## Conclusion — they compose; run both

Best practice is to run the **unknown-engine to seed** the gold set + taxonomy, then run the
**known-engine to optimize and guard** it. RegEval silently assumed discovery was already done; the
known/unknown ledger (`failure-taxonomy.md`) and the deferred discovery front-end are how that
assumption gets repaid.

| Half of the purpose | Engine | Status in RegEval |
|---|---|---|
| **What we KNOW** (measure + guard) | RegEval κ loop | Built, rigorous |
| **What we DON'T KNOW** (discover) | Shreya discovery front-end | **Not built — the gap** |

## Related

[[Evals/regeval/failure-taxonomy]] · [[Evals/regeval/regeval-suite]] · [[Evals/regeval/metric]] · [[Evals/regeval/review-queue]] · [[.claude/skills/evals/SKILL]] · [[Evals/index]]
