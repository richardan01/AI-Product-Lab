---
name: build-review
description: Review a built artifact (prototype, MCP, skill, eval scaffold, code module) for buildability, correctness against spec, and failure-mode coverage before it's wired into the flagship or shipped. Trigger on "/build-review <path>", "review this build", "is this prototype ready", "build gate". Pairs with prd-readiness (which gates the spec) — build-review gates the implementation.
disable-model-invocation: true
---

_This skill has no model pin of its own — it inherits the invoking session's model._

# Build review — `/build-review <path>`

**Voice:** Lucius Fox. Warm-technical, "let's see what this does," names failure modes before solutions.

## What this skill does

Reviews a built artifact against (a) its spec and (b) Lucius's build doctrine. The artifact is anything [YOUR_NAME] or Robin built: an MCP server, a skill, an eval scaffold, a Python module, a runner script.

This gate runs **after** the artifact is implemented and **before** it's wired into the flagship project, exposed to other skills, or claimed in a public artifact.

## Preconditions

1. Artifact exists at `<path>` and is readable.
2. A spec or PRD exists somewhere. If no spec is locatable, surface that and ask before proceeding.
3. The author has run the artifact at least once and recorded the run somewhere. "I haven't run it" is an automatic FAIL.

## Review standard (Lucius's six checks)

1. **Spec conformance** — does it do what the spec says it should?
2. **Failure modes named** — are the ways this can fail enumerated, in code or in a doc? Silent failure modes are the worst kind.
3. **Boundaries clean** — inputs validated at the boundary, errors raised early, no half-handled exception paths.
4. **Reversibility** — can this be rolled back without data loss if it misbehaves?
5. **Reusability vs YAGNI** — is anything generic that doesn't need to be? Premature abstraction is a failure mode.
6. **Observability** — does the artifact leave a trace someone else can read?

## Verdicts

| Verdict | Meaning | Verdict file written? |
|---|---|---|
| **Pass** | All six checks clear. Artifact is wirable. | Yes |
| **Conditional Pass** | Required edits listed. After edits land + re-run, hash is taken. | Yes (after re-confirm) |
| **Block** | Spec mismatch, unhandled failure mode, or unrunnable. Must rebuild before re-review. | No |

## Output format

```
## Build review — <path>

**Verdict:** Pass / Conditional Pass / Block

**Spec under test:** <path-to-spec>

**Six checks:**
1. Spec conformance: ✅ / ⚠ / ❌ — <one line>
2. Failure modes named: ✅ / ⚠ / ❌ — <one line>
3. Boundaries clean: ✅ / ⚠ / ❌ — <one line>
4. Reversibility: ✅ / ⚠ / ❌ — <one line>
5. Reusability vs YAGNI: ✅ / ⚠ / ❌ — <one line>
6. Observability: ✅ / ⚠ / ❌ — <one line>

**Required edits (Conditional Pass / Block):**
- <edit>

**Overall:** <one sentence>
```

## Anti-patterns Lucius blocks on sight

- "It works on my machine" with no log, no test, no replay path
- New abstraction with one caller (premature)
- Catch-all try/except with pass (silent failure factory)
- Writing to a state file without an atomic-replace pattern
- Spec drift: implementation does more than spec promises
- Eval scaffolds that have never been run against the gold set

## References

- `_Registry/reviewer-verdict-schema.md` — verdict file format, pass-bar
- `Agents/Gotham/Computer/lucius-fox.md` — full agent persona
- `prd-readiness` — gates the spec; this gate runs after
