# Roadmap Review

**Agent:** Strategy & Roadmap (Bruce Wayne voice) — see `Agents/README.md` voice map.
**Sub-agent:** Spawn `project-scanner` to assess milestone status across projects.

Usage: "roadmap review" — weekly check-in on roadmap progress and deliverable status. Best run Monday or Friday.

## Steps

1. **Pull current state** — read:
   - `Tasks/active.md` — what's in flight
   - `Tasks/backlog.md` — what's queued
   - `Projects/[YOUR_ANCHOR_PROJECT]/brief.md` — milestone status
   - `GOALS.md` — 30-60-90 day targets
   - `Knowledge/Reference/metrics/latest.md` — key metrics (if available)

2. **Task–OKR alignment check** — for each task in `Tasks/active.md`, verify it maps to at least one OKR or milestone in `GOALS.md`. Flag orphaned tasks.

| Task | Maps to OKR / Milestone | Aligned? |
|------|------------------------|----------|
| | | ✓ / ✗ Orphaned |

   - **Orphaned task** = no clear link to any current goal → deprioritize or drop
   - If >2 orphaned tasks found → flag: "Active work has drifted from OKRs — reprioritize before proceeding"

3. **Review milestones** — for each active milestone:

| Milestone | Target Date | Status | On Track? | Notes |
|-----------|-------------|--------|-----------|-------|
| | | | 🟢/🟡/🔴 | |

4. **Identify risks & blockers** — for each 🟡 or 🔴 item:
   - Root cause
   - What's needed to unblock
   - Who to talk to
   - Whether timeline adjustment needed

5. **Reprioritize active tasks:**
   - Archive completed items
   - Pull next-up from backlog
   - Ensure alignment to nearest milestone
   - Confirm: highest-leverage work in focus?

6. **Prepare for [YOUR_MANAGER]** (if 1:1 or weekly update coming):
   - 2–3 key updates
   - Decisions needed from them
   - Suggest running `/weekly-update` to draft the update

## Output Format

```
**Roadmap Review — [Date]**

**Overall Status:** [🟢/🟡/🔴]

**Milestones:**
[table]

**Risks & Blockers:**
- [risk/blocker with mitigation]

**Task Reprioritization:**
- Archived: [items]
- Pulled in: [items]
- Focus this week: [top 2-3 items]

**For [YOUR_MANAGER]:**
- [key updates / decisions needed]
```

After review, offer:
- "Update `Tasks/active.md` with these changes?"

**Next Steps (run one of these now):**
- `weekly update` — draft your [YOUR_MANAGER] update based on this review
- `[YOUR_ANCHOR_PROJECT]-status` — drill into project detail if any milestone is 🟡 or 🔴
- `meeting prep [YOUR_MANAGER]` — prep your 1:1 if happening this week
