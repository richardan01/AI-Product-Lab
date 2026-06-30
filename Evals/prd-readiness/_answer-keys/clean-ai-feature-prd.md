# Answer key — clean-ai-feature-prd.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

**PRD type:** AI-feature (has Model design + Eval criteria sections → all 12 gates apply)
**Expected verdict:** READY ✅ (CONDITIONAL ⚠️ acceptable only if the single open question Q1 is treated as a minor condition — it has an owner and a due date, so it is tracked work, not a blocker)

## Planted flaws
None. This is the false-positive control.

The PRD is deliberately complete: every user story (US-1, US-2, US-3) has its own testable acceptance criteria; the eval-criteria table carries method + baseline + target + ship threshold for each metric; four failure modes each have a guardrail; fallback paths are specified for the critical failures (inference timeout → no suggestion; harmful-rate breach → per-team kill switch); dependencies have owners and ETAs; scope is explicitly in/out; model choice is justified with a latency rationale and an explicit lethal-trifecta note.

## Grading notes
- **Eval 01 (verdict-correct):** correct verdict is READY (or CONDITIONAL citing only Q1). NOT READY here is a P0 false-positive failure.
- **Eval 02 (no-hallucinated-gaps):** any gate marked **Fail** is a hallucinated gap — every one of the 12 gates has genuine supporting content. Marking "Acceptance criteria — Fail" or "Failure modes — Fail" etc. is a fabricated finding.
- **Eval 04 (clean-prd-not-flunked):** passes only if the verdict is READY/CONDITIONAL with **zero Fail gates** and no fabricated Must-Fix items. Demanding a section that is already present under a different heading (e.g., claiming no rollback when the Launch plan specifies "feature flag off restores the prior inbox") is the exact false-positive this fixture catches.
- A gate legitimately marked **CONDITIONAL** solely on Q1 (alternative drafts in v1) is acceptable.
