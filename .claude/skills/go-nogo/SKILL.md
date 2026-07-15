---
description: Quality gate — structured go/no-go decision for launch (run 24-48 hours before launch)
disable-model-invocation: true
---

# Go / No-Go

**Agent:** Launch Manager (Batman voice) — see `Agents/agent-system-architecture.md` voice map.

Run a structured go/no-go decision for [project]. Use this 24–48 hours before planned launch.

## Step 0 — Eval Staleness Check

If any launch-plan or UAT input cites an eval suite's pass rate, invoke `/eval-ci check <suite>` for each cited suite before scoring gates. If any returns `BLOCK`, the Product gate cannot score 🟢 — mark it 🔴 with the finding "stale eval: re-run `<suite>` before this decision cites it (changed `<source file>`, SHA `<sha>`)." If all cited suites return `OK` (or none is cited), proceed to Step 1.

## Steps

1. **Read:**
   - `Projects/[project]/launch-plan.md` — checklist status
   - `Projects/[project]/uat-results.md` — QA sign-off
   - `Knowledge/Reference/risk-register.md` — unmitigated risks
   - `Tasks/active.md` — any open P0 items

2. **Score each gate:**

| Gate | Criteria | Status | Decision |
|------|----------|--------|----------|
| Product | All P0 acceptance criteria met and tested | 🟢/🟡/🔴 | Go/No-Go |
| Data | Quality checks passing, PII confirmed | 🟢/🟡/🔴 | Go/No-Go |
| Stakeholders | Training done, users confirmed ready | 🟢/🟡/🔴 | Go/No-Go |
| Comms | Announcement drafted, [YOUR_MANAGER] briefed | 🟢/🟡/🔴 | Go/No-Go |
| Risk | No unmitigated 🔴 risks | 🟢/🟡/🔴 | Go/No-Go |
| Rollback | Rollback plan documented and tested | 🟢/🟡/🔴 | Go/No-Go |

3. **Final decision:**
   - All green → **GO** — confirm launch date and send comms
   - Any red → **NO-GO** — list blockers with owners and ETAs
   - Yellow items → **CONDITIONAL GO** — list conditions with hard deadlines

4. **Output:**

```
**Go/No-Go Decision — [Project] — [Date]**

**Planned Launch:** [date/time]

**Gate Results:**
[table]

**Decision: GO / NO-GO / CONDITIONAL GO**

**Conditions / Blockers:**
- [item — owner — must resolve by: date]

**Next action:** [confirmed launch / rescheduled to: date]
```

---

**Next Steps:**
- Decision is GO → `launch-comms [project]` — send the announcement now
- Decision is NO-GO → `risk-register` — log the blockers as tracked risks
- Post-launch → `post-launch [project]` — schedule 1-week review

---

## Verdict file (per `_Registry/reviewer-verdict-schema.md`)

On GO (or CONDITIONAL-GO), write `<launch-doc-path>.go-nogo-passed` with the byte-exact header + scorecard:

```
<sha256>
go                  ← or conditional-go
go-nogo
<ISO 8601 UTC>

## Scorecard

| Dimension | Score (1–5) | Reason (required if ≤ 3) |
|---|---|---|
| Accuracy | <n> | — |
| Completeness | <n> | — |
| Consistency | <n> | — |
| Timeliness | <n> | — |
| Uniqueness | <n> | — |
| Validity | <n> | — |

**Composite:** <x.x> · **Pass-bar:** Completeness ≥ 4 · Validity ≥ 4 · Timeliness ≥ 4 · composite ≥ 4.0
```

NO-GO writes no verdict file; instead, log blockers to `risk-register`.
