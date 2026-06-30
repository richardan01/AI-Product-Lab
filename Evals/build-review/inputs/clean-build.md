# Build-review packet — Slack daily-digest MCP tool

**Author:** PM · **Artifact:** `mcp/slack_digest.py` · **Spec:** `Projects/digest/spec.md` · **Status:** for build review

## Spec (under test)
- Expose one MCP tool `slack_digest(channel_id, since_iso)` that returns the top 5 messages in a channel since a timestamp, ranked by reaction count.
- Read-only — never posts, edits, or deletes. Returns JSON `{messages: [...], generated_at}`.
- Bad channel id or unparseable timestamp → raise a typed error the caller can read; never return an empty success.

## What was built
- `slack_digest.py` implements the single tool exactly as specced — top 5 by reaction count, read-only client (no write scopes requested in the manifest).
- **Inputs validated at the boundary:** `channel_id` checked against `^C[A-Z0-9]{8,}$`; `since_iso` parsed with `datetime.fromisoformat` — both raise `DigestInputError` (a typed, documented exception) before any API call.
- **Failure modes named** in the module docstring: (1) Slack rate-limit → retry with backoff, then raise `DigestRateLimitError`; (2) channel not found → `DigestInputError`; (3) empty channel → returns `{messages: [], ...}` (a valid, documented result, not an error).
- **Observability:** every call logs `channel_id`, message count, and elapsed ms to the existing structured logger; errors logged at WARN with the typed error name.
- **Reversibility:** read-only tool, no state written, so disabling = removing the one tool entry from the MCP manifest. Documented in the module header.
- **No premature abstraction:** one tool, one concrete client; no generic "connector" layer.

## Run record
- Ran against the dogfood workspace on 2026-06-20: `slack_digest("C01ABCDEFGH", "2026-06-19T00:00:00")` returned 5 ranked messages; sample output pasted in `Projects/digest/run-2026-06-20.md`.
- Also ran the two error cases: bad channel id and `"not-a-date"` — both raised the typed errors as specced. Transcript in the same run file.
