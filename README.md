# AI Product Lab

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Primary%20surface](https://img.shields.io/badge/primary-agent%20trajectory%20eval-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**A public AI product-management proof-of-work lab for evaluating whether an agent did the
right thing—not only whether its final answer looked convincing.**

AI Product Lab reads a real Claude Code or Codex session, turns it into a normalized trace,
and grades both task success and the trajectory that produced it. The method is local and
Markdown-native; Claude Code is the current grading runner.

## Human-data product direction

[From agent traces to defensible human judgments](docs/case-studies/human-data-quality-loop.md) describes the proposed sampling, independent labeling, disagreement adjudication, and research-to-product decision loop. It is a roadmap, **not** a claim that researcher-facing annotation operations are already deployed.

## What the lab evaluates

An agent can produce a plausible answer while choosing the wrong tool, guessing parameters,
forgetting a constraint, or recovering badly from an error. The active `agent-harness` suite
checks seven things:

| Phase | Question |
|---|---|
| Task success | Did the final result actually satisfy the user's goal? |
| Tool choice | Did the agent use the right tools at the right moments? |
| Parameter extraction | Were arguments grounded in the session rather than guessed? |
| Error recovery | Did the agent adapt after failures? |
| Context retention | Did it preserve earlier facts and constraints? |
| Efficiency | Did it avoid redundant calls and loops? |
| Goal alignment | Did it stay focused on the requested outcome? |

Every finding is tied to evidence and marked `bad` (blocks trust) or `sad` (recoverable
friction). One trace is one data point, not a success rate.

## See the evidence in three minutes

1. [Latest suite run (2026-09-19)](evals/agent-harness/evidence/2026-09-19_sample-coding-retry.md)
   — the method end to end on a synthetic trace, with author/grader separation held across
   seven isolated graders. Six of seven axes reproduced a run from 70 days earlier; the one
   that diverged is written up rather than smoothed over.
2. [Synthetic tutorial report](evals/agent-harness/evidence/2026-07-11_sample-coding-retry.md)
   — the deterministic example used to teach the scorecard.
3. [Controlled real-session report](evals/agent-harness/evidence/controlled-real-run/aggregate.md)
   — a real Codex tool-use run on a public toy task. Read the
   [provenance note](evals/agent-harness/evidence/controlled-real-run/README.md) first: its
   grader model was never recorded and author/grader separation did **not** hold, so it is a
   worked example, not citable evidence.
4. [RegEval integrity case study](evals/regeval/discovery-pass-2026-06-28.md) — the lab found
   that its supposed held-out set was contaminated, invalidated the claim, and rebuilt the
   measurement approach.

Every published report carries a provenance block — run date, repo commit, grader model, and
whether separation held. Unknown provenance is recorded as an explicit `null` and explained,
never omitted and never invented.

## Try it in 15 minutes

Requirements: Python 3.10+ and Claude Code. No Python packages are required for trace
normalization.

```bash
git clone https://github.com/richardan01/AI-Product-Lab.git
cd AI-Product-Lab
claude
```

Inside Claude Code, run the safe sample first:

```text
/evaluate-agent-session sample
```

To grade your own completed session:

```text
/evaluate-agent-session /absolute/path/to/session.jsonl --harness claude-code
/evaluate-agent-session /absolute/path/to/rollout.jsonl --harness codex
```

Before a private trace is graded, the command shows the selected file and asks you to confirm
the privacy disclosure. Raw traces and private reports are gitignored.

For manual normalization without grading:

```bash
python3 scripts/trace_adapter.py claude-code --input /path/to/session.jsonl --suite agent-harness
python3 scripts/trace_adapter.py codex --input /path/to/rollout.jsonl --suite agent-harness
```

## How the repository is organized

| Path | Start here when you want to… |
|---|---|
| [`docs/`](docs/) | Learn the method, architecture, privacy model, and design case studies |
| [`evals/`](evals/) | Inspect the active agent-harness and RegEval evidence |
| [`scripts/`](scripts/) | Normalize traces, create N-1 fixtures, and run deterministic checks |
| [`.claude/`](.claude/) | See the one-command runner and isolated grader contract |

The complete earlier personal PM operating system—including Gotham agents, workflows,
onboarding, tasks, and meta-eval suites—is preserved at
[`ai-product-lab-os-v1`](https://github.com/richardan01/AI-Product-Lab/tree/ai-product-lab-os-v1).
It is historical evidence, not the current product surface.

## Learn the method

The [guided learning path](docs/learn.md) offers 10-minute, 30-minute, 60-minute, and two-hour
routes. The short version is:

```text
real session → normalized trace → isolated graders → aggregate verdict
             → failure analysis → new fixture → rerun
```

The design combines two compounding patterns:

- **Knowledge compounds:** sources become maintained synthesis, indexes, and logs rather than
  being rediscovered from scratch.
- **Experiments compound:** one falsifiable metric, fixed scope, fixed budget, keep/discard,
  and an append-only record.

See [architecture and method](docs/architecture.md) for the Karpathy-inspired design and its
limits.

## The flagship case study: RegEval

RegEval asks whether an LLM judge can classify regulated-domain compliance examples in
agreement with human labels. Its most important result is not a headline score—it is the
documented discovery that an early held-out claim was invalid.

The public clone includes the scorer, historical experiment lineage, and a small synthetic
demo dataset. The later private 36-item held-out set is not published, so its historical score
is **not independently reproducible from this repository**. RegEval's last run was
2026-06-28; it is a frozen historical case study, not a suite that is re-run on a schedule.
Start with the [RegEval case-study guide](evals/regeval/README.md).

## Capability and limitation table

| Capability | Status |
|---|---|
| Normalize Claude Code sessions | Adapter regression-tested against the committed format |
| Normalize Codex rollouts | Verified against a controlled real run and sample format |
| Grade through one Claude Code command | Shipped; last run 2026-09-19 with separation held |
| Run the grader directly in Codex | Not shipped |
| Cowork trace support | Planned; format unconfirmed |
| Hosted dashboard or production monitoring | Not provided |
| Fully reproducible historical RegEval held-out score | Not provided; private data excluded |
| Autonomous public RegEval loop | Design case study only; no public unattended driver |

## Privacy

No hosted observability platform or SDK is required. Trace files and reports stay in local,
gitignored directories unless you deliberately sanitize and publish them. Content selected
for LLM grading is still processed by your chosen inference provider. Read the full
[privacy model](docs/privacy.md) before grading a work session.

## What this is not

- It is not a reusable personal PM workspace.
- It is not a replacement for production observability platforms such as LangSmith or
  Braintrust.
- It is not evidence that one clean trace proves an agent is reliable.
- It is not a finished cross-provider product.

## License

MIT. You may study, reuse, and adapt the method with attribution. See [LICENSE](LICENSE).
