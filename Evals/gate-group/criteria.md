# Gate Group — Eval Criteria

Eight behavioral criteria for the pre-publish gate group (`Workflows/gate-dispatch.md` + `gate-merge.md`, agents Riddler / Vicki Vale / Henri Ducard). Each is graded ✅ pass / ❌ fail / ⚠ partial **across the full fixture battery** — a single fixture is a data point, not a signal.

The eval tests **gate behavior**, not whether a given artifact "should" pass. Whether an artifact lands SHIP/REVISE/BLOCK, the gate must compute it correctly from the agents' verdicts and obey the orchestration contract.

| # | Criterion | Pass | Fail |
|---|---|---|---|
| C1 | **Isolation** | In every standard gate, Riddler's and Vicki Vale's responses contain no reference to each other's verdict, content, or existence. Each reviews the artifact independently. | Either reviewer references, anticipates, or echoes the other's verdict or findings. |
| C2 | **Escalation correctness** | Henri Ducard (Task C) is spawned **if and only if** Riddler's verdict is `block` **and** `depth_gap_flag` is `true`. No Ducard in any other case. | Ducard spawned without the trigger, or not spawned when the trigger fired, or spawned speculatively before Riddler returns. |
| C3 | **depth_gap_flag discipline** | Riddler sets `depth_gap_flag: true` only when a BLOCK reflects a genuine technical-depth gap (author can't defend under follow-up). Sourcing/citation, style, structure, or non-block verdicts → `false`. | Flag `true` on a missing-citation or style block, or `false` on a genuine faked-depth block. |
| C4 | **Merge-logic correctness** | Overall verdict matches the rule: SHIP = Riddler `pass` AND Vale `read`; BLOCK = any `block`/`bounce`/Riddler `depth_gap_flag`; REVISE otherwise. Precedence BLOCK > REVISE > SHIP. | Computed overall verdict contradicts the agent verdicts under the rule. |
| C5 | **Verdict-axis adherence** | Each agent uses only its own axis — Riddler `pass\|conditional\|block`, Vale `read\|skim\|bounce`, Ducard `drill-required\|cleared`. Vale does not adjudicate argument defensibility; Riddler does not grade reader attention. | An agent returns an off-axis verdict, or reviews on the wrong dimension. |
| C6 | **Issue specificity** | Every issue carries a concrete, actionable `fix` (a specific edit, not "tighten this"). Vale's `skim`/`bounce` names the **exact** stop-sentence. | Any issue's `fix` is vague, or a Vale bounce/skim fails to name the exact location. |
| C7 | **Schema conformance** | Each response parses against `gate-response.schema.md`: required fields present, `verdict` on-axis, `issues[]` well-formed. | Missing required field, malformed structure, or unparseable response. |
| C8 | **Additivity (Ducard)** | When Ducard runs, the overall verdict is unchanged by his `drill-required`/`cleared` — it remains BLOCK (Riddler already blocked). His output only shapes WHAT-TO-FIX priority. | Ducard's verdict upgrades or downgrades the overall verdict. |

## Threshold

**Pass bar: ≥ 7 / 8 criteria pass across the battery, with C2 and C4 mandatory.** C2 (escalation) and C4 (merge logic) are the correctness core — a failure on either fails the suite regardless of total score. The gate group is a control surface for everything that ships publicly, so the orchestration logic must be exact.

## Known soft spots (not gate bugs — log, don't fail on)

- `depth_gap_flag` is Riddler-only by schema; Vale/Ducard returning a non-false value is harmless (the merger reads it only from Riddler) but should be logged as a prompt-tightening item.
- An agent inventing a `verdict_file` path it didn't write is cosmetic; the dispatcher owns persistence.

## Related

[[Evals/gate-group/gate-group-suite]] · [[Evals/gate-group/fixtures]] · [[Evals/index]] · [[Workflows/gate-dispatch]] · [[Workflows/gate-merge]]
