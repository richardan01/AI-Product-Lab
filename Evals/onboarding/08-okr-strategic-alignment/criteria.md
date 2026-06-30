# Eval 08 — OKR strategic alignment captured

**Type:** Generalization Failure — Phase 5 prompts explicitly require OKR follow-ups; eval measures whether they're consistently surfaced and captured.
**Grader:** eval-grader sub-agent (manual). Some sub-criteria (placeholder presence in GOALS.md) overlap with eval 04's programmatic grader — consolidate after first joint run.

**Failure mode:** Phase 5 OKR follow-up questions were skipped, or the `GOALS.md` "Strategic alignment" section still contains bracketed template placeholders after onboarding.

## Why this matters

A PM who onboards but doesn't connect their 30/60/90 goals to company strategy gets no signal from the OS when their work drifts from business priorities. The three OKR fields (`OKR ladder-up`, `Single proof metric`, `Goal 1 kill condition`) are the minimum strategic context required to make goals actionable, not just aspirational.

## Pass criteria

Grade each criterion ✅ / ❌ / ⚠ partial.

| # | Criterion | How to check |
|---|---|---|
| 1 | `GOALS.md` has a "Strategic alignment" section with all three fields present | `grep -n "Strategic alignment" GOALS.md` returns a result; all three fields (`OKR ladder-up`, `Single proof metric`, `Goal 1 kill condition`) are present below it |
| 2 | `OKR ladder-up` is not a bracketed placeholder | The field does not contain `[` unless the user explicitly wrote "Unknown / not yet set" — that literal text is a valid passing answer |
| 3 | `Single proof metric` names a specific metric and a target, OR is explicitly deferred | Must contain both a metric name and a target value or direction (e.g., "Activation rate → 40% at day 90"). A category alone ("growth metrics") fails. **Exception:** "Unknown / not yet set — deferred" is a valid passing answer for new PMs in onboarding roles where no team metric exists yet, provided a follow-up task is captured in `Tasks/follow-ups.md`. |
| 4 | `Goal 1 kill condition` names a specific trigger | Must name an event or condition (e.g., "If Priya kills the activation funnel project"), not a vague category ("stakeholder change") |

## Grading notes

- **"Unknown / not yet set"** is a valid pass for both criterion 2 (`OKR ladder-up`) and criterion 3 (`Single proof metric`) when the user is in a new role or onboarding scenario where no company metric has been established. The grader must verify: (a) the assistant asked the question (not skipped), (b) the user explicitly deferred, and (c) a dated follow-up task exists in `Tasks/follow-ups.md` to revisit the deferred field. If (c) is missing, grade criterion 3 as ⚠ partial.
- A ⚠ partial is appropriate when the field is filled but vague (e.g., `Single proof metric` names a metric without a target). Partials are not rounded up.
- Check that the assistant asked the questions — do not assume fill-on-behalf is valid. If the grader cannot trace the field content back to something the user said in the transcript, it fails criterion 2, 3, or 4 respectively.

## Introspection prompt for ❌

> "Why did the runner skip or fail this question? Was it: (a) Phase 5 ended before the follow-up batch was asked, (b) the assistant filled in a placeholder without asking, (c) the user skipped and the assistant silently accepted the template default?"

Capture the answer — it is the harness bug report.
