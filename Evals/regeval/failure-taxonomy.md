# RegEval failure-mode taxonomy

The named, counted catalogue of failure modes observed in the RegEval judge-alignment
loop. This is the first-class artifact the Shankar/Husain error-analysis method
requires (`shreyashankar/error-discovery-skill`; mirrored in `.claude/skills/evals/SKILL.md`
Step 0: open coding → axial coding → frequency → prioritization).

## Two honesty caveats (read first)

1. ~~**This is post-hoc axial coding, not a forward open-coding pass.**~~ **UPDATED 2026-06-28 —
   the forward pass has now been run.** See [[Evals/regeval/discovery-pass-2026-06-28]]: a forward
   open→axial coding pass over the *actual disagreement set* (read scenario text + rationale, not the
   log) was completed. It found the confusion structure was identical across tuning and "held-out" —
   which exposed **FM-11** (the held-out set was a duplicate of the tuning set) — and it drove the
   **binary collapse** decision after **FM-12** (the `unclear` class fails IAA). The taxonomy below
   is retained as the pre-collapse record; FM-11/FM-12 are the new top-priority entries.

2. **These are JUDGE failures, not primary-system failures.** RegEval does error analysis
   on the *LLM judge* (judge-vs-gold disagreement), which is a meta-eval. The methodology
   as taught analyzes where the *system under test* fails. Legitimate for a judge-alignment
   project — but a different activity, and the gap is named, not hidden.

**Frequency basis:** `items` = gold items affected where the log states a count;
`runs` = number of logged experiments in which the mode was observed.

## Taxonomy

### A. Abstention-calibration modes (scaffold)

| ID | Mode | Items | Runs | Status | Source |
|----|------|-------|------|--------|--------|
| **FM-1** | **Anti-hedge suppression** — anti-hedge policy emits zero `unclear` labels, so all genuinely-indeterminate items are forced into a binary class (0/10 unclear recovered). | 10 | 2 | RESOLVED — lifting the anti-hedge clause + enumerated triggers recovered unclear recall | `log.md` 2026-05-23-01 (baseline), 2026-05-29-01 (rubric-strict) |
| **FM-2** | **Unclear-class collapse** — overall κ looks healthy while per-class κ on `unclear` stays weak; the judge can't reliably distinguish genuine ambiguity. **The dominant residual mode.** | — | ≥5 | **OPEN** — champion still only unclear-κ=0.488 | `log.md` 2026-05-30-01 (0.488), 2026-06-10-01 (0.299), 2026-06-23-02 (0.359), 2026-06-24-01 (0.150), 2026-06-24-02 (0.316) |

### B. Trigger over-fire modes (scaffold)

| ID | Mode | Items | Runs | Status | Source |
|----|------|-------|------|--------|--------|
| **FM-3** | **Trigger-1 over-fire on educational-compliant** — abstention trigger 1 fires on educational content that is actually compliant. | 8 | 1 | RESOLVED in v4 (trigger-1 refined); note 2 of these were later found to be gold errors (FM-8) | `log.md` 2026-05-29-04 (rubric-graded-v2) |
| **FM-4** | **Trigger-5b over-fire on clear non-compliant / "standard in flux"** — fires on decidable non-compliant items; the v3 fix over-corrected and broke 12 more. | 4 (+12 on over-correction) | 2 | RESOLVED in v4 (standard-in-flux clarification) | `log.md` 2026-05-29-04, 2026-05-29-05 (v3) |
| **FM-5** | **Trigger-5a over-fire on policy/procedure descriptions** — Step-4 evidence-completeness check flags compliant policy descriptions (TPR 1.00→0.79). | 7 | 1 | PARTIAL — skills-v2 description-exclusion patch restored TPR→0.976, but skills-v2 is only HOLD | `log.md` 2026-06-08-01 (skills-v1), 2026-06-23-01 (skills-v2) |

### C. Architecture modes

| ID | Mode | Items | Runs | Status | Source |
|----|------|-------|------|--------|--------|
| **FM-6** | **Advisory-edge-case under-commit** — when the edge-case reference is advisory not mandatory, unclear items get committed to non-compliant at the final step. | 5 | 1 | Contributed to skills-v1 DISCARD | `log.md` 2026-06-08-01 |
| **FM-7** | **Adversarial-challenger over-refutation** — a "default refute:true" challenger flips already-correct verdicts (flip_degraded=24); κ crashed 0.770→0.380. | 24 | 1 | DISCARDED architecture; revealed model-upgrade is higher-leverage | `log.md` 2026-06-08-02 (challenger-v1) |

### D. Gold-data modes

