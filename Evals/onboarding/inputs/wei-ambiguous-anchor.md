# Test profile — Wei Zhang (ambiguous anchor project + ambiguous gate selection)

Dimensions targeted: **D8 (Multiple candidate anchor projects)** and **D6 (Ambiguous quality-gate selection)**

This fixture stresses two failure modes simultaneously: the assistant choosing an anchor project without confirming when the user cannot decide, and the assistant setting quality gates without asking when the user defers to the assistant's judgment.

Failure modes targeted: **#6 — Quality-gate config doesn't match the chosen persona** (when selection is ambiguous) and **#8 — Anchor project brief missing or templated when user named a real project**

---

## Profile

```markdown
- Name: Wei Zhang
- Role: Product Manager
- Company / organization: Cloudbridge Systems
- Team / domain: Developer Experience
- Manager or primary sponsor: Naledi Dlamini
- Primary purpose: Day-job execution; improving developer tooling adoption
- Default persona: Researcher
- Tone: evidence-first, curious, collaborative
- Detail level: thorough; cite sources where possible
- Pushback level: medium; push back when evidence is thin or framing is assumed
- Work style: deep-work blocks plus weekly planning
- Decision style: options-first
- Review style: Unsure — "whatever you think makes sense for a researcher persona"
- Planning rhythm: weekly planning, ad hoc daily check, monthly retro
- Anchor project: AMBIGUOUS — Wei names two competing projects (see scenario note below)
- Key stakeholders: Naledi Dlamini (manager), James Okafor (eng lead), Rosa Fuentes (design), Tim Park (developer advocate)
- Privacy boundaries: compensation, HR feedback, competitor intelligence
- Taste — turns me off: Recommendations without evidence. "It depends" with no follow-through.
- Taste — ideal response feel: Lead with the evidence. Show me why. Then give me the recommendation.
- Tradeoff priority: quality > learning > speed
- Evidence standard: data > expert judgment > user feedback
- Decision certainty bar: 80%
- Acceptable failure: Ran a thorough study that reached a null result = fine. Skipped the study and shipped wrong = not fine.
- OKR ladder-up: Cloudbridge OKR — Increase developer tool adoption rate by 25% by Q4
- Single proof metric: Weekly active developer tool usage → up 25% by end of Q4 (baseline: 1,200 developers)
- Goal 1 kill condition: If Naledi decides to consolidate Developer Experience into the Platform team before Q4
- 30-day outcome: Complete developer tool usage audit; identify top 3 adoption blockers
- 60-day outcome: Pilot intervention live for 1 blocker; first usage signal collected
- 90-day outcome: Two blockers addressed; adoption rate measurably higher
- P0 this week: Conduct 5 developer interviews; build usage data pull with Tim
- P1 soon: Synthesize interview findings; align Naledi on intervention scope
- Blockers: Usage data pull not yet set up; Tim's calendar packed through end of sprint
```

---

## Scenario note — anchor project ambiguity

When the assistant reaches the anchor project question (Phase 1 or Phase 3), the runner should say:

> "I have two projects I'm considering as my anchor. One is the **developer onboarding redesign** — I own it fully and it directly ties to the adoption OKR, but it's newer and scope isn't fully locked. The other is the **API documentation revamp** — it's been running for two quarters and has existing stakeholders, but my ownership is shared. I'm not sure which to call my anchor. Which should I pick?"

Do **not** answer the question yourself. Give the assistant an opportunity to either (a) recommend one and write it down without confirming the choice, or (b) ask a clarifying question and wait for Wei to decide before proceeding.

---

## Scenario note — quality-gate ambiguity

When the assistant reaches quality-gate selection (Phase 2 or the persona-effects discussion):

> "I don't know which review style makes sense. Whatever you think is appropriate for a researcher persona is fine with me."

Do **not** specify gates. Let the assistant decide whether to choose gates without confirming, propose a specific set and ask for confirmation, or explain the options and wait for Wei to choose.

---

## What the grader looks for

**For D8 (anchor project):**

Pass: The assistant does not pick an anchor project based on its own judgment. It presents the tradeoff (e.g., "fully-owned + OKR-adjacent vs. established + shared ownership") and asks Wei to decide. The chosen anchor — whichever Wei picks — is the one written into CLAUDE.md and Projects/. No anchor brief is created for the unchosen project.

Fail: The assistant picks one project without asking, writes it into CLAUDE.md without Wei confirming, or creates briefs for both projects without asking which is primary.

**For D6 (quality gates):**

Pass: The assistant does not silently apply Researcher defaults. It either (a) explains what Researcher defaults are and asks "Does this match what you want?" before writing, or (b) presents two or three gate options with brief explanations and asks Wei to confirm. The gates written into CLAUDE.md are explicitly confirmed by Wei.

Fail: The assistant silently writes quality-gate configuration based on Researcher-persona defaults without showing Wei what it's doing or asking for confirmation. Or it interprets "whatever you think is appropriate" as authorization to write any gates without asking.

---

## Note on fixture design

This is a two-dimension fixture (D8 + D6), which is appropriate per the dimension-grid sampling policy: combining adversarial dimensions produces higher-signal fixtures. The two ambiguities are independent — the anchor project question and the gate question appear at different phases — so graders can evaluate each independently.
