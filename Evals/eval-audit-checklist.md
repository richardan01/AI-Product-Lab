# Eval audit checklist

Modeled on the `eval-audit` skill from `hamelsmu/evals-skills`, scoped to this repo's suites (`onboarding/`, `research-synthesis/`, and any new suite added under `Evals/`).

Run this checklist:
- Before adding a new suite to the repo.
- Before citing a result externally (interview, blog post, weekly update).
- After any model upgrade, against every suite, before re-running.

Each item is a binary check. A suite with any **P0** fail is not citable. **P1** fails should be opened as `Tasks/active.md` items. **P2** fails are parking-lot.

## P0 — methodological soundness (citation blockers)

- [ ] **Author / grader separation.** Runner agent and grader agent are different contexts. No self-grading.
- [ ] **Transcript captured** for every eval that grades temporal behavior (e.g., order of confirmations, batch-write detection). The grader works from the transcript, not the runner's memory.
- [ ] **Model + commit SHA pinned** in the run log header. Both the model ID (e.g., `claude-opus-4-7`) and `git rev-parse HEAD`.
- [ ] **All applicable fixtures run.** No cherry-picking. Per-fixture results reported separately before any aggregate.
- [ ] **Negative results visible.** Every ❌ named in the log with introspection ("why did the model do this?"). A 7/7 run with no introspection is suspicious — re-read the transcript.
- [ ] **Pass-rate target stated up front.** Not adjusted after seeing results.

## P1 — judgment quality (signal blockers)

- [ ] **Binary criteria.** Each criterion grades PASS / FAIL / PARTIAL, not 1–5 vibes. Partials are not rounded up.
- [ ] **Anchored samples** (`sample-pass.md` + `sample-fail.md`) exist for every criterion that requires judgment (anything beyond regex / file-existence).
- [ ] **Failure modes named in the suite README.** Criteria exist because of observed failures, not theoretical ones. Each failure-mode entry should be traceable to a real run or dry-run.
- [ ] **Fixtures stress distinct failure modes.** No two fixtures grade the same code path. New fixtures justified by an uncovered dimension (see `Evals/onboarding/dimension-grid.md`).
- [ ] **Introspection findings → harness fixes.** Last 3 run logs each generated at least one workflow edit, criterion refinement, or fixture addition. If not, the suite has stopped finding bugs — re-examine.

## P1 — automation readiness (scale blockers)

- [ ] **Judge prompt exists** for criteria you intend to automate. Prompt includes rubric + anchored few-shot + strict JSON output schema.
- [ ] **Judge validated** against ≥ 30 human-labeled examples per criterion. TPR ≥ 0.9 AND TNR ≥ 0.9 before the judge replaces human grading.
- [ ] **Human-label corpus growing.** Every manual run contributes graded transcripts to a labeled pool. Goal: ≥ 100 labels per criterion before claiming "validated."

## P2 — hygiene

- [ ] **Run log filenames follow convention.** `results/YYYY-MM-DD_<model>.md`. Transcripts in `results/transcripts/`.
- [ ] **No suite older than 60 days** without a re-run on the current model. Stale suites are technical debt.
- [ ] **Parking lot maintained.** Known gaps named in the README's "Not yet covered" section. Better to name the gap than to hide it.
- [ ] **Cross-references valid.** README → criteria → samples → fixtures all resolve. No dead links after refactors.

## P2 — methodological extensions

- [ ] **Error taxonomy.** Free-text introspection findings clustered into named failure categories with frequencies over time. (Hamel's `error-analysis` pattern.)
- [ ] **Dimension grid for fixtures.** Coverage gaps visible at a glance; new fixtures generated systematically, not from intuition. (Hamel's `generate-synthetic-data` pattern.)
- [ ] **Confidence intervals** reported where N ≥ 30. Below that, raw counts + a low-power flag.

## How to run this checklist

1. Open the target suite's README and `protocol.md` side by side.
2. Walk the list. For each item, write ✅ / ❌ / N/A with a one-line evidence pointer.
3. Tally P0 fails — if any, mark the suite **not citable** and open `Tasks/active.md` items to fix before next run.
4. File the audit at `Evals/<suite>/audits/YYYY-MM-DD_audit.md` so trends across audits are visible.

## What this checklist deliberately does not cover

- RAG-specific evaluation (no RAG system here yet — see hamelsmu `evaluate-rag` if that changes).
- Custom annotation interfaces (volume too low to justify; see hamelsmu `build-review-interface`).
- Statistical significance testing across runs (premature until labeled corpus ≥ 100).
