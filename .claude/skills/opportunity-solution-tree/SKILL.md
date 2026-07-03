---
name: opportunity-solution-tree
description: Map a desired outcome to the opportunity space and branch into solutions and experiments (Teresa Torres OST). Trigger on "/opportunity-solution-tree <outcome or project>".
---

# Opportunity Solution Tree

**Agent:** Discovery & Solution Analyst — maps the opportunity space, then evaluates solution feasibility.
**Methodology:** Teresa Torres, *Continuous Discovery Habits* — OST maps a desired outcome to the opportunity space, then branches into solutions and experiments.

Usage: `opportunity-solution-tree [outcome or project]`

## Steps

1. **Establish the desired outcome**
   - State the business outcome you're trying to move (not a feature — a metric or behavior)
   - Example: "Increase merchant activation rate from 40% to 60% within 90 days"
   - If unclear: ask [YOUR_NAME] — "What does success look like in 90 days, in one measurable sentence?"

2. **Map the opportunity space**
   - Identify user needs, pain points, and desires that, if addressed, would move the outcome
   - Source from: `Projects/[project]/research/`, `synthesize-research` outputs, or [YOUR_NAME]'s direct input
   - Use the JTBD lens: what job is the user trying to get done, and where are they struggling?

   | Opportunity | Type (Need / Pain / Desire) | Evidence | Confidence |
   |---|---|---|---|
   | | | | H/M/L |

3. **Prioritize opportunities**
   - Rank by: reach (how many users) × impact (how much it moves the outcome) × evidence strength
   - Flag the top 2–3 opportunities worth exploring
   - Do NOT jump to solutions yet — make sure the opportunity is real before branching

4. **Branch solutions**
   - For each top opportunity, generate 2–3 solution ideas (not specs — concepts)
   - Deliberately include at least one unconventional option per opportunity

   | Opportunity | Solution Idea | Assumption it tests | Effort (S/M/L) |
   |---|---|---|---|
   | | | | |

5. **Design experiments**
   - For each solution, identify the riskiest assumption and the fastest way to test it
   - Prefer: fake door, wizard-of-oz, concierge, or lightweight prototype over full build

   | Solution | Riskiest assumption | Experiment | Signal to look for |
   |---|---|---|---|
   | | | | |

6. **Output:**

```
**Opportunity Solution Tree — [Project] — [Date]**

**Desired outcome:** [one sentence, measurable]

**Top opportunities:**
1. [opportunity — evidence — confidence]
2.
3.

**Solution branches:**
[table]

**Experiments to run first:**
[table]

**Recommended next step:** [which experiment to run and why]
```

---

**What to run next:**
- Ready to spec a solution → `prd-readiness` after drafting the PRD
- Need to validate assumptions first → design the experiment and run it before building
- Opportunities unclear → `synthesize-research` to go deeper on user needs
- Committing to an outcome → `quarterly-planning` to align it to OKRs
