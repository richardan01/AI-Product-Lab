# RegEval — wall-clock budget tracker

**Weekly cap:** fixed (per Q3 thesis allocation)
**Session cap:** 60 min / 12 experiments
**Per-experiment cap:** 5 min target, 8 min hard kill

The runner refuses new experiments once the session cap is hit. Weekly cap is enforced by you; if a week's row crosses the cap, RegEval is closed for the week — go work the canonical essay or technical depth.

## Week log

| Week (Mon–Sun) | Experiments | Wall clock (min) | KEEP count | Notes |
|---|---|---|---|---|
| 2026-W18 (Apr 27 – May 3) | 0 | 0 | 0 | scaffolding only — no runs yet |
| 2026-W21 (May 18 – May 24) | 1 | 5 | 0 | REV-003 baseline run — HOLD κ=0.500 |
| 2026-W22 (May 25 – May 31) | 5 | ~22 | 0 | 4 experiments (strict/lenient/graded/graded-v2) + full N=100 validation. Best: rubric-graded-v2 κ=0.740 HOLD. REV-007 done (gold=100). No KEEP yet — trigger 1 + trigger 5b need refinement. |
| 2026-W23 (Jun 2 – Jun 8) | 4 | ~34 | 1 | gold-cal-v1 KEEP κ=0.820. skills-v1 DISCARD κ=0.733. challenger-v1 DISCARD κ=0.380 (final) / 0.770 (judge-only Opus). Adversarial flip logic wrong for calibrated judge. Opus model native improvement > challenger architecture. |

## Session log (rolling, last 30 days)

| Date | Session start (UTC) | Experiments | Wall clock | Outcome |
|---|---|---|---|---|
| 2026-05-23 | ~09:00 UTC | 1 | ~5 min | HOLD — κ=0.500; next: baseline-v2-unclear-expanded |
| 2026-05-29 | ~02:40 UTC | 3 | ~6 min | 1 DISCARD (strict), 2 HOLD κ=0.600 (lenient, graded); next: graded + 5th 'unverifiable-satisfaction' trigger |
| 2026-05-29 | ~03:10 UTC | 2 | ~10 min | rubric-graded-v2: N=30 κ=1.000 (initially KEEP, revoked); N=100 κ=0.740 (HOLD). REV-007 gold expanded to 100. Best scaffold to date. |
| 2026-06-04 | session | 1 | ~20 min | gold-cal-v1: KEEP κ=0.820. Gold adjudication of 6 unclear items → 2 relabeled compliant. rubric-graded-v4 promoted to current. First KEEP. |
| 2026-06-08 | session | 3 | ~30 min | skills-v1 DISCARD κ=0.733. challenger-v1 DISCARD κ=0.380 final / 0.770 judge-only (Opus). skills-v2 candidate drafted. Hidden finding: Opus judge-only beats Sonnet skills-v1 by +0.037 with zero trigger-5a over-fires. |
| 2026-06-10 | ~04:06 UTC | 1 | ~6 min | fable-judge-v1 DISCARD κ=0.677. Fable 5 on unchanged v4 scaffold regressed −0.143: unclear class collapsed (per-class κ=0.299), binaries strong. "Model upgrade > architecture" hypothesis refuted for this scaffold — scaffold is Sonnet-bias-tuned. Subagent harness (no API key), batched 10/context. Next: fable-judge-v2 retuning abstention section only. |
| 2026-06-23 | 02:26 UTC | 1 | ~3 min | skills-v2 HOLD κ=0.822 (CI [0.721,0.917]). Description-exclusion patch to Step 4 recovered 6/7 compliant items skills-v1 lost (TPR 0.786→0.976). Meets KEEP bar but not promoted: +0.002 vs champion is within noise AND judges were Opus subagents vs champion's sonnet-4-5 — and W23 already showed Opus alone clears the trigger-5a over-fires, so the gain is confounded with model. Next: sonnet-4-5 confirmation run to disentangle patch vs model. |

## How to update

After every `/regeval-run` invocation, append a row to the session log. At week-end (Sunday 23:59 SGT), roll the week's totals into the week log and reset the session log filter.

If a session crossed the cap, write a one-line root-cause in the Notes column. Three over-cap weeks in a row = audit the loop, the cap is right.

## Related

[[Evals/regeval/regeval-suite]] · [[Evals/regeval/runner]] · [[Evals/regeval/experiments/log]] · [[Projects/ralph/brief]] · [[Agents/Gotham/thesis-q3-2026]]
