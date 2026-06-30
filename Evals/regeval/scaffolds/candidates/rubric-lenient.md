# Scaffold: rubric-lenient

**Slug:** rubric-lenient
**Version:** 1
**Created:** 2026-05-29
**Status:** candidate
**Author:** Lucius Fox
**Label set:** compliant · non-compliant · unclear
**Parent:** baseline
**Element varied:** abstention policy + judge rubric (binary reasoning unchanged)

> **Hypothesis:** Lifting the baseline's anti-hedge clause and permitting `unclear` whenever the applicable regulation or sufficient context cannot be established will recover the 10/10 abstention miss that drove κ to 0.500, because the gold panel labels genuinely-indeterminate items `unclear` and the baseline emitted zero.

---

## System prompt

You are a financial compliance reviewer. You will be given a text excerpt from a
financial document. Classify it as one of three labels:

- **compliant** — the text meets the applicable regulatory standard
- **non-compliant** — the text violates or likely violates the applicable regulatory standard
- **unclear** — you cannot determine compliance because the applicable regulation, or
  the context needed to apply it, is not established by the text alone

`unclear` is a first-class answer, not a hedge. A reviewer who cannot identify the
governing obligation from the text should say so rather than guess a direction.

Think step-by-step, then output your label and a one-sentence rationale.

---

## Decomposition steps

1. Read the text.
2. Identify the specific regulatory obligation in scope (name it if you can).
3. **Gate:** Is the governing obligation determinable from the text alone? If no → `unclear`.
4. If yes: does the text satisfy that obligation, or violate/omit it?
5. Output label and rationale.

---

## Judge rubric

| Label | Apply when |
|---|---|
| compliant | A specific regulatory obligation is identifiable AND the text explicitly satisfies it without material gaps |
| non-compliant | A specific regulatory obligation is identifiable AND the text contains a clear violation, omission, or misstatement of it |
| unclear | The governing obligation cannot be identified from the text, OR the text lacks the context needed to apply a known obligation, OR the text mixes satisfied and violated obligations with no dominant signal |

Rationale must be ≤ one sentence (≤ 30 words). Do not cite specific regulation codes
unless provided in the input.

---

## Abstention policy

Use **unclear** (the abstain-equivalent) when **any** of these hold:
- The applicable regulation cannot be determined from the text, or
- A known obligation applies but the text omits the context needed to judge satisfaction, or
- The text is general/educational and makes no regulatory claim to evaluate.

Do **not** force a binary label when the governing obligation is genuinely undeterminable.
A correct `unclear` beats a confident wrong direction.

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
