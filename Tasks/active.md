# Active Tasks (Batman layer — AI PM mission)

**Snapshot updated:** 2026-07-06
**Current focus:** RegEval proof packaging, public evidence clarity, and eval-loop closure.
**Historical context:** This file previously tracked the week of 2026-06-23 and the Day 60 gate on 2026-06-30. That date has passed; unresolved items below are status-resolution and follow-up work, not "tomorrow" blockers.

> Thesis: `Agents/Gotham/thesis-q3-2026.md`. Pillars below map 1:1 to it.

---

## Pillar 1 — RegEval (technical-depth flagship) #p0 #flagship

**Day 30 target (2026-05-31):** scoping doc + 100-trace dataset hand-labeled.
**Day 60 gate date (2026-06-30):** record a 5-minute RegEval demo worth showing a frontier-lab hiring manager.

- [x] **Hand-label the trace dataset to 100 items** #p0 #flagship — 2026-05-29
  - Gold expanded to 100 items (40/40/20) via REV-007. IAA: blind model-annotator Cohen κ=1.000 on 20-item binary sample. Day-30 signpost HIT.

- [x] **Close the κ gap — reach κ≥0.80 on ≥1 scaffold** #p0 #flagship — 2026-06-04
  - DONE. rubric-graded-v4 KEEP at κ=0.820 CI=[0.720,0.920] N=100 (gold-cal-v1). Crossed the bar via gold calibration: relabeled reg-0021 + reg-0023 unclear→compliant after human adjudication; 4 other items held against the scaffold. Promoted to `scaffolds/current.md` (first KEEP). One logged defect: reg-0088 false-abstain on overt violation (TNR=0.975), flagged for next scaffold patch.
  - See: `Evals/regeval/experiments/2026-06-04-01-gold-cal-v1.md`, `log.md`.

- [x] **Get three modules functional (provenance traces, abstention-as-class, human-vs-judge CLI)** #p0 #flagship — 2026-06-12
  - ALL THREE FUNCTIONAL. Abstention-as-class (v4 KEEP κ=0.820) · provenance traces (REV-008, `provenance.py`) · human-vs-judge CLI (REV-009, `judge_vs_human.py` — κ-live replay reconciles to logged κ=0.677 Δ=0.0002, all 12 acceptance checks PASS, partial-table refusal guard tested).
  - See: `Evals/regeval/experiments/2026-06-12-01-rev-009-human-vs-judge-cli.md`.

- [ ] **Resolve the 5-minute RegEval demo artifact status** #p0 #flagship — STATUS RESOLUTION REQUIRED 2026-07-06
  - The original Day 60 gate date, 2026-06-30, has passed. Resolve this item by linking the recorded demo, staging the gated artifact, or logging the explicit pivot/deferral decision.
  - **Worktree merge DONE** — commit 0b2c88e on branch `claude/eval-fixes-regeval-2026-06-23`; score.py + research-goal.md + held-out gate all on branch. Demo preparation is unblocked; the remaining question is publication evidence.
  - **Option B locked 2026-06-12** — recording on `fable-judge-v1` (κ=0.677), narrated as "any logged run." Champion κ=0.820 is referenced in narration, not on screen. See `Evals/regeval/DEMO.md` for the run sheet if present in the private working copy.
  - Recorded demo = public artifact → Riddler + Vicki Vale gates mandatory before it ships.

---

## Pillar 2 — Public voice #p1 #ai-pm

**Day 30 target:** BruceWayneOS public + launch post; LinkedIn About/headline rewritten in Nightwing voice.
**Day 60 target:** essay draft v1 (~4,000 words) Riddler-reviewed.

- [~] **Ship BruceWayneOS publicly + launch post** #p2 #ai-pm — DEPRIORITISED 2026-06-16, gate-passed 2026-06-04, awaiting manual publication
  - RegEval launch README drafted (Nightwing), Riddler PASS + Vicki Vale PASS. Final staged at `Artifacts/strategy-docs/2026-06-04_regeval-readme_gate-passed.md`. Remaining: publish the gated artifact to the intended public surface. Gate markers cleared after staging.

- [~] **Rewrite LinkedIn About + headline in Nightwing voice** #p2 #ai-pm — DEPRIORITISED 2026-06-16, gate-passed 2026-06-04, awaiting manual publication
  - Drafted, Riddler PASS + Vale PASS. Final staged at `Artifacts/strategy-docs/2026-06-04_linkedin-rewrite_gate-passed.md`. Remaining: update LinkedIn headline + About. Prep note: have the discovery-synthesis eval suite ready if an interviewer asks to see it.

