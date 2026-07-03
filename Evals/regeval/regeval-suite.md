# RegEval — Autoresearch loop

**Owner:** Lucius Fox (build) · Bruce Wayne (kill/keep) · Henri Ducard (depth review)
**Q3 thesis tie:** flagship deliverable; Day-30 signpost = first credible run.
**Karpathy frame:** one runner, one metric, one fixed time budget, compounding log. The metric is the reviewer.

---

## What this loop optimizes

A **judge-alignment scaffold** for regulated-domain LLM output. The artifact under test is the *scaffold* (prompt, decomposition, abstention policy, judge rubric) — not the underlying model. Each experiment varies one element of the scaffold, runs against the gold dataset, scores, and is kept or discarded.

This is Karpathy's autoresearch shape: many small bets, fast cycle, single metric, tight budget.

## The metric (single, named, falsifiable)

**Cohen's κ between LLM-as-judge and the human gold label**, computed over the gold dataset.

- κ ≥ 0.80 → judge is a credible stand-in for human labelers ("substantial agreement")
- 0.60 ≤ κ < 0.80 → directional only; do not ship

> **2026-06-28 — task is now BINARY** (compliant vs non-compliant). The `unclear` class failed IAA
> (κ=0.48) and is quarantined; the prior "held-out" was a duplicate of the tuning set (FM-11).
> Current champion `binary-v1`: κ=1.000 in-sample (82) + κ=1.000 genuine held-out (36, 20 unseen
> regimes). Score with `score.py --binary`. Full record + caveats:
> [[Evals/regeval/discovery-pass-2026-06-28]].

## Related

[[Evals/index]] · [[Projects/ralph/brief]] · [[Agents/Gotham/Computer/lucius-fox]] · [[Agents/Gotham/Computer/henri-ducard]] · [[Evals/eval-audit-checklist]] · [[Knowledge/Research/regeval-synthesis]]
- κ < 0.60 → judge is unreliable; treat the scaffold as failing

Secondary diagnostics (logged, not optimized): TPR, TNR, abstention rate. These exist to catch κ-gaming (e.g. a judge that abstains on everything will look "calibrated" but is useless).

Definition + computation: see [metric.md](metric.md).

## The time budget (fixed; non-negotiable)

| Window | Budget | Cap |
|---|---|---|
| Per experiment | ≤ 5 min wall clock end-to-end | hard kill at 8 min |
| Per session | ≤ 60 min (12 experiments) | walk away after |
| Per week | fixed cap (Q3 thesis allocation) | RegEval cannibalises nothing else |

If an experiment exceeds 8 min, it is *discarded as a failed experiment*, not extended. Karpathy principle: unbounded effort dilutes all pillars.

## The loop

```
1. Pick ONE scaffold element to vary (prompt section, decomposition step, judge rubric line, abstention threshold)
2. Make the change in scaffolds/<name>.md
3. Run runner against inputs/gold.jsonl
4. Compute κ + diagnostics
5. Append a row to experiments/log.md
6. Keep (overwrite scaffolds/current.md) or discard (no overwrite)
7. Repeat until session budget exhausted
```

Trigger: `/regeval-run <scaffold-name>` (skill at [runner.md](runner.md)).

## Kill / pivot criterion (Day 60 — June 30, 2026)

Per the Q3 thesis: *"Can I record a 5-minute RegEval demo I'd show a frontier-lab hiring manager without flinching?"*

Concrete signals at Day 60:
- κ ≥ 0.80 on at least one scaffold variant **and** the variant is reproducible from the log
- Gold dataset ≥ 100 labelled items with inter-annotator agreement documented
- One experiment per session-day for the prior 14 days (compounding cadence, not bursts)

Miss any → pivot per thesis-q3-2026.md.

## Directory contract

```
Evals/regeval/
├── regeval-suite.md                ← this file
├── metric.md                       ← κ definition, computation, edge cases
├── runner.md                       ← /regeval-run skill
├── budget.md                       ← weekly wall-clock budget tracker
├── inputs/
│   ├── regeval-gold-dataset.md     ← gold dataset spec, labelling protocol
│   └── gold.jsonl                  ← {id, input, gold_label, gold_rationale}
├── scaffolds/
│   ├── current.md                  ← the live champion (only overwrite on keep)
│   └── candidates/                 ← variants under test
└── experiments/
    ├── _template.md                ← per-experiment writeup
    ├── log.md                      ← chronological one-line-per-experiment log
    └── <YYYY-MM-DD-NN>-<slug>.md   ← individual experiment files
```

## Anti-patterns (kill on sight)

- Running an experiment without writing it to `log.md` (untracked = didn't happen)
- Editing `scaffolds/current.md` outside a Keep decision (state corruption)
- Optimizing on a held-out set seen during scaffold authoring (leakage) — ⚠️ this exact failure
  occurred and went undetected until 2026-06-28 (FM-11: `gold_expansion.jsonl` was a duplicate of
  the tuning set). The lesson is now load-bearing: a held-out set must be verified disjoint from
  tuning (id + text) before any out-of-sample κ is cited.
- Self-graded judge alignment (judge ≠ author of scaffold)
- "Just one more variant" past the 60-min session cap

## References

- [Q3 thesis — Day-30 signpost](../../Agents/Gotham/thesis-q3-2026.md)
- [Karpathy autoresearch](https://github.com/karpathy/autoresearch)
- [judge-calibration skill](../../.claude/skills/judge-calibration/SKILL.md) — judge-alignment methodology
- [eval-runner](../../.claude/agents/eval-runner.md) / [eval-grader](../../.claude/agents/eval-grader.md) — author/grader separation enforcement
- discovery-synthesis suite — private companion eval (different harness, same discipline; not included in this public repo)