| ID | Mode | Items | Runs | Status | Source |
|----|------|-------|------|--------|--------|
| **FM-8** | **Gold-panel calibration error** — the gold panel marked items `unclear` that human adjudication confirmed were `compliant`; the scaffold was right and the gold was wrong. | 2 | 1 | RESOLVED — relabeled unclear→compliant, +0.030 κ (0.790→0.820 KEEP) | `inputs/corrections-log.md` reg-0021, reg-0023 (2026-06-04); `log.md` 2026-06-04-01 |

### E. Portability / instrument modes (meta — measurement validity)

| ID | Mode | Items | Runs | Status | Source |
|----|------|-------|------|--------|--------|
| **FM-9** | **Model-specific hedging non-portability** — anti-hedge triggers tuned against Sonnet-4-5's hedging bias don't transfer; on other models the unclear class collapses. | — | 2 | **OPEN** — scaffold is Sonnet-4-5-specific, not model-portable | `log.md` 2026-06-10-01 (Fable, κ=0.677), 2026-06-23-02 (Opus, κ=0.768) |
| **FM-10** | **Harness instrument variance** — the eval harness (single-API-call/item vs. batched-subagent) shifts κ by ~0.25, **larger than the gap between the scaffolds under comparison**. | — | 1 | **OPEN** — hold harness fixed when comparing; live champion replay needs an API run | `log.md` 2026-06-24-01 (champion 0.820 API → 0.570 subagent) |

### F. Integrity / gold-validity modes (found by the 2026-06-28 forward pass)

| ID | Mode | Items | Status | Source |
|----|------|-------|--------|--------|
| **FM-11** | **Phantom held-out** — `gold_expansion.jsonl` (70) is an exact id+text+label subset of the tuning set `gold.jsonl` (reg-0031..0100). Every "held-out / anti-overfit / KEEP-confirmed" claim before 2026-06-28 was in-sample and void. | 70 | **RESOLVED** — real held-out `heldout_v2.jsonl` (36, 20 new regimes) built; old file deprecated | `discovery-pass-2026-06-28`; verified id-overlap 70/70 |
| **FM-12** | **`unclear` class fails IAA** — blind second annotator agreed compliant 13/13, non-compliant 13/13, **unclear 2/18** → IAA κ=0.48 (< 0.60). The class the judge was optimised against is unreliable gold. Reframes FM-2 from a judge defect to a gold-label defect. | 18 | **RESOLVED (design)** — collapsed to binary judge; `unclear` quarantined pending human re-adjudication | `discovery-pass-2026-06-28`; 56-item mixed IAA |

> **Post-collapse result:** binary judge (forced-commit, shuffled) scores **κ=1.000 in-sample (82)**
> and **κ=1.000 on the genuine net-new held-out (36)** — first valid generalization evidence.
> Caveat: both sets are clean-construct; borderline + production testing is the next gap.

## Prioritization (what to attack next)

Ranked by severity × persistence, not δκ (**re-ranked 2026-06-28 post-collapse**):

1. **Borderline + production validity** — the binary judge is κ=1.000 on clean-construct items;
   the boundary and real-world distribution are untested. Author hard binary items + stand up CD
   (`cd-monitoring-design.md`). This is now the real frontier.
2. **Human re-adjudication (FM-12 follow-through)** — replace model-as-annotator with a real second
   human on the 18 quarantined + the 36 held-out (`human-annotation-protocol.md`). Until then the
   κ=1.000 carries a model-annotator caveat.
3. ~~FM-2 (unclear-class collapse)~~ — **dissolved by the binary collapse**; was substantially a
   gold-label defect (FM-12), not a judge defect.
4. **FM-10 + FM-9 (instrument + model variance)** — still live: pin model+harness on every cited κ.

## Relationship to the review queue

`review-queue.md` now surfaces **two** slices after every run (`score.py`):

- **Abstains** → feed FM-1 / FM-2 (the hedging modes).
- **⚠ Confident mismatches** (judge committed and was wrong; `FALSE-CLEAR` = cleared an
  actual violation) → feed FM-3 / FM-4 / FM-5 / FM-9 and any new confident-wrong modes.
  Before this slice existed the loop was **blind to confident-and-wrong verdicts** — the
  catastrophic class for a compliance judge. New confident-mismatch patterns discovered via
  the queue should be added here as new FM-rows.

## Related

[[Evals/regeval/methodology-comparison]] · [[Evals/regeval/experiments/log]] · [[Evals/regeval/inputs/corrections-log]] · [[Evals/regeval/review-queue]] · [[Evals/regeval/metric]] · [[Evals/severity-taxonomy]] · [[.claude/skills/evals/SKILL]]
