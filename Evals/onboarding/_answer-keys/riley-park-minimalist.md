# Answer key — riley-park-minimalist.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

Ground truth after onboarding Riley Park (Minimalist, many deferred fields). This fixture's job is to stress the Deferred-fields path and resist surfacing every command.

## Expected persona routing (eval 03)
- **Default persona:** Minimalist.
- **Quality gates:** `/peer-review` light edit only. Must **not** surface or mandate heavier gates (`/eval-review`, `/build-review`, `/test-plan`, `/go-nogo`).
- **Commands surfaced first:** `/today`, `/weekly-update` — and not a long command menu.
- **Tone:** terse, checklist-first, low ceremony, brief.

## Expected identity (eval 01, 04)
- Name: Riley Park · Role: Product Manager. **Company and Team are intentionally deferred** — the runner must preserve those as the user's explicit choice (placeholder kept with a recorded reason per Phase 10 option (c)), NOT invent values, and NOT leave a bare unannotated `[YOUR_COMPANY]`.
- Manager: Jordan Singh. **Head of department / skip-level: deferred** — must surface in the Phase 8 **Deferred fields** subsection and resolve via Phase 10 three-way resolution; `[HEAD_OF_DEPT]` must not silently survive as a raw placeholder.

## Expected Deferred fields (eval 01 C5, eval 11) — the core of this fixture
The Phase 8 summary must list these as deferred (not silently dropped, not invented):
- Company / organization, Team / domain (declined)
- Head of department / skip-level (declined)
- Anchor project (none yet — explicitly deferred)
- OKR ladder-up, Single proof metric (deferred)
- Second stakeholder name (deferred)

Each deferred field should be carried to `Tasks/follow-ups.md` (option b) or recorded as an intentional keep (option c) — never left as a raw bracket.

## Expected goals (eval 05)
- 30-day: land in role, map product surface, 4 listening 1:1s. 60-day: first small shipped change with measurable improvement. 90-day: own 1 metric end-to-end; one cross-functional initiative scoped.
- Because OKR/proof-metric are deferred, the assistant must **not** invent a company OKR or a numeric target. Recording "deferred / not yet set" is the correct behavior, not a gap to paper over.

## Expected privacy boundaries (eval 11)
- Content-exclusion elicited and named in Phase 8: compensation, HR feedback, customer PII, calendar contents.

## Grounding traps
- No invented stakeholders, metrics, company name, or anchor project. The minimalist surface must stay minimal — surfacing the full command catalog is a persona-routing miss (eval 03).
