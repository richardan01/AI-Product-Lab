---
name: evals
description: >
  Design, run, and iterate on eval suites for the AIPM-OS portfolio lab.
  Trigger whenever the operator asks to write evals, test a skill, benchmark a workflow,
  measure model+harness quality, build pass criteria, run regression tests after
  a model release, or quantify whether an automation is "100% there" (Cat Wu's
  bar). Also trigger on phrases like "is this skill working", "test my prompt",
  "what should the success criteria be", "did this regress", "model upgrade
  audit", "harness check", "introspection loop". Use broadly — eval discipline
  is the core AI PM craft and applies to discovery synthesis, tracking plan
  validation, vendor briefs, segmentation frameworks, classification tasks,
  and any repeatable AI workflow being hardened toward 100% reliability.
---

# Evals Skill — AIPM-OS portfolio lab edition

## Purpose

This skill encodes the lab's eval discipline. It exists because:

> **"You don't need to build hundreds of evals for them to be useful. Just
> building 10 great evals is important for helping the team quantify what the
> goal is and what their progress towards it is."** — Cat Wu, Anthropic

Evals are how this lab proves — to its operator and to anyone inspecting the
repo — that its AI-augmented workflows actually work. Not "feel like they
work." **Quantitatively work.**

---

## Step 0: Error Analysis (Before Writing Any Eval)

**Do this before writing a single eval.** Error analysis finds the failure
patterns your evals should target. Skipping this produces evals that miss the
real problems.

### How to do Error Analysis

1. **Collect Traces**: Gather a diverse sample of 100+ traces from production
   or your own real/synthetic usage.
