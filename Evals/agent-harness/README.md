# agent-harness — evaluate an agent's trajectory, not just its answer

This suite grades a **real agent session** (Claude Code, Codex, or Cowork) instead of a
finished document. It is how AI Product Lab evaluates agentic products, chatbots, and coding
harnesses — the thing the other suites can't do, because they grade outputs and this grades
*behavior*.

## The 15-minute path

```
# 1. Turn a real session into a normalized trace
python3 scripts/trace_adapter.py claude-code --latest --suite agent-harness

# 2. Read the schema so you know what got captured
#    Evals/_schema/trace-schema.md   (turns, tool_calls, retrievals, metrics)

# 3. Grade it (author/grader separation via the eval-grader sub-agent)
#    -> follow protocol.md, Mode A, steps 3-6
```

You get one **task-success** verdict (did it accomplish the goal?) plus six **step-level**
verdicts (tool choice, parameter extraction, error recovery, context retention, efficiency,
goal alignment).

## Why two phases

Grounded in Shankar & Husain, *Evals for AI Engineers* (2026) + their
[evals FAQ](https://hamel.dev/blog/posts/evals-faq/): an agent scored on final output alone
looks far better than it is, because the failure surface — bad tool arguments, dropped
state, goal drift — is invisible at the output layer. So Phase 1 grades the outcome as a
black box, and Phase 2 opens the box.

| Phase | Eval | Grades |
|---|---|---|
| 1 (black box) | `00-task-success` | Did the final result meet the goal? |
| 2 (diagnostics) | `01-tool-choice` | Right tool for each step? |
| | `02-parameter-extraction` | Right arguments, grounded not guessed? |
| | `03-error-recovery` | Adapted after a failed tool call? |
| | `04-context-retention` | Held earlier constraints/facts? |
| | `05-efficiency` | No thrashing / redundant steps? |
| | `06-goal-checkpoints` | Stayed aligned to the goal? |

## Files

| File | Purpose |
|---|---|
| `agent-harness-suite.md` | Methodology + grounding + scoring |
| `protocol.md` | Run procedure (Mode A: real session · Mode B: fresh workflow run) |
| `00-…/`–`06-…/criteria.md` | Binary pass criteria + `bad`/`sad` severity per eval |
| `failure-transitions.md` | Transition matrix — where first failures cluster across traces |
| `samples/` | Committed reference fixtures: a synthetic trace + answer key, and a Codex rollout for adapter regression checks |
| `_public-evidence/` | Sanitized end-to-end runs that ship publicly (raw `_traces/` do not) |
| `../_schema/trace-schema.md` | The normalized trace contract every adapter emits |
| `../../scripts/trace_adapter.py` | claude-code / codex → normalized trace |
| `../../scripts/make_n1_fixture.py` | Truncate a trace at its first error → N-1 fixture |
| `../../scripts/test_trace_adapter.py` | Regression coverage: `turn_index` semantics, N-1 truncation, plumbing/sidechain filtering, Codex retrieval heuristic — `python3 scripts/test_trace_adapter.py` |

## Pass bar

A trace passes when `00-task-success` is ✅ **and** no Phase-2 axis returns a `bad` finding
(`../severity-taxonomy.md`). A trace that succeeds end-to-end but carries a `bad` axis is a
**latent failure** — logged as a candidate N-1 fixture, not a clean pass. One trace is a
data point; grade several before quoting a rate. Any per-axis LLM judge must clear
`/judge-calibration` (TPR/TNR ≥ 0.9) before it is cited.

## Status

New suite (2026-07). Harness support: **claude-code** (verified against a real session),
**codex** (documented format + regression-tested against a synthetic rollout; **real
rollout validation still blocked** — no Codex CLI available in the environment this was
built in, see the `adapt_codex` docstring in `scripts/trace_adapter.py` for the repro
recipe for whoever validates it next), **cowork** (planned — format unconfirmed). First
dogfood evidence in `_public-evidence/`.
