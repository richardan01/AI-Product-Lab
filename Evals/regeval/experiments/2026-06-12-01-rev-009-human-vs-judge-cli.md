# Experiment 2026-06-12-01 — rev-009-human-vs-judge-cli

**Verdict:** SHIP (module experiment, not a scaffold κ-experiment — see note)
**κ:** n/a — this REV does not vary the scaffold; champion κ=0.820 (gold-cal-v1) unchanged
**Diagnostics:** recomputed κ reconciles to logged κ on every full-table run; demoed on fable-judge-v1 (N=100, 80 agree / 20 mismatch, κ=0.677) and refusal-tested on rubric-graded-v4 (N=13 partial table)
**Wall clock:** ~1:20 (build + run on artifacts; no judge calls, no API key)
**Gold snapshot:** `inputs/snapshots/2026-06-04.jsonl` (compliant=42, non-compliant=40, unclear=18; sha8 64d49383)

> **Note on verdict type:** REV-009 builds the human-vs-judge CLI *module* (RegEval
> Module 3), not a scaffold variant. It does not touch `current.md` and does not move κ.
> The gold panel's `gold_label` IS the human label, so "human vs judge" == exactly what
> Cohen's κ already measures; this module makes that comparison visible, item-by-item, and
> live, and self-audits by reconciling its recomputed κ against the logged κ. Logged here
> for lineage continuity alongside REV-008 (provenance.py).

## Hypothesis

The single most evals-literate visual for a Day-60 demo is *the metric assembling
itself as the reviewer judges*. If you stream an already-logged judge run as if the human is
labeling it now — recomputing Cohen's κ after each item — the abstraction "κ measures
human-vs-judge agreement" becomes a concrete screen visual. And if the recomputed κ MUST
reconcile to the logged κ, the harness checks itself on camera: a credibility signal, and a
real bug surfaced honestly if it ever fails to reconcile.

## Brainstorm — three framings (chosen + rejected)

- **A — blind side-by-side adjudication tool:** rejected as the spine. Most "interactive" and
  produces fresh human labels (which the unclear-class IAA flag wants), but a 5-min recorded
  demo would need a live human typing labels on camera — slow, error-prone, and the audience
  sees clicking, not rigor. Fresh labels also aren't reproducible from the log, breaking the
  no-API-key / deterministic contract. **Absorbed into C** as the optional, scriptable
  `adjudicate` subcommand (stdin-driven: `echo unclear | ... adjudicate ...`).
- **B — disagreement-review queue (mismatch cards + provenance):** rejected as the spine. This
  is ~80% what `provenance.py mismatches` + `card` already do — Module 3 would be a thin
  wrapper on Module 2, weak as a distinct third module. **Absorbed into C** as the `card`
  subcommand, which reuses the provenance loaders and adds the adjudication-outcome line.
- **C — κ-live session runner (CHOSEN):** replay a logged run as a live human-labeling session;
  recompute κ after each item; end with a confusion matrix + per-class κ that must reconcile to
  the logged κ (built-in self-audit). Adds a `--mismatches-only` fast path, a `card` adjudication
  view, a `summary` scoreboard, and the optional blind `adjudicate` moment from A.

One-line justification: C is the only framing that renders "the metric is the reviewer" as a
deterministic, no-API-key, self-auditing screen visual — and it absorbs the demo-worthy bits of
A and B without their on-camera-typing fragility.

## Scaffold delta vs champion

- None. Champion scaffold `rubric-graded-v4` (current.md) unchanged. No κ movement.

## What was built

- `Evals/regeval/judge_vs_human.py` — the module. Pure stdlib; imports loaders from
  `provenance.py` (`parse_raw_outputs`, `parse_experiment_header`, `load_gold_snapshot`,
  `resolve`); inline `cohen_kappa` verbatim from `metric.md` (no scipy). Subcommands:
  - `replay <exp> --gold-snapshot <snap> [--mismatches-only] [--no-anim]` — streams each item
    `reg-NNNN  human=<gold>  judge=<judge>  ✓/✗  κ_so_far=0.NNN`, recomputing κ live; footer
    has final κ, the `RECONCILES ✓/✗` self-audit vs logged κ, a confusion matrix, and per-class
    one-vs-rest κ (abstain class flagged).
  - `card <exp> <item-id> --gold-snapshot <snap>` — human-vs-judge adjudication card; renders
    the adjudication OUTCOME from `corrections-log.md` (relabel) or, for items only characterized
    in a selected-mismatch table, the scaffold-defect record cross-referenced from that table.
  - `summary <exp> --gold-snapshot <snap>` — one-screen scoreboard: N, agree/mismatch, κ
    (recomputed + logged + reconcile), TPR/TNR/abstention, per-class κ, corrections-log count.
  - `adjudicate <exp> <item-id> --gold-snapshot <snap>` — blind moment (Framing A): prints item
    text + masked judge verdict, reads ONE human label from stdin, reveals judge + gold, reports
    agree/disagree. Scriptable and headless; does NOT persist (prints a "log to corrections-log"
    hint instead).