2. **Annotate Traces (Open Coding)**: Review each trace and write brief,
   unstructured notes on the problem (e.g., "hallucinated a fact", "misread
   the user's name", "failed to use the calculator tool").
3. **Group & Categorize (Axial Coding)**: Group similar notes into clusters
   (e.g., tone violation, failed tool call, missing field).
4. **Prioritize**: Count the frequency of each category — this informs your
   eval priority order.

Keep looking at data until you reach **theoretical saturation**: you stop
seeing new failure modes and re-coding no longer changes your categories.
As a rule of thumb, you need ~100 high-quality, diverse traces.

> ❌ **Anti-pattern**: Building evals before doing error analysis. Your evals
> should target errors you've actually observed or can induce — not errors
> you imagine might exist.

---

## Step 1: Decide Whether to Write an Eval

**You don't always need to write an eval.** Use this decision tree:

```
Have you observed the failure with error analysis?
│
├─ NO → Stay Away. Do error analysis first.
│
└─ YES → How much iteration is required to fix?
          │
          ├─ LITTLE → Unclear Value
          │            Consider: Can a code-based assertion work?
          │            Does it make sense to just fix and move on?
          │
          └─ LOTS → High Value ✅
                     Evals are most valuable here. Expensive evals
                     like LLM-as-a-judge might be feasible.
```

Evals provide the most value when you need to **hill climb against an error**
through many iterations. If you can fix it in one go and move on, the overhead
of a formal eval suite may not pay off.

---

## Core Principles (Cat Wu Doctrine)

1. **10 great evals > 100 mediocre evals.** Don't over-engineer. Cap each suite at ~10.
2. **Pass criteria, not exact-match.** AI outputs vary; grade against criteria, not strings.
3. **Test the harness, not the model.** Each fail teaches you what to change in the skill/prompt.
4. **Introspection loop is mandatory.** When an eval fails, ask Claude *why* before fixing.
5. **Trusted-5 humans complement evals.** Evals catch regressions; humans catch vibes.
6. **Build for next month's model.** Some evals should fail today and pass on the next Opus release — that's the AGI-pilled prototype.
7. **100% or it's not an automation.** A 9/10 pass rate means one bug in production. Keep iterating.

---

## Types of Automated Evals

Not all evals are equal. Use the cheapest type that covers the failure:

**Type 1 — Code-Based Assertions** (default choice)
Check for objective, rule-based failures: matching keywords, confirming tool
execution, verifying field presence. Use these whenever possible — they are
fast, cheap, deterministic, and interpretable.

**Type 2 — LLM-as-a-Judge**
Uses an LLM to assess subjective or nuanced criteria that code can't handle.
Powerful, but slower, more expensive, and requires calibration against human
labels (see LLM Judge section below). Reserve for important failures only.

**Type 3 — Guardrails**
Run synchronously in the request/response path to block failures before they
reach the user. Fast, low false-positive rate. Commonly code-based checks or
small classifiers. These prevent bad outputs from shipping, not just detecting
them after the fact.

---

## Eval Metric Standards

### Use Binary Scores, Not Likert Scales

Binary (pass/fail) scores are required. Do **not** use 1–5 rating scales.

Why: Likert scales are expensive to align with domain experts, annotators
default to middle values to avoid hard decisions, and they encourage overall
quality scores instead of targeted evals. Binary scores compel a definitive
decision — which aligns with the real question: is this good enough to ship?

```
❌ Don't do this:
  LLM Output → Likert Scale Judge → Score: 3/5

✅ Do this instead:
  LLM Output → is_specific_to_context? → Pass/Fail
             → fields_all_present?    → Pass/Fail
             → no_hallucinated_tools? → Pass/Fail
```

### Use Application-Specific Metrics, Not Generic Ones

Good eval metrics:
- Measure an **error you've observed**
- Relate to a **non-trivial issue** you will iterate on
- Are scoped to a **specific failure**
- Have a **binary outcome** (not a 1–5 score)
- Are **verifiable** (human labels for LLM-as-a-Judge)

```
❌ Generic (avoid):          ✅ Application-specific (use):
  Rouge                        Feature Definition Drift
  Bleu                         Missing User Onboarding Stage
  Faithfulness                 Region-Specific Feature Fit
  Helpfulness                  Event Taxonomy Consistency
  Tone                         Vendor Brief Missing Comparison Column
```

---

## How to Design Each Eval

Every eval has four sections. Keep each tight.

### 1. Input
The fixture or input pattern. Either inline or referenced from `inputs/`.

### 2. Output Spec
What format the output should take. E.g., "a markdown table with columns:
Tool, Category, Owner" or "a 3-bullet list of next actions."

### 3. Pass Criteria
Concrete, gradable conditions. Aim for 3–6 criteria per eval. Each should be
binary-ish (yes/no with a brief judgment call).

Good criteria:
- ✅ "All tools mentioned in transcript appear in output"
- ✅ "No tools added that weren't in transcript"
- ✅ "Each tool is categorized as exactly one of: CRM / engagement / data / comms"

Bad criteria:
- ❌ "Output is high quality" (not gradable)
- ❌ "Captures the essence" (subjective without anchor)

### 4. Failure Modes to Catch
The specific bad behaviors this eval is designed to surface. Naming them
explicitly makes the eval more useful as a debugging tool, not just a grade.

---

## Building Your Test Data

### Option A: Traces from Production

Use production traces as the most reliable source of real failure patterns.

**How to sample traces:**

| Mode | Method | When to use |
|------|--------|-------------|
| Explore | **Random** sampling | Always do this alongside other strategies to discover unknown issues |
| Explore | **Clustering** | Group traces by semantic similarity to surface new error clusters |
| Explore | **Data Analysis** | Analyze latency, turns, tool calls, tokens for statistical outliers |
| Explore | **Classification** | Use existing evals or LLM to surface problematic traces (use with caution) |
| Use Signals | **Customer Feedback** | Filter traces using explicit thumbs down / complaint signals |

**Traces for Evals — the N-1 Protocol:**
1. Start with error analysis. When reviewing traces, stop at the **first (most
   upstream) error** you find — upstream failures tend to be more important.
2. For your top failures, **minimally reproduce the failure in as few turns
   with as least complexity as possible**.
3. **N-1**: Collect a dataset of minimally reproduced error traces and use
   the N-1 turns before the error as test cases.
4. Advanced: Modify traces from step 3 in valid ways (rephrasing the user
   question, etc.) using an LLM for additional coverage.
5. Advanced: Simulate a user with another LLM (challenging to do well).

### Option B: Synthetic Data (When You Don't Have Traces Yet)

Use this to bootstrap evals before a workflow has accumulated real traces.

**How to generate good synthetic data:**
- **Use structured input for diversity**: Define key dimensions (e.g., Feature,
  User Persona, Region, Scenario) and use them as variables in your
  generation prompt.
- **Seed with real logs or traces when possible**: Then ask the model to inject
  changes (new constraint, modified variable) to create realistic edge cases.
- **Enforce output structure & filter**: Define a schema for the output.
  Generate many candidates, then filter to retain the highest-quality,
  challenging examples.
- **Increase complexity iteratively**: Start with simple queries, then
  incrementally ask the LLM to add constraints, complex formatting, etc.

> ❌ **Don't**: Prompt zero-shot — "Generate 50 test cases". This yields
> generic, repetitive inputs that won't surface real failure modes.

---

## Eval Suite Anatomy

```
suite-name/
├── README.md                    # Overview, run protocol, pass-rate log
├── inputs/                      # Reusable input fixtures (transcripts, briefs)
│   └── <fixture>.md
├── 01-<eval-name>/
│   ├── input.md                 # The actual or referenced input
│   ├── criteria.md              # Pass criteria + failure modes
│   └── sample-pass.md           # (optional) Example of a passing output
├── 02-<eval-name>/
│   └── ...
└── results/                     # Run logs over time (date-stamped)
    └── 2026-04-25_opus-4-7.md
```

**Why this structure**: criteria files travel with inputs so anyone (or any
Claude) can pick up the suite and run it. Results history tracks
drift across model releases.

---

## Run Protocol

When asked to run an eval suite, this skill orchestrates **two dedicated sub-agents** to enforce author/grader separation architecturally rather than by convention:

- **`eval-runner`** sub-agent — runs each fixture through the workflow, captures verbatim transcripts. Never reads the criteria. Blocks (synchronous) so transcripts are visible before grading starts.
- **`eval-grader`** sub-agent — reads only (transcript + criteria + sample-pass/fail). Returns structured JSON verdict per eval. Runs in the background, one per (transcript × eval) pair.

### Orchestration sequence

1. **Read the suite README** for context (use case, last run date, last pass rate).
2. **Pin the run inputs** — model ID, `git rev-parse HEAD` for commit SHA, list of fixtures to use, list of evals in the suite.
3. **Fan-out runner agents** — one `eval-runner` per fixture, **blocking**. Each writes its transcript to `Evals/<suite>/results/transcripts/<date>_<fixture>_<model>.md` and returns the path. Wait for all transcripts before grading.
4. **Fan-out grader agents** — for each (transcript, eval) pair, launch an `eval-grader` sub-agent with `run_in_background: true`. Each grader returns structured JSON when it finishes. Do NOT poll — wait for completion notifications.
5. **Aggregate** — once all graders return, collect per-eval ✅/❌/⚠ verdicts across fixtures. For each judge-graded eval, look up the judge's `tpr_test` and `tnr_test` from `judge-prompt.md` and compute bias-corrected θ̂.
6. **Introspection on failures** — for each ❌, ask the original runner's model *why* it produced what it did. Capture the answer.
7. **Log the run** in `results/YYYY-MM-DD_<model>.md` with the schema below.
8. **Update `Evals/run-log.md`** with the summary row.
9. **Clear pending re-runs** — call `/eval-ci clear <suite>` to mark any pending rows resolved by this run.

### Result file schema (extended)

`Evals/<suite>/results/YYYY-MM-DD_<model>.md`:
```markdown
# Eval run — <suite> — <date>

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Suite | <suite> |
| Model | <model> |
| Commit SHA | <sha> |
| Runner | eval-runner sub-agent |
| Grader | eval-grader sub-agent |
| Fixtures | <list> |

## Per-eval results

| Eval | Fixture A | Fixture B | Fixture C | Raw pass | TPR_test | TNR_test | θ̂ (corrected) | 95% CI |
|---|---|---|---|---|---|---|---|---|
| 01 | ✅ | ✅ | ❌ | 2/3 | — | — | — (manual-graded) | — |
| 04 | ✅ | ✅ | ✅ | 3/3 | — | — | — (programmatic) | — |
| 05 | ✅ | ❌ | ⚠ | 1/3 | 0.92 | 0.88 | (0.33 + 0.88 - 1) / (0.92 + 0.88 - 1) = 0.26 | [..., ...] |

## Introspection findings
- Eval 05 / fixture B ❌: model said "I assumed 30-day outcome was a placeholder, so I generated a typical activation-PM outcome." → harness fix: tighten Phase 5 prompt to forbid generation when user input is "I don't know yet."

## Recommended harness changes
- ...
```

### Bias-corrected success rate (Hamel §5.6)

For any eval graded by an LLM judge:
```
θ̂ = (p_obs + TNR_test - 1) / (TPR_test + TNR_test - 1)
```
Where `p_obs` is the raw judge pass rate (k passes out of N graded), and TPR/TNR come from the judge's most recent `_calibration/<date>_final.md`. Report θ̂ alongside the raw rate. The corrected rate is the citable number for judge-graded evals.

For manually-graded evals (no judge): the raw rate IS the unbiased estimate. Leave the TPR/TNR/θ̂ cells blank.

For programmatic (code-based) evals: same — raw rate is unbiased.

### Hybrid execution rationale
Runner blocks because the transcript is needed for grading and the user wants immediate visibility into what the workflow actually did. Grader is parallelized in the background because it's read-only and many can run at once — a 12-eval × 3-fixture suite produces 36 grader calls.

---

## How to Grade Outputs

Don't be a pushover, don't be a perfectionist. Three rules:

- **Concrete > vibes.** If a criterion says "captures all 4 fields," count to 4.
- **Reading the transcript first matters.** You can't grade hallucination if you don't know what was in the input.
- **Partial credit is fine, but tracked separately.** A ⚠️ partial isn't a ✅. Don't round up.

When grading subjective criteria ("specific to this context, not generic"),
ask: *would this output be different if the input were a generic SaaS company
discovery session?* If no, it's not specific enough.

---

## Introspection Loop (The AI PM Move)

This is the highest-leverage habit in the suite. After any eval failure:

1. Show the model its own output
2. Show it the criterion it missed
3. Ask: *"Why did you produce this output? What in your context led to this decision?"*

The model will often surface the actual harness bug — a confusing line in the
skill, a missing piece of context, a misinterpreted instruction. **That's the
fix.** Apply it, re-run the eval, verify it passes.

Cat Wu's exact framing: *"A lot of times just being very curious about why
the model made the decision that it did will show you what misled it so that
you can fix the harness in order to close this gap."*

---

## How to Trust an LLM Judge

The **only** way to trust an LLM Judge is to measure it against human labels.

**Setup:**
Split your human-labeled data into 3 sets:
- **Train (~20%)**: Draw your few-shot examples from here
- **Dev (~40%)**: Hill climb against this set to optimize the judge prompt
- **Test (~40%)**: Final check to make sure you haven't overfit

**Metrics to use:**
Do **not** report "accuracy" — it's misleading on imbalanced data.
Use **True Positive Rate (TPR)** and **True Negative Rate (TNR)**. Aim for >90% on both.

```
TPR = TP / (TP + FN)   →  proportion of actual errors correctly identified
TNR = TN / (TN + FP)   →  proportion of non-errors correctly dismissed
```

**The workflow:**
1. Label ~100 examples by hand
2. Select few-shot examples for your judge prompt from Train
3. Iterate the judge prompt against Dev until TPR & TNR ≥ 90%
4. Run a final check against Test — if it drops, you overfit; go back to Dev

---

## Transition Matrix: Finding Failure Hotspots in Multi-Step Agents

When a skill or agent has many steps (e.g., Plan → Search → Synthesize → Format),
it's hard to know which step is failing most. A **Transition Failure Matrix**
finds the hotspots.

**How it works:**

1. **Define states**: List all the possible steps or states your agent can be in
   (e.g., for discovery synthesis: ParseInput → IdentifyThemes → ExtractEvidence → Format → Output)
2. **Create a matrix**: Rows = "From State", Columns = "Failure Occurred In State"
3. **Count failures**: For each failure, identify the last successful state
   before the error. Populate the count in the corresponding cell.

High numbers on the diagonal = the step is failing in itself.
High numbers off-diagonal = upstream context is corrupting a downstream step.

**Example for a discovery-synthesis agent:**

| From State → | ParseInput | IdentifyThemes | ExtractEvidence | Format | Output |
|---|---|---|---|---|---|
| ParseInput | 0 | 3 | 0 | 0 | 0 |
| IdentifyThemes | 0 | 0 | 4 | 0 | 0 |
| ExtractEvidence | 0 | 0 | 0 | 6 | 0 |
| Format | 0 | 0 | 0 | 0 | 7 |

This view quickly surfaces whether failures cluster in a specific transition,
so you fix the right thing.

---

## Deploying Evals (CI/CD, Online Monitoring, Guardrails)

Offline evals catch problems during development. Deploy evals to protect
production users. Three deployment modes:

| | CI/CD | Online Monitoring | Guardrails |
|---|---|---|---|
| **Goal** | Prevent regressions | Discover new failures & track performance | Enforce safety & block high-impact errors |
| **When** | Pre-merge (pull request) | Async (post-response) | Synchronous (pre-response) |
| **How** | Unit tests, LLM-judge | Unit tests, LLM-judge, A/B testing | Unit tests, small classifiers |
| **Data** | Curated test cases | Sampled production traffic | 100% of live traffic |
| **On failure** | Block merge | Trigger an alert | Block response, retry, or fallback to alternative |

**For AIPM-OS workflows:**
- **CI/CD**: Before pushing any skill update, run the full eval suite. A failed
  eval blocks the skill from being deployed to production prompts. This is what
  `/eval-ci` + `_pending-reruns.md` enforce — a mapped source-file edit blocks
  `/peer-review` and `/go-nogo` from citing a stale suite until it re-runs.
- **Online Monitoring** (operationalized — see `Evals/monitoring/README.md`):
  a **weekly loop**, hooked off `/weekly-update`. `trace-collector` (wired into
  `/eod`) samples 10–15 recent real artifacts → async `eval-grader` sub-agents
  grade them against the relevant suite's criteria + answer key (and the
  **deployed** eval-05 judge once calibrated), bucketing each finding `bad`/`sad`
  per `Evals/severity-taxonomy.md`. The headline metric is the **bad-rate**
  (fraction of samples with ≥1 `bad` finding) trended week over week — an
  outcome metric, not a volume count. Recurring `bad` findings feed
  `/error-analysis` and become new fixtures.
