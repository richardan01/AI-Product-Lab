# Today

**Agent:** Alfred — see `Agents/Gotham/Computer/alfred.md` for full context.

Read the following files to prepare [YOUR_NAME]'s daily to-do list:
1. `Tasks/active.md` — current sprint tasks, blockers, and completed items
2. `GOALS.md` — 30-60-90 day goals and current focus areas
3. Check `Meetings/` for any meetings today (if accessible)

Then output a daily to-do list in this format:

---

**Today — [Today's Date]**

**Done:**
- [Completed tasks or meaningful progress from Tasks/active.md]

**To Do Today:**

**#p0 — Must do:**
- [Tasks tagged #p0 from active.md, highest leverage first]

**#p1 — Should do:**
- [Tasks tagged #p1 from active.md]

**#p2 — Nice to do:**
- [Tasks tagged #p2 from active.md, only if bandwidth]

**Blockers:**
- [Anything in the Blocked section of active.md]
- [Flag if any active task has been in-progress for too long without movement]

**On my radar:**
- [Any upcoming deadlines, meetings, or decisions needed]

---

After showing the list, ask:
- "Any updates to today's tasks or priorities?"
- "Anything new to add to the backlog?"

If the user confirms updates, edit `Tasks/active.md` accordingly.

---

**What to run next:**
- Monday or Friday → `roadmap review` to check milestone and project status
- [YOUR_MANAGER] 1:1 this week → `meeting prep [YOUR_MANAGER]` to prep agenda and open items
- Tasks feel stale or priorities shifted → `groom` to clean up the backlog
- Want full system context → `briefing` for tasks + metrics + project status in one view
