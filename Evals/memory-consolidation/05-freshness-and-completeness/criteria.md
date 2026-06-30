# 05 — Freshness + completeness

**Criterion:** `Last consolidated:` in `MEMORY.md` was bumped to the run date; the full window was covered (no in-range session transcript skipped); `daily-learnings.md` received an entry (or an explicit "nothing durable today").

**Why:** The date stamp is the routine's clock — if it doesn't advance, the window silently grows and the loop breaks. This is exactly the failure that froze memory at 2026-06-11. A skipped transcript = silent context loss.

**Pass:** Date bumped; every in-range transcript accounted for; learnings appended.

**Fail:** Date unchanged after a run that had new content; a transcript in range never read; no learnings entry on a day that contained corrections or preferences.

**How to check:** Confirm the `Last consolidated` delta. List in-range transcripts and confirm the run referenced each.
