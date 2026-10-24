# Provenance and sanitization

This evidence came from a real Codex tool-use run on a temporary, public toy project created
for this repository review. The task used only Python's standard library.

Sanitization replaced the temporary absolute path and session identifier, removed environment
metadata and timestamps, and summarized tool result bodies while retaining the failure,
parameters, ordering, and verification outcome needed by the scorecard. No work code, personal
name, credential, provider secret, or private dataset is included.

The capture environment's Claude Code CLI was installed but not authenticated. To avoid a
false provenance claim, the trace and aggregate identify Codex as the source and review runner.
This is controlled real evidence, not production evidence and not proof of population-level
reliability.

## Provenance (reconstructed 2026-09-19)

| Field | Value |
|---|---|
| Run date | `2026-07-21` — **not the capture date.** Sanitization stripped every timestamp from this run, so no date survives in any file here. The value shown is the commit date of `da41917`, which first published these files. |
| Repo commit | `da41917` |
| Grader runner | `codex-review` |
| Grader model | **Not recorded.** The model that produced the seven verdicts was not captured and cannot be recovered. It is recorded as `null` rather than guessed. |
| Author/grader separation | **Did not hold.** |
| Evidence class | Controlled real run — worked example, not citable evidence |

### Why separation did not hold

`protocol.md` requires seven isolated `eval-grader` contexts and states: "Never grade in the
context that authored the session." This run did not meet that bar. Claude Code was
unauthenticated in the capture environment, so the seven verdicts were produced as a single
structured Codex review in the same context that authored the session.

That substitution was disclosed from the start, but its consequence was not recorded in
machine-readable form until now. **This run must not be cited as evidence of agent
reliability, or as a demonstration of the shipped seven-isolated-grader method.** It shows
the scorecard applied to a real tool-use trajectory, and nothing more.

For a run where separation did hold, see
[`../2026-09-19_sample-coding-retry.md`](../2026-09-19_sample-coding-retry.md) — synthetic
trace, but graded by seven genuinely isolated contexts with the model and commit recorded.
