# Worked example — agent-harness run on `coding-retry` (2026-09-19)

A re-run of the suite on the same synthetic trace as the 2026-07-11 example, executed through
the shipped `/evaluate-agent-session sample` path with author/grader separation intact. Its
purpose is threefold: refresh the suite's last-run date, demonstrate the seven-isolated-grader
method actually running end to end, and test whether the 2026-07-11 verdicts reproduce.

Machine-readable report: [`2026-09-19_sample-coding-retry.report.json`](2026-09-19_sample-coding-retry.report.json).

## Provenance

| Field | Value |
|---|---|
| Run date | 2026-09-19 |
| Repo commit graded | `41518c2` |
| Suite | `agent-harness` (7 axes) |
| Trace | `samples/coding-retry.json` (`ah-sample-coding-retry`, harness `claude-code`, synthetic) |
| Preflight | `scripts/preflight_agent_eval.py sample` → `status: ready`, 5 turns, 6 tool calls |
| Grader runner | `claude-code` |
| Grader model | `sonnet` — the alias in `.claude/agents/eval-grader.md`; the runtime resolved it at run time and the resolved build string was not observed, so only the alias is recorded |
| Author/grader separation | **Held.** 7 parallel `eval-grader` subagents, each given exactly two paths (trace + one `criteria.md`). No grader read a sibling criterion, the answer key, the suite docs, or another grader's result. No axis was graded in the parent context. |
| Evidence class | Synthetic worked example — **not** a reliability claim |

## Per-eval verdicts

| Phase | Eval | Verdict | Severity | Grader evidence (abridged) |
|---|---|---|---|---|
| 1 | `00-task-success` | ✅ pass | — | Edit adds the 3-attempt backoff loop; "test passes" backed by `tool_calls[5]` "1 passed in 0.42s"; auth never touched. |
| 2 | `01-tool-choice` | ❌ fail (C3) | `sad` | `tool_calls[1]` and `[2]` are a verbatim re-Read — the criteria file's own example of a gratuitous call. |
| 2 | `02-parameter-extraction` | ✅ pass | — | Params well-formed and grounded; the ungrounded pytest path accepted under the "obviously derivable" exception. **Diverges from the answer key — see below.** |
| 2 | `03-error-recovery` | ✅ pass | — | After `ok:false` (missing `requests`), the next call installed the dep and re-ran; cause named before success claimed. |
| 2 | `04-context-retention` | ✅ pass | — | "Don't touch auth" honored; grounded facts carried forward unchanged. |
| 2 | `05-efficiency` | ❌ fail (C1) | `sad` | Identical back-to-back Read with no intervening change. |
| 2 | `06-goal-checkpoints` | ✅ pass | — | Every step serves the goal; dep-install is diligence, not scope creep. |

## Aggregate

**Suite verdict: PASS.** `00-task-success` ✅ and **zero `bad` findings**. Two `sad` findings
(`01-C3`, `05-C1`), both tracing to the single planted redundant read.

## Reproducibility against 2026-07-11

Six of seven axes reproduced exactly, 70 days apart. One did not:

- **`02-parameter-extraction` flipped from ⚠ partial (`sad`) to ✅ pass.** Both runs saw the
  same fact — the pytest path `tests/test_api.py::test_upload_retry` is never grounded in a
  prior tool result. The 2026-07-11 grader scored it a `02-C2` "guessed identifier"; this
  grader accepted it under the exception in the criteria's own grader notes for arguments that
  are obviously derivable from the goal.

This is a criterion-design problem, not a grader failure: `02-C2` contains an escape hatch
broad enough for two isolated graders to read the same evidence in opposite directions. The
suite verdict is unaffected (the finding was `sad` either way), but the divergence is the
useful result of this run and is logged rather than smoothed over. The fix is a fixture where
a guessed identifier is *wrong* rather than lucky, which forces the exception to be narrowed.

## Two contract defects this run exposed

Both were found while aggregating, and both are fixed in the same change that adds this file:

1. **`eval_id` copied from the template.** Four of seven graders returned
   `"eval_id": "00-task-success"` regardless of the criterion they were given, because the
   output example in `.claude/agents/eval-grader.md` hardcoded that value. Verdicts were
   correct; their labels were not. Unnoticed, this silently misfiles axes during aggregation —
   and `validate_agent_report.py` would have rejected the report on the `EXPECTED_IDS` check
   without explaining why. The contract now requires the id to come from the grader's own
   `criteria_path`.
2. **`finding_severity` returned as the string `"null"`.** Three of seven emitted `"null"`
   instead of JSON `null`, because the template rendered the union as `"bad|sad|null"` inside
   quotes. `ALLOWED_SEVERITIES` accepts `None`, not `"null"`, so this would fail validation.
   The contract now shows the literal typing.

Neither defect changed a verdict in this run. Both would corrupt an unattended one, which is
precisely why the suite is run rather than assumed to work.

## Follow-ups registered

- Add the wrong-guess fixture that settles `02-C2`'s "obviously derivable" exception.
- Narrow `01-C3` to "need for a tool at all", leaving redundancy to `05` (carried over from
  2026-07-11; the double-count reproduced here unchanged).
- Still pending: a real redacted **Claude Code** session graded this same way. Both published
  runs to date are synthetic or controlled-toy; neither is production evidence.
