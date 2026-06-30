# Workflow: Pre-Publish Gate Dispatch

**Use when:** Any public artifact is about to ship and needs the Batman-layer review gates (essay, post, README, demo script, interview answer, PRD, thread).
**Trigger phrase:** "run the gate" / "gate this" / invoked by `/riddler` + `/vale` composition
**Output:** A merged verdict (SHIP / REVISE / BLOCK) via `Workflows/gate-merge.md`, plus persisted sibling verdict files.

The gate group has **two always-parallel reviewers** and **one conditional escalation**:

```
Always parallel:    Riddler (Opus)  +  Vicki Vale (Sonnet)
Conditional:        Henri Ducard (Opus) — only if Riddler = BLOCK AND depth_gap_flag = true
```

Two modes:
- **Standard gate** — 2 agents (Riddler + Vicki Vale).
- **Depth-escalation gate** — 3 agents (adds Henri Ducard).

---

## Input

| Field | Required | Notes |
|---|---|---|
| `artifact_path` | yes | Path to the artifact under review. |
| `artifact_type` | yes | `essay \| post \| readme \| demo \| interview_answer \| prd \| thread`. |
| `context` | no | What the artifact is for, who it's for. Sharpens both reviews. |

---

## Steps

### Step 0: Pre-flight — claim-source verification and loop cap check

Before spawning any agents, do two checks:

**Loop cap check.** Look for an existing `.riddler-passed` marker sibling to the artifact (e.g. `<artifact_path>.riddler-passed`). If it exists and the pass count recorded inside is 2/2, **stop and escalate to the user** — do not spawn Task A. A third Riddler pass must be explicitly authorized.

**Claim-source map.** For any artifact with quantitative or data-backed claims (κ values, TPR/TNR, n counts, experiment IDs, dates), build a one-line claim-source index:

```
claim: "κ = 0.82"  → source: Evals/regeval/experiments/log.md (gold-cal-v1 row)
claim: "n=42 compliant" → source: Evals/regeval/inputs/gold.jsonl (count)
claim: "relabeled 2 items" → source: Evals/regeval/inputs/corrections-log.md
```

Attach this map to the payload (field: `claim_sources`). Riddler receives the source file excerpts alongside the artifact text so it can verify direction, not just plausibility. If no quantitative claims exist, set `claim_sources: []`.

---

### Step 1: Build the Task Payload

Read the artifact at `artifact_path`. Assemble the payload per `Agents/Gotham/_shared/gate-payload.schema.md`:

```json
{
  "artifact_path": "...",
  "artifact_content": "<full text>",
  "artifact_type": "...",
  "context": "...",
  "resubmission": false,
  "prior_verdicts": []
}
```

On a resubmission, set `resubmission: true` and populate `prior_verdicts` with the earlier `gate-response` objects so agents verify named fixes instead of re-litigating.

Also include the `claim_sources` map from Step 0 in every payload, first dispatch and resubmission alike.

---

### Step 2: Spawn the two reviewers IN PARALLEL

Spawn both in a **single message, two Task calls** — never sequentially:

- **Task A** → `Agents/Gotham/Computer/riddler.md` (Opus) — receives the payload.
- **Task B** → `Agents/Gotham/Computer/vicki-vale.md` (Sonnet) — receives the **identical** payload.

Neither agent sees the other's output. Isolation is enforced by Task context boundaries — this is what makes the two verdicts independent.

---

### Step 3: Await both responses

Collect Task A and Task B `gate-response` objects (schema: `Agents/Gotham/_shared/gate-response.schema.md`). Do not proceed until both have returned.

---

### Step 4: Conditional depth escalation

Check **Riddler's** response only:

```
IF riddler.verdict == "block" AND riddler.depth_gap_flag == true:
    Spawn Task C → Agents/Gotham/Computer/henri-ducard.md (Opus)
      payload = standard payload + riddler_issues (Riddler's issues[] array)
    Await Task C response.
ELSE:
    No third agent. Proceed with 2 responses.
```

Task C **only** spawns after Task A has returned, and **only** when the flag is set. Never spawn Ducard speculatively or in parallel with A/B.

Ducard receives Riddler's issues by design — he triages whether the depth gap is a quick re-drill (`cleared`) or real study (`drill-required`). His verdict is **additive**; it never changes the overall verdict (Riddler already returned BLOCK).

---

### Step 5: Merge

Pass all responses (2 or 3) to `Workflows/gate-merge.md` for the side-by-side merged verdict.

---

## Constraints

- **Tasks A and B spawn simultaneously, never sequentially.** Parallelism is the point — the two reviews must not influence each other's timing or content.
- **Task C only spawns after Task A returns, and only on the flag.** Never speculative.
- **Identical payload to A and B.** Any divergence breaks isolation comparability.
- **One response per spawned agent.** No agent runs twice in a single dispatch (resubmission is a fresh dispatch).
- **Loop cap inherited from Riddler:** max 2 Riddler passes per artifact across resubmissions; a third BLOCK escalates to the user rather than auto-redispatching.

---

## See also

- `Agents/Gotham/_shared/gate-payload.schema.md` — payload contract
- `Agents/Gotham/_shared/gate-response.schema.md` — response contract
- `Workflows/gate-merge.md` — verdict merge logic
