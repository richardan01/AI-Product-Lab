# Evals

This directory contains **offline audit suites** for AI Product Lab. They are not real-time response graders — there are no inline graders that automatically evaluate output as it's produced. This is intentional: grading in the same context window as authoring violates author/grader separation, which the eval protocol enforces as a hard requirement.

---

## Suites

Two kinds of suite live here:

- **Workflow suites** grade an AI workflow's output.
- **Meta-eval (gate) suites** grade a quality *gate* itself with the planted-flaw method: a fixture with known flaws plus a grader-only answer key; the gate must catch the flaws and must **not** flunk a clean control.

| Suite | Kind | Criteria | What it catches | Pass threshold |
|---|---|---|---|---|
| [`agent-harness/`](agent-harness/) | agentic trajectory | 7 (1+6) | Two-phase agentic eval of a real Claude Code / Codex / chatbot session: task success + tool choice, parameter extraction, error recovery, context retention, efficiency, goal drift | `00` ✅ + no `bad` axis |
| [`onboarding/`](onboarding/) | workflow | 12 | Placeholder residue, persona-routing bugs, batch-write violations, invented identity, polite-ack-as-authorization | ≥ 10 / 12 per fixture |
| [`research-synthesis/`](research-synthesis/) | workflow | 7 | Invented quotes, generic synthesis, missing conflicting signals, unactionable open questions | ≥ 6 / 7 per fixture |
| [`discovery-synthesis/`](discovery-synthesis/) | workflow | in progress | Discovery synthesis structure, evidence retention, and product-insight quality | in progress |
| [`regeval/`](regeval/) | workflow | κ | LLM-as-judge alignment against human gold labels | κ ≥ 0.80 |
| [`peer-review/`](peer-review/) | meta-eval | 5 | Reviewer gate misses a planted blocker, hallucinates a finding, or flunks clean work | ≥ 3 / 4 + clean eval-01 |
| [`prd-readiness/`](prd-readiness/) | meta-eval | 4 | Readiness gate returns a wrong verdict, mis-applies the AI gates, or flunks a clean PRD | no ❌ on eval-01 |
| [`go-nogo/`](go-nogo/) | meta-eval | 4 | Launch gate fails to block on a 🔴, flunks a clean packet, or averages a red away | no ❌ on eval-01 |
| [`research-sufficiency/`](research-sufficiency/) | meta-eval | 4 | Sufficiency gate clears thin/single-source/stale research, or flunks sufficient research | no ❌ on eval-01 |
| [`build-review/`](build-review/) | meta-eval | 4 | Build gate passes a never-run or silent-failure artifact, or blocks a clean build | no ❌ on eval-01 |
| [`gate-group/`](gate-group/) | meta-eval | suite-level | Riddler + Vicki Vale + Ducard gate isolation and schema behavior | re-run pending |
| [`memory-consolidation/`](memory-consolidation/) | workflow | 5 | Faithful memory promotion, deduplication, canonicality, and freshness | ≥ 4 / 5; 01+02 mandatory |
| [`monitoring/`](monitoring/) | online monitor | weekly loop | Samples real artifacts, grades async, and tracks bad/sad rates | weekly |

Each criterion folder contains:
- `criteria.md` — the rubric (pass/fail/partial definitions, with a `bad`/`sad` severity bucket)
- `sample-pass.md` / `sample-fail.md` — anchored examples (workflow suites; judgment criteria)
- `_answer-keys/` — grader-only ground truth per fixture (meta-eval suites)
- `judge-prompt.md` — a calibrated LLM-as-judge prompt (subjective criteria only; e.g. onboarding eval 05)

Each suite has its own README and a `protocol.md` with the full run procedure.

## Cross-cutting

- [`severity-taxonomy.md`](severity-taxonomy.md) — the `bad` (irrecoverable) vs `sad` (recoverable) model + stacking rule that drives every gate verdict.
- [`monitoring/`](monitoring/README.md) — the weekly online-monitoring loop (sample real artifacts → grade async → bucket bad/sad → bad-rate → error analysis). The achievable form of "every response evaluated."
- LLM-as-judge calibration — `/judge-calibration` validates a judge (TPR/TNR ≥ 0.9 on a held-out test split) before it is deployed.
- [`eval-audit-checklist.md`](eval-audit-checklist.md) — the P0/P1/P2 audit applied before citing any result.
- `_ci-map.md` + `_pending-reruns.md` — the regression sentinel: editing a mapped source file blocks `/peer-review` and `/go-nogo` from citing a stale suite until it re-runs.

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
| Meta-eval (gate) suites | 4–5 | no ❌ on eval-01 (verdict) **and** the clean control not flunked | A gate that returns a wrong verdict or flunks clean work is untrustworthy; verdict correctness is the gating criterion. |

A run that scores 9/12 or 5/7 — or a gate that misses the verdict on any fixture — is a regression, not a pass with caveats. Name the failures and fix the harness.

---

## When to run

| Trigger | Suite(s) |
|---|---|
| Model upgrade (new Claude version) | All suites |
| A mapped source file changed (see `_ci-map.md`) | The mapped suite (auto-registered in `_pending-reruns.md`) |
| Onboarding / synthesis workflow changed | Onboarding / research-synthesis |
| A gate skill changed (`peer-review`, `prd-readiness`, `go-nogo`, `research-sufficiency`, `build-review`) | That gate's meta-eval suite |
| Weekly | The `monitoring/` loop (sample real artifacts) |
| 60-day cadence (no other trigger) | All suites |

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
