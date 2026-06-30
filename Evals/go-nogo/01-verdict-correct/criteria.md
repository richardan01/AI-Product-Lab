# Pass criteria — Verdict correct

**Severity bucket:** `bad` (a wrong go/no-go verdict ships a broken launch or blocks a ready one).
**Applies to:** all fixtures.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

The gate's final verdict must match the answer key's expected verdict and follow the skill's own decision rules and the severity taxonomy (all gates 🟢 → GO; any 🔴 → NO-GO; 0 🔴 and ≥3 🟡 → NO-GO; 0 🔴 and 1–2 🟡 → CONDITIONAL GO).

## Criteria (binary)

1. ✅ / ❌ The gate emits exactly one final verdict: GO, NO-GO, or CONDITIONAL GO.
2. ✅ / ❌ The verdict matches the key's expected verdict. (Clean fixture → GO. Flawed fixture → NO-GO.)
3. ✅ / ❌ The verdict is consistent with the gate's own scorecard: if any gate is 🔴, the verdict is NO-GO (not CONDITIONAL GO, not GO); if ≥3 gates are 🟡 with no 🔴, the verdict is NO-GO; if 0 🔴 and 0 🟡, it is GO.

## Failure modes this catches

- Gate clears a launch that is not ship-ready (false negative — ships a broken launch).
- Gate no-gos a launch-ready packet (false positive — blocks good work; see also eval 03).
- Verdict contradicts the scorecard (e.g., a 🔴 gate but a CONDITIONAL GO verdict — see eval 04).
