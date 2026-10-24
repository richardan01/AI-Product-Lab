# RegEval case study

RegEval tests agreement between an LLM compliance classifier and human labels using Cohen's
κ. It is retained because its experiment history shows both improvement and measurement
failure.

## Start with the integrity correction

Read [`discovery-pass-2026-06-28.md`](discovery-pass-2026-06-28.md). It documents two defects:
the supposed held-out set duplicated tuning data, and the `unclear` class failed agreement
testing. Earlier held-out claims were invalidated instead of being silently replaced.

## Run the public scorer demo

The demo data is synthetic and proves only that the scorer and diagnostics work:

```bash
python3 evals/regeval/score.py \
  --slug binary-v1 \
  --pred evals/regeval/demo/predictions.jsonl \
  --gold evals/regeval/demo/gold.jsonl \
  --binary --dry-run
```

The historical private 36-item held-out set is intentionally excluded from the repository.
Its reported result is not independently reproducible from the public clone.

## What to inspect

- [`metric.md`](metric.md) — metric definition and caveats.
- [`experiments/log.md`](experiments/log.md) — append-only experiment history.
- [`failure-taxonomy.md`](failure-taxonomy.md) — named failure modes.
- [`research-goal.md`](research-goal.md) — historical research-program design.

The unattended autoresearch driver is not shipped. Related documents are design lineage, not
a claim that the public clone can run an autonomous overnight loop.

## Reading the experiment files

The experiment, scaffold, and discovery files are historical records and are deliberately
left unedited, in line with the append-only rule. Their `[[wikilinks]]` and file paths point
into the earlier OS-era tree (preserved at the tag `ai-product-lab-os-v1`) or at working files
and private inputs that are not published, so many will not resolve from this clone. That is a
property of the record, not a broken link to repair.
