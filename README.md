# AI Product Lab

![AI Product Management](https://img.shields.io/badge/AI%20Product%20Management-Working%20Lab-blue)
![LLM Evals](https://img.shields.io/badge/LLM-Evals-purple)
![RegEval](https://img.shields.io/badge/RegEval-Flagship%20Project-green)
![Agentic Workflows](https://img.shields.io/badge/Agentic-Workflows-orange)
![Status](https://img.shields.io/badge/status-active-brightgreen)

A working lab for practicing AI Product Management with real eval discipline — LLM evals, agentic workflows, quality gates, and measurable product artifacts, built and run in the open.

**The problem it works on.** AI products are easy to demo and hard to trust. The demo is the first 10%; the rest is a clear user problem, a falsifiable metric, quality gates, human review, and an honest log of what failed and what fixed it. This repo is where that after-the-demo discipline gets practiced on real work instead of described in the abstract.

This is not a reusable PM workflow template — for that, see [PM Command Center](https://github.com/richardan01/PM-Command-Center). This is the applied lab: a flagship eval project, artifact quality gates, and eval loops, built and run in the open.

The Batman / Bruce Wayne layer is just the routing metaphor — Batman for focused execution, Bruce Wayne for long-range strategy. It organizes the work; it isn't the point of it. The substance is the eval and product work below.

---

## Start here

- [`PROOF-OF-WORK.md`](PROOF-OF-WORK.md) — how the lab measures its own work: RegEval, the gates, and the run logs, and how they connect.
- [`HOW-IT-WORKS.md`](HOW-IT-WORKS.md) — the architecture: agents, gates, evals, and how they compose.
- [`Evals/regeval/regeval-suite.md`](Evals/regeval/regeval-suite.md) — the flagship RegEval methodology and acceptance criteria.
- [`Evals/run-log.md`](Evals/run-log.md) — chronological eval and gate run history.
- [`Projects/ralph/brief.md`](Projects/ralph/brief.md) — the RegEval/Ralph project brief.

## What's inside

- An eval loop built on falsifiable metrics with explicit acceptance bars.
- Failure-mode tracking, with logged remediations and reruns.
- Two mandatory review gates on every public artifact.
- Claude Code used as the workflow runtime.
- A run log that keeps what was measured, what failed, and what changed visible over time.

---

## What this is

AI Product Lab treats AI PM practice the way Karpathy treats autoresearch: one runner, one metric, a fixed time budget, a compounding log. Applied here, that means AI product work gets built, measured, reviewed, logged, and improved over time.

It is a lab and a working log — not a generic operating system, and not a template to fork.

The system runs on a single layer: the **Batman Strategic Layer** — 8 agents in `Agents/Gotham/Computer/` covering the day-to-day work (flagship build, writing, research, technical depth).

## Naming clarification

This repo was formerly named AIPM-OS. The new name better reflects what it is: an AI Product Management lab focused on evals, agents, and measurable artifacts.

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

An LLM-as-judge evaluation framework for regulated-domain compliance classification. It's where the eval discipline in this repo is applied end to end — the thing the lab is built around.

Three modules:
1. **Provenance traces** — per-verdict run-lineage envelope (JSONL + human-readable cards)
2. **Abstention as a first-class class** — judge abstains on ambiguous items; abstention rate is a metric, not an error
3. **Human-vs-judge CLI** — live κ computation against a gold dataset; reconciles logged vs live results

**Current status (2026-06-29):** Binary judge (`binary-v1`) at κ=1.000 in-sample (N=82) + κ=1.000 genuine held-out (N=36, 20 unseen regimes). Clean-construct result — not yet production-validated. See `Evals/regeval/regeval-suite.md` for methodology and `Evals/run-log.md` for the full run history.

### Quality gate pipeline (`Workflows/`, `Tools/`)

Every public artifact goes through two mandatory gates before shipping:
- **Riddler** — adversarial review: "find every way this could be wrong or misleading"
- **Vicki Vale** — reader-voice review: "would a stranger stick with this past the first paragraph"

Both must pass. A PreToolUse hook in `.claude/settings.json` runs `Tools/gate-check.sh`, which blocks writes to `Artifacts/` — and to any filename containing `-essay`, `-post`, or `-thread` — unless `.riddler-passed` + `.vicki-passed` markers are present and fresh (6h TTL). The gate verdicts themselves are committed (see `Evals/regeval/.riddler-passed`) so the review trail is inspectable.

### Eval discipline layer (`Evals/`, `.claude/agents/`)

Beyond the flagship: 8+ eval suites with planted-flaw inputs and answer keys, a severity taxonomy, an eval-CI regression sentinel, judge-calibration (TPR/TNR ≥ 0.9 before a judge is trusted), Hamel/Shankar-style error analysis, and author/grader-separated sub-agents (`eval-runner` may never read the answer keys `eval-grader` grades against).

### Skill library (`.claude/skills/`)

Reusable skill files for recurring workflows: `/peer-review`, `/prd-readiness`, `/judge-calibration`, `/error-analysis`, `/eval-ci`, and more. Each skill is a SKILL.md file with frontmatter, procedure, and output shape. The RegEval experiment loop and monthly memory consolidation are workflow specs (`Workflows/regeval-run.md`, `Workflows/memory-consolidation.md`), invoked by name rather than as slash commands.

---

## How to adapt this

This repo is intentionally personal and opinionated, but the pattern is portable:

1. `Agents/Gotham/thesis-q3-2026.md` — your own quarterly thesis (mission, pillars, signposts)
2. `CLAUDE.md` — your identity, routing rules, and quality gates
3. `Agents/Gotham/Computer/` agent files — adapt voice samples to your own context
4. `Projects/` — your flagship project (Ralph = RegEval here; name yours)
5. `Evals/` — your own eval suites (keep the methodology; replace the domain)

The Batman persona is the frame. The Karpathy compounding principle is the engine. For a reusable PM workspace rather than a personal working lab, start from [PM Command Center](https://github.com/richardan01/PM-Command-Center).

---

## Stack

- **Claude Code** (CLI + agent SDK) — primary runtime
- **Claude API** — `claude-sonnet-4-6` for most tasks; `claude-opus-4-8` for strategic depth
- **Local git** — lab files versioned; eval result files gitignored

---

## RegEval — deeper context

The core research question: *can an LLM judge reliably classify regulatory compliance with agreement high enough to replace a human spot-checker?*

The metric: **Cohen's κ** (judge vs human gold labels). Bar: κ ≥ 0.80, CI-lower ≥ 0.70.

The integrity lesson embedded in the harness: a held-out validation set must be verified disjoint from the tuning set (by item ID + text) before any out-of-sample κ is cited. This exact failure occurred (FM-11) and is now a load-bearing anti-pattern in `Evals/regeval/regeval-suite.md`.

See `Knowledge/Research/regeval-synthesis.md` for the full research synthesis.

---

*A personal working lab — updated as the work happens.*
