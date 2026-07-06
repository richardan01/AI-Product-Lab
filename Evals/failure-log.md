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
