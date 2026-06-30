# Eval failure log

Append-only. One row per failed criterion per run. Captures what was fixed and whether the fix held on re-run.

---

| Date | Suite | Criterion | Agent file edited | Re-run date | Re-run result |
|---|---|---|---|---|---|
| 2026-06-10 | gate-group | C1 isolation (⚠ F4 Vale named Riddler by role) | `vicki-vale.md` — "never name other gate agents" line NOT found on 2026-06-28 check | — | ⏳ PENDING — fix unverified; gate-group not re-run |
| 2026-06-10 | gate-group | C7 schema conformance (⚠ F5 Vale issue fields off-contract) | `vicki-vale.md` — still points to `gate-response.schema.md`, schema NOT embedded verbatim (2026-06-28 check) | — | ⏳ PENDING — fix not applied; re-run needed |
| 2026-06-10 | gate-group | Fixture integrity (F2 source missing) | `Evals/gate-group/fixtures.md` — F2 README inlined verbatim ✅ | 2026-06-28 (file verified) | ✅ fix applied; confirming gate-group re-run still pending |

> **Status 2026-06-28 (audit reconciliation):** gate-group has **never logged a full re-run** (`run-log.md` has no gate-group entry), so none of these rows can be closed. F2's fixture fix is verified in `fixtures.md`; the F4/F5 Vale fixes are **not** verified in `vicki-vale.md`. To close: apply F4/F5 to `vicki-vale.md`, then run the gate-group suite and log the result.

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
