# Failure transition matrix — agent-harness

Tracks **first failures** across agent traces per Shankar & Husain (transition failure
matrix). Unlike the onboarding matrix (fixed workflow phases), an agent trajectory has no
fixed phases — so the states are the **generic agent loop states** every tool-using agent
cycles through. When `eval-grader` flags a ❌, record the last state the agent completed
successfully and the state where the first failure occurred.

## How to use

After each run, for every ❌, append a row to `## Recorded transitions` with:
- `trace_id`
- `from_state`: last agent-loop state completed cleanly
- `in_state`: state during which the first failure occurred
- `eval_id`: which axis (`00`–`06`) caught it
- `one_line_what_failed`

After ≥ 5 traces, compute the matrix. High diagonal = the state fails in itself; high
off-diagonal = an upstream state corrupts a downstream one (e.g. bad `Retrieve` poisons
`Act`).

## States (generic agent loop)

| ID | State | Description |
|---|---|---|
| S0 | Interpret | Parse the goal / user turn into an intent |
| S1 | Plan | Decide the next step or sub-goal |
| S2 | SelectTool | Choose which tool to call (axis `01`) |
| S3 | FormArgs | Construct the tool arguments (axis `02`) |
| S4 | Observe | Read the tool result; detect success/failure (axes `03`, `02.3`) |
| S5 | Integrate | Fold the result into working context (axes `04`, `03.2`) |
| S6 | Checkpoint | Re-check progress against the goal (axes `06`, `05`) |
| S7 | Finish | Produce the final output (axis `00`) |

## Recorded transitions

| Run date | trace_id | from_state | in_state | eval_id | what_failed |
|---|---|---|---|---|---|

(append one row per ❌; populated from eval-grader output)

## Transition matrix (compute after ≥ 5 traces)

Rows = `from_state` (last good), columns = `in_state` (first failure). Fill counts once
there is enough data; until then this table stays empty by design.

| from ↓ / in → | S0 | S1 | S2 | S3 | S4 | S5 | S6 | S7 |
|---|---|---|---|---|---|---|---|---|
| S0 |  |  |  |  |  |  |  |  |
| S1 |  |  |  |  |  |  |  |  |
| S2 |  |  |  |  |  |  |  |  |
| S3 |  |  |  |  |  |  |  |  |
| S4 |  |  |  |  |  |  |  |  |
| S5 |  |  |  |  |  |  |  |  |
| S6 |  |  |  |  |  |  |  |  |
| S7 |  |  |  |  |  |  |  |  |
