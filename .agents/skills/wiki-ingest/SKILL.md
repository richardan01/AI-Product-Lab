---
name: wiki-ingest
description: Ingest a new source into the Knowledge wiki — read, summarize, file under the right entity/concept, update index and log. Trigger on "/wiki-ingest <path-or-url>", "ingest this", "file this in the wiki", "add this to knowledge". Implements the Ingest op of the Karpathy LLM-wiki gist.
---

# Wiki ingest — `/wiki-ingest <source>`

**Voice:** Oracle. Citation-disciplined, "as of <date>", refuses to assert without source.

## What this skill does

Takes a single new source (file path or URL) and threads it into the Knowledge wiki. One source typically touches 5–15 pages: a primary summary page, plus updates to existing entity/concept pages where the source corroborates, contradicts, or extends them.

This is the only sanctioned way to add content to `Knowledge/`. Direct file creation outside this skill bypasses index + log discipline and will be flagged by `/wiki-lint`.

## Preconditions

1. `Knowledge/index.md` and `Knowledge/log.md` exist (bootstrap-on-first-run if not).
2. The source is readable: a local file path **or** a public URL.
3. If the source is a transcript, the interviewees are already entries in `Knowledge/People/` — if not, surface and confirm before ingesting.

## Step-by-step

### 1. Read and stage
- Read the full source. Do not skim.
- Extract: title, author/source name, publication or capture date, type (transcript / paper / article / brief / spec / other).
- Stage in `Knowledge/_drafts/<YYYY-MM-DD>-<slug>.md` until the user confirms the framing in step 4.

### 2. Identify touch-points
List every page in `Knowledge/` that this source corroborates, contradicts, or extends. For each:
- New page (need to create) — file path under `People/`, `Reference/`, `Research/`, or `Concepts/`
- Existing page (need to update) — file path + which section
- Index entry (always one new row)

### 3. Draft the primary summary page
Under `Knowledge/Research/` (for transcripts/paper digests) or `Knowledge/Reference/` (for canonical domain docs), draft a page with:
- One-paragraph TL;DR
- Top 3 takeaways with verbatim quote + source line/timestamp
- Open questions surfaced
- Back-links: `## Related` section listing the touched pages

### 4. Confirm with user
Print:
- Primary page draft path + 3 takeaways
- List of touched pages with the proposed delta on each
- One-line summary for `log.md`

Wait for explicit go-ahead before any write outside `_drafts/`.

### 5. Apply
- Move the draft from `_drafts/` to its final location.
- Apply each delta (insert sections, add citations, update "Last verified").
- Add the new row to `Knowledge/index.md` under the correct rubric.
- Append a row to `Knowledge/log.md`.

## Output format

```
## Wiki ingest — <source>

**Primary page:** Knowledge/<path>
**Touch-points:** <n> pages
- [path] — <delta>

**Top 3 takeaways:**
1. <takeaway> — "<verbatim quote>" (source: <line/page>)
2. ...
3. ...

**Open questions raised:**
- <question>

**Log entry:** <one-line>

**Confirm to apply, or revise framing.**
```

## Anti-patterns

- Filing under `Knowledge/` without a back-link to the source (orphan; Lint failure)
- Summarizing without quoting (loses provenance)
- Skipping the user-confirm step
- Adding to existing pages without recording the delta in `log.md`
