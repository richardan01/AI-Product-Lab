# RegEval autoresearch — per-candidate judging procedure

**Voice:** Lucius Fox. This procedure is executed by a headless `claude` session that `regeval-loop.sh` spawns **once per candidate**, in a fresh context. You are the judging brain for ONE candidate; the bash driver owns the queue, the budget, and the stop conditions.

**Read [research-goal.md](research-goal.md) first** — its Harness, Held-out verify, and Forbidden-actions sections are binding. The hard ones: gold labels are stripped from judge inputs; you never overwrite `current.md`; you never commit.

You are given one input: **`SLUG`** (the candidate to run). If `SLUG` is missing, stop.

## Procedure

### 1. Load the candidate
Read `scaffolds/candidates/<SLUG>.md`. Its full text **is the judge system prompt**. If the file is missing, write a `skip` status (step 6) and stop.

### 2. Judge the tuning set via subagents
Judge every item in `inputs/gold.jsonl` (N=100).

- **Batch 10 items per subagent**, ~10 subagents, spawned in parallel.
- Each subagent's system prompt = the candidate scaffold text verbatim.
- Each subagent's user message = its 10 items, **`input` field only** — `gold_label` and `gold_rationale` MUST be removed. Add: *"Classify each item independently. Do not let one item's classification influence another's."*
- Each subagent returns **strict JSONL**, one line per item: `{"id": "reg-00NN", "pred": "compliant|non-compliant|unclear"}` — nothing else.

Concatenate all subagent outputs into `experiments/.preds/<DATE>-<SLUG>.jsonl` (create `.preds/` if absent). Verify you have ~100 lines; missing items are tolerated (score.py reports coverage) but flag if < 90.

### 3. Score the tuning run (no API key)
```
python3 score.py --slug <SLUG> --pred experiments/.preds/<DATE>-<SLUG>.jsonl \
  --mode tuning --parent current --harness subagent
```
This writes the experiment file, appends `log.md` and `results.tsv`, and prints a `RESULT verdict=… kappa=…` line. Capture it.

### 4. Held-out verify — ONLY if verdict starts with `KEEP`
> ⚠️ **CORRECTED 2026-06-28.** `inputs/gold_expansion.jsonl` is **DEPRECATED** — it was a duplicate
> slice of the tuning set, not a held-out set (FM-11). Use **`inputs/heldout_v2.jsonl`** (genuine
> net-new, 20 unseen regimes) and the **binary** scorer. The task is now binary — see
> [[Evals/regeval/discovery-pass-2026-06-28]]. The steps below are kept for loop structure; swap the
> gold path to `inputs/heldout_v2.jsonl` and add `--binary`.

If (and only if) the tuning verdict is `KEEP`, judge the held-out set the same way:
- Judge `inputs/heldout_v2.jsonl` (N=36, was `gold_expansion.jsonl` — deprecated) via subagents (same batching, same label-stripping).
- Write `experiments/.preds/<DATE>-<SLUG>-holdout.jsonl`.
- Score it against the held-out gold:
```
python3 score.py --slug <SLUG> --pred experiments/.preds/<DATE>-<SLUG>-holdout.jsonl \
  --gold inputs/gold_expansion.jsonl --mode holdout
```
- `HOLDOUT-PASS` (κ ≥ 0.70 on held-out) → this is a **KEEP-confirmed** candidate.
- `HOLDOUT-FAIL` → **KEEP-overfit-flag**: it won the tuning set but not held-out. Do not treat as a real KEEP.

If the tuning verdict is not KEEP, skip this step entirely.

### 5. NEVER promote
Do **not** copy the candidate over `scaffolds/current.md`. Do **not** `git commit` or `git add`. Promotion is a human decision made after reading the morning report. You stage; you never crown.

### 6. Write the status line
Append one line to `experiments/.loop-status` (create if absent), tab-separated, for the bash driver to read:
```
<DATE>\t<SLUG>\t<final_status>\tkappa=<x.xxx>\tholdout=<PASS|FAIL|NA>
```
where `<final_status>` is one of: `KEEP-confirmed`, `KEEP-overfit-flag`, `HOLD`, `DISCARD`, `FAIL`, `skip`.

Then stop. The driver picks the next candidate.

## Honesty notes
- The subagent harness batches 10/context — κ is **comparable-with-caveat**, not strictly comparable to a one-call-per-item API run. score.py records this in the note column. Do not claim strict comparability.
- If you cannot spawn subagents or the scaffold is malformed, write a `FAIL` status with a one-line reason rather than guessing labels.
