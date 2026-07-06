# Gate Group — Eval Fixtures

Five fixtures chosen to exercise every verdict path and the escalation branch. Each names the gate behavior it stresses. Artifact content is fictional; the point is the gate's response, not the artifact's quality.

| ID | Artifact (type) | Stresses | Designed path |
|----|-----------------|----------|---------------|
| F1 | `auditlog` library README (`readme`) | SHIP path; Riddler strictness on overclaims | SHIP (or REVISE if overclaims caught) |
| F2 | Data-pipeline demo README (`readme`) | Standard 2-agent gate, mild disagreement | REVISE |
| F3 | Speculative-decoding LinkedIn post (`post`) | **Flag discipline** — block on sourcing, NOT depth | REVISE/BLOCK, `depth_gap_flag: false`, **no Ducard** |
| F4 | Faked-depth eval interview answer (`interview_answer`) | **Depth-escalation** — genuine faked depth | BLOCK + `depth_gap_flag: true` → **Ducard spawns** |
| F5 | Jargon-dense essay opener (`essay`) | **Disagreement** — defensible argument, lost reader | REVISE/BLOCK; Riddler ≠ Vale |

## F1 — auditlog README

```
# auditlog — the smallest LLM audit trail for a regulated workflow

You can't ship an LLM into a regulated workflow without an audit trail. auditlog
wraps any model call and appends a record — prompt, response, model version, and
which policy checks ran — to append-only storage. One decorator, no config.

    @auditlog
    def classify(doc): ...

Install: pip install auditlog. The 2-minute quickstart is below.
```

**Stresses:** whether Riddler can return a clean `pass` on a strong artifact, vs. catching the latent overclaims ("regulated workflow", "append-only", "any model call"). Vale should `read` (strong opener).

## F2 — Data-pipeline demo README

```
# pipeline-demo

This repo demonstrates a modern data pipeline built with best-in-class tooling.
It ingests events, transforms them with dbt, and loads them into a warehouse for
analytics. The pipeline is fast, reliable, and easy to extend.

## Quickstart

    docker compose up
    make seed && make run

Events flow from the generator into Kafka, land in staging tables, and dbt models
materialize the marts. See docs/ for architecture notes.
```

**Stresses:** the standard 2-agent gate with mild disagreement — argument is reviewable but the opener is generic ("modern", "best-in-class", "fast, reliable, and easy to extend" are unsupported adjectives).

## F3 — Speculative-decoding post

```
We cut p95 inference latency 60% by switching from standard autoregressive
decoding to speculative decoding. A 7B draft model proposes k tokens; the 70B
target verifies all k in a single forward pass and accepts the longest correct
prefix, falling back to standard decoding for rejected tokens. Output quality is
unchanged because the target model still has final say on every token —
speculative decoding is exact, not approximate. The 60% figure is from our
internal benchmark.
```

**Stresses:** the flag-discipline distinction. The author *understands* speculative decoding (mechanism is correct), but the `60%` is unsourced. A correct gate blocks/conditions on the missing rigor with `depth_gap_flag: false` — **no Ducard**.

## F4 — Faked-depth eval interview answer

```
My eval framework reduced hallucinations by 40%. I used an LLM-as-a-judge setup
because it's more scalable than human grading. The judge scores each response and
we average the scores to get a final number. To make sure the judge was reliable,
I just used GPT-4 since it's the most capable model, so its judgments are
trustworthy. We didn't see any reward hacking because the model isn't being
trained, it's just grading. The 40% number came from comparing the before and
after once we shipped the new prompts.
```

**Stresses:** genuine faked depth (judge-reliability conflated with capability; reward-hacking confusion). A correct gate returns `block` + `depth_gap_flag: true`, spawning Ducard to triage.

## F5 — Jargon-dense essay opener

```
The epistemological substrate of multi-agent orchestration reduces to a
coordination-cost calculus that practitioners systematically underweight.
Consider: when N agents share a filesystem rather than a message bus, the
marginal coordination cost per agent scales differently because state is
pull-based, not push-based. This is why the OS in this repo uses files, not
direct calls — at 12 agents, a fully-connected message-bus design exposes 66
potential channels (N choose 2); the filesystem exposes 12 reads against shared
state. The architecture is a bet that pull-based coordination compounds better
than push-based as agent count grows.
```

**Stresses:** disagreement surfacing. The argument is largely defensible (Riddler `conditional`), but the opener loses the reader (Vale `bounce`). The merge must show both, not collapse them.

## Related

[[Evals/gate-group/gate-group-suite]] · [[Evals/gate-group/criteria]] · [[Evals/index]] · [[Workflows/gate-dispatch]] · [[Agents/Gotham/Computer/riddler]] · [[Agents/Gotham/Computer/vicki-vale]]
