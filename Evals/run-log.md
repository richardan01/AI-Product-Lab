# Eval run log

Append new entries below. Do not edit past runs — they are the historical record. For full result files and transcripts, see `<suite>/results/`.

> **2026-07 model-currency note:** entries before this date may cite `claude-sonnet-4-6` (real, was current at the time) or older models — these are accurate historical records and are not being retroactively corrected. `eval-runner`/`eval-grader` were re-pinned to `claude-sonnet-5` on 2026-07-02; new entries should reflect that.

> **Public template note**
> Run result files and transcripts are intentionally gitignored (`Evals/*/results/*`).
> The public repo stores suite structure and protocol only.
> Private working copies should track the latest run evidence in local result files.

---

## Entry format

```
### YYYY-MM-DD — <suite> — <model>

| Field       | Value |
|-------------|-------|
| Date        | YYYY-MM-DD |
| Suite       | onboarding / research-synthesis |
| Model       | model ID |
| Commit SHA  | git rev-parse HEAD at run time |
| Runner      | eval-runner sub-agent (or session identifier) |
| Grader      | eval-grader sub-agent (or separate session identifier) |
| Fixture(s)  | file(s) from inputs/ |
| Raw pass rate | <p_obs>/<N> = <%> |
| Bias-corrected θ̂ | (p_obs + TNR - 1) / (TPR + TNR - 1) — judge-graded evals only |
| 95% CI on θ̂ | [<lo>, <hi>] via bootstrap (B=20000) — judge-graded evals only |
| Status      | ✅ pass / ❌ regression |

**Per-eval grading method** (so reviewers can see at a glance which judges were involved):
| Eval | Method | Judge TPR_test | Judge TNR_test |
|---|---|---|---|
| 04 | programmatic (`grade.sh`) | — | — |
| 05 | LLM judge (`judge-prompt.md`) | 0.XX | 0.XX |
| others | eval-grader sub-agent (manual) | — | — |

**Failures:**
- <criterion-id> ❌ — <one-line description of what failed>

**Introspection:**
> Why did the runner produce this output? What in the workflow or context led to this?

**Remediation:**
- <what was changed, or "none — accepted as known limitation">

**Result file:** `<suite>/results/YYYY-MM-DD_<model>.md`
```

### Bias-corrected success rate (Hamel §5.6)

For judge-graded evals only. With raw observed pass rate `p_obs = k/N` and judge calibration `TPR_test`, `TNR_test`:

```
θ̂ = (p_obs + TNR_test - 1) / (TPR_test + TNR_test - 1)
```

The corrected θ̂ is the citable number. Leave blank for programmatic and manually-graded evals (raw rate is already unbiased there).

Confidence interval: bootstrap with B = 20000 resamples over the labeled examples used to compute TPR/TNR.

---

## Run history

### 2025-01-15 — onboarding — claude-3-5-sonnet-20241022

| Field | Value |
|---|---|
| Date | 2025-01-15 |
| Suite | onboarding |
| Model | `claude-3-5-sonnet-20241022` |
| Commit SHA | `b94a501` |
| Runner | Session A (fresh clone, no prior context) |
| Grader | Session B (separate invocation, transcript-only) |
| Fixture(s) | `jordan-lee-profile.md` (Executive operator) |
| Score | 11 / 12 |
| Status | ✅ pass |

**Failures:**

- `07-per-step-interactivity` ❌ — At Phase 9, the runner presented all three proposed file writes (`CLAUDE.md`, `GOALS.md`, `Tasks/active.md`) in a single message and accepted a single "yes, go ahead" reply as authorization to write all three. Criteria requires individual per-file confirmation.

**Introspection:**

> The Phase 9 prompt in `Workflows/interactive-onboarding.md` read: "Shall I write all proposed files?" — this phrasing invited a batch approval. The runner correctly asked before writing (eval 02 passed), but the granularity of confirmation was insufficient. The model followed the prompt faithfully; the bug was in the prompt wording, not model behavior.

**Remediation:**

- Phase 9 prompt tightened to enumerate each file by name and require a per-file confirmation before writing. Phrasing changed from "Shall I write all proposed files?" to "I'll confirm each file individually. First: `CLAUDE.md` — does this look right to write?" with subsequent turns for each remaining file.
- Added `taylor-polite-acks.md` fixture to the fixture set to stress this failure mode explicitly in future runs.

**Result file:** `onboarding/results/2025-01-15_claude-3-5-sonnet-20241022.md`

---

*The entry above is a worked sample, not the latest run. In a private working copy, the next run fires on the 60-day cadence or the next model upgrade, whichever comes first; current run evidence is tracked locally per the note above.*

---

### 2026-06-10 — onboarding — claude-fable-5

| Field | Value |
|---|---|
| Date | 2026-06-10 |
| Suite | onboarding |
| Model | `claude-fable-5` |
| Commit SHA | `8f1e329d88f3d536116fc7bacee7ad80e18e0774` |
| Runner | eval-runner sub-agent (isolated context) |
| Grader | eval-grader sub-agent (isolated context) |
| Fixture(s) | `jordan-lee-profile.md`, `sam-okafor-builder-variant.md`, `riley-park-minimalist.md` |
| Raw pass rate | Jordan Lee: 6/11 · Sam Okafor: 6/10 · Riley Park: 6/11 |
| Bias-corrected θ̂ | N/A — all manual/programmatic grading |
| Status | ❌ NOT CITABLE (target ≥ 10/12 per fixture; P0 harness bugs found) |

**Per-eval grading method:**
| Eval | Method |
|---|---|
| 04 | programmatic (`grade.sh`) |
| all others | eval-grader sub-agent (manual) |

**Failures and partials:**

- `04-no-residual-placeholders` ❌ (all 3 fixtures) — `[HEAD_OF_DEPT]` consistently survives into CLAUDE.md; `grade.sh` also generates false positives from backtick-quoted bracket patterns in documentation text.
- `11-privacy-boundaries-enforced` ⚠ (all 3 fixtures) — riley-park: privacy list auto-generated without eliciting from user (no Phase 7 content-exclusion question); jordan-lee/sam-okafor: privacy categories not named explicitly in Phase 8 summary table.
- `07-per-step-interactivity` ⚠ (sam-okafor, riley-park) — C5: "sounds good" treated as Phase 6 draft-content confirmation without re-asking for explicit yes; Phase 9 write gates enforced correctly.
- `01-no-invented-identity` ⚠ (jordan-lee, sam-okafor) — C5: `[HEAD_OF_DEPT]` not listed as a deferred field in Phase 8 summary table; riley-park correctly surfaces deferred fields.
- `03-persona-routing-respected` insufficient-evidence (sam-okafor) — criteria C1–C4 written for Executive operator; cannot apply literally to Builder/AI PM run.

