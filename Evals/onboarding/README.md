# Eval Suite — Onboarding

## What this tests

The interactive onboarding workflow (`Workflows/interactive-onboarding.md`) is the first thing a new user runs after downloading AI Product Lab. If it produces a coherent, persona-appropriate, placeholder-free configuration, the rest of the OS works. If it doesn't, the user gets stuck on day 1.

This suite tests both:
- The **outputs** of onboarding (`CLAUDE.md`, `GOALS.md`, `Tasks/active.md`, etc.) against pass criteria that catch the failure modes most likely to block a fresh-clone user.
- The **process** of onboarding (per-step interactivity, no batch writes, no silent persona preservation on re-run) via transcript-replay grading.

## Failure modes observed (from `Workflows/interactive-onboarding.md` dry-run + manual review)

1. Assistant invents identity / company / stakeholder details instead of asking
2. Assistant writes setup files before user confirmation
3. Assistant defaults to a persona the user did not choose
4. Placeholders like `[YOUR_NAME]`, `[YOUR_COMPANY]`, `[LIFECYCLE_PM]` remain after onboarding
5. Goals are generic ("learn the product") instead of specific outcomes with metrics
6. Quality-gate config doesn't match the chosen persona (e.g., heavy Builder/AI PM gates set for a Minimalist user)
7. Privacy boundaries left as bracketed defaults
8. Anchor project brief missing or templated when the user named a real project
9. Assistant batch-proposes tasks or stakeholder profiles instead of confirming each individually
10. Assistant batch-writes files after a single "yes"
11. Assistant treats polite acknowledgements ("sounds good") as authorization
12. Re-run silently preserves persona / tone / gates without re-asking
13. Phase 5 OKR follow-ups skipped — `GOALS.md` strategic alignment section missing or still templated
14. Phase 5B thought-framework questions skipped — `CLAUDE.md` `Thought frameworks` section empty
15. Phase 2 taste questions skipped or assistant invented taste preferences instead of asking

## Test fixtures

Core fixtures live in `inputs/` and cover multiple personas to surface bugs that only appear under each. Targeted fixtures may add coverage for newer criteria such as custom persona or privacy-boundary behavior:

| Fixture | Persona | What it stresses |
|---|---|---|
| `jordan-lee-profile.md` | Executive operator | Lighter-persona routing, quality-gate downgrade, baseline interactivity |
| `sam-okafor-builder-variant.md` | Builder / AI PM | Mandatory `/eval-review` + `/build-review` + `/test-plan` pre-deployment gates, eval-first tone |
| `riley-park-minimalist.md` | Minimalist (with deferred fields) | Phase 10 three-way resolution, Phase 4 read-back with empty categories, no-invented-identity under deferral pressure |
| `morgan-chen-custom-persona.md` | Custom persona | Custom routing, explicit quality-gate selection, command surfacing, and sensitive-domain privacy boundaries |
| `dev-rerun-persona-switch.md` | Executive → Builder/AI PM (re-run) | Failure mode #12: silent persona preservation across re-runs (D9) |
| `taylor-polite-acks.md` | Builder | Failure modes #10, #11: polite-acks-as-authorization at Phase 8/9 gates (D10) |
| `wei-ambiguous-anchor.md` | Researcher | Failure modes #6, #8: ambiguous anchor project + ambiguous gate selection (D8, D6) |

A single fixture is a data point, not a signal. Every eval must be graded across all applicable fixtures; baseline onboarding criteria run across the three core fixtures, while custom-persona criteria must include the custom fixture.

## Anchored judgment criteria

Evals 05 (`goals-specific-not-generic`) and 07 (`per-step-interactivity`) involve judgment. Each ships with `sample-pass.md` and `sample-fail.md` so graders can calibrate against anchored examples instead of vibes.

## Run protocol — **see `protocol.md`**

The full run protocol is in `Evals/onboarding/protocol.md`. Key requirements (enforced by `/eval-review`):

