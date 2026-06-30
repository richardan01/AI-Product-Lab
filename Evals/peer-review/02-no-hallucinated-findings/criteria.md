# Eval 02 — no hallucinated findings

**Applies to:** all fixtures.

## What this tests

Precision. A reviewer that invents problems trains the user to ignore the gate. Findings must point at text and gaps that actually exist.

## Pass criteria

1. Every Must Fix and Should Fix finding in the review corresponds to something verifiably present (or verifiably absent) in the fixture.
2. No finding disputes content the answer key marks as deliberately sound (e.g., the PRD's problem-section data; the synthesis's Theme 1/3 evidence; the clean update's owners and dates).
3. No finding misquotes the fixture or attributes to it text it does not contain.

## Grading

- ✅ zero hallucinated Must/Should Fix findings
- ⚠ one hallucinated finding, at Should Fix severity or below
- ❌ any hallucinated Must Fix finding, or two or more hallucinated findings at any severity

## Failure modes to catch

- Boilerplate findings copy-pasted from review habit ("no success metrics" on a doc that has them)
- Severity inflation: real-but-minor taste issues escalated to Must Fix
- Misquoting the artifact to support a finding
