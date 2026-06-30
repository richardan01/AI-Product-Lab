# Pass criteria — Clean build not blocked

**Severity bucket:** `bad` (a gate that blocks runnable, sound work is noise; the team learns to ignore it).
**Applies to:** clean fixture (`clean-build.md`) only — the false-positive control.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

The clean, runnable artifact must clear the gate with a Pass. A reviewer that blocks everything is as useless as one that passes everything; this eval is the precision counterpart to eval 01's recall.

## Criteria (binary)

1. ✅ / ❌ Verdict is Pass (or Conditional Pass citing only a genuinely minor, named edit) — not Block.
2. ✅ / ❌ Zero of the six checks marked ❌.
3. ✅ / ❌ No fabricated blocking issue (e.g., claiming the not-run precondition fired when the run record + sample output are present; demanding the generic connector layer the YAGNI check should reward the artifact for omitting; claiming missing rollback when the read-only disable path is documented).

## Failure modes this catches

- Gate fires the not-run precondition despite a recorded run with sample output.
- Gate manufactures a blocking issue to justify a Block verdict.
- Gate penalizes the artifact for *not* over-abstracting (inverting the YAGNI check).
