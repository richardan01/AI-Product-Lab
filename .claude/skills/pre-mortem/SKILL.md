---
name: pre-mortem
description: Pre-mortem exercise — imagine the project failed, work backwards to causes (tigers / paper tigers / elephants). Trigger on "/pre-mortem <project>" 2-4 weeks before a launch or high-stakes commitment.
---

# Pre-mortem

**Agent:** Risk & Dependency Tracker
**Methodology:** Gary Klein's pre-mortem method — imagine the project has failed, then work backwards to find causes. Risk taxonomy: **Tigers** (real threats), **Paper Tigers** (perceived threats that aren't real), **Elephants** (uncomfortable truths the team is avoiding).

Usage: `pre-mortem [project or initiative]`

Run this 2–4 weeks before a launch, major decision, or high-stakes commitment. Distinct from `risk-register` (ongoing tracking) — this is a point-in-time structured exercise.

## Steps

1. **Set the scene**
   Read:
   - `Projects/[project]/brief.md` — scope and success criteria
   - `Projects/[project]/prd-*.md` — what's being built (if exists)
   - `Knowledge/Reference/risk-register.md` — existing risk log

   State: "It is [target date]. The project has failed. What went wrong?"

2. **Generate failure modes**
   Produce 8–12 distinct failure scenarios across these categories:
   - Execution (missed deadline, scope creep, quality issues)
   - Adoption (users don't use it, wrong segment targeted)
   - Technical (integration failure, data quality, performance)
   - Stakeholder (misaligned expectations, org change, sponsor loss)
   - External (market shift, competitor move, regulatory)
   - Team (key person leaves, knowledge gap, capacity)

3. **Classify each failure mode**

   | # | Failure mode | Type | Probability | Impact | Owner |
   |---|---|---|---|---|---|
   | 1 | | 🐯 Tiger / 📄 Paper Tiger / 🐘 Elephant | H/M/L | H/M/L | |

   **Definitions:**
   - 🐯 **Tiger** — real threat with genuine probability and impact. Needs a mitigation plan.
   - 📄 **Paper Tiger** — sounds scary but is unlikely or low-impact on reflection. Name it, dismiss it, move on.
   - 🐘 **Elephant** — something the team knows is a problem but isn't talking about. Naming it is the intervention.

4. **Mitigation plan for Tigers**
   For each Tiger (High probability OR High impact):

   | Tiger | Root cause | Mitigation | Owner | Deadline |
   |---|---|---|---|---|
   | | | | | |

5. **Surface the Elephants**
   List each Elephant explicitly. Assign a conversation owner and a date by which the team will address it.
   - "The real Elephant in the room is: [uncomfortable truth]. Owner to address: [name]. By: [date]."

6. **Output:**

```
**Pre-mortem — [Project] — [Date]**

**Scenario:** It is [target date]. The project failed. Here's what went wrong.

**Tigers (real threats — act on these):**
[table with mitigation]

**Paper Tigers (dismiss):**
- [item — why it's not a real threat]

**Elephants (address before proceeding):**
- [uncomfortable truth — owner — date to address]

**Highest-risk item overall:** [one sentence]

**Recommendation:** [proceed / address elephants first / escalate specific tigers]
```

---

**What to run next:**
- Tigers identified → add them to `risk-register` for ongoing tracking
- Elephants named → address in next `meeting-prep [person]` with the relevant stakeholder
- Ready to commit → `go-nogo [project]` as the final launch gate
- Major risk requires [YOUR_MANAGER] input → `weekly-update` to surface it
