# Run protocol — Research synthesis eval suite

Adapted from `Evals/onboarding/protocol.md`. Same author/grader separation rules apply.

## 1. Fix the run inputs

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Model | e.g. `claude-sonnet-5` |
| Skill commit SHA | `git rev-parse HEAD` |
| Runner agent | Identifier of the agent/session executing `/synthesize-research` |
| Grader agent | **Separate** context — must not be the runner |
| Fixtures used | List from `Evals/research-synthesis/inputs/` |

Runner ≠ Grader. Self-graded runs are blocked at `/eval-review`.

## 2. Run the skill

For each fixture in `inputs/`:

1. Copy the fixture content into a fresh session.
2. Invoke `/synthesize-research` with the fixture as input.
3. Capture the full output verbatim — do not edit, summarize, or truncate.
4. Save to: `Evals/research-synthesis/results/transcripts/YYYY-MM-DD_<fixture>_<model>.md`

The transcript must include the full skill output plus any intermediate steps if the skill produces them.

## 3. Grade independently

The grader reads only:
- The captured transcript
- `criteria.md` for each eval
- The fixture file (to verify quote accuracy and evidence traceability)
- The matching `_answer-keys/<fixture>.md` — the ground-truth themes, pain points, named contradictions, and (for the sparse corpus) the "insufficient signal" expectation. Grade the synthesis against this ground truth, not only against the abstract criteria.

The grader does **not** read the skill file or the runner's notes. **Isolation rule:** the runner must never open `_answer-keys/`; a run where it did is void.

Grade each criterion: ✅ / ❌ / ⚠ partial. Partials are not rounded up.

For each ❌, run the introspection loop:
> "Why did the runner produce this output? What in the skill or context led to this decision?"

## 4. Aggregate across fixtures

Run all 7 evals against all 3 fixtures. Report per-fixture results and per-eval pass rate.

Pass target: ≥ 6/7 evals per fixture.

The sparse corpus fixture will likely produce a different pattern than the full-signal fixtures — that's expected and meaningful. Document the differences.

## 5. Log the run

Write `Evals/research-synthesis/results/YYYY-MM-DD_<model>.md` with:
- Header table (model, SHA, runner, grader, fixtures)
- Per-eval ✅/❌ for each fixture
- Per-eval pass rate
- Introspection findings for every ❌
- Recommended skill changes

## 6. Anti-patterns

- **Grading from memory.** Grader must work from the captured transcript only.
- **Skipping the sparse corpus.** It tests the most important failure mode (hallucinated confidence). Always run it.
- **Calling 7/7 "validated."** A single run is a baseline. Re-run on model upgrades.
- **Skipping introspection on ❌.** A failure without a "why" is half a result.
