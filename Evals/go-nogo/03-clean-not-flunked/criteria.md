# Pass criteria — Clean packet not flunked

**Severity bucket:** `bad` (a gate that no-gos launch-ready work is noise; the team learns to ignore it).
**Applies to:** clean fixture (`clean-launch-packet.md`) only — the false-positive control.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

The launch-ready packet must clear the gate. A gate that no-gos everything is as useless as one that gos everything; this eval is the precision counterpart to eval 01's recall.

## Criteria (binary)

1. ✅ / ❌ Verdict is GO — not NO-GO, and not a manufactured CONDITIONAL GO.
2. ✅ / ❌ Zero gates scored 🔴 and zero gates scored 🟡 across all 6 gates.
3. ✅ / ❌ No fabricated blocker (e.g., claiming an untested rollback when the packet records a rehearsed rollback drill; claiming missing sign-off when QA and UAT are both signed off).

## Failure modes this catches

- Gate demands a sign-off that is already recorded under a different heading.
- Gate manufactures a 🔴 or 🟡 to justify a NO-GO or CONDITIONAL GO verdict.
- Gate treats a closed, signed-off item as an open condition.
