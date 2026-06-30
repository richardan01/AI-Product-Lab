# Pass criteria — Clean PRD not flunked

**Severity bucket:** `bad` (a gate that flunks handoff-ready work is noise; the team learns to ignore it).
**Applies to:** clean fixture (`clean-ai-feature-prd.md`) only — the false-positive control.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

The handoff-ready PRD must clear the gate. A reviewer that flunks everything is as useless as one that passes everything; this eval is the precision counterpart to eval 01's recall.

## Criteria (binary)

1. ✅ / ❌ Verdict is READY (or CONDITIONAL citing only the single owned + dated open question Q1) — not NOT READY.
2. ✅ / ❌ Zero gates marked Fail across all 12 applicable gates.
3. ✅ / ❌ No fabricated Must-Fix / blocking gap (e.g., claiming a missing rollback when the Launch plan specifies the feature-flag rollback; claiming missing acceptance criteria when all three user stories have them).

## Failure modes this catches

- Gate demands template sections that are already present under a different heading.
- Gate manufactures a blocking gap to justify a NOT READY verdict.
- Gate treats a tracked open question (owner + due date) as a blocker.
