# RegEval autoresearch — research goal

**This is the `program.md` of the loop.** The autonomous overnight loop (`regeval-loop.sh`) reads this file to decide *what to run, in what order, when to stop, and what it is forbidden to do*. Humans write hypotheses here; the loop executes them. That separation is the whole design (Karpathy: humans write goals, agents run mechanics).

**Architecture:** Framing 1 (Lab Notebook) + held-out verify slice. The loop runs a human-authored queue of candidate scaffolds — it does **not** invent its own variants. See `Agents` decision log / `os-karpathy-km-assessment` memory (2026-06-20).

---

## Objective

> **SUPERSEDED 2026-06-28 by the forward discovery pass** — see
> [[Evals/regeval/discovery-pass-2026-06-28]]. Two integrity defects were found:
> the "held-out" set was a duplicate of the tuning set (FM-11), and the `unclear` class failed IAA
> (FM-12, κ=0.48). The task is now **binary** (compliant vs non-compliant); `unclear` is quarantined.
> New objective: **hold binary κ on a GENUINE held-out** (`heldout_v2.jsonl`, 20 new regimes) and
> extend to borderline + production data. Current: binary κ=1.000 in-sample (82) and κ=1.000 held-out
> (36) — clean-construct caveat applies. **Pin model_id + harness on every cited κ** (FM-10: the API
> 0.820 does not reproduce on the demo-able subagent harness).

*(historical objective, pre-collapse:)* Find a judge scaffold that beats the champion (κ=0.820) AND
holds up on held-out data — i.e. a more *robust*, not just higher, κ.

Single optimized metric: **Cohen's κ** (judge vs human gold). Definition + bands: [metric.md](metric.md). KEEP bar: κ ≥ 0.80 **and** CI lower bound ≥ 0.70 **and** abstention ≤ 0.50.

## Harness (locked 2026-06-20: subagent, no API key)

The loop judges via **Claude Code subagents**, not the API. Per candidate, in a fresh `claude` context:
- Spawn judge subagents over `inputs/gold.jsonl`, **batched 10 items/context**, with explicit per-item independence instructions.
- **Strip `gold_label` and `gold_rationale` from judge inputs** — the judge sees only `input`.
- Caveat (must be logged on every row): batching is a within-context contamination confound — κ is **comparable-with-caveat**, not strictly comparable to the API path. If an `ANTHROPIC_API_KEY` ever becomes available, `run_experiment.py`'s one-call-per-item path supersedes this and the caveat drops.

Scoring (κ, CI, TPR/TNR, abstention, per-class κ) is computed from the subagent predictions by `score.py` (no API key needed) — see that module.

## Held-out verify slice (the anti-overfit gate)

The champion was tuned on the 100-item `inputs/gold.jsonl`. The 70-item **`inputs/gold_expansion.jsonl`** (30 compliant / 30 non-compliant / 10 unclear, same schema) was **never used for tuning** — it is the held-out validation set.

**Promotion rule:** a candidate that scores KEEP on the 100-item tuning set is **not** promoted to champion until it also scores **κ ≥ 0.70 on the held-out 70**.
- Passes both → status `KEEP-confirmed` (still requires a human nod to overwrite `current.md` — see Forbidden actions).
- Passes tuning, fails held-out → status `KEEP-overfit-flag`. Logged, surfaced, **not** promoted. This is the demo-defensible answer to "how do you know it didn't overfit your 100?"

## Candidate queue (human-authored — the loop runs these in order)

A candidate is runnable only if `scaffolds/candidates/<slug>.md` exists. Missing-file entries are skipped with a note (author the scaffold to activate).

| # | slug | status | scaffold file? | hypothesis (one line) |
|---|---|---|---|---|
| 1 | `skills-v2` | **pending** | ✅ exists | Retune the skills-architecture (drafted 2026-06-08, never run) to fix skills-v1's trigger-5a over-fire on policy/procedure descriptions while keeping the structured workflow. |
| 2 | `fable-judge-v2` | queued — needs scaffold | ❌ author first | Retune only the abstention section of v4 for Fable's non-hedging bias (fable-judge-v1 collapsed unclear at κ=0.299). |

Add rows as you author candidates. Keep the queue ranked by expected leverage. Mark `done` after a run (the loop also records this in `results.tsv`).

## Ruled-out levers (DO NOT re-run — the log already killed these)

- **Binary-threshold tightening / low-abstention** — `rubric-strict` reproduced baseline exactly; unclear items are genuinely indeterminate, not borderline-binary.
- **Blanket trigger-5b constraint** — `rubric-graded-v3` over-corrected (−2 net vs v2).
- **Adversarial challenger / refutation flip** — `challenger-v1` catastrophic (κ=0.380); flip logic is wrong when the judge is already calibrated.

## Stop conditions (loop halts when ANY is true)

1. Queue exhausted (no `pending` candidates with an existing scaffold file).
2. **Loop-until-dry:** K=2 consecutive runs with no result above champion (no HOLD-above-0.820 or KEEP).
3. **Hard cap:** 12 experiments in one night (matches the `/regeval-run` walking-away rule).
4. Per-candidate 8-min hard kill (inherited from the runner).
5. Nightly wall-clock ≥ 60 min.

The loop records *which* condition stopped it in the morning report.

## Forbidden actions (the loop refuses these)

- **Inventing candidates not in the queue** (no fishing — this is Framing 1).
- **Overwriting `scaffolds/current.md`** unattended. The champion is only ever promoted by a human after reviewing a `KEEP-confirmed` morning report. The loop stages, it never crowns.
- **Re-grading a prior experiment's outputs** to find a better κ.
- **Auto-committing or pushing.** Writes stay under `Evals/regeval/`; commits are human-approved (ralph.sh pattern).
- **Leaking gold labels** into judge inputs.

## Trifecta-safety contract

Closed world: input is the local, trusted gold set (no untrusted web); egress is Claude-subscription inference only (no API key, no MCP egress, no web fetch); writes are confined to `Evals/regeval/`. Satisfies all three hard-nos — this is why RegEval (not Oracle) is the unattended loop.

## Outputs (every run)

- One row appended to `results.tsv` (machine-parseable) **and** `experiments/log.md` (human narrative).
- One experiment file `experiments/<date>-<NN>-<slug>.md`.
- A morning report (overnight verdicts, current champion, KEEP-confirmed/overfit flags, what stopped the loop, next-to-author) — surfaced in the daily morning brief.

## Related

[[Evals/regeval/regeval-suite]] · [[Evals/regeval/runner]] · [[Evals/regeval/metric]] · [[Evals/regeval/results]] · [[Evals/regeval/experiments/log]] · [[Projects/ralph/brief]]
