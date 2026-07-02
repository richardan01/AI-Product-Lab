# AI PM Portfolio Lab (AIPM-OS)

A public portfolio lab for developing AI PM craft through measurable proof-of-work: eval discipline, RegEval, quality gates, Claude Code loops, and public run logs.

This repo is a live, opinionated instance of an AI PM operating system — a flagship project, public artifact gates, eval loops, and career-positioning artifacts, all built and run in the open. The Batman/Bruce Wayne layer is the routing metaphor: Batman means focused execution mode; Bruce Wayne means multi-year strategy. It supports the work, but the value proposition is the professional proof-of-work system.

---

## Start here

- [`PROOF-OF-WORK.md`](PROOF-OF-WORK.md) — how this repo turns AI PM learning into inspectable portfolio evidence.
- [`HOW-IT-WORKS.md`](HOW-IT-WORKS.md) — the architecture: agents, gates, evals, and how they compose.
- [`Evals/regeval/regeval-suite.md`](Evals/regeval/regeval-suite.md) — the flagship RegEval methodology and acceptance criteria.
- [`Evals/run-log.md`](Evals/run-log.md) — chronological eval and gate run history.
- [`Projects/ralph/brief.md`](Projects/ralph/brief.md) — the RegEval/Ralph project brief.

## What this proves

- I can design an eval loop.
- I can define a falsifiable metric.
- I can track failures and remediations.
- I can use Claude Code as a workflow runtime.
- I can turn AI PM learning into public proof-of-work.

---

## What this is

This lab treats AI PM capability development the same way Karpathy treats autoresearch: one runner, one metric, fixed time budget, compounding log. Applied to career development and public proof-of-work.

The system runs on a single layer: the **Batman Strategic Layer** — 8 agents in `Agents/Gotham/Computer/` for AI PM mission work (flagship build, public voice, network, technical depth).

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

The full design has 12 agents; 4 (network/negotiation/execution-mode/parallel-drafting specialists) are left out of this public repo. See the note in `Agents/agent-system-architecture.md` for how leftover references to them are handled.

### RegEval — the flagship project (`Projects/ralph/`, `Evals/regeval/`)

An LLM-as-judge evaluation framework for regulated-domain compliance classification. The flagship proof that an AI PM can build and measure the thing they claim to understand.

Three modules:
1. **Provenance traces** — per-verdict run-lineage envelope (JSONL + human-readable cards)
2. **Abstention as a first-class class** — judge abstains on ambiguous items; abstention rate is a metric, not an error
3. **Human-vs-judge CLI** — live κ computation against a gold dataset; reconciles logged vs live results

**Current status (2026-06-29):** Binary judge (`binary-v1`) at κ=1.000 in-sample (N=82) + κ=1.000 genuine held-out (N=36, 20 unseen regimes). Clean-construct result — not yet production-validated. See `Evals/regeval/regeval-suite.md` for methodology and `Evals/run-log.md` for the full run history.

### Quality gate pipeline (`Workflows/`, `Tools/`)

Every public artifact goes through two mandatory gates before shipping:
- **Riddler** — adversarial review: "find every way this could be wrong or misleading"
- **Vicki Vale** — reader-voice review: "would a stranger stick with this past the first paragraph"

Both must pass. A PreToolUse hook in `.claude/settings.json` runs `Tools/gate-check.sh`, which blocks writes to `Artifacts/` without `.riddler-passed` + `.vicki-passed` markers. The gate verdicts themselves are committed (see `Evals/regeval/.riddler-passed`) so the review trail is inspectable.

### Eval discipline layer (`Evals/`, `.claude/agents/`)

Beyond the flagship: 8+ eval suites with planted-flaw inputs and answer keys, a severity taxonomy, an eval-CI regression sentinel, judge-calibration (TPR/TNR ≥ 0.9 before a judge is trusted), Hamel/Shankar-style error analysis, and author/grader-separated sub-agents (`eval-runner` may never read the answer keys `eval-grader` grades against).

### Skill library (`.claude/skills/`)

Reusable skill files for recurring workflows: `/peer-review`, `/prd-readiness`, `/regeval-run`, `/judge-calibration`, `/error-analysis`, `/eval-ci`, `/memory-consolidation`, and more. Each skill is a SKILL.md file with frontmatter, procedure, and output shape.

---

## How to adapt this

This repo is intentionally personal and opinionated, but the pattern is portable:

1. `Agents/Gotham/thesis-q3-2026.md` — your own quarterly thesis (mission, pillars, signposts)
2. `CLAUDE.md` — your identity, routing rules, and quality gates
3. `Agents/Gotham/Computer/` agent files — adapt voice samples to your own context
4. `Projects/` — your flagship project (Ralph = RegEval here; name yours)
5. `Evals/` — your own eval suites (keep the methodology; replace the domain)

The Batman persona is the frame. The Karpathy compounding principle is the engine.

---

## Stack

- **Claude Code** (CLI + agent SDK) — primary runtime
- **Claude API** — `claude-sonnet-4-6` for most tasks; `claude-opus-4-8` for strategic depth
- **Local git** — all OS files versioned; eval result files gitignored

---

## RegEval — deeper context

The core research question: *can an LLM judge reliably classify regulatory compliance with agreement high enough to replace a human spot-checker?*

The metric: **Cohen's κ** (judge vs human gold labels). Bar: κ ≥ 0.80, CI-lower ≥ 0.70.

The integrity lesson embedded in the harness: a held-out validation set must be verified disjoint from the tuning set (by item ID + text) before any out-of-sample κ is cited. This exact failure occurred (FM-11) and is now a load-bearing anti-pattern in `Evals/regeval/regeval-suite.md`.

See `Knowledge/Research/regeval-synthesis.md` for the full research synthesis.

---

*Built by an AI PM aspirant proving the thing they claim to understand.*
