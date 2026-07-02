---
name: judge-calibration
description: Calibrate an LLM-as-judge for a specific eval against human-labeled examples. Splits labeled data into train/dev/test, iterates the judge prompt until TPR ≥ 0.9 AND TNR ≥ 0.9 on dev, runs a final unbiased check on test, and writes a calibration report. Trigger on "calibrate the judge for <eval>", "validate this judge prompt", "run TPR/TNR check", or "is the judge ready to deploy".
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

_This skill has no model pin of its own — it documents a default judge model for the sub-invocations it drives; it does not change the invoking session's model._

# /judge-calibration — Validate an LLM-as-judge against human labels

This skill turns an aspirational "TPR/TNR ≥ 0.9" policy into a concrete pass-or-fail check. It implements Hamel & Shankar §5.4–5.5 verbatim: train/dev/test split, iterate on dev, final read on test, deploy only if test thresholds clear.

## When to run
- Before deploying any `judge-prompt.md` in production grading
- Every 90 days for already-deployed judges (re-validation)
- After a Claude model version change (the judge model may have shifted)
- When `/eval-review` flags a judge as "stale > 90 days"

## Inputs
- `<suite>`: e.g. `onboarding`
- `<eval-id>`: e.g. `05-goals-specific-not-generic`

The skill reads:
- `Evals/<suite>/<eval-id>/judge-prompt.md` — the judge prompt to calibrate
- `Evals/<suite>/<eval-id>/criteria.md` — what the judge is grading
- `Evals/<suite>/<eval-id>/_labeled/*.md` — human-labeled examples
- `Evals/<suite>/<eval-id>/calibration-data-plan.md` — labeled corpus plan

## Required corpus
Minimum: **30 Pass + 30 Fail** human-labeled examples. Block if not met — report current counts and what needs collecting.

Each labeled example lives at `Evals/<suite>/<eval-id>/_labeled/<label>_<NNNN>.md` with this header:
```
---
example_id: pass-0001
human_label: pass
labeled_date: YYYY-MM-DD
labeler: <name or "self">
source: <trace_id from _traces/ | synthetic | sample-pass | sample-fail>
notes: <one line — any borderline reasoning>
---
<the verbatim example content the judge would grade>
```

## The procedure

### Step 1: Verify corpus
1. Read `calibration-data-plan.md`. Confirm current counts ≥ 30 Pass and ≥ 30 Fail.
2. If short, output what's missing and stop.

### Step 2: Stratified split (20/40/40)
1. List all labeled examples. Shuffle deterministically using a seed equal to today's date (`YYYYMMDD` as int). This makes runs reproducible.
2. Within each label class (Pass, Fail), split: first 20% → train, next 40% → dev, last 40% → test.
3. Write the split to `Evals/<suite>/<eval-id>/_calibration/<YYYY-MM-DD>_split.json`:
   ```json
   {
     "split_date": "YYYY-MM-DD",
     "seed": YYYYMMDD,
     "train": ["pass-0001", "pass-0002", "fail-0001", ...],
     "dev":   ["pass-0007", ..., "fail-0007", ...],
     "test":  ["pass-0019", ..., "fail-0019", ...]
   }
   ```

### Step 3: Build the few-shot prompt
1. Read the existing `judge-prompt.md`.
2. Replace its few-shot examples with 4–6 examples drawn from the **train** split (balanced Pass/Fail, prefer borderline cases).
3. Save the candidate prompt to `Evals/<suite>/<eval-id>/_calibration/<YYYY-MM-DD>_candidate.md`. Do NOT overwrite `judge-prompt.md` yet.

### Step 4: Run on dev
For each dev example, run the judge prompt (model: same as production target, default `claude-sonnet-5`). Record:
- Predicted verdict (pass/fail)
- Human label
- Judge's stated reasoning
- Latency (optional)

