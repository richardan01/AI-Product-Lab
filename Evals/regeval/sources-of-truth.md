# RegEval sources of truth

**Purpose:** Defines the priority hierarchy for what the judge consults when classifying an item. Enforced procedurally by `skills/judge-workflow.md`. Consult this document when updating skills or scaffold to ensure the hierarchy is respected.

---

## Priority order

| Priority | Source | Consult when |
|---|---|---|
| **1 — Primary** | Enumerated abstention triggers (rubric-graded-v4 KEEP scaffold; carried into skills-v1) | Always. Check all five triggers before any other source. Triggers fire or don't fire based on the text alone. |
| **2 — Secondary** | HK SFC regulatory reference (`skills/hk-sfc-reference.md`) | When obligation identification is ambiguous — i.e., you are not sure whether an obligation is "known" in HK, or what compliant conduct looks like for a specific regime. |
| **3 — Tertiary** | Edge-case pattern library (`skills/ambiguous-patterns.md`) | Only when primary + secondary are inconclusive and the item pattern resembles a known ambiguous case from the gold dataset. |
| **4 — Jurisdiction check** | Jurisdiction scope (`skills/jurisdiction-scope.md`) | When the text references offshore entities, foreign regulators, or cross-border arrangements. Used at Step 2 of the workflow; can be consulted earlier if jurisdiction is immediately unclear. |
| **Fallback** | Abstain (`unclear`) | If after consulting all four sources above the classification is still indeterminate, label unclear. Only fire if a trigger genuinely applies — not as a hedge. |

---

## Why this order matters

The Anthropic analytics blog identified **concept-entity ambiguity** (multiple plausible interpretations of what an obligation means) as the primary failure mode. Enforcing a strict consultation hierarchy solves this:

- The trigger rubric (Priority 1) always decides first — no freestyle reasoning before checking triggers.
- The regulatory reference (Priority 2) narrows the interpretation space for the obligation before the judge commits.
- The pattern library (Priority 3) catches close calls that have been adjudicated before — it prevents re-litigating settled edge cases.
- Jurisdiction (Priority 4) is a filter that often short-circuits: if trigger 4 fires early, skip priorities 2–3.

---

## Governance

- Updates to the trigger rubric (Priority 1) require a new KEEP experiment. Do not edit `current.md` directly; run a `/regeval-run` candidate.
- Updates to skills (Priorities 2–4) do not require a full re-run but SHOULD be validated by running the next scheduled experiment against the updated skills.
- Any relabeling of gold items must be logged in `inputs/corrections-log.md` before a new experiment is run.
- Rubric changes must be human-authored. Do not auto-generate rubric variants (blog-validated: auto-generation encodes existing ambiguities).
