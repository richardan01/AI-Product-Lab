# Public evidence — agent-harness

Raw traces (`evals/agent-harness/_traces/`) are gitignored: they are unsanitized session
records that may contain private paths, names, or content. This directory is the **opposite**
— a small set of **sanitized, end-to-end runs that ship publicly**, so the repo's grounding
claim is backed by visible proof instead of a private log.

## What goes here

- One or two fully worked runs: the normalized trace (redacted), the seven per-eval verdicts,
  and the aggregate — enough for a reader to see the method actually ran on a real session.
- One worked **failure → N-1 fixture → fix** story, when one exists. That narrative is the
  point of the whole lab.

## Sanitization checklist (before adding anything here)

- [ ] Replace absolute paths, usernames, org names, and any credential-shaped strings.
- [ ] Drop `params`/`result` bodies that carry private content; keep tool *names*, ok flags,
      and metrics (that is what the axes grade).
- [ ] Keep `goal` only if it is safe to publish; otherwise paraphrase it.
- [ ] Re-read the whole file before committing — sanitization is manual and easy to get wrong.

## Provenance is mandatory

Every report here must satisfy the provenance block in `../report-schema.json` (v1.1): run
date, repo commit, grader model, and whether author/grader separation held. Unknown provenance
is recorded as an explicit `null` and explained in `provenance_note` — never omitted, and
never invented. `scripts/validate_agent_report.py` enforces this.

A run whose `author_grader_separation` is `false` is a worked example of the scorecard, not
evidence of agent behaviour, and must not be cited as a reliability claim.

## Status

| Run | Date | Separation | Class |
|---|---|---|---|
| [`2026-09-19_sample-coding-retry.md`](2026-09-19_sample-coding-retry.md) | 2026-09-19 | ✅ held (7 isolated graders) | Synthetic worked example |
| [`2026-07-11_sample-coding-retry.md`](2026-07-11_sample-coding-retry.md) | 2026-07-11 | ✅ held (7 isolated graders) | Synthetic worked example |
| [`controlled-real-run/`](controlled-real-run/) | 2026-07-21 (commit date; capture date not recorded) | ❌ did not hold | Controlled real trajectory, not citable |

The controlled trace was reviewed against the same seven criteria, but in the context that
authored it; it is not evidence that Codex can execute the shipped Claude Code orchestration
command. **No run here is production evidence or supports a population-level reliability
claim.** A real, redacted Claude Code session graded by seven isolated contexts is still
pending — that is the gap this directory has not yet closed.
