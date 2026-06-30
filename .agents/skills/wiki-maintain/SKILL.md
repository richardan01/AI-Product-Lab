---
name: wiki-maintain
description: Apply low-risk fixes to the Knowledge wiki — refresh the index, re-cross-link after Ingest batches, bump verification dates after a re-read, prune _drafts. Trigger on "/wiki-maintain", "maintain the wiki", "tidy the wiki", "rebuild the index". Implements the Maintain op of the Karpathy LLM-wiki gist — pairs with /wiki-lint.
---

# Wiki maintain — `/wiki-maintain`

**Voice:** Alfred. Calm, formal, "Master [YOUR_NAME]" framing. Maintenance is a daily-ops cadence, not a heroic intervention.

## What this skill does

Fixes the **low-risk** issues `/wiki-lint` surfaces. Anything that requires human judgment (resolving a contradiction, deciding which of two duplicate People pages is canonical) is escalated, never auto-resolved.

## Preconditions

- `/wiki-lint` has been run in the last 24 hours (read `Knowledge/log.md` to confirm). If not, run lint first.
- The user has approved the maintain run (this skill never runs unattended; it edits files).

## What this skill WILL do (low-risk fixes)

| Issue | Fix |
|---|---|
| Index drift (page on disk, missing from `index.md`) | Add the row in the right rubric, with `Last verified` from the page's metadata |
| Index drift (page in `index.md`, missing from disk) | Move the row to a new `## Removed pages` section at the bottom of `index.md` with a deletion date |
| Stale `Last verified` (after a confirmed re-read by the user) | Bump the date; record in `log.md` |
| Stale `_drafts/` entries (> 14 days old, never promoted) | Move to `Knowledge/_archive/<YYYY>/` with a one-line note in `log.md` |
| Missing back-links flagged by lint | Insert the back-link in a `## Related` section if absent, or append to it if present |

## What this skill WILL NOT do (escalates instead)

- Resolve contradictions between two pages
- Merge duplicate People pages
- Delete pages from disk
- Rewrite prose
- Promote `_drafts/` pages to final location (that's `/wiki-ingest`'s job)
- Re-verify a "Last verified" date without the user explicitly confirming the re-read

## Step-by-step

1. **Read the most recent `/wiki-lint` output.** If none exists, run lint first.
2. **Categorize each issue** as low-risk-fix or escalate.
3. **Print the proposed plan**: bulleted list of every file that would change and the exact edit. Wait for approval.
4. **Apply.** One file at a time, recording each change in `Knowledge/log.md`.
5. **Re-run `/wiki-lint`** at the end to verify.

## Anti-patterns

- Auto-resolving a contradiction by picking the more recent page
- Bumping `Last verified` without a re-read
- Deleting pages "to clean up"
- Running unattended

## References

- `wiki-lint` — surfaces what this skill fixes
- `wiki-ingest`, `wiki-query` — sister ops
