# Answer key — flawed-standard-prd.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

**PRD type:** Standard (no Model design / Eval criteria section → AI-specific gates MUST NOT be applied)
**Expected verdict:** NOT READY ❌ (multiple Fail-severity standard gates)

## Planted flaws

| ID | Gate (standard) | Location | Flaw |
|---|---|---|---|
| G1 | Acceptance criteria | US-3 | "Get notified when ready" has **no acceptance criteria** — US-1 and US-2 have them, US-3 ends after the story sentence. Not handoff-ready. |
| G2 | Scope boundaries | Whole document | **No explicit in-scope / out-of-scope section.** A "Non-goals" list names two exclusions but there is no in-scope boundary, leaving scope ambiguous for handoff. |
| G3 | Dependencies | Dependencies | Object storage dependency has **owner: TBD and ETA: TBD** — a load-bearing dependency (artifacts can't be stored without it) with no owner or date. |
| G4 | Goals / Success metrics | Goals + Success metrics | Success is **undefined and partly incoherent**: a goal reads "Improve checkout completion rate significantly" (wrong product, pasted in), and success metrics are "export time improves" / "job success rate is high" — no baseline, no target, not measurable. |

## Grading notes
- **Eval 01 (verdict-correct):** correct verdict is NOT READY. G1–G3 each independently block; the verdict is unambiguous. READY or CONDITIONAL here is a ❌.
- **Eval 02 (no-hallucinated-gaps):** a review that finds G1–G4 but words them differently still counts — match on substance. The Data requirements section (export_jobs schema) and Priority tags (must/should/nice) are deliberately solid; flagging them as Fail without cause is a hallucinated gap. The async worker dependency (owner: Elena, ETA 2026-07-05) is complete — only the object-storage row is the G3 flaw.
- **Eval 03 (ai-gates-applied-when-ai-feature):** this PRD is **NOT** an AI feature (no Model design / Eval criteria / model section). The gate **must not** emit AI-specific gate rows (model choice, eval criteria, failure modes, fallback paths). Applying AI gates here is a ❌ on eval 03 — it means the type-detection step misfired.
- G4 maps to the spirit of the readiness bar (a PRD with no measurable success isn't handoff-ready) even though the skill's 8 named gates lack a dedicated metrics row; catching it is expected, but the verdict is already NOT READY from G1–G3, so eval 01 does not hinge on G4.
