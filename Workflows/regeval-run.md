# Workflow — RegEval experiment run

**Trigger:** `/regeval-run <scaffold-name>` — one autoresearch experiment iteration
**Owner:** Lucius Fox
**Canonical spec:** [`Evals/regeval/runner.md`](../Evals/regeval/runner.md) — this file is the routing entry; the runner spec is the source of truth.

---

## Shape of one run

1. **Preconditions** — gold dataset ≥ 30 items, champion scaffold exists, candidate variant exists, session budget not exceeded. Refuse on any miss.
2. **Experiment file** — created from `Evals/regeval/experiments/_template.md` with hypothesis, scaffold delta, wall-clock start.
3. **Run against gold** — candidate scaffold over every `gold.jsonl` item; raw outputs recorded.
4. **Score** — κ, TPR, TNR, abstention rate, per-class κ, N, 95% CI per `Evals/regeval/metric.md`. Kill at 8 min wall-clock.
5. **Verdict** — the metric is the reviewer: KEEP (κ ≥ 0.80, CI-lower ≥ 0.70, abstention < 50%) / HOLD / DISCARD / FAIL.
6. **Log** — one immutable line appended to `Evals/regeval/experiments/log.md`; budget updated in `budget.md`.

## Relationship to the Ralph loop

`Projects/ralph/ralph.sh` is the **outer** build loop (story-level, from `prd.json`). `/regeval-run` is the **inner** experiment loop that cycles scaffold variants once the harness exists. Ralph invokes stories; stories invoke experiments.

## Related

[[Evals/regeval/regeval-suite]] · [[Evals/regeval/runner]] · [[Projects/ralph/brief]] · [[Agents/Gotham/Computer/lucius-fox]]
