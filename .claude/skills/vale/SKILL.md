---
name: vale
description: Run the Vicki Vale reader-voice review gate on a public artifact. Trigger on "/vale <artifact>", "/vicki <artifact>", "reader review this", or "where will the reader stop reading".
disable-model-invocation: true
---

# Vicki Vale review — `/vale <artifact>`

Read the artifact as a skeptical but fair target reader. Find where attention drops, what feels unclear, and what needs sharper human stakes.

## Output

- Verdict: Pass / Revise / Block
- First likely drop-off point
- Confusing or flat section
- Reader question left unanswered
- Highest-leverage revision

## Close the loop (mandatory — verdict must persist)

After delivering the review, persist the verdict so the publish gate (`Tools/gate-check.sh`) can see it:

**On Pass (or Conditional Pass):**
1. Write the per-artifact verdict file `<artifact-path>.vicki-passed` in the same directory as the artifact, per `_Registry/reviewer-verdict-schema.md`:
   ```
   Gate:     vale
   File:     <reviewed file path>
   Date:     YYYY-MM-DD
   Verdict:  PASS | CONDITIONAL
   Hash:     <first 12 chars of sha256 of the reviewed file — `shasum -a 256 <file>`>
   Reviewed-by: agent:vicki-vale
   ```
   followed by the review scorecard (drop-off point / unanswered question / revision).
2. Arm the gate: write the same header block to `_Registry/.vicki-passed`. This is what unblocks Write to `Artifacts/`. It is cleared by `Workflows/gate-merge.md` after the artifact is staged — never leave it armed across artifacts.

**On Revise or Block:**
- Do NOT write either marker (rule 1 of the verdict schema: no verdict file on FAIL).
- On Block, write `<artifact-path>.vicki-blocked-YYYY-MM-DD.md` containing the specific fixes required.

Never edit an existing verdict file; a re-review writes a new one with a date suffix.
