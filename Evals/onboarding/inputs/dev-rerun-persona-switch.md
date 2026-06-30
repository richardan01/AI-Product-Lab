# Test profile — Alex Reyes (re-run with persona switch)

Dimension targeted: **D9 (Re-run with new persona)**

This fixture is a two-scenario structure. The runner executes onboarding twice against the same identity, changing only the persona between runs. The test grades whether the assistant re-asks persona/tone/gates on re-run, or silently preserves the first-run configuration.

Failure mode targeted: **#12 — Re-run silently preserves persona / tone / gates without re-asking**

---

## Scenario A — First run (Executive operator)

Use the profile below as the simulated user for the first onboarding run:

```markdown
- Name: Alex Reyes
- Role: Senior Product Manager
- Company / organization: Meridian Software
- Team / domain: Platform Products
- Manager or primary sponsor: Camille Osei
- Primary purpose: Day-job execution, stakeholder alignment, quarterly planning
- Default persona: Executive operator
- Tone: direct, recommendation-first, low ceremony
- Detail level: standard
- Pushback level: medium; challenge unclear goals and missing evidence
- Work style: weekly planning plus daily focus check
- Decision style: recommendation-first with tradeoffs
- Review style: strict PM craft review
- Planning rhythm: weekly planning, daily `/today`, Friday `/weekly-update`
- Anchor project: Platform API migration
- Key stakeholders: Camille Osei (manager), Dev Patel (eng lead), Priya Menon (design)
- Privacy boundaries: compensation, HR feedback, sensitive customer data
- Taste — turns me off: Long preambles. Sycophantic openers. Restating the question before answering.
- Taste — ideal response feel: Recommendation first. Tradeoff visible. Short.
- Tradeoff priority: speed > quality > learning
- Evidence standard: data > user feedback > expert judgment
- Decision certainty bar: 70%
- Acceptable failure: Fast experiment that missed = fine. Avoidable deadline slip = not fine.
- OKR ladder-up: Meridian company OKR — Reduce API integration time for enterprise customers by 40% by Q4
- Single proof metric: Median integration time for new enterprise customers → down 40% by end of Q4
- Goal 1 kill condition: If the eng team is reorged into separate mobile and platform tracks before migration ships
- 30-day outcome: Complete API audit; align Camille on migration scope and timeline
- 60-day outcome: Pilot migration live for 2 enterprise customers; v1 changelog published
- 90-day outcome: 80% of integrations on new API; deprecation plan published
- P0 this week: Finish API audit doc; book Camille alignment meeting
- P1 soon: Draft customer migration guide; align Dev on instrumentation gaps
- Blockers: 2 legacy endpoints still undocumented; eng capacity constrained by Q3 features
```

After the first run is complete and all files are written, the runner should stop. The first-run CLAUDE.md, GOALS.md, and Tasks/active.md are the baseline.

---

## Scenario B — Re-run with new persona

Use the same identity fields as Scenario A. The **only change** is the persona:

```markdown
- Default persona: Builder / AI PM
```

All other fields (name, company, role, stakeholders, project, OKRs) are identical to Scenario A.

**Runner instructions for Scenario B:**
1. Start a new onboarding session (do not continue Scenario A's session).
2. State to the assistant: "I want to re-run onboarding. My name is Alex Reyes and I'm re-configuring the OS."
3. When the assistant asks (or proceeds through) persona selection, indicate Builder / AI PM.
4. Capture the full transcript verbatim.

---

## What the grader looks for

Grade against **eval 03** (persona-routing-respected) and **eval 07 criterion 7** (re-run re-asks persona/tone/gates):

**Pass:** The assistant explicitly re-asks persona, tone, and quality-gate preference during Scenario B. The resulting CLAUDE.md reflects Builder / AI PM configuration (mandatory `/eval-review` + `/build-review` + `/test-plan` pre-deployment gates, eval-first tone). The assistant does **not** say "I see you already have Executive operator configured — keeping that."

**Fail:** The assistant detects the prior configuration and preserves it, or silently outputs files with Executive operator defaults despite the user indicating Builder / AI PM. The transcript shows no re-ask of persona, tone, or gates.

---

## Note on fixture design

Alex Reyes is intentionally similar to Jordan Lee (both start as Executive operators, both at tech companies, both with a platform-adjacent project). The variable that matters is D9. Cosmetic differences (name, company, project) are present only to avoid exact duplication — they do not change what is being tested.
