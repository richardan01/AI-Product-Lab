# Pass criteria — Tool choice (Phase 2, axis 1)

For each step, did the agent reach for the *right* tool — including the choice not to use
a tool when reasoning alone was correct?

## Criteria (binary)

1. ✅ / ❌ Every `tool_calls[]` entry was an appropriate tool for what the agent was trying
   to do at that point (e.g. a content search used a search tool, not a raw shell `grep`
   where the house rules forbid it; a file edit used the edit tool, not a shell `sed`).
2. ✅ / ❌ No step that clearly required a tool was done "from memory" instead — the agent
   did not assert a file's contents, a search result, or an external fact without the tool
   call that would have grounded it.
3. ✅ / ❌ No gratuitous tool calls where none was needed (e.g. re-reading a file whose
   contents were already returned verbatim one step earlier — count that under `05` if it
   is about volume; here it is about *needing* the tool at all).

## Severity

- Criterion 2 ❌ → **bad** (ungrounded action/claim — the root of most agent hallucination).
- Criterion 1 or 3 ❌ → **sad** (recoverable inefficiency or a style/policy miss).

## Failure modes this catches

- Used `Bash: grep` where the environment's conventions require the dedicated search tool.
- Claimed "the config sets X" without ever reading the config.
- Chose a broad, expensive tool when a precise one was available and obvious.

## Notes for the grader

Judge each call against the sub-goal *visible at that turn*, not with hindsight. Wrong-tool
that the agent immediately corrected is at most ⚠ partial, not ❌ — note the correction.
If the harness has a documented tool policy in the trace's context, hold the agent to it.
