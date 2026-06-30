# Failure transition matrix — onboarding

Tracks **first failures** in the 9-phase onboarding workflow per Hamel & Shankar §8.3. When `eval-grader` flags a ❌, the grader (or post-aggregator) records which phase transition produced the first failure in that trace. Over time, the matrix surfaces hotspot phases for targeted workflow fixes.

## How to use

After each run, for every ❌ in the result file, append a row to `## Recorded transitions` below with:
- `trace_id` or fixture name
- `from_state`: the last successfully completed phase
- `in_state`: the phase during which the first failure occurred
- `eval_id`: which eval caught it
- `one_line_what_failed`

After ≥ 5 runs, compute the matrix below.

## States (onboarding workflow phases)

| ID | Phase | Description |
|---|---|---|
| P0 | Greeting | "Computer, onboard me" trigger |
| P1 | Persona selection | One of Executive / Researcher / Coach / Builder / AI PM / Minimalist / Custom |
| P2 | Taste questions | Tone, detail level, turn-offs, ideal feel |
| P3 | Identity capture | Name, role, company, team, manager |
| P4 | Read-back | Confirm persona + identity + taste in three separate steps |
| P5 | OKR alignment | Strategic ladder-up, proof metric, kill conditions |
| P5B | Thought frameworks | Tradeoff priority, evidence standard, decision certainty bar, acceptable failure |
| P6 | Stakeholders | Confirm per-stakeholder before drafting profiles |
| P7 | Anchor project | Project brief + key dates |
| P8 | Phase 8 summary | Enumerated edit plan, awaiting explicit approval |
| P9 | Per-file writes | Confirm each file individually before writing |
| P10 | Verification | Three-way choice (fill / defer / accept with reason) on any ❌ |

## Recorded transitions

| Run date | Trace / fixture | from_state | in_state | eval_id | what_failed |
|---|---|---|---|---|---|

(append one row per ❌; populated by eval-grader output)

## Transition matrix (compute after ≥ 5 runs)

Rows = `from_state` (last successful phase). Columns = `in_state` (first failure phase). Cell counts the number of times a first failure occurred in column `j` immediately after column `i` completed successfully.

|              | P0 | P1 | P2 | P3 | P4 | P5 | P5B | P6 | P7 | P8 | P9 | P10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **P0**       | — |   |   |   |   |   |    |   |   |   |   |    |
| **P1**       |   | — |   |   |   |   |    |   |   |   |   |    |
| **P2**       |   |   | — |   |   |   |    |   |   |   |   |    |
| **P3**       |   |   |   | — |   |   |    |   |   |   |   |    |
| **P4**       |   |   |   |   | — |   |    |   |   |   |   |    |
| **P5**       |   |   |   |   |   | — |    |   |   |   |   |    |
| **P5B**      |   |   |   |   |   |   | —  |   |   |   |   |    |
| **P6**       |   |   |   |   |   |   |    | — |   |   |   |    |
| **P7**       |   |   |   |   |   |   |    |   | — |   |   |    |
| **P8**       |   |   |   |   |   |   |    |   |   | — |   |    |
| **P9**       |   |   |   |   |   |   |    |   |   |   | — |    |
| **P10**      |   |   |   |   |   |   |    |   |   |   |   |  — |

## Hotspot analysis (after matrix is populated)

After the matrix has ≥ 10 recorded transitions:

1. **Column sum** identifies the overall most-failing phase. That's the highest-leverage workflow fix target.
2. **Cell intensity** identifies specific transition hotspots — e.g. if `P8 → P9` has high count, the Phase 8 summary may not be enumerating files clearly enough, so the model batches at Phase 9.
3. **Row sparsity**: phases that never appear as `from_state` may indicate runs aren't reaching that phase reliably (an earlier failure is masking later ones).

Update this analysis section after each milestone run.
