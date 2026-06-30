---
name: wiki-lint
description: Health-check the Knowledge wiki — surface orphans, contradictions, stale claims, and missing cross-references. Trigger on "/wiki-lint", "lint the wiki", "wiki health check", "knowledge audit". Implements the Lint op of the Karpathy LLM-wiki gist — keeps the wiki healthy as it scales. Run weekly.
---

# Wiki lint — `/wiki-lint`

**Voice:** The Riddler. Adversarial sweep — finds drift, calls it out without softening.

## What this skill does

Walks the entire `Knowledge/` tree and reports failures across five categories. Lint **never auto-fixes** — it surfaces, you decide. (`/wiki-maintain` is the fixer skill.)

## When to run

- Weekly (Sunday) as part of the retro cadence
- After any `/wiki-ingest` batch that touched ≥ 5 pages
- Before any decision doc that claims "the wiki says X"
- Before publishing the OS as an open-source template (gates the README)

## The five lint categories

### 1. Orphans
A page reachable from no other page (and absent from `index.md`).

### 2. Contradictions
Two pages making conflicting claims with no resolution note.

### 3. Stale claims
Pages with `Last verified` older than 90 days, or with no `Last verified` field at all.

### 4. Broken cross-references
A back-link to a page that no longer exists, or a citation to a section that has been renamed.

### 5. Index drift
`index.md` lists a page that doesn't exist on disk, or omits a page that does.

## Method

1. Parse `Knowledge/index.md` to get the canonical page list.
2. Walk `Knowledge/` filesystem to get the actual page list.
3. Diff (1) and (2) → Index drift.
4. For each on-disk page: extract `Last verified`, inbound links, outbound links → Stale + Broken refs.
5. Compute reachability graph from `index.md` → Orphans.
6. Cross-read pages that share entities/concepts → Contradictions (flag for human read, do not auto-resolve).

## Output format

```
## Wiki lint — <date>

**Total pages scanned:** <n>
**Failures by category:**
- Orphans: <n>
- Contradictions: <n>
- Stale claims: <n>
- Broken cross-references: <n>
- Index drift: <n>

### Orphans
- <list>

### Contradictions
- <list>

### Stale claims
- <list>

### Broken cross-references
- <list>

### Index drift
- <list>

**Recommended next:** `/wiki-maintain` to apply low-risk fixes; manual resolution for contradictions.
```

## What Lint does NOT do

- Does not fix anything (that's `/wiki-maintain`)
- Does not write to pages
- Does not delete files

Surfacing is the job. The user picks resolution.

## References

- `wiki-maintain` — the fixer that pairs with this surfacer
