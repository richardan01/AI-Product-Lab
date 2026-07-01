# Metric — memory-consolidation eval

How we measure whether the daily consolidation routine stays **near ground truth** (faithful) and **loses no context** (complete). Follows the applied-eval method of Hamel Husain & Shreya Shankar: look at data first, binary failure modes, bespoke (not generic) metrics, validate the judge. Reference: <https://hamel.dev/blog/posts/evals-faq/>

## Order of operations (metrics come LAST)
1. **Error analysis first.** Read the routine's real outputs — ≥100 traces to start, 10–20/week ongoing (Hamel's heuristic). Open-code what went wrong; cluster into failure modes. The two modes below are the *current hypothesis* — let data reshape them (Shreya's "criteria drift").
2. Define each failure mode as a **binary** question (Hamel: binary > Likert) with an **explicit positive class**.
3. **Code-assert** what's deterministic; LLM-judge only the fuzzy parts.
4. **Validate the judge** against your own labels (TPR/TNR) before trusting its numbers.
5. *Only then* report the rates below, with confidence intervals.

## The unit and the positive class (define before measuring)
You don't define TP/TN/FP/FN directly — they fall out once you fix the unit, the positive class, and the match rule.

- **Unit:** one *claim* — a single fact written to (or that should be in) memory for the window.
- **Positive class (PRODUCT matrix):** "a claim that belongs in memory" = durable **and** true **and** traceable to a source in the window.

| Cell | Meaning in the OS                                   | Example                                                             |
| ---- | --------------------------------------------------- | ------------------------------------------------------------------- |
| TP   | wrote a claim that belongs                          | "the vendor decision was deferred pending a resource sign-off" — a session said so |
| FP   | wrote a claim that doesn't belong (**fabrication**) | "the data source was confirmed single-tenant" — no source said it   |
| FN   | failed to write a claim that belongs (**drop**)     | a session settled a definition; routine never wrote it              |
| TN   | correctly didn't write a non-claim                  | skipped chit-chat — **unbounded; this is why accuracy is excluded** |

## Metrics (the product output)
- **Precision = TP / (TP + FP)** — faithfulness / trust. Target **≥ 0.98**. Fabrication is the cardinal sin → near-zero tolerance. Measured **exactly**: the routine writes a small set, so audit every written claim against the window.
- **Recall = TP / (TP + FN)** — completeness / anti-context-rot. Target **≥ 0.85**. Measured by **sampling**: draw 10–15 high-signal items from the window's sources, check how many reached memory. (Enumerating "everything that should have been written" is too costly; sample instead.)
- **F1 = 2·P·R / (P + R)** — single headline only. Keep watching P and R **separately**: the costs are asymmetric — a *wrong* memory is worse than a *missing* one (the missing fact still lives in the transcript and is recoverable).
- **Cadence:** weekly — aggregate ~5–7 daily runs to reach N ≥ 30 claims for a stable number.

## Accuracy — explicitly EXCLUDED
Not used anywhere in this suite. Three reasons:
1. **No meaningful true-negative set.** The "correctly-not-written" class is unbounded, so accuracy is undefined or swamped — it reads ≈0.997 even while the routine fabricates and drops facts. Class-imbalance trap.
2. **Generic aggregate → false confidence** (Hamel: generic metrics "measure abstract qualities that may not matter… create false confidence"). It hides *which* failure is occurring.
3. **Collapses two errors** that have different costs and different fixes (fabrication → tighten faithfulness; drop → broaden extraction).

Do **not** re-add accuracy by reflex. It is the right tool only for **balanced, fixed-set, symmetric-cost** classification — which this is not.

## Validating the judge (the only place classification metrics belong)
The LLM judge that scores faithfulness can itself be wrong. Before trusting its precision/recall:
- Hand-label a sample, then measure the **judge's TPR and TNR** against your labels on a held-out set (Hamel: "achieve high True Positive Rate (TPR) and True Negative Rate (TNR)… on a held out labeled test set").
- **Use TPR/TNR, not accuracy, even here.** The failure class is rare: if ~5% of claims are fabrications, a judge that always says "faithful" scores 95% accuracy but TPR = 0% (catches nothing). TPR/TNR expose that; accuracy hides it.
- Judge positive class = "the failure is present" (distinct from the product positive class above — don't conflate the two matrices).

## Deterministic checks (no judge)
Criterion 05 (freshness + completeness) is pure code — assert, don't grade:
- `Last consolidated:` advanced to the run date.
- Every in-range `*.jsonl` transcript was opened.
- `daily-learnings.md` received an entry (or an explicit "nothing durable").

## Confidence intervals (sound stats; NOT from the Hamel FAQ)
Weekly N is small → report a 95% CI (e.g. Wilson interval) on precision/recall. Precision 0.93 at N=30 ≈ ±0.09. Track the **trend across weeks**, don't over-read a single point. Flagged as an add-on so a future reader doesn't attribute it to the FAQ.

## Status
**Provisional-measured** (as of 2026-06-20). The first gold fixture makes the product metric computable: first run scored **Precision 100% (23/23), Recall 95.2% (20/21), F1 97.5% — PASS**. Both point estimates beat target, but with N≈23 the Wilson CIs are wide (precision [85.7%, 100%], recall [77.3%, 99.2%]) — **one fixture is a baseline, not a validated suite.** *(Fixture data — real session transcripts + gold labels — is kept in the private working copy and not shipped in this public repo.)*

Still outstanding before this is a *validated* metric:
1. **Gold verification** — the fixture's gold set is DRAFT (model-authored from primary sources); a human must confirm it. Until then the numbers are provisional-measured, not measured.
2. **More fixtures** — add `normal-day`, `conflicting-facts`, `empty-day` to tighten the CIs (per `inputs/README.md`).
3. **Judge validation** — no LLM judge has been validated on TPR/TNR yet; the 2026-06-20 run was human/agent-graded. Do not wire an automated weekly metric before a judge is validated on labeled data.

The inline Step-6 self-check remains the live daily guard between offline runs.

## Related
[[Evals/memory-consolidation/memory-consolidation-suite]] · [[Evals/memory-consolidation/protocol]] · [[Evals/regeval/metric]] · [[Evals/eval-audit-checklist]] · [[Evals/index]] · Hamel's evals FAQ: <https://hamel.dev/blog/posts/evals-faq/>
