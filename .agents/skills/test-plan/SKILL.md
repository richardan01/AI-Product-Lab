# Test Plan

**Agent:** QA & Acceptance Tester (Riddler voice) — see `Agents/README.md` voice map.

Build a structured test plan from the acceptance criteria in [feature]'s PRD.

## Steps

1. **Read:**
   - `Projects/[project]/prd-[feature].md` — acceptance criteria (required)
   - `Knowledge/Reference/data-architecture/` — data schema (for data features)
   - `Projects/[project]/brief.md` — launch context and timeline

2. **For each acceptance criterion, create a test case:**

| # | Acceptance Criterion | Test Steps | Expected Result | Priority | Pass/Fail |
|---|---------------------|------------|-----------------|----------|-----------|
| 1 | | 1. ... 2. ... | | P0/P1/P2 | |

3. **Categorize tests:**
   - **Happy path** — expected normal flow works end-to-end
   - **Edge cases** — empty states, boundary values, missing data
   - **Data quality** — completeness, nulls, schema validation, duplicate records
   - **Access / permissions** — right users see right data, wrong users cannot
   - **Privacy / PII** — sensitive fields masked, excluded from exports

4. **Output:**

```
**Test Plan — [Feature] — [Date]**

**PRD Source:** [file path]
**Total Test Cases:** [n]
**P0 Cases (launch-blocking):** [n]

**Test Cases:**
[table]

**Data Quality Checks:**
- [ ] Field completeness >95% for: [key fields]
- [ ] No unexpected nulls in: [required fields]
- [ ] PII fields confirmed masked: [list fields]
- [ ] Schema matches expected: [source system]

**Sign-off Required From:** [relevant team members]
**UAT Target Date:** [date — should be 5+ days before launch]
```

5. **Save to** `Projects/[project]/test-plan.md`

---

**Next Steps:**
- `uat-check [feature]` — run through this checklist when the feature is ready to test
- `data-quality-check [source]` — validate data ingestion specifically
- `go-nogo [project]` — share UAT results with Launch Manager for launch decision