- **Guardrails**: A true synchronous pre-response guardrail is not possible in a
  markdown OS with no runtime. The practical equivalent is the **pre-ship gate**
  (`/peer-review`, `/prd-readiness`, `/go-nogo`) made *graded* (its own meta-eval
  suite) and *severity-aware* (any `bad` finding blocks; see the taxonomy). State
  this honestly rather than claiming a real-time blocker.

---

## Common AI Eval Mistakes

1. **Skipping data and traces, jumping straight to auto-eval magic.**
   An automated eval is useless if it doesn't measure your specific failures.
   The best way to find those is to look at your data first. Off-the-shelf
   metrics like "Helpfulness score" are a bad idea for this reason.

2. **Using an LLM Judge without validating it against human labels.**
   Not doing so creates an untrustworthy, misaligned metric. You'll be
   optimizing against the judge's biases, not your actual quality bar.

3. **Declaring a suite done when it hits 100%.**
   A perfect score often means the suite is saturated or too easy. Add hard
   test cases to keep guiding improvement. Evals are most valuable when they
   find new failures.

---

## What Counts as "Done"

A suite is healthy when:
- Pass rate ≥ 9/10 on the current model
- At least 1 eval is "AGI-pilled" — fails today, expected to pass on next model
- Introspection findings have all been triaged (fixed, parked, or wontfix)
- Last run was less than 30 days ago OR right after a model release
- LLM judges (if used) have documented TPR/TNR ≥ 90% against human labels

