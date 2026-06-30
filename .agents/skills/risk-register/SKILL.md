# Risk Register

**Agent:** Risk & Dependency Tracker (Riddler voice) — see `Agents/README.md` voice map.

View and update the unified risk register across all active projects. Run this weekly alongside `roadmap review`.

## Steps

1. **Read:**
   - `Knowledge/Reference/risk-register.md` — existing risk log (create if missing)
   - `Projects/[YOUR_ANCHOR_PROJECT]/brief.md` — extract any risks or dependencies listed
   - `Tasks/active.md` — identify blocked items not yet logged as risks

2. **For any new risk found, capture:**

| ID | Risk | Probability | Impact | Severity | Owner | Mitigation | Status | Last Updated |
|----|------|-------------|--------|----------|-------|------------|--------|--------------|
| R001 | | H/M/L | H/M/L | 🔴/🟡/🟢 | | | Open/Mitigated/Closed | |

   Severity rules:
   - 🔴 High prob + High impact, OR blocking a launch milestone
   - 🟡 Medium — monitor weekly, has a mitigation plan
   - 🟢 Low — logged, revisit monthly

3. **Escalation triggers — flag immediately if:**
   - Any 🔴 risk has no owner → assign one now
   - Any 🔴 risk open >2 weeks → draft escalation to [YOUR_MANAGER]
   - Any external dependency (vendor, eng, budget, legal) has no ETA → chase it

4. **Output:**

```
**Risk Register — [Date]**

**🔴 High Severity:** [n] — [list titles]
**🟡 Medium:** [n]
**🟢 Low:** [n]

**Action Required This Week:**
- [risk ID + title — action — owner — deadline]

**Full Register:**
[table]

**Dependencies with No ETA:**
- [item — who owns it — last chased: date]
```

5. **Run escalation trigger check:**
   - Scan every 🔴 risk: does it have an owner? How many days has it been open?
   - Scan every external dependency: is there an ETA? When was it last updated?
   - If any trigger fires, append an **Escalation Alerts** section to the output
   - If no triggers fire, omit this section.

6. **Save updated register to** `Knowledge/Reference/risk-register.md`

---

**Next Steps:**
- `dependency-check` — deep-dive on external dependencies separately
- `escalation-draft [risk-id]` — draft a [YOUR_MANAGER] message for any blocked 🔴 risk
- `roadmap review` — always review risks alongside milestone status
- `go-nogo [project]` — share risk register with Launch Manager before launch decision
