# Workflow — Memory Consolidation

**Cadence:** Monthly (first Sunday of each month)
**Owner:** Alfred (runs the audit) + [Your Name] (approves promotions)
**Purpose:** Prevent drift between Cowork auto-memory (fast-write cache) and AIPM-OS Knowledge (canonical source of truth)

---

## The two-system design

These systems have different jobs. Overlap = drift risk.

| System | Location | Purpose | Who writes |
|--------|----------|---------|------------|
| **Cowork auto-memory** | `~/.claude/.../memory/` | Fast-write cache — day-job context, meeting outcomes, formatting preferences, stakeholder updates | Claude (automatic) |
| **AIPM-OS Knowledge/** | `Knowledge/People/`, `Knowledge/Reference/`, `Knowledge/Concepts/` | Canonical source of truth — AI PM mission, public-facing work, stable stakeholder profiles | [Your Name] (deliberate) |

**Rule on conflict: AIPM-OS wins. Always.**

---

## Domain ownership (what goes where — no overlap)

### Cowork auto-memory ONLY
- Day-job meeting outcomes and decisions
- Formatting and response preferences (bullets, emojis, P0/P1/P2)
- Day-job stakeholder updates
- Short-term project state (blockers, action items, dates)

### AIPM-OS Knowledge ONLY
- AI PM mission contacts and network (Anthropic staff, hiring managers)
- Canonical company context that doesn't change weekly (`Knowledge/Reference/`)
- PM frameworks, patterns, concepts (`Knowledge/Concepts/`)
- Public artifact drafts and interview prep

### Either (promote if recurring or high-stakes)
- Decisions that cross both layers (e.g. CDP as AI PM portfolio signal)
- Stakeholder facts that matter for interview stories (e.g. a day-job manager's AI initiative = Bruce Wayne signal)

---

## Monthly consolidation steps

### Step 1 — Scan Cowork auto-memory (15 min)
Read all entries in `MEMORY.md`. Flag any entry that:
- [ ] Contradicts a `Knowledge/People/` or `Knowledge/Reference/` file → **update AIPM-OS to match**
- [ ] Contains AI PM mission signal (RegEval, Bruce Wayne, frontier-lab contacts) → **promote to AIPM-OS Knowledge**
- [ ] Is stale (project completed, decision superseded) → **archive or delete**
- [ ] Duplicates an AIPM-OS file → **delete from Cowork, keep AIPM-OS**

### Step 2 — Scan AIPM-OS Knowledge (10 min)
- [ ] `Knowledge/People/team.md` — does it match Cowork stakeholder memories? Update if diverged.
- [ ] `Knowledge/Concepts/pm-decisions-log.md` — are recent CDP decisions logged here in PD-TOL? Promote from Cowork if not.
- [ ] `Knowledge/Reference/` — is anything out of date?

### Step 3 — Promote cross-layer decisions (10 min)
For any Cowork memory tagged as CDP + AI PM signal:
- Write a PD-TOL entry in `Knowledge/Concepts/pm-decisions-log.md`
- Update `Skills/cdp-to-ai-pm-bridge.md` if it adds a new interview story

### Step 4 — Log the audit
Add one line to the bottom of this file:
```
YYYY-MM-DD audit: N entries reviewed, N promoted, N deleted, N conflicts resolved
```

---

## Conflict resolution protocol

When Cowork memory contradicts AIPM-OS:

1. Check which is more recent
2. Check which has primary source evidence (meeting file, decision doc)
3. **AIPM-OS wins** unless Cowork has more recent primary source evidence
4. Update the losing system to match

---

## Audit log

_Add entries below after each monthly run._

---

## Related

[[CLAUDE.md]] · [[Knowledge/Concepts/pm-decisions-log]] · [[Skills/cdp-to-ai-pm-bridge]] · [[Workflows/index]]
