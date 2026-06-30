# Pass criteria — Verdict correct

**Severity bucket:** `bad` (a wrong readiness verdict ships a broken spec or blocks good work).
**Applies to:** all fixtures.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

The gate's final verdict must match the answer key's expected verdict and follow the skill's own decision rules (all applicable gates pass → READY; any fail → NOT READY; minor gaps only → CONDITIONAL).

## Criteria (binary)

1. ✅ / ❌ The gate emits exactly one final verdict: READY, NOT READY, or CONDITIONAL.
2. ✅ / ❌ The verdict matches the key's expected verdict. (Clean fixture → READY, or CONDITIONAL on the single owned+dated open question only. Flawed fixtures → NOT READY.)
3. ✅ / ❌ The verdict is consistent with the gate's own scorecard: if any applicable gate is marked Fail, the verdict is NOT READY (not CONDITIONAL); if zero gates Fail, it is not NOT READY.

## Failure modes this catches

- Gate clears a PRD that is not handoff-ready (false negative — ships a broken spec).
- Gate flunks a handoff-ready PRD (false positive — blocks good work; see also eval 04).
- Verdict contradicts the scorecard (e.g., a Fail gate but a CONDITIONAL verdict).
