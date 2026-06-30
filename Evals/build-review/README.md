# Eval suite — build-review (meta-eval)

Tests that the `/build-review` gate actually catches the build flaws that make an artifact unsafe to wire into the flagship or ship — and that it does **not** block a clean, runnable artifact. `/build-review` is the gate that stands between a built artifact (MCP, skill, eval scaffold, code module) and being wired into the flagship project or claimed in a public artifact. If the gate is blind, broken or never-run builds ship as "Pass." This suite calibrates the gate itself.

It is the sibling of the `prd-readiness` meta-eval: same planted-flaw method, same isolation rule, applied to the build gate (the implementation) instead of the readiness gate (the spec). It closes the build-side hole in the OS's eval coverage — `prd-readiness` grades whether the spec is handoff-ready; this grades whether the gate that reviews the implementation is trustworthy.

## How it works (planted-flaw method)

Each fixture in `inputs/` is a realistic build-review packet (a short spec + a description of the built module) with **known planted flaws**, documented in a matching answer key under `_answer-keys/`. The runner executes `/build-review <fixture>` **without ever reading the answer key**. The grader compares the gate output against the key.

**Isolation rule (hard):** the runner must not read anything in `_answer-keys/`. A run where the runner opened an answer key is void. The grader reads the answer key, the fixture, and the captured gate output — nothing else.

One fixture is deliberately **clean** (runnable, no planted flaws). It measures false positives: a gate that blocks everything is as useless as one that passes everything.

## Evals

| Eval | Tests for | Applies to | Bucket |
|---|---|---|---|
| 01-verdict-correct | Gate verdict (Pass / Conditional Pass / Block) matches the key's expected verdict and follows the skill's own decision rules | all fixtures | bad |
| 02-no-hallucinated-issues | Every issue reported points at a genuine build flaw; no check marked ❌ on an aspect that is actually sound | all fixtures | bad |
| 03-clean-not-blocked | The clean control gets Pass — no fabricated issues, no demanding abstraction the artifact doesn't need | clean fixture | bad |
| 04-unrun-or-silent-failure-blocked | A never-run artifact OR a silent-failure catch-all forces Block — the precondition and the worst anti-pattern are non-negotiable | flawed fixture | bad |

All four evals are `bad`-bucket per `Evals/severity-taxonomy.md`: a gate that returns a wrong verdict, invents issues, blocks clean work, or waves through a never-run/silent-failure build is untrustworthy, not merely imperfect.

## Fixtures

| Fixture | Scenario | Run status | Planted flaws |
|---|---|---|---|
| `inputs/clean-build.md` | Slack-digest MCP tool, run with sample output | Run ≥ 1 time, recorded | 0 — false-positive control |
| `inputs/flawed-build.md` | CSV-ingest module for an eval scaffold | Author states NOT run | 4 (see key) |

## Pass-rate target

- **Clean fixture** (evals 01, 02, 03): all 3 pass. Eval 03 failing is a P0 finding on its own — the gate generates noise and the team learns to ignore it.
- **flawed-build** (evals 01, 02, 04): all 3 pass; eval 04 here means *the not-run precondition OR the silent-failure catch-all forced a Block*.
- Suite is citable only if no ❌ on eval 01 (verdict correctness) across any fixture.

## Run protocol

See `protocol.md` (adapts `Evals/prd-readiness/protocol.md`). In short: runner (separate context) runs `/build-review <fixture>` and captures the verbatim gate output (spec under test, six-check scorecard, verdict, required edits); grader (separate context) reads only transcript + fixture + answer key + each `criteria.md`; grade ✅/❌/⚠ (no rounding up); introspect every ❌; log to `results/` and `Evals/run-log.md`.

## Maintenance

- When `/build-review`'s SKILL.md or `_Registry/reviewer-verdict-schema.md` changes, `/eval-ci register build-review <file>` (mapped in `Evals/_ci-map.md`).
- Refresh fixtures occasionally — a memorized fixture is a saturated fixture.
