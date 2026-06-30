# Experiment 2026-05-29-03 — rubric-graded

**Verdict:** HOLD
**κ:** 0.600 (95% CI [0.405, 0.793])  vs champion 0.000 (placeholder) · baseline 0.500
**Diagnostics:** TPR=1.000 · TNR=1.000 · abst=0.067 · N=30
**Per-class κ:** compliant=0.667 · non-compliant=0.791 · unclear=0.250
**Wall clock:** ~1:00  (blind-grader run, start 2026-05-29T02:40 UTC → end ~02:45 UTC)
**Gold snapshot:** `inputs/snapshots/2026-05-29.jsonl` (30 items; compliant=10, non-compliant=10, unclear=10)
**Grader separation:** scaffold authored by Lucius (this session); labels produced by a blind grader subagent given inputs stripped of `gold_label`.

## Hypothesis

Enumerated explicit `unclear` triggers will calibrate the abstention class to the gold panel more precisely than a broad 'abstain when uncertain' rule, lifting κ without over-abstaining.

## Scaffold delta vs champion (baseline)

- Abstention policy replaced with 4 enumerated triggers (no obligation / missing applicability context / conflicting signals / out-of-scope jurisdiction)
- Decomposition checks the enumerated triggers in order before committing to a binary label
- Rubric `unclear` row defined by trigger-firing rather than general uncertainty

## Result narrative

Recovered 2/10 `unclear` (reg-0022, 0029) while keeping TPR=1.00 and TNR=1.00 — no binary-class damage. κ=0.600, tied with lenient but with cleaner diagnostics. The enumerated triggers fired only on the items that visibly lack an obligation; the harder `unclear` items (where an obligation is referenced but satisfaction is unverifiable) still read as compliant.

## Why this verdict

κ=0.600 beats baseline 0.500 with zero binary-class regression, making it the cleaner base scaffold; still below the 0.80 KEEP bar.

## Next experiment suggestion

Add a 5th trigger for 'obligation referenced but satisfaction not verifiable from text' — the pattern behind the remaining 8 missed `unclear` items.

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
| reg-0022 | unclear | unclear | ✓ |
| reg-0023 | unclear | compliant | ✗ |
| reg-0024 | unclear | compliant | ✗ |
| reg-0025 | unclear | non-compliant | ✗ |
| reg-0026 | unclear | non-compliant | ✗ |
| reg-0027 | unclear | compliant | ✗ |
| reg-0028 | unclear | compliant | ✗ |
| reg-0029 | unclear | unclear | ✓ |
| reg-0030 | unclear | non-compliant | ✗ |

</details>

---

## Confusion matrix (rows = gold, cols = judge)

|  | judge=compliant | judge=non-compliant | judge=unclear |
|---|---|---|---|
| gold=compliant | 10 | 0 | 0 |
| gold=non-compliant | 0 | 10 | 0 |
| gold=unclear | 5 | 3 | 2 |
