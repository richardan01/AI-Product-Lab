---
title: Pre-publish gate pattern
first_seen: Workflows/gate-dispatch
type: pattern
---

# Pre-publish gate pattern

## What it is

The standard quality gate that runs before any public artifact ships from the Batcave. Two mandatory parallel reviewers + one conditional escalation.

**Stage 1 (parallel):**
- [[Agents/Gotham/Computer/riddler]] — Task A: adversarial review. Argument strength, claim defensibility, technical accuracy.
- [[Agents/Gotham/Computer/vicki-vale]] — Task B: user-voice review. Reader attention, opener quality, "does she close the tab?"

**Stage 2 (conditional):**
- [[Agents/Gotham/Computer/henri-ducard]] — Task C: spawns only if `Riddler.verdict == block AND Riddler.depth_gap_flag == true`. Triages whether the depth gap is a quick re-drill or requires real study.

**Verdict merge:** [[Workflows/gate-merge]] combines 2-3 verdicts into `SHIP | REVISE | BLOCK`.

---

## Invoke via

```
Workflows/gate-dispatch.md
```

Or manually: `/riddler <artifact>` + `/vicki-vale <artifact>` run in parallel.

---

## Verdicts

| Riddler | Vicki Vale | Merge |
|---|---|---|
| pass | read | SHIP |
| conditional | read | REVISE (minor) |
| pass | bounce | REVISE (opener) |
| block (no depth_gap) | any | BLOCK (fix claims) |
| block (depth_gap=true) | any | BLOCK + Ducard drill |

---

## When to use

- Every public artifact: essays, LinkedIn posts, X threads, READMEs, demo scripts, talk decks
- Every interview answer script (PD-TOL, "Why [Target Company]" essay)
- Any eval claim involving a number, percentage, or benchmark

## When NOT to use

- Internal drafts, `_temp/` working files, private notes
- Internal PM deliverables (use `/peer-review` and `/prd-readiness` instead)

---

## Files that implement this pattern

- [[Workflows/gate-dispatch]] — orchestrator
- [[Workflows/gate-merge]] — verdict merger
- [[Agents/Gotham/_shared/gate-payload.schema]] — input contract
- [[Agents/Gotham/_shared/gate-response.schema]] — output contract
- `Tools/gate-check.sh` — pre-publish hook script (enforces gate at Write time)

## Related

[[Knowledge/Concepts/concepts-index]] · [[Agents/Gotham/Computer/nightwing]] · [[Agents/Gotham/Computer/lucius-fox]]
