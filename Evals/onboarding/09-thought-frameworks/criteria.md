# Eval 09 — Thought frameworks captured

**Type:** Generalization Failure — Phase 5B is mandatory in the workflow; eval catches the model skipping it when running long sessions or under deferral-heavy fixtures.
**Grader:** eval-grader sub-agent (manual). Placeholder-detection sub-criterion overlaps with eval 04's programmatic grader.

**Failure mode:** Phase 5B was skipped, or all four `Thought frameworks` fields in `CLAUDE.md` are still bracketed defaults after onboarding.

## Why this matters

Thought frameworks are how the OS calibrates its responses to the user's actual decision style — not a generic "analytical PM." Without these, every session defaults to the OS's generic output defaults. With them, the assistant can frame evidence the way the user actually weighs it, flag tradeoffs in the order the user actually prioritizes them, and distinguish acceptable experimentation from avoidable failures.

## Pass criteria

Grade each criterion ✅ / ❌ / ⚠ partial.

| # | Criterion | How to check |
|---|---|---|
| 1 | `CLAUDE.md` has a `Thought frameworks` section with all four fields | `grep -n "Thought frameworks" CLAUDE.md` returns a result; all four fields (`Tradeoff priority`, `Evidence standard`, `Decision certainty bar`, `Acceptable failure`) are present below it |
| 2 | At least 3 of 4 fields are filled with user-specific content | Fields containing `[` brackets (other than as part of an example list) count as unfilled. "Not specified" (meaning the user explicitly skipped) is a valid filled state. |
| 3 | No field is copied verbatim from the workflow's example list | The examples in the workflow are "e.g." prompts — user words must differ. If `Tradeoff priority` literally reads "e.g., quality > speed > learning" unchanged, that's a fail. |
| 4 | `Acceptable failure` distinguishes two categories | Must name what IS acceptable (a learning) vs. what IS NOT (avoidable). A single-sided answer ("failed experiments are OK") only partially passes — grade ⚠. |

## Grading notes

- The user may explicitly skip one question. Record `Not specified` in that field — that is a valid pass for criterion 2.
- If the grader cannot trace a field's content back to something the user said in the transcript, grade ❌ on criterion 3 (likely invented or defaulted).
- Partials (⚠) are not rounded up toward pass.

## Introspection prompt for ❌

> "Why did the runner skip or fail Phase 5B? Was it: (a) the phase was omitted entirely from the session, (b) the assistant filled in example text without asking, (c) the user skipped all four and the assistant silently accepted the bracketed defaults?"

Capture the answer — it is the harness bug report.
