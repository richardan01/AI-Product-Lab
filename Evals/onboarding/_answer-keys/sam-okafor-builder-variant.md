# Answer key — sam-okafor-builder-variant.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

Ground truth after onboarding Sam Okafor (Builder / AI PM). Same identity facts as Jordan Lee so **persona is the only variable** — the config must differ from Jordan's exactly where the Builder persona differs, and nowhere else.

## Expected persona routing (eval 03, 06)
- **Default persona:** Builder / AI PM.
- **Quality gates:** `/eval-review` + `/build-review` + `/test-plan` **mandatory pre-deployment**, in addition to `/peer-review` (the default reviewer gate for every persona). This is the key contrast with Jordan Lee — the heavier gate set IS expected here and its absence is a miss.
- **Commands surfaced first:** `/today`, `/evals`, `/eval-review`, `/build-review`, `/test-plan`, `/synthesize-research`.
- **Tone:** pragmatic, eval-first, model-aware; failure mode named first; no soft hedging; do not summarize the user's input back before answering.

## Expected identity (eval 01, 04)
- Name: Sam Okafor · Senior PM · Acme AI · Growth Platform.
- Manager line resolves fully: `Priya Shah → Dana Whitfield (VP Product)` — `[HEAD_OF_DEPT]` must not survive. No residual placeholders.

## Expected goals (eval 05, 08)
- 30-day outcome recognizable: **"Ship activation funnel discovery readout; align Priya on top 3 hypotheses."**
- OKR ladder-up: D30 activation 35% by Q3 (from 22%). Proof metric: D30 activation → 35% by end of Q3. Kill condition: Priya pivots team to retention (requires full thesis reset).
- Certainty bar: **80%** (note: differs from Jordan's 70% — must be captured as 80%, not defaulted). Tradeoff: quality > speed > learning. Evidence: data > expert judgment > user feedback.

## Expected stakeholders
- Priya Shah, Marco Chen, Elena Torres, Sam Rivera — as stated.

## Expected privacy boundaries (eval 11)
- Content-exclusion elicited and named in Phase 8: compensation, health, private HR feedback, sensitive customer data.

## Deferred fields
- None expected (profile complete).

## Anchor project
- Activation funnel redesign (AI-assisted onboarding). Because it is an AI feature, an AI-feature PRD template / eval framing is appropriate if a PRD is scaffolded.
