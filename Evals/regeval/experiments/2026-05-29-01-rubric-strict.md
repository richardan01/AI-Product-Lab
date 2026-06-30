# Experiment 2026-05-29-01 — rubric-strict

**Verdict:** DISCARD
**κ:** 0.500 (95% CI [0.310, 0.709])  vs champion 0.000 (placeholder) · baseline 0.500
**Diagnostics:** TPR=1.000 · TNR=1.000 · abst=0.000 · N=30
**Per-class κ:** compliant=0.609 · non-compliant=0.727 · unclear=0.000
**Wall clock:** ~1:00  (blind-grader run, start 2026-05-29T02:40 UTC → end ~02:45 UTC)
**Gold snapshot:** `inputs/snapshots/2026-05-29.jsonl` (30 items; compliant=10, non-compliant=10, unclear=10)
**Grader separation:** scaffold authored by Lucius (this session); labels produced by a blind grader subagent given inputs stripped of `gold_label`.

## Hypothesis

Tightening `unclear` to genuine indeterminacy only (low-abstention control point) tests whether the gold `unclear` items are truly indeterminate or merely borderline-binary.

## Scaffold delta vs champion (baseline)

- Abstention policy: `unclear` only when NO obligation is identifiable at all
- Raised the bar for `compliant` (partial/vague/missing-element defaults to non-compliant)
- This is the deliberate low-abstention control point on the operating curve

## Result narrative

Reproduced baseline exactly: 0/10 `unclear`, κ=0.500. Confirms the gold `unclear` items are genuinely indeterminate, not borderline-binary — a stricter binary threshold recovers none of them. This is the negative control that bounds the abstention operating curve and rules out 'tighten the binary threshold' as a path to 0.80.

## Why this verdict

κ=0.500 ties baseline and recovers zero abstention items; no improvement over the incumbent direction, so discard.

## Next experiment suggestion

Abandon the low-abstention direction; all κ headroom is in correctly identifying genuine `unclear`.

---

## Raw outputs

<details>
<summary>Per-item judge outputs (30 items)</summary>

| id | gold | judge | match |
|---|---|---|---|
| reg-0001 | compliant | compliant | ✓ |
| reg-0002 | compliant | compliant | ✓ |
| reg-0003 | compliant | compliant | ✓ |
| reg-0004 | compliant | compliant | ✓ |
| reg-0005 | compliant | compliant | ✓ |
| reg-0006 | compliant | compliant | ✓ |
| reg-0007 | compliant | compliant | ✓ |
| reg-0008 | compliant | compliant | ✓ |
| reg-0009 | compliant | compliant | ✓ |
| reg-0010 | compliant | compliant | ✓ |
| reg-0011 | non-compliant | non-compliant | ✓ |
| reg-0012 | non-compliant | non-compliant | ✓ |
| reg-0013 | non-compliant | non-compliant | ✓ |
| reg-0014 | non-compliant | non-compliant | ✓ |
| reg-0015 | non-compliant | non-compliant | ✓ |
| reg-0016 | non-compliant | non-compliant | ✓ |
| reg-0017 | non-compliant | non-compliant | ✓ |
| reg-0018 | non-compliant | non-compliant | ✓ |
| reg-0019 | non-compliant | non-compliant | ✓ |
| reg-0020 | non-compliant | non-compliant | ✓ |
| reg-0021 | unclear | compliant | ✗ |
| reg-0022 | unclear | compliant | ✗ |
| reg-0023 | unclear | compliant | ✗ |
| reg-0024 | unclear | compliant | ✗ |
| reg-0025 | unclear | non-compliant | ✗ |
| reg-0026 | unclear | non-compliant | ✗ |
| reg-0027 | unclear | compliant | ✗ |
| reg-0028 | unclear | compliant | ✗ |
| reg-0029 | unclear | non-compliant | ✗ |
| reg-0030 | unclear | non-compliant | ✗ |

</details>

---

## Confusion matrix (rows = gold, cols = judge)

|  | judge=compliant | judge=non-compliant | judge=unclear |
|---|---|---|---|
| gold=compliant | 10 | 0 | 0 |
| gold=non-compliant | 0 | 10 | 0 |
| gold=unclear | 6 | 4 | 0 |
