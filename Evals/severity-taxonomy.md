# Severity taxonomy — "bad" vs "sad"

A single, system-wide language for how serious an eval failure or a gate finding is. Adapted from how the Claude Code team frames quality (Fiona Fung): **bad** = irrecoverable; **sad** = a recoverable pain point — *but stacked-up sads become bad.*

This taxonomy is the connective tissue between three things that were previously unrelated:
- **Eval criteria** (`Evals/*/*/criteria.md`) — each criterion is tagged `bad` or `sad`.
- **Quality gates** (`/peer-review`, `/prd-readiness`, `/go-nogo`) — the gate verdict is driven by the taxonomy, not by counting headers.
- **Monitoring** (`Evals/monitoring/`) — sampled real outputs are bucketed `bad`/`sad` so trends are legible.

---

## Definitions

### `bad` — irrecoverable, blocks the artifact's purpose

An error the reader cannot recover from, or that causes a wrong decision / broken handoff / loss of trust. In a markdown PM OS there is no live "crash," so the equivalent is: **the artifact, if shipped as-is, misleads the decider, blocks the builder, or destroys an evidence trail.**

Canonical `bad`:
- **Hallucinated finding / invented quote / invented metric** — a claim with no support in the source. (Erodes trust irrecoverably; the reader can't tell which claims to believe.)
- **Missed Must-Fix blocker** — a gate that clears an artifact which is not handoff-ready (e.g., a user story with no acceptance criteria; a payments PRD with no rollback plan).
- **Wrong go/no-go / wrong readiness verdict** — the gate says GO/READY when an unmitigated 🔴 risk exists, or NO-GO/NOT-READY on a clean artifact (the false-positive failure that makes a gate untrustworthy).
- **Unpreserved contradiction** — two conflicting sources flattened into false consensus (see `ground-truth.md` contradiction rule).
- **Privacy / safety violation** — sensitive content written where it was excluded; missing safety/compliance treatment on a risky flow.

### `sad` — recoverable pain point

An error the reader can recover from with low cost. Annoying, lowers quality, but does not by itself cause a wrong decision or broken handoff.

Canonical `sad`:
- Verbosity, preamble, filler.
- Formatting/heading drift where the information is present elsewhere.
- Soft hedging ("we should consider…") where an owner/action is otherwise clear.
- A single Should-Fix with an owner and date already attached (tracked work, not a blocker).

### The stacking rule

> "It's interesting when you stack up sads — it could generally go to bad." — Fiona Fung

**Three or more `sad` findings in one artifact escalate to a single `bad`.** A document that is individually-recoverable in ten small ways is, in aggregate, not shippable. Gates must apply this rule, not just count headers.

---

## Gate behavior (how the taxonomy drives a verdict)

| Condition | `/peer-review` | `/prd-readiness` | `/go-nogo` |
|---|---|---|---|
| Any `bad` finding | **NEEDS REVISION** | **NOT READY** | **NO-GO** |
| 0 `bad`, ≥ 3 `sad` (stacking rule) | **NEEDS REVISION** | **NOT READY** | **CONDITIONAL** |
| 0 `bad`, 1–2 `sad` | **CONDITIONAL** | **CONDITIONAL** | **CONDITIONAL GO** |
| 0 `bad`, 0 `sad` | **CLEARED** | **READY** | **GO** |

`bad` findings keep full severity **regardless of degraded mode** (see the peer-review degraded-mode rule): the cap on purely structural/template findings never applies to a `bad`.

---

## Mapping current eval criteria to the taxonomy

| Suite | Criterion | Bucket | Why |
|---|---|---|---|
| peer-review | 01-planted-blockers-caught (recall) | **bad** | A missed Must-Fix ships a broken artifact |
| peer-review | 02-no-hallucinated-findings | **bad** | Fabricated findings erode trust |
| peer-review | 03-verdict-matches-rubric | **bad** | A wrong verdict makes the gate untrustworthy |
| peer-review | 04-clean-artifact-not-flunked | **bad** | False-positive flunk of clean work = gate noise |
| peer-review | 05-fix-checklist-actionable | **sad** | Vague fix item is recoverable |
| research-synthesis | 01-themes-grounded-in-evidence | **bad** | Ungrounded theme = hallucination |
| research-synthesis | 02-no-invented-quotes | **bad** | Invented quote = hallucination |
| research-synthesis | 04-conflicting-signals-named | **bad** | Flattened contradiction = lost signal |
| research-synthesis | 03 / 05 / 06 / 07 | **sad** | Quality/specificity gaps, recoverable |
| onboarding | 02-confirmation-before-write | **bad** | Writing files without consent is irrecoverable |
| onboarding | 11-privacy-boundaries-enforced | **bad** | Privacy violation |
| onboarding | 01 / 04 (placeholders) | **bad** | Invented identity / residual placeholder misleads |
| onboarding | others | **sad** | Specificity/interactivity polish |
| prd-readiness | 01-verdict-correct, 02-no-hallucinated-gaps, 03-ai-gates-applied, 04-clean-prd-not-flunked | **bad** | Same logic as the peer-review meta-eval |
| go-nogo | 01-verdict-correct, 02-no-hallucinated-blockers, 03-clean-not-flunked, 04-red-risk-blocks-go | **bad** | A wrong launch verdict ships a broken release or blocks a good one |
| research-sufficiency | 01-verdict-correct, 02-no-hallucinated-gaps, 03-clean-not-flunked, 04-insufficiency-detected | **bad** | Clearing thin research drives a wrong decision |
| build-review | 01-verdict-correct, 02-no-hallucinated-issues, 03-clean-not-blocked, 04-unrun-or-silent-failure-blocked | **bad** | A wrong build verdict ships an unrun/silent-failure artifact |

When adding a new criterion, tag it `bad` or `sad` in its `criteria.md` header and add a row here.
