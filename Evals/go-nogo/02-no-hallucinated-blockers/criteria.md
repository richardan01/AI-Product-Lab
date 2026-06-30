# Pass criteria — No hallucinated blockers

**Severity bucket:** `bad` (fabricated blockers make the gate untrustworthy and delay a ready launch).
**Applies to:** all fixtures.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

Every gate the review scores 🔴 or 🟡 (and every item in "Conditions / Blockers") must point at a genuinely red or yellow signal in the packet. The gate must not invent blockers on gates that are actually green.

## Criteria (binary)

1. ✅ / ❌ Every gate scored 🔴 or 🟡 corresponds to a real deficiency present in the fixture (cross-check against the key's "deliberately green" list).
2. ✅ / ❌ No blocker is reported for a gate the key marks green (e.g., on the clean fixture, no 🔴/🟡 gates at all; on the flawed fixture, the Comms gate is not marked 🔴).
3. ✅ / ❌ Reported blockers quote or name the specific packet line/element, not a generic complaint ("rollback could be more robust").

## Failure modes this catches

- Gate scores a green gate 🔴/🟡 to look thorough (template pedantry).
- Gate demands a sign-off that is present under a different heading.
- Gate inflates a tracked 🟡 condition (owner + ETA attached) into a 🔴 blocker.
