# Run protocol — build-review meta-eval

Adapts `Evals/prd-readiness/protocol.md` for the planted-flaw method. Author/grader separation is enforced architecturally via the `eval-runner` and `eval-grader` sub-agents.

## Steps

1. **Pin run inputs.** Model ID, `git rev-parse HEAD` for the commit SHA, the two fixtures, the four evals.
2. **Runner (isolated context), one per fixture.** The `eval-runner` sub-agent executes `/build-review <fixture>` and captures the **verbatim** gate output (spec under test, full six-check scorecard, verdict, required edits) to `results/transcripts/YYYY-MM-DD_<fixture>_<model>.md`.
   - **Hard isolation:** the runner must not read anything under `_answer-keys/`. A run where the runner opened an answer key is **void**. The runner attests no answer-key access in its return.
3. **Grader (isolated context), per (transcript × eval) pair.** The `eval-grader` sub-agent reads only: the transcript, the fixture, the matching `_answer-keys/<fixture>.md`, and the eval's `criteria.md`. It returns structured JSON: `{"eval_id", "fixture", "verdict": pass|fail|partial, "evidence"}`. Partials are not rounded up.
4. **Aggregate** per-eval ✅/❌/⚠ across fixtures against the pass-rate target in `README.md`.
5. **Introspection loop** on every ❌: show the runner its output + the missed criterion, ask *why*, capture the harness bug (a confusing line in `build-review/SKILL.md` or the precondition/anti-pattern lists), and propose the fix.
6. **Log** the run to `results/YYYY-MM-DD_<model>.md` and append a summary row to `Evals/run-log.md`.
7. **Clear CI** via `/eval-ci clear build-review`.

## Map each fixture to its applicable evals

| Fixture | Evals to grade |
|---|---|
| `clean-build.md` | 01, 02, 03 |
| `flawed-build.md` | 01, 02, 04 (not-run precondition AND silent-failure catch-all must force Block) |

## Citability

Citable only if no ❌ on eval 01 (verdict correctness) across any fixture, and the clean control passes eval 03. Otherwise NOT CITABLE — fix the harness and re-run.
