# Eval suite — prd-readiness (meta-eval)

Tests that the `/prd-readiness` gate actually catches the gaps that make a PRD unsafe to hand to engineering — and that it does **not** flunk a handoff-ready PRD. `/prd-readiness` is the gate that stands between a PRD and an engineering handoff (and between a PRD and `/add-task` extraction). If the gate is blind, broken specs ship as "READY." This suite calibrates the gate itself.

It is the sibling of the `peer-review` meta-eval: same planted-flaw method, same isolation rule, applied to the readiness gate instead of the reviewer gate. It closes the biggest hole in the OS's eval coverage — until now the quality gates themselves were ungraded.

## How it works (planted-flaw method)

Each fixture in `inputs/` is a realistic PRD with **known planted gaps**, documented in a matching answer key under `_answer-keys/`. The runner executes `/prd-readiness <fixture>` **without ever reading the answer key**. The grader compares the gate output against the key.

**Isolation rule (hard):** the runner must not read anything in `_answer-keys/`. A run where the runner opened an answer key is void. The grader reads the answer key, the fixture, and the captured gate output — nothing else.

One fixture is deliberately **clean** (handoff-ready, no planted gaps). It measures false positives: a gate that flunks everything is as useless as one that clears everything.

## Evals

| Eval | Tests for | Applies to | Bucket |
|---|---|---|---|
| 01-verdict-correct | Gate verdict (READY / NOT READY / CONDITIONAL) matches the key's expected verdict and follows the skill's own decision rules | all fixtures | bad |
| 02-no-hallucinated-gaps | Every gap reported points at a genuinely missing/weak element; no gate marked Fail on a section that is actually complete | all fixtures | bad |
| 03-ai-gates-applied-when-ai-feature | AI-specific gates are applied **iff** the PRD is an AI feature — applied and scored on the AI fixture; **not** applied on the standard fixture | both flawed fixtures | bad |
| 04-clean-prd-not-flunked | The clean control gets READY (or CONDITIONAL with zero Fail gates) — no fabricated blockers | clean fixture | bad |

All four evals are `bad`-bucket per `Evals/severity-taxonomy.md`: a gate that returns a wrong verdict, invents gaps, mis-applies the AI gates, or flunks clean work is untrustworthy, not merely imperfect.

## Fixtures

| Fixture | Scenario | PRD type | Planted gaps |
|---|---|---|---|
| `inputs/clean-ai-feature-prd.md` | AI reply-suggestion feature, handoff-ready | AI-feature | 0 — false-positive control |
| `inputs/flawed-standard-prd.md` | Bulk-export feature, headed to engineering | Standard | 4 (see key) |
| `inputs/flawed-ai-feature-prd.md` | AI ticket-triage feature | AI-feature | 4, incl. AI-specific (see key) |

## Pass-rate target

- **Clean fixture** (evals 01, 02, 04): all 3 pass. Eval 04 failing is a P0 finding on its own — the gate generates noise.
- **flawed-standard** (evals 01, 02, 03): all 3 pass; eval 03 here means *AI gates were NOT applied* to a non-AI PRD.
- **flawed-ai-feature** (evals 01, 02, 03): all 3 pass; eval 03 here means *AI gates WERE applied and the AI-specific gaps were caught*.
- Suite is citable only if no ❌ on eval 01 (verdict correctness) across any fixture.

## Run protocol

See `protocol.md` (adapts `Evals/onboarding/protocol.md`). In short: runner (separate context) runs `/prd-readiness <fixture>` and captures the verbatim gate output; grader (separate context) reads only transcript + fixture + answer key + each `criteria.md`; grade ✅/❌/⚠ (no rounding up); introspect every ❌; log to `results/` and `Evals/run-log.md`.

## Maintenance

- When `/prd-readiness`'s SKILL.md or `Templates/prd.md` / `Templates/prd-ai-feature.md` changes, `/eval-ci register prd-readiness <file>` (mapped in `Evals/_ci-map.md`).
- Refresh fixtures occasionally — a memorized fixture is a saturated fixture.
