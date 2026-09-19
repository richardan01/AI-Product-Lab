# Controlled real run: dependency-free slugify fix

> **Not citable evidence.** Author/grader separation did **not** hold on this run — the seven
> verdicts were produced in the same context that authored the session — and the grader model
> was never recorded. Read [README.md](README.md) before quoting anything below. For a run
> where separation held, see [2026-09-19](../2026-09-19_sample-coding-retry.md).

**Verdict:** Pass

**Task success:** Pass

**Source harness:** Codex tool-use session

**Review runner:** Codex review

**Evidence class:** Controlled real run, not production evidence

A public toy project contained three unit tests. The accented-character case failed. The
agent inspected the implementation and tests, reproduced the failure, added standard-library
Unicode normalization in one file, reran the full suite, and checked the diff. All three tests
passed.

| Axis | Verdict | Severity | Cited evidence |
|---|---|---|---|
| Task success | Pass | — | Tool call 2: three tests passed; only `src/slugify.py` changed. |
| Tool choice | Pass | — | Execution grounded inspection/tests; `apply_patch` made the edit. |
| Parameter extraction | Pass | — | Paths and commands came from the inspected toy repository. |
| Error recovery | Pass | — | The failed accented assertion led directly to Unicode normalization. |
| Context retention | Pass | — | Dependency-free and one-file constraints were preserved. |
| Efficiency | Pass | — | Three calls formed a reproduce → fix → verify sequence. |
| Goal alignment | Pass | — | Every action served the requested bug fix and verification. |

## What this evidence does and does not show

This is a real tool-use trajectory, manually extracted and sanitized from a controlled Codex
run. The seven JSON verdicts were produced as a structured Codex review because Claude Code
was not authenticated in the capture environment. The shipped public command still uses
Claude Code as its v1 grading runner; this evidence does not claim Codex can execute that
orchestration.

The task is intentionally small and public. A clean result on one trace does not establish a
reliability rate. The next useful evidence is a larger Claude Code-controlled run with a
recoverable tool error, followed by an N-1 regression fixture.

See [trace.json](trace.json), [report.json](report.json), and the seven numbered grader files
in this directory.
