---
name: competitive-analysis
description: SWOT + Porter's Five Forces + competitive battlecard for a company, product, or market. Trigger on "/competitive-analysis <target>" or "competitive scan".
---

# Competitive Analysis

**Agent:** Research Analyst
**Methodology:** SWOT analysis + Porter's Five Forces + competitive battlecard with landmine questions (Pawel Huryn, *pm-skills*)

Usage: `competitive-analysis [company, product, or market]`

## Steps

1. **Scope the analysis**
   - Who are the direct competitors (same job-to-be-done, same buyer)?
   - Who are the indirect competitors (alternative ways to solve the same problem)?
   - What's the specific question to answer — market entry, feature parity, pricing, or positioning?

2. **Build the competitor matrix**
   For each competitor, assess:

   | Competitor | Core value prop | Target segment | Pricing model | Key strengths | Key weaknesses | Moat |
   |---|---|---|---|---|---|---|
   | | | | | | | |

3. **SWOT vs. our position**
   Frame SWOT relative to [YOUR_COMPANY]'s position in the market:

   | | Strengths | Weaknesses |
   |---|---|---|
   | **Internal** | What [YOUR_COMPANY] does better | Where [YOUR_COMPANY] is behind |
   | **External** | **Opportunities** | **Threats** |
   | | Gaps competitors leave open | Competitor moves that could hurt us |

4. **Porter's Five Forces (if market-entry or strategic context)**
   - Threat of new entrants
   - Bargaining power of buyers
   - Bargaining power of suppliers
   - Threat of substitutes
   - Competitive rivalry intensity
   Rate each: High / Medium / Low with a one-line rationale.

5. **Competitive battlecard**
   Build a one-page card for use in stakeholder conversations or sales contexts:

   ```
   **[YOUR_COMPANY] vs. [Competitor]**

   We win when:
   - [situation 1 — why we're the better choice]
   - [situation 2]

   They win when:
   - [situation where they genuinely have the edge — be honest]

   Our differentiators:
   - [specific, defensible, not just "easier to use"]

   Their likely objections to us:
   - "[common objection]" → Our response: [one sentence]
   ```

6. **Landmine questions**
   Questions designed to expose competitor weaknesses in a conversation — use in demos, stakeholder reviews, or customer calls:
   - "[Question that forces a competitor to reveal a limitation]"
   - "[Question that highlights our strength by comparison]"
   Generate 3–5 per primary competitor.

7. **Output:**

```
**Competitive Analysis — [Market/Product] — [Date]**

**Scope:** [direct vs. indirect, question being answered]

**Competitor Matrix:**
[table]

**SWOT:**
[table]

**Porter's Five Forces:** [if applicable]
[ratings + rationale]

**Battlecard — [Top Competitor]:**
[card]

**Landmine questions:**
[list]

**Strategic implication for [YOUR_COMPANY]:**
[1–2 sentences — what this means for roadmap, positioning, or pricing]
```

---

**What to run next:**
- Positioning gaps identified → take them to `roadmap-review` or a PRD
- Need to validate market assumptions → `research-sufficiency` before using this in a business case
- Preparing for a stakeholder meeting → `meeting-prep [person]` with battlecard as context
- Building GTM strategy → use this as input into `launch-plan`
