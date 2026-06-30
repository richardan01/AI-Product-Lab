# Weekly operating loop

**Purpose:** Keep My-OS useful as Richard's private live cockpit.

This workflow is the weekly control loop for the OS. It is not a public-template
release check. It assumes Richard is using My-OS daily with Cursor and Claude
cowork desktop, so private/local state is allowed, but runtime clutter and
unreviewed structural drift must be surfaced before it becomes operational debt.

## Trigger

Run weekly, ideally before Monday planning or after a heavy weekend build.

Run immediately when:

- `Evals/`, `Agents/`, `.claude/skills/`, or `Workflows/` changed materially
- New runtime tools or MCPs were added
- A Claude cowork session created many files
- Richard asks whether My-OS still operates cleanly

## Inputs

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `Tasks/active.md`
- `Tasks/dayjob-active.md`
- `Evals/index.md`
- `Evals/evals-hub.md`
- `Evals/run-log.md`
- `_Registry/MCPs.md`
- `.gitignore`
- Files changed in the last 7 days, using git when available and file modified
  time when this cockpit is not a git repo

## Operating stance

Agents do the repetitive inspection. Evals and reviewers surface deltas. Richard
judges what to accept.

The runner must not:

- Delete, move, commit, or push files
- Treat private runtime evidence as public-template evidence
- Auto-promote local experiment results into canonical docs
- Create new top-level folders unless Richard explicitly approves
- Mark a suite fresh when run evidence only exists somewhere else

## Procedure

1. Confirm scope: this is `My-OS`, Richard's private live cockpit.
2. Check whether git is available. If not, use modified-time fallback and say so.
3. Group changed files by area:
   - Core OS: `AGENTS.md`, `CLAUDE.md`, `README.md`, `GOALS.md`
   - Agents and skills: `Agents/`, `.claude/skills/`
   - Workflows: `Workflows/`
   - Evals: `Evals/`
   - Knowledge: `Knowledge/`
   - Tasks and reviews: `Tasks/`, `Reviews/`
   - Tools/runtime: `Tools/`, `.wwebjs_cache/`, screenshots, local MCP state
4. Run deterministic hygiene checks where available:
   - Markdown lint
   - Eval registry sync
   - Eval run freshness
   - Runtime/private-state exposure
   - Placeholder hygiene
   - Complexity creep
5. For eval freshness, first read public/local files. If the log says evidence is
   private or in Notion STATE, record `requires private-state confirmation`
   instead of failing the suite.
6. For automation-like skill changes, require an eval, test, checklist, or
   documented manual review path.
7. Convert findings into STATE debt candidates, not file changes.
8. Ask Richard which, if any, fixes to implement.

## Scoring

Use the smallest severity that protects daily operation:

| Severity | Meaning |
|---|---|
| P0 | Could leak private state, break the cockpit, or make automation unreliable |
| P1 | Blocks trustworthy weekly operation or eval discipline |
| P2 | Cleanup, polish, stale references, or noisy lint |

## Output format

```
Summary
Changed files
P0 findings
P1 findings
P2 findings
Recommended Claude STATE debt updates
No-file-change confirmation
Questions
```

## Done criteria

- Richard can see what changed without reading the whole tree
- Private/local state is separated from canonical OS files
- Eval freshness is either confirmed or explicitly pending confirmation
- Any proposed fix passes AGENTS.md relevance, simplicity, stability, and signal
- No files were changed unless Richard explicitly asked for implementation
