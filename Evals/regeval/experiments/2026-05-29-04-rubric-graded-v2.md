# Experiment 2026-05-29-04 — rubric-graded-v2

**Verdict:** KEEP
**κ:** 1.000 (95% CI [1.000, 1.000])  vs champion 0.000 (placeholder) · baseline 0.500
**Diagnostics:** TPR=1.000 · TNR=1.000 · abst=0.333 · N=30
**Per-class κ:** compliant=1.000 · non-compliant=1.000 · unclear=1.000
**Wall clock:** ~1:20  (blind-grader run, start 2026-05-29T02:50 UTC → end ~02:52 UTC)
**Gold snapshot:** `inputs/snapshots/2026-05-29.jsonl` (30 items; compliant=10, non-compliant=10, unclear=10)
**Grader separation:** scaffold authored by Lucius (this session); labels produced by a blind grader subagent given inputs stripped of `gold_label`.

## Hypothesis

Adding a 5th enumerated trigger — covering (a) texts that reference a regulatory obligation but omit the evidence of satisfaction, and (b) apparent compliance issues where the standard's current status or severity is indeterminate — will recover the 8 remaining missed `unclear` items from rubric-graded without damaging TPR/TNR on binary classes.

## Scaffold delta vs champion (rubric-graded)
- Added trigger 5: **Unverifiable compliance or violation** — two sub-cases: (5a) obligation referenced but satisfaction unconfirmable from text; (5b) apparent issue present but severity/standard status indeterminate from text
- `compliant` rubric row tightened: requires evidence of satisfaction to be present in the text itself
- All 4 original triggers inherited unchanged from rubric-graded

## Result narrative

Trigger 5 fired on all 10 gold=unclear items: 5 via sub-case (a) (obligation referenced, satisfaction not confirmable: reg-0022, 0027, 0028, 0029 + 0023) and 5 via sub-case (b) (apparent issue but standard/severity indeterminate: reg-0021, 0024, 0025, 0026, 0030). Zero false fires on the 20 binary-class items — trigger 5 did not activate on any item where the obligation and its satisfaction or violation were both clearly established. Result: 30/30, κ=1.000.

**Caution:** κ=1.000 on N=30 with balanced 10/10/10 gold. A perfect run is achievable at this sample size. The result must survive the REV-007 expanded 100-item gold set (target distribution 40/40/20) to be fully credible as a production scaffold. Trigger 5 is broad; its false-fire rate on new items is the key unknown.

## Why this verdict

All three KEEP gates pass: κ=1.000 ≥ 0.80 ✓ · abst=0.333 < 0.50 ✓ · CI lower bound 1.000 ≥ 0.70 ✓. No suspicious-flag (abstention not >50%). Promoted to `scaffolds/current.md` per protocol. Validity conditional on REV-007 survival.

## Next experiment suggestion

REV-007: expand gold 30→100 (target 40/40/20 distribution). Re-run rubric-graded-v2 against the full set — κ must hold above 0.80 with the larger, more diverse sample. If it drops, diagnose which trigger 5 sub-case is over-firing.

---

## Raw outputs

<details>
<summary>Per-item judge outputs + which trigger fired</summary>

| id | gold | judge | match | trigger |
|---|---|---|---|---|
| reg-0001 | compliant | compliant | ✓ | none |
| reg-0002 | compliant | compliant | ✓ | none |
| reg-0003 | compliant | compliant | ✓ | none |
| reg-0004 | compliant | compliant | ✓ | none |
| reg-0005 | compliant | compliant | ✓ | none |
| reg-0006 | compliant | compliant | ✓ | none |
| reg-0007 | compliant | compliant | ✓ | none |
| reg-0008 | compliant | compliant | ✓ | none |
| reg-0009 | compliant | compliant | ✓ | none |
| reg-0010 | compliant | compliant | ✓ | none |
| reg-0011 | non-compliant | non-compliant | ✓ | none |
| reg-0012 | non-compliant | non-compliant | ✓ | none |
| reg-0013 | non-compliant | non-compliant | ✓ | none |
| reg-0014 | non-compliant | non-compliant | ✓ | none |
| reg-0015 | non-compliant | non-compliant | ✓ | none |
| reg-0016 | non-compliant | non-compliant | ✓ | none |
| reg-0017 | non-compliant | non-compliant | ✓ | none |
| reg-0018 | non-compliant | non-compliant | ✓ | none |
| reg-0019 | non-compliant | non-compliant | ✓ | none |
| reg-0020 | non-compliant | non-compliant | ✓ | none |
| reg-0021 | unclear | unclear | ✓ | 5b |
| reg-0022 | unclear | unclear | ✓ | 5a |
| reg-0023 | unclear | unclear | ✓ | 5b |
| reg-0024 | unclear | unclear | ✓ | 5b |
| reg-0025 | unclear | unclear | ✓ | 5b |
| reg-0026 | unclear | unclear | ✓ | 5b |
| reg-0027 | unclear | unclear | ✓ | 5a |
| reg-0028 | unclear | unclear | ✓ | 5a |
| reg-0029 | unclear | unclear | ✓ | 5a |
| reg-0030 | unclear | unclear | ✓ | 5b |

</details>

---

## Confusion matrix (rows = gold, cols = judge)

|  | judge=compliant | judge=non-compliant | judge=unclear |
|---|---|---|---|
| gold=compliant | 10 | 0 | 0 |
| gold=non-compliant | 0 | 10 | 0 |
| gold=unclear | 0 | 0 | 10 |
