<!-- The Quality gates workflow enforces these automatically. This checklist is
     the human pre-flight — tick before requesting merge. See CLAUDE.md § Quality gates. -->

## What & why

<!-- One or two lines: what changed and the reason. -->

## Gate checklist

- [ ] **Residue-clean** — no employer / day-job / PII residue, no `[Your name]` placeholders (`scripts/check-repo.sh` green).
- [ ] **Artifacts gated** — any file added under `Artifacts/` ships with fresh `.riddler-passed` + `.vicki-passed` sidecars, hashes match current content (`scripts/verify-artifact-gates.sh` green).
- [ ] **Evals fresh** — no uncleared `pending` rows in `Evals/_pending-reruns.md` for any suite this PR cites (`scripts/check-eval-freshness.sh` green).
- [ ] **CLAUDE.md `DO NOT` respected** — no unapproved deletes; `Knowledge/People/` profiles unchanged without confirmation; no new top-level folders.

## Notes

<!-- Anything a reviewer should know: known-stale suites, follow-ups, links. -->
