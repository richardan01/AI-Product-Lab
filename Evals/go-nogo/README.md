# Eval suite — go-nogo (meta-eval)

Tests that the `/go-nogo` launch gate actually blocks an unsafe launch — and that it does **not** flunk a launch-ready packet. `/go-nogo` is the gate that stands between a launch-readiness packet and "ship it" (and between a packet and the launch-comms send). If the gate is blind, broken launches ship as "GO." This suite calibrates the gate itself.

It is the sibling of the `prd-readiness` and `peer-review` meta-evals: same planted-flaw method, same isolation rule, applied to the launch gate instead of the readiness or reviewer gate. It closes the launch-side hole in the OS's eval coverage — the gate that authorizes a ship was itself ungraded.

## How it works (planted-flaw method)

Each fixture in `inputs/` is a realistic launch-readiness packet (checklist status, UAT/QA sign-off, risk list, comms status, rollback status) with **known planted blockers**, documented in a matching answer key under `_answer-keys/`. The runner executes `/go-nogo <fixture>` **without ever reading the answer key**. The grader compares the gate output against the key.

**Isolation rule (hard):** the runner must not read anything in `_answer-keys/`. A run where the runner opened an answer key is void. The grader reads the answer key, the fixture, and the captured gate output — nothing else.

One fixture is deliberately **clean** (all 6 gates green, launch-ready, no planted blockers). It measures false positives: a gate that no-gos everything is as useless as one that gos everything.

## Evals

| Eval | Tests for | Applies to | Bucket |
|---|---|---|---|
| 01-verdict-correct | Gate verdict (GO / NO-GO / CONDITIONAL GO) matches the key's expected verdict and follows the skill's own decision rules and the severity taxonomy | all fixtures | bad |
| 02-no-hallucinated-blockers | Every blocker reported points at a genuinely red/yellow gate; no gate scored 🔴/🟡 on a gate that is actually green | all fixtures | bad |
| 03-clean-not-flunked | The clean control gets GO — no fabricated 🔴 and no manufactured CONDITIONAL | clean fixture | bad |
| 04-red-risk-blocks-go | Any 🔴 (`bad`) gate forces NO-GO — never CONDITIONAL GO, never GO | flawed fixture | bad |

All four evals are `bad`-bucket per `Evals/severity-taxonomy.md`: a gate that returns a wrong verdict, invents blockers, downgrades a 🔴 to CONDITIONAL, or no-gos clean work is untrustworthy, not merely imperfect.

## Fixtures

| Fixture | Scenario | Gate posture | Planted blockers |
|---|---|---|---|
| `inputs/clean-launch-packet.md` | Bulk-export GA, all checks green | all 6 gates 🟢 | 0 — false-positive control |
| `inputs/flawed-launch-packet.md` | AI reply-suggestions GA, headed to ship | ≥1 🔴, ≥1 🟡 | 3 (see key) |

## Pass-rate target

- **Clean fixture** (evals 01, 02, 03): all 3 pass. Eval 03 failing is a P0 finding on its own — the gate generates noise.
- **flawed fixture** (evals 01, 02, 04): all 3 pass; eval 04 here means *the 🔴 gate forced NO-GO and was not softened to CONDITIONAL GO*.
- Suite is citable only if no ❌ on eval 01 (verdict correctness) across any fixture.

## Run protocol

See `protocol.md` (adapts `Evals/prd-readiness/protocol.md`). In short: runner (separate context) runs `/go-nogo <fixture>` and captures the verbatim gate output; grader (separate context) reads only transcript + fixture + answer key + each `criteria.md`; grade ✅/❌/⚠ (no rounding up); introspect every ❌; log to `results/` and `Evals/run-log.md`.

## Maintenance

- When `/go-nogo`'s SKILL.md or `Evals/severity-taxonomy.md` changes, `/eval-ci register go-nogo <file>` (mapped in `Evals/_ci-map.md`).
- Refresh fixtures occasionally — a memorized fixture is a saturated fixture.
