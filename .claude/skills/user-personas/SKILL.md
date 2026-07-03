---
name: user-personas
description: Build jobs-to-be-done user personas from research and interviews. Trigger on "/user-personas <product, segment, or project>".
---

# User Personas

**Agent:** Research Analyst
**Methodology:** Jobs-to-be-Done persona framework — personas defined by the job they're trying to get done, not demographics. Based on Christensen, Ulwick (*Outcome-Driven Innovation*), and Torres (*Continuous Discovery Habits*).

Usage: `user-personas [product, segment, or project]`

## Steps

1. **Ground in research**
   Look for existing inputs in:
   - `Projects/[project]/research/` — interview notes
   - `Knowledge/Research/` — prior synthesis
   - Any `synthesize-research` output
   If no research exists: ask [YOUR_NAME] — "What do we know about our users from data, interviews, or support tickets?" Work with what's available and flag confidence level.

2. **Identify distinct segments**
   - Who are the distinct types of people using (or who should use) this product?
   - Segment by: job-to-be-done, current alternative, and switching trigger — NOT by age, gender, or demographic
   - Aim for 2–4 personas. More than 4 usually means under-segmented.

3. **Build each persona**

   ```
   **Persona: [Name]** (fictional, memorable)

   **Who they are:**
   [2 sentences — role, context, relationship to the product. No demographics unless relevant.]

   **Job-to-be-done:**
   When [situation], I want to [motivation], so I can [expected outcome].

   **Functional needs:**
   - [What they need the product to do]

   **Emotional needs:**
   - [How they want to feel while doing it — or avoid feeling]

   **Social needs:**
   - [How they want to be seen by others — or avoid being seen]

   **Current alternative:**
   [What they use today to get this job done — could be a competitor, a workaround, or "nothing"]

   **Switching trigger:**
   [What would make them switch to our product — the moment the current alternative fails them]

   **Biggest frustration with current alternative:**
   [The pain that creates the opening]

   **Confidence level:** H / M / L
   [High = backed by direct interviews; Medium = inferred from data; Low = assumed]
   ```

4. **Prioritize personas**
   Which persona is the beachhead — the one to design for first?
   - Highest pain + clearest switching trigger + accessible to reach = best beachhead
   - State explicitly: "Design for [Persona X] in v1. [Persona Y] is a v2 expansion."

5. **Output:**
   One block per persona (using the template above), followed by the prioritization call.

---

**What to run next:**
- Personas defined → `opportunity-solution-tree` to map their needs to opportunity space
- Beachhead unclear → `competitive-analysis` to check which segment is underserved vs. competitors
- Ready to write requirements → use personas in the PRD's user stories section (`/prd-readiness` gates the result)
- Personas need validation → design `opportunity-solution-tree` experiments to test assumptions
