# Eval 03 — verdict matches rubric

**Applies to:** all fixtures.

## What this tests

Internal consistency of the judgment. The skill defines hard verdict rules (CLEARED = all pass; CONDITIONAL = 1–2 Partials, no Fail; NEEDS REVISION = any Fail or 3+ Partials). A verdict that contradicts the review's own scorecard means the bottom line is vibes, not the rubric.

## Pass criteria

1. The overall verdict follows mechanically from the review's own Layer 1 + Layer 2 scores per the skill's rules (any Fail → NEEDS REVISION; etc.).
2. The verdict matches the answer key's expected verdict for the fixture.
3. If the verdict is CLEARED or CONDITIONAL, the review **states the verdict-file content** (the 4-line header + scorecard per `_Registry/reviewer-verdict-schema.md`) it would write; if NEEDS REVISION, it states that no verdict file is produced. In eval runs the file itself must **not** be written into `inputs/` — a written `.peer-review-passed` file beside a fixture leaks the expected verdict to future runs.

## Grading

- ✅ all three criteria hold
- ⚠ verdict matches the key but criterion 1 or 3 has a defect (e.g., scorecard shows a Fail yet verdict text says CONDITIONAL; verdict file step skipped)
- ❌ verdict contradicts the answer key's expected verdict

## Failure modes to catch

- Scorecard says Fail, verdict says CONDITIONAL (rubric ignored to be agreeable)
- Verdict softened because the document is well-written even though it has blocking gaps
- Verdict file written on a NEEDS REVISION outcome
