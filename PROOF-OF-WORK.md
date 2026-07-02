# Proof of Work

AIPM-OS is an applied AI PM portfolio lab: a public operating system for product-management craft used to build artifacts, run evals, record failures, and show how the system performs under real project pressure.

## Flagship measurable project: RegEval

RegEval is the flagship measurable project in this lab. It tests whether an LLM-as-judge workflow can classify regulated-domain compliance examples with enough agreement against human labels to be useful.

The point is not only the result. The point is the measurement loop:

- define a falsifiable metric;
- run the judge against a fixed dataset;
- compare against human labels;
- log failures and remediations;
- rerun with documented changes;
- preserve the run history so learning is visible over time.

## Quality gates protect public artifacts

Public artifacts are gated before they are treated as portfolio evidence. The quality-gate system is designed to catch:

- unsupported claims;
- unclear positioning;
- missing evidence;
- brittle methodology;
- reader confusion;
- overclaiming from partial eval results.

In this repo, those gates are part of the proof: they show how public-facing work is reviewed before it is shipped.

## Evals and run logs show learning over time

The eval suites and run logs are the longitudinal evidence layer. They make the work inspectable by showing:

- what was measured;
- what failed;
- what changed;
- what improved;
- what remains uncertain.

This is the portfolio claim AIPM-OS is meant to support: AI PM learning should become public, measurable proof-of-work rather than private notes or vague positioning.
