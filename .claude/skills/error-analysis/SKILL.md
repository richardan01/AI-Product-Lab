---
name: error-analysis
description: Open code + axial code real captured traces to surface failure modes before writing or revising evals. Trigger on "open code these traces", "what's failing in real use", "error analysis on <suite>", "axial coding", or "find failure modes". Implements Hamel & Shankar Ch. 3 verbatim — the Analyze phase of the Analyze-Measure-Improve lifecycle.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

# /error-analysis — Find failure modes from real traces

This skill turns a pile of captured traces into a named failure-mode taxonomy. It is the missing **Analyze** step in AIPM-OS's eval discipline. Without it, every eval is designed top-down against imagined failures.

## When to run
- After `trace-collector` has accumulated ≥ 20 real traces for a suite
- Before writing a new eval suite from scratch
- Before adding new criteria to an existing suite
- When eval pass rates are inexplicably high (suspect the suite is missing real failure modes)
- After a model upgrade (new failure modes may have emerged)

## Inputs
- `<suite>`: which suite's traces to analyze (e.g. `gate-group`, `regeval`, `research-synthesis`)
- Source: `Evals/<suite>/_traces/traces.csv` and the trace files it references

## The procedure (Hamel Ch. 3)

### Step 1: Sample
Read `Evals/<suite>/_traces/traces.csv`. If fewer than 20 unlabeled real traces exist, stop and tell the user to capture more via `trace-collector` first. Otherwise, select a sample of 20–30 traces. Prefer unlabeled rows (`labeled = no`). If the sample is mixed in length, take a stratified mix (some short, some long).

### Step 2: Open coding (no taxonomy)
For each trace, read it in full. Write a **free-text observation** of what went wrong — one to three sentences. Do not borrow categories. Do not consult any existing failure-mode list. Each observation should be specific to what you saw, e.g.:

- ✅ "Assistant invented a 60-day outcome (`Ship the v2 launch`) even though the user said they were unsure of OKR alignment."
- ✅ "Phase 8 enumerated 4 files but assistant wrote 5 — added a `Knowledge/People/manager.md` that wasn't in the plan."
- ❌ "Hallucination." (too generic — don't do this)
- ❌ "Verbosity." (borrowed taxonomy — don't do this)

If a trace shows no failure, mark it `no-failure-observed` and move on.

Write observations into `Evals/<suite>/_traces/open-coding-<YYYY-MM-DD>.md` with one row per trace:

```markdown
## <trace_id>
**File:** <path>
**Observation:** <one to three sentences>
```

### Step 3: Axial coding (cluster into named failure modes)
Once all observations are written, group them. Look for shared patterns. Each cluster becomes a **named failure mode** with:
- A short, specific label (e.g. `phase-8-file-count-mismatch`, not `bug`)
- A one-paragraph description
- The list of `trace_id`s that exemplify it

Aim for 5–10 named failure modes total per analysis pass. If you have more, you're under-clustering. If fewer than 3, you're over-clustering.

Write to `Evals/<suite>/_traces/axial-coding-<YYYY-MM-DD>.md`:

```markdown
# Axial coding — <suite> — <date>

## Failure mode: <label>
**Description:** <one paragraph>
**Trace IDs:** trace-id-1, trace-id-2, ...
**Frequency:** N / total
**Provisional classification:** Specification Failure | Generalization Failure | (mark "unsure")
```

### Step 4: Theoretical saturation check
After clustering, ask: am I still seeing new failure modes in each new trace, or are new traces falling into existing clusters? If still seeing new modes → sample more traces. If new traces fall into existing clusters → saturated, move on.

Document the saturation decision in the axial-coding file:
```markdown
## Saturation
- Sample size: <n>
- New failure modes in last 5 traces: <count>
- Decision: saturated | need more traces
```

### Step 5: Update the suite README
Append findings to `Evals/<suite>/README.md` under a "Failure modes observed (from error analysis)" section. For each failure mode:

- If a corresponding eval exists, link it.
- If no eval exists, propose one (just the name + one-line scope; full eval design is `/evals`'s job).
- If the failure mode is a Specification Failure (root cause is ambiguous prompt), propose a workflow edit instead and link the relevant `Workflows/*.md` or skill file.

### Step 6: Propose eval changes
Output a short proposal to the user, NOT auto-applied:

```markdown
## Proposed eval suite changes (from <date> error analysis)

**Add evals (Generalization Failures not currently covered):**
- <eval-name> — covers <failure mode>

**Retire evals (no real traces show this failure mode in <N> samples):**
- <eval-id> — <one-line reason>

**Workflow edits instead of evals (Specification Failures):**
- <workflow file> — <one-line fix>
```

Wait for the user's "go" before editing any other file.

### Step 7: Mark traces as coded
Update the CSV: for each trace included in this pass, fill `open_code_notes` with the one-line observation and `failure_modes_observed` with the cluster label(s). Leave `labeled` as `no` (this is open coding, not judge calibration labeling).

## Hard rules
- Do NOT read existing eval criteria or sample-pass/fail files during open coding. They will bias the categories you invent.
- Do NOT borrow taxonomies from outside AIPM-OS (no "hallucination/verbosity/refusal" lists).
- Do NOT label or judge fix priorities during open coding. Saturation first, then planning.
- A pass that produces zero failure modes is a valid result — write it up as "no failures observed in N traces" and propose making the suite harder, not easier.

## Output
Two files written to `Evals/<suite>/_traces/`:
1. `open-coding-<date>.md` (per-trace observations)
2. `axial-coding-<date>.md` (clusters)

Plus a short summary to the user with the proposed eval changes from Step 6.

## References
- Hamel & Shankar, Ch. 3 (`Application-Centric AI Evals for Engineers and Technical PMs`)
- The Analyze phase of Analyze-Measure-Improve (lifecycle in `/evals` skill)
- `trace-collector` agent — upstream dependency
