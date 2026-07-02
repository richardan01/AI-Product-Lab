# Artifacts — gated public-artifact staging area

Final, gate-passed public artifacts are staged here before they ship (repo push, post, publish). Nothing lands in this folder without passing **both** pre-publish gates:

- **Riddler** — adversarial review (`/riddler`, or via `Workflows/gate-dispatch.md`)
- **Vicki Vale** — reader-voice review (`/vale`)

## How the gate is enforced

A PreToolUse hook in `.claude/settings.json` runs `Tools/gate-check.sh` on every Write/Edit. Writes into `Artifacts/` are **blocked** unless both global gate markers are armed:

```
_Registry/.riddler-passed
_Registry/.vicki-passed
```

The markers are written by the reviewer skills on PASS/CONDITIONAL (per `_Registry/reviewer-verdict-schema.md`) and deleted by `Workflows/gate-merge.md` after the artifact is staged — so a stale pass can never ship the next artifact.

## Conventions

- Staged files are named `YYYY-MM-DD_<slug>_gate-passed.md` under a type folder (e.g. `strategy-docs/`).
- Per-artifact verdict files (`<artifact>.riddler-passed`, `<artifact>.vicki-passed`) sit next to the staged artifact as the permanent audit trail.
- Every ship is logged in `_Registry/artifact-log.md`.
- Staged personal artifacts (LinkedIn rewrites, launch posts) are kept out of the public repo by local convention; this folder ships with structure + audit trail, not private drafts.
