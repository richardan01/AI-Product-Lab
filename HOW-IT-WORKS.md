# HOW IT WORKS — architecture of the portfolio lab

How the pieces compose: agents, gates, evals, workflows, and the compounding log. Written for someone inspecting the repo cold. The one-page pitch is [`PROOF-OF-WORK.md`](PROOF-OF-WORK.md); the mission summary is [`GOALS.md`](GOALS.md).

---

## The three layers

```
1. STRATEGY   Agents/Gotham/          8 character agents + quarterly thesis
2. EXECUTION  Projects/ + Evals/      flagship build loop + eval suites
3. ENFORCEMENT Workflows/ + Tools/    quality gates wired as hooks, not habits
```

### 1. Strategy — the Gotham agent suite

8 agents in `Agents/Gotham/Computer/`, each a full prompt (mission, JTBD, voice fingerprint, file ownership, handoffs). Routing lives in `CLAUDE.md`; voice contracts live in `_Registry/voice-map.md`. Bruce Wayne owns the quarterly thesis (`Agents/Gotham/thesis-q3-2026.md`) — every task in `Tasks/active.md` maps to one of its three pillars.

The design rationale, model selection, and the 4 agents deliberately left out of the public repo are documented in `Agents/agent-system-architecture.md`.

### 2. Execution — Ralph, RegEval, and the eval suites

- **Ralph** (`Projects/ralph/`) — the outer build loop: reads stories from `prd.json`, invokes Claude Code per story, enforces quality gates and HITL pauses (`ralph.sh`).
- **RegEval** (`Evals/regeval/`) — the flagship: an LLM-as-judge framework for regulated-domain compliance classification. Real Python (`score.py`, `provenance.py`, `judge_vs_human.py`), a 100-item gold dataset, 20+ dated experiment write-ups, and a KEEP/HOLD/DISCARD log where the metric — not the author — is the reviewer. Inner loop spec: `Evals/regeval/runner.md` (`/regeval-run`).
- **Eval suites** (`Evals/`) — the meta-layer: the OS's own gates are eval'd with planted-flaw inputs and answer keys (`peer-review`, `prd-readiness`, `go-nogo`, `gate-group`, `onboarding`, …). Severity taxonomy, eval-CI staleness sentinel (`_ci-map.md`), and a bias-aware run log (`run-log.md`).

Discipline rules that hold everywhere:
- **Author/grader separation** — the agent that runs an eval never reads the answer keys the grader uses (`.claude/agents/eval-runner` vs `eval-grader`).
- **Judges are calibrated before trusted** — TPR ≥ 0.9 AND TNR ≥ 0.9 on a held-out dev split (`/judge-calibration`).
- **Failures are first-class** — `Evals/failure-log.md`, RegEval's failure taxonomy, and integrity incidents (FM-11 held-out contamination) are documented, not buried.

### 3. Enforcement — gates as hooks

Public artifacts pass two mandatory reviews:

```
draft ready → Workflows/gate-dispatch.md
                ├── Task A: Riddler   (adversarial — weakest claim, faked depth)
                └── Task B: Vicki Vale (reader-voice — where does a stranger stop reading)
                     └── conditional Task C: Henri Ducard (depth escalation)
            → Workflows/gate-merge.md  (BLOCK > REVISE > SHIP precedence)
            → stage into Artifacts/ + log in _Registry/artifact-log.md
```

The gate is **mechanical, not aspirational**: a PreToolUse hook (`.claude/settings.json` → `Tools/gate-check.sh`) blocks any write into `Artifacts/` unless both `_Registry/.riddler-passed` + `_Registry/.vicki-passed` markers are armed. The reviewer skills arm them on PASS; `gate-merge` disarms them after staging. Verdict format: `_Registry/reviewer-verdict-schema.md`.

---

## The compounding principle

The lab runs on Karpathy's autoresearch shape: **one runner, one falsifiable metric, fixed time budget, append-only log.** Nothing is edited retroactively — experiments, run logs, and verdict markers accumulate, so learning (including failures) stays inspectable over time.

## A typical loop, end to end

1. Session starts → read thesis + `Tasks/active.md`.
2. Lucius Fox runs `/regeval-run <candidate>` → experiment file + κ verdict → one line in `experiments/log.md`.
3. A result worth publishing → Nightwing drafts → `gate-dispatch` → Riddler + Vale verdicts → `gate-merge` → staged in `Artifacts/`.
4. Monthly: `Workflows/memory-consolidation.md` audits memory drift; `/retro` feeds the next thesis revision.

## Repo map

| Path | What lives there |
|---|---|
| `CLAUDE.md` | Operating contract + routing |
| `Agents/Gotham/` | Agent prompts, thesis, gate I/O schemas |
| `Projects/ralph/` | Flagship build loop |
| `Evals/` | RegEval + all eval suites, run log, taxonomies |
| `Workflows/` | Gate pipeline + planning/research/memory workflows |
| `Tools/` | `gate-check.sh` publish-gate hook |
| `_Registry/` | Voice map, verdict schema, artifact log, live gate markers |
| `Artifacts/` | Gate-passed public artifacts (staging) |
| `Templates/` | Document skeletons |
| `.claude/` | Skills, eval sub-agents, settings + hook wiring |

## Related

[[README]] · [[GOALS]] · [[PROOF-OF-WORK]] · [[Agents/agent-system-architecture]] · [[Workflows/index]] · [[Evals/index]]
