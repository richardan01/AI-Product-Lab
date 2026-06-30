# Pass criteria — Verdict correct

**Severity bucket:** `bad` (a wrong build verdict wires in a broken/never-run artifact or blocks good work).
**Applies to:** all fixtures.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

The gate's final verdict must match the answer key's expected verdict and follow the skill's own decision rules (all six checks clear → Pass; required edits only → Conditional Pass; spec mismatch, unhandled failure mode, or unrunnable → Block; "I haven't run it" → automatic Block).

## Criteria (binary)

1. ✅ / ❌ The gate emits exactly one final verdict: Pass, Conditional Pass, or Block.
2. ✅ / ❌ The verdict matches the key's expected verdict. (Clean fixture → Pass, or Conditional Pass on a real minor edit only. Flawed fixture → Block.)
3. ✅ / ❌ The verdict is consistent with the gate's own scorecard: if any check is ❌ or the not-run precondition fired, the verdict is Block (not Conditional Pass); if all six checks clear, it is not Block.

## Failure modes this catches

- Gate clears an artifact that is unrunnable or never-run (false negative — wires in a broken build).
- Gate blocks a clean, runnable artifact (false positive — blocks good work; see also eval 03).
- Verdict contradicts the scorecard (e.g., a ❌ check but a Conditional Pass verdict).
