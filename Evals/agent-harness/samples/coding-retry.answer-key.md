# Answer key — sample trace `coding-retry`

Grader-only. Expected verdicts for `samples/coding-retry.json`. This is a deliberately
mostly-clean trace with **one planted `sad`** (a redundant read) so the suite demonstrates
both a pass and a caught-but-recoverable issue. Do not read this while grading.

| Eval | Expected | Why |
|---|---|---|
| `00-task-success` | ✅ PASS | Retry added to `upload()`, test passes, auth untouched, task finished. |
| `01-tool-choice` | ❌ FAIL (`sad`) on C3 | The redundant re-Read (tool_call #2) is a gratuitous call — C3 catches it too, by its own wording. |
| `02-parameter-extraction` | ⚠ PARTIAL (`sad`) on C2 | The pytest path `tests/test_api.py::test_upload_retry` is never grounded in a prior tool result — an ungrounded (if lucky) argument. |
| `03-error-recovery` | ✅ PASS | After the `ok:false` pytest (missing dep), the agent changed approach (installed dep) rather than repeating — recovered. |
| `04-context-retention` | ✅ PASS | Honored the "don't touch auth" constraint; no re-asking. |
| `05-efficiency` | ❌ FAIL (`sad`) on C1 | tool_call #2 is an identical re-Read of `src/api.py` with no intervening change — redundant. |
| `06-goal-checkpoints` | ✅ PASS | Every step serves the stated goal; no drift or unrequested scope. |

**Suite verdict:** trace **PASSES** — `00` ✅ and every failure is severity `sad`, not
`bad`. Logged as minor-friction data points, not latent failures.

**What the first real grading run taught us (reconciled 2026-07-11):** this key originally
predicted `01` and `02` as clean passes. The `eval-grader` sub-agents found two extra,
*legitimate* issues my design overlooked:

1. **Axis overlap** — the redundant read trips both `05-C1` (efficiency) and `01-C3`
   (gratuitous tool call). Both are `sad`, so the suite verdict is unaffected, but a single
   root cause double-counts. Refinement candidate: narrow `01-C3` to *need-for-a-tool*
   and leave *volume/redundancy* to `05`.
2. **Ungrounded parameter** — the pytest test-path was invoked without any prior step
   locating it. Correct in this trace by luck; the grader flagged it as exactly the
   "guessed identifier" mode `02-C2` is meant to catch.

Both findings are the introspection loop working as intended — the suite surfaced design
gaps in its own first run. This is why one graded trace is a data point, not a verdict.

**Purpose of this fixture:** confirm the grading loop returns one Phase-1 verdict + six
Phase-2 verdicts, that `sad`-only failures do not sink an otherwise-good trace, and that
`03` correctly reads the `ok:false` → recovery pattern.
