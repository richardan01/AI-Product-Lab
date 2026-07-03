# Evals — index

**Purpose:** Offline audit suites for AI Product Lab. Author/grader separation enforced. No inline grading in the same context window.

**Cadence:** Run both primary suites every 60 days at minimum, or after any model upgrade / workflow change.

**Before citing any suite externally:** run [[Evals/eval-audit-checklist]] (P0/P1/P2 framework).

---

## Suites

| Suite | Criteria | Pass threshold | Owned by | Last run |
|---|---|---|---|---|
| [[Evals/onboarding/onboarding-suite\|onboarding]] | 12 | ≥ 10/12 | [[Agents/Gotham/Computer/alfred\|Alfred]] | [2026-06-23](Evals/run-log.md) · `opus-4-8` · content evals PASS (0 ❌); ⚠ temporal 02/07 not run (no interactive runner) — not fully citable |
| [[Evals/research-synthesis/research-synthesis-suite\|research-synthesis]] | 7 | ≥ 6/7 | [[Agents/Gotham/Computer/oracle\|Oracle]] | _not yet logged_ |
| discovery-synthesis *(private companion suite — not shipped in this repo)* | in progress | — | [[Agents/Gotham/Computer/oracle\|Oracle]] | _not yet logged_ |
| [[Evals/regeval/regeval-suite\|regeval]] | binary (κ) | κ ≥ 0.80 | [[Agents/Gotham/Computer/lucius-fox\|Lucius Fox]] | [2026-06-28](Evals/run-log.md) · **BINARY collapse** (see [[Evals/regeval/discovery-pass-2026-06-28]]). Forward pass found 2 integrity defects: phantom held-out (FM-11, `gold_expansion`=dup of tuning set → old κ=0.661 was in-sample) + `unclear` fails IAA (FM-12, κ=0.48). Binary judge: **κ=1.000 in-sample (82)** + **κ=1.000 genuine held-out (36, 20 new regimes)** — clean-construct caveat; borderline+prod = next gap. Old 3-class 0.820 was Sonnet-4-5 API, doesn't reproduce on demo harness (FM-10). |
| [[Evals/gate-group/gate-group-suite\|gate-group]] | meta-eval | — | [[Agents/Gotham/Computer/riddler\|Riddler]] | _no full run logged_ · 3 failures logged 2026-06-10 (see failure-log); re-run pending |
| peer-review (meta-eval) | 5 | CITABLE (0 ❌) | [[Agents/Gotham/Computer/riddler\|Riddler]] | [2026-06-23](Evals/run-log.md) · `opus-4-8` r2 · ✅ CITABLE (post-fix; synthesis 4/4, clean cleared, PRD recall fixed) |
| prd-readiness (meta-eval) | 4 | CITABLE (0 ❌) | [[Agents/Gotham/Computer/lucius-fox\|Lucius Fox]] | [2026-06-23](Evals/run-log.md) · `opus-4-8` r2 · ✅ CITABLE (post-fix; AI gates added, clean→READY 12/12) |
| [[Evals/memory-consolidation/memory-consolidation-suite\|memory-consolidation]] | 5 | ≥ 4/5 (01+02 mandatory) | [[Agents/Gotham/Computer/alfred\|Alfred]] | 2026-06-20 · `opus-4-8` · PASS · P 100% / R 95.2% (provisional-measured) *(result file local — results/ is gitignored)* |

---

## Run log

All runs → `Evals/run-log.md` (append-only). Individual result files → `<suite>/results/YYYY-MM-DD_<model>.md`.

**Update the "Last run" column above after every run.**

---

## Suite → project map

| Suite | Project it validates | Agent that runs it |
|---|---|---|
| onboarding | Fresh-clone onboarding of the OS | Alfred |
| research-synthesis | Any Oracle research brief | Oracle |
| discovery-synthesis | Product discovery synthesis workflow | Oracle |
| regeval | [[Projects/ralph/brief]] — RegEval flagship | Lucius Fox |
| gate-group | The gate pipeline itself (Riddler + Vale + Ducard) | Riddler (meta) |

---

## Failure log

When a suite fails → log to `Evals/failure-log.md`:

```
Date | Suite | Criterion | Agent prompt file edited | Re-run result
```

---

## Related

[[Agents/agent-system-architecture]] · [[Workflows/gate-dispatch]] · [[Projects/ralph/brief]] · [[Knowledge/Research/regeval-synthesis]] · [[Evals/eval-audit-checklist]] · [[Evals/regeval/methodology-comparison]] · [[Evals/regeval/failure-taxonomy]]
