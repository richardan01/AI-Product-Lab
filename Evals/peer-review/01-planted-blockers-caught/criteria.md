# Eval 01 — planted blockers caught

**Applies to:** flawed fixtures (`prd-activation-checkout.md`, `synthesis-support-tickets.md`). N/A for the clean control.

## What this tests

Recall on blocking flaws. The reviewer gate is only worth running if it catches the problems a competent human reviewer would catch.

## Pass criteria

1. Every **Must Fix**-severity flaw in the fixture's answer key appears in the review's findings (any layer, any wording — match on substance).
2. Each caught flaw is attributed to the right location (section or line), not just named in the abstract.
3. The cross-section contradiction flaw (F3 / S2) is among those caught — it is listed separately because it requires reading the whole document, not section-by-section scanning.

## Grading

- ✅ all Must Fix flaws caught with correct locations
- ⚠ all but one caught, or caught with vague/wrong locations
- ❌ two or more Must Fix flaws missed

## Failure modes to catch

- Section-by-section review that never cross-references (misses contradictions)
- Structural-checklist review that confirms sections exist without reading their content (misses the unmeasurable metric, the evidence-free theme)
- Review that paraphrases the document instead of auditing it