Output a dev results table: `Evals/<suite>/<eval-id>/_calibration/<YYYY-MM-DD>_dev.md`:
```markdown
| example_id | human | judge | match? | judge_reasoning |
|---|---|---|---|---|
| pass-0007 | pass | pass | ✅ | <quote> |
| fail-0008 | fail | pass | ❌ FP | <quote> |
```

Compute:
- TPR = (true positives) / (true positives + false negatives)
- TNR = (true negatives) / (true negatives + false positives)
- 95% Wilson CI on each

### Step 5: Iterate
If TPR < 0.9 OR TNR < 0.9 on dev:
1. Inspect false positives and false negatives. Quote the judge's reasoning.
2. Propose prompt refinements: tighter criteria, additional borderline anchor, more explicit rule.
3. Edit the candidate prompt. Re-run on dev.
4. Cap iterations at 5. If dev still fails after 5, recommend one of: (a) decompose the criterion, (b) add more diverse training examples, (c) upgrade judge model, (d) accept the failure mode is too subjective and revert to human grading.

Record each iteration to `_calibration/<date>_iteration-<N>.md`.

### Step 6: Final test (no peeking)
When dev TPR/TNR ≥ 0.9:
1. Run the **final** candidate prompt on the test split. **Do not iterate on test.** One read only.
2. Compute test TPR, TNR, and 95% CI.
3. If test TPR ≥ 0.9 AND TNR ≥ 0.9 → PASS, ready to deploy.
4. If test TPR or TNR < 0.9 → FAIL (overfit to dev). Recommend more labeled data and another pass; do NOT deploy.

### Step 7: Write the final report
`Evals/<suite>/<eval-id>/_calibration/<YYYY-MM-DD>_final.md`:
```markdown
# Calibration final report — <suite>/<eval-id>

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Judge model | claude-sonnet-5 |
| Corpus size | <pass>/<fail> labeled |
| Split seed | YYYYMMDD |
| Iterations on dev | <n> |

## Dev (final iteration)
- TPR: X.XX (95% CI [a, b])
- TNR: X.XX (95% CI [a, b])

## Test (unbiased)
- TPR: X.XX (95% CI [a, b])
- TNR: X.XX (95% CI [a, b])

## Verdict
✅ PASS — judge deployable
or
❌ FAIL — do not deploy; <reason>

## Deployment metadata for run-log
Use the test TPR/TNR when computing bias-corrected θ̂ in `/evals` runs:
- TPR_test = ...
- TNR_test = ...
- Last calibrated: YYYY-MM-DD
- Re-validate by: YYYY-MM-DD (+90 days)
```

### Step 8: Promote the prompt (only on PASS)
If verdict is PASS:
1. Copy `_calibration/<date>_candidate.md` → `judge-prompt.md` (overwriting old version).
2. Add a header to `judge-prompt.md`:
   ```
   ---
   last_calibrated: YYYY-MM-DD
   judge_model: claude-sonnet-5
   tpr_test: 0.XX
   tnr_test: 0.XX
   revalidate_by: YYYY-MM-DD
   calibration_report: _calibration/<date>_final.md
   ---
   ```
3. Update `calibration-data-plan.md` Status field to `deployed`.

If verdict is FAIL: do NOT promote. Surface what's needed.

## Hard rules
- Test set is read-once. Never iterate on test. If you peek at test during dev and then change the prompt, the split is contaminated — start over with a new shuffle seed.
- Do NOT use sample-pass.md / sample-fail.md from the eval directory as labeled examples. Those are public anchors and may have leaked into the judge prompt as few-shot. Use only `_labeled/` examples.
- Do NOT use train examples as few-shot AND test against them. Train is for prompt construction only.
- If labeled corpus is < 60 (30 Pass + 30 Fail), do not split. Stop and report what's needed.

## Tools
Read, Write, Bash. Bash is used for the actual judge invocations — typically via `claude -p` or equivalent. The user may pass an invocation pattern; default is to print the candidate prompt with each dev/test example interpolated and rely on the parent session to actually call the model.

## Output
The final report file path + one-line verdict.