- **Refusal guard:** a "selected mismatches" / prose table (col-4 not ✓/✗) is detected as
  `partial`; `replay`/`summary` print a PARTIAL-TABLE banner and exit 2 rather than quote a
  meaningless full-set κ. (Embarrassment scenario averted: silently computing κ≈0 over 13
  all-mismatch rows.)

## Result narrative

Ran on real logged data, no judge calls. On `fable-judge-v1` (N=100): the recomputed final
κ=0.677 reconciles to the logged κ=0.677 (Δ=0.0002, within the ±0.001 bar) — the self-audit
passes. The confusion matrix and per-class κ reproduce the logged diagnostics exactly:
compliant=0.834, non-compliant=0.720, unclear=0.299; `summary` reproduces TPR=0.857, TNR=0.950,
abstention=0.120. `--mismatches-only` prints the 20 ✗ rows and still reports the same final κ.
`card reg-0021` renders the corrections-log relabel outcome ("the human sat in judgment over the
judge and WON: 2026-06-04 judge=non-compliant → human=unclear, δκ +0.030"). `card reg-0088`
renders the scaffold-defect outcome (trigger-5a false-abstain), correctly sourced from the
rubric-graded-v4 mismatch table — NOT invented, since reg-0088 is not in corrections-log.
`replay`/`summary` on rubric-graded-v4 (N=13 selected mismatches) refuse the full-set κ and
print the partial-table banner. `adjudicate reg-0021` piped (`echo unclear |`) reveals headless:
your=unclear / judge=unclear (AGREE) / gold=compliant (DISAGREE).

## Why this verdict

SHIP as MVP for the Day-60 demo: runs on real artifacts with no API key, renders the
metric-as-reviewer visual deterministically, and self-audits (recomputed κ == logged κ). It
degrades honestly — refuses to quote κ on partial tables, sources the reg-0088 scaffold-defect
line from a real logged table rather than inventing it, and surfaces gold drift if the snapshot
disagrees with the table. Not production: `adjudicate` does not persist fresh labels (so it does
not yet feed the unclear-class IAA sample), and the strongest demo (κ climbing to 0.820 on the
KEEP champion) is still blocked because gold-cal-v1 has no per-item table — same flag REV-008
raised.

## Next experiment suggestion

Two open decisions carried from REV-008 / the corrections-log:
1. **Champion re-run (A/B):** (A) re-run rubric-graded-v4 over the 2026-06-04 snapshot to mint a
   verified-hash N=100 champion trace, so `replay` can show κ climbing to 0.820 on the KEEP run;
   or (B) demo Module 2/3 on fable-judge-v1, narrated as "any logged run." (A) is the stronger
   demo but costs a re-run 18 days from the gate.
2. **Unclear-class IAA:** the `unclear` class is not yet blind-IAA-validated (corrections-log
   flag, target ≥10 unclear items). A future enhancement: have `adjudicate` persist fresh labels
   to seed that IAA sample. Out of scope for this MVP; a publication risk a reviewer may probe.

## Raw outputs
<details>
<summary>replay footer — fable-judge-v1 (N=100)</summary>

```
────────────────────────────────────────────────────────────
  final: N=100  agree=80  mismatch=20
  RECONCILES ✓  recomputed κ=0.677 == logged κ=0.677  (Δ=0.0002)

  confusion matrix
    human↓ \ judge→      compliant non-compliant       unclear
    compliant                   36             2             4
    non-compliant                0            38             2
    unclear                      2            10             6

  per-class κ (one-vs-rest)
         compliant: 0.834
     non-compliant: 0.720
           unclear: 0.299  ← abstain class
```
</details>

<details>
<summary>card reg-0021 — corrections-log relabel outcome</summary>

```
│ ── adjudication outcome (corrections-log) ──
│   the human sat in judgment over the judge and WON:
│   2026-06-04  judge=non-compliant → human=unclear
│   trigger : Trigger 5b — standard in flux not recognised
│   action  : Gold relabeled: non-compliant → unclear. Snapshot: 2026-06-04  (δκ +0.030)
```
</details>

<details>
<summary>card reg-0088 — scaffold-defect outcome (cross-referenced)</summary>

```
│ ── adjudication outcome (mismatch-table review) ──
│   SCAFFOLD DEFECT (human-reviewed in 2026-05-30-01-rubric-graded-v4.md):
│   judge=unclear vs gold=non-compliant — judge=unclear: unverified PI private placement — trigger 5a fires
```
</details>

<details>
<summary>refusal guard — rubric-graded-v4 (N=13 partial table)</summary>

```
┌─ PARTIAL TABLE — κ NOT COMPUTABLE OVER FULL SET ───────────
│ detected   : col-4 carries prose (selected mismatches); N=13, 0 agree — not a full per-item stream
│ logged κ   : 0.79  (over the FULL gold set, N≈100)
│ ... refuses to quote it. (exit code 2)
└────────────────────────────────────────────────────────────
```
</details>

## Related

[[Evals/regeval/regeval-suite]] · [[Evals/regeval/experiments/log]] · [[Evals/regeval/judge_vs_human.py]] · [[Evals/regeval/provenance.py]] · [[Evals/regeval/inputs/corrections-log]] · [[Evals/regeval/metric]] · [[Projects/ralph/brief]]