**What passed cleanly:**
- `09-thought-frameworks` ✅ 3/3 — consistent across all personas
- `10-taste-captured` ✅ 3/3 — consistent across all personas
- `05-goals-specific-not-generic` ✅ 2/3 (partial on riley-park: single 60-day outcome, workflow doesn't prompt for second)
- `08-okr-strategic-alignment` ✅ 2/3 (partial on riley-park: deferred proof metric without follow-up task)
- Phase 10 verification loop ✅ — all three runners correctly ran verification, caught residual placeholders, and offered three-way resolution

**Introspection:**
> Four harness bugs identified: (1) workflow has no question for HEAD_OF_DEPT (fix: add optional Phase 3 question); (2) grade.sh matches backtick-quoted bracket patterns as false positives (fix: regex update); (3) Phase 6 lacks explicit-yes requirement for draft confirmations (fix: parallel the Phase 9 language); (4) no mandatory Phase 7 content-exclusion question (fix: add "what should never go in your files?" prompt). All are workflow/harness fixes, not model capability gaps.

**Remediation (recommended — not yet applied):**
- P0: Add Phase 1/3 question for HEAD_OF_DEPT (optional)
- P0: Fix `grade.sh` regex to skip backtick-quoted bracket patterns
- P0: Add mandatory Phase 7 content-exclusion question
- P0: Rewrite eval-03 criteria C1–C4 to be persona-agnostic
- P1: Add explicit-yes requirement to Phase 6 draft confirmations
- P1: Mandate "Deferred fields" sub-section in Phase 8 summary template
- P1: Auto-create Tasks/follow-ups.md entry when a Phase 5B strategic field is deferred

**Result file:** `onboarding/results/2026-06-10_claude-fable-5.md` *(gitignored per public template policy)*

---

### 2026-06-11 — peer-review — claude-sonnet-4-6

| Field | Value |
|---|---|
| Date | 2026-06-11 |
| Suite | peer-review (meta-eval — first decision-quality suite; grades the reviewer gate) |
| Model | `claude-sonnet-4-6` |
| Commit SHA | `fab4e2342c3574c4202ba41cd0e0a9fc9f656774` |
| Runner | eval-runner sub-agent (isolated; attested no `_answer-keys/` access) |
| Grader | eval-grader sub-agent (isolated; transcript + fixture + answer key + criteria only) |
| Fixture(s) | `prd-activation-checkout.md`, `synthesis-support-tickets.md`, `weekly-update-clean.md` (clean control) |
| Raw pass rate | PRD: 2/4 · Synthesis: 3/4 · Clean control: **0/3** |
| Bias-corrected θ̂ | N/A — all manual grading |
| Status | ❌ FAIL — P0: clean control flunked (gate generates noise) |

**Per-eval grading method:**
| Eval | Method |
|---|---|
| all (01–05) | eval-grader sub-agent (manual, against `_answer-keys/`) |

**Failures:**

- `04-clean-artifact-not-flunked` ❌ — reviewer returned NEEDS REVISION + 2 Must Fix on the false-positive control, demanding "Blocked"/"Decisions needed" section headers on a document that communicates both in substance. Template pedantry, the exact failure mode the eval was built to catch.
- `02-no-hallucinated-findings` ❌ (clean) / ⚠ (PRD) — clean: the two Must Fix items are hallucinated gaps; PRD: F6 (Should Fix in key) severity-inflated to Must Fix.
- `03-verdict-matches-rubric` ❌ (clean) — rubric applied correctly to a broken scorecard; error propagated from the structural scan, not the verdict step.
- `01-planted-blockers-caught` ⚠ (synthesis) — S2 (412 vs 380 cross-section count contradiction) missed; rationalized as population-vs-sample ambiguity.
- `05-fix-checklist-actionable` ⚠ (PRD) — US-3 item names the location but not what the acceptance criteria must cover.

**What passed:** recall on planted blockers 9/10 across flawed fixtures (incl. the PRD Q3/Q4 cross-section contradiction); zero fabricated findings on flawed fixtures; verdict mechanics exact on both flawed fixtures; isolation held end-to-end; no verdict-file pollution (pre-run fix verified).

**Introspection:**
> Root cause of the P0: `ground-truth.md` is still placeholder-state, so the reviewer anchored on the document-type section checklist and tested header presence instead of information presence — the skill's Step 3 literally instructs "mark each required section present/partial/missing." Harness bug, not model capability. Recall is strong; precision is the failure axis.

**Remediation (recommended — not yet applied):**
- P0: peer-review Step 3 — test information presence, not header presence
- P0: peer-review degraded-mode rule when ground-truth.md is unfilled (cap structural findings at Should Fix)
- P1: severity guidance (Must Fix = blocks stated purpose) + explicit cross-section quantity-consistency pass
- P2: checklist items state what added content must contain

**Result file:** `peer-review/results/2026-06-11_claude-sonnet-4-6.md` *(local, not shipped — results/ is gitignored in this public repo)*

---

### 2026-06-12 — peer-review — claude-sonnet-4-6 (r2, post P0+P1 fixes)

| Field | Value |
|---|---|
| Date | 2026-06-12 |
| Suite | peer-review |
| Model | `claude-sonnet-4-6` |
| Commit SHA | `622767eaf51a2c1e3c707e7cd1d7fc27ec7c003c` *(transcripts stamped `30c1ba6` — pre-amend, tree-identical)* |
| Runner | eval-runner sub-agents (3 parallel; isolated context) |
| Grader | eval-grader sub-agents (3 parallel; isolated context) |
| Fixture(s) | `prd-activation-checkout.md`, `synthesis-support-tickets.md`, `weekly-update-clean.md` |
| Raw pass rate | PRD: 2/4 · Synthesis: 4/4 · Clean: 1+2⚠/3 |
| Bias-corrected θ̂ | N/A — all manual grading |
| Status | ⚠️ PARTIAL — P0 fixed; synthesis PASS; PRD eval 01 ❌ (recall regression) |

**Per-eval grading method:**
| Eval | Method |
|---|---|
| all (01–05) | eval-grader sub-agents (manual, against `_answer-keys/`) |

**P0+P1 fixes confirmed working:**

- `04-clean-artifact-not-flunked` r1 ❌ → r2 ⚠️ — P0 fixed: CONDITIONAL (not NEEDS REVISION), zero Must Fix on clean control. Degraded-mode cap and information-presence check working.
- `01-planted-blockers-caught` synthesis r1 ⚠ (S2 missed) → r2 ✅ (S2 caught) — Pass 1b cross-section consistency check caught 412 vs 380 contradiction.
- `02-no-hallucinated-findings` PRD r1 ⚠ (severity inflation) → r2 ✅ — severity bar fix working.

**New failures:**

- `01-planted-blockers-caught` PRD r2 ❌ — F1 (US-3: no acceptance criteria) and F5 (no rollback/failure plan for payments flow) both missed. F1: runner scanned for user-story section presence, marked "US-1, US-2, US-3 with acceptance criteria ✅" without verifying US-3 content. F5: degraded-mode cap suppressed the rollback-plan finding (treated as template gap, capped to Should Fix sub-bullet of Launch Plan).

**What passed:**

- Synthesis: 4/4 ✅ — first full PASS on any flawed fixture.
- PRD eval 02 ✅, eval 03 ✅.
- Clean: eval 03 ✅, eval 04 P0 not triggered (CONDITIONAL ≠ NEEDS REVISION).
- Isolation held end-to-end on all 3 runners; no `_answer-keys/` access confirmed.

**Introspection:**
> F1 regression: the information-presence instruction changed the structural scan from header-checking to surface content-checking, but didn't add per-element depth (checking each user story for its own ACs). The fix improved precision at the cost of recall depth. F5 regression: the degraded-mode cap is over-broad — "purely structural/template findings" should not include risk/safety content that happens to coincide with a missing section (rollback plan for held-funds payments is substantive regardless of degraded mode).

**Remediation (recommended — not yet applied):**
- P0: Per-user-story AC check — explicit instruction: "for each user story, verify that story's ACs are present"
- P0: Narrow degraded-mode cap — "substantive safety/risk/compliance content keeps full severity regardless of degraded mode"
- P1: Clean-fixture threshold — extend information-presence principle to Should Fix (information present under different heading = Nice to Fix, not Should Fix)
- P2: Flag unsourced quantified claims ("78% of X" with no data source)

**Result file:** `peer-review/results/2026-06-12_claude-sonnet-4-6_r2.md` *(local, not shipped — results/ is gitignored in this public repo)*

---

### 2026-06-23 — prd-readiness — claude-opus-4-8

| Field       | Value |
|-------------|-------|
| Date        | 2026-06-23 |
| Suite       | prd-readiness (meta-eval — FIRST RUN) |
| Model       | claude-opus-4-8 |
| Commit SHA  | 8d1ddf64ebbb993698a64c629269c2f953a9eb36 |
| Runner      | 3 blind Opus subagents (emulated; eval-runner agent does not exist), attested ANSWER-KEY ACCESS: none |
| Grader      | 3 separate Opus subagents (emulated; eval-grader agent does not exist) |
| Fixture(s)  | clean-ai-feature-prd, flawed-standard-prd, flawed-ai-feature-prd |
| Raw pass rate | evals 01–04 aggregate: 0/4 evals clean (01 ❌, 02 ❌, 03 ❌, 04 ❌) |
| Status      | ❌ NOT CITABLE |

**Verdict: NOT CITABLE** — ❌ on eval 01 (clean fixture) and ❌ on eval 04. First run of the suite; harness (eval-runner/eval-grader/eval-ci) does not exist — emulated with generic blind subagents.

**Defects found in `.claude/skills/prd-readiness/SKILL.md`:**
- D1 (P0 false-positive): Feasibility-input gate flunks clean/complete PRDs lacking an explicit architect sign-off line → CONDITIONAL on the clean control (should be READY); sinks evals 01/02/04 on the clean fixture.
- D2 (skill gap): no AI-specific gates exist → eval 03 ❌ on the AI fixture (A2 failure-modes≥3 and A3 fallback-paths structurally uncatchable).
- D3 (decision-rule inconsistency): "any fail → NOT READY" conflicts with "most pass, minor gaps → CONDITIONAL".
- D4 (recall miss): planted scope-ambiguity gap G2 missed on flawed-standard (Scope boundaries marked Pass).

**Remediation:** soften Feasibility gate (D1), add AI-gate branch (D2), make decision rule precise by gate bucket (D3), strengthen scope gate (D4). Re-run after fixes. Full detail: `prd-readiness/results/2026-06-23_claude-opus-4-8.md`.

---

### 2026-06-23 — peer-review — claude-opus-4-8

| Field       | Value |
|-------------|-------|
| Date        | 2026-06-23 |
| Suite       | peer-review (re-run; 2026-06-22 SKILL change) |
| Model       | claude-opus-4-8 |
| Commit SHA  | 8d1ddf64ebbb993698a64c629269c2f953a9eb36 |
| Runner      | 3 blind Opus subagents (emulated), attested ANSWER-KEY ACCESS: none |
| Grader      | 3 separate Opus subagents (emulated) |
| Fixture(s)  | prd-activation-checkout, synthesis-support-tickets, weekly-update-clean |
| Raw pass rate | synthesis 4/4 ✅, clean 3/3 ✅, PRD 1/4 (01 ❌, 02 ⚠, 03 ⚠, 05 ✅) |
| Status      | ❌ NOT CITABLE |

**Verdict: NOT CITABLE** — ❌ on eval 01 (PRD fixture missed 2 Must-Fix planted blockers).

**Improved:** the 2026-06-22 per-story-AC fix WORKED — F1 (US-3 no acceptance criteria) now caught (was the prior r2 miss). Clean control correctly CLEARED (no false positives).

**Residual recall failure (PRD fixture):** F3 (exec "GA Q3 2026" vs timeline "2026-10-30 Q4" cross-section contradiction — flagged a different inconsistency instead) and F5 (no rollback/failure plan for held-funds + deferred-KYC payments flow) both missed. Synthesis fixture's cross-section contradiction (412 vs 380) WAS caught, so the gap is PRD-domain risk + cross-section reasoning specifically.

**Remediation:** P0 add cross-section consistency check (closes F3); P0 require rollback/failure plan for payments/held-funds/auth flows (closes F5); P2 stop flagging present-but-relabeled sections as gaps. Re-run after fixes. Detail: `peer-review/results/2026-06-23_claude-opus-4-8.md`.

---

### 2026-06-23 — onboarding — claude-opus-4-8 (CONTENT-ONLY)

| Field       | Value |
|-------------|-------|
| Date        | 2026-06-23 |
| Suite       | onboarding (content evals only) |
| Model       | claude-opus-4-8 |
| Commit SHA  | 8d1ddf64ebbb993698a64c629269c2f953a9eb36 |
| Runner      | 3 blind Opus subagents (emulated; produce end-state config), attested ANSWER-KEY ACCESS: none |
| Grader      | 3 separate Opus subagents (emulated) |
| Fixture(s)  | jordan-lee-profile, sam-okafor-builder-variant, riley-park-minimalist |
| Raw pass rate | content evals: 7 ✅ / 2 ⚠ / 0 ❌ (per-eval agg across 3 fixtures); temporal 02/07 NOT-RUN |
| Status      | content PASS (0 ❌); suite NOT FULLY CITABLE (02/07 not run) |

**Content evals strong:** 01,03,05,08,09,10,11 all ✅; 04 ⚠ and 06 ⚠ are eval-design tensions, not workflow defects. Validated: no invented identity, correct persona routing (Exec/Builder/Minimalist gates), 80%-certainty trap caught (sam), minimalist deferral correct.

**NOT FULLY CITABLE:** temporal evals 02 (confirmation-before-write) and 07 (per-step-interactivity) NOT RUN — require a real interactive eval-runner (doesn't exist; emulation produces end-state artifacts only, not a trustworthy temporal transcript).

**Recommended fixes:** (1) eval-04 criteria → deferral-aware (annotated/boundary-preserved placeholders pass; only silent raw placeholders fail); (2) build a real eval-runner to enable 02/07. Caveat: jordan-lee runner over-deferred 6 answered fields — likely emulation artifact. Detail: `onboarding/results/2026-06-23_claude-opus-4-8.md`.

---

### 2026-06-23 — prd-readiness r2 (POST-FIX) — claude-opus-4-8

| Field       | Value |
|-------------|-------|
| Date        | 2026-06-23 |
| Suite       | prd-readiness (re-run after skill remediation) |
| Model       | claude-opus-4-8 |
| Commit SHA  | 8d1ddf64ebbb993698a64c629269c2f953a9eb36 |
| Runner      | 3 blind Opus subagents (emulated), attested ANSWER-KEY ACCESS: none |
| Grader      | 3 separate Opus subagents (emulated) |
| Fixture(s)  | clean-ai-feature-prd, flawed-standard-prd, flawed-ai-feature-prd |
| Raw pass rate | evals 01 ✅, 02 ✅, 03 ✅, 04 ✅ (all clean) |
| Status      | ✅ CITABLE |

**Verdict: CITABLE** (was NOT CITABLE in r1). Skill fix validated: D1 false-positive gone (clean → READY 12/12); D2 AI gates applied + A1–A3 caught on AI fixture; D3 bucket-driven decision rule consistent; D4 scope gap G2 now caught. Residual: flawed-standard G4 (incoherent goals) still missed — non-blocking per key (G1–G3 independently block; not a hallucination). Detail: `prd-readiness/results/2026-06-23_claude-opus-4-8_r2.md`.

---

### 2026-06-23 — peer-review r2 (POST-FIX) — claude-opus-4-8

| Field       | Value |
|-------------|-------|
| Date        | 2026-06-23 |
| Suite       | peer-review (re-run after Pass-3 risk-checks added) |
| Model       | claude-opus-4-8 |
| Commit SHA  | 8d1ddf64ebbb993698a64c629269c2f953a9eb36 |
| Runner      | 2 blind Opus subagents (PRD + clean), attested ANSWER-KEY ACCESS: none |
| Grader      | 1 Opus subagent (PRD); clean regression self-evident (CLEARED) |
| Fixture(s)  | prd-activation-checkout (r1 failure), weekly-update-clean (regression); synthesis carried from r1 (4/4) |
| Raw pass rate | PRD 01✅/02✅/05✅; clean CLEARED (02✅/03✅/04✅); synthesis 4/4 (r1) |
| Status      | ✅ CITABLE |

**Verdict: CITABLE** (was NOT CITABLE in r1). Pass-3 cross-cutting risk checks fixed the recall gap: F3 (GA-date cross-section contradiction) and F5 (held-funds rollback/failure plan) now both caught as Must Fix → all 5 Must-Fix planted flaws caught. No regression: clean control stayed CLEARED (Pass-3 correctly produced no false positive — status report ≠ flow spec; dates consistent). Detail: `peer-review/results/2026-06-23_claude-opus-4-8_r2.md`.

---

### 2026-06-04 — regeval — champion of record (gold-cal-v1) + current state

> **Why this entry exists:** regeval's per-experiment evidence lives in `regeval/results.tsv` and `regeval/experiments/log.md` (16 logged runs), but the suite was never surfaced in this canonical run-log or the `index.md` "Last run" column. This entry reconciles the flagship's evidence into the index a reviewer reads first. It is a *roll-up of already-logged runs*, not a new run.

| Field | Value |
|---|---|
| Date | 2026-06-04 (champion) · most-recent run 2026-06-24 |
| Suite | regeval (LLM-as-judge alignment — Cohen's κ vs human gold) |
| Champion scaffold | `rubric-graded-v4` (promoted via `gold-cal-v1`) → `scaffolds/current.md` |
| Champion model | Sonnet (sonnet-4-5 lineage), one-call-per-item analytical score |
| Commit SHA | record at next commit (`git rev-parse HEAD`) — entry written 2026-06-28 |
| Fixture(s) | `inputs/gold.jsonl` (N=100; compliant 42 / non-compliant 40 / unclear 18 post gold-cal) |
| Optimized metric | Cohen's κ (judge vs human gold) |
| **Champion κ** | **0.820** (95% CI [0.720, 0.920]) |
| Diagnostics | TPR=1.000 · TNR=0.975 · abstention=0.090 · confusion 89/100 correct |
| KEEP bar | κ ≥ 0.80 AND CI-lower ≥ 0.70 AND abstention ≤ 0.50 — **all met** |
| Status | ✅ KEEP (champion of record) — see caveats below |

**Logged defect (carried):**
- `reg-0088` ❌ — trigger-5a false-abstains on an overt unauthorised-offering violation (returns `unclear`, gold = `non-compliant`). Does not move champion κ (single item). Scaffold patch scoped, low priority. Source: `experiments/2026-06-04-01-gold-cal-v1.md`.

**Honesty caveats (must travel with the 0.820 number):**
- **Gold-calibration, not scaffold change.** The 0.790→0.820 KEEP came from relabeling 2 gold items (reg-0021, reg-0023 unclear→compliant) after human adjudication confirmed the scaffold was right — the scaffold prompt was unchanged. Legitimate (gold was the error) but it is a gold-calibration KEEP, narrate it as such.
- **Held-out anti-overfit confirm = RUN 2026-06-28 — FAILS THE BAR.** Champion scaffold (rubric-graded-v4) scored on the never-tuned 70-item `inputs/gold_expansion.jsonl` via the subagent harness → **κ=0.661 (CI [0.516, 0.800]), TPR=0.700 TNR=0.967 abst=0.214, N=70** (results.tsv row 17; log.md 2026-06-28). That is **below the κ≥0.70 promotion bar** in `research-goal.md`. Status: KEEP on the tuning set but **NOT `KEEP-confirmed`** out-of-sample → a **`KEEP-overfit / harness-sensitivity flag`**, not a clean confirm. Note the harness story: the headline 0.820 was Sonnet-4-5 API one-call; the *same scaffold* on the reproducible subagent harness scores 0.570 (2026-06-24, tuning set) and 0.661 (held-out) — i.e. **0.820 does not reproduce on the harness you can actually demo.**
- **Cross-model / new-harness re-runs regress (comparable-with-caveat):**
  - 2026-06-24 champion re-run on subagent harness (sonnet-4.6, gold-stripped, batched 10/context) → **κ=0.570** DISCARD. Batching is a within-context contamination confound; not strictly comparable to the one-call champion.
  - 2026-06-23 `skills-v2` on Opus (one-call, cross-model) → **κ=0.822** HOLD (+0.002, within noise; no overwrite, confirmation queued).
  - 2026-06-23 champion repro on Opus → κ=0.768 (Opus under-abstains; unclear class collapses). Third cross-model data point: champion is Sonnet-bias-tuned.

**Introspection:**
> The open frontier is the **unclear class** (champion per-class κ ≈ 0.49) and **cross-model robustness** (champion is Sonnet-tuned). The macro κ=0.820 is real and defensible *with* its caveats; the demo narration should lead with the κ-improvement lineage (0.50→0.74→0.79→0.82) and the held-out-open honesty flag, not the headline number alone.

**Remediation / next:**
- P0 — held-out run DONE 2026-06-28 (κ=0.661, below 0.70 bar → overfit/harness-sensitivity flag). **Open decision:** the demo's honest framing — either (a) demo the Sonnet-4-5 API champion and explicitly disclose the harness/held-out gap, or (b) re-tune for the subagent harness before recording. Do NOT present 0.820 as a stable, reproducible number.
- P1 — patch trigger-5a (reg-0088).
- P2 — maintain `index.md` "Last run" column (onboarding/peer-review/prd-readiness cells are also stale vs this log).

**Evidence:** `regeval/experiments/log.md`, `regeval/results.tsv`, `regeval/experiments/2026-06-04-01-gold-cal-v1.md`, `regeval/scaffolds/current.md`.

---

### 2026-06-28 — regeval — forward discovery pass + BINARY collapse (CORRECTION + new evidence)

| Field | Value |
|---|---|
| Date | 2026-06-28 |
| Suite | regeval (LLM-as-judge alignment) |
| Model | Sonnet subagent harness, forced-commit, shuffled order (pinned: log model_id + harness on every cite) |
| Fixtures | `inputs/gold.jsonl` (dev, binary 82 + 18 quarantined-unclear) · `inputs/heldout_v2.jsonl` (test, 36 net-new, 20 regimes) |
| Optimized metric | Cohen's κ — **now BINARY** (compliant vs non-compliant) |
| Status | ✅ binary κ=1.000 in-sample (82) AND κ=1.000 genuine held-out (36) — first VALID out-of-sample evidence |

**This entry CORRECTS the 2026-06-04 roll-up and the 2026-06-28 "held-out confirm" above.** A forward
open→axial coding pass (the long-deferred Shreya unknown-engine) found two integrity defects:

- **FM-11 — phantom held-out.** `gold_expansion.jsonl` (70, reg-0031..0100) is an **exact subset** of
  the tuning set `gold.jsonl`. The earlier κ=0.661 "held-out confirm" was **in-sample**. Every prior
  held-out / anti-overfit / KEEP-confirmed claim is void. Replaced by genuine `heldout_v2.jsonl`.
- **FM-12 — `unclear` fails IAA.** Blind 2nd annotator: compliant 13/13, non-compliant 13/13,
  **unclear 2/18** → IAA κ=0.48 (<0.60). The `unclear` gold is unreliable; FM-2 was largely a
  gold-label defect, not a judge defect.

**Decision:** collapse to binary; quarantine the 18 `unclear` items. **Result:** binary judge
κ=1.000 on both in-sample (82) and net-new held-out (36, dimension-sampled across 20 regimes the
tuning set never touched). The fresh binary run beat the old 3-class run even on binary items.

**Honest caveat:** both gold sets are clean-construct → κ=1.000 = perfect on clear-cut cases, NOT a
production number. **Next:** author borderline binary items; human re-adjudication
(`human-annotation-protocol.md`); CD on production traces (`cd-monitoring-design.md`).

**Demo implication:** the recorded "0.820→0.661 overfit" story rests on the invalid duplicate set
(0.661 was in-sample). The true, stronger story = *caught two integrity defects in my own eval, fixed
the design, built a real held-out.* Re-record decision pending.

**Evidence:** `regeval/discovery-pass-2026-06-28.md`, `results.tsv` rows 02–03 (2026-06-28),
`experiments/log.md` (2026-06-28), `inputs/heldout_v2.jsonl`, `inputs/gold_expansion.DEPRECATED.md`.

---

### 2026-07-05 — onboarding — temporal evals 02/07 — claude-sonnet-5

| Field | Value |
|---|---|
| Date | 2026-07-05 |
| Suite | onboarding (temporal evals 02-confirmation-before-write, 07-per-step-interactivity) |
| Model | `claude-sonnet-5` (eval-runner + eval-grader pinned) |
| Commit SHA | 67f2db295e22cb3aa7ae518f69444a58fd187afc |
| Runner | 3× eval-runner sub-agents (one per fixture, parallel, isolated) |
| Grader | 6× eval-grader sub-agents (separate contexts; transcript + criteria + samples only) |
| Fixture(s) | jordan-lee-profile · sam-okafor-builder-variant · riley-park-minimalist |
| Raw pass rate | 02: 14✅/1⚠/0❌ (15 gradings) · 07: 16✅/0⚠/0❌ scorable (C6 exercised on riley-park; C7 unexercised) |
| Status | ✅ PASS (0 ❌) — completes the temporal half of the 2026-06-22 pending re-run; suite now fully run (content 2026-06-23 + temporal 2026-07-05) |

Completes the 2026-06-22 hardening-batch re-run: content evals passed 2026-06-23 (`opus-4-8`); this
run adds the missing temporal 02/07 on a real runner/grader pair with author/grader separation and
simulated (recorded, not executed) file writes. Perturbations per `02/input.md` + `07/input.md`:
Phase-8 re-display request, non-explicit "ok"/"sounds good" acks, defer-to-follow-ups on the ❌ row.

**Negative results / gaps:** 02-C4 ⚠ on riley-park — Phase-10 "defer to follow-ups" remediation
wrote `Tasks/follow-ups.md`, outside the Phase-8 approved plan (own fresh consent; criterion vs.
workflow-remediation tension, fix candidates logged). 07-C7 (re-run scenario) unexercised by all
three protocol fixtures — needs `dev-rerun-persona-switch.md` added to the protocol set. Phase-10
checklist never surfaces Phase-8-deferred fields as ❌ rows (coverage gap). N=3 — low statistical
power; baseline, not validation.

**Evidence:** `onboarding/results/2026-07-05_claude-sonnet-5.md`,
`onboarding/results/transcripts/2026-07-05_{jordan-lee-profile,sam-okafor-builder-variant,riley-park-minimalist}_claude-sonnet-5.md` (local — results/ gitignored).

---

### 2026-07-06 — gate-group — FIRST FULL RUN (r1 fail → remediation → r2 pass)

| Field | Value |
|-------------|-------|
| Date | 2026-07-06 |
| Suite | gate-group (meta-eval — grades `Workflows/gate-dispatch.md` + `gate-merge.md` orchestration; FIRST RUN — no prior full run existed since the 2026-06-10 audit) |
| Models | Riddler = `claude-opus-4-8`, Vicki Vale = Sonnet (persona pin `claude-sonnet-4-6` unavailable in Task API tiers, substituted), Henri Ducard = `claude-opus-4-8` |
| Commit SHA | 7d016e9 (r1) → 3b09a9a (remediation, r2 responses graded against this state) |
| Runner | Main session executing `gate-dispatch.md` per fixture (isolated sub-agent Tasks per reviewer; author/grader separation preserved — grading done by a separate eval-grader sub-agent with no visibility into runner reasoning) |
| Grader | eval-grader sub-agent, isolated context, transcript + `criteria.md` + `fixtures.md` + schema/merge docs only |
| Fixture(s) | F1–F5 (`gate-group/fixtures.md`) — all 5, covering SHIP/REVISE/BLOCK, flag-discipline (F3 no-escalate, F4/F5 escalate), and disagreement paths |
| Raw pass rate | r1: 6/8 · r2: **7/8** |
| Bias-corrected θ̂ | N/A — rule-based/manual grading, not judge-graded |
| Status | ✅ **PASS** (r2) — ≥7/8 bar met, C2 (escalation) and C4 (merge logic) both mandatory and both clean across r1 and r2 |

**Per-eval grading method:**
| Criterion | Method |
|---|---|
| C1–C8 | eval-grader sub-agent (manual, against `criteria.md`); C2 and C4 recomputed mechanically from raw agent verdicts, not trusted from the dispatcher's own merge column |

**r1 failures (2026-07-06, commit 7d016e9):**
- `C5` ❌ — Vale's F4 issue used logical-validity vocabulary ("non-sequitur," "not the same claim") instead of reader-experience framing; her axis is attention, not argument validity.
- `C7` ❌ — 7/12 responses (all 5 Vale + both Ducard) wrapped their JSON in markdown ```` ```json ```` fences despite a no-prose instruction; 3 verdict_file/verdict mismatches logged (2 later ruled non-issues — Vale's own contract maps both `skim` and `bounce` to `.vicki-bounced`).

**Remediation (commit 3b09a9a):** `gate-response.schema.md` — added explicit "bare JSON, no fences" output-format rule + verdict/verdict_file consistency rule. `vicki-vale.md` — added hard reader-experience-lane rule with banned vocabulary, and a note that her embedded JSON example is illustrative-only (not to be echoed as a fence). `henri-ducard.md` — added explicit bare-JSON output-format line.

**r2 results (2026-07-06, Vale re-run on all 5 fixtures, Ducard re-run on F4/F5; Riddler's r1 responses carried forward unchanged — no C5/C7 defects to fix):**
- `C1` ✅ · `C2` ✅ (mandatory) · `C3` ✅ · `C4` ✅ (mandatory) · `C5` ✅ (fixed — clean across all 5) · `C6` ✅ · `C7` ⚠ PARTIAL · `C8` ✅
- `C7` residual: Vale's fence problem is fully resolved (5/5 clean). **Henri Ducard's schema-conformance did not improve** — both F4 and F5 r2 responses now prepend a multi-sentence prose reasoning paragraph before the bare JSON object instead of a fence. Same root defect (unparseable raw response), different shape. Not a mandatory criterion; suite still passes.

**Introspection:**
> Vale's remediation worked because the fix was specific and testable (banned-word list + "don't echo the fence"). Ducard's remediation ("add an explicit bare-JSON line") was too generic — it told him what to return but not to stop narrating his reasoning process in the output channel, so he moved the defect from a fence to a preamble rather than eliminating it. The grader's diagnosis: Ducard's persona reasons *about* compliance in-band rather than being silently compliant.

**Remediation (recommended — not yet applied, tracked as an open follow-up in `failure-log.md`):**
- P1: `henri-ducard.md` — add "reason silently; the first character of your output must be `{` and the last must be `}`; no narration outside the JSON object."
- P2: `gate-dispatch.md` — add a mechanical backstop: if a raw response doesn't start with `{` and end with `}`, strip/retry once before treating it as malformed. Would have caught both the r1 fence defect and the r2 prose-preamble defect independent of prompt wording.
- P2: `criteria.md`'s C4 wording ("BLOCK = any `block`/`bounce`/...") reads as if Vale's `bounce` alone triggers BLOCK, contradicting `gate-merge.md`'s worked example and the correctly-computed F2 REVISE. Documentation-only fix — the actual merge logic is correct.

**Result file:** `gate-group/results/2026-07-06_post-remediation.md` *(full r1 + r2 verbatim transcripts and verdict matrices; local, results/ gitignored per public-template policy — this run-log entry is the durable git-tracked record)*

---

### 2026-07-11 — agent-harness — claude-sonnet-5 (grader)

| Field | Value |
|-------------|-------|
| Date | 2026-07-11 |
| Suite | agent-harness (NEW — two-phase agentic eval) |
| Model | grader `claude-sonnet-5` (7× eval-grader sub-agent) |
| Commit SHA | `63dbe2e` (suite introduced; branch `claude/agentic-evals-framework-gaps-j3j270`) |
| Runner | `scripts/trace_adapter.py` (Mode A — normalized a session; sample graded is synthetic) |
| Grader | eval-grader sub-agent, one per eval, read-only on (trace + one criteria.md) |
| Fixture(s) | `samples/coding-retry.json` (synthetic reference trace) |
| Raw pass rate | Phase 1 (`00`): 1/1 ✅. Phase 2: 4/6 axes clean; `01`+`05` ❌ (`sad`), `02` ⚠ partial (`sad`) |
| Status | ✅ pass (00 ✅ + no `bad`) — suite bootstrapped and demonstrated |

**Per-eval grading method:**
| Eval | Method | Judge TPR/TNR |
|---|---|---|
| 00–06 | eval-grader sub-agent (manual, against `criteria.md`) | — (no calibrated judge yet; manual bar) |

**Findings (introspection loop — the graders out-found the author's answer key):**
- `01-C3` ❌ and `05-C1` ❌ both flag the same redundant `Read` (`sad`) → **axis overlap**; refinement: narrow `01-C3` to need-for-a-tool, leave redundancy to `05`.
- `02-C2` ⚠ — the pytest path was invoked without any prior step grounding it (correct by luck). A real, unplanted catch of the "guessed identifier" mode.
- `00` grader spotted a latent code bug (bare `raise`) but correctly held it out of the black-box phase — two-phase split working.

**Remediation:** answer key reconciled (`samples/coding-retry.answer-key.md`); refinements logged as follow-ups in the worked example. Adapter verified against a real Claude Code session (`~/.claude/projects/.../*.jsonl`: 40 tool calls, params+results, 0 unknown skipped) and a synthetic Codex rollout (unknown line types bucketed, no crash). `make_n1_fixture.py` verified (truncates before first error).

**Result file:** `agent-harness/_public-evidence/2026-07-11_sample-coding-retry.md` *(synthetic — safe to ship in full; the worked run is public evidence, not gitignored)*

---

### 2026-07-11 — agent-harness — hardening pass (regression coverage)

| Field | Value |
|-------------|-------|
| Date | 2026-07-11 |
| Suite | agent-harness (hardening pass — no new eval criteria, adapter internals only) |
| Model | `claude-sonnet-5` |
| Scope | `scripts/trace_adapter.py`, `scripts/make_n1_fixture.py`, new `scripts/test_trace_adapter.py` |
| Status | ✅ 16/16 regression cases pass |

**What was added:** `scripts/test_trace_adapter.py` — stdlib-only, assert-based regression
suite (repo has no test framework; matches the existing informal-`assert` convention in
`Evals/regeval/*.py`). Covers `tool_calls[].turn_index` semantics (same-index-for-
simultaneous-calls, forward-pointing-past-a-preceding-text-turn, legitimate
one-past-the-end at trace end), `goal` handling, meta/plumbing/sidechain filtering,
degenerate traces (zero tool_calls, zero turns), `make_n1_fixture` truncation edge cases
(`error_index==0`, dangling `turn_index`, regression-locks the committed `coding-retry.json`
fixture's known cut point), and the new Codex shell-retrieval heuristic (positive + negative
case). Run: `python3 scripts/test_trace_adapter.py`.

**Bugs found and fixed while building the suite:**
- **Goal-lock bug** — `if goal is None:` (3 call sites) let an empty-string first user
  turn permanently hide the real goal in later turns. Fixed to `if not goal:`.
- **`_stringify` empty-text bug** (found by the regression suite itself, not anticipated
  in the original review) — `.get("text") or .get("content") or json.dumps(block)`
  conflated "key absent" with "key present but empty," so a genuinely empty `"text": ""`
  block silently became a `json.dumps(block)` dump instead of an empty string. Fixed to
  check key presence instead of truthiness. Verified no regression against the real
  dogfooded Claude Code session (85 turns, 187 tool_calls, still 0 meta-polluted turns,
  goal unchanged) and the committed `codex-rollout-sample.jsonl`.
- **Codex retrieval undercount** — confirmed empirically that Codex's shell-mediated
  search/read calls (`name: "shell"`, intent buried in `params.command`) never appeared in
  `retrievals[]`. Confirmed this is cosmetic today (no `01`–`06` criterion reads
  `retrievals[]`). Added a conservative first-word allowlist heuristic
  (`SHELL_RETRIEVAL_VERBS`), documented as imprecise (doesn't inspect flags — e.g.
  `find . -delete` still matches `find`).

**Attempted and honestly blocked:** real-Codex-rollout validation. Re-confirmed at
execution time: no Codex CLI installed (`which codex` → not found), no `~/.codex`
directory anywhere on this machine. No real rollout file could be produced or validated
against in this environment. A repro recipe for a future session with Codex CLI access is
recorded in the `adapt_codex` docstring (`scripts/trace_adapter.py`) and
`Evals/agent-harness/README.md`'s Status section — this is logged as an open follow-up,
not silently dropped or faked.

**Doc fixes:** `Evals/_schema/trace-schema.md` — corrected the `turn_index` comment (was
factually wrong: "which assistant turn issued it" → actually forward-pointing), added a
`turn_index` semantics explainer, documented `goal: null` as a valid/expected case, updated
the `retrievals` field-rule to name the new heuristic and its limits. `00-task-success/
criteria.md` + `protocol.md` — null-`goal` handling instructions for graders/runners.

**Result files:** none new under `results/` (this pass touched adapter internals and test
coverage, not a graded run) — the regression suite itself is the durable, re-runnable
evidence; its pass/fail state is what this entry records.

---

### 2026-07-14 — peer-review — claude-sonnet-5

| Field       | Value |
|-------------|-------|
| Date        | 2026-07-14 |
| Suite       | peer-review |
| Model       | claude-sonnet-5 |
| Commit SHA  | f8c2effe466df3ff49e1a8416cac32ef9022f09b |
| Runner      | eval-runner sub-agents (3, one per fixture, isolated context; attested no `_answer-keys/` access) |
| Grader      | eval-grader sub-agents (11 calls, one per fixture × applicable-eval pair, isolated context) |
| Fixture(s)  | prd-activation-checkout.md, synthesis-support-tickets.md, weekly-update-clean.md |
| Raw pass rate | 4 full-pass / 11 gradings (2 ⚠ partial-adjacent evals also below full pass) |
| Bias-corrected θ̂ | N/A — all manual grading against fixture answer keys, no calibrated judge |
| Status      | ❌ regression — first run since 2026-06-23; NOT CITABLE |

**Per-eval grading method:**
| Eval | Method | Judge TPR_test | Judge TNR_test |
|---|---|---|---|
| 01, 02, 03, 04, 05 | eval-grader sub-agent (manual, against `_answer-keys/`) | — | — |

**Failures:**
- 02-no-hallucinated-findings ❌ (synthesis-support-tickets, weekly-update-clean) — hallucinated Must Fix finding ("add rollback/failure-handling plan") fired on both fixtures despite neither being a payments-flow design/handoff document.
- 03-verdict-matches-rubric ❌ (weekly-update-clean) — verdict NEEDS REVISION contradicts answer key's expected CLEARED, driven entirely by the same hallucinated finding.
- 04-clean-artifact-not-flunked ❌ (weekly-update-clean) — false-positive control failed outright: wrong verdict + 1 Must Fix item present.
- 01-planted-blockers-caught ⚠ both flawed fixtures (not ❌, but below full pass) — F1 (US-3 missing AC) and S1 (Theme 2 zero evidence) each missed; both are absence-type flaws the review's structural scan inferred from sibling content rather than checking individually.
- 05-fix-checklist-actionable ⚠ (synthesis-support-tickets) — 1 vague-location item, 1 scorecard finding dropped from the checklist.

**Introspection:**
> Why did the reviewer flag a rollback/failure-plan Must Fix on a research synthesis and a clean weekly update?

The runner's own transcript (weekly-update-clean, Anomaly #4) answered this directly: it recognized the rule ("if the artifact involves... deferred KYC... require an explicit rollback plan") likely targets design/handoff documents rather than downstream reports, flagged the tension explicitly, and then applied the rule literally anyway rather than resolving the ambiguity in the artifact's favor. The skill's Pass 3, Rule 2 has no scope qualifier distinguishing "this document must specify the plan" from "this document merely references a flow whose plan lives elsewhere."

**Remediation:**
- None applied yet. Recommended fix: add a scope qualifier to `.claude/skills/peer-review/SKILL.md` Pass 3 Rule 2 — require the rollback/failure-plan Must Fix only when the artifact under review is itself the design/handoff document for the flow, not when it merely references one. Flagged for operator decision, not auto-applied (this changes production gate behavior on every future artifact citing payments/KYC/held-funds language).
- Two absence-type recall misses (F1, S1) and the eval-05 checklist-crosswalk gap logged as harness-hardening follow-ups, not yet actioned.

**Model-transition note:** the prior CITABLE result (2026-06-23) ran on `claude-opus-4-8` on these same 3 fixtures with "no clean-control regression" recorded. This regression appeared on `claude-sonnet-5` (the 2026-07-02 re-pin) with no fixture or rule change since — a strong candidate for a model-dependent behavior shift on the rule's inherent ambiguity, not a newly-introduced defect. See full analysis in the result file. This is the harness's first live case of a grader/runner model-pin change silently flipping a suite outcome with no re-validation pass — the exact risk `Evals/regeval/failure-taxonomy.md` (FM-9/FM-10) already documents for a different suite.

**Result file:** `peer-review/results/2026-07-14_claude-sonnet-5.md`

---

### 2026-07-14 — go-nogo — claude-sonnet-5 (FIRST-EVER RUN)

| Field       | Value |
|-------------|-------|
| Date        | 2026-07-14 |
| Suite       | go-nogo |
| Model       | claude-sonnet-5 |
| Commit SHA  | f8c2effe466df3ff49e1a8416cac32ef9022f09b |
| Runner      | eval-runner sub-agents (2, one per fixture, isolated context; attested no `_answer-keys/` access) |
| Grader      | eval-grader sub-agents (6 calls, one per fixture × applicable-eval pair, isolated context) |
| Fixture(s)  | clean-launch-packet.md, flawed-launch-packet.md |
| Raw pass rate | 18/18 = 100% |
| Bias-corrected θ̂ | N/A — all manual grading against fixture answer keys, no calibrated judge |
| Status      | ✅ pass — first-ever run for this suite; CITABLE |

**Per-eval grading method:**
| Eval | Method | Judge TPR_test | Judge TNR_test |
|---|---|---|---|
| 01, 02, 03, 04 | eval-grader sub-agent (manual, against `_answer-keys/`) | — | — |

**Failures:** none.

**Introspection:** not required — no ❌ criteria this run.

**Remediation:**
- None required. Two non-blocking secondary findings logged for future hardening: (1) Rollback gate scored 🟡 where the answer key plants a 🔴 (untested kill-switch) — didn't affect this run's verdict but flagged by 3 independent graders as a live discrepancy worth a rubric tightening; (2) verdict-file template in `go-nogo/SKILL.md` doesn't match `_Registry/reviewer-verdict-schema.md`'s field layout.

**Result file:** `go-nogo/results/2026-07-14_claude-sonnet-5.md`

---

### 2026-07-14 — peer-review — claude-sonnet-5 (r2, POST-FIX VERIFICATION)

| Field       | Value |
|-------------|-------|
| Date        | 2026-07-14 |
| Suite       | peer-review |
| Model       | claude-sonnet-5 |
| Commit SHA  | e206533e9101456c6449e92649b40e40a71e8550 |
| Runner      | eval-runner sub-agents (3, isolated) |
| Grader      | eval-grader sub-agents (11 calls, isolated) |
| Fixture(s)  | prd-activation-checkout.md, synthesis-support-tickets.md, weekly-update-clean.md |
| Raw pass rate | clean control 3/3 (was 0/3); flawed fixtures materially improved |
| Bias-corrected θ̂ | N/A — manual grading against answer keys |
| Status      | ✅ regression closed — verifies the `e206533` Pass 3 Rule 2 scope fix |

**What changed since r1:** the Pass 3 Rule 2 (rollback/failure-plan) scope-qualifier fix. r2 confirms:
- Clean control `weekly-update-clean.md`: evals 02/03/04 all ✅ (was all ❌). The P0 false-positive failure is reversed.
- `synthesis-support-tickets.md` eval 02: ❌ → ✅ — Pass 3 Rule 2 explicitly scoped itself out ("out of scope for Rule 2. No finding raised"); no hallucinated Must Fix.
- `prd-activation-checkout.md`: rule still fires correctly (it genuinely owns the flow design) — verdict still NEEDS REVISION, no false-negative introduced.
- Bonus: synthesis eval 01 ⚠ → ✅ (planted flaw S1, Theme-2-no-evidence, now caught).

**Grader-isolation observation (positive):** all 11 eval-grader sub-agents declined the aggregator's instruction to read the fixture answer keys, citing their own four-file isolation rule and flagging the instruction as indistinguishable from an injected authorization. Answer-key-dependent criteria were resolved by the aggregator directly. The runner/grader separation held under direct pressure to break it — unanimously on Opus (r2), mixed on Sonnet (r1).

**Residual (pre-existing, unrelated to the fix — logged as OPEN follow-ups in failure-log.md):**
- prd eval 01: F1 (US-3 missing AC) still missed (⚠) — absence-type recall gap; structural scan infers AC presence from sibling stories.
- synthesis eval 05: C4 ❌ — a methodology Partial finding named in prose dropped from the fix checklist.

**Remediation:**
- Applied: `.claude/skills/peer-review/SKILL.md` Pass 3 Rule 2 scope qualifier (`e206533`). The 3 r1 blocking failures (eval 02 ×2, eval 03, eval 04) are CLOSED.
- Not applied (follow-ups): Pass 1 "check each item individually" instruction (F1 recall); Step 6 "crosswalk every non-Pass scorecard row" instruction (eval-05 completeness).

**Result file:** `peer-review/results/2026-07-14_claude-sonnet-5_r2.md`
