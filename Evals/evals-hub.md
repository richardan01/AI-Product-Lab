# Evals

This directory contains **offline audit suites** for AI Product Lab. They are not real-time response graders — there are no inline graders that automatically evaluate output as it's produced. This is intentional: grading in the same context window as authoring violates author/grader separation, which the eval protocol enforces as a hard requirement.

---

## Active suites

| Suite | Criteria | What it catches | Pass threshold |
|---|---|---|---|
| [`onboarding/`](onboarding/) | 12 | Placeholder residue, persona-routing bugs, batch-write violations, invented identity, skipped Phase 5/5B, polite-ack-as-authorization | ≥ 10 / 12 per fixture |
| [`research-synthesis/`](research-synthesis/) | 7 | Invented quotes, generic synthesis, missing conflicting signals, unactionable open questions | ≥ 6 / 7 per fixture |
| [`discovery-synthesis/`](discovery-synthesis/) | In progress | Self-grading bias, weak synthesis, missing adversarial cases | κ target defined in suite |
| [`regeval/`](regeval/) | Varies | RegEval scaffold regressions and rubric quality drift | κ ≥ 0.80 |
| [`gate-group/`](gate-group/) | Meta-eval | Gate-pipeline routing and reviewer-group failures | Defined in suite |

_This is the curated primary set. Additional graded suites on disk (peer-review, prd-readiness, memory-consolidation, build-review, go-nogo, research-sufficiency) and the README-only `monitoring/` are in the canonical registry — see [`Evals/index.md`](index.md)._

Each criterion folder contains:
- `criteria.md` — the rubric (pass/fail/partial definitions)
- `sample-pass.md` — anchored passing example
- `sample-fail.md` — anchored failing example
- `judge-prompt.md` — grader prompt (some criteria only)

Each suite has its own named suite hub and a `protocol.md` with the full run procedure.

---

## Run protocol (summary)

Full protocols: [`onboarding/protocol.md`](onboarding/protocol.md) · [`research-synthesis/protocol.md`](research-synthesis/protocol.md)

**Three non-negotiable requirements:**

1. **Fresh context window.** The grader must run in a context that has never seen the output being graded. Never grade in the same session that produced the artifact.
2. **Author/grader separation.** The runner agent and grader agent must be different contexts (different sessions, different model invocations). Self-graded runs are invalid.
3. **Transcript capture.** Evals 02 and 07 (onboarding suite) grade temporal behavior — they require a captured verbatim transcript, not the runner's recollection. Save transcripts to `onboarding/results/transcripts/YYYY-MM-DD_<fixture>_<model>.md`.

**Steps:**
1. Record run inputs: date, model ID, workflow commit SHA (`git rev-parse HEAD`), runner identity, grader identity, fixtures used.
2. Runner executes the workflow against each fixture; captures full transcript.
3. Grader reads transcript + criteria only (not the workflow or OS files).
4. Grader scores each criterion: ✅ pass / ❌ fail / ⚠ partial. Partials are not rounded up.
5. For every ❌: run the introspection loop — "Why did the runner produce this output?" Capture the answer.
6. Log results in `run-log.md` (append-only) and in a dated result file under `<suite>/results/`.

---

## Scoring

| Suite | Total criteria | Pass threshold | Notes |
|---|---|---|---|
| Onboarding | 12 | ≥ 10 / 12 | Onboarding is day-1 UX — bar is strict. A single fixture is a data point; run all three core fixtures. |
| Research-synthesis | 7 | ≥ 6 / 7 | Single fixture acceptable; add corpora that stress your specific research domain. |

A run that scores 9/12 or 5/7 is a regression, not a pass with caveats. Name the failures and fix the harness.

---

## When to run

| Trigger | Suite(s) |
|---|---|
| Model upgrade (new Claude version) | Both suites |
| Onboarding workflow changed | Onboarding suite |
| Research-synthesis workflow changed | Research-synthesis suite |
| 60-day cadence (no other trigger) | Both suites |

A suite that hasn't been run in 60 days is technical debt. The `run-log.md` last-run date is the signal.

---

## Sample run log format

Runs are recorded in [`run-log.md`](run-log.md) (append-only) and as individual result files in `<suite>/results/YYYY-MM-DD_<model>.md`.

Minimum fields per entry:

| Field | Example |
|---|---|
| Date | `2025-01-15` |
| Suite | `onboarding` |
| Model | `claude-3-5-sonnet-20241022` |
| Commit SHA | `a1b2c3d` |
| Fixture | `jordan-lee-profile.md` |
| Score | `11 / 12` |
| Failures | `07-per-step-interactivity ❌` |
| Remediation | `Phase 9 prompt tightened to require explicit per-file confirmation` |

See `run-log.md` for a complete example entry.

---

## Eval authoring conventions

- Every new criterion needs `criteria.md` + `sample-pass.md` + `sample-fail.md` before it is considered gradeable.
- Judgment criteria (those requiring interpretation rather than binary presence/absence) require anchored samples.
- New fixtures must cover at least one failure mode not covered by existing fixtures.
- Do not add criteria that can be checked mechanically (e.g., "file exists") — those belong in CI, not evals.

See `eval-audit-checklist.md` for the P0/P1/P2 audit framework applied before citing any suite as credible.