A suite that hasn't been run in 60 days is technical debt.

---

## Communicating Results to Stakeholders

When sharing eval results with a non-eval audience (a reader, a hiring manager, a stakeholder):

- **Don't lead with the number.** Lead with what the suite tested and why it matters.
- **Frame regressions as caught risks**, not failures. "Eval suite caught a
  hallucination regression in vendor naming after the 4.7 release — fixed
  before it hit any deliverable."
- **Tie pass rate to business impact** when possible. "9/10 pass rate on
  discovery synthesis means roughly 1 in 10 sessions needs manual rework —
  down from 4 in 10 before the harness changes."

---

## Active suites in this lab

| Suite | Use Case | Where |
|-------|----------|-------|
| `regeval` | Flagship — LLM-as-judge vs human gold on regulated-domain compliance (Cohen's κ) | `Evals/regeval/` — see `regeval-suite.md` + `experiments/log.md` |
| `gate-group` | Meta-eval: does the Riddler+Vale gate pipeline hit the designed verdict paths? | `Evals/gate-group/` |
| `peer-review` | Meta-eval: does the reviewer gate catch planted flaws? | `Evals/peer-review/` |
| `prd-readiness` / `go-nogo` / `build-review` / `research-sufficiency` | Meta-evals for the remaining gates | `Evals/<suite>/` |
| `onboarding` | Interactive onboarding workflow → coherent config | `Evals/onboarding/` |
| `research-synthesis` | Interview corpus → synthesis doc | `Evals/research-synthesis/` |
| `memory-consolidation` | Monthly memory audit quality | `Evals/memory-consolidation/` |

Run history and citability status: `Evals/run-log.md`. Staleness: `Evals/_pending-reruns.md`.

## Related skills and agents

| When | Use |
|---|---|
| Before writing evals from scratch | `/error-analysis` — open code real traces first (Hamel Ch. 3) |
| To capture real traces | `trace-collector` sub-agent (wired into `/eod`) |
| To run an eval suite | This skill — orchestrates `eval-runner` + `eval-grader` sub-agents |
| To validate an LLM judge | `/judge-calibration` — TPR/TNR ≥ 0.9 on held-out test |
| When editing a mapped workflow/skill | `/eval-ci` — registers a pending re-run; blocks stale citations |
| Before citing a result publicly | `/eval-review` — methodology gate, P0/P1/P2 audit |

---

## Anti-Patterns (Things That Look Like Evals But Aren't)

- **Vibes-only review.** "I read the output and it seems fine" — not an eval.
- **Single example.** One transcript ≠ a suite. You need variation.
- **No failure mode named.** If you can't articulate what bad output looks like, the eval will let it through.
- **Identical inputs across evals.** Each eval should test something distinct.
- **Grading your own intent, not the criterion.** Easy trap when you're both author and grader.
- **Self-graded eval.** Author and grader are the same context — not an eval.
- **Generic metrics.** "Helpfulness: 3/5" tells you nothing actionable.
- **Likert scales.** Binary only. Make the hard call.
- **No LLM judge calibration.** If you use an LLM judge, measure it against human labels first.
- **Evals before error analysis.** Always look at traces before writing a single eval.

---

## The Bigger Move

Building this suite is the visible artifact of being an AI PM. When someone
asks "what makes you an AI PM?", the honest answer is: *"I run an eval
suite on every model release and I can show you the pass rate over time."*

That's not a job title. That's a practice.
