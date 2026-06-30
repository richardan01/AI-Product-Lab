# Answer key — flawed-ai-feature-prd.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

**PRD type:** AI-feature (has Model design + Eval criteria sections → all 12 gates apply, including the 4 AI-specific gates)
**Expected verdict:** NOT READY ❌ (AI-specific gates fail, plus one standard gate)

## Planted flaws

| ID | Gate | Location | Flaw |
|---|---|---|---|
| A1 | AI · Eval criteria defined | Eval criteria | Eval criteria are **prose only** ("we will track classification accuracy… make sure it's doing a good job") — no metrics table, no measurement method, no baseline, no target, no ship/no-ship threshold. Fails the gate. |
| A2 | AI · Failure modes named | Failure modes | **Only 2 failure modes** listed (mis-classification, latency). Gate requires ≥ 3, each with a mitigation/guardrail. Fails. |
| A3 | AI · Fallback paths specified | Whole document | **No fallback path for the critical failure** (low-confidence / mis-route). A rollback (flag off) exists but that is a release-level revert, not a per-failure fallback; the confidence-threshold fallback is left as an unresolved open question (Q1), not specified. Fails. |
| S1 | Standard · Acceptance criteria | US-2 | "Ops overrides a route" has **no acceptance criteria** (US-1 and US-3 have them). Not handoff-ready. |

## Grading notes
- **Eval 01 (verdict-correct):** correct verdict is NOT READY. A1–A3 + S1 each block.
- **Eval 02 (no-hallucinated-gaps):** match on substance. Deliberately solid (do NOT flag as Fail): model choice IS justified (latency rationale + explicit lethal-trifecta note → "Model choice justified" should PASS); scope boundaries are explicit in/out; dependencies have owners + ETAs; data requirements name the routing_events schema; US-1 and US-3 have acceptance criteria. Flagging any of these as Fail is a hallucinated gap.
- **Eval 03 (ai-gates-applied-when-ai-feature):** this PRD **is** an AI feature — the gate **must** apply the 4 AI-specific gates and must score A1/A2/A3 as Fail (and "Model choice justified" as Pass). Not applying the AI gates, or applying them but missing A1–A3, is a ❌ on eval 03.
- The distinction the gate must hold: "Model choice justified" PASS while "Eval criteria / Failure modes / Fallback paths" FAIL — partial AI-gate pass, not all-or-nothing.
