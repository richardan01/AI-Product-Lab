# Sample passing output — eval 04 (no residual placeholders)

Based on the Jordan Lee fixture (complete onboarding, no deferrals). Graders use this as the anchor for clean post-onboarding files.

---

## CLAUDE.md — passes C1

All identity and operating style fields filled with Jordan Lee's specific values:

```markdown
**[YOUR_NAME]** → Jordan Lee
**[YOUR_ROLE]** → Senior Product Manager
**[YOUR_COMPANY]** → Acme AI
**[YOUR_TEAM_OR_DOMAIN]** → Growth Platform
**[YOUR_MANAGER]** → Priya Shah
**[HEAD_OF_DEPT]** → (not provided — preserved as [HEAD_OF_DEPT] with user-note "not yet known")
```

`grep '[YOUR_' CLAUDE.md` returns one line: the `[HEAD_OF_DEPT]` field with an adjacent note `# user said: not yet known`. That is a documented deferral, not a silent placeholder.

---

## GOALS.md — passes C2, C3

No `[YOUR_*]`, `[AREA_*]`, `[METRIC_*]`, or `[STAKEHOLDER_*]` brackets remain. Legacy marketing placeholders (`[LIFECYCLE_PM]`, `[CURRENT_QUARTER]`, etc.) are absent — they were not present in the first place because the template was filled cleanly.

---

## Tasks/active.md — passes C4

```markdown
## In Progress

- [ ] Finish discovery readout draft for activation funnel project #p0 #project
- [ ] Book Priya 1:1 for readout review #p0 #stakeholders

## To Do

### #p0
- [ ] Review Marco's instrumentation spike results #p0 #project

### #p1
- [ ] Draft top 3 hypotheses for Priya readout #p1 #strategy
```

No `[Task description]`, `[Sprint N]`, or `[Start Date]` brackets in any populated row.

---

## Deferred field handling — passes C5

`[HEAD_OF_DEPT]` in CLAUDE.md is preserved because the user said "I don't know yet." The field reads:

```markdown
**[HEAD_OF_DEPT]** — [HEAD_OF_DEPT] # user said: not yet known — follow-up in Tasks/follow-ups.md
```

The deferral is visible and annotated. `Tasks/follow-ups.md` contains:

```
| 2026-05-14 | Jordan Lee | Fill in [HEAD_OF_DEPT] when org chart is confirmed | — | Open |
```
