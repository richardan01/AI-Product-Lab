# Answer key — flawed-build.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

**Artifact type:** Python module for an eval scaffold (spec present → all six checks apply)
**Precondition:** VIOLATED — the author states "I haven't run it against a real CSV yet." This is the automatic-FAIL precondition. The verdict is **Block** before the six checks are even scored; the checks below document the rest.
**Expected verdict:** Block ❌ (precondition violated, plus multiple failed checks)

## Planted flaws

| ID | Check | Location | Flaw |
|---|---|---|---|
| B1 | Precondition (not run) | Run record | Author states **"I haven't run it against a real CSV yet."** Per the skill, "I haven't run it" is an **automatic FAIL / Block** — independent of code quality. Imports-clean is not a run. |
| B2 | Boundaries clean / Failure modes named | Row-handling loop | **Catch-all `try/except: pass`** swallows every error and silently skips the row. This is the worst anti-pattern — a silent-failure factory — and directly violates the spec ("never silently drop a row; fail loudly with the offending row number"). Fails. |
| B3 | Reversibility | Output write | Opens `out.json` in `"w"` mode and dumps at end — **no atomic-replace, no rollback.** A crash mid-write or a re-run corrupts/clobbers prior output; the spec requires safe re-run. No documented rollback path. Fails. |
| B4 | Reusability vs YAGNI | `Pipeline` class | **Premature abstraction:** a generic `Pipeline` with `register_stage()`/`run_stages()` whose **single caller** registers exactly one stage. Abstraction with one caller is a named anti-pattern. Fails. |

(Observability is also weak — no row-read vs. emitted counter, no log line — reinforcing B2, but B1–B4 are the scored planted issues.)

## Grading notes
- **Eval 01 (verdict-correct):** correct verdict is Block. B1 alone (never run) forces Block per the precondition; B2 (silent failure + spec violation) independently forces Block. Pass or Conditional Pass here is a ❌.
- **Eval 02 (no-hallucinated-issues):** match on substance. Deliberately solid (do NOT flag as ❌): the module *does* read the specced columns and emit one record per row (spec conformance is partial-correct on the happy path — the failure is the silent-drop, not the mapping). Inventing issues beyond B1–B4 (e.g., claiming the CSV parser itself is wrong) is a hallucinated issue.
- **Eval 04 (unrun-or-silent-failure-blocked):** this is the core check — the gate **must** force Block on **either** the not-run precondition (B1) **or** the silent-failure catch-all (B2); both are present and either alone is sufficient. A verdict that notes the catch-all but still lands Conditional Pass, or that misses the "I haven't run it" line entirely, is a ❌ on eval 04.
- The distinction the gate must hold: the not-run precondition is an **automatic Block** that short-circuits the scorecard — the gate should surface it explicitly, not bury it as one ⚠ among six.
