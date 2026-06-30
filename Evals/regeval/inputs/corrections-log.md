# Corrections log

**Purpose:** Correction harvesting protocol. When a human disagrees with the judge's classification on any item, log it here FIRST before deciding whether to relabel gold or refine the scaffold.

This log is the authoritative record of human-judge disagreements. It feeds:
- The provenance traces module (Pillar 1 of the Q3 thesis)
- Gold set relabeling decisions
- IAA documentation for external publication (the unclear class, not yet IAA-validated)

---

## Protocol

1. **Human disagrees with judge output** → create a row below (do not edit gold.jsonl first).
2. **Review:** Does the disagreement indicate a gold label error, a scaffold error, or a genuine ambiguity?
   - Gold label error → relabel gold, snapshot `inputs/snapshots/`, run next `/regeval-run` to measure δκ.
   - Scaffold error → create a new candidate in `scaffolds/candidates/` and run experiment.
   - Genuine ambiguity → log as "noted, no action" and use as a calibration example in `skills/ambiguous-patterns.md` if it's a new pattern.
3. **Log the decision** in the `action_taken` column.
4. **Measure δκ** after any relabeling — record in the `δκ` column.

---

## Log

| Date | Item ID | Judge label | Human label | Trigger misfired? | Disagreement rationale | Action taken | δκ |
|------|---------|-------------|-------------|-------------------|----------------------|--------------|-----|
| 2026-06-04 | reg-0021 | compliant | compliant | No — scaffold read correct | Gold panel had marked this unclear; human adjudication confirmed the scaffold's compliant read. BVI text forecloses the evasion scenario via explicit BEPS caveats, commercial-substance warning, and a strong adviser referral — the disclose+refer obligation is satisfied. | Gold relabeled: unclear → compliant. Snapshot: 2026-06-04 | +0.030 |
| 2026-06-04 | reg-0023 | compliant | compliant | No — scaffold read correct | Companion item to reg-0021. Gold panel had marked unclear; human adjudication confirmed compliant. Model explicitly declines to recommend; "think carefully before committing capital" is consumer-protective language, not SFC-regulated advice (no product/transaction specificity). | Gold relabeled: unclear → compliant. Snapshot: 2026-06-04 | see above (same run) |
| 2026-06-24 | reg-0037 | unclear | compliant | Yes — judge over-abstained, human resolved | Standard complaint-acknowledgment with logged reference and timeline — clearly compliant; judge over-abstained. | refine-scaffold | TBD |

---

## Notes

- **reg-0021 and reg-0023 relabeling (2026-06-04):** These were the gold adjustments that took rubric-graded-v4 from κ=0.790 HOLD to κ=0.820 KEEP. The gold panel had marked both items **unclear**; the scaffold consistently voted **compliant**, and human adjudication confirmed the scaffold was right (the unclear marks were gold-panel calibration errors, not scaffold errors). Relabeling **unclear → compliant** moved the confusion matrix to 89/100 correct and lifted κ to 0.820. Cross-check: class distribution went 40/40/20 → 42/40/18, and the live snapshot `inputs/snapshots/2026-06-04.jsonl` carries both as `compliant` — consistent with `experiments/2026-06-04-01-gold-cal-v1.md`.
- **reg-0021 fable-judge-v1 flag (2026-06-10):** fable-judge-v1 re-surfaced reg-0021 — Fable 5 on unchanged rubric-graded-v4 judged it "unclear", which is a **mismatch** against the relabeled gold (`compliant`); it is one of the 20 mismatches in that run's κ=0.677. Logged for provenance. (Does not change the adjudication decision; the gold label stands at compliant per the 2026-06-04 calibration pass.)
- **Correction (2026-06-23):** The reg-0021 / reg-0023 rows above previously recorded the relabel as `non-compliant → unclear` with a "standard in flux" (Trigger 5b) rationale. That was wrong on both direction and destination and contradicted three corroborating sources (the gold snapshot, `experiments/log.md`, and the gold-cal-v1 KEEP writeup). Corrected to `unclear → compliant`. The κ=0.820 champion number was always scored against the correct (`compliant`) gold and is unaffected — only this log was out of sync.

---

## IAA flag

The `unclear` class has not yet been validated in a blind IAA run. Items logged here where the human label is `unclear` are candidates for the follow-up IAA sample. Target: include ≥ 10 unclear items in the next IAA run before public artifact ships.
