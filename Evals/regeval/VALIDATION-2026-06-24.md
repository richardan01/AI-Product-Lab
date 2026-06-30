# RegEval — offline harness validation

> ⚠️ **SUPERSEDED 2026-06-28.** This validation predates the forward discovery pass, which found the
> "held-out" set was a duplicate of the tuning set (FM-11) and the `unclear` class fails IAA
> (FM-12). Any κ=0.820 / held-out claim here is void; the task is now binary. Current state:
> [[Evals/regeval/discovery-pass-2026-06-28]]. Retained for lineage.

**Run:** 2026-06-24 · **Operator:** Claude (offline, no API spend) · **Gate:** Day-60 2026-06-30 (6 days out)
**Scope:** Phase A of the approved plan — validate the demo harness end-to-end against existing on-disk artifacts. No judge calls, no `run_experiment.py`, no metered API.
**Environment:** Python 3.14.3 · `anthropic` SDK not exercised (offline)

---

## Verdict: 🟢 GO — harness is demo-ready, run sheet recording-ready

The harness runs clean and **reconciles κ to the logged value within Δ=0.0002** on the full-trace run. The partial-table guard refuses correctly. Both originally-flagged DEMO.md items are now closed (see Flags below) — the run sheet matches what prints on camera. No blockers to recording remain on the harness side.

---

## Results — per command

| # | Command | Result | Notes |
|---|---------|--------|-------|
| PF1 | `python3 --version` | ✅ | 3.14.3 |
| PF2 | `ls inputs/snapshots/2026-06-04.jsonl` | ✅ | present, 82 KB |
| PF3 | `ls provenance.py judge_vs_human.py run_experiment.py` | ✅ | all present (`judge_vs_human.py` modified 06-24 10:06) |
| PF4 | `provenance.py build … fable-judge-v1` (→/dev/null) | ✅ | exit 0 |
| PF5 | `judge_vs_human.py summary …` | ✅ | **RECONCILES ✓** Δ=0.0002 |
| Beat 1 | `provenance.py build …` | ✅⚠ | 100 traces, run κ=0.677 — prints `⚠ UNVERIFIED` (see Flag 1) |
| Beat 2 | `provenance.py card … reg-0088` | ✅ | MISMATCH defect card (judge=unclear, gold=non-compliant) |
| Beat 3 | `judge_vs_human.py replay … --no-anim` | ✅ | **RECONCILES ✓** Δ=0.0002; confusion matrix + per-class κ render |
| Beat 4 | `judge_vs_human.py summary …` | ✅ | TPR 0.857 · TNR 0.950 · abst 0.120 |
| Beat 5 | `judge_vs_human.py card … reg-0021` | ✅⚠ | adjudication card renders; **content differs from DEMO.md script** (see Flag 2) |
| Edge 1 | `replay … rubric-graded-v4` (N=13 partial) | ✅ | **refuses, exit 2**, prints PARTIAL-TABLE banner — guard works |
| Edge 2 | `provenance.py mismatches …` | ✅ | 20 mismatches listed, unattributed flagged |

**Reconciliation:** recomputed κ = logged κ = 0.677 (Δ=0.0002) on the only full-trace N=100 run.
**Gold-drift:** no spurious drift warning against the 06-04 snapshot.

---

## Flags (fix in DEMO.md before recording — narration, not code)

**Flag 1 — Beat 1 `⚠ UNVERIFIED (passed file slug ≠ run slug)` — RESOLVED 2026-06-24.**
`provenance build` flags the slug mismatch (run `fable-judge-v1` vs scaffold-file slug `rubric-graded-v4`); this shows on camera. DEMO.md already pre-empts it in narration (Beat 1, the "If the ⚠ UNVERIFIED flag shows" line). The only gap was the "What the viewer sees" block showing an idealized output without the flag — **updated 2026-06-24 to show the real line including `[⚠ UNVERIFIED …]`**. No further action.

**Flag 2 — Beat 5 narration — ALREADY CORRECT (stale flag).**
This flag was raised against the 2026-06-22 run-sheet text (*"judge=non-compliant → human=unclear"*). The current DEMO.md Beat 5 already matches the real card: **human=compliant, judge=unclear → MISMATCH**, with the corrections-log relabel (unclear→compliant, δκ +0.030) and an accurate "the gold set itself improves" narration that even notes Fable's abstention. It was corrected between 06-22 and 06-24. No action needed.

---

---

## Phase B — fresh subagent eval runs (executed 2026-06-24, no API spend)

Two candidates judged via the `regeval-autoresearch.md` procedure: 10 parallel subagents, 10 items/context, gold labels stripped from inputs, model pinned to `sonnet` (4.6). Scored with `score.py` (no API key). Both produced full per-item tables and **reconcile through the demo tooling**.

| Run | Scaffold | κ | verdict | TPR | TNR | abst | reconciles |
|---|---|---|---|---|---|---|---|
| 2026-06-24-01 | rubric-graded-v4 (champion) | **0.570** | DISCARD | 0.690 | 0.975 | 0.160 | ✓ Δ=0.0005 |
| 2026-06-24-02 | skills-v2 (never-run) | **0.620** | HOLD | 0.619 | 0.950 | 0.290 | ✓ Δ=0.0002 |

Full traces: `traces/2026-06-24-01-rubric-graded-v4.jsonl`, `traces/2026-06-24-02-skills-v2.jsonl` (100 records each).

### Headline finding — harness sensitivity dominates scaffold differences

The champion scaffold scored **0.820** via the original sonnet-4-5 *one-call-per-item API* run, but only **0.570** here via *batched-subagent sonnet-4-6*. That ~0.25 κ drop from swapping the harness/model is **larger than the gaps between the scaffolds we were testing**. Implication for eval validity: **candidate comparisons are only meaningful when the harness is held fixed.** The subagent harness cannot reproduce the champion number — it is a different measurement instrument.

Secondary findings:
- Under the *same* subagent harness, **skills-v2 (0.620) > champion scaffold (0.570)** — its Step-4 "description exclusion" patch genuinely recovers some compliant edge cases (TPR/abstention behaviour), but it **over-abstains (0.290)**, which caps κ. Defensible "the patch helped on its target class but introduced a new failure mode" narrative.
- `fable-judge-v1` (0.677, also subagent harness) remains the **highest full-trace run on disk** — higher than either run today.

### Demo implication
Phase B did **not** yield a champion replay. To replay the real 0.820 champion live, an **API-key `run_experiment.py` run (sonnet-4-5, one-call-per-item)** is required — out of scope under the no-API-spend constraint. So **Option B stands**: the demo replays `fable-judge-v1` (0.677) and narrates the champion verbally. Net positive: there are now **3 full-trace runs that reconcile** (0.677 / 0.570 / 0.620), proving the harness on fresh, never-before-scored data — a stronger "the harness works" story than a single logged run.

---

## What this validation does NOT cover

- **No champion (0.820) live replay** — not achievable via the subagent harness (see Phase B). Needs an API run if desired before recording.
- No recording, no publish — recorded demo remains gated behind **Riddler + Vicki Vale**.
- **Phase C resolved:** orphaned worktree `relaxed-rosalind-2381b2` / commit `f805270` is **already merged into main** (`0b2c88e`); branch deleted. No disposition needed.
