# Eval suite — memory-consolidation

Tests that the daily `myos-memory-consolidation` routine writes memory that is **(a) faithful to its source window** and **(b) loses no still-valid context** — the two failure modes that would silently corrupt the OS's long-term memory.

## Why this suite exists

The consolidation routine runs unattended every morning and writes directly to auto-memory (`~/.claude/projects/.../memory/`). Its failure modes are quiet and compounding: a **fabricated fact** (drift from ground truth) or a **dropped/overwritten fact** (context loss) persists and is then loaded into every future session. This suite is the offline check that the routine stays near ground truth as models and inputs change.

Two layers guard the memory:
- **Inline self-verification** — Step 6 of the routine itself. Fast, every run, logs to `consolidation-verification-log.md`.
- **This offline suite** — rigorous, author/grader separated, run on cadence and after every model upgrade.

## Criteria

| Eval                          | Tests for                                                                                             |
| ----------------------------- | ----------------------------------------------------------------------------------------------------- |
| 01-faithful-to-source         | Every written claim traces to a specific source in the window                                         |
| 02-no-invented-facts          | No name / date / number / decision absent from the sources                                            |
| 03-context-preserved          | No still-valid memory dropped or overwritten without a superseding source; high-signal items captured |
| 04-dedup-and-canonicality     | Updates existing files vs duplicating; never contradicts Knowledge/People + Knowledge/Reference       |
| 05-freshness-and-completeness | `Last consolidated` bumped; full window covered (no sessions skipped); learnings appended             |

## Pass-rate target

**≥ 4/5 — AND 01 + 02 are mandatory.** A single fabricated fact is an automatic Block regardless of the other scores. Faithfulness is non-negotiable for a memory system.

Per-run grading is the 5 binary criteria above. The **weekly quantitative metric** — precision (≥0.98), sampled recall (≥0.85), F1 headline, judge validation by TPR/TNR, and why accuracy is excluded — is defined in `metric.md`.

## Run protocol

See `protocol.md`. Author/grader separation enforced: the routine's run is the author; a **separate** context grades. The routine never grades its own output (that's the inline check, not this suite).

## Fixtures

A fixture is a dated `[LASTRUN → TODAY]` window with known content + a gold expectation. See `inputs/`.

## Last run

**2026-06-20** · `claude-opus-4-8` · **PASS** (3/5 PASS + 2 PARTIAL; 01+02 mandatory ✅) · Precision 100% (23/23), Recall 95.2% (20/21), F1 97.5% — *provisional-measured*, gold DRAFT pending Rich. First fixture `2026-06-20-heavy-day`. See `results/2026-06-20_claude-opus-4-8.md`.

## Related

[[Evals/index]] · [[Evals/research-synthesis/research-synthesis-suite]] · [[Evals/eval-audit-checklist]] · scheduled task `myos-memory-consolidation`
