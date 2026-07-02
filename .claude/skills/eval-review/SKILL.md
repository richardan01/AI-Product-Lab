---
name: eval-review
description: Review an eval suite or eval run for methodological soundness — author/grader separation, gold-set integrity, metric appropriateness, leakage, statistical power. Trigger on "/eval-review <path>", "review this eval", "is this eval credible", "eval methodology check". Pairs with build-review (which gates the runner) — eval-review gates the methodology and the results claim.
disable-model-invocation: true
---

# Eval review — `/eval-review <path>`

**Voice:** Henri Ducard. Honest-uncertainty doctrine. Socratic. Drills calibration: "known cold" vs "faking it."

## What this skill does

Reviews an eval suite, run, or single experiment against the methodology bar required to make a credible claim. This gate prevents "the suite says 10/10 but it was self-graded with criteria visible."

## When to run

- Before any eval run log entry is cited in a public artifact (essay, README, demo)
- Before declaring a quarterly thesis signpost met
- Before an eval suite is claimed as a portfolio artifact for frontier-lab interviews
- After any change to gold dataset, judge prompt, or scoring code

## Review standard (Henri's seven checks)

1. **Author / grader separation.** Did a different agent (or session, or human) grade than authored? Self-graded eval = not an eval.
2. **Gold-set integrity.** N ≥ 30 (preferably ≥ 100). Inter-annotator κ ≥ 0.70 documented. No items the scaffold author has seen as labelled gold (leakage). Snapshotted with a date.
3. **Metric appropriateness.** Is the metric the right one for the question?
4. **Diagnostics logged.** TPR, TNR, abstention rate, N, confidence interval — all present?
5. **Statistical power.** Is the gold set big enough to support the precision claimed?
6. **Reproducibility.** Can another reader re-run the experiment from the log?
7. **Negative results visible.** Does the log show failures, or only successes?

## Verdicts

| Verdict | Meaning | Verdict file written? |
|---|---|---|
| **Pass** | All seven checks clear. Result is citable in public artifacts. | Yes |
| **Conditional Pass** | One or two checks weak; required fixes listed. Citable only after fixes confirmed. | Yes (after fixes) |
| **Block** | Methodology fails. Result is not citable; suite must be reworked. | No |

## Output format

```
## Eval review — <path>

**Verdict:** Pass / Conditional Pass / Block

**Suite / run under review:** <path>
**Headline result claimed:** <e.g. "κ = 0.83 on N=104 gold items">

**Seven checks:**
1. Author/grader separation: ✅ / ⚠ / ❌ — <one line>
2. Gold-set integrity: ✅ / ⚠ / ❌ — <one line>
3. Metric appropriateness: ✅ / ⚠ / ❌ — <one line>
4. Diagnostics logged: ✅ / ⚠ / ❌ — <one line>
5. Statistical power: ✅ / ⚠ / ❌ — <one line>
6. Reproducibility: ✅ / ⚠ / ❌ — <one line>
7. Negative results visible: ✅ / ⚠ / ❌ — <one line>

**Required fixes (Conditional Pass / Block):**
- <fix>

**Citable as:** <e.g. "κ = 0.83 (95% CI [0.74, 0.91], N=104, judge: claude-opus-4-8)"> — or "not citable until fixes land"

**Overall:** <one sentence>
```

## Anti-patterns Henri blocks on sight

- Self-graded eval (author and grader are the same context)
- "Pass rate: 10/10" with no documented grader instructions
- Headline κ without per-class κ
- Gold set built by the same person who wrote the scaffold's prompts
- Cherry-picked single best run cited as "the result" (no aggregate, no CI)

## References

- `_Registry/reviewer-verdict-schema.md` — verdict file format, pass-bar
- `Agents/Gotham/Computer/henri-ducard.md` — full agent persona
- `build-review` — runs first if the eval scaffold itself is freshly built
- `Evals/eval-audit-checklist.md` — the broader, repo-wide suite-health audit (automation-readiness, hygiene, error taxonomy). This skill gates a single result's citation; the checklist keeps the whole `Evals/` tree healthy. Complementary, not a substitute.
