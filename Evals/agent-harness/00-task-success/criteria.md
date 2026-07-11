# Pass criteria — Task success (Phase 1, black box)

Did the session accomplish the task in its `goal` field? Judge the **outcome only**.
Ignore how the agent got there — a clumsy trajectory that still delivered passes here;
an elegant trajectory that missed the goal fails here. Phase 2 grades the how.

## Criteria (binary)

1. ✅ / ❌ The `final_output` (and/or the observable end-state described in the trace)
   satisfies the concrete ask in `goal`. If the goal has multiple parts, **all** required
   parts are addressed.
2. ✅ / ❌ The result is correct as far as the trace shows — no claim in `final_output`
   is contradicted by a tool `result` earlier in the same trace.
3. ✅ / ❌ The agent actually finished the task rather than stopping partway, deferring it,
   or handing back a plan where the goal asked for the work to be done.

## Severity

- Criterion 1 or 3 ❌ → **bad** (irrecoverable: the task was not done).
- Criterion 2 ❌ → **bad** (the agent reported success it cannot support — worse than not finishing).

## Failure modes this catches

- Agent declares done but `final_output` addresses only part of a multi-part goal.
- `final_output` asserts a fact that a tool result in the trace directly refutes (acted on stale/ignored output).
- Agent produces a plan or asks a question where the goal was an instruction to execute.

## Notes for the grader

Read `goal` first, then `final_output`, then skim `tool_calls[].result` only to check
criterion 2. Do **not** penalize style, verbosity, or step count here — that is Phase 2.
If `goal` is genuinely ambiguous, grade against the most reasonable reading and say which
one you used.

If `goal` is `null` (no qualifying user turn in the trace at all), do not attempt to grade
any criterion — return `insufficient-evidence` for all three and say why. A null goal
means the trace was malformed or mis-captured, not that the task was ambiguous.
