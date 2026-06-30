# Eval 04 — clean artifact not flunked

**Applies to:** clean control fixture (`weekly-update-clean.md`) only. N/A for flawed fixtures.

## What this tests

The false-positive rate of the gate. A reviewer that finds blocking problems in a sound artifact generates noise, erodes trust in the gate, and trains the user to rubber-stamp past it.

## Pass criteria

1. Verdict is CLEARED (or CONDITIONAL with only defensible Partial findings — see answer key grading notes).
2. Zero Must Fix items.
3. Any Should Fix / Nice to Fix items are genuine improvements, not manufactured objections to content the key marks as deliberately sound.

## Grading

- ✅ CLEARED with no Must Fix items
- ⚠ CONDITIONAL where the Partial findings are defensible real gaps
- ❌ NEEDS REVISION verdict, or any Must Fix item

## Failure modes to catch

- Reviewer severity-anchors on "every review must find something blocking"
- Template-completeness pedantry (flunking a weekly update for lacking PRD sections)
- Taste preferences escalated to blocking severity
