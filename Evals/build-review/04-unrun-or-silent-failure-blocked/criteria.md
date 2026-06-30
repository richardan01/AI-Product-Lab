# Pass criteria — Unrun or silent-failure build blocked

**Severity bucket:** `bad` (waving through a never-run artifact or a silent-failure factory wires a broken build into the flagship).
**Applies to:** flawed fixture (`flawed-build.md`) only — the recall control for the precondition and the worst anti-pattern.
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

The skill's hard precondition — the author must have run the artifact at least once ("I haven't run it" is an automatic FAIL) — and its top anti-pattern — a catch-all `try/except` with `pass` (silent failure factory) — are both non-negotiable Blocks. This eval verifies the gate enforces **either** one as a Block, given both are planted in the fixture.

## Criteria (binary)

1. ✅ / ❌ The gate surfaces the **not-run precondition**: it identifies the "I haven't run it" statement and treats it as an automatic Block (not a soft ⚠ buried in the scorecard).
2. ✅ / ❌ The gate flags the **catch-all `try/except: pass`** as a silent-failure issue (failure-modes / boundaries check ❌), naming it as the spec-violating silent drop.
3. ✅ / ❌ The final verdict is **Block** — driven by either or both of the above; a verdict that names the issues but lands Pass / Conditional Pass fails this eval.

(All three sub-checks must hold for this eval to pass.)

## Failure modes this catches

- Gate scores code quality but never checks whether the artifact was actually run (precondition blind).
- Gate treats a catch-all `try/except: pass` as acceptable error handling.
- Gate notes the issues in prose but rubber-stamps a passing verdict anyway.
