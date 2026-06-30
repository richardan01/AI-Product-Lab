# Judge prompt — eval 04 (no residual placeholders)

A worked-example LLM-as-judge prompt for the first criterion to automate. Chosen because the criteria are near-deterministic (regex-checkable) — a good calibration baseline before tackling judgment-heavy evals (05, 07).

## How to use

1. Run the runner agent through onboarding against a fixture; capture the three output files (`CLAUDE.md`, `GOALS.md`, `Tasks/active.md`) verbatim.
2. Send the prompt below to a **separate** model context with those files as input. Use a low-temperature model (Sonnet 4.6 or Opus 4.7 at temp ≤ 0.2).
3. Compare the judge's verdict to the human grader's verdict from the same transcript. After ~30 paired grades you can compute TPR / TNR per criterion and decide whether the judge is calibrated enough to replace human grading on this eval (Hamel's bar: TPR ≥ 0.9 and TNR ≥ 0.9, or you keep grading by hand).

## Prompt

```
You are an eval grader. You are evaluating whether an interactive-onboarding
workflow left any unfilled template placeholders in the user's config files.

You will receive three files (CLAUDE.md, GOALS.md, Tasks/active.md) produced
by the workflow. Grade each of the five criteria below as PASS / FAIL /
PARTIAL. Partials are NOT rounded up. Output strict JSON only.

Criteria

C1 — CLAUDE.md placeholders absent
  PASS if CLAUDE.md contains zero unannotated occurrences of any of:
    [YOUR_NAME], [YOUR_ROLE], [YOUR_COMPANY], [YOUR_TEAM_OR_DOMAIN],
    [YOUR_MANAGER], [HEAD_OF_DEPT], [PRIMARY_PURPOSE],
    [YOUR_ANCHOR_PROJECT], [STAKEHOLDER_*], [METRIC_*].
  Annotated exception: a placeholder is OK if an adjacent line contains
  "# user said:", "# TODO: ask user", or "Unknown / TBD".
  FAIL if any unannotated placeholder remains.
  PARTIAL if 1 placeholder remains AND a follow-up task exists in
  Tasks/follow-ups.md referencing it.

C2 — GOALS.md placeholders absent
  PASS if GOALS.md contains zero occurrences of [YOUR_*], [AREA_*],
  [METRIC_*], [STAKEHOLDER_*], [DEV_GOAL_*].
  FAIL otherwise. Same annotated-exception rule as C1.

C3 — No legacy marketing placeholders
  FAIL if GOALS.md contains ANY of: [LIFECYCLE_PM], [PAID_ADS_PM],
  [WEBSITE_PM], [CONTENT_PM], [CURRENT_QUARTER].
  PASS if none present.
  (No partial — these are template debris and should never survive.)

C4 — Tasks/active.md populated rows are clean
  PASS if every checkbox row under "In Progress" or "To Do" contains a
  real task description (no [Task description], [Sprint N], [Start Date],
  or [area-tag] brackets in populated rows).
  Empty section headers with no rows are PASS.
  FAIL if any populated row contains a bracket placeholder.

C5 — Deferred fields annotated, not silent
  PASS if every remaining bracketed placeholder across all three files has
  an adjacent annotation ("# user said:", "# TODO: ask user", "Unknown /
  TBD") AND a corresponding row in Tasks/follow-ups.md.
  PASS by default if no placeholders remain at all.
  FAIL if any bracketed placeholder is unannotated.

Few-shot anchors

PASS example for C1:
  **[HEAD_OF_DEPT]** — [HEAD_OF_DEPT] # user said: not yet known
  (Annotated deferral. C1 PASS, contributes to C5 PASS if follow-up exists.)

FAIL example for C1:
  - **Manager or primary sponsor:** [YOUR_MANAGER] -> [HEAD_OF_DEPT]
  (User gave Priya Shah in Phase 0; assistant did not write it. C1 FAIL.)

FAIL example for C3:
  | [LIFECYCLE_PM] | Lifecycle and retention |
  (Marketing template debris. C3 FAIL regardless of context.)

FAIL example for C5:
  - **[HEAD_OF_DEPT]** — [HEAD_OF_DEPT]
  (No annotation, no follow-up row. Silent deferral. C5 FAIL.)

Output format (strict JSON, no prose, no markdown fences):

{
  "C1": {"verdict": "PASS|FAIL|PARTIAL", "evidence": "<verbatim line(s) or 'none found'>", "rationale": "<one sentence>"},
  "C2": {...},
  "C3": {...},
  "C4": {...},
  "C5": {...},
  "overall_pass_count": <0-5>
}

Files to grade:

<<<CLAUDE.md
{{CLAUDE_MD}}
>>>

<<<GOALS.md
{{GOALS_MD}}
>>>

<<<Tasks/active.md
{{TASKS_ACTIVE_MD}}
>>>
```

## Validation plan

| Step | What | Bar |
|---|---|---|
| 1 | Run judge over the existing `sample-pass.md` and `sample-fail.md` content | Must score sample-pass 5/5 and sample-fail 0–1/5 |
| 2 | Run judge in parallel with human grader on next 3 fixture runs (9 file triples total) | Record per-criterion agreement |
| 3 | After ≥ 30 paired grades, compute TPR / TNR per criterion | TPR ≥ 0.9 AND TNR ≥ 0.9 → judge replaces human on eval 04 |
| 4 | If a criterion misses the bar, inspect disagreements, refine rubric or anchors, re-validate | Do not ship an uncalibrated judge |

## Known limitations

- Criteria C1–C4 are regex-detectable. A judge is overkill *if* you can also write the regex check; the judge wins when you want one prompt template you can clone for criteria where regex doesn't work (07, 09, 10).
- C5 requires cross-file reasoning (follow-ups.md must reference the deferred field). Judge will be weaker here than on C1–C4; expect this to be the first criterion that fails calibration.
- Do not extend this prompt to evals 02 or 07 without redesigning — those grade transcript order, not file content.
