# RegEval human-annotation protocol

**Why:** every IAA run to date used the author (RC) + a model as the "second annotator." That is a
known shortcut — models tend to agree with the framing of whoever authored the items, inflating
agreement. The 2026-06-28 re-IAA already showed the limit: it covered the `unclear` class for the
first time and agreement collapsed (κ=0.48, 2/18). This protocol closes the loop with a **real
second human**. Per Husain/Shankar Lesson 3 workflow.

## Scope (priority order)
1. **Re-adjudicate the 18 `quarantined-unclear` items** (now `split: quarantined-unclear` in
   `gold.jsonl`). Decide per item: is it genuinely binary (relabel compliant/non-compliant and
   promote to dev) or genuinely indeterminate (keep out of the binary gold)?
2. **Validate `heldout_v2.jsonl`** (36 authored test items) — confirm a second human agrees with the
   binary labels before the κ=1.000 result is cited externally.
3. **Author borderline binary items** — the current sets are clean-construct; the boundary is
   untested. Target ≥20 genuinely contestable compliant-vs-non-compliant cases.

## Workflow (per Lesson 3)
1. **Recruit** 1 second annotator with HK financial-compliance domain knowledge (compliance/legal
   colleague; Enhu or a RevOps/compliance contact).
2. **Independent annotation** — both label the shared set with NO discussion (this surfaces rubric
   ambiguity, not just label noise). Use the label-stripped files in `inputs/`.
3. **Measure IAA** — Cohen's κ. Floor = **0.60** before any item enters gold.
4. **Alignment session** — discuss disagreements to refine the *rubric wording*, not just flip
   labels. Re-label, re-measure, iterate until κ ≥ 0.60.
5. **Finalise** — documented rubric + consensus labels; snapshot `gold.jsonl` first (lineage).

## Annotation guidance (binary)
- **compliant** — identifiable obligation, text explicitly satisfies it, no material gap.
- **non-compliant** — identifiable obligation, text clearly violates/omits/misstates it (severity
  may be uncertain).
- Self-disclosed past breaches: label on the **underlying conduct** (a good disclosure of a real
  breach is still evidence of non-compliance) — this was a live disagreement axis in the re-IAA;
  pin it in the alignment session.

## Outputs
- `inputs/iaa/<date>-human-iaa.jsonl` (second-human labels) + κ in `experiments/log.md`.
- Updated `gold.jsonl` (promoted/relabelled items) with a fresh snapshot.
- Alignment-session notes appended here.

## Related
[[Evals/regeval/discovery-pass-2026-06-28]] · [[Evals/regeval/inputs/regeval-gold-dataset]] · [[Evals/regeval/metric]] · [[Evals/regeval/failure-taxonomy]]
