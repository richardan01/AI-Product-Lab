# Experiment 2026-06-11-01 — rev-008-provenance-traces

**Verdict:** SHIP (module experiment, not a scaffold κ-experiment — see note)
**κ:** n/a — this REV does not vary the scaffold; champion κ=0.820 (gold-cal-v1) unchanged
**Diagnostics:** module reconstructs traces for any logged run; demoed on fable-judge-v1 (N=100, 80 agree / 20 mismatch) and rubric-graded-v4 (N=13 partial table)
**Wall clock:** ~1:30 (build + run on artifacts; no judge calls)
**Gold snapshot:** `inputs/snapshots/2026-06-04.jsonl` (compliant=42, non-compliant=40, unclear=18; sha8 64d49383)

> **Note on verdict type:** REV-008 builds the provenance-traces *module*, not a scaffold
> variant. It does not touch `current.md` and does not move κ. The "metric is the reviewer"
> contract still holds for scaffold experiments; this is harness infrastructure that the
> Day-60 demo and the corrections-log both depend on. Logged here for lineage continuity.

## Hypothesis

A verdict is only credible if it is *reconstructable*. The Day-60 gate requires "the variant
is reproducible from the log" — but the log proves reproducibility at the *run* level (one κ
per experiment), not the *verdict* level. Building a per-verdict provenance record (judge label
+ gold label + scaffold hash + snapshot hash + run id, joined from artifacts already on disk)
makes any single verdict auditable, and surfaces the reg-0088-class defect as a visible
mismatch rather than a number buried in a confusion matrix.

## Brainstorm — three framings (chosen + rejected)

- **A — citation chains (verdict → source regulation text):** rejected. Requires changing the
  judge contract to emit citations and a citable SFC corpus the suite doesn't have; re-running
  the KEEP experiment 19 days from the gate is unjustified risk. v2 feature.
- **B — rubric-step decision traces (which trigger fired, in what order):** rejected as the sole
  framing. The live judge emits only `label + rationale`, no structured step path; reconstructing
  it post-hoc from prose is lossy. **Folded into C** as a best-effort `abstention_trigger` field,
  parsed from the rationale and explicitly marked `confidence=low`.
- **C — run-lineage / reproducibility envelope (CHOSEN):** one trace record per verdict joining
  judge output ⋈ gold snapshot ⋈ content-hashed scaffold. Ships without changing the judge
  contract or re-running the KEEP experiment; directly satisfies the gate's reproducibility bar;
  runs with no API key (reconstructs from artifacts). Absorbs B's trigger attribution and, for
  free, A's better half — gold *relabeling history* flows through from the snapshot's
  `gold_rationale` field (e.g. reg-0021's "RELABELED 2026-06-04" note).

One-line justification: C is the only framing that is demo-ready inside the window without
touching the judge contract, and it cleanly absorbs the demo-worthy parts of A and B.

## Scaffold delta vs champion

- None. Champion scaffold `rubric-graded-v4` (current.md) unchanged. No κ movement.

## What was built

- `Evals/regeval/provenance.py` — the module. Three subcommands:
  - `build <experiment> --gold-snapshot <snap> [--scaffold <s>]` → writes `traces/<exp-stem>.jsonl`,
    one provenance record per verdict.
  - `card <experiment> <item-id> --gold-snapshot <snap>` → human-readable trace card for one item.
  - `mismatches <experiment> --gold-snapshot <snap>` → the audit short-list (disagreements only).
- `Evals/regeval/traces/` — output dir; `2026-06-10-01-fable-judge-v1.jsonl` (100 records) and
  `2026-05-30-01-rubric-graded-v4.jsonl` (13 records) generated as demo fixtures.

Trace record fields: `trace_id · item_id · judge_label · judge_rationale · gold_label ·
gold_rationale · agreement · abstention_trigger · trigger_confidence · experiment_id ·
scaffold_slug · scaffold_file · scaffold_sha8 · scaffold_hash_verified · gold_snapshot_file ·
gold_snapshot_sha8 · verdict_of_run · kappa_of_run · input_excerpt · built_at · reconstructed`.

## Result narrative

Ran on real logged data, no judge calls. On `fable-judge-v1`: 100 traces, 80 agree / 20 mismatch,
matching the logged κ=0.677 run. The reg-0088 trace renders as a clean MISMATCH card
(judge=unclear, gold=non-compliant) — the false-abstain defect is now a one-line audit artifact,
not a buried confusion-matrix cell. An integrity check was added after a real bug surfaced: when
the `--scaffold` passed doesn't match the run's scaffold slug, the `scaffold_sha8` is NOT
provenance for that run, so the card and build summary now flag it `⚠ UNVERIFIED` rather than
imply a false hash match. Verified path (rubric-graded-v4 run ⋈ its own candidate scaffold) shows
`[verified]`. Gold relabeling history (reg-0021's "RELABELED 2026-06-04") flows through from the
snapshot for free — input-lineage without extra plumbing.

## Why this verdict

SHIP as MVP: runs on real artifacts with no API key, satisfies the per-verdict reproducibility
the Day-60 gate implies, and degrades honestly (marks low-confidence trigger attribution and
unverified hashes rather than overclaiming). Not production: trigger attribution is prose-parsed,
and trace fidelity is capped by what the source experiment table logged (the KEEP run gold-cal-v1
has no per-item table at all — see risks).

## Next experiment suggestion

The cleanest demo run (the KEEP champion, gold-cal-v1) has **no `## Raw outputs` table** — it was
an analytical re-score. Before the demo, either (a) re-run rubric-graded-v4 over the 2026-06-04
snapshot to regenerate a full N=100 per-item table for the champion, or (b) demo on fable-judge-v1
and narrate it as "any logged run." Option (a) gives a verified-hash, κ=0.820 trace set — the
stronger demo. Separately: the reg-0088 trigger-5a patch (logged in gold-cal-v1) would let a
future trace attribute the defect to a named trigger instead of `unattributed`.

## Raw outputs
<details>
<summary>Provenance build — fable-judge-v1 (N=100)</summary>

```
Built 100 traces → traces/2026-06-10-01-fable-judge-v1.jsonl
  agree=80  mismatch=20  (run κ=0.677)
  scaffold fable-judge-v1 @ 1ab40859 [⚠ UNVERIFIED (passed file slug ≠ run slug)]  snapshot @ 64d49383
```

reg-0088 trace card:
```
┌─ provenance trace ─────────────────────────────────────────
│ trace_id   : 2026-06-10-01::reg-0088
│ verdict    : judge=unclear  gold=non-compliant  → MISMATCH
│ attributed : unattributed (confidence=low; parsed from rationale)
│ judge says : (no rationale in source table)
│ gold says  : Offering unaudited, unverified private placement instruments without adequate
│              issuer risk disclosure likely constitutes an unauthorised CIS offer ...
│ reproducibility envelope
│   scaffold      : fable-judge-v1  (current.md @ 1ab40859)  ⚠ hash NOT verified against run slug
│   gold snapshot : 2026-06-04.jsonl @ 64d49383
│   run           : 2026-06-10-01  verdict=DISCARD  κ=0.677
│   built         : reconstructed from artifacts, no live judge call
└────────────────────────────────────────────────────────────
```
</details>

## Related

[[Evals/regeval/regeval-suite]] · [[Evals/regeval/experiments/log]] · [[Evals/regeval/provenance.py]] · [[Evals/regeval/inputs/corrections-log]] · [[Evals/regeval/inputs/snapshots/2026-06-04.jsonl]] · [[Projects/ralph/brief]]
