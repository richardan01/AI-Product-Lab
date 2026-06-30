---
description: Quality gate — ensure PRD is ready for engineering handoff (all gates pass before spec extraction)
disable-model-invocation: true
---

# PRD Readiness

**Agent:** Product Definer (Lucius Fox voice) — see `Agents/README.md` voice map.
**Pattern:** Evaluator/Gate — applied before a PRD is shared with engineering or used for task extraction.

Run this gate before handing off a PRD to engineering, before `/spec-handoff`, or before `/add-task` extracts implementation work from a PRD.

## Steps

1. **Read:**
   - The target PRD file (user provides path, or infer from `Projects/*/prd-*.md`)
   - The relevant agent file — quality checks section
   - `Projects/[YOUR_ANCHOR_PROJECT]/brief.md` — project context for alignment check

2. **Score each gate:**

| Gate | Criteria | Status | Notes |
|------|----------|--------|-------|
| Problem statement | Clearly defines the user problem and business impact | Pass/Fail | |
| User stories | All key user stories present with persona, action, outcome | Pass/Fail | |
| Acceptance criteria | Every requirement has testable acceptance criteria | Pass/Fail | |
| Data requirements | Data sources, schemas, and dependencies identified | Pass/Fail | |
| Scope boundaries | Explicit in/out of scope section — no ambiguity | Pass/Fail | |
| Dependencies | External dependencies listed with owners and ETAs | Pass/Fail | |
| Priority tags | Requirements tagged must/should/nice-to-have | Pass/Fail | |
| Feasibility input | Data & Tech Architect has reviewed (or flagged as needed) | Pass/Fail | |

3. **Final decision:**
   - All pass → **READY** — safe to hand off or extract tasks
   - Any fail → **NOT READY** — list gaps with specific fix actions
   - Most pass, minor gaps → **CONDITIONAL** — list conditions, safe to proceed if flagged

4. **Output:**

```
**PRD Readiness — [filename] — [Date]**

**Score:** [n] / 8 gates passed

**Gate Results:**
[table]

**Decision: READY / NOT READY / CONDITIONAL**

**Gaps to resolve:**
- [gate — what's missing — suggested fix]

**Next action:** [proceed to spec-handoff / return to Product Definer for revision]
```

---

**Next Steps:**
- PRD is READY → `spec-handoff [project]` to package for engineering
- PRD is NOT READY → fix gaps, then re-run `prd-readiness`
- Need feasibility input → `tech-feasibility [feature]` before re-checking

---

## Verdict file (per `_Registry/reviewer-verdict-schema.md`)

On READY (or READY-WITH-CONDITIONS), write `<prd-path>.prd-readiness-passed` with the byte-exact 4-line header followed by the scorecard.