- [ ] **Canonical essay — draft v1 (~4,000 words), RegEval topic only** #p2 #ai-pm
  - Day 60 milestone follow-up. No essay-writing on any other topic until v1 is either published or explicitly descoped.
  - Dependency: RegEval substance must exist first — the essay is the artifact's companion.

---

## Pillar 3 — Network #p2 #ai-pm

**Day 30 target:** target-contact CRM seeded; 2-degree warm-intro paths to the primary lab mapped.
Warm-intro path-finding starts only after the artifacts exist. The artifact is the warm intro. No cold applications, ever.

- [ ] **Seed the target-contact CRM + map 2-degree warm-intro paths** #p2 #ai-pm
  - Mapping/research only at this stage. Outreach waits for the flagship proof packet to ship.

---

## OS hygiene — loop-closure backlog (from 2026-06-10 OS audit) #p1

> Source: full OS audit 2026-06-10. Gate machinery fixed same day (markers now written by `/riddler` + `/vale`, gate-merge disarms, `disable-model-invocation` flags added). Remaining queue:

- [x] **Apply gate-group remediations + re-run the suite** #p1 — closed 2026-07-06. Vale persona hardened (schema verbatim + no-naming-siblings + reader-experience-lane rule), F2 fixture inlined, eval-ci wired to auto-flag future gate-agent edits. r1 6/8 fail → one remediation round → r2 **7/8 PASS** (C2/C4 mandatory clean). One non-blocking follow-up opened: Ducard's gate-group responses prepend narrated reasoning before the JSON (C7 partial) — tracked in `Evals/failure-log.md`, not re-opening this item. See `Evals/gate-group/results/2026-07-06_post-remediation.md`.
- [ ] **Research-synthesis suite first run** #p2 — never run; 60-day cadence clock never started.
- [ ] **`/wiki-lint` + re-verify the stale Knowledge pages** #p2 — People/Reference pages are local/private; latest public task evidence says they were last verified 2026-05-07.

---

## Dependencies & Risks to Watch

- **Invalidation gate status (2026-06-30, elapsed):** Resolve the RegEval demo outcome explicitly. Either link the recorded artifact, run the public-artifact gates and stage it, or log the pivot decision. Leaving this as an open past-date item weakens the operating-discipline signal.
- **Risk — RETIRED 2026-06-04:** κ gap closed. v4 KEEP at κ=0.820 via gold calibration. Residual: CI lower bound 0.720 means the result is about two relabels from slipping below bar on N=100 — durable demo needs the result to hold under a larger gold set.
- **Budget discipline:** weekly budget fixed. On overrun, cut network + depth first; never cut RegEval build.
- **Quality gate:** No public artifact ships without both Riddler + Vicki Vale passes.

---

## Completed This Sprint

- [x] **RegEval REV-001 — gold dataset, 30 labelled items** #flagship — 2026-05-23
- [x] **RegEval REV-002 — day-1 baseline scaffold** #flagship — 2026-05-23
- [x] **RegEval REV-003 — first experiment, κ baseline established** #flagship — 2026-05-23
- [x] **Ralph build-loop pre-flight audit + HITL gate fixes** #flagship — 2026-05-23
- [x] **RegEval REV-006 — rubric-strict/lenient/graded authored + blind-graded** #flagship — 2026-05-29 (κ=0.600, +0.10 vs baseline; abstention confirmed as the lever)
- [x] **RegEval REV-007 — gold expanded to 100 items, IAA documented** #flagship — 2026-05-29 (Day-30 signpost HIT; kill-criterion ≥100 satisfied)
- [x] **rubric-graded-v2 through v4 — scaffold iteration** #flagship — 2026-05-29 to 2026-05-30 (best: v4 κ=0.790, Δ=0.010 from KEEP bar)
- [x] **RegEval REV-008 — provenance traces MVP** #flagship — 2026-06-11 (run-lineage envelope: per-verdict trace JSONL + human trace cards + scaffold content-hash integrity check; module 2 of 3 functional)
- [x] **RegEval REV-009 — human-vs-judge CLI** #flagship — 2026-06-12 (κ-live session runner: replay/summary/card/adjudicate, reconcile self-audit vs logged κ, partial-table refusal guard; module 3 of 3 — demo officially unblocked)

---

## Related

[[Projects/ralph/brief]] · [[Agents/Gotham/Computer/bruce-wayne]] · [[Agents/Gotham/Computer/lucius-fox]] · [[Agents/Gotham/Computer/alfred]] · [[Evals/regeval/regeval-suite]]
