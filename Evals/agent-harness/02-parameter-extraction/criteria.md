# Pass criteria — Parameter extraction (Phase 2, axis 2)

Right tool, right arguments? This axis is about the `params` on each `tool_calls[]` entry —
the single most common agent failure surface per Shankar & Husain.

## Criteria (binary)

1. ✅ / ❌ Each tool call's `params` are well-formed for that tool (required arguments
   present, correct types, no malformed JSON/paths/queries).
2. ✅ / ❌ Argument *values* are drawn from context, not invented — file paths that exist,
   identifiers that appeared earlier in the trace, quoted strings that match the source.
3. ✅ / ❌ When a call's `result` shows the arguments were wrong (not found, no match,
   syntax error), the *next* call corrected the specific argument at fault rather than
   re-issuing the same bad value.

## Severity

- Criterion 2 ❌ → **bad** (a hallucinated parameter is an ungrounded action).
- Criterion 1 ❌ → **sad** if corrected next step; **bad** if it caused a wrong end-state.
- Criterion 3 ❌ → overlaps `03-error-recovery`; grade it here only for the *argument* fault.

## Failure modes this catches

- `Read` on a path that never appears in any prior tool result — guessed the filename.
- A search pattern with unescaped regex metacharacters that silently matched nothing, taken as "no results."
- Reused a stale value (old line number, old id) after the file had changed earlier in the trace.

## Notes for the grader

Cross-reference each param against earlier `tool_calls[].result` and `turns[]`. A value is
"grounded" if you can point to where in the trace it came from. If you cannot, and it is not
obviously derivable, criterion 2 is ❌. Empty/zero-result tool outputs that the agent treated
as authoritative truth are the classic tell.
