# RegEval CD / production-monitoring — design (not built)

**Status:** DESIGN ONLY. There is no live system emitting production traces, so this layer cannot
be built or measured today. This doc closes the *design* gap named in the Husain/Shankar audit
(Lesson 6: CI guards known-unknowns; CD surfaces unknown-unknowns). RegEval currently has CI
(a curated gold set run on every scaffold change) but **zero CD**.

## Why it's missing (honest)

RegEval is a judge-alignment research project, not a deployed pipeline. CI is legitimate now;
CD is not buildable until a regulated-output system is in production with logged traces. Naming
the gap beats faking it.

## The two halves (per Lesson 6)

| | CI (have) | CD (this design) |
|---|---|---|
| Guards | known failure modes (regression) | unknown-unknowns (drift, novel inputs) |
| Data | curated gold set (`gold.jsonl` dev + `heldout_v2.jsonl` test) | sampled production traces |
| Cadence | every scaffold change | continuous + periodic re-alignment |
| Metric | binary κ (frozen test) | corrected θ̂ + 95% CI on sampled prod |

## Design

### 1. Logging (prerequisite)
Per request, log: input text, judge label + rationale, scaffold version, **pinned judge model id**,
timestamp, and any downstream human override. Organise as traces. Without this, nothing else works.

### 2. Async production evals
- Sample **1–5% stratified** by regulatory regime (so rare regimes aren't lost).
- Run the binary judge async (latency/cost tolerant).
- Compute **corrected θ̂ = (p_obs + TNR − 1) / (TPR + TNR − 1)** using the *frozen test-set* TPR/TNR,
  with 95% CI. Dashboard θ̂; alert on deviation beyond CI.

### 3. Judge-drift re-alignment loop
- Every few weeks (or on any provider model update): sample recent prod traces, get **fresh human
  labels**, recompute judge TPR/TNR. If they drop → re-tune prompt, re-validate on the frozen test,
  redeploy. (Directly addresses FM-9 model non-portability + FM-10 harness variance.)

### 4. Synchronous guardrails (separate from the judge)
Lightweight, code-based, very low false-fail: PII/secrets blocklist, schema/format validation,
banned-claim regex (e.g. "guaranteed return"). Action on fail: reject / retry / fallback. These run
inline; the LLM judge runs async.

## Triggers to build this
Build when ANY: (a) a regulated-output system goes to pilot; (b) ≥100 real traces/week exist;
(c) an external party asks for a production accuracy number (θ̂ is the only honest answer there).

## Related
[[Evals/regeval/discovery-pass-2026-06-28]] · [[Evals/regeval/metric]] · [[Evals/regeval/human-annotation-protocol]] · [[Evals/regeval/failure-taxonomy]]
