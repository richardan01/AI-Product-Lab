# Experiment 2026-05-29-02 — rubric-lenient

**Verdict:** HOLD
**κ:** 0.600 (95% CI [0.354, 0.798])  vs champion 0.000 (placeholder) · baseline 0.500
**Diagnostics:** TPR=0.900 · TNR=1.000 · abst=0.133 · N=30
**Per-class κ:** compliant=0.651 · non-compliant=0.791 · unclear=0.294
**Wall clock:** ~1:00  (blind-grader run, start 2026-05-29T02:40 UTC → end ~02:45 UTC)
**Gold snapshot:** `inputs/snapshots/2026-05-29.jsonl` (30 items; compliant=10, non-compliant=10, unclear=10)
**Grader separation:** scaffold authored by Lucius (this session); labels produced by a blind grader subagent given inputs stripped of `gold_label`.

## Hypothesis

Lifting the anti-hedge clause and permitting `unclear` whenever the governing obligation or context cannot be established will recover the abstention miss that capped baseline at 0.500.

## Scaffold delta vs champion (baseline)

- Abstention policy: anti-hedge clause removed; `unclear` is a first-class answer
- Decomposition adds an explicit gate: 'is the governing obligation determinable from the text alone?'
- Rubric `unclear` row broadened to cover undeterminable obligation, missing applicability context, and mixed-signal items

## Result narrative

Recovered 3/10 `unclear` (reg-0003, 0022, 0027, 0029 region) and moved κ to 0.600. But the permissive policy also cost one true-`compliant` (reg-0003 → unclear), dropping TPR to 0.90. Net κ improvement +0.10 over baseline; abstention is confirmed as the lever, but recall on `unclear` is still only 0.30 — most indeterminate items still read as confidently binary.

## Why this verdict

κ=0.600 beats baseline 0.500 and recovers part of the abstention class, but misses the 0.80 KEEP bar and trades a binary error for the abstention gain.

## Next experiment suggestion

Combine graded's enumerated triggers with lenient's permissiveness; target the 7 still-missed `unclear` items that present as superficially binary.

---

## Raw outputs

<details>
<summary>Per-item judge outputs (30 items)</summary>

| id | gold | judge | match |
|---|---|---|---|
| reg-0001 | compliant | compliant | ✓ |
| reg-0002 | compliant | compliant | ✓ |
| reg-0003 | compliant | unclear | ✗ |
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
| reg-0022 | unclear | unclear | ✓ |
| reg-0023 | unclear | compliant | ✗ |
| reg-0024 | unclear | compliant | ✗ |
| reg-0025 | unclear | non-compliant | ✗ |
| reg-0026 | unclear | non-compliant | ✗ |
| reg-0027 | unclear | unclear | ✓ |
| reg-0028 | unclear | compliant | ✗ |
| reg-0029 | unclear | unclear | ✓ |
| reg-0030 | unclear | non-compliant | ✗ |

</details>

---

## Confusion matrix (rows = gold, cols = judge)

|  | judge=compliant | judge=non-compliant | judge=unclear |
|---|---|---|---|
| gold=compliant | 9 | 0 | 1 |
| gold=non-compliant | 0 | 10 | 0 |
| gold=unclear | 4 | 3 | 3 |
