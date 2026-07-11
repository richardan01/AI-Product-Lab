# Agent-harness eval suite

The suite that grades an **agent trajectory** — a real Claude Code, Codex, or Cowork
session — instead of a finished document. This is the capability that lets a PM point
AI Product Lab at their own agentic product, chatbot, or coding harness and get a
grounded read on whether the *agent* (not just its final answer) is doing the right thing.

## Grounding

Implements the two-phase agentic evaluation from **Shankar & Husain, _Evals for AI
Engineers_** (O'Reilly, 2026) and their [evals FAQ](https://hamel.dev/blog/posts/evals-faq/),
"How to evaluate agentic workflows":

> Two-phase approach: (1) end-to-end task success as a black box, (2) step-level
> diagnostics of tool choice, parameter extraction, error recovery, context retention,
> efficiency, goal checkpoints. Use transition failure matrices … to identify hotspots.

The book's own framing of *why* step-level matters: agents scored on final output alone
pass materially more cases than trajectory-level evaluation reveals — the failure surface
lives in tool arguments, state propagation, and goal drift, none of which a final-answer
grade can see.

## What it grades

Input: one normalized trace JSON (`Evals/_schema/trace-schema.md`), produced by
`scripts/trace_adapter.py` from a real session. The suite has **two phases**:

### Phase 1 — end-to-end task success (black box)

| Eval | Question |
|---|---|
| `00-task-success` | Did the final output accomplish the trace's stated `goal`? Judge the outcome only — ignore how it got there. |

This is the outcome metric. An agent can nail every step and still fail the task, or
muddle through and succeed. Phase 1 is graded independently of Phase 2 for exactly this
reason (the FAQ's black-box/white-box split).

### Phase 2 — step-level diagnostics (six axes)

| Eval | Axis | What a failure looks like |
|---|---|---|
| `01-tool-choice` | Tool choice | Reached for the wrong tool, skipped a tool it needed, or ran a tool where reasoning alone was correct. |
| `02-parameter-extraction` | Parameter extraction | Correct tool, wrong arguments — bad path, malformed query, a value hallucinated rather than read from context. |
| `03-error-recovery` | Error recovery | After a tool returned `ok:false`, the agent repeated the same call, ignored the error, or gave up instead of adapting. |
| `04-context-retention` | Context retention | Forgot or contradicted a constraint/fact established earlier in the session; re-asked for something already provided. |
| `05-efficiency` | Efficiency | Reached the goal via redundant or looping steps — repeated identical reads, re-derived known facts, thrashed. |
| `06-goal-checkpoints` | Goal alignment | Drifted from the stated goal; optimized a sub-task the user did not ask for; never re-checked against the goal. |

Every criterion is **binary** (✅/❌, ⚠ partial tracked separately, never rounded up) per
the lab's metric standard, and carries a `bad`/`sad` severity tag
(`Evals/severity-taxonomy.md`). A single `bad` on any axis flags the trace.

## Why this suite is different from the others

The other suites grade a document against a rubric in a fresh grader context. This suite
grades a *trajectory*. Three consequences:

1. **The runner is the adapter, not `eval-runner`.** Capture already happened in the real
   session; `trace_adapter.py` normalizes it. `eval-runner` is only used when you want to
   grade a *fresh* run of a repo workflow (see `protocol.md`, mode B).
2. **The grader reads the trace JSON as its "transcript."** `eval-grader` is reused
   unchanged — author/grader separation still holds, because the grader never sees the
   adapter code or this methodology doc, only the trace + `criteria.md`.
3. **N-1 fixtures come from real failures.** `scripts/make_n1_fixture.py` truncates a
   trace at its first upstream error so a fix can be tested against the exact prefix that
   produced the failure (FAQ's N-1 protocol).

## Scoring

- **Phase 1** (`00-task-success`): the raw pass/fail is the headline. This is the number a
  stakeholder cares about.
- **Phase 2**: report per-axis ✅/❌ across the graded traces. The suite "passes" a trace
  when `00` is ✅ **and** no axis returns a `bad`. A trace that succeeds end-to-end but
  carries a `bad` on, say, `03-error-recovery` is a **latent failure** — it worked this
  time but the trajectory is not trustworthy. Log it; it is a candidate N-1 fixture.
- Over ≥ 5 graded traces, populate `failure-transitions.md` to find which agent state the
  first failures cluster in.

## Not in scope (deferred)

- Automated cross-harness replay (re-running turn N against a live external agent) — the
  adapter + `make_n1_fixture.py` produce the N-1 prefix; re-running is target-dependent
  and wired only for repo workflows via `eval-runner`.
- An LLM-judge for any axis is **opt-in and must be calibrated** (`/judge-calibration`,
  TPR/TNR ≥ 0.9) before it is cited — same bar as every other judge in the lab.
