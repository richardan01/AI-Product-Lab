# Weekly operating loop checklist

Use this checklist with `Workflows/weekly-operating-loop.md`.

## Scope

- [ ] Confirm cwd is the My-OS repo root
- [ ] State that My-OS is the private live cockpit
- [ ] State whether git is available
- [ ] If git is unavailable, use modified-time fallback and label it as fallback

## Changed files

- [ ] Group changed files by area
- [ ] Separate canonical OS files from runtime/tool/cache files
- [ ] Count large generated surfaces such as `node_modules`, auth sessions, cache,
      screenshots, and build output
- [ ] Do not delete or move anything during the review

## Eval discipline

- [ ] List suite folders under `Evals/`
- [ ] Compare suite folders with `Evals/index.md`
- [ ] Compare active suites with `Evals/evals-hub.md`
- [ ] Read `Evals/run-log.md`
- [ ] Identify latest visible run per suite
- [ ] If evidence is private/local/Notion STATE, mark confirmation required
- [ ] Flag suites older than 60 days only when no private confirmation exists

## Skill and workflow discipline

- [ ] Identify changed `.claude/skills/**` files
- [ ] Classify changed skills as deterministic, judgment-heavy, or automation-like
- [ ] For automation-like changes, require an eval, test, checklist, or manual
      review path
- [ ] Flag new agents, new top-level folders, or duplicated workflows unless they
      pass AGENTS.md acceptance criteria

## Runtime safety

- [ ] Check for `.DS_Store`
- [ ] Check for `node_modules`
- [ ] Check for `.wwebjs_auth` and `.wwebjs_cache`
- [ ] Check for root screenshots or visual debugging captures
- [ ] Check whether `.gitignore` protects private/runtime state

## Output

- [ ] Summary says whether the cockpit loop is healthy
- [ ] Findings are grouped into P0, P1, P2
- [ ] STATE debt updates are phrased as candidate tasks
- [ ] Include no-file-change confirmation unless Richard asked for edits
- [ ] Ask only unresolved questions that block the next decision
