# Dimension grid — onboarding fixtures

Modeled on the `generate-synthetic-data` skill from `hamelsmu/evals-skills`. Instead of authoring fixtures from intuition, enumerate the dimensions that meaningfully change runner behavior, then sample tuples. Coverage gaps become visible.

## Dimensions

| # | Dimension | Values | Why it matters |
|---|---|---|---|
| D1 | Persona | Executive operator / Researcher / Coach / Builder / AI PM / Minimalist / Custom | Different quality gates, different surfaced commands, different default tones. The single biggest behavior-changing input. |
| D2 | Identity completeness | Fully provided / Some deferred / Mostly deferred | Stresses "no invented identity" (eval 01) and "deferred fields annotated" (eval 04 C5). |
| D3 | OKR alignment provided | Provided / Skipped by user / User unsure | Stresses Phase 5 (eval 08). |
| D4 | Thought-framework answers | Provided / Skipped / Partial | Stresses Phase 5B (eval 09). |
| D5 | Taste preferences | Provided / "I don't know yet" / Contradictory across phases | Stresses Phase 2 (eval 10). |
| D6 | Quality-gate selection | Persona-default / Explicit override / Ambiguous | Stresses eval 06; especially adversarial when persona defaults differ from explicit choice. |
| D7 | Privacy boundaries | None set / Standard / Sensitive domain (legal, health, comp) | Stresses eval 11. |
| D8 | Anchor project | Named real project / "Not sure yet" / Multiple candidates | Stresses brief-creation guardrail and routing. |
| D9 | Re-run behavior | First run / Re-run with same persona / Re-run with new persona | Catches silent persona preservation (eval 03, observed failure mode #12). |
| D10 | Polite-but-non-explicit acknowledgements | None / Mid-flow / At Phase 8 | Stresses confirmation gates (eval 02, criterion 5 — "polite acks ≠ authorization"). |

## Coverage map — current fixtures

| Fixture | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| `jordan-lee-profile.md` | Executive | Full | Provided | Provided | Provided | Default | None | Real | First run | None |
| `sam-okafor-builder-variant.md` | Builder / AI PM | Full | Provided | Provided | Provided | Default | Standard | Real | First run | None |
| `riley-park-minimalist.md` | Minimalist | Mostly deferred | Skipped | Skipped | "Don't know" | Default | None | Not sure | First run | None |
| `morgan-chen-custom-persona.md` | Custom | Full | Provided | Provided | Provided | Explicit override | Sensitive | Real | First run | None |
| `dev-rerun-persona-switch.md` | Executive → Builder/AI PM | Full | Provided | Provided | Provided | Default → Default | Standard | Real | Re-run new persona | None |
| `taylor-polite-acks.md` | Builder | Full | Provided | Provided | Provided | Default | Standard | Real | First run | At Phase 8+9 |
| `wei-ambiguous-anchor.md` | Researcher | Full | Provided | Provided | Provided | Ambiguous | Standard | Multiple candidates | First run | None |

## Visible gaps (parking lot, ordered by leverage)

1. **D2 = Mostly deferred + D1 = Builder / AI PM.** No fixture stresses the heavier Builder/AI PM gate defaults *under deferral pressure* — does the assistant fall back to heavy gates or actually preserve the user's deferrals?
2. **D7 = Sensitive domain + non-Executive persona.** Only the custom persona stresses sensitive boundaries. Does a heavier persona's tone override the privacy boundaries, or respect them?

## Previously addressed (closed gaps)

| Gap | Fixture added |
|---|---|
| D9 = Re-run with new persona | `dev-rerun-persona-switch.md` |
| D10 = Polite-but-non-explicit acknowledgements | `taylor-polite-acks.md` |
| D8 = Multiple candidate projects | `wei-ambiguous-anchor.md` |
| D6 = Ambiguous gate selection | `wei-ambiguous-anchor.md` |

## Anti-patterns when authoring fixtures

- **Adding a fixture without naming the dimension it covers.** If you can't fill in a row in the coverage map, the fixture is decorative.
- **Authoring two fixtures that differ only in cosmetic details** (name, company, role) but trigger the same code paths. Two fixtures, one signal.
- **Building a fixture to make a known-good behavior look thorough.** Fixtures exist to catch bugs, not to inflate pass rates.

## Sampling policy

When the matrix grows large, do not exhaustively enumerate. Sample by:

1. Always cover **every value of D1** (persona) at least once — it's the dominant variable.
2. Cover **every named failure mode** in the suite README with at least one fixture that targets it.
3. Beyond that, prefer **tuples that combine two adversarial dimensions** (e.g., Builder/AI PM + deferred fields; Custom + sensitive privacy). Single-dimension fixtures usually grade only the dimension they target.
