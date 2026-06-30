# Pass criteria — Clean research not flunked

**Severity bucket:** `bad` (a gate that flunks decision-ready research is noise; the team learns to ignore it).
**Applies to:** sufficient fixture (`sufficient-research.md`) only — the false-positive control.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

The decision-ready research summary must clear the gate. A gate that flunks everything is as useless as one that passes everything; this eval is the precision counterpart to eval 04's recall.

## Criteria (binary)

1. ✅ / ❌ Verdict is SUFFICIENT (or CONDITIONAL citing only the single acknowledged correlation-vs-causation gap) — not INSUFFICIENT.
2. ✅ / ❌ Zero gates marked Fail across all 7 gates.
3. ✅ / ❌ No fabricated blocking gap (e.g., claiming no confidence levels when each finding F1–F4 carries one; claiming a single source when three distinct source types are cited; demanding causal proof the summary already names as a known gap and defers to an A/B).

## Failure modes this catches

- Gate demands evidence that is already present (confidence levels, source diversity, gaps section).
- Gate manufactures a blocking gap to justify an INSUFFICIENT verdict.
- Gate treats an already-acknowledged, correctly-scoped limitation as a blocker.
