# Gate Response Schema

The **Response** every gate agent returns to `Workflows/gate-dispatch.md` after reviewing the artifact.

This is the **in-flight JSON** contract between a gate agent and the dispatcher. It is distinct from the *persisted* sibling verdict file (`.riddler-passed`, `.vicki-bounced`, etc.) that the agent also writes — the response's `verdict_file` field points to that persisted file. For the persisted skill-gate format, see `_Registry/reviewer-verdict-schema.md`; this gate-group response is a separate, lighter layer used only for live orchestration.

## Response

```json
{
  "agent": "riddler | vicki-vale | henri-ducard",
  "verdict": "pass | conditional | block | read | skim | bounce | drill-required | cleared",
  "issues": [
    {
      "severity": "blocking | major | minor",
      "location": "exact sentence or paragraph reference",
      "description": "what is wrong",
      "fix": "specific edit required — never vague"
    }
  ],
  "depth_gap_flag": false,
  "verdict_file": ".riddler-passed | .riddler-blocked-<ts> | .vicki-passed | .vicki-bounced | null"
}
```

> **`depth_gap_flag` is a Riddler-only field.** It appears in the response **only when `agent == "riddler"`**. Vicki Vale and Henri Ducard **omit it entirely** — they do not own the escalation signal, so they must not carry it (not even as `false`). Validation rule: `depth_gap_flag` present ⟹ `agent == "riddler"`. The dispatcher and merger read it solely from Riddler's response.

## Verdict vocabulary by agent

Each agent uses its own verdict axis. The merger (`Workflows/gate-merge.md`) maps these to the overall SHIP / REVISE / BLOCK.

| Agent | Verdict values | Axis |
|---|---|---|
| `riddler` | `pass` · `conditional` · `block` | Argument strength, claim defensibility |
| `vicki-vale` | `read` · `skim` · `bounce` | Reader attention — does the artifact earn the read |
| `henri-ducard` | `drill-required` · `cleared` | Technical-depth gap fixability (conditional gate only) |

## Field rules

| Field | Rule |
|---|---|
| `agent` | Identifies the returning agent. One response per spawned agent. |
| `verdict` | One value from that agent's axis above. |
| `issues[]` | Every issue must have a **specific, actionable `fix`**. "This section is weak" is invalid; "the claim in para 4 needs the eval name + dataset + TPR or remove it" is valid. Vicki Vale's bounce issue names the **exact stop-sentence**. |
| `depth_gap_flag` | **Riddler-only field.** Present only when `agent == "riddler"`; set `true` only when a BLOCK is driven by a technical-depth gap (the sole trigger that spawns Henri Ducard). Vicki Vale and Ducard **omit the field entirely** — they do not own the escalation signal. |
| `verdict_file` | Path to the persisted sibling verdict file the agent wrote. Explicitly `null` for additive agents that don't persist a gate sibling: Vicki Vale may inline her verdict, and Henri Ducard logs to `drill-log.md` rather than a gate file. `null` is a valid, documented value for these agents — not a malformed response. |

## depth_gap_flag — the escalation trigger

`depth_gap_flag: true` on a Riddler `block` is the **only** condition that causes `gate-dispatch` to spawn a third agent (Henri Ducard). The merger checks this field before deciding whether a third Task is needed.

- Riddler returns `block` because a claim is **unsupported but fixable with sourcing** → `depth_gap_flag: false` (no Ducard; author just adds the citation).
- Riddler returns `block` because a claim reflects a **genuine technical-depth gap** the author can't defend under follow-up → `depth_gap_flag: true` (spawn Ducard to triage whether it's a quick re-drill or real study).

## Ducard's verdict is additive

When Ducard runs, Riddler has already returned `block`, so the overall verdict is **already BLOCK**. Ducard's `drill-required` / `cleared` never upgrades or downgrades that — it only annotates **WHAT TO FIX**:

- `cleared` → the gap is a quick re-drill; author can likely close it and resubmit fast.
- `drill-required` → real study needed before resubmission; the fix is not cosmetic.

## See also

- `Agents/Gotham/_shared/gate-payload.schema.md` — what agents receive
- `Workflows/gate-merge.md` — how these responses combine into one verdict
- `_Registry/reviewer-verdict-schema.md` — persisted verdict-file format (separate layer)
