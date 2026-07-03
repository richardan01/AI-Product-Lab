# Workflow: Pre-Publish Gate Merge

**Use when:** `Workflows/gate-dispatch.md` has collected all gate responses (2 or 3) and needs one combined verdict.
**Input:** Array of `gate-response` objects (Riddler + Vicki Vale, plus Henri Ducard if the depth-escalation path fired).
**Output:** A single side-by-side verdict block — SHIP / REVISE / BLOCK — with every agent's verdict visible.

**Merge principle: surface all verdicts side-by-side. Never hide the disagreement.** If Riddler passes but Vicki Vale bounces, both are shown and the overall verdict reflects the stricter signal, with Vale's exact stop-sentence listed.

---

## Output structure

```
┌──────────────────────────────────────────┐
│  OVERALL VERDICT:  SHIP | REVISE | BLOCK  │
└──────────────────────────────────────────┘

Riddler:     pass | conditional | block
Vicki Vale:  read | skim | bounce
Henri Ducard (if spawned):  drill-required | cleared

COMBINED ISSUES (deduplicated, ranked by severity):
  🔴 Blocking: [list]
  🟡 Major:    [list]
  ⚪ Minor:    [list]

WHAT TO FIX (numbered, specific, assignable to Nightwing / Robin):
  1. ...
  2. ...
```

---

## Steps

### Step 1: Lay out each agent's verdict side-by-side

One line per agent that returned. Always show Riddler and Vicki Vale. Show Henri Ducard only if he was spawned. Do not collapse or reconcile differing verdicts — show them as they came back.

### Step 2: Deduplicate and rank issues

Merge `issues[]` across all responses. When two agents flag the same location, keep one entry and note both agents. Rank by severity: 🔴 blocking → 🟡 major → ⚪ minor.

### Step 3: Compute the overall verdict

```
SHIP    →  Riddler == pass   AND  Vale == read
REVISE  →  any conditional  OR  skim  OR  bounce  OR  (issues present but all minor)
BLOCK   →  any block  OR  Riddler.depth_gap_flag == true
```

Evaluate in precedence **BLOCK > REVISE > SHIP** — any BLOCK condition wins regardless of other verdicts.

**CONDITIONAL fast-path.** When Riddler returns CONDITIONAL and all conditions are mechanical fixes (add a number, name a handle, correct a label — no new argument required), apply them in-line, verify each condition is met, and flip the verdict to PASS without re-dispatch. Document the conditions and their resolutions in the `.riddler-passed` marker file with the pass count. Use this path only when no condition requires new reasoning or new content. If any condition requires rewriting an argument or adding a claim, treat as REVISE and re-dispatch.

`depth_gap_flag` is read **only from Riddler's response** (it's Riddler-only by schema). Ignore the field on any other agent's response — this guards the verdict against an agent that misfills it.

**Ducard is additive only.** When he was spawned, Riddler already returned BLOCK, so the overall is already BLOCK. His verdict never upgrades that — `cleared` vs `drill-required` only shapes WHAT TO FIX priority (quick re-drill vs. real study).

### Step 4: Write WHAT TO FIX

Numbered, specific, each item assignable to Nightwing (rewrite) or Robin (mechanical fixes). Pull the `fix` field verbatim from each issue — never restate as vague guidance. If Vicki Vale bounced, item 1 is her exact stop-sentence and the rewrite she suggested.

### Step 5: Route the verdict

**On SHIP (or CONDITIONAL fast-path → SHIP):** proceed to gate disarm below.

**On REVISE:** route the numbered WHAT TO FIX list to Nightwing (rewrites) or Robin (mechanical fixes). When all items are applied, re-invoke `gate-dispatch.md` with `resubmission: true` and `prior_verdicts` populated. The loop cap counter increments on every Riddler re-dispatch — check it in gate-dispatch Step 0 before spawning.

**On BLOCK:** same routing as REVISE, but flag the loop cap. If this was pass 2/2, do not re-dispatch — present the BLOCK and escalate to the user with the specific depth gap or structural issue that needs resolution. The escalation format is: a one-paragraph summary of what failed and why a third automated pass won't resolve it.

---

### Step 6: Disarm the gate after staging (SHIP only)

On SHIP, the reviewer skills have already armed the publish gate (`_Registry/.riddler-passed` + `_Registry/.vicki-passed` — written by `/riddler` and `/vale` per `_Registry/reviewer-verdict-schema.md`). After the final artifact is written into `Artifacts/`:

1. Confirm the per-artifact verdict files (`<artifact>.riddler-passed`, `<artifact>.vicki-passed`) sit next to the staged artifact — they are the permanent audit trail.
2. Delete `_Registry/.riddler-passed` and `_Registry/.vicki-passed` to re-arm the gate for the next artifact. **Never leave the global markers in place** — an armed gate lets any file ship without review.
3. Log the ship in `_Registry/artifact-log.md` (one line: date · artifact path · Riddler verdict · Vale verdict · notes). If the file does not exist, create it with this header first:
   ```
   | Date shipped | Artifact path | Riddler | Vicki Vale | Notes |
   |---|---|---|---|---|
   ```

On REVISE or BLOCK, the markers should not exist; if a stale one does, delete it.

---

## Disagreement examples

| Riddler | Vale | Ducard | Overall | Why |
|---|---|---|---|---|
| pass | read | — | **SHIP** | Both gates clear. |
| pass | bounce | — | **REVISE** | Argument holds, but the reader stops. List Vale's stop-sentence as fix #1. |
| conditional | read | — | **REVISE → SHIP** | If all conditions are mechanical, apply in-line and fast-path to SHIP. If any require new reasoning, treat as REVISE and re-dispatch. |
| block | read | cleared | **BLOCK** | Riddler blocks on a depth gap; Vale liked it anyway. Ducard says the gap is a quick re-drill. |
| block | bounce | drill-required | **BLOCK** | Everything fails. Ducard flags real study needed; prioritize the depth gap in WHAT TO FIX. |

---

## See also

- `Workflows/gate-dispatch.md` — spawns the agents and routes responses here
- `Agents/Gotham/_shared/gate-response.schema.md` — the response objects being merged
