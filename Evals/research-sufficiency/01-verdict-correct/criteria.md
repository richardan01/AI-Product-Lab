# Pass criteria — Verdict correct

**Severity bucket:** `bad` (a wrong sufficiency verdict feeds a confident decision on thin evidence, or blocks a decision-ready read).
**Applies to:** all fixtures.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

The gate's final verdict must match the answer key's expected verdict and follow the skill's own decision rules (all gates pass → SUFFICIENT; any fail → INSUFFICIENT; most pass with minor gaps → CONDITIONAL).

## Criteria (binary)

1. ✅ / ❌ The gate emits exactly one final verdict: SUFFICIENT, INSUFFICIENT, or CONDITIONAL.
2. ✅ / ❌ The verdict matches the key's expected verdict. (Sufficient fixture → SUFFICIENT, or CONDITIONAL on the single acknowledged causality gap only. Insufficient fixture → INSUFFICIENT.)
3. ✅ / ❌ The verdict is consistent with the gate's own scorecard: if any gate is marked Fail, the verdict is INSUFFICIENT (not CONDITIONAL); if zero gates Fail, it is not INSUFFICIENT.

## Failure modes this catches

- Gate clears research that is not decision-ready (false negative — feeds a confident decision on thin evidence).
- Gate flunks decision-ready research (false positive — blocks good work; see also eval 03).
- Verdict contradicts the scorecard (e.g., a Fail gate but a CONDITIONAL verdict).
