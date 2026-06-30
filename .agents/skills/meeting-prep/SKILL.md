# Meeting Prep

**Agent:** Alfred → Oracle — see `Agents/Gotham/Computer/alfred.md` for full context.
**Sub-agent:** Spawn `stakeholder-profiler` to build rich person context in parallel if preparing for a complex meeting.

Usage: "meeting prep [name]" (e.g., "meeting prep [YOUR_MANAGER]", "meeting prep [LIFECYCLE_PM]")

Steps:

1. **Find the person** in `Knowledge/People/` based on the name argument
2. **Pull meeting history** from `Meetings/1on1s/[name].md` if it exists
3. **Read current context** from `Tasks/active.md` and `GOALS.md`
4. **Read project context** from `Projects/[YOUR_ANCHOR_PROJECT]/brief.md` if relevant

Then generate a prep doc:

---

**Meeting Prep: [Name] — [Date]**

**Their role:** [From Knowledge/People/]
**Last met:** [From meeting history, or "First meeting"]

**My agenda (what I want to cover):**
1. [Most important topic — decision needed, update to give, ask to make]
2.
3.

**Updates to give them:**
- [Progress on things they care about]
- [Any commitments I made last time — did I follow through?]

**Questions to ask:**
- [Things I genuinely want to learn from them]
- [Open items from last meeting]

**Decisions needed:**
- [Anything that requires their input or approval]

**What they likely care about:**
- [Based on their role and past interactions — tailor the conversation]

**Things to avoid:**
- [Known sensitivities or topics that derail]

---

After generating the prep doc, ask:
- "Anything specific you want to add or change before this meeting?"
- "Any background context I should know?"
