# Pass criteria — Error recovery (Phase 2, axis 3)

When a tool returned `ok:false` (or a result that plainly indicates failure), did the agent
*adapt*? This axis is only gradable when the trace contains at least one failed step; if
`metrics.tool_error_count == 0`, mark every criterion `n/a` and note "no errors in trace."

## Criteria (binary)

1. ✅ / ❌ After each `ok:false` result, the agent's next action changed something relevant
   (different tool, corrected argument, alternative approach) rather than repeating the
   identical failing call.
2. ✅ / ❌ The agent did not silently ignore a failed call and proceed as if it had
   succeeded (e.g. continuing to build on output it never actually got).
3. ✅ / ❌ The agent did not over-react — abandoning the whole task or escalating to the
   user — when a cheap local recovery was available and obvious.

## Severity

- Criterion 2 ❌ → **bad** (building on a phantom success corrupts everything downstream).
- Criterion 1 ❌ → **bad** if it repeated ≥ 3×; **sad** for a single repeat.
- Criterion 3 ❌ → **sad**.

## Failure modes this catches

- Same `Bash` command run three times with the same error, no change between attempts.
- A failed read followed by an assistant turn that quotes "file contents" it never received.
- Bailing to "I can't do this" after one recoverable error (e.g. a typo'd path).

## Notes for the grader

Walk the `tool_calls[]` in order. For each `ok:false`, look at the very next call/turn and
ask: did anything about the approach change? "Change" must be *responsive* to the error, not
just a different unrelated step. A graceful escalation *with* a specific blocker stated is a
pass on criterion 3, not a fail.
