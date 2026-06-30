---
description: Quality gate — ensure PRD is ready for engineering handoff (all gates pass before spec extraction)
disable-model-invocation: true
---

# PRD Readiness

**Agent:** Product Definer (Lucius Fox voice) — see `Agents/agent-system-architecture.md` voice map.
**Pattern:** Evaluator/Gate — applied before a PRD is shared with engineering or used for task extraction.

Run this gate before handing off a PRD to engineering, before `/spec-handoff`, or before `/add-task` extracts implementation work from a PRD.

## Steps

1. **Read:**
   - The target PRD file (user provides path, or infer from `Projects/*/prd-*.md`)
   - The relevant agent file — quality checks section
   - `Projects/[YOUR_ANCHOR_PROJECT]/brief.md` — project context for alignment check

2. **Score each gate.** Each gate is tagged **[substantive]** (a Fail blocks handoff) or **[process]** (a Fail is a flag, not a blocker) — this drives the decision in Step 3.

| Gate | Bucket | Criteria | Status | Notes |
|------|--------|----------|--------|-------|
| Problem statement | substantive | Clearly defines the user problem and business impact | Pass/Fail | |
| User stories | substantive | All key user stories present with persona, action, outcome | Pass/Fail | |
| Acceptance criteria | substantive | **Every user story** has its own testable acceptance criteria (check each story individually, not just that an AC section exists) | Pass/Fail | |
| Data requirements | substantive | Data sources, schemas, and dependencies identified | Pass/Fail | |
| Scope boundaries | substantive | **Both** an explicit in-scope list **and** an out-of-scope / non-goals section are present and unambiguous. A non-goals list alone does **not** satisfy this if in-scope is not explicitly bounded. | Pass/Fail | |
| Dependencies | process | External dependencies listed with owners and ETAs (TBD owner or TBD ETA = Fail) | Pass/Fail | |
| Priority tags | process | Requirements tagged must/should/nice-to-have | Pass/Fail | |
| Feasibility input | process | Feasibility is **addressed in-doc** (model/infra rationale, latency or capacity budget, dependencies with owners+ETAs) **OR** a Data & Tech Architect review is recorded **OR** review is explicitly flagged as needed. **Fail only if feasibility is neither addressed nor flagged.** Do **not** Fail an otherwise-complete PRD merely for lacking a literal "architect sign-off" line. | Pass/Fail | |

   **AI-feature gates — apply *iff* the PRD is an AI/LLM feature** (it has a Model design / model-choice section, an Eval-criteria section, or describes an LLM/ML component). If the PRD is a standard (non-AI) feature, **do not add these rows** — their presence on a non-AI PRD is itself an error. All four are **[substantive]**:

| AI Gate | Criteria | Status | Notes |
|------|----------|--------|-------|
| Model choice justified | Model/approach named with a rationale (latency, cost, accuracy, or capability) | Pass/Fail | |
| Eval criteria defined | Quality bar is **quantified** — accuracy/precision/recall targets or a pass threshold, not prose like "doing a good job" | Pass/Fail | |
| Failure modes named | **≥3** failure modes listed, each with a mitigation | Pass/Fail | |
| Fallback paths | A per-failure fallback (low-confidence / mis-classification / model-down) is specified | Pass/Fail | |

3. **Final decision** (bucket-driven — resolves the old "any fail vs minor gaps" ambiguity):
   - **All applicable gates pass → READY** — safe to hand off or extract tasks.
   - **Any [substantive] gate (standard or AI) Fails → NOT READY** — list gaps with specific fix actions.
   - **Only [process] gates Fail (all substantive gates pass) → CONDITIONAL** — safe to proceed if the flagged process gaps are owned and tracked; list the conditions.

4. **Output:**

```
**PRD Readiness — [filename] — [Date]**

**PRD type:** [Standard / AI-feature]  ·  **Score:** [n] / [total applicable] gates passed (8 standard, +4 AI gates if AI-feature)

**Gate Results:**
[table — include the AI-gate rows only if AI-feature]

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
