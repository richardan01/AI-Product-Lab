# Evals — index

**Purpose:** Offline audit suites for AI Product Lab. Author/grader separation enforced. No inline grading in the same context window.

**Cadence:** Run both primary suites every 60 days at minimum, or after any model upgrade / workflow change.

**Before citing any suite externally:** run [[Evals/eval-audit-checklist]] (P0/P1/P2 framework).

---

## Suites

| Suite | Criteria | Pass threshold | Owned by | Last run |
|---|---|---|---|---|
| [[Evals/onboarding/onboarding-suite\|onboarding]] | 12 | ≥ 10/12 | [[Agents/Gotham/Computer/alfred\|Alfred]] | [2026-07-05](Evals/run-log.md) · content 2026-06-23 `opus-4-8` PASS (0 ❌) + temporal 02/07 2026-07-05 `sonnet-5` PASS (0 ❌, 1 ⚠) — citable; C7 (re-run scenario) still unexercised, coverage gap logged |
| [[Evals/research-synthesis/research-synthesis-suite\|research-synthesis]] | 7 | ≥ 6/7 | [[Agents/Gotham/Computer/oracle\|Oracle]] | _not yet logged_ |
| discovery-synthesis _(private companion suite — not shipped in this repo)_ | in progress | — | [[Agents/Gotham/Computer/oracle\|Oracle]] | _not yet logged_ |
| [[Evals/regeval/regeval-suite\|regeval]] | binary (κ) | κ ≥ 0.80 | [[Agents/Gotham/Computer/lucius-fox\|Lucius Fox]] | [2026-06-28](Evals/run-log.md) · **BINARY collapse** (see [[Evals/regeval/discovery-pass-2026-06-28]]). Forward pass found 2 integrity defects: phantom held-out (FM-11, `gold_expansion`=dup of tuning set → old κ=0.661 was in-sample) + `unclear` fails IAA (FM-12, κ=0.48). Binary judge: **κ=1.000 in-sample (82)** + **κ=1.000 genuine held-out (36, 20 new regimes)** — clean-construct caveat; borderline+prod = next gap. Old 3-class 0.820 was Sonnet-4-5 API, doesn't reproduce on demo harness (FM-10). |
| [[Evals/gate-group/gate-group-suite\|gate-group]] | meta-eval | ≥ 7/8, C2+C4 mandatory | [[Agents/Gotham/Computer/riddler\|Riddler]] | [2026-07-06](Evals/run-log.md) · Riddler=opus, Vale=sonnet, Ducard=opus · r1 6/8 FAIL → remediation → r2 **7/8 PASS** (C2/C4 clean; C5 fixed; C7 partial — Ducard prose-preamble follow-up open, see failure-log) |
| peer-review (meta-eval) | 5 | CITABLE (0 ❌) | [[Agents/Gotham/Computer/riddler\|Riddler]] | [2026-07-14](Evals/run-log.md) · `sonnet-5` · r1 ❌ NOT CITABLE (clean control failed 0/3 — Pass 3 Rule 2 hallucinated a rollback Must Fix on non-design artifacts) → fix `e206533` → **r2 ✅ regression CLOSED** (clean control 3/3; eval 04 P0 passes; no ❌ on eval 01). Two pre-existing non-blocking follow-ups remain (prd F1 recall miss; synthesis eval-05 checklist crosswalk) — see failure-log.md. |
| prd-readiness (meta-eval) | 4 | CITABLE (0 ❌) | [[Agents/Gotham/Computer/lucius-fox\|Lucius Fox]] | [2026-06-23](Evals/run-log.md) · `opus-4-8` r2 · ✅ CITABLE (post-fix; AI gates added, clean→READY 12/12) |
| [[Evals/memory-consolidation/memory-consolidation-suite\|memory-consolidation]] | 5 | ≥ 4/5 (01+02 mandatory) | [[Agents/Gotham/Computer/alfred\|Alfred]] | 2026-06-20 · `opus-4-8` · PASS · P 100% / R 95.2% (provisional-measured) _(result file local — results/ is gitignored)_ |
| build-review (meta-eval) | on disk | — | [[Agents/Gotham/Computer/lucius-fox\|Lucius Fox]] | _not yet logged_ |
| go-nogo (meta-eval) | on disk | 18/18 | [[Agents/Gotham/Computer/bruce-wayne\|Bruce Wayne]] | [2026-07-14](Evals/run-log.md) · `sonnet-5` · ✅ CITABLE (first-ever run — 18/18 criteria, both fixtures clean; 2 non-blocking findings logged: Rollback-gate severity one notch soft, verdict-file schema mismatch) |
| research-sufficiency (meta-eval) | on disk | — | [[Agents/Gotham/Computer/oracle\|Oracle]] | _not yet logged_ |
| monitoring | README only — not yet a graded suite | — | — | — |

This table is the canonical suite registry. `Evals/evals-hub.md` shows only the small curated set of primary/active suites.

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
