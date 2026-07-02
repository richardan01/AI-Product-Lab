# Workflows — index

Executable process specs. Each workflow defines trigger, inputs, steps, and outputs. Invoke by naming the workflow in a session or referencing it in an agent handoff.

---

## Workflows

| Workflow | Trigger | Who invokes | Related agents |
|---|---|---|---|
| [[Workflows/gate-dispatch\|gate-dispatch]] | Any public artifact ready for review | Nightwing, Lucius Fox | [[Agents/Gotham/Computer/riddler]], [[Agents/Gotham/Computer/vicki-vale]], [[Agents/Gotham/Computer/henri-ducard]] |
| [[Workflows/gate-merge\|gate-merge]] | After gate-dispatch returns 2-3 verdicts | gate-dispatch orchestrator | [[Agents/Gotham/Computer/riddler]], [[Agents/Gotham/Computer/vicki-vale]] |
| [[Workflows/regeval-run\|regeval-run]] | RegEval experiment iteration | Lucius Fox | [[Agents/Gotham/Computer/lucius-fox]] |
| [[Workflows/memory-consolidation\|memory-consolidation]] | Monthly (first Sunday) | Alfred | [[Agents/Gotham/Computer/alfred]] |
| [[Workflows/quarterly-planning/workflow-spec\|quarterly-planning]] | Quarter start or thesis needs revision | Bruce Wayne, Alfred | [[Agents/Gotham/Computer/bruce-wayne]], [[Agents/Gotham/Computer/alfred]] |
| [[Workflows/roadmap-review/workflow-spec\|roadmap-review]] | Weekly Sunday review | Bruce Wayne | [[Agents/Gotham/Computer/bruce-wayne]] |
| [[Workflows/user-research-synthesis/workflow-spec\|user-research-synthesis]] | After ≥3 research sources collected | Oracle | [[Agents/Gotham/Computer/oracle]] |
| [[Workflows/interactive-onboarding\|interactive-onboarding]] | Fresh clone of OS | New user | — |

## Utility

| Workflow | Purpose |
|---|---|
| [[Workflows/github-account-switch\|github-account-switch]] | Switch between personal and work GitHub |

---

## Gate workflow anatomy

The gate pipeline for public artifacts:

```
Nightwing / Lucius Fox signals "ready to ship"
  → gate-dispatch spawns Task A (Riddler) + Task B (Vicki Vale) in parallel
  → if Riddler.block AND Riddler.depth_gap_flag → Task C (Henri Ducard) spawns
  → gate-merge combines verdicts → SHIP / REVISE / BLOCK
```

Schemas: [[Agents/Gotham/_shared/gate-payload.schema]] · [[Agents/Gotham/_shared/gate-response.schema]]

---

## Related

[[Agents/agent-system-architecture]] · [[Evals/index]] · [[Tasks/active]]
