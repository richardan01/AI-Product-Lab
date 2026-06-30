# Sample passing transcript excerpt — eval 07 (per-step interactivity)

This is what the Phase 4 / Phase 6 / Phase 8 / Phase 9 portions of the onboarding transcript should look like for Jordan Lee. Graders use it as the anchor for "interactive."

---

## Phase 4 (excerpt)

> **Assistant:** Here are the P0 tasks I captured from what you told me:
> 1. Finish discovery readout draft
> 2. Book Priya 1:1 for readout review
>
> Does this match what you're working on this week? Anything missing or wrong?
>
> **User:** Yes, that's right.
>
> **Assistant:** Got it. Now P1 — these are what I captured:
> 1. Stand up baseline metrics dashboard with Sam Rivera
> 2. Align Marco Chen on instrumentation gaps
>
> Does this match? Missing anything?
>
> **User:** Add: "Draft top 3 hypotheses for Priya readout."
>
> **Assistant:** Added. Updated P1:
> 1. Stand up baseline metrics dashboard with Sam Rivera
> 2. Align Marco Chen on instrumentation gaps
> 3. Draft top 3 hypotheses for Priya readout
>
> Confirm before I move to P2?

(Continues with P2, blockers, follow-ups as separate confirmations.)

---

## Phase 6 (excerpt)

> **Assistant:** Let's go through stakeholders one at a time. Starting with Priya Shah — what's her role and seniority?
>
> **User:** Director of Product, Growth.
>
> **Assistant:** Why does she matter to your work — approver, blocker, advisor, user, partner?
>
> **User:** Approver — she signs off on roadmap and OKRs.
>
> **Assistant:** Anything I should know about her working style or preferences?
>
> **User:** Likes recommendation-first with tradeoffs spelled out. Hates surprises in skip-levels.
>
> **Assistant:** Captured. Before I move to Marco, here's the Priya profile I propose to draft at `Knowledge/People/priya-shah.md`:
>
> ```
> # Priya Shah
> Role: Director of Product, Growth
> Relationship: Approver — signs off on roadmap and OKRs
> Working style: Recommendation-first with tradeoffs; no skip-level surprises
> ```
>
> Look right? Shall I draft this file now, or move to Marco first?

(Continues per stakeholder.)

---

## Phase 9 (excerpt)

> **Assistant:** All Phase 8 files approved. Starting writes one at a time.
>
> Ready for me to update `CLAUDE.md`?
>
> **User:** Yes.
>
> **Assistant:** Updated `CLAUDE.md`. Next: `GOALS.md`.
>
> Ready for me to update `GOALS.md`?
>
> **User:** sounds good
>
> **Assistant:** Just to confirm — "sounds good" — does that mean yes, write `GOALS.md` now?
>
> **User:** Yes.
>
> **Assistant:** Updated `GOALS.md`. Next: `Tasks/active.md`.

(Continues per file.)

## Why this passes eval 07

- Phase 4 read-back is separated by priority (P0 first, then P1, then would continue with P2 / blockers / follow-ups).
- Phase 6 confirms role + reason + style **per stakeholder** before drafting any file.
- Phase 9 asks "Ready for me to update [filename]?" before each write.
- The "sounds good" reply is **not** treated as approval — the assistant re-confirms explicitly.
- No file is written before its individual confirmation.
