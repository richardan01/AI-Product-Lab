# Answer key — activation-funnel-interviews.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

Ground truth for grading a synthesis of the 4 activation interviews. Match on substance, not phrasing. The synthesis need not use these exact labels, but a passing synthesis should land these themes, keep pain points distinct, name the contradictions, and invent nothing.

## Expected themes (each must cite real evidence)
- **T1 — Sample/demo data is the activation unlock; real-data-first means a blank screen.** Power user (I2) self-discovered the sample data set and that's how they learned the product; new user (I1) saw "zeros everywhere" with no data connected and bounced. Onboarding does **not** surface sample data.
- **T2 — Activation is role-mediated and onboarding is role-blind.** I1 ("they don't tell me what setup means for someone in my role"), I4 CSM ("no 'start here for a CSM' path"; 8-min help video showed the wrong use case), I3 ops ("I'm not really your target user"). Generic guidance is the blocker for high-intent users.
- **T3 — Activation is gated by dependencies / other people, and its definition varies by persona.** I1 needed the data team first; I3 was set up by their team and "activates" by reading an export, not by using the UI.

## Expected pain points (must be distinct from the theme labels)
- First-session blank dashboard (zeros) when no data is connected (I1).
- Permissions / configuration flow is confusing (I2 "almost didn't connect real data either"; I4 "all these configuration options and I don't know which are relevant").
- Generic help content (8-min video, wrong use case) (I4).
- "Complete your setup" emails with no role context (I1).

## Conflicting signals (must be named, not flattened — eval 04)
- **Is permissions/config friction a blocker?** I2 (power user) pushed through it; I1 and I4 were blocked by it. Same friction, opposite outcomes depending on motivation.
- **What does "activation" even mean?** I3 (ops manager) says reading the weekly export *is* their use — directly contradicts a UI-first "complete a first action" activation definition. Preserve this; do not declare a single activation definition.

## Expected implications
- Surface sample/demo data in the onboarding flow (T1).
- Build role-specific activation paths / "start here for [role]" (T2).
- Define activation per persona; some personas activate via output, not UI (T3).

## Grounding / hallucination traps (eval 01, 02, 07)
- There are **no numeric metrics** in this corpus (no conversion %, no activation rate). Inventing any quantified finding is a Fail.
- Only 4 interviews — do not generalize to "most users" beyond what the interviews support.
- "zeros everywhere" appears in I1 only — do not attribute it to other participants.
- Acceptable theme count: ~3 (the above). 5+ thin themes padded to fill space is a signal of generic synthesis.
