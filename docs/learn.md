# Learn AI Product Lab

This path is designed for a reader who has never seen the repository.

## 10 minutes: understand the scorecard

1. Read the seven questions in the root README.
2. Open the [latest suite run](../evals/agent-harness/evidence/2026-09-19_sample-coding-retry.md)
   (synthetic trace, seven isolated graders).
3. Compare task success with the six trajectory axes.
4. Notice that a successful final answer can still contain recoverable `sad` friction or a
   blocking `bad` trajectory failure.

Outcome: you can explain why final-answer-only evaluation misses important agent failures.

## 30 minutes: run the safe sample

1. Clone the repository and start Claude Code.
2. Run `/evaluate-agent-session sample`.
3. Inspect the seven isolated grades and aggregate.
4. Compare the generated report with the committed
   [2026-09-19 run](../evals/agent-harness/evidence/2026-09-19_sample-coding-retry.md) and the
   earlier [2026-07-11 synthetic tutorial](../evals/agent-harness/evidence/2026-07-11_sample-coding-retry.md).

Outcome: you understand the input, criteria, evidence, severity, and aggregate decision.

## 60 minutes: inspect a controlled real run

Read the files in
[`controlled-real-run/`](../evals/agent-harness/evidence/controlled-real-run/):

1. the sanitized normalized trace;
2. the seven grader verdicts;
3. the aggregate report;
4. the sanitization and provenance note.

Start with the provenance note (item 4): this run is a worked example, **not citable
evidence**, because author/grader separation did not hold. Then read the
[run protocol](../evals/agent-harness/protocol.md). Focus on the separation between the
session being evaluated and the fresh grader contexts, and on exactly where this run falls
short of it.

Outcome: you can distinguish a designed fixture from a real, controlled harness run, and a
run that meets the separation rule from one that does not.

## Two hours: study the full learning loop

1. Read the [agent-harness methodology](../evals/agent-harness/agent-harness-suite.md).
2. Read the [RegEval discovery pass](../evals/regeval/discovery-pass-2026-06-28.md).
3. Inspect the [RegEval experiment log](../evals/regeval/experiments/log.md).
4. Read [architecture and method](architecture.md) to see how failures become fixtures and
   how append-only evidence prevents retrospective cleanup.
5. Run the deterministic RegEval demo from its [case-study guide](../evals/regeval/README.md).

Outcome: you can explain the complete loop from trace inspection to metric correction and
repeatable regression evidence.
