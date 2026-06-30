# Run protocol — memory-consolidation eval suite

Adapted from `Evals/research-synthesis/protocol.md`. Same author/grader separation rules apply.

## 1. Fix the run inputs

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Model | e.g. `claude-opus-4-8` |
| Routine version | `~/.claude/scheduled-tasks/myos-memory-consolidation/SKILL.md` (note last-modified) |
| Window | `LASTRUN → TODAY`, or a fixture id from `inputs/` |
| Runner agent | The session/run that executed the consolidation |
| Grader agent | **Separate** context — must not be the runner |

Runner ≠ Grader. Self-graded runs do not count.

## 2. Produce the artifact to grade

**Fixture mode** — run the consolidation logic against a fixture window in `inputs/`; capture the resulting memory writes (new files + diffs of changed files) verbatim to `results/transcripts/YYYY-MM-DD_<fixture>_<model>.md`.

**Live mode** — before a real run, snapshot the memory dir to `results/snapshots/YYYY-MM-DD_pre/`; after the run, capture the diff. Include the routine's own `consolidation-verification-log.md` entry for that date.

## 3. Grade independently

The grader reads only:
- The captured memory writes / diff
- The source window (in-range `*.jsonl` transcripts + `git log --since` + relevant `Decisions/` and `Tasks/`)
- Each `criteria.md`

The grader does **not** read the routine prompt or the runner's notes.

Grade each criterion ✅ / ❌ / ⚠ partial. Partials are not rounded up. For each ❌, run the introspection loop:
> "Why did the routine write (or drop) this? What in the prompt or the window led to it?"

## 4. Aggregate

Run all 5 criteria against all fixtures. Report per-fixture and per-criterion pass rate. **01 or 02 failing = Block**, regardless of total.

## 5. Log

Write `results/YYYY-MM-DD_<model>.md`: header table, per-criterion ✅/❌ per fixture, pass rate, introspection for every ❌, recommended routine-prompt changes. Append one line to `Evals/run-log.md` and update the "Last run" cell in `Evals/index.md`.

## 6. Anti-patterns

- **Grading from memory.** Work from the captured diff only.
- **Self-grading.** The routine checking its own output is the inline Step-6 guard, not this suite.
- **Skipping the conflicting-facts fixture.** It tests canonicality + drift — the highest-value failure mode.
- **Calling one clean run "validated."** A single run is a baseline. Re-run after every model upgrade.
- **Skipping introspection on ❌.** A failure without a "why" is half a result.

## Related

[[Evals/memory-consolidation/memory-consolidation-suite]] · [[Evals/index]] · [[Evals/eval-audit-checklist]] · [[Evals/research-synthesis/protocol]]
