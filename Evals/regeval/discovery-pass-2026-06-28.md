# RegEval forward discovery pass — 2026-06-28

**What this is:** the forward open-coding → axial-coding pass that `failure-taxonomy.md` and
`methodology-comparison.md` had named as *the one deferred gap* (Shreya/Husain "unknown-engine").
Triggered by an audit of RegEval against the Husain/Shankar AI-Evals course. It is the first
pass that read the *errors themselves* rather than reverse-extracting modes from the experiment log.

It surfaced two **integrity defects** that invalidate prior claims, and produced one **decision**
(collapse to binary) that is now empirically validated on a genuine held-out set.

---

## TL;DR

- 🔴 **The "held-out" set was not held out.** `gold_expansion.jsonl` (70) is an exact id+text+label
  subset of the tuning set `gold.jsonl` (reg-0031..reg-0100). The κ=0.661 "held-out confirm" was
  **in-sample**. There was **no valid out-of-sample measurement** in the project until today.
- 🔴 **The `unclear` class fails inter-annotator agreement.** A fresh blind expert annotator agreed
  on **compliant 13/13, non-compliant 13/13, but unclear only 2/18** → IAA κ=0.480, below the 0.60
  floor. Two experts do not agree the "unclear" items are unclear. The class the judge has been
  optimised against is **unreliable gold**, not just hard.
- ✅ **Decision: collapse to a binary judge** (drop `unclear`). Validated: binary judge scores
  **κ=1.000 in-sample (82)** and **κ=1.000 on a genuine net-new held-out (36 items, 20 regulatory
  regimes never tuned on)** — the first valid generalization evidence the project has ever had.
- ⚠️ **Honesty caveat on the 1.000:** both gold sets are author-constructed to have clear labels.
  κ=1.000 means "perfect on clear-cut cases," not "perfect in production." The next gap is
  **borderline/hard binary items** and **real production traces** (see CD design doc).

---

## Method (Shreya open → axial coding)

1. **Open coding.** Pulled every judge-vs-gold disagreement on the most-recent reproducible
   (subagent) runs — 27 on the tuning set, 15 on the (then-believed) held-out — and read the
   *full scenario text + gold rationale* for each, writing descriptive notes on why each error
   occurred. No pre-set categories.
2. **Axial coding.** Clustered the open codes into the confusion structure below.
3. **Saturation check.** Tuning and "held-out" produced the *same* confusion structure — which
   was itself the clue that led to the duplicate-set discovery.

### Axial clusters (judge error modes, pre-collapse)

| Cluster | Pattern (gold → pred) | Tuning | "Held-out" | Reading |
|---|---|---|---|---|
| **C1 Over-abstention on accurate complex disclosure** | compliant → unclear | 10 | 9 | Triggers 2/5a fire on dense-but-correct regulatory-process text (licence renewal, liquid-capital, complaint policy). The judge reads complexity as indeterminacy. |
| **C2 Ambiguity-as-violation** | unclear → non-compliant | 9 | 4 | The judge collapses genuine ambiguity toward "violation" when any risk signal is present. |
| **C3 Under-flagging ambiguity** | unclear → compliant | 4 | 1 | Opposite of C2 on softer items. |
| **C4 Missed violation via abstention** | non-compliant → unclear | 1 | 1 | The safety-critical false-abstain (a real violation hedged). |

**Key axial insight:** C1–C3 all live on the `unclear` boundary. The binary classes barely err.
The disagreement is not about *compliance judgement* — it is about *whether a third category
exists at all*. That pointed straight at the gold standard, not the judge.

---

## Integrity finding 1 — the held-out set is a duplicate

```
dev   gold.jsonl            reg-0001..reg-0100  (N=100)
test  gold_expansion.jsonl  reg-0031..reg-0100  (N=70)   ⊂ dev, identical text+labels (70/70)
```

`gold_expansion.jsonl` was treated everywhere (`research-goal.md`, `run-log.md`, `index.md`) as a
"never-tuned 70-item held-out validation set." It is not. It is the tail slice of the tuning set.

**Consequence:** every "held-out" / "anti-overfit" / "KEEP-confirmed" claim prior to today is
void. The κ=0.661 was in-sample. The project had **zero** generalization evidence. This is the
single most important correction in the RegEval record.

