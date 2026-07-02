# GOALS — the mission this OS serves

**Mission (24-month arc):** AI PM at a frontier AI lab by mid-2027.
**Current quarter:** [`Agents/Gotham/thesis-q3-2026.md`](Agents/Gotham/thesis-q3-2026.md) — the live quarterly thesis. This file is the stable summary; the thesis is the operating detail.

---

## The three-pillar structure

Every quarter's thesis decomposes the mission into the same three pillars:

| Pillar | What it produces | Q3 2026 instance |
|---|---|---|
| **Technical depth credibility** | A flagship, measurable artifact a hiring manager can inspect | RegEval — LLM-as-judge eval framework (κ vs human gold) |
| **Public voice** | Published artifacts that carry the work to strangers | Canonical essay + launch posts, all Riddler/Vale-gated |
| **Network** | Warm-intro paths built **on** the artifacts, never before them | Warm-intro mapping after the flagship ships |

**Order is load-bearing:** artifact → voice → network. The artifact is the warm intro. No cold applications, ever.

## How progress is measured

- **Signposts, not vibes.** Each pillar has Day-30/60/90 signposts in the thesis; each has a binary hit/miss.
- **One invalidation criterion per quarter.** Q3's: a 5-minute RegEval demo worth showing a frontier-lab hiring manager. If it fails, the thesis pivots — the fallback is pre-declared, not improvised.
- **Falsifiable flagship metric.** RegEval's bar: Cohen's κ ≥ 0.80 with CI-lower ≥ 0.70 against human gold labels. Run history in [`Evals/run-log.md`](Evals/run-log.md).

## Quality bar for anything public

No public artifact ships without both gates: Riddler (adversarial) + Vicki Vale (reader-voice). Enforced by `Tools/gate-check.sh` — see [`Artifacts/README.md`](Artifacts/README.md).

## Related

[[Agents/Gotham/thesis-q3-2026]] · [[Tasks/active]] · [[HOW-IT-WORKS]] · [[PROOF-OF-WORK]]
