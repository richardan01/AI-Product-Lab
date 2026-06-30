# Answer key — insufficient-research.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

**Research type:** Decision-input research (feeds the H2 roadmap fund/no-fund decision → all 7 gates apply)
**Expected verdict:** INSUFFICIENT ❌ (multiple Fail-severity gates; the recommendation overclaims confidence the evidence cannot support)

## Planted flaws

| ID | Gate | Location | Flaw |
|---|---|---|---|
| R1 | Source diversity | Sources | **Single source** — one vendor marketing whitepaper. No internal data, no customer signal, no second viewpoint. One self-interested source cannot triangulate a build decision. Fails. |
| R2 | Recency | Market opportunity + Sources | Market data is from a **2023 vendor report** (>6 months / ~3 years stale) used to size a 2026 decision. Fails the ≤6-month recency bar for market data. |
| R3 | Confidence levels | Findings | **No explicit confidence level on any finding** — every finding is stated as flat assertion ("clearly a top unmet need", "substantial"). Gate requires high/medium/low per finding. Fails. |
| R4 | Actionability / overclaim | Recommendation | Recommendation overclaims: **"clear, high-confidence bet… commit the roadmap now"** on thin, single-source, undated signal. Confident commitment is not supported by the evidence; the actionable output would be to scope discovery, not commit a full build. Fails. |
| R5 | Gaps acknowledged | Whole document | **No gaps / limitations section.** No known unknowns named despite the obvious ones (no internal demand signal, no willingness-to-pay, no competitive depth). Fails. |

## Grading notes
- **Eval 01 (verdict-correct):** correct verdict is INSUFFICIENT. R1–R5 each independently block; the verdict is unambiguous. SUFFICIENT or CONDITIONAL here is a ❌.
- **Eval 02 (no-hallucinated-gaps):** a review that finds R1–R5 but words them differently still counts — match on substance. Do not invent gaps beyond the real ones: the summary *does* state an intended use and brief questions, so "no stated decision use" would be a hallucinated gap. Match on the genuine deficiencies only.
- **Eval 04 (insufficiency-detected):** this is the precision-of-flunking check — the thin, single-source, no-confidence, overclaiming summary **must** be marked INSUFFICIENT, never SUFFICIENT. Clearing it (SUFFICIENT) is the exact false-negative this fixture catches; a confidently-recommended build on one stale vendor source is precisely the decision the gate exists to stop.
- The [YOUR_COMPANY]-relevance gate is also weak (findings are generic, not tied to [YOUR_COMPANY]'s book), but the verdict is already INSUFFICIENT from R1–R5, so eval 01 does not hinge on it.
