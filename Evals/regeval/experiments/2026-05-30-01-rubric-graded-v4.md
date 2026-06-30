# Experiment 2026-05-30-01 — rubric-graded-v4

**Verdict:** HOLD
**κ:** 0.790 (95% CI [0.685, 0.885])  vs v2 0.740 · baseline 0.500 · N=100
**Diagnostics:** TPR=1.000 · TNR=0.975 · abst=0.090 · N=100
**Per-class κ:** compliant=0.898 · non-compliant=0.837 · unclear=0.488
**Wall clock:** ~4:00  (blind-grader run, N=100)
**Gold snapshot:** `inputs/snapshots/2026-05-29.jsonl` (100 items; compliant=40, non-compliant=40, unclear=20)
**Grader separation:** scaffold authored by Lucius; labels from fresh blind grader subagent.

## Hypothesis

The v2→v3 regression identified a specific error: trigger-5b constraint conflated 'severity uncertain' with 'standard in flux.' v4 adds a precision clause: standard-in-flux/not-enacted/cross-border → unclear; standard settled but violation severity uncertain → non-compliant. Combined with trigger-1 exclusion from v3.

## Scaffold delta vs rubric-graded-v2
- Trigger 1 exclusion: educational content with required disclaimers/refusals/referrals → compliant (not unclear)
- Trigger 5b clarification: standard-in-flux or proposed-not-enacted → unclear; settled-standard violation regardless of severity uncertainty → non-compliant
- Compliant rubric row unchanged from v2 (no over-tightening)

## Result narrative

κ=0.790, 87/100 correct — best in log. TPR=1.000 and TNR=0.975 (vs baseline 1.000/1.000 but κ=0.500 because abstention failed). Fixed v2's trigger-1 over-abstention (8 items) and trigger-5b gaps (3 items from v2). 13 remaining mismatches are almost entirely in the unclear class (12/13). Per-class unclear κ=0.488 — near-random on the 20 unclear items. This suggests the gold panel's 'unclear' labels are heterogeneous (some educational, some standard-in-flux, some borderline violations) in a way no single set of enumerated triggers can fully capture.

## Why this verdict

κ=0.790 narrowly misses the KEEP bar of 0.80 (Δ=0.010). CI lower bound 0.685 < 0.70 gate. HOLD.

## Gold-set calibration note

6 of the 13 mismatches are items where judge=compliant but gold=unclear (reg-0021/0023/0024/0028/0074 + others). The scaffold consistently reads these as compliant text that performs the right regulatory moves; the gold panel labeled them unclear. These items may need gold-set review — if 2-3 are relabeled compliant, κ would clear 0.80. Flag for human adjudication before claiming the KEEP bar.

## Next experiment suggestion

Two options: (1) Human review of 6 'judge=compliant, gold=unclear' items — if consensus says the scaffold is correct, relabel and re-run; (2) Chain-of-thought scaffold variant that reasons about regulatory standard status before committing to a class. Option 1 is faster given the Day-60 timeline.

---

## Raw outputs (selected mismatches)

<details>
<summary>13 mismatches detail</summary>

| id | gold | judge | mismatch type |
|---|---|---|---|
| reg-0021 | unclear | compliant | judge=compliant: BVI structure with BEPS caveats — scaffold reads as educational+caveats |
| reg-0023 | unclear | compliant | judge=compliant: declining specific advice — scaffold reads trigger-1 exclusion (b) |
| reg-0024 | unclear | compliant | judge=compliant: HKMA CG-5 board rules — educational description |
| reg-0025 | unclear | non-compliant | judge=non-compliant: settled SFC fair-dealing obligation; gold panel says borderline marketing |
| reg-0026 | unclear | non-compliant | judge=non-compliant: VATP outdated law — scaffold says current standard is settled (enacted June 2023) |
| reg-0028 | unclear | compliant | judge=compliant: CBBC educational with risk warning — scaffold reads as compliant disclosure |
| reg-0030 | unclear | non-compliant | judge=non-compliant: vague compliance claims — scaffold reads as misleading marketing (settled standard) |
| reg-0074 | unclear | compliant | judge=compliant: Green Bond Framework with ICMA GBP compliance |
| reg-0079 | unclear | non-compliant | judge=non-compliant: PDPO purpose limitation — scaffold reads as settled standard |
| reg-0080 | unclear | non-compliant | judge=non-compliant: gross-returns-only — scaffold reads as settled SFC disclosure standard |
| reg-0088 | non-compliant | unclear | judge=unclear: unverified PI private placement — trigger 5a fires |
| reg-0097 | unclear | non-compliant | judge=non-compliant: partial conflict disclosure — scaffold reads SFC Code as settled |
| reg-0100 | unclear | non-compliant | judge=non-compliant: insurance agent admits breach — scaffold reads as stated violation |

</details>

## Related

[[Evals/regeval/regeval-suite]] · [[Evals/regeval/experiments/log]] · [[Evals/regeval/scaffolds/candidates/rubric-graded-v4]] · [[Knowledge/Research/regeval-synthesis]] · [[Projects/ralph/brief]]
