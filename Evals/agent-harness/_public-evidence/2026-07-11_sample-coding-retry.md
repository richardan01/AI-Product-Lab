# Worked example — agent-harness run on `coding-retry` (2026-07-11)

The first end-to-end run of the `agent-harness` suite: one agent trajectory, seven graded
verdicts, one aggregate. Trace is synthetic (`samples/coding-retry.json`) so the full run
ships unredacted — it exists to show the method actually runs, not to expose a real session.

## Run inputs

| Field | Value |
|---|---|
| Suite | `agent-harness` |
| Trace | `samples/coding-retry.json` (`ah-sample-coding-retry`, harness `claude-code`) |
| Goal | "Add a 3-attempt retry with exponential backoff to `upload()` in `src/api.py`, and do not touch the auth module." |
| Graders | 7× `eval-grader` sub-agent, one per eval, read-only on (trace + one `criteria.md`) |
| Separation | Each grader read **only** its trace + criteria — never the answer key, suite docs, or sibling criteria |

## Per-eval verdicts

| Phase | Eval | Verdict | Severity | Grader evidence (abridged) |
|---|---|---|---|---|
| 1 | `00-task-success` | ✅ 3/3 | — | Edit adds 3-attempt backoff loop; final "test passes" backed by `tool_calls[5]` "1 passed"; auth never touched. |
| 2 | `01-tool-choice` | ❌ 2/3 (C3) | `sad` | Right tools throughout, but `tool_calls[2]` is a verbatim re-Read — a gratuitous call. |
| 2 | `02-parameter-extraction` | ⚠ 2/3 (C2 partial) | `sad` | Args well-formed; but the pytest path was invoked without any prior step locating it — ungrounded (if lucky). |
| 2 | `03-error-recovery` | ✅ 3/3 | — | After `ok:false` (missing `requests`), next call installs the dep and re-runs — recovered, no repeat. |
| 2 | `04-context-retention` | ✅ 3/3 | — | "Don't touch auth" honored; grounded facts (signature, test path) reused unchanged. |
| 2 | `05-efficiency` | ❌ 2/3 (C1) | `sad` | `tool_calls[1]` and `[2]` are identical Reads with no intervening change — redundant. |
| 2 | `06-goal-checkpoints` | ✅ 3/3 | — | Every step traces to the goal; dep-install is diligence, not scope creep; final output on-goal. |

## Aggregate

**Suite verdict: PASS.** `00-task-success` ✅ and **no `bad` finding** on any axis. The three
Phase-2 misses are all `sad` (recoverable): one redundant read (double-counted by `01-C3`
and `05-C1`) and one ungrounded-but-correct parameter. A trace that ships the task with only
`sad` friction passes; it is logged, not blocked.

## What this run proved (and found)

1. **The loop works end to end** — adapter-normalized trace → 7 parallel graders → one
   Phase-1 + six Phase-2 binary verdicts, with author/grader separation architecturally held.
2. **The graders out-found the author.** The answer key predicted `01` and `02` as clean.
   The graders caught (a) the redundant read *also* trips `01-C3`, and (b) the pytest path
   was never grounded — a subtle `02-C2` hit that wasn't deliberately planted. Both are
   real; both are `sad`. See `samples/coding-retry.answer-key.md` for the reconciliation.
3. **Scope discipline held.** The `00` grader spotted a latent code bug (a bare `raise`
   outside its `except`) but correctly kept it out of the black-box phase — Phase 1 grades
   the outcome, Phase 2 grades the how. That is the two-phase split doing its job.

## Follow-ups registered

- Narrow `01-C3` to "need for a tool at all" and leave redundancy/volume to `05` (remove the
  double-count).
- Add a fixture where a guessed identifier is *wrong* (not lucky) to harden `02-C2`.
- Capture a real (non-synthetic) Claude Code session, redact it, and add it here as the
  first real-world evidence entry.
