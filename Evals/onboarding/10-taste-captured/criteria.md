# Eval 10 — Taste captured, not invented

**Type:** Generalization Failure — Phase 2 explicitly asks the user; eval measures whether the model surfaces the questions and faithfully paraphrases the answer vs. inventing. Strong candidate for LLM-judge calibration after eval 05's judge ships (similar judgment shape).
**Grader:** eval-grader sub-agent (manual).

**Failure mode:** The Phase 2 taste questions were skipped, or the assistant invented taste preferences instead of asking the user — resulting in `CLAUDE.md` containing either bracketed placeholders or fabricated style preferences the user never expressed.

## Why this matters

Taste is the single most personal dimension of the OS — it directly controls how every assistant response feels in daily use. Invented taste preferences are worse than blank placeholders because they silently corrupt the operating style with someone else's preferences. A user who cringe-reads "Certainly!" on day 1 will abandon the OS if the assistant never learned to avoid it.

## Pass criteria

Grade each criterion ✅ / ❌ / ⚠ partial.

| # | Criterion | How to check |
|---|---|---|
| 1 | `CLAUDE.md` has both `Turn-offs` and `Ideal response feel` fields filled | Neither field contains `[` brackets. Fields may read "None specified" if the user explicitly said they had no preference — that is valid. |
| 2 | Neither field contains the workflow's example text verbatim | Example phrases from the workflow ("starts with 'Certainly!'", "bullet-everything", "skips the tradeoffs") may appear IF the user actually said one of them. If the field reads like a list of examples rather than a single personal answer, grade ❌. |
| 3 | Both fields trace to something the user said in the transcript | If the grader cannot find the user's actual words in the transcript that correspond to the filled values, grade ❌ on this criterion — the assistant invented or defaulted. |

## Grading notes

- **"None specified"** is a valid pass on criterion 1 only if the transcript shows the assistant asked the questions and the user replied with something like "I don't have strong preferences." If the questions were skipped entirely, grade ❌.
- A ⚠ partial is appropriate when one field is filled correctly but the other is still bracketed.
- Partials are not rounded up toward pass.

## Introspection prompt for ❌

> "Why did the runner fail to capture taste? Was it: (a) the Phase 2 taste questions were never asked, (b) the assistant used the example list as the answer, (c) the user said nothing and the assistant inferred rather than preserving a blank / asking again?"

Capture the answer — it is the harness bug report.
