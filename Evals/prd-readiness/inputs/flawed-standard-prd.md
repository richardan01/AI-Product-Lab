# PRD — Bulk CSV Export for Reporting

**Author:** PM · **Status:** For engineering handoff · **Last updated:** 2026-06-14

## Overview / Problem statement
Analysts can only export one report at a time, so monthly board prep takes ~6 hours of manual clicking (baseline: 14 reports × ~25 min each). We will let analysts queue a bulk export of multiple reports as a single CSV bundle.

## Goals
- Cut monthly board-prep export time.
- Improve checkout completion rate significantly.

## Non-goals
- Scheduled/recurring exports (later release).
- Export formats other than CSV.

## Background
The current export uses a synchronous endpoint that times out beyond ~50k rows. Bulk export needs an async job + download link.

## User stories
- **US-1 — Queue a bulk export.** As an analyst, I select multiple reports and queue them as one export job.
  - *Acceptance criteria:* analyst can select 2–20 reports; job appears in a jobs list with status; queuing is non-blocking.
- **US-2 — Download the bundle.** As an analyst, I download the finished bundle from the jobs list.
  - *Acceptance criteria:* download link valid 24h; bundle is a single zip of CSVs; expired link shows a clear message.
- **US-3 — Get notified when ready.** As an analyst, I am notified when my export finishes.

## Requirements (priority-tagged)
- **Must:** multi-select; async job; download bundle.
- **Should:** email notification on completion.
- **Nice-to-have:** job history beyond 30 days.

## Data requirements
- Reads existing `reports` and `report_rows`. New `export_jobs` table (status, requested_by, report_ids, artifact_url, expires_at).

## Dependencies
- Object storage for artifacts — owner: TBD — ETA TBD.
- Async worker queue — owner: Platform (Elena) — ETA 2026-07-05.

## Launch plan
- Stage 1: internal beta with the analytics team.
- Stage 2: GA to all analyst-role users.
- Rollback: feature flag off; queued jobs drain or are cancelled.

## Success metrics
- Board-prep export time improves.
- Export job success rate is high.

## Open questions
- Q1: Max number of reports per bundle? — owner: PM — due 2026-06-20.
