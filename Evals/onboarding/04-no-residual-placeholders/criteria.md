# Pass criteria — No residual placeholders

**Type:** Generalization Failure (mechanically checkable — programmatic grading required)
**Grader:** programmatic regex via `grade.sh` (see end of file). No LLM judge — code beats judge when both are reliable (Hamel §5.2).

After a complete onboarding (no deferrals), zero template placeholders should remain in core config files — including the `Memory/` files onboarding writes.

## Criteria (binary)

1. ✅ / ❌ `CLAUDE.md` contains zero `[YOUR_*]`, `[HEAD_OF_DEPT]`, `[STAKEHOLDER_*]`, or `[METRIC_*]` placeholders.
2. ✅ / ❌ `GOALS.md` contains zero `[YOUR_*]`, `[AREA_*]`, `[METRIC_*]`, `[STAKEHOLDER_*]`, or `[DEV_GOAL_*]` placeholders.
3. ✅ / ❌ `GOALS.md` does not contain marketing-team-legacy placeholders: `[LIFECYCLE_PM]`, `[PAID_ADS_PM]`, `[WEBSITE_PM]`, `[CONTENT_PM]`, `[CURRENT_QUARTER]`.
4. ✅ / ❌ `Tasks/active.md` has no bracketed `[Task description]`, `[Sprint N]`, or `[Start Date]` placeholders in the populated rows.
5. ✅ / ❌ Any placeholder the user explicitly chose to defer is annotated with a visible `# TODO: ask user` comment or `Unknown / TBD` marker so it doesn't silently survive.
6. ✅ / ❌ `Memory/USER.md` exists (onboarding wrote it) and contains zero `[YOUR_*]` identity placeholders.
7. ✅ / ❌ `Memory/OPERATING_CONTEXT.md` exists (onboarding wrote it) and contains zero `[YOUR_*]` identity placeholders.

> C6–C7 are scoped to `[YOUR_*]` identity tokens only. Other bracketed strings in the `Memory/` files (e.g. `[daily / weekly / sprint]`, `[Monday / Sunday / other]`) are intentional option-text the user selects from, not residual placeholders, so checking them would produce false positives.

## Failure modes this catches

- Assistant leaves marketing-team-legacy placeholders untouched because they "weren't asked about."
- Assistant copies the template verbatim into the user's `GOALS.md` 30-60-90 section.
- Assistant fills some placeholders but skips others without telling the user.
- Assistant treats `[YOUR_NAME]` and `[YOUR_COMPANY]` as literal values to preserve.

## Programmatic grading

This eval is graded by `grade.sh` (in this directory), not by an LLM judge. The script checks each criterion via regex against the target files (`CLAUDE.md`, `GOALS.md`, `Tasks/active.md`, `Memory/USER.md`, `Memory/OPERATING_CONTEXT.md`) and prints a verdict line per criterion. The grader sub-agent should run this script and parse its output.

The old `judge-prompt.md` is retired to `_retired/judge-prompt.md` because LLM judgment is not the right tool for a deterministic regex check (Hamel §5.2: "code-based assertions when possible — they are fast, cheap, deterministic, and interpretable").
