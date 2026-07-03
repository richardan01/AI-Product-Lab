# Workflow — Memory Consolidation

**Cadence:** Monthly (first Sunday of each month)
**Owner:** Alfred (runs the audit) + [Your Name] (approves promotions)
**Purpose:** Prevent drift between runtime auto-memory (fast-write cache) and AI Product Lab Knowledge (canonical source of truth)

---

## The two-system design

These systems have different jobs. Overlap = drift risk.

| System | Location | Purpose | Who writes |
|--------|----------|---------|------------|
| **Runtime auto-memory** | `~/.claude/.../memory/` | Fast-write cache — session facts, formatting preferences, short-term project state | Claude (automatic) |
| **AI Product Lab Knowledge/** | `Knowledge/People/`, `Knowledge/Reference/` (both local/gitignored), `Knowledge/Concepts/` | Canonical source of truth — AI PM mission, public-facing work, stable contact profiles | [Your Name] (deliberate) |

**Rule on conflict: AI Product Lab wins. Always.**

---

## Domain ownership (what goes where — no overlap)

### Runtime auto-memory ONLY
- Formatting and response preferences (bullets, emojis, P0/P1/P2)
- Short-term project state (blockers, action items, dates)
- Session-scoped facts that expire within the sprint

### AI Product Lab Knowledge ONLY
- AI PM mission contacts and network (frontier-lab staff, hiring managers)
- Canonical reference context that doesn't change weekly (`Knowledge/Reference/`)
- PM frameworks, patterns, concepts (`Knowledge/Concepts/`)
- Public artifact drafts and interview prep

### Either (promote if recurring or high-stakes)
- Decisions with lasting AI PM portfolio signal
- Stakeholder facts that matter for interview stories

---

## Monthly consolidation steps

### Step 1 — Scan runtime auto-memory (15 min)
Read all entries in `MEMORY.md`. Flag any entry that:
- [ ] Contradicts a `Knowledge/People/` or `Knowledge/Reference/` file → **update AI Product Lab to match**
- [ ] Contains AI PM mission signal (RegEval, Bruce Wayne, frontier-lab contacts) → **promote to AI Product Lab Knowledge**
- [ ] Is stale (project completed, decision superseded) → **archive or delete**
- [ ] Duplicates an AI Product Lab file → **delete from auto-memory, keep AI Product Lab**

### Step 2 — Scan AI Product Lab Knowledge (10 min)
- [ ] `Knowledge/People/` — do profiles match auto-memory? Update if diverged.
- [ ] `Knowledge/Concepts/pm-decisions-log.md` (local, gitignored) — are recent durable decisions logged here in PD-TOL? Promote from auto-memory if not.
- [ ] `Knowledge/Reference/` — is anything out of date?

### Step 3 — Promote durable decisions (10 min)
For any auto-memory entry tagged as durable AI PM signal:
- Write a PD-TOL entry in `Knowledge/Concepts/pm-decisions-log.md`
- Note it in the relevant interview-prep material if it adds a new story

### Step 4 — Log the audit
Add one line to the bottom of this file:
```
YYYY-MM-DD audit: N entries reviewed, N promoted, N deleted, N conflicts resolved
```

---

## Conflict resolution protocol

When runtime auto-memory contradicts AI Product Lab:

1. Check which is more recent
2. Check which has primary source evidence (meeting file, decision doc)
3. **AI Product Lab wins** unless auto-memory has more recent primary source evidence
4. Update the losing system to match

---

## Audit log

_Add entries below after each monthly run._

---

## Related

[[CLAUDE.md]] · [[Knowledge/Concepts/pm-decisions-log]] · [[Workflows/index]]
