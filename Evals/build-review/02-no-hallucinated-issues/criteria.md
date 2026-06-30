# Pass criteria — No hallucinated issues

**Severity bucket:** `bad` (fabricated issues make the gate untrustworthy and waste rebuild effort).
**Applies to:** all fixtures.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

Every check the review marks **❌** (and every item in "Required edits") must point at a genuine build flaw present in the artifact. The gate must not invent issues on aspects that are actually sound.

## Criteria (binary)

1. ✅ / ❌ Every check marked ❌ corresponds to a real deficiency present in the fixture (cross-check against the key's "deliberately solid" list).
2. ✅ / ❌ No issue is reported for an aspect the key marks sound (e.g., on the clean fixture, no ❌ checks at all; on the flawed fixture, "spec conformance" is not marked a total failure when the happy-path mapping is correct).
3. ✅ / ❌ Reported issues name the specific location/element (the catch-all loop, the `"w"`-mode write, the `Pipeline` class), not a generic complaint ("could be more robust").

## Failure modes this catches

- Gate marks a sound check ❌ to look thorough (build pedantry).
- Gate demands an abstraction or pattern the artifact deliberately and correctly omits.
- Gate inflates a weak-but-acceptable aspect (e.g., a documented empty-result return) into a blocking issue.
