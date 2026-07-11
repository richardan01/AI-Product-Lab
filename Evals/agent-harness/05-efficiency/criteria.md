# Pass criteria — Efficiency (Phase 2, axis 5)

Did the agent reach the goal without thrashing? Efficiency is a *quality* signal, not just
cost — repeated identical steps usually mean the agent is confused, not thorough.

## Criteria (binary)

1. ✅ / ❌ No redundant tool calls: the trace does not contain the same call (same tool,
   same `params`) repeated with no intervening change that would alter its result.
2. ✅ / ❌ No obvious loop: the agent did not cycle through the same 2–3 steps more than
   twice without progress toward the goal.
3. ✅ / ❌ `metrics.tool_call_count` is proportionate to the task's difficulty — a
   one-line change did not take dozens of calls. (Judgment call; use the goal to calibrate.)

## Severity

- All three ❌ → **sad** by default (the task can still succeed inefficiently). Escalate a
  criterion to **bad** only if the thrashing is so severe it prevented completion (then it
  will also fail `00-task-success`).

## Failure modes this catches

- The same file read 4 times across the trace with no edits in between.
- Grep → read → grep → read cycling on the same target without narrowing.
- 30 tool calls to accomplish what the goal implies is a 2–3 step task.

## Notes for the grader

Use `metrics.tool_call_count` and the ordered `tool_calls[]` list. "Redundant" means the
second call could not plausibly return anything new. Legitimate re-reads (file changed
between reads, pagination, genuinely new query) are **not** redundant — check the params and
any intervening edit. Be generous: exploration is not thrashing. Only flag clear waste.
