---
name: eval-ci
description: Lightweight regression sentinel for AIPM-OS. When workflows or skills mapped to an eval suite are edited, this skill registers a pending re-run and blocks /peer-review and /go-nogo from passing for artifacts citing that suite until a fresh eval run lands. Trigger on "register an eval rerun", "what suites need re-running", "is suite X stale", or automatically after edits to mapped files.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

# /eval-ci — Regression sentinel for AIPM-OS

A real CI pipeline runs evals automatically on every change. AIPM-OS has no build server. This skill is the next best thing: a markdown ledger that tracks which suites are out of date and a contract that gates whose results are citable.

## When to run
- After editing a workflow or skill that maps to an eval suite (manual trigger; see "Automating registration with a hook" below to make this mechanical)
- Before running `/peer-review` on any artifact that cites an eval result
- Before running `/go-nogo` on any decision that depends on an eval pass rate
- On demand: "what suites are stale?"

## The map
File → Suite mapping lives at `Evals/_ci-map.md`. The skill reads this file as the source of truth.

Default mapping (created if file doesn't exist):

```markdown
# Eval CI map

| Source file | Affected suite |
|---|---|
| Workflows/interactive-onboarding.md | onboarding |
| .claude/skills/synthesize-research/SKILL.md | research-synthesis |
| CLAUDE.md (Operating contract section) | onboarding |
| Templates/profile.md | onboarding |
```

Extend this table as new suites are added.

## The ledger
File: `Evals/_pending-reruns.md`. Append-only.

```markdown
# Pending eval re-runs

Each row was registered when a mapped source file changed. A row is cleared only when a fresh eval run lands in `Evals/<suite>/results/` with date ≥ the source file's last edit date.

| Suite | Source file changed | Source commit SHA | Registered date | Status | Cleared by run |
|---|---|---|---|---|---|
| onboarding | Workflows/interactive-onboarding.md | abc1234 | 2026-05-30 | pending | — |
```

Status values: `pending` | `cleared`

## Operations

### Register a re-run
When called with `register <suite> <source-file>`:

1. Read `Evals/_ci-map.md` to confirm the mapping exists.
2. `git rev-parse HEAD` to capture commit SHA.
3. Append a new row to `Evals/_pending-reruns.md` with status `pending`.
4. Surface to the user: "Suite `<suite>` is now flagged as pending re-run. `/peer-review` and `/go-nogo` will block citations of this suite until a fresh run lands at `Evals/<suite>/results/<date>_<model>.md` (date ≥ today)."

### Check whether citing a suite is OK
When called with `check <suite>`:

1. Read `Evals/_pending-reruns.md`. Find all rows for this suite with status `pending`.
2. Look up the latest result file at `Evals/<suite>/results/`. Get its date from the filename.
3. If any pending row has `registered_date > latest_result_date`, return `BLOCK` with the source file and SHA that triggered the block.
4. Otherwise return `OK` with the citable run.

Return format:
```
**Suite:** <suite>
**Verdict:** OK | BLOCK
**Latest run:** <path> (<date>, <model>)
**Pending re-runs blocking citation:** <count>
  - <source file>: changed <date>, SHA <sha>
**Next step:** <run the suite via /evals | citable as: <latest run>>
```

### Clear a pending row
When called with `clear <suite>` (after a fresh eval run lands):

1. Read `Evals/_pending-reruns.md`.
2. For all rows of `<suite>` with status `pending`, set status to `cleared` and fill `cleared_by_run` with the latest result file path.
3. Report what was cleared.

### List stale suites
When called with `list`:

Walk all suites in `Evals/`. For each, report:
- Last run date (most recent file in `<suite>/results/`)
- Days since last run
- Pending re-runs count
- Verdict: ✅ healthy / ⚠ stale / ❌ blocked

## Integration with /peer-review and /go-nogo
Both gates should call `eval-ci check <suite>` before passing any artifact that cites a `<suite>` pass rate. If the verdict is BLOCK, the gate fails with a "stale eval" finding.

This integration is implemented by adding to `/peer-review` and `/go-nogo`:
```
For each eval result cited in the artifact, invoke /eval-ci check <suite>.
If any returns BLOCK, return Conditional Pass with required fix:
"Re-run <suite> via /evals before this artifact can ship."
```

## Automating registration with a hook (manual install)

Registration currently relies on remembering to run `register` after editing a mapped file. To make it mechanical, install a `PostToolUse` hook on `Edit|Write` that checks the edited path against `Evals/_ci-map.md` and appends the pending row itself. **Install this yourself, deliberately** — hooks execute on every edit, so review the code before wiring it.

In `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/eval-ci-register.py\"" }
        ]
      }
    ]
  }
}
```

The script at `.claude/hooks/eval-ci-register.py` should: read the hook JSON from stdin, take `tool_input.file_path` relative to the project dir, match it against the `Source file` column of `Evals/_ci-map.md`, and on a match append a `pending` row (suite, path, `git rev-parse HEAD`, today, `pending`) to `Evals/_pending-reruns.md` — deduping if an uncleared `pending` row for the same (suite, file) pair already exists — then emit `hookSpecificOutput.additionalContext` announcing the registration. It must exit 0 on every path so a hook bug can never block normal editing.

## Hard rules
- Do not modify any file outside `Evals/_pending-reruns.md`, `Evals/_ci-map.md`, and the source files for cleared rows.
- Do not silently mark a row cleared. Always require a real result file at `Evals/<suite>/results/`.
- The ledger is append-only: you can flip status `pending` → `cleared`, but you do not delete rows. History matters for audit.
- If a source file is edited but the mapping doesn't exist in `_ci-map.md`, prompt the user to add the mapping. Do not silently skip.

## Output
For `register`: one-line confirmation with the new row.
For `check`: the verdict block above.
For `clear`: list of rows cleared.
For `list`: a table of all suites with health.
