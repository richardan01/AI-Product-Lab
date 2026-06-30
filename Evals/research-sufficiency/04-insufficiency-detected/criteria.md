# Pass criteria — Insufficiency detected

**Severity bucket:** `bad` (a gate that clears thin, single-source, overclaiming research feeds a confident decision the evidence cannot support).
**Applies to:** insufficient fixture (`insufficient-research.md`) only — the false-negative control.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

The thin / single-source / no-confidence / overclaiming research summary must be marked INSUFFICIENT — never cleared as SUFFICIENT. This is the recall counterpart to eval 03's precision: the gate exists to stop exactly this kind of confidently-recommended build on one stale vendor source.

## Criteria (binary)

1. ✅ / ❌ Verdict is INSUFFICIENT — not SUFFICIENT, and not CONDITIONAL (multiple gates Fail, so the skill's rules require INSUFFICIENT).
2. ✅ / ❌ The gate marks as Fail the genuinely-failing gates per the key: Source diversity (R1, single source), Recency (R2, 2023 data), Confidence levels (R3, none stated), Gaps acknowledged (R5, no limitations section).
3. ✅ / ❌ The gate flags the overclaiming recommendation (R4) — it does not accept a "high-confidence" build commitment on single-source stale signal as actionable.

## Failure modes this catches

- Gate rubber-stamps a confident recommendation without checking the evidence beneath it (clears overclaim).
- Gate counts one vendor whitepaper as adequate source diversity.
- Gate misses that no finding carries a confidence level, or that the market data is years stale.
