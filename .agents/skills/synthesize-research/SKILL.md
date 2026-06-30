# Synthesize Research

**Agent:** Oracle (Research Analyst voice) — see `Agents/Gotham/Computer/oracle.md` for full context.

Usage: "synthesize research" — run after completing a round of user research or discovery interviews.

Steps:

1. **Find interview notes** — look in `Projects/[YOUR_ANCHOR_PROJECT]/research/` or ask [YOUR_NAME] where the notes are
2. **Read each interview** — extract pain points, needs, quotes, and themes
3. **Extract patterns** — cluster themes across interviews, count frequency

Pattern extraction table:
| Theme | # Mentions | Best Quote | Participants |
|-------|-----------|-----------|-------------|
| | | | |

4. **Rank by impact** — combine frequency with business impact (key metrics for [YOUR_ROLE])

5. **Draft synthesis** using `Templates/research-summary.md`:
   - Executive summary (3–5 sentences: what we learned, what to do)
   - Top 3 findings with evidence and confidence level
   - Themes table
   - Recommendations: immediate actions + what NOT to do

6. **Suggest use case implications:**
   - Based on findings, which use case(s) have the strongest case for flight 1?
   - What data sources are needed to support them?
   - Any blockers or dependencies to flag?

7. **Ask [YOUR_NAME] to review:**
   - "Does this match what you heard?"
   - "Any key finding I missed?"
   - "Which use case does this point to for flight 1?"

8. **Update knowledge base:**
   - Offer to update `Knowledge/Reference/[YOUR_ANCHOR_PROJECT].md` use case table with findings
   - Offer to update `Projects/[YOUR_ANCHOR_PROJECT]/brief.md` open questions based on what was learned
