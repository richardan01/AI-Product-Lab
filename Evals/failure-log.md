# Eval failure log

Append-only. One row per failed criterion per run. Captures what was fixed and whether the fix held on re-run.

---

| Date | Suite | Criterion | Agent file edited | Re-run date | Re-run result |
|---|---|---|---|---|---|
| 2026-06-10 | gate-group | C1 isolation (⚠ F4 Vale named Riddler by role) | `vicki-vale.md` — hard "never name other gate agents" rule added 2026-07-06 | 2026-07-06 (r1+r2) | ✅ CLOSED — C1 passed clean across both runs, 5/5 fixtures each |
| 2026-06-10 | gate-group | C7 schema conformance (⚠ F5 Vale issue fields off-contract) | `vicki-vale.md` + `gate-response.schema.md` — schema embedded verbatim + bare-JSON output-format rule added 2026-07-06 | 2026-07-06 (r1+r2) | ✅ CLOSED for Vale (5/5 clean in r2, was 5/5 fenced in r1). ⚠ NEW residual: Ducard (not part of the original 2026-06-10 finding) prepends prose reasoning before his JSON in both r1 (fenced) and r2 (unfenced but prose-prefixed) — same root defect, different shape. Suite still passes (7/8, C2+C4 mandatory clean) because this is a C7 partial, not a mandatory-criterion failure. |
| 2026-06-10 | gate-group | Fixture integrity (F2 source missing) | `Evals/gate-group/fixtures.md` — F2 README inlined verbatim ✅ | 2026-07-06 | ✅ CLOSED — verified present and used in both r1 and r2 dispatches |
| 2026-07-06 | gate-group | C5 verdict-axis adherence (Vale F4 used logical-validity language — "non-sequitur," "not the same claim" — instead of reader-experience framing) | `vicki-vale.md` — hard reader-experience-lane rule + banned vocabulary list added same day | 2026-07-06 (r2) | ✅ CLOSED — r2 F4 response reframes entirely in trust/attention terms; clean across all 5 r2 fixtures |
| 2026-07-06 | gate-group | C7 residual — Henri Ducard prepends narrated reasoning before the bare JSON object (both F4 and F5, r2) | Not yet applied — grader recommends a stronger persona instruction ("reason silently; first char of output must be `{`") plus a mechanical parse-retry backstop in `gate-dispatch.md` | — | ⏳ OPEN — non-blocking (suite passes 7/8 with mandatory C2/C4 clean); scoped as a follow-up, not re-opening this closure |
| 2026-07-14 | peer-review | 02-no-hallucinated-findings (❌ synthesis-support-tickets + weekly-update-clean) — hallucinated Must Fix "add rollback/failure-handling plan" on 2 of 3 fixtures | `.claude/skills/peer-review/SKILL.md` Pass 3 Rule 2 — scope qualifier added (`e206533`): rule fires only when the artifact IS the design/handoff doc for the flow, not when it merely references one | 2026-07-14 (r2, `e206533`) | ✅ CLOSED — r2 both fixtures ✅; Pass 3 Rule 2 explicitly scoped out on synthesis ("out of scope... no finding raised"), zero Must Fix on the clean control. See `peer-review/results/2026-07-14_claude-sonnet-5_r2.md` |
| 2026-07-14 | peer-review | 03-verdict-matches-rubric (❌ weekly-update-clean) — verdict NEEDS REVISION vs. expected CLEARED, driven by the same hallucinated finding above | Same fix (Pass 3 Rule 2 scope qualifier, `e206533`) | 2026-07-14 (r2) | ✅ CLOSED — r2 verdict CLEARED, matches answer key |
| 2026-07-14 | peer-review | 04-clean-artifact-not-flunked (❌ weekly-update-clean) — false-positive control failed outright, same root cause (P0-significance per suite README) | Same fix (Pass 3 Rule 2 scope qualifier, `e206533`) | 2026-07-14 (r2) | ✅ CLOSED — r2 CLEARED + 0 Must Fix; clean control fully restored (0/3 → 3/3) |
| 2026-07-14 | peer-review | 01-planted-blockers-caught (⚠ both flawed fixtures) — absence-type flaws (US-3 missing AC / F1; Theme 2 zero evidence / S1) missed | Not yet applied — recommend an explicit "check each item individually, do not infer from sibling content" instruction in `.claude/skills/peer-review/SKILL.md` Pass 1 | 2026-07-14 (r2, partial) | ⏳ OPEN (improved) — r2: synthesis S1 now caught (eval 01 ⚠→✅), but prd F1 (US-3 missing AC) still missed (⚠). Non-blocking; harness-hardening follow-up. |
| 2026-07-14 | peer-review | 05-fix-checklist-actionable (❌ synthesis r2) — a methodology/confidence Partial finding named in Pass 1 prose was dropped from the Step 6 fix checklist | Not yet applied — recommend a Step 6 "crosswalk every non-Pass scorecard row against the checklist before finalizing" instruction | — | ⏳ OPEN — pre-existing checklist-completeness gap, non-blocking, harness-hardening follow-up |

> **Status 2026-07-06 (post-remediation, r1+r2):** gate-group's first full logged run(s). r1 (2026-07-06): 6/8, FAILED bar — C5 and C7 both failed (Vale fence-wrapping + axis-bleed). One remediation round applied (schema output-format rule, Vale banned-vocabulary rule, Ducard output-format line) and Vale (5) + Ducard (2) re-run. r2 (2026-07-06): **7/8, PASSED bar** — C2/C4 mandatory both clean; C5 fully fixed; C7 partial (Vale clean, Ducard's prose-preamble defect persists in a new shape). All three original 2026-06-10 findings are closed. One new follow-up opened (Ducard C7) — logged above, not blocking. Full transcript and per-criterion grading: `gate-group/results/2026-07-06_post-remediation.md`.

---

## How to use

When a suite run scores below the pass threshold:
1. Identify which criteria failed
2. Determine which agent prompt or workflow is responsible
3. Edit the file (note the path in "Agent file edited")
4. Re-run the criterion (not the full suite unless needed)
5. Log the re-run result here

## Related

[[Evals/eval-schedule]] · [[Evals/index]] · [[Evals/eval-audit-checklist]]
