# Online monitoring — sampled post-hoc grading of real outputs

This is the **achievable version** of "every response is evaluated against ground truth." Real-time grading is impossible in the OS (author/grader separation forbids grading in the authoring context). Instead, monitoring closes the loop *asynchronously*: sample real artifacts the OS produced, grade them in a fresh context, and feed the failures back into error analysis and new fixtures.

This is Fiona Fung's "monitor over more human review," and the third column of the `Deploying Evals` table in `.claude/skills/evals/SKILL.md` (CI/CD · **Online Monitoring** · Guardrails).

## The weekly loop

```
trace-collector (wired into /eod)  ──►  Evals/onboarding/_traces/ + real artifacts
        │
        ▼  (weekly, hooked off /weekly-update)
1. SAMPLE   take N=10–15 recent real artifacts (PRDs, syntheses, reviews, goals sections).
            Mix random + signal-based (anything the user reworked or flagged).
        │
        ▼
2. GRADE    async eval-grader sub-agents grade each sample against the relevant suite's
            criteria + answer-key (and the DEPLOYED judge for eval 05 once calibrated).
            Fresh context. Bucket each finding bad / sad per Evals/severity-taxonomy.md.
        │
        ▼
3. LOG      append a row per sample to Evals/monitoring/<YYYY-Www>.md (template below).
        │
        ▼
4. ANALYZE  run /error-analysis (open + axial coding) over the week's bad findings.
            New failure modes that recur become new fixtures in the relevant suite.
        │
        ▼
5. ESCALATE any bad-bucket trend (e.g., hallucinated findings rising) → register an
            eval re-run via /eval-ci and surface in the next /weekly-update.
```

## What this buys

- **Coverage of "every response"** — not by grading each one live, but by sampling the live stream so no failure mode hides for long.
- **New failures, not just regressions** — CI/CD catches known regressions; monitoring discovers the failure modes the curated suites never imagined (Cat Wu: "a perfect score often means the suite is too easy — add hard cases").
- **A real metric tied to outcome** (Fiona's "don't forsake motion for progress"): the headline is the **bad-rate** — fraction of sampled artifacts with ≥1 `bad` finding — trended week over week, not a vanity volume count.

## Weekly log template

`Evals/monitoring/<YYYY-Www>.md`:

```markdown
# Monitoring — week <YYYY-Www>

| Sample | Artifact | Suite/criteria applied | bad | sad | Verdict | Note |
|---|---|---|---|---|---|---|
| 1 | Projects/x/prd.md | prd-readiness | 0 | 1 | ok | verbose non-goals |
| 2 | .../synthesis.md | research-synthesis (+judge eval 05 n/a) | 1 | 0 | flagged | invented a 30% metric |

**bad-rate this week:** <#samples with ≥1 bad> / <N> = <%>  (last week: <%>)

## New failure modes (→ candidate fixtures)
- ...

## Actions
- [ ] /eval-ci register <suite> ... (if a mapped file needs a re-run)
- [ ] add fixture: ...
```

## Cadence & ownership

- Runs weekly, hooked off `/weekly-update` (see that skill's monitoring step).
- Sampling is cheap; grading is the cost — keep N small (10–15) and let it compound. A stale monitoring log (>2 weeks) is the same technical debt as a stale suite.
- Result files here follow the same gitignore policy as `Evals/*/results/*` in the public template; the bad-rate trend is what gets surfaced, not raw artifacts.
