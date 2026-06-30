# Scaffold: challenger-v1

**Slug:** challenger-v1  
**Version:** 1  
**Created:** 2026-06-08  
**Status:** candidate  
**Author:** Lucius Fox  
**Architecture:** Two-agent (judge + adversarial challenger)  
**Parent:** skills-v1 (run skills-v1 first; challenger-v1 requires skills-v1 as judge)  
**Experiment dependency:** Run AFTER skills-v1 experiment. Challenger wraps the judge, not the baseline.

> **Hypothesis:** Adding an adversarial challenger sub-agent that tries to REFUTE the judge's classification will improve κ beyond skills-v1 by catching cases where the judge over-committed. The Anthropic analytics blog found +6% accuracy at +32% token cost using this pattern. At RegEval scale (N=100), expect improvement on the marginal unclear items where the judge currently commits incorrectly.

> **Token cost note:** Do NOT use a cheaper model for the challenger. The blog found accuracy gains evaporate with a smaller model. Use the same model as the judge.

> **Run protocol:** This scaffold requires TWO model calls per item. Wall-clock budget applies to the full two-call sequence. If the challenger + judge round-trip exceeds 8 min for the full gold set, log as FAIL (budget exceeded) — do not extend.

---

## Stage 1 — Judge prompt (same as skills-v1 system prompt)

Use the `skills-v1` scaffold system prompt as Stage 1. Record:
- `judge_label`: the judge's output label
- `judge_rationale`: the judge's rationale

---

## Stage 2 — Challenger prompt

**System prompt:**

You are an adversarial compliance reviewer. Your job is to REFUTE the judge's classification of a financial compliance text. You are NOT trying to find a better answer — you are trying to find a reason the judge's answer is wrong.

Default to `refuted: true` if you are uncertain. Only mark `refuted: false` if you are confident the judge's classification is clearly correct and you cannot construct a reasonable counter-argument.

**User message template:**

```
## Regulation text to review

{{input}}

## Judge's classification

label: {{judge_label}}
rationale: {{judge_rationale}}

## Your task

Try to refute this classification. Consider:
- Is there a trigger the judge missed that changes the label?
- Did the judge apply a trigger that shouldn't fire?
- Is the judge's label on the wrong side of a close call?
- Did the judge miss an obligation or misidentify the scope?

Output exactly:
refuted: <true|false>
reason: <one sentence, ≤ 30 words — why this classification is wrong OR why it is clearly correct>
```

---

## Stage 3 — Resolution logic

| Judge label | Challenger verdict | Final label |
|---|---|---|
| any | `refuted: false` | Judge label stands |
| any | `refuted: true` | Re-classify: flip compliant ↔ non-compliant; if unclear → keep unclear; if compliant → non-compliant; if non-compliant → compliant |

> **Simplification for first experiment:** On refutation, flip the binary labels (compliant ↔ non-compliant). If the judge said unclear and challenger refutes, keep unclear (challenger cannot un-abstain). This is a conservative resolution — measure δκ vs. always accepting judge.

> **Alternative to test in challenger-v2:** On refutation, return to judge with challenger's counter-argument for a final verdict. Two-stage costs more tokens; measure whether the extra call improves on simple flip.

---

## Output format (per item)

```
judge_label: <compliant|non-compliant|unclear>
judge_rationale: <one sentence>
refuted: <true|false>
challenger_reason: <one sentence>
final_label: <compliant|non-compliant|unclear>
```

---

## Experiment log fields (add to standard template)

- `challenger_refutation_rate`: % of items where challenger refuted judge
- `refutation_flip_rate`: % of refutations where flip changed κ positively
- `token_delta_vs_skills-v1`: estimated token multiplier (expect ~1.3–1.5x)
- `κ_challenger`: Cohen's κ on `final_label`

---

## Label mapping to metric

| Final label | κ computation maps to |
|---|---|
| compliant | accept |
| non-compliant | reject |
| unclear | abstain |
