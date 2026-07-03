# Agentic PM System — Architecture

## "Computer" — The Invocation Pattern

When you say **"Computer, [task]"**, the system routes to the right agent automatically. This is the Batman/Bruce Wayne operating contract: "Computer" is the Batcave interface.

### Routing table

| "Computer, ..." | Routes to | Model | Voice |
|---|---|---|---|
| what should I focus on today / morning brief | Alfred | Haiku → Sonnet | Dry, precise, "Master [Your Name]" |
| prep me for [meeting] / who is [person] | Alfred → Oracle | Sonnet | Alfred briefs; Oracle researches |
| scan for frontier-lab PM roles / what did [person] ship | Oracle | Sonnet / Opus | Crisp, citation-dense |
| what's our Q3 2026 thesis / should I pursue this target | Bruce Wayne | Opus | Measured, strategic, future-tense |
| draft this X thread / write the essay opener | Nightwing | Sonnet/Opus | Charismatic, rhythmic, narrative-led |
| review this essay / is this ready to ship | Riddler + Vicki Vale | Opus (Riddler), Sonnet (Vale) | Sharp adversarial + plain reader |
| prototype the eval harness / build the MCP | Lucius Fox | Opus / Sonnet | Warm-technical, failure-modes-first |
| drill me on RLHF / can I defend this claim | Henri Ducard | Opus | Socratic, calibration-obsessed |

> **Note:** This template ships 8 of the 12 agents from the full Batman-layer design. Some agent files' Handoffs/"does NOT do" sections still reference the other 4 (Batman — high-stakes execution mode via `/cowl-up`, Robin — parallel drafting, Commissioner Gordon — network/warm-intro, Selina Kyle — offer negotiation) as handoff targets. Those aren't included here; the references illustrate the intended handoff design rather than pointing to files in this repo.

### Model complexity tiers

| Tier | Model | When |
|---|---|---|
| **Fast** | `claude-haiku-4-5-20251001` | Read-only triage, simple lookups. Never in agentic loops with untrusted input. |
| **Standard** | `claude-sonnet-4-6` | Default — research synthesis, draft writing, build review, most skills |
| **Deep** | `claude-opus-4-8` | Riddler, Bruce Wayne, Henri Ducard, Lucius Fox (complex builds) — never downgrade these |

---

## The Problem

A Product Manager's daily work is high-context, multi-domain, and interruptible. On any given day you're switching between sprint planning, stakeholder prep, vendor evaluation, risk tracking, and writing PRDs — each requiring different data, different frameworks, and different output formats.

A single AI assistant with one long prompt can't handle this well. It conflates domains, loses context, and produces generic output. The alternative — 14 separate tools — fragments the workflow and forces the human to be the orchestrator.

**This system solves that.** It's a multi-agent architecture where each agent owns a narrow domain, agents coordinate through a shared file system (not direct calls), and orchestration patterns govern how they compose into workflows.

The design philosophy: **agents do narrow things well; the system handles coordination.**

---

## Architecture Overview

### Three Tiers

```
┌─────────────────────────────────────────────────────────┐
│  TIER 1: Skills (.claude/skills/[name]/SKILL.md)        │
│  User-facing commands — the interface layer              │
│  /today  /weekly-update  /risk-register  /go-nogo       │
└──────────────────────────┬──────────────────────────────┘
                           │ invokes
┌──────────────────────────▼──────────────────────────────┐
│  TIER 2: Agents                                          │
│  Batman layer: Agents/Gotham/Computer/ (8 agents)        │
│  Domain owners — context, quality checks, file ownership │
└──────────────────────────┬──────────────────────────────┘
                           │ spawns
┌──────────────────────────▼──────────────────────────────┐
│  TIER 3: Sub-Agents (.claude/agents/[name].md)          │
│  Isolated workers — parallel execution, no file writes   │
│  Sub-agents for data gathering and drafting              │
└──────────────────────────┬──────────────────────────────┘
                           │ reads / writes
┌──────────────────────────▼──────────────────────────────┐
│  SHARED FILE SYSTEM (the "message bus")                  │
│  Tasks/  Projects/  Knowledge/  Meetings/  GOALS.md      │
│  Agents coordinate through files, not direct calls       │
└─────────────────────────────────────────────────────────┘
```

**Why three tiers, not one?**

| Tier | Concern | Analogy |
|------|---------|---------|
| Skills | *What* to do — user intent, output format | API endpoint / controller |
| Agents | *How* to do it — domain logic, quality standards, file ownership | Service / domain layer |
| Sub-Agents | *Fetch* data — isolated, stateless, parallel-safe | Worker / microservice |

---

## Design Principles

### 1. Single Responsibility per Agent
Each agent owns one domain with clearly scoped read/write permissions. No two agents write to the same file.

### 2. File-Based Coordination (Pub/Sub via Filesystem)
Agents never call each other directly. Agent A writes to a shared file. Agent B reads that file when invoked. This is asynchronous pub/sub where the filesystem is the message broker.

### 3. Sub-Agents for Isolation
Sub-agents run in isolated contexts. They can read files but not write them. They return structured data to the parent skill.

### 4. Quality Gates at Lifecycle Boundaries
Every transition between phases (discovery → build, build → launch) has an evaluator skill that scores readiness against a checklist.

---

## Batman Voice Overlay (operating contract applied to all agents)

Per the Batman / Bruce Wayne operating contract installed in `CLAUDE.md`, every agent speaks in a Batman-character voice while keeping its functional name and domain expertise.

→ See `_Registry/voice-map.md` (single source of truth — voice fingerprints, layer disambiguation, overlay mechanics).

---

## Orchestration Patterns

Six patterns govern how agents compose into workflows.

### 1. Sequential / Chain
One agent's output feeds the next in a fixed order.

### 2. Parallel / Fan-Out
Multiple sub-agents run simultaneously on independent data sources. The parent skill merges results.

### 3. Hub-and-Spoke / Smart Router
The Orchestrator detects which agent domain(s) a request belongs to and routes accordingly.

### 4. Iterative Loop (Quality Gate)
An output is evaluated against quality checks. If it fails, it loops back for revision. Capped at 2 iterations.

### 5. Evaluator / Gate
A skill that scores readiness against a checklist at lifecycle boundaries (discovery → build, build → launch).

### 6. Conditional Trigger
A check embedded inside an existing skill that fires when data-driven conditions are met.

---

## The Message Bus

All inter-agent coordination flows through shared files.

**Design rule:** Each file has exactly one writer and one or more readers. No two agents write to the same file. This eliminates write conflicts and makes data lineage traceable.

---

## Sub-Agents (Workers)

Isolated workers that agents spawn for parallel data gathering and drafting.

This public repo ships the eval trio (`.claude/agents/`); further general-purpose workers (task/meeting/metrics readers, profilers, drafters) live in the private local layer and are not committed.

| Sub-Agent | Model | Spawned by | Purpose |
|-----------|-------|-----------|---------|
| eval-runner | Sonnet | `/evals` | Run a fixture, capture a verbatim transcript — never reads criteria or answer keys |
| eval-grader | Sonnet | `/evals` | Grade a transcript against criteria only — never reads the workflow |
| trace-collector | Haiku | `/evals`, `/error-analysis` | Sample recent outputs into `_traces/` for open coding |

**Constraint:** Sub-agents are read-only. They return structured data to the parent skill. Only the parent skill decides what to write and where.

## Related

[[HOW-IT-WORKS]] · [[CLAUDE]] · [[Workflows/index]] · [[Evals/index]] · [[_Registry/voice-map]]
