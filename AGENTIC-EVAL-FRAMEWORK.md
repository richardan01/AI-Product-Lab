# AI Product Lab — the agentic eval loop framework

AI Product Lab runs on a reviewed agentic eval system for product work. It turns recurring product work into workflows that can be run, reviewed, evaluated, monitored, and improved over time — with the eval loop, not the workflows, as the point. The lab's flagship project (RegEval) and public artifacts run on top as the application domain.

The goal is not to make AI write more documents. The goal is to make AI-assisted product work measurable, reviewable, and continuously improvable.

## 1. Problem

Most PMs use AI through one-off prompts. That helps with speed, but it does not create a reliable system:

- context is rediscovered every time
- outputs are hard to compare across runs
- review standards live in the user's head
- failures do not automatically become better test cases
- workflow quality is assumed instead of measured

PM work needs the same loop discipline as software and model work: clear context, repeatable execution, quality gates, evals, monitoring, and a feedback path from failure to improvement.

## 2. Framework

```text
Trigger
  -> Context
  -> Agent workflow
  -> Artifact
  -> Quality gate
  -> Offline eval
  -> Human review
  -> Online monitoring
  -> Improvement
```

Each step has a job:

| Step | Role in the loop |
|---|---|
| Trigger | A user command or workflow request starts a bounded PM task. |
| Context | Repo-native knowledge, project files, tasks, and goals provide durable state. |
| Agent workflow | A documented workflow or skill performs the work in a repeatable way. |
| Artifact | The output is a PRD, review, launch gate, synthesis, update, plan, or decision record. |
| Quality gate | A reviewer loop checks whether the artifact is ready for handoff. |
| Offline eval | Separate grader contexts test workflows and gates against fixtures and answer keys. |
| Human review | The PM makes the judgment call and approves, revises, or rejects the output. |
| Online monitoring | Real artifacts are sampled after the fact and graded for failure trends. |
| Improvement | Recurring failures become new fixtures, rubrics, workflow edits, or knowledge updates. |

## 3. Architecture

The lab is intentionally simple: Markdown files are the operating surface.

| Layer | Repo surface | Purpose |
|---|---|---|
| Knowledge layer | `CLAUDE.md`, `Knowledge/`, `Projects/`, `Tasks/`, `GOALS.md` | Durable context, source of truth, working state, preferences, decisions, and provenance. |
| Workflow layer | `Workflows/`, `Templates/`, `.claude/skills/`, `.claude/agents/` | Repeatable PM processes and task-specific agent instructions. |
| Eval and monitoring layer | `Evals/`, `Evals/monitoring/`, `Evals/severity-taxonomy.md`, `Evals/_ci-map.md`, `Evals/_pending-reruns.md` | Offline audit suites, planted-flaw meta-evals, severity rules, and freshness sentinels. |

This follows the same pattern as agentic research systems: the human edits the operating instructions and review standards; agents execute bounded work; the metric and review loop decide whether the run improved the system.

## 4. Loop Design

### Daily PM Loop

```text
/today -> focused work -> artifact drafting/review -> /eod -> task/context update
```

This loop keeps `Tasks/active.md`, goals, blockers, and current context fresh so later workflows start with better state.

### Quality Gate Loop

```text
artifact -> gate rubric -> bad/sad severity -> verdict -> revision checklist
```

Quality gates separate drafting from review. They look for PM handoff risks such as hallucinated findings, missing acceptance criteria, weak evidence, unresolved red risks, or research that is too thin for the decision. Public artifacts additionally pass the Riddler (adversarial) and Vale (user-voice) gates before shipping.

### Offline Eval Loop

```text
fixture -> runner context -> transcript/output -> separate grader context -> score -> run log
```

Offline evals preserve author/grader separation. The runner creates the artifact; a fresh grader context applies criteria and, where relevant, answer keys. Results are recorded in `Evals/run-log.md` and suite-specific result files.

### Planted-Flaw Meta-Eval Loop

```text
known flawed artifact + clean control -> gate under test -> grader -> pass/fail
```

The lab does not only evaluate PM artifacts. It evaluates the gates themselves. A reviewer gate must catch known blockers, avoid hallucinated findings, and avoid flunking clean work.

### Online Monitoring Loop

```text
trace collector -> sample -> grade -> log -> analyze -> escalate
```

Real outputs are sampled asynchronously, graded in fresh contexts, bucketed by severity, and turned into new fixtures or workflow changes when failure patterns repeat.

## 5. Metrics

The useful metrics are tied to artifact quality and decision readiness:

| Metric | What it measures |
|---|---|
| Artifact pass rate | Share of artifacts that clear the relevant quality gate. |
| Bad-rate | Share of sampled artifacts with one or more irrecoverable `bad` findings. |
| Sad-rate | Recoverable friction that lowers artifact quality but does not block handoff. |
| Human approval rate | Share of AI-assisted outputs accepted with light edits. |
| Gate false-positive rate | Clean artifacts incorrectly blocked by a gate. |
| Gate false-negative rate | Flawed artifacts incorrectly cleared by a gate. |
| Eval freshness | Whether mapped workflows/gates have been re-run after relevant changes. |
| Decision readiness | Whether the output supports a real PM decision, escalation, or handoff. |
| Time saved | Time removed from formatting, search, synthesis, and drafting without lowering quality. |

The core portfolio metric is not output volume. It is whether the lab lowers the `bad` rate while preserving useful PM throughput.

## 6. Example Use Cases

| Use case | Workflow/gate | Eval or monitoring path |
|---|---|---|
| AI feature PRD review | `/prd-readiness`, `/peer-review` | `Evals/prd-readiness/`, `Evals/peer-review/` |
| Research synthesis | `Workflows/user-research-synthesis/`, `/research-sufficiency` | `Evals/research-synthesis/`, `Evals/research-sufficiency/` |
| Launch readiness | `/go-nogo`, `/launch-plan` | `Evals/go-nogo/` |
| Build or artifact review | `/build-review`, `/eval-review`, `/test-plan` | `Evals/build-review/` |
| LLM-as-judge reliability | `Evals/regeval/` (RegEval flagship) | `Evals/regeval/regeval-suite.md`, `Evals/run-log.md` |
| Onboarding a PM into the OS | `Workflows/interactive-onboarding.md` | `Evals/onboarding/` |
| Weekly operating review | `/weekly-update`, `Evals/monitoring/` | Sample real artifacts, grade asynchronously, and feed new failures back into fixtures. |

## 7. Why This Matters

This repo is not just a personal productivity system. It is a lightweight example of loop engineering for PM work:

- context compounds instead of being rediscovered
- workflows are explicit enough to improve
- review standards are captured outside the author's head
- gates are tested against planted flaws and clean controls
- monitoring finds new failures in real usage
- failures become better fixtures, better workflows, or better knowledge

That is the shift from AI as a writing assistant to AI as a measurable PM execution system.

## 8. Portfolio Framing

Use this framing when presenting the repo:

```text
AI Product Lab is a proof-of-work eval system for AI-assisted product work: it turns recurring product work into reviewed agentic workflows and then measures whether they actually work.

It combines repo-native knowledge, structured workflows, quality gates, offline eval suites, planted-flaw meta-evals that grade the gates themselves, a reproducible LLM-as-judge harness (RegEval), online monitoring, and weekly feedback loops.

The goal is to make AI-assisted product work measurable, reviewable, and continuously improvable.
```

Short portfolio title:

```text
AI Product Lab
```

Long portfolio title:

```text
AI Product Lab: an agentic workflow + eval-loop system for AI-assisted product work
```
