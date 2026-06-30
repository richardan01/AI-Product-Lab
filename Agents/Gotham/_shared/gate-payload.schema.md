# Gate Payload Schema

The **Task Payload** every gate agent receives when spawned by `Workflows/gate-dispatch.md`.

Every gate agent in a standard gate receives the **identical** payload — Riddler and Vicki Vale see exactly the same input. No agent sees another agent's output before returning its own verdict; isolation is enforced by Task tool context boundaries. The one exception is Henri Ducard in a depth-escalation gate, who additionally receives `riddler_issues` (see below) — by design, because his job is to triage the depth gap Riddler already found, not to re-derive it.

> **Related, not duplicate:** This schema is the *in-flight input* a gate agent receives in-context. The *persisted* verdict file an agent writes (e.g. `.riddler-passed`) follows the loose sibling-file convention described in each agent file, and is conceptually adjacent to `_Registry/reviewer-verdict-schema.md` (the format for skill-gate verdict files like `<artifact>.peer-review-passed`). Keep the two layers distinct: payload/response = in-flight JSON between dispatcher and agent; verdict file = persisted artifact sibling.

## Standard payload (all gate agents)

```json
{
  "artifact_path": "string — path to the artifact under review",
  "artifact_content": "string — full text of the artifact",
  "artifact_type": "essay | post | readme | demo | interview_answer | prd | thread",
  "context": "string (optional) — what this artifact is for, who it's for",
  "resubmission": false,
  "prior_verdicts": []
}
```

### Field notes

| Field | Required | Notes |
|---|---|---|
| `artifact_path` | yes | Used to site the verdict file sibling on return. |
| `artifact_content` | yes | Full text. Agents review content, not a re-read from disk, so the reviewed bytes are pinned. |
| `artifact_type` | yes | Shapes what each agent weights — e.g. Vicki Vale reads a `readme` opener differently from an `interview_answer`. |
| `context` | no | Audience + purpose. "Frontier-lab hiring manager, flagship repo README." Sharpens both reviews. |
| `resubmission` | yes | `true` when the artifact returns after a prior BLOCK/REVISE. Signals agents to check whether named fixes were made. |
| `prior_verdicts` | yes | Array of prior `gate-response` objects (empty on first pass). On resubmission, lets an agent verify its earlier issues were addressed rather than re-litigating from scratch. |

## Depth-escalation addendum (Henri Ducard only)

When `gate-dispatch` spawns Ducard (Task C), the payload carries one extra field:

```json
{
  "...standard payload fields...",
  "riddler_issues": [
    {
      "severity": "blocking | major | minor",
      "location": "exact sentence or paragraph reference",
      "description": "what is wrong",
      "fix": "specific edit required"
    }
  ]
}
```

`riddler_issues` is the `issues[]` array from Riddler's BLOCK response. Ducard receives it so the drill is targeted at the specific depth gap, not a generic survey. This is the **only** cross-agent context sharing in the gate group, and it flows one direction only (Riddler → Ducard), after Riddler's verdict is already locked.

## See also

- `Agents/Gotham/_shared/gate-response.schema.md` — what agents return
- `Workflows/gate-dispatch.md` — who builds and routes this payload
- `_Registry/reviewer-verdict-schema.md` — persisted verdict-file format (separate layer)
