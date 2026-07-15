# Reviewer Verdict Schema

Canonical format for verdict files written by the gate skills: `/riddler`, `/vale`, `/peer-review`, `/prd-readiness`, `/research-sufficiency`, `/go-nogo`, `/eval-review`, `/build-review`.

A verdict file is a lightweight audit trail. It proves a gate ran, by whom (which skill), on what (file path + date + content hash), and with what outcome. It does not replace the full review output — it's the header block plus the review scorecard.

---

## Verdict file naming

| Skill | Suffix |
|---|---|
| `/riddler` | `<artifact-path>.riddler-passed` |
| `/vale` | `<artifact-path>.vicki-passed` |
| `/peer-review` | `<doc-path>.peer-review-passed` |
| `/prd-readiness` | `<prd-path>.prd-readiness-passed` |
| `/research-sufficiency` | `<doc-path>.research-sufficiency-passed` |
| `/go-nogo` | `<project-path>.go-nogo-passed` |
| `/eval-review` | `<suite-path>.eval-review-passed` |
| `/build-review` | `<path>.build-review-passed` |

Place the verdict file in the same directory as the reviewed artifact.

---

## Verdict file format

Every verdict file must contain exactly this header block, followed by the scorecard:

```
Gate:     <skill name>
File:     <reviewed file path>
Date:     YYYY-MM-DD
Verdict:  PASS | CONDITIONAL
Hash:     <first 12 chars of sha256 of the reviewed file — `shasum -a 256 <file>`>
Reviewed-by: <human | agent:skill-name>
```

Followed immediately by the review scorecard from the skill output (Riddler: weakest claim / missing evidence / publish decision; Vale: drop-off point / unanswered reader question / highest-leverage revision).

`Reviewed-by:` records who conducted the review — `human` for a manual sign-off, or `agent:<skill-name>` (e.g. `agent:riddler`, `agent:vicki-vale`) when an agent ran the gate. `Tools/gate-check.sh` requires the field to be present and well-formed; it records provenance and does not by itself mandate a human — a human-in-the-loop publish policy would additionally require `Reviewed-by: human`.

On CONDITIONAL, every condition and its resolution must be listed in the marker before the artifact ships (see the CONDITIONAL fast-path in `Workflows/gate-merge.md`).

---

## Global gate markers (`_Registry/.riddler-passed`, `_Registry/.vicki-passed`)

The per-artifact verdict files are the permanent audit trail. The **global markers** in `_Registry/` are the live gate state:

- `/riddler` and `/vale` write the same header block to `_Registry/.riddler-passed` / `_Registry/.vicki-passed` on PASS or CONDITIONAL. This **arms** the gate.
- `Tools/gate-check.sh` (PreToolUse hook in `.claude/settings.json`) blocks any write to `Artifacts/` — or to any filename containing `-essay`, `-post`, or `-thread` — unless both global markers exist and are fresh (mtime within `GATE_TTL_SECONDS`, default 6h; expired = missing).
- `Workflows/gate-merge.md` Step 6 **disarms** the gate — deletes both global markers after the artifact is staged and logged. Never leave the gate armed across artifacts.

---

## Verdict levels

| Verdict | Meaning |
|---|---|
| **PASS** | All checks clear. Artifact approved to ship. |
| **CONDITIONAL** | Mechanical fixes required and applied inline; documented in the marker. Approved once every condition is confirmed applied. |
| **REVISE / BLOCK** | No verdict file is written. On BLOCK, write `<artifact-path>.<gate>-blocked-YYYY-MM-DD.md` with the required fixes. |

---

## Rules

1. Verdict files are only written on PASS or CONDITIONAL — never on REVISE or BLOCK.
2. Do not back-date verdict files. The date is the date the skill ran.
3. Verdict files are never edited after creation. A re-review writes a new file with a date suffix; a superseded marker is annotated VOID by the re-review, never silently deleted.
4. A verdict is bound to content: if the artifact changes after the review (hash mismatch), the verdict is void and the gate must re-run.
5. Per-artifact verdict files are committed alongside the artifact they cover — they are part of the artifact's history.
