# AI PM Portfolio Lab (AIPM-OS)

A public personal portfolio lab for developing AI PM craft, shipping proof-of-work, and compounding toward a frontier-lab PM path.

This is **not** the reusable Product Management OS template. If you want the forkable operating-system template for PM workflows, start with [`Product-Management_OS`](https://github.com/richardan01/Product-Management_OS). If you want to see one applied instance of that discipline, with a flagship project, public artifact gates, and career-positioning loops, this repo is the lab.

Built on Claude Code + Claude API, structured around a Batman/Bruce Wayne dual-persona framework.

**Batman = execution mode.** Bruce Wayne = multi-year strategy. The 24-month arc beats the 24-hour reaction.

---

## Public repo map

| Repo | Public role | Use it when |
| --- | --- | --- |
| [`Product-Management_OS`](https://github.com/richardan01/Product-Management_OS) | Reusable Product Management OS template | You want a forkable PM operating system for workflows, memory, knowledge, quality gates, and evals. |
| [`AIPM-OS`](https://github.com/richardan01/AIPM-OS) | Personal AI PM portfolio lab | You want to inspect the applied proof-of-work: RegEval, public artifact gates, AI PM craft, and frontier-lab preparation. |

In short: **Product Management OS is the reusable system**. `AIPM-OS` is the personal proof-of-work lab built with that operating-system discipline.

---

## What this is

This lab treats AI PM capability development the same way Karpathy treats autoresearch: one runner, one metric, fixed time budget, compounding log. Applied to career development and public proof-of-work.

The system runs on two layers:
- **Batman Strategic Layer** — 8 agents in `Agents/Gotham/Computer/` for AI PM mission work (flagship build, public voice, network, technical depth).
- **Day-Job Operations Layer** — separate layer for current employment context (not included in this public repo).

The Batman layer is the default. Day-job layer is opt-in.

---

## Key components

### Gotham agent suite (`Agents/Gotham/Computer/`)

8 Batman-character agents, each with a distinct domain and voice:

| Agent | Domain |
|---|---|
| Bruce Wayne | Career strategy, quarterly thesis, positioning |
| Alfred | Daily ops, calendar, prep, accountability |
| Lucius Fox | Build, prototype, MCP/skill authoring |
| Oracle | Research, JD scans, hiring-manager recon |
| Nightwing | Essays, posts, threads, talks |
| The Riddler | Adversarial review (pre-publish gate) |
| Henri Ducard | Technical-depth coaching and drilling |
| Vicki Vale | Reader-voice review (pre-publish gate) |

The full design has 12 agents; 4 (network/negotiation/execution-mode/parallel-drafting specialists) are left out of this public template. See the note in `Agents/agent-system-architecture.md` for how leftover references to them are handled.

### RegEval — the flagship project (`Projects/ralph/`, `Evals/regeval/`)

An LLM-as-judge evaluation framework for regulated-domain compliance classification. The flagship proof that an AI PM can build and measure the thing they claim to understand.

Three modules:
1. **Provenance traces** — per-verdict run-lineage envelope (JSONL + human-readable cards)
2. **Abstention as a first-class class** — judge abstains on ambiguous items; abstention rate is a metric, not an error
3. **Human-vs-judge CLI** — live κ computation against a gold dataset; reconciles logged vs live results

**Current status (2026-06-29):** Binary judge (`binary-v1`) at κ=1.000 in-sample (N=82) + κ=1.000 genuine held-out (N=36, 20 unseen regimes). Clean-construct result — not yet production-validated. See `Evals/regeval/regeval-suite.md` for methodology and `Evals/run-log.md` for the full run history.

### Quality gate pipeline (`Workflows/`)

Every public artifact goes through two mandatory gates before shipping:
- **Riddler** — adversarial review: "find every way this could be wrong or misleading"
- **Vicki Vale** — reader-voice review: "would a stranger stick with this past the first paragraph"

Both must pass. The gate hook in `.claude/settings.json` blocks writes to `Artifacts/` without `.riddler-passed` + `.vicki-passed` markers.

### Skill library (`.claude/skills/`, `.agents/skills/`)

Reusable skill files for recurring workflows: `/peer-review`, `/prd-readiness`, `/regeval-run`, `/gate-dispatch`, `/memory-consolidation`, and more. Each skill is a SKILL.md file with frontmatter, procedure, and output shape.

---

## How to adapt this

To adapt this portfolio-lab pattern for your own use, start from the reusable [`Product-Management_OS`](https://github.com/richardan01/Product-Management_OS) template first, then replace the personal layer here:

1. `Agents/Gotham/thesis-q3-2026.md` — your own quarterly thesis (mission, pillars, signposts)
2. `CLAUDE.md` — your identity, routing rules, and quality gates
3. `Agents/Gotham/Computer/` agent files — adapt voice samples to your own context
4. `Projects/` — your flagship project (Ralph = RegEval here; name yours)
5. `Evals/` — your own eval suites (keep the methodology; replace the domain)

The Batman persona is the frame. The Karpathy compounding principle is the engine. Both are portable, but this repo is intentionally personal and opinionated.

---

## Stack

- **Claude Code** (CLI + agent SDK) — primary runtime
- **Claude API** — `claude-sonnet-4-6` for most tasks; `claude-opus-4-8` for strategic depth
- **MCP servers** (always-on): FatHippo (shared memory), Lark (comms), Apple Notes (report fallback)
- **Local git** — all OS files versioned; eval result files gitignored

---

## RegEval — deeper context

The core research question: *can an LLM judge reliably classify regulatory compliance with agreement high enough to replace a human spot-checker?*

The metric: **Cohen's κ** (judge vs human gold labels). Bar: κ ≥ 0.80, CI-lower ≥ 0.70.

The integrity lesson embedded in the harness: a held-out validation set must be verified disjoint from the tuning set (by item ID + text) before any out-of-sample κ is cited. This exact failure occurred (FM-11) and is now a load-bearing anti-pattern in `Evals/regeval/regeval-suite.md`.

See `Knowledge/Research/regeval-synthesis.md` for the full research synthesis.

---

*Built by an AI PM aspirant proving the thing they claim to understand.*