**Status:** `gold_expansion.jsonl` deprecated (see header note in that file); replaced by the
genuine `heldout_v2.jsonl`.

## Integrity finding 2 — `unclear` fails IAA

The original IAA (κ=1.000, 20 items) **excluded the unclear class** — its own documented
limitation. A 56-item mixed re-run *with unclear included* (28 unclear + 14/14 binary), labelled by
a blind independent expert annotator:

| Gold class | Independent annotator agreed | 
|---|---|
| compliant | 13/13 |
| non-compliant | 13/13 |
| **unclear** | **2/18** |

Overall κ = **0.480** (< 0.60 floor). The annotator reclassified 16/18 "unclear" items into
compliant (6) or non-compliant (10). **You cannot align a judge to labels two humans don't share.**
FM-2 ("unclear-class collapse"), chased across 5 experiments as a *judge* defect, is substantially
a *gold-label* defect.

> Honesty caveat: the second annotator is a model (Sonnet), not a human — same limitation the
> original IAA had. But the *direction* is unambiguous and large (2/18), and it covers the class
> the original IAA skipped. A human re-annotation is queued (`human-annotation-protocol.md`).

---

## Decision — collapse to binary

**Problem → Decision → Tradeoff → Outcome → Risk**

- **Problem.** The three-class design carries an unreliable class (`unclear`, IAA κ=0.48) that
  drives the headline κ down and has no valid held-out to test against.
- **Decision.** Drop `unclear`. Judge `compliant` vs `non-compliant` only (both IAA-perfect).
- **Tradeoff.** Loses the abstention / "know-when-to-defer" capability that was a design goal.
  Mitigation: re-introduce abstention later as a *calibrated confidence flag* measured separately,
  not as a gold class (see `metric.md` → "abstention as confidence").
- **Outcome.** Binary judge, forced-commit, shuffled to kill ordering cues:
  - In-sample (82): **κ=1.000**, TPR 42/42, TNR 40/40.
  - Genuine net-new held-out (36, 20 new regimes): **κ=1.000**, TPR 18/18, TNR 18/18.
  - Note: the fresh binary run beat the old 3-class run *even on the binary items* (old run made
    3 binary errors + 11 abstentions). The broken `unclear` triggers were degrading binary
    decisions too.
- **Risk.** κ=1.000 is *clean by construction* — authored items have unambiguous labels. Real
  production text contains borderline cases this set does not. **Do not present 1.000 as a
  production number.** Next: hard/borderline binary items + production traces.

---

## The genuine held-out (`heldout_v2.jsonl`)

36 net-new binary items (18/18) built by Shreya **dimension sampling** (regime × doc-type ×
status × difficulty), covering 20 regulatory surfaces the original 82 never touched: AMLO/CDD,
margin financing, Professional-Investor opt-in, SFC VATP (virtual assets), short-position
reporting, client-money segregation, research-analyst independence, ILAS cooling-off, best
execution, monetary-benefit disclosure, PDPO breach/marketing, market sounding, marking-the-close
(MMO), record-keeping, outsourcing, SFO Part XV disclosure-of-interests, MPF intermediary,
unsolicited calls. This file is the project's first real test set and doubles as the long-missing
**discovery/synthetic-data front-end**.

---

## What this changes for the demo

The recorded demo's "honest overfit (0.820→0.661)" framing rests on the invalid duplicate set —
**0.661 was in-sample, not overfit evidence.** The stronger, true story is:

> "I audited my own eval against the Husain/Shankar method and found two integrity defects: my
> held-out set was a duplicate of my training set, and my hardest class failed inter-annotator
> agreement. I collapsed to the validated binary task and built a genuine net-new held-out across
> 20 regulatory regimes — the binary judge generalises at κ=1.000 on clear-cut cases, and I've
> scoped borderline + production testing as the next gap."

That is a *catching-your-own-broken-eval* story — a rarer and stronger signal than a high κ.

---

## Related

[[Evals/regeval/failure-taxonomy]] · [[Evals/regeval/methodology-comparison]] · [[Evals/regeval/metric]] · [[Evals/regeval/research-goal]] · [[Evals/regeval/human-annotation-protocol]] · [[Evals/regeval/cd-monitoring-design]] · [[Evals/regeval/results]] · [[Evals/run-log]]
