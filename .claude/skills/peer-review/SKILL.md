---
description: Quality gate — evaluate agent output against personal ground truth and agent-specific checks before sharing or handoff
disable-model-invocation: true
---

# Peer Review

**Agent:** Orchestrator (Alfred voice) — see `Agents/agent-system-architecture.md` voice map.

Evaluate any agent's output file against **two layers of quality standards**:
1. **Agent-specific checks** — the quality gates defined in the producing agent's agent file
2. **Personal ground truth** — [YOUR_NAME]'s 5 criteria in `Knowledge/Reference/ground-truth.md`

Run this before passing any output to the next agent in the chain, and before sharing anything externally with [YOUR_MANAGER], [HEAD_OF_DEPT], or the broader team.

Usage: `peer-review [file path]`
Example: `peer-review Projects/[YOUR_ANCHOR_PROJECT]/vendor-scorecard.md`

---

## Step 0 — Eval Staleness Check

If the target file cites an eval suite's pass rate or result (e.g. "onboarding suite: 10/12", "gate-group PASS"), invoke `/eval-ci check <suite>` for each suite cited. If any returns `BLOCK`, do not proceed to Step 1 — return a Conditional Pass with the required fix: "Re-run `<suite>` via `/evals` before this artifact can ship (stale since `<source file>` changed, SHA `<sha>`)." If all cited suites return `OK` (or no suite is cited), proceed.

## Step 1 — Read the Target File

Read the file the user specified. Identify:
- What type of document it is (PRD, research synthesis, strategy, proposal, business case, etc.)
- Which agent produced it (infer from file path, structure, or content)
- Whether it is intended for internal use or external sharing ([YOUR_MANAGER], [HEAD_OF_DEPT], engineering)

---

## Step 2 — Check for External Reviewer Comments

Before scoring, scan the conversation and the document itself for evidence of prior reviewer feedback:
- Has the user mentioned [YOUR_MANAGER], [HEAD_OF_DEPT], or any named reviewer?
- Has the user pasted comments, markup, or a review note alongside the file?
- Does the document contain a comments section, tracked changes, or explicit "Reviewer notes"?

If yes: extract all comments into a numbered list. Evaluate each under Layer 2, Criterion 5.
If no: mark Criterion 5 as N/A.

---

## Step 3 — Layer 1: Agent-Specific Quality Checks

Identify the producing agent and read its quality checks from the appropriate agent file.

**Pass 1 — Structural scan**
Check the document type against `Knowledge/Reference/ground-truth.md` → "Document-Type Templates" to find the required sections for that type. List each required section and mark it as present, partial, or missing. Flag any placeholders (TBD, TODO, insert here).

**Pass 2 — Agent quality check**
Score each quality check from the producing agent's file:

```
**Layer 1 — Agent Quality Checks ([Agent Name])**

| Check | Status | Evidence / Gap |
|-------|--------|----------------|
| [check from agent file] | ✅ Pass / ❌ Fail / ? Cannot Assess | [specific finding] |

Layer 1 Score: [n Pass] / [n total checks]
```

**Pass 3 — Cross-cutting risk checks** (apply to every artifact, regardless of producing agent — these catch the flaws whole-document reasoning misses):

1. **Cross-section consistency.** Scan for claims that must agree across sections and verify they do — dates/timelines (e.g. an exec summary "GA Q3" vs a timeline "GA 2026-10-30 / Q4"), quantities and denominators (e.g. "412 tickets" in one place, "380" in another), metrics vs targets, and capability claims vs scope. Any contradiction between two sections is a **Must Fix** — name both locations and the conflicting values. This is distinct from a single vague claim; it is two statements that cannot both be true.
2. **Rollback / failure plan for high-risk flows.** First check scope: does *this artifact* need to specify the rollback/failure-handling plan, or does it just need to point at where that plan lives (a separately-cited design/handoff document that owns the flow)? Only design/handoff artifacts (PRDs, technical design docs, runbooks) that introduce or define a high-risk flow — payments, held or escrowed funds, money movement, auth/identity, deferred KYC, irreversible deletes, or data migration — are in scope. A status update, synthesis, or other artifact that merely *references* a high-risk flow whose design is owned elsewhere is out of scope for this rule, even if it names the same risk keywords. For in-scope artifacts, require an explicit rollback / failure-handling / recovery plan; its absence is a **Must Fix** — a high-risk flow with no failure plan is not handoff-ready, regardless of how complete the happy path is.

Record any Pass-3 finding in the Fix Checklist at the severity stated above; these feed the verdict like any other Layer-1 Fail.

---

## Step 4 — Layer 2: Personal Ground Truth

Read `Knowledge/Reference/ground-truth.md`. Apply all 5 criteria to the document regardless of type.

```
**Layer 2 — Personal Ground Truth**

| # | Criterion | Score | Finding |
|---|-----------|-------|---------|
| 1 | Structure & Completeness | ✅ Pass / ⚠️ Partial / ❌ Fail | [specific finding] |
| 2 | Clarity & Writing Quality | ✅ Pass / ⚠️ Partial / ❌ Fail | [specific finding] |
| 3 | Strategic Alignment ([YOUR_COMPANY]) | ✅ Pass / ⚠️ Partial / ❌ Fail | [specific finding] |
| 4 | Actionability | ✅ Pass / ⚠️ Partial / ❌ Fail | [specific finding] |
| 5 | External Reviewer Comments | ✅ Pass / ⚠️ Partial / ❌ Fail / ⏭️ N/A | [finding or "N/A — no reviewer comments detected"] |

Layer 2 Score: [n Pass] / 5 criteria
```

---

## Step 5 — Overall Verdict

```
**Overall Verdict: CLEARED ✅ / CONDITIONAL ⚠️ / NEEDS REVISION ❌**
```

Rules:
- **CLEARED** — all Layer 1 checks pass AND all Layer 2 criteria are Pass or N/A
- **CONDITIONAL** — 1–2 items are Partial across both layers, none are Fail
- **NEEDS REVISION** — any item is Fail, or 3+ items are Partial across both layers

---

## Step 6 — Fix Checklist

List every gap as a checkbox, grouped by severity.

```
**🔧 Fix Checklist**

### Must Fix (Blocking)
- [ ] [L2 · Criterion 3] Tie metric to specific [YOUR_COMPANY] context — Section 2 is generic.

### Should Fix (Important — fix before external sharing)
- [ ] [L2 · Criterion 4] Assign owner to open action — Section 3.

### Nice to Fix (Minor — polish)
- [ ] [L2 · Criterion 2] Remove filler phrase — Executive Summary, line 1.
```

---

## Step 7 — Revised Version (if needed)

If verdict is NEEDS REVISION or CONDITIONAL, produce a corrected version applying all Must Fix and Should Fix items.

---

## Step 8 — Outcome & Next Steps

```
**🎯 Outcome & Next Steps**

**Expected outcome after fixes:** [1–2 sentences]

**Your action sequence:**
1. [Highest-severity fix first]
2. [Next item]
```

---

## Verdict file (per `_Registry/reviewer-verdict-schema.md`)

On PASS (or CONDITIONAL-PASS), write `<doc-path>.peer-review-passed` with the byte-exact 4-line header + scorecard.
