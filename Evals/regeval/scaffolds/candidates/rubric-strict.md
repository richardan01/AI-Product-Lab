# Scaffold: rubric-strict

**Slug:** rubric-strict
**Version:** 1
**Created:** 2026-05-29
**Status:** candidate
**Author:** Lucius Fox
**Label set:** compliant · non-compliant · unclear
**Parent:** baseline
**Element varied:** abstention policy + judge rubric (binary reasoning unchanged)

> **Hypothesis:** Tightening `unclear` to genuine regulatory indeterminacy only — while raising the bar for a `compliant` finding — tests whether the gold panel's `unclear` items are truly indeterminate (strict stays near 0/10, confirming abstention must be broadened) or merely borderline-binary (strict recovers some). This is the low-abstention control point on the operating curve.

---

## System prompt

You are a financial compliance reviewer. You will be given a text excerpt from a
financial document. Classify it as one of three labels:

- **compliant** — the text affirmatively and completely meets the applicable regulatory standard
- **non-compliant** — the text violates or likely violates the applicable regulatory standard
- **unclear** — no applicable regulatory standard can be identified from the text at all

Hold a high bar for **compliant**: partial satisfaction, vague gestures at a process,
or missing required elements default to **non-compliant**, not compliant. Reserve
**unclear** strictly for the case where no governing obligation is identifiable.

Think step-by-step, then output your label and a one-sentence rationale.

---

## Decomposition steps

1. Read the text.
2. Attempt to identify a specific regulatory obligation. If none is identifiable at all → `unclear`.
3. If an obligation is identifiable: does the text **fully and explicitly** satisfy it?
   - Fully satisfied → compliant
   - Anything less (partial, vague, missing element, violation) → non-compliant
4. Output label and rationale.

---

## Judge rubric

| Label | Apply when |
|---|---|
| compliant | A regulatory obligation is identifiable and the text **fully and explicitly** satisfies it with no missing required element |
| non-compliant | A regulatory obligation is identifiable and the text fails to fully satisfy it — including partial satisfaction, omission, vagueness, or violation |
| unclear | No applicable regulatory obligation can be identified from the text at all |

Rationale must be ≤ one sentence (≤ 30 words). Do not cite specific regulation codes
unless provided in the input.

---

## Abstention policy

Use **unclear** only when **no** governing regulatory obligation can be identified from
the text. Do not use `unclear` for partial information, conflicting signals, or
borderline judgement — in those cases commit to the binary label (defaulting to
**non-compliant** when satisfaction is not affirmatively established).

This is deliberately the most restrictive abstention point, to bound the operating curve.

---

## Output format

```
label: <compliant|non-compliant|unclear>
rationale: <one sentence>
```

---

## Label mapping to metric

| Scaffold label | κ computation maps to |
|---|---|
| compliant | accept |
| non-compliant | reject |
| unclear | abstain |
