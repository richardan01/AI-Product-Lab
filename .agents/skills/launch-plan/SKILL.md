# Launch Plan

**Agent:** Launch Manager (Batman voice) — see `Agents/README.md` voice map.

Build a launch readiness checklist for [project]. Run this 2–3 weeks before target go-live.

## Steps

1. **Read project context:**
   - `Projects/[project]/brief.md` — scope, milestones, acceptance criteria
   - `Projects/[project]/prd-*.md` — feature details (if exists)
   - `Projects/[project]/uat-results.md` — QA status (if exists)
   - `Knowledge/Reference/risk-register.md` — open risks
   - `Tasks/active.md` — current pre-launch task status

2. **Build launch checklist across 5 areas:**

   **Product Readiness**
   - [ ] All P0 acceptance criteria met and tested
   - [ ] UAT completed and signed off
   - [ ] Known bugs documented with severity ratings
   - [ ] Rollback plan defined

   **Data Readiness**
   - [ ] Data sources connected and validated
   - [ ] Data quality checks passing (>95% completeness)
   - [ ] PII/privacy compliance confirmed
   - [ ] Metrics baseline captured pre-launch

   **Stakeholder Readiness**
   - [ ] Training completed for relevant team members
   - [ ] User guides available
   - [ ] Support escalation path defined

   **Comms Readiness**
   - [ ] Internal announcement drafted
   - [ ] [YOUR_MANAGER] briefed
   - [ ] Launch date confirmed with all parties

   **Post-Launch Readiness**
   - [ ] Success metrics defined
   - [ ] Monitoring in place
   - [ ] 1-week post-launch review scheduled

3. **Output:**

```
**Launch Plan — [Project] — [Date]**

**Target Launch Date:** [date]
**Overall Readiness:** 🟢/🟡/🔴 ([X]/[Y] criteria met)

**Checklist:**
[by area, with owner for any unchecked item]

**Blockers to Launch:**
- [item — owner — ETA]

**Recommendation:** [go / hold / conditional go with conditions]
```

---

**Next Steps:**
- `go-nogo [project]` — run final go/no-go when all checklist items are green
- `launch-comms [project]` — draft the internal launch announcement
- `risk-register` — review open risks before committing to the launch date
- `training-plan [feature]` — build training if stakeholder readiness is incomplete
