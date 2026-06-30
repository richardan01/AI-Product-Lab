# Eval suite — research-synthesis

Tests that the `/synthesize-research` skill produces synthesis grounded in the actual input corpus — not generic AI output that would look the same regardless of what research was ingested.

## Why this suite exists

The `/synthesize-research` skill is one of the highest-leverage daily tools in the OS: it turns raw interview notes into themes, pain points, and implications. The failure modes are quiet — hallucinated quotes, invented themes, conflated signals, generic implications that don't reflect the specific corpus. Without evals, these failures compound silently into downstream decisions.

## Suites and evals

| Eval | Tests for |
|---|---|
| 01-themes-grounded-in-evidence | Every theme cites evidence from the corpus |
| 02-no-invented-quotes | No quotes or attributed statements not in the source notes |
| 03-pain-points-distinct-from-themes | Pain points are specific problems, not theme labels |
| 04-conflicting-signals-named | Contradictions in the corpus are surfaced, not averaged away |
| 05-use-case-implications-present | Synthesis includes implications for the stated use case |
| 06-open-questions-actionable | Open questions name a next step, not just a topic |
| 07-no-generic-synthesis | Output changes meaningfully if inputs change |

## Pass-rate target

≥ 6/7 evals per fixture. A 7/7 run is healthy but should prompt harder fixture additions.

## Run protocol

Follow `Evals/onboarding/protocol.md` adapted for this suite:

1. Runner executes `/synthesize-research` against each fixture in `inputs/`.
2. Runner captures the full output verbatim in `results/transcripts/YYYY-MM-DD_<fixture>_<model>.md`.
3. Grader (separate context) reads only the transcript + criteria files. Does **not** read the skill or the runner's reasoning.
4. Grade each criterion ✅ / ❌ / ⚠ partial. Partials are not rounded up.
5. For each ❌, run the introspection loop: show the model its output, the missed criterion, and ask "Why did you produce this?"
6. Log run in `results/YYYY-MM-DD_<model>.md`.

## Run this suite

```text
/evals research-synthesis
```

Or manually: run `/synthesize-research` against a fixture, capture output, grade against criteria.

## Fixtures

| Fixture | Scenario | Personas |
|---|---|---|
| `inputs/activation-funnel-interviews.md` | 4 discovery interviews for a B2B activation funnel feature | New user, power user, ops manager, CSM |
| `inputs/ai-assistant-mixed-signals.md` | 6 interviews with conflicting signals about AI trust | Enthusiasts, skeptics, neutral |
| `inputs/sparse-corpus.md` | 3 short interviews with thin signal | Tests hallucination under sparse input |

## Last run

See `results/` for dated run logs.