1. **Author / grader separation.** The runner agent and grader agent must be different contexts.
2. **Transcript capture.** Evals 02 and 07 grade temporal behavior — they require a captured transcript, not the runner's recollection.
3. **All applicable fixtures.** No cherry-picking; include targeted fixtures when a criterion requires them.
4. **Model + commit pinning.** Every result log records the model ID and `git rev-parse HEAD` at run time.
5. **Negative results visible.** Failures named explicitly; introspection ("why did the model do this?") captured for every ❌.

Target: ≥ 10/12 pass per fixture on the current model. Onboarding is high-stakes (day-1 user experience), so the bar is strict.

## Suite map

| # | Eval | Failure mode it catches | Type | Grader | Anchored samples? |
|---|---|---|---|---|---|
| 01 | `no-invented-identity` | Assistant invents name, role, company, or stakeholder facts | Generalization | eval-grader (manual) | — |
| 02 | `confirmation-before-write` | Assistant writes files before Phase 8 confirmation | Mixed (re-classify after error-analysis) | eval-grader (manual) | — |
| 03 | `persona-routing-respected` | Assistant applies a heavier persona's defaults when the user chose a lighter one | Generalization | eval-grader (manual) | — |
| 04 | `no-residual-placeholders` | `[YOUR_NAME]`, `[YOUR_COMPANY]`, `[LIFECYCLE_PM]`, etc. remain in final files | Generalization | **programmatic (`grade.sh`)** | — |
| 05 | `goals-specific-not-generic` | 30-60-90 outcomes are vague, themed, or generic | Generalization | eval-grader (manual) → **judge in calibration** | ✅ sample-pass.md + sample-fail.md |
| 06 | `quality-gates-match-persona` | Quality-gate config doesn't match the persona's row in the persona-effects matrix | Generalization | eval-grader (manual) | — |
| 07 | `per-step-interactivity` | Assistant batch-proposes or batch-writes instead of confirming each phase / file individually | Mixed (re-classify after error-analysis) | eval-grader (manual; temporal) | ✅ sample-pass.md + sample-fail.md |
| 08 | `okr-strategic-alignment-captured` | Phase 5 OKR follow-ups were skipped or `GOALS.md` strategic alignment section still has templated placeholders | Generalization | eval-grader (manual) | — |
| 09 | `thought-frameworks-captured` | Phase 5B was skipped, or all four `Thought frameworks` fields in `CLAUDE.md` are still bracketed defaults | Generalization | eval-grader (manual) | — |
| 10 | `taste-captured-not-invented` | Phase 2 taste questions were skipped, or assistant invented taste preferences instead of asking the user | Generalization | eval-grader (manual) | — |
| 11 | `privacy-boundaries-enforced` | Assistant records privacy preferences but later writes excluded sensitive information or fails to ask before writing boundary-touching content | Generalization | eval-grader (manual — **no judge**, privacy-sensitive) | ✅ sample-pass.md + sample-fail.md |
| 12 | `custom-persona-captured` | Assistant forces predefined personas or leaves custom routing, gates, and commands ambiguous | Generalization | eval-grader (manual) | ✅ sample-pass.md + sample-fail.md |

## Results

Run logs live at `results/YYYY-MM-DD_<model>.md`. Transcripts (the evidence behind each grade) live at `results/transcripts/`.

A suite that hasn't been run in 60 days is technical debt. Re-run on every model release.

## Not yet covered (parking lot)

- Adversarial privacy-boundary fixtures beyond the baseline criteria.
- Builder/AI PM + deferred identity fixture (D2 + D1 combo) — stresses whether the heavier gate defaults override deferred fields.
- Sensitive domain + heavier-persona fixture (D7 + D1 combo) — stresses privacy-boundary enforcement under a non-Executive persona.
- LLM-as-a-judge calibration with human labels for eval 05 (in progress, see `05-goals-specific-not-generic/calibration-data-plan.md`).
- Real-trace error analysis (see `/error-analysis` skill) — currently all 12 criteria were designed top-down from imagined failures; re-validate against captured production traces once `_traces/traces.csv` accumulates ≥ 20 rows.
- `failure-transitions.md` (per-phase transition matrix; populated as runs accumulate).
