# Eval 05 — fix checklist actionable

**Applies to:** flawed fixtures. N/A for the clean control (no required fixes expected).

## What this tests

Whether the review's output closes the loop. A finding the author can't act on without re-deriving the review is half a finding.

## Pass criteria

1. Every Must Fix and Should Fix checklist item names the location (section, story, table, or line) where the fix applies.
2. Every item states the concrete change required ("add acceptance criteria to US-3 covering threshold, queue, and SLA" — not "improve user stories").
3. Items are grouped by severity (Must / Should / Nice) per the skill's checklist format, so the author can sequence work.
4. The checklist is complete: every Fail or Partial finding in the scorecard has a corresponding checklist item.

## Grading

- ✅ all four criteria hold for every item
- ⚠ one or two items vague on location or change, rest solid
- ❌ multiple items unactionable, severity grouping absent, or scorecard findings missing from the checklist

## Failure modes to catch

- "Improve clarity" / "add more detail" items with no object
- Findings named in prose but dropped from the checklist
- All items flattened to one severity, forcing the author to re-triage
