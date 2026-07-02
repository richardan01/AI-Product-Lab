# Run protocol — Onboarding eval suite

This protocol exists because evals 02 and 07 grade **temporal behavior** (who confirmed what, when, in what order). Without a captured transcript and an independent grader, the suite is self-graded and not citable.

Follow this protocol every time the suite is run.

## 1. Fix the run inputs

Record before the run starts:

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Model | e.g. `claude-opus-4-8` |
| Workflow commit SHA | `git rev-parse HEAD` against this repo at run time |
| Runner agent | Identifier of the agent or session that will execute the workflow |
| Grader agent | Identifier of the **separate** agent or session that will grade |
| Fixtures used | List from `Evals/onboarding/inputs/` |

The runner and grader must be **different contexts**. Self-graded runs are blocked at review (`/eval-review`).

## 2. Capture the transcript

The runner agent executes `Workflows/interactive-onboarding.md` against each fixture and captures the full session transcript verbatim into a markdown file. Save to:

```
Evals/onboarding/results/transcripts/YYYY-MM-DD_<fixture>_<model>.md
```

The transcript must include:

- Every assistant question and every user reply, in order.
- The order and granularity of file-write operations (one row per write, with filename).
- The Phase 10 verification ✅/❌ row results.
- Any place the user replied with a polite-but-non-explicit acknowledgement (so eval 07 criterion 5 can be graded).

## 3. Grade independently

The grader agent reads only:

- The captured transcript
- `Evals/onboarding/0N-<name>/criteria.md` for each eval
- `Evals/onboarding/0N-<name>/sample-pass.md` and `sample-fail.md` when present
- `Evals/onboarding/_answer-keys/<fixture>.md` — the ground-truth config for that fixture (expected persona routing, the user's stated 30-day outcome verbatim, named stakeholders, privacy exclusions, and which fields must be **deferred** vs. answered). Grade content evals (01, 03, 05, 08, 11) against this ground truth, not only the abstract criteria.

The grader does **not** read the workflow, the runner's reasoning, or any other file from the OS. **Isolation rule:** the runner must never open `_answer-keys/`; a run where it did is void. This isolation is what gives the grade methodological weight.

Grade each criterion as ✅ / ❌ / ⚠ partial. Partials are not rounded up.

For each ❌, run the introspection loop:

> "Why did the runner produce this output? What in the workflow or context led to this decision?"

Capture the answer — it is the harness bug report.

## 4. Aggregate across fixtures

A single fixture is a data point, not a signal. Run every eval against **all three fixtures**:

- `inputs/jordan-lee-profile.md` (Executive operator)
- `inputs/sam-okafor-builder-variant.md` (Builder / AI PM)
- `inputs/riley-park-minimalist.md` (Minimalist, with many deferred fields)

Report per-fixture results and a per-eval pass rate. Compute a 95% confidence interval where N ≥ 30; below that, report the raw count and flag low statistical power.

## 5. Log the run

Write `Evals/onboarding/results/YYYY-MM-DD_<model>.md` with:

- The header table from step 1 (model, commit SHA, runner, grader, fixtures)
- Per-eval ✅/❌ result for each fixture
- Per-eval pass rate (X / N fixtures)
- Introspection findings for every ❌
- Recommended harness fixes (workflow edits, criteria edits, fixture additions)
- A "Negative results" section that names every failure observed — not just successes

## 6. Re-grade if any check is missing

If the run log does not include:

- Captured transcript with author/grader separation
- Per-fixture results across all three fixtures
- Introspection findings for failures
- Model and commit SHA pinned

…then the result is not citable. Re-run with the missing piece in place. This is the bar `/eval-review` enforces.

## Anti-patterns to avoid

- **Cherry-picking the best fixture.** All three fixtures or none.
- **Grading from memory.** The grader must work from the captured transcript only.
- **Skipping introspection.** A ❌ without a "why" is half a result.
- **Calling a 7/7 result "validated."** A single run on a single model is a baseline, not validation. Re-run on model upgrades.
