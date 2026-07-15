---
name: riddler
description: Run the Riddler adversarial review gate on a public artifact. Trigger on "/riddler <artifact>", "Riddler review this", or "adversarial review this before publishing".
disable-model-invocation: true
---

# Riddler review — `/riddler <artifact>`

Read the artifact and review it as The Riddler: find weak claims, hidden assumptions, unsupported jumps, and places a critical reader can puncture the argument.

## Output

- Verdict: Pass / Revise / Block
- Weakest claim
- Missing evidence
- Highest-leverage revision
- One-line publish decision

## Close the loop (mandatory — verdict must persist)

After delivering the review, persist the verdict so the publish gate (`Tools/gate-check.sh`) can see it:

**On Pass (or Conditional Pass):**
1. Write the per-artifact verdict file `<artifact-path>.riddler-passed` in the same directory as the artifact, per `_Registry/reviewer-verdict-schema.md`:
   ```
   Gate:     riddler
   File:     <reviewed file path>
   Date:     YYYY-MM-DD
   Verdict:  PASS | CONDITIONAL
   Hash:     <first 12 chars of sha256 of the reviewed file — `shasum -a 256 <file>`>
   Reviewed-by: agent:riddler
   ```
   followed by the review scorecard (weakest claim / missing evidence / decision).
2. Arm the gate: write the same header block to `_Registry/.riddler-passed`. This is what unblocks Write to `Artifacts/`. It is cleared by `Workflows/gate-merge.md` after the artifact is staged — never leave it armed across artifacts.

**On Revise or Block:**
- Do NOT write either marker (rule 1 of the verdict schema: no verdict file on FAIL).
- On Block, write `<artifact-path>.riddler-blocked-YYYY-MM-DD.md` containing the specific fixes required.

Never edit an existing verdict file; a re-review writes a new one with a date suffix.
