# Pass criteria — No hallucinated gaps

**Severity bucket:** `bad` (fabricated gaps make the gate untrustworthy and waste rework).
**Applies to:** all fixtures.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

Every gate the review marks **Fail** (and every gap in "Gaps to resolve") must point at a genuinely missing or weak element of the PRD. The gate must not invent gaps on sections that are actually complete.

## Criteria (binary)

1. ✅ / ❌ Every gate marked Fail corresponds to a real deficiency present in the fixture (cross-check against the key's "deliberately solid" list).
2. ✅ / ❌ No gap is reported for a section the key marks complete (e.g., on the clean fixture, no Fail gates at all; on the AI fixture, "Model choice justified" is not marked Fail).
3. ✅ / ❌ Reported gaps quote or name the specific location/element, not a generic template complaint ("could be more detailed").

## Failure modes this catches

- Gate marks a complete section Fail to look thorough (template pedantry).
- Gate demands a section that is present under a different heading.
- Gate inflates a Nice-to-have into a blocking gap.
