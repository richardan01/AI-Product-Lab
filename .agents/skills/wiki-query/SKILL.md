---
name: wiki-query
description: Synthesize an answer from the Knowledge wiki across multiple pages, cite sources inline, file good answers back as new wiki pages. Trigger on "/wiki-query <question>", "what does the wiki say about", "synthesize from the wiki", "knowledge query". Implements the Query op of the Karpathy LLM-wiki gist — explorations compound like ingested sources.
---

# Wiki query — `/wiki-query <question>`

**Voice:** Oracle. Three signals beat twelve. Refuses to assert without a wiki citation.

## What this skill does

Answers a question by synthesizing across the wiki. Every good answer is **filed back as a new wiki page** — explorations compound like ingested sources.

## Step-by-step

### 1. Decompose the question
Break the question into 2–5 sub-queries, each anchored on an entity or concept that should exist in the wiki.

### 2. Search the wiki
For each sub-query: identify candidate pages in `Knowledge/` (use `index.md` first, then targeted Grep). Read relevant sections. Note: page path, exact passage cited, and "Last verified" date.

If a sub-query has no answer in the wiki, surface it as a **gap** — do not improvise from outside knowledge. Suggest `/wiki-ingest` for the missing source.

### 3. Synthesize
- A 2–4 sentence headline answer.
- A bulleted reasoning chain, each bullet citing a wiki page (path) and a verbatim phrase or fact.
- An "Unknowns" section listing what the wiki cannot answer yet.
- A "Stale check" flag if any cited page has `Last verified` > 90 days old.

### 4. File the answer back
If the answer is non-trivial (≥ 3 sources, or surfaces a synthesis not previously written down), file it as a new page under `Knowledge/Concepts/<slug>.md`. If trivial — single citation, no synthesis — do NOT file.

## Output format

```
## Wiki query — <question>

**Headline:** <2–4 sentences>

**Reasoning:**
- <claim> — `Knowledge/<path>` "<verbatim phrase>" (verified <date>)

**Unknowns (gaps in the wiki):**
- <gap> — suggest `/wiki-ingest <source candidate>`

**Stale citations:**
- `Knowledge/<path>` — last verified <date>, > 90 days old

**Filed as:** `Knowledge/Concepts/<slug>.md` (or "not filed — trivial single-source answer")
```

## Anti-patterns

- Answering from outside knowledge without flagging "(not in wiki)"
- Filing every answer as a new page (only file synthesis-grade ones)
- Citing a page without quoting from it

## References

- Karpathy LLM-wiki gist — Query is op #2 of 4
- `wiki-ingest`, `wiki-lint`, `wiki-maintain` — sister ops
