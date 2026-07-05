---
name: regeval-run
description: Run one RegEval autoresearch experiment — vary one scaffold element, score against gold, keep or discard. Trigger on "/regeval-run", "regeval experiment", "run a regeval variant". Enforces the 5-min wall-clock budget and writes to experiments/log.md. The metric is the reviewer.
---

# RegEval runner — `/regeval-run <scaffold-name>`

**Voice:** Lucius Fox. Precise, build-grade, terse on success and explicit on failure.

## What this skill does

Runs **one** experiment in the autoresearch loop. One experiment = one variation of one scaffold element. Multiple experiments per session run by re-invoking this skill.

## Preconditions (refuse if any miss)

1. `Evals/regeval/inputs/gold.jsonl` exists and has ≥ 30 labelled items.
2. `Evals/regeval/scaffolds/current.md` exists (the champion).
3. The candidate variant exists at `Evals/regeval/scaffolds/candidates/<name>.md`.
4. The 60-min session budget has not been exceeded (check `budget.md`).

If any precondition fails, stop and surface the gap. Do not improvise.

## Step-by-step

### 1. Start the experiment file
Create `Evals/regeval/experiments/<YYYY-MM-DD-NN>-<slug>.md` from `_template.md`. NN is the day's nth experiment, zero-padded.

Capture upfront:
- **Hypothesis** — one sentence: "Changing X to Y will improve κ because Z."
- **Scaffold delta** — what specifically differs from `current.md` (a diff or a 3-bullet summary).
- **Wall-clock start** — UTC timestamp.

### 2. Run against gold
Execute the candidate scaffold over every item in `gold.jsonl`. Record raw judge outputs into the experiment file under `## Raw outputs` (collapsible).

### 3. Compute κ + diagnostics
Per [metric.md](metric.md): κ, TPR, TNR, abstention rate, per-class κ, N, 95% CI.

If wall-clock exceeds 8 min, **kill the run** and log it as a failed experiment with reason "budget exceeded". Do not extend.

### 4. Verdict (the metric is the reviewer)

| Result | Action |
|---|---|
| κ ≥ 0.80 **and** abstention < 50% **and** CI lower bound ≥ 0.70 | **Keep.** Overwrite `scaffolds/current.md`. Append `KEEP` row to `log.md`. |
| κ ≥ champion's κ but below 0.80 | **Hold.** Do not overwrite. Append `HOLD` row. Useful direction. |
| κ < champion's κ, or suspicious diagnostics | **Discard.** No overwrite. Append `DISCARD` row. |
| Run killed for budget | **Failed.** Append `FAIL` row with reason. |

### 5. Append the one-line log entry

`experiments/log.md` is the compounding artifact. One line per experiment, never edited retroactively:

```
| YYYY-MM-DD | NN | <slug>           | <verdict> | κ=<x.xx> | TPR=<x.xx> TNR=<x.xx> abst=<x.xx> N=<n> | <one-sentence why> |
```

### 6. Update `budget.md`
Record minutes spent. If session total ≥ 60 min, refuse further `/regeval-run` calls in this session.

## Output format

```
## RegEval experiment <date>-<NN> — <slug>

**Verdict:** KEEP / HOLD / DISCARD / FAIL
**κ:** <x.xx> (95% CI [<lo>, <hi>])  vs champion <x.xx>
**Diagnostics:** TPR=<x.xx> · TNR=<x.xx> · abst=<x.xx> · N=<n>
**Wall clock:** <m>:<ss>

**Hypothesis:** <one sentence>
**Scaffold delta:** <bullets>

**Why this verdict (one sentence):** <reason>

**Next experiment suggestion (one line):** <if applicable>
```

## Anti-patterns (the runner refuses these)

- Editing `current.md` directly (only the runner overwrites, only on KEEP)
- Running without an explicit hypothesis (no fishing)
- Re-grading a prior experiment's outputs to "find" a better κ
- Extending past the 8-min hard kill
- Skipping `log.md` append "to clean up later"

## Walking-away rule

After 12 experiments or 60 minutes, this skill refuses further runs in the same session. Karpathy: ~100 experiments while you sleep — yours run while you don't. Come back tomorrow.

## Autonomous loop

This skill runs ONE experiment, hand-driven. The unattended overnight version is the **autoresearch loop**: it runs a human-authored candidate queue while you sleep, scores each, runs a held-out verify on any KEEP, and never promotes the champion on its own.
- [research-goal.md](research-goal.md) — the `program.md`: queue, ruled-out levers, stop conditions, verify policy
- [regeval-autoresearch.md](regeval-autoresearch.md) — per-candidate judging procedure (subagent harness)
- [score.py](score.py) — no-API-key scorer (κ + CI + diagnostics → log.md + results.tsv) · [queue.py](queue.py) — what runs next
- Scheduled task: `~/.claude/scheduled-tasks/myos-regeval-autoresearch/SKILL.md`

## Audit tooling — provenance traces + human-vs-judge (REV-008 / REV-009)

Two offline, no-API-key tools make every verdict auditable after a run. Both
reconstruct from on-disk artifacts (experiment table + gold snapshot + hashed
scaffold); neither calls the judge.

- **Provenance traces** — [provenance.py](provenance.py) builds `traces/<experiment-stem>.jsonl`,
  one record per item (judge vs gold, abstain trigger, scaffold hash + verify flag).
  Schema and usage: [traces/README.md](traces/README.md). This is the regulated-fintech
  differentiator — a verdict you can trace, not just a score.
- **Human-vs-judge CLI** — [judge_vs_human.py](judge_vs_human.py): `replay` streams the
  comparison with κ recomputed live and a **RECONCILES ✓/✗** self-audit against the logged
  κ (the check the Day-60 demo runs); `card` / `summary` for one item / a scoreboard;
  `adjudicate` for a blind human label. Adjudication outcomes persist to
  [inputs/corrections-log.md](inputs/corrections-log.md) (the abstain→human-judgment spine),
  not a separate `cli/adjudications/` dir. A refusal guard blocks quoting a full-set κ over a
  partial/selected-mismatch table.

## References

- [regeval-suite.md](regeval-suite.md) — loop, budget, kill criteria
- [Evals/regeval/metric.md](metric.md) — κ definition
- [judge-calibration skill](../../.claude/skills/judge-calibration/) — judge-alignment methodology
- [Q3 thesis Day-30 signpost](../../Agents/Gotham/thesis-q3-2026.md)
