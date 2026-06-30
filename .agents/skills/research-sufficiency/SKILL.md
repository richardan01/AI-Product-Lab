---
description: Quality gate — checks whether research is sufficient to inform a decision, before it feeds into strategy, PRDs, or business cases
disable-model-invocation: true
---

# Research Sufficiency

**Agent:** Oracle (Research Analyst voice) — see `Agents/Gotham/Computer/oracle.md` for full context.
**Pattern:** Evaluator/Gate — checks whether research is sufficient to inform a decision, before it feeds into strategy, PRDs, or business cases.

Run this gate before using research output in `/business-case`, `/prioritize`, `/prd`, or any decision doc.

## Steps

1. **Read:**
   - The target research file (user provides path, or scan `Knowledge/Research/`)
   - The downstream use case — what decision or document will this research feed?

2. **Score each gate:**

| Gate | Criteria | Status | Notes |
|------|----------|--------|-------|
| Coverage | Key questions from the research brief are answered | Pass/Fail | |
| Source diversity | Multiple sources cited (not just one vendor or one article) | Pass/Fail | |
| Recency | Data and sources are current (within 6 months for market data) | Pass/Fail | |
| [YOUR_COMPANY] relevance | Findings are contextualized to [YOUR_COMPANY] (business model, market, customer base) | Pass/Fail | |
| Confidence levels | Each finding has an explicit confidence level (high/medium/low) | Pass/Fail | |
| Gaps acknowledged | Known unknowns and research limitations are stated | Pass/Fail | |
| Actionability | Findings lead to clear recommendations or decision inputs | Pass/Fail | |

3. **Final decision:**
   - All pass → **SUFFICIENT** — safe to use in decisions
   - Any fail → **INSUFFICIENT** — list gaps and what additional research is needed
   - Most pass, minor gaps → **CONDITIONAL** — usable but flag caveats downstream

4. **Output:**

```
**Research Sufficiency — [filename] — [Date]**

**Intended use:** [what decision or doc this feeds]
**Score:** [n] / 7 gates passed

**Gate Results:**
[table]

**Decision: SUFFICIENT / INSUFFICIENT / CONDITIONAL**

**Gaps:**
- [gate — what's missing — how to fill it]

**Next action:** [proceed to use in decision / run additional research first]
```

---

## Verdict file (per `_Registry/reviewer-verdict-schema.md`)

On SUFFICIENT (or SUFFICIENT-WITH-GAPS), write `<research-path>.research-sufficiency-passed` with the byte-exact header + scorecard.
