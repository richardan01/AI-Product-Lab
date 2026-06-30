# Test profile — Morgan Chen (Custom persona)

Use this fixture to test the custom-persona path. The assistant must not force Morgan into Executive operator, Research partner, Product coach, Builder, or Minimalist defaults. It should capture the custom behavior, ask which gates and commands should apply, and preserve privacy boundaries.

```markdown
- Name: Morgan Chen
- Role: Principal Product Manager
- Company / organization: Northstar Health
- Team / domain: AI clinical operations
- Manager or primary sponsor: Dana Patel
- Primary purpose: Mixed setup — day-job execution plus AI PM craft development
- OS mode: Custom
- Default persona: Calm operator with clinical-safety rigor
- Tone: concise, careful, evidence-first, never theatrical
- Detail level: standard, but include a deeper appendix for safety-critical decisions
- Pushback level: high when patient safety, privacy, or model-risk claims are weak; medium otherwise
- Work style: weekly planning, daily priority check, monthly risk review
- Decision style: options-first for safety-critical calls; recommendation-first for routine execution
- Review style: strict PM craft review plus safety/risk review for AI features
- Commands to surface first: `/today`, `/weekly-update`, `/meeting-prep`, `/prd-readiness`, `/eval-review`, `/risk-register`
- Quality gates requested: `/peer-review` for normal artifacts; `/eval-review` + `/risk-register` before AI clinical workflow decisions
- Planning rhythm: Monday planning, daily `/today`, Friday `/weekly-update`, monthly risk review
- Anchor project: Clinical triage assistant pilot
- Key stakeholders: Dana Patel (manager), Luis Romero (clinical ops), Asha Green (privacy counsel), Maya Singh (ML lead)
- Privacy boundaries: patient names, PHI, clinician performance feedback, legal advice, compensation
- Taste — turns me off: Hype, faux certainty, and treating model risk as a checklist
- Taste — ideal response feel: Starts with the safest useful recommendation, names assumptions, and separates evidence from judgment
- Tradeoff priority: safety > quality > speed > learning
- Evidence standard: validated data > clinician review > user feedback > expert judgment
- Decision certainty bar: 90% for safety-critical changes; 70% for reversible workflow changes
- Acceptable failure: A reversible workflow experiment that fails to move adoption is acceptable. A privacy leak or unsafe model recommendation is not acceptable
- OKR ladder-up: Reduce triage backlog by 20% without increasing clinical escalation errors
- Single proof metric: Median triage backlog age → down 20% while escalation-error rate does not increase
- Goal 1 kill condition: If privacy counsel blocks use of clinical notes in the pilot dataset
- 30-day outcome: Map triage workflow, agree on pilot scope, define eval criteria with Maya and Luis
- 60-day outcome: Run offline eval on de-identified cases and review failure modes with clinical ops
- 90-day outcome: Launch limited pilot if eval gates pass and privacy counsel approves
- P0 this week: Draft pilot PRD outline; schedule privacy counsel review
- P1 soon: Gather de-identified case sample requirements; define escalation-error taxonomy
- Blockers: Privacy counsel has not approved data-retention approach
```

Morgan's profile deliberately mixes custom persona, AI PM, and sensitive-domain privacy requirements. It should stress Eval 11 and Eval 12.
