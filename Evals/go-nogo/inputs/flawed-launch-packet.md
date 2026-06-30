# Launch Readiness Packet — AI Reply Suggestions (GA)

**Owner:** PM · **Planned launch:** 2026-06-25 09:00 UTC · **Last updated:** 2026-06-23

## Launch checklist status
- US-1 (inline suggestion) and US-2 (edit-and-send) met and verified in the 10% rollout.
- US-3 (flag-as-wrong) **not met**: the one-click flag stores the ticket id but does **not** exclude flagged suggestions from the training set — a P0 acceptance criterion. Fix in progress.
- Feature flag `reply_suggestions_ga` wired; per-team enable confirmed.

## UAT / QA sign-off
- QA: regression suite green (208/208). Signed off — Priya (QA Lead), 2026-06-22.
- UAT: support team dogfood, 1 week, 0 blocking defects. Signed off — Sam (Support Lead), 2026-06-21.

## Data
- Data-quality checks on `suggestion_events` passing.
- PII review confirmed: retrieval scoped to current ticket + public macros; no cross-customer context. Signed off — Marco (Data Eng), 2026-06-21.

## Stakeholders
- Support agents trained: walkthrough done, 14/16 agents confirmed ready; 2 on PTO, back 2026-06-26 (after launch).

## Comms
- Announcement drafted and approved; scheduled to send on GO.
- [YOUR_MANAGER] briefed on launch window, 2026-06-22.

## Risk
- Risk register reviewed: harmful/incorrect-draft rate measured at 2.4% on the 10% rollout — **above the 2% ship threshold**, High severity, **unmitigated**. Owner: ML Platform (Wei), no ETA.

## Rollback
- Rollback = kill switch disables suggestions per-team; documented in the runbook.
- Kill switch **never tested** — no drill run; behavior under an in-flight suggestion render is unverified.
