# Eval suite — research-sufficiency (meta-eval)

Tests that the `/research-sufficiency` gate actually catches the gaps that make a research summary unsafe to feed into a decision — and that it does **not** flunk decision-ready research. `/research-sufficiency` is the gate that stands between research output and a downstream decision (`/business-case`, `/prioritize`, `/prd`). If the gate is blind, thin or stale research feeds a confident decision as "SUFFICIENT." This suite calibrates the gate itself.

It is the sibling of the `prd-readiness` and `peer-review` meta-evals: same planted-flaw method, same isolation rule, applied to the decision-readiness gate instead of the handoff or reviewer gate. It closes a coverage hole — until now the research-sufficiency gate itself was ungraded.

## How it works (planted-flaw method)

Each fixture in `inputs/` is a realistic research summary with **known planted gaps** (or none, for the control), documented in a matching answer key under `_answer-keys/`. The runner executes `/research-sufficiency <fixture>` **without ever reading the answer key**. The grader compares the gate output against the key.

**Isolation rule (hard):** the runner must not read anything in `_answer-keys/`. A run where the runner opened an answer key is void. The grader reads the answer key, the fixture, and the captured gate output — nothing else.

One fixture is deliberately **clean** (decision-ready, no planted gaps). It measures false positives: a gate that flunks everything is as useless as one that clears everything.

## Evals

| Eval | Tests for | Applies to | Bucket |
|---|---|---|---|
| 01-verdict-correct | Gate verdict (SUFFICIENT / INSUFFICIENT / CONDITIONAL) matches the key's expected verdict and follows the skill's own decision rules | all fixtures | bad |
| 02-no-hallucinated-gaps | Every gap reported points at a genuinely missing/weak element; no gate marked Fail on a section that is actually complete | all fixtures | bad |
| 03-clean-not-flunked | The decision-ready control gets SUFFICIENT (or CONDITIONAL with zero Fail gates) — no fabricated blockers | sufficient fixture | bad |
| 04-insufficiency-detected | The thin / single-source / no-confidence / overclaiming research gets INSUFFICIENT — never cleared as SUFFICIENT | insufficient fixture | bad |

All four evals are `bad`-bucket per `Evals/severity-taxonomy.md`: a gate that returns a wrong verdict, invents gaps, flunks clean research, or clears thin research is untrustworthy, not merely imperfect.

## Fixtures

| Fixture | Scenario | Research type | Planted gaps |
|---|---|---|---|
| `inputs/sufficient-research.md` | SMB merchant churn drivers, decision-ready | Decision-input | 0 — false-positive control |
| `inputs/insufficient-research.md` | Loyalty/rewards program build, single stale vendor source | Decision-input | 5 (see key) |

## Pass-rate target

- **Sufficient fixture** (evals 01, 02, 03): all 3 pass. Eval 03 failing is a P0 finding on its own — the gate generates noise.
- **insufficient** (evals 01, 02, 04): all 3 pass; eval 04 here means *the thin, single-source, overclaiming research was marked INSUFFICIENT, not cleared*.
- Suite is citable only if no ❌ on eval 01 (verdict correctness) across any fixture.

## Run protocol

See `protocol.md` (adapts `Evals/onboarding/protocol.md`). In short: runner (separate context) runs `/research-sufficiency <fixture>` and captures the verbatim gate output; grader (separate context) reads only transcript + fixture + answer key + each `criteria.md`; grade ✅/❌/⚠ (no rounding up); introspect every ❌; log to `results/` and `Evals/run-log.md`.

## Maintenance

- When `/research-sufficiency`'s SKILL.md changes, `/eval-ci register research-sufficiency <file>` (mapped in `Evals/_ci-map.md`).
- Refresh fixtures occasionally — a memorized fixture is a saturated fixture.
