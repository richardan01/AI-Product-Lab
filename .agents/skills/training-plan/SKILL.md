# Training Plan

**Agent:** Enablement & Change Manager (Robin voice) — see `Agents/README.md` voice map.

Build a role-specific training plan for [feature] launch. Run this at least 1 week before the launch date.

## Steps

1. **Read:**
   - `Knowledge/People/team.md` — team member roles and use cases
   - `Projects/[project]/brief.md` or `prd-[feature].md` — what the feature does and who uses it

2. **Map users to what they need to DO (not just know):**

| User | Role | What they'll use this for | Training needed | Format | By when | Sign-off criteria |
|------|------|--------------------------|-----------------|--------|---------|-------------------|
| [LIFECYCLE_PM] | Lifecycle | | | Live walkthrough / Loom / Written guide | | Can do X without help |
| [WEBSITE_PM] | Website | | | | | |
| [PAID_ADS_PM] | Paid Ads | | | | | |
| [CONTENT_PM] | Content | | | | | |

   Only include users who will actually touch the feature — skip irrelevant rows.

3. **Define materials needed:**
   - Written step-by-step guide (for reference post-training)
   - Live walkthrough session (30 min max — demo + hands-on)
   - Sandbox / practice environment (if available)

4. **Output:**

```
**Training Plan — [Feature] — [Date]**

**Launch Target:** [date]
**Training Deadline:** [date — 3 days before launch minimum]

**By User:**
[table]

**Materials to Create:**
- [ ] Written guide for [feature] — owner: [YOUR_NAME]
- [ ] Loom walkthrough for [feature] — owner: [YOUR_NAME]
- [ ] Sandbox access confirmed — owner: [eng/vendor]

**Schedule:**
- [ ] Walkthrough with [LIFECYCLE_PM]: [date]
- [ ] Walkthrough with [WEBSITE_PM]: [date]
- [ ] Walkthrough with [PAID_ADS_PM]: [date]

**Readiness Gate:** All users confirmed ready before UAT sign-off
```

5. **Save to** `Projects/[project]/training-plan.md`

---

**Next Steps:**
- `user-guide [feature]` — draft the written reference guide
- `change-impact [project]` — assess if this changes existing workflows for any user
- `adoption-check` — schedule a 4-week post-launch adoption review
- `go-nogo [project]` — training completion is a launch gate — confirm status there
