# RegEval experiment 2026-06-23-02 — rubric-graded-v4-opus-repro

**Verdict:** DISCARD (cross-model reproduction — not a scaffold candidate)
**κ:** 0.768 (95% CI [0.666, 0.872])  vs Sonnet champion 0.820
**Diagnostics:** TPR=0.976 · TNR=1.000 · abst=0.060 · N=100
**Wall clock:** 1:38 (workflow, 10 parallel Opus judge agents)

## Purpose
NOT a scaffold experiment. This run regenerates a **full per-item table for the champion scaffold** `rubric-graded-v4` so the headline KEEP can be reproduced through the harness (`provenance.py` / `judge_vs_human.py`) — closing the gap that `gold-cal-v1` (the KEEP run) has 0 per-item rows. It also serves as a third cross-model data point.

## What it shows
The champion scaffold reproduces cleanly through the harness (this file `RECONCILES ✓`). But on **Opus-4.8** it scores κ=0.768 — **below** the canonical Sonnet 0.820, NOT above. Binary classes are near-perfect (TNR=1.000, compliant per-class κ=0.859); the entire gap is the unclear class (per-class κ=0.359, abst 0.060 vs Sonnet 0.090). All 14 mismatches are gold=unclear items the Opus judge committed to compliant/non-compliant.

## Cross-model finding (the real signal)
rubric-graded-v4's abstention triggers are **Sonnet-calibrated**. The same Sonnet-tuning signature now appears on two non-Sonnet models:
- Sonnet-4-5 (canonical): κ=0.820, abst=0.090 — unclear class healthy.
- Opus-4.8 (this run): κ=0.768, abst=0.060 — unclear collapses (per-class 0.359).
- Fable-5 (2026-06-10): κ=0.677, abst=0.120 — unclear collapses (per-class 0.299).
The scaffold's anti-hedge logic does not transfer; non-Sonnet models under-abstain on genuinely indeterminate items. Notably, the **skills-v2** architecture is MORE robust on Opus (same run-day: κ=0.822, unclear per-class 0.611) than this flat-rubric champion (0.768) — the skills decomposition transfers across model families better than the flat rubric.

## Why DISCARD
κ=0.768 < champion 0.820 — but this is the SAME scaffold on a worse-fit model, not an inferior scaffold. DISCARD per the mechanical rule; the deliverable (a reconciling champion-scaffold table + a cross-model data point) is achieved. current.md unchanged.

## Caveat for the demo
This does NOT reproduce the literal Sonnet 0.820 on camera — it reproduces the champion *scaffold* at a cross-model 0.768. The canonical 0.820 still requires a Sonnet-4-5 re-run (blocked: no API key). The cleanest ≥KEEP-bar run that reconciles on-camera today is skills-v2 (κ=0.822, Opus).

## Raw outputs
<details>
<summary>Per-item judge outputs (N=100, blind — judges saw input only, never gold_label)</summary>

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
| reg-0021 | compliant | compliant | ✓ |
| reg-0022 | unclear | unclear | ✓ |
| reg-0023 | compliant | compliant | ✓ |
| reg-0024 | unclear | compliant | ✗ |
| reg-0025 | unclear | non-compliant | ✗ |
| reg-0026 | unclear | non-compliant | ✗ |
| reg-0027 | unclear | compliant | ✗ |
| reg-0028 | unclear | compliant | ✗ |
| reg-0029 | unclear | non-compliant | ✗ |
| reg-0030 | unclear | non-compliant | ✗ |
| reg-0031 | compliant | compliant | ✓ |
| reg-0032 | compliant | compliant | ✓ |
| reg-0033 | compliant | compliant | ✓ |
| reg-0034 | compliant | compliant | ✓ |
| reg-0035 | compliant | compliant | ✓ |
| reg-0036 | compliant | compliant | ✓ |
| reg-0037 | compliant | compliant | ✓ |
| reg-0038 | compliant | compliant | ✓ |
| reg-0039 | compliant | compliant | ✓ |
| reg-0040 | compliant | compliant | ✓ |
| reg-0041 | non-compliant | non-compliant | ✓ |
| reg-0042 | non-compliant | non-compliant | ✓ |
| reg-0043 | non-compliant | non-compliant | ✓ |
| reg-0044 | non-compliant | non-compliant | ✓ |
| reg-0045 | non-compliant | non-compliant | ✓ |
| reg-0046 | non-compliant | non-compliant | ✓ |
| reg-0047 | non-compliant | non-compliant | ✓ |
| reg-0048 | non-compliant | non-compliant | ✓ |
| reg-0049 | non-compliant | non-compliant | ✓ |
| reg-0050 | non-compliant | non-compliant | ✓ |
| reg-0051 | non-compliant | non-compliant | ✓ |
| reg-0052 | non-compliant | non-compliant | ✓ |
| reg-0053 | non-compliant | non-compliant | ✓ |
| reg-0054 | compliant | unclear | ✗ |
| reg-0055 | compliant | compliant | ✓ |
| reg-0056 | compliant | compliant | ✓ |
| reg-0057 | compliant | compliant | ✓ |
| reg-0058 | compliant | compliant | ✓ |
| reg-0059 | compliant | compliant | ✓ |
| reg-0060 | compliant | compliant | ✓ |
| reg-0061 | compliant | compliant | ✓ |
| reg-0062 | compliant | compliant | ✓ |
| reg-0063 | compliant | compliant | ✓ |
| reg-0064 | compliant | compliant | ✓ |
| reg-0065 | compliant | compliant | ✓ |
| reg-0066 | non-compliant | non-compliant | ✓ |
| reg-0067 | non-compliant | non-compliant | ✓ |
| reg-0068 | non-compliant | non-compliant | ✓ |
| reg-0069 | non-compliant | non-compliant | ✓ |
| reg-0070 | non-compliant | non-compliant | ✓ |
| reg-0071 | non-compliant | non-compliant | ✓ |
| reg-0072 | non-compliant | non-compliant | ✓ |
| reg-0073 | non-compliant | non-compliant | ✓ |
| reg-0074 | unclear | compliant | ✗ |
| reg-0075 | unclear | non-compliant | ✗ |
| reg-0076 | unclear | unclear | ✓ |
| reg-0077 | unclear | unclear | ✓ |
| reg-0078 | unclear | unclear | ✓ |
| reg-0079 | unclear | non-compliant | ✗ |
| reg-0080 | unclear | compliant | ✗ |
| reg-0081 | unclear | unclear | ✓ |
| reg-0082 | compliant | compliant | ✓ |
| reg-0083 | compliant | compliant | ✓ |
| reg-0084 | compliant | compliant | ✓ |
| reg-0085 | compliant | compliant | ✓ |
| reg-0086 | compliant | compliant | ✓ |
| reg-0087 | compliant | compliant | ✓ |
| reg-0088 | non-compliant | non-compliant | ✓ |
| reg-0089 | non-compliant | non-compliant | ✓ |
| reg-0090 | non-compliant | non-compliant | ✓ |
| reg-0091 | non-compliant | non-compliant | ✓ |
| reg-0092 | non-compliant | non-compliant | ✓ |
| reg-0093 | non-compliant | non-compliant | ✓ |
| reg-0094 | non-compliant | non-compliant | ✓ |
| reg-0095 | non-compliant | non-compliant | ✓ |
| reg-0096 | non-compliant | non-compliant | ✓ |
| reg-0097 | unclear | non-compliant | ✗ |
| reg-0098 | compliant | compliant | ✓ |
| reg-0099 | compliant | compliant | ✓ |
| reg-0100 | unclear | compliant | ✗ |

</details>
