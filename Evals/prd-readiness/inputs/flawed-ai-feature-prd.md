# PRD — AI Ticket Triage (auto-routing)

**Author:** PM · **Status:** For engineering handoff · **Last updated:** 2026-06-13

## Overview / Problem statement
Incoming support tickets are routed by hand, adding ~9 min median delay before an agent picks one up (baseline: queue logs, May 2026). We will use a model to classify each new ticket's category and priority and auto-route it to the right queue.

## Goals
- Cut median time-to-first-touch from 9 min to ≤ 4 min.
- Reduce mis-routes (ticket reassigned at least once) from the 18% baseline.

## Non-goals
- Drafting replies (separate feature).
- Routing of phone/voice contacts.

## Background
Routing rules are a brittle keyword tree maintained by ops. A classifier should generalize better to new phrasings.

## User stories
- **US-1 — Ticket is auto-routed.** As a new ticket, I am classified and placed in the correct queue within 5s.
  - *Acceptance criteria:* category + priority assigned ≤ 5s p95; routed to mapped queue; classification logged with model version + confidence.
- **US-2 — Ops overrides a route.** As an ops lead, I can reassign a mis-routed ticket and the system learns from it.
- **US-3 — Ops sees routing stats.** As an ops lead, I see a daily breakdown of routes and overrides.
  - *Acceptance criteria:* dashboard shows volume per queue, override rate, and confidence distribution, refreshed daily.

## Requirements (priority-tagged)
- **Must:** classify + route; ops override.
- **Should:** routing stats dashboard.
- **Nice-to-have:** per-queue confidence thresholds.

## Data requirements
- Reads `tickets`. New `routing_events` table (ticket_id, predicted_category, predicted_priority, confidence, model_version, overridden_bool).

## Scope boundaries
- **In scope:** English email/chat tickets, web.
- **Out of scope:** voice, non-English, reply drafting.

## Dependencies
- Inference endpoint — owner: ML Platform (Wei) — ETA 2026-07-10.
- `routing_events` migration — owner: Data Eng (Marco) — ETA 2026-06-28.

## Model design
- Model: `claude-haiku-4-5` behind the internal gateway. Rationale: classification is single-turn and latency-sensitive; Haiku meets the 5s budget at acceptable offline accuracy. Inputs are agent/customer ticket text (not arbitrary untrusted tool output); single-turn classification only.

## Eval criteria
We will track classification accuracy and keep an eye on the override rate to make sure the model is doing a good job before we expand the rollout.

## Failure modes
1. **Mis-classification** → ops can override (US-2).
2. **Latency spike** → cap at 5s budget.

## Launch plan
- Stage 1: shadow mode (predict, don't route) for 1 week.
- Stage 2: auto-route 25% of tickets.
- Stage 3: GA.
- Rollback: flag off reverts to the keyword routing tree.

## Success metrics
- Time-to-first-touch ≤ 4 min; mis-route rate below the 18% baseline.

## Open questions
- Q1: Confidence threshold below which we fall back to the keyword tree? — owner: PM — due 2026-06-20.
