# Eval Suite — Gate Group

## What this tests

The pre-publish **gate group** (`Workflows/gate-dispatch.md` + `Workflows/gate-merge.md`, agents Riddler / Vicki Vale / Henri Ducard) is the control surface for everything that ships publicly. If its orchestration is wrong — an escalation that fires when it shouldn't, a merge that miscomputes SHIP/REVISE/BLOCK, a reviewer that contaminates another's verdict — bad artifacts ship or good ones are blocked.

This suite grades **gate behavior**, not artifact quality. Whatever verdict an artifact earns, the gate must obey its contract: parallel isolation, conditional escalation, correct merge, on-axis verdicts, specific fixes, schema conformance.

## Criteria

Eight behavioral criteria — see `criteria.md`. C2 (escalation correctness) and C4 (merge-logic correctness) are **mandatory**: a failure on either fails the suite regardless of total.

| # | Criterion |
|---|---|
| C1 | Isolation — Riddler and Vale don't reference each other |
| C2 | Escalation correctness — Ducard spawns IFF Riddler `block` + `depth_gap_flag` (mandatory) |
| C3 | `depth_gap_flag` discipline — true only for genuine depth gaps |
| C4 | Merge-logic correctness — overall verdict matches the rule (mandatory) |
| C5 | Verdict-axis adherence — each agent stays on its own axis |
| C6 | Issue specificity — every fix concrete; Vale names the exact stop-sentence |
| C7 | Schema conformance — responses parse against `gate-response.schema.md` |
| C8 | Additivity — Ducard never changes the overall verdict |

## Fixtures

Five fixtures cover every verdict path and the escalation branch — see `fixtures.md`. The battery deliberately includes F3 (a sourcing block that must **not** escalate) and F4 (a genuine depth gap that **must** escalate) to stress the `depth_gap_flag` discipline that separates them.

## Run protocol

Follows the shared protocol in `Evals/evals-hub.md` — author/grader separation is the hard requirement:

1. **Runner (dispatcher):** executes `gate-dispatch` against each fixture, spawning the gate agents in isolated Task contexts, and captures every response verbatim.
2. **Grader (separate context):** scores the captured responses against `criteria.md` only. The grader does not see the runner's reasoning or the agent prompts — it works from the response data and the rule set. This is what makes the verdict citable.
3. **Verify the mechanical criteria first:** C2 (escalation) and C4 (merge) are deterministic given the agent verdicts — the grader recomputes them by hand.

**Pass bar:** ≥ 7/8 with C2 and C4 both passing.

**When to run:** after any edit to the dispatcher, merger, or the three agent I/O blocks; after a model upgrade; or on the 60-day cadence.

## Results

Run logs live in `results/YYYY-MM-DD_<label>.md` and are **kept local — not committed to this public template** (gitignored; see `results/gate-group-results-log.md`). Record each run's scorecard, the observed verdict matrix, and any remediation in your private working copy.

## Related

[[Evals/index]] · [[Evals/eval-audit-checklist]] · [[Agents/Gotham/Computer/riddler]] · [[Agents/Gotham/Computer/vicki-vale]] · [[Agents/Gotham/Computer/henri-ducard]] · [[Workflows/gate-dispatch]] · [[Workflows/gate-merge]]
