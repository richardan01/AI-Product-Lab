# Eval 12 — Custom persona captured

**Type:** Generalization Failure post-2026-05-30-audit-fix. Pre-fix, the failure mode "Custom not surfaced as first-class option" was a Specification Failure (workflow didn't enumerate Custom equally). Audit added that criterion and the fix landed at workflow Phase 3. Now the eval measures whether the model captures custom inputs faithfully — pure generalization.
**Grader:** eval-grader sub-agent (manual).

**Failure mode:** Assistant forces the user into a predefined persona or leaves custom persona routing, quality gates, and command defaults ambiguous.

## Pass criteria

| # | Criterion |
|---|---|
| 1 | The assistant accepts a custom persona name and captures the user's own tone/behavior words without rewriting them into a canned persona. |
| 2 | The assistant asks which quality gates should apply to the custom persona, or proposes options and gets confirmation. |
| 3 | The assistant asks which commands should be surfaced first for the custom persona. |
| 4 | `CLAUDE.md` output records the custom persona's gates and surfaced commands clearly — which gates are mandatory, under what conditions, and which commands come first. |

## Grading notes

Grade against the captured transcript and final proposed file contents. A passing run must show that the assistant asked rather than inferred, and that any sensitive or custom behavior was confirmed before writing.
