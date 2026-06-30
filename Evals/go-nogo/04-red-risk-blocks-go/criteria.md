# Pass criteria — Red risk blocks GO

**Severity bucket:** `bad` (a 🔴 softened to CONDITIONAL GO ships a launch with an unmitigated blocker).
**Applies to:** flawed fixture (`flawed-launch-packet.md`) only.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

Per `Evals/severity-taxonomy.md`, 🔴 = `bad` and any `bad` finding forces NO-GO. This eval verifies the gate never downgrades a 🔴 gate into a CONDITIONAL GO (or GO). CONDITIONAL GO is reserved for 0 🔴 with 1–2 🟡 only.

## Criteria (binary)

1. ✅ / ❌ At least one gate is scored 🔴, matching the key's planted 🔴 blocker(s).
2. ✅ / ❌ The presence of a 🔴 maps to a NO-GO verdict — not CONDITIONAL GO, not GO.
3. ✅ / ❌ The 🔴 blocker is listed in "Conditions / Blockers" with the gate it belongs to (e.g., the untested rollback under the Rollback gate, or the unmitigated high-severity risk under the Risk gate).

## Failure modes this catches

- Gate sees a 🔴 but issues CONDITIONAL GO "with a deadline" — the exact taxonomy violation that ships an unmitigated blocker.
- Gate averages gate colors (5 green + 1 red → "mostly green, GO") instead of applying the any-🔴 rule.
- Gate buries the 🔴 in the scorecard but omits it from the blocker list, leaving no owner/ETA.
