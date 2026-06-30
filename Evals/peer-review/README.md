# Eval suite — peer-review (meta-eval)

Tests that the `/peer-review` skill actually catches flaws. Every other artifact in the OS passes through this gate — if the reviewer is blind, every downstream "PASS" is noise. This suite calibrates the gate itself.

## Why this suite exists

`/peer-review` is the default reviewer gate for all personas and all public artifacts. But nothing previously measured whether its reviews are *accurate*: does it catch the blockers a competent reviewer would catch, does it invent problems that aren't there, and does its verdict follow its own rubric? This is the first decision-quality eval in the OS — it grades the reviewer's judgment, not an artifact's formatting.

## How it works (planted-flaw method)

Each fixture in `inputs/` is a realistic artifact with **known planted flaws**, documented in a matching answer key under `_answer-keys/`. The runner executes `/peer-review` on the fixture **without ever reading the answer key**. The grader then compares the review output against the key.

**Isolation rule (hard):** the runner must not read anything in `_answer-keys/`. A run where the runner opened an answer key is void. The grader reads the answer key, the fixture, and the captured review output — nothing else.

One fixture is deliberately **clean** (no planted flaws). It exists to measure false positives: a reviewer that flunks everything is as useless as one that passes everything.

## Evals

| Eval | Tests for | Applies to |
|---|---|---|
| 01-planted-blockers-caught | Every Must-Fix-severity planted flaw is found (recall) | flawed fixtures |
| 02-no-hallucinated-findings | No findings that point at text/problems that don't exist (precision) | all fixtures |
| 03-verdict-matches-rubric | Verdict follows the skill's own CLEARED/CONDITIONAL/NEEDS REVISION rules and matches the key's expected verdict | all fixtures |
| 04-clean-artifact-not-flunked | The clean control gets CLEARED or CONDITIONAL with zero Must Fix items | clean fixture |
| 05-fix-checklist-actionable | Every Must/Should Fix item names a location and a concrete change | flawed fixtures |

## Fixtures

| Fixture | Scenario | Planted flaws |
|---|---|---|
| `inputs/prd-activation-checkout.md` | PRD for a checkout-activation feature, headed for engineering handoff | 6 (see key) |
| `inputs/synthesis-support-tickets.md` | Research synthesis from a support-ticket study | 5 (see key) |
| `inputs/weekly-update-clean.md` | Tight weekly update | 0 — false-positive control |

## Pass-rate target

- **Flawed fixtures** (4 applicable evals: 01, 02, 03, 05): ≥ 3 of 4 pass, and no ❌ on eval 01 — a reviewer that misses planted blockers fails the suite regardless of other scores.
- **Clean fixture** (3 applicable evals: 02, 03, 04): all 3 pass. Eval 04 failing is a P0 finding on its own — it means the gate generates noise.

## Run protocol

Follow `Evals/onboarding/protocol.md` adapted for this suite:

1. Runner (separate context) executes `/peer-review <fixture>` for each fixture and captures the full review output verbatim to `results/transcripts/YYYY-MM-DD_<fixture>_<model>.md`. Runner never opens `_answer-keys/`.
2. Grader (separate context) reads only: the transcript, the fixture, the matching answer key, and each eval's `criteria.md`.
3. Grade ✅ / ❌ / ⚠ partial. Partials are not rounded up.
4. For each ❌, run the introspection loop and capture the harness bug.
5. Log the run in `results/YYYY-MM-DD_<model>.md` and update `Evals/run-log.md`.

## Maintenance

- When `/peer-review`'s SKILL.md or the verdict schema changes, `/eval-ci register peer-review <file>` (mapped in `Evals/_ci-map.md`).
- Refresh fixtures occasionally: a memorized fixture is a saturated fixture. Decision records graded at `/retro` step 3b (expected vs. actual outcomes) are the seed corpus for harder, real-world fixtures.
