# PRD — AI Reply Suggestions for Support Inbox

**Author:** PM · **Status:** For engineering handoff · **Last updated:** 2026-06-15

## Overview / Problem statement
Support agents retype the same answers to common questions. In Q1, 38% of ticket replies (baseline: 12,400 of 32,600 replies) were near-duplicates of a prior reply, costing a median 2.4 min each. We will suggest a draft reply the agent can edit and send, to cut handle time without lowering CSAT.

## Goals
- Reduce median first-reply time from 2.4 min to ≤ 1.6 min on eligible tickets.
- Hold CSAT at or above the current 4.3/5 baseline.

## Non-goals
- Auto-sending replies without agent review (out of scope this release).
- Non-English tickets (deferred to a later release).

## Background
Agents already use saved replies, but adoption is 21% because finding the right macro is slow. Reply suggestions surface the macro-or-better draft inline.

## User stories
- **US-1 — Agent sees a suggestion.** As an agent opening an eligible ticket, I see one suggested draft reply within 1.5s so I can edit and send.
  - *Acceptance criteria:* suggestion renders ≤ 1.5s p95; agent can edit before send; suggestion is dismissible; no suggestion shown when confidence < threshold.
- **US-2 — Agent edits and sends.** As an agent, I can edit the draft inline and send, and my edits are captured.
  - *Acceptance criteria:* edited text sends as the reply; original suggestion + final text both logged; send path unchanged when no suggestion present.
- **US-3 — Agent reports a bad suggestion.** As an agent, I can flag a suggestion as wrong in one click.
  - *Acceptance criteria:* flag stored with ticket id + suggestion id; flagged suggestions excluded from training set; agent sees confirmation toast.

## Requirements (priority-tagged)
- **Must:** inline suggestion render; edit-before-send; confidence gate; flag-as-wrong.
- **Should:** suggestion latency telemetry; per-team enable toggle.
- **Nice-to-have:** multiple alternative drafts.

## Data requirements
- Source: `tickets` + `replies` tables (existing). New `suggestion_events` table (schema in appendix: suggestion_id, ticket_id, model_version, confidence, shown_at, accepted_bool, edited_bool, final_text_hash).
- No new PII collected; final reply text is hashed in events, not stored raw.

## Scope boundaries
- **In scope:** English tickets, web inbox, agent-reviewed sends.
- **Out of scope:** auto-send, mobile inbox, non-English, voice.

## Dependencies
- Inference endpoint — owner: ML Platform (Wei) — ETA 2026-07-01.
- `suggestion_events` table migration — owner: Data Eng (Marco) — ETA 2026-06-25.

## Model design
- Model: `claude-haiku-4-5` for latency, behind the existing internal gateway. Rationale: p95 < 1.5s required; Haiku meets it at acceptable quality on the offline set. NOT used in an agentic loop with untrusted input — single-turn draft generation only.

## Eval criteria
| Metric | Method | Baseline | Target | Ship threshold |
|---|---|---|---|---|
| Suggestion acceptance rate | `suggestion_events.accepted_bool` | n/a (new) | ≥ 35% | ≥ 25% to ship |
| Edit distance (accepted) | mean Levenshtein on final vs. suggested | n/a | ≤ 40% | ≤ 55% |
| CSAT on AI-touched tickets | post-ticket survey | 4.3/5 | ≥ 4.3 | ≥ 4.2, no regression |
| Harmful/incorrect rate | LLM-judge on sampled drafts, human-calibrated | n/a | ≤ 1% | ≤ 2% |

## Failure modes & guardrails
1. **Confidently wrong draft** → confidence gate hides low-confidence drafts; flag-as-wrong feeds exclusion list.
2. **PII leakage across tickets** → retrieval scoped to the current ticket + public macros only; no cross-customer context.
3. **Latency spike** → 1.5s p95 budget; on timeout, fall back to no suggestion (US-1 dismiss path).
4. **CSAT regression** → CSAT ship threshold gates rollout; monitored weekly.

## Fallback paths
- Inference timeout or error → render no suggestion; agent uses existing flow (no degradation).
- Harmful-rate breach in monitoring → kill switch disables suggestions per-team; documented in runbook.

## Launch plan
- Stage 1: internal dogfood (support team, 1 week).
- Stage 2: 10% of eligible tickets, monitor eval thresholds.
- Stage 3: GA if all ship thresholds hold for 1 week.
- Rollback: feature flag off restores the prior inbox with no data migration.

## Success metrics
See Eval criteria. Primary: median first-reply time ≤ 1.6 min with CSAT ≥ 4.3.

## Open questions
- Q1: Do we expose alternative drafts in v1? — owner: PM — due 2026-06-22.
