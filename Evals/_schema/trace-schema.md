# Normalized trace schema

The **contract** shared by every harness adapter (`scripts/trace_adapter.py`) and every
consumer (the `agent-harness` eval suite, `/error-analysis`, `make_n1_fixture.py`).

Why this exists: Shankar & Husain define a *trace* as the complete record of messages,
tool calls, and retrievals from first user query to final response. Each harness
(Claude Code, Codex, Cowork) persists that record in its own JSONL dialect. This schema
is the single normalized shape they are all mapped onto, so the eval layer never has to
know which harness produced a session.

## Format

One JSON object per file: `Evals/<suite>/_traces/files/<trace_id>.json`.

```jsonc
{
  "trace_id": "ah-0001",              // suite-prefixed, stable
  "source_harness": "claude-code",    // claude-code | codex | cowork
  "session_id": "7a2b29c9-…",         // harness-native session id
  "captured_from": "~/.claude/projects/…/<session>.jsonl",
  "adapter_version": "1",             // bump when mapping logic changes
  "goal": "…",                        // first user turn — the task under evaluation.
                                      // null if no qualifying user turn exists (e.g.
                                      // an all-tool-output session) — see Field rules.
  "turns": [                          // ordered, main-thread only (sidechains excluded)
    { "i": 0, "role": "user",      "text": "…", "ts": "2026-07-11T03:07:02.946Z" },
    { "i": 1, "role": "assistant", "text": "…", "ts": "…" }
  ],
  "tool_calls": [                     // ordered; each call matched to its result by id
    {
      "i": 0,
      "name": "Bash",
      "params": { "command": "…" },   // the tool input, verbatim
      "result": "…",                  // result content (stringified if structured)
      "ok": true,                     // false when the harness flagged is_error
      "ts": "…",
      "turn_index": 3                 // forward-pointing, NOT the turn that issued
                                      // it — see "turn_index semantics" below
    }
  ],
  "retrievals": [                     // subset of tool_calls the adapter classes as
                                      // retrieval (heuristic — see Field rules)
    { "tool_call_index": 0, "name": "Grep", "query": "…" }
  ],
  "final_output": "…",                // last assistant text block
  "metrics": {
    "turn_count": 12,
    "tool_call_count": 35,
    "tool_error_count": 1,
    "input_tokens": 1234,             // null if the harness does not record usage.
                                      // Claude Code: non-cached input only — cache
                                      // reads are excluded, so this understates
                                      // true context size on cached sessions.
    "output_tokens": 5678,
    "wall_seconds": 184.4             // last_ts − first_ts; null if timestamps absent
  },
  "skipped_lines": { "queue-operation": 8, "unknown": 0 }  // version-tolerance audit
}
```

## Field rules

- **`goal`** — the first `user` turn whose content is a plain string (not a tool_result).
  This is what Phase-1 (E2E task success) grades against. **Can be `null`** if no
  qualifying user turn exists in the whole trace (e.g. a fully tool-output/plumbing
  session). A grader seeing `goal: null` should return `insufficient-evidence`, not guess
  at a goal — this is a malformed/mis-captured trace, not a real Phase-1 input.
- **`tool_calls[].ok`** — `true` unless the harness marked the result an error. Feeds the
  `error-recovery` axis (did the agent recover after an `ok:false`?).
- **`tool_calls[].turn_index` semantics** — this is **forward-pointing**, not a
  back-reference to "the turn that issued the call." It is set to `len(turns)` at the
  instant the call is processed — i.e. the index the *next* appended turn will receive.
  Consequences: (1) multiple tool_calls appearing before any intervening text/message all
  share the same `turn_index`; (2) it can legitimately equal `len(turns)` — one past the
  last real turn index — when the call is the final item in a session with no further
  turn ever appended. Both are expected, not corruption; `make_n1_fixture.py`'s truncation
  relies on this (see its own comments) and needs no bounds-check for the dangling case.
- **`retrievals`** — a *heuristic* classification (Read/Grep/Glob/WebFetch/WebSearch, the
  codex-native equivalents, and — for Codex's shell-mediated tools — a conservative
  first-word allowlist over `params.command`, since Codex often buries search/read intent
  in a generic shell call rather than a dedicated tool name). Present so RAG-style
  retrieval quality can be graded separately, per the FAQ's retrieval/generation split.
  **Not authoritative**: the shell-command heuristic is a first-token allowlist, not a
  flag parser, so e.g. `find . -delete` still matches on `find` and is misclassified as
  retrieval. No current grading criterion (`01`–`06`) reads this field — it grades off
  `tool_calls[]` directly — so this heuristic's imprecision doesn't affect pass/fail today.
- **`skipped_lines`** — every input line the adapter did not map is counted here by its
  raw type. A non-zero `unknown` bucket is the signal that the harness changed its format
  and the adapter needs updating (both formats are internal + version-unstable per their
  own docs). The adapter **never** aborts on an unknown line; it counts and continues.

## Non-goals

- This is not a lossless mirror of the source JSONL. Sidechains (sub-agent transcripts),
  hook metadata, and mode/queue bookkeeping are intentionally dropped — the eval layer
  grades the main agent's trajectory, not the harness's internal plumbing.
- No PII scrubbing happens here. Sanitization for the public evidence tier is a separate,
  explicit step (see `Evals/agent-harness/_public-evidence/README.md`).
