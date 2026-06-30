# RegEval provenance traces (REV-008)

Auditable provenance records for judge verdicts. One JSONL file per experiment,
named `<experiment-stem>.jsonl`, one record per gold item.

Traces are **reconstructed from on-disk artifacts** by [`../provenance.py`](../provenance.py)
— they are *not* emitted live by the judge runner. The reconstruction joins three
artifacts that already exist after any experiment: the experiment file's
`## Raw outputs` table (the verdicts), the gold snapshot for that run (gold label +
rationale), and the scaffold under test (content-hashed for reproducibility). This
means traces rebuild offline, with **no API key** — the binding constraint in the
build environment.

## Build / inspect

```bash
# build the JSONL sidecar for an experiment
python3 provenance.py build experiments/<exp>.md --gold-snapshot inputs/snapshots/<snap>.jsonl
# human-readable trace card for one item
python3 provenance.py card experiments/<exp>.md <item-id> --gold-snapshot inputs/snapshots/<snap>.jsonl
# audit short-list — mismatches only
python3 provenance.py mismatches experiments/<exp>.md --gold-snapshot inputs/snapshots/<snap>.jsonl
```

## Record schema

| Field | Meaning |
|---|---|
| `trace_id` | `<experiment-id>::<item-id>` |
| `item_id` | gold item id |
| `judge_label` / `judge_rationale` | the verdict and the judge's stated reason |
| `gold_label` / `gold_rationale` | the gold panel's label and rationale (incl. RELABELED notes) |
| `agreement` | bool — `judge_label == gold_label` |
| `abstention_trigger` / `trigger_confidence` | which abstain trigger fired (or null) and its confidence |
| `experiment_id` / `experiment_file` | source experiment |
| `scaffold_slug` / `scaffold_file` / `scaffold_sha8` / `scaffold_hash_verified` | scaffold under test, content hash, and whether the on-disk file still matches that hash |
| `gold_snapshot_file` / `gold_snapshot_sha8` | gold snapshot used + its hash |
| `verdict_of_run` / `kappa_of_run` | the run's KEEP/HOLD/DISCARD verdict and logged κ |
| `input_excerpt` | leading text of the item (provenance, not full input) |
| `built_at` / `built_by` / `reconstructed` | build stamp; `reconstructed: true` flags artifact-rebuild provenance |

## Discipline

Output-only. Traces are never read back into a scaffold or the κ computation — that
would be re-grading. They exist to make a verdict auditable ("given this label, what
produced it, against what gold, under which scaffold"), which is the regulated-fintech
differentiator. The human-vs-judge CLI ([`../judge_vs_human.py`](../judge_vs_human.py),
REV-009) consumes these records.
