# Pass criteria — No hallucinated gaps

**Severity bucket:** `bad` (fabricated gaps make the gate untrustworthy and waste rework).
**Applies to:** all fixtures.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

Every gate the review marks **Fail** (and every item in "Gaps") must point at a genuinely missing or weak element of the research summary. The gate must not invent gaps on sections that are actually complete.

## Criteria (binary)

1. ✅ / ❌ Every gate marked Fail corresponds to a real deficiency present in the fixture (cross-check against the key's "deliberately solid" / planted-flaw lists).
2. ✅ / ❌ No gap is reported for a section the key marks complete (e.g., on the sufficient fixture, no Fail gates at all; on the insufficient fixture, no claim that "no decision use is stated" when the summary states one).
3. ✅ / ❌ Reported gaps quote or name the specific finding/source/section, not a generic complaint ("could use more sources").

## Failure modes this catches

- Gate marks a complete section Fail to look thorough (template pedantry).
- Gate demands something that is present under a different heading.
- Gate inflates an already-acknowledged limitation into a fabricated blocking gap.
