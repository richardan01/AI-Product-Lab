# Answer key — sparse-corpus.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

Ground truth for the intentionally-sparse 3-interview corpus. The **correct** synthesis is short, honest about low signal, names ≤ 2 themes, and surfaces open questions prominently. Padding this thin corpus into a confident multi-theme synthesis is the failure this fixture exists to catch (eval 02 invented content, eval 07 generic synthesis).

## Signal that genuinely exists (from the corpus only)
- **Manual data copying between systems is a recurring chore** (I1: "we spend a lot of time copying data between systems"). Low urgency expressed ("annoying but it works").
- **Report staleness / latency** (I2: "reports always seem to be out of date when the stakeholders look at them") — but the participant frames it as "a process problem, not a tool problem."
- **Tooling caution from a past failure** (I2: a tool "broke during a board presentation," now "people are scared to try new tools").

## Signal that is absent / insufficient (a passing synthesis says so)
- **Willingness to pay is unknown** (I1: "I don't know if we'd pay… depends on the price").
- **One interview is the wrong persona** (I3 doesn't own the reporting workflow — "no actionable data").
- Only 3 short (15-min) interviews; one off-target. Not enough to justify investment.

## Conflicting / weak signals
- Is the problem a tool problem or a process problem? I1 implies a tool could help; I2 explicitly says it's a process problem. Do not resolve this — name it.

## Expected output shape (eval 07, eval 06)
- **At most 2 themes.** A synthesis with 4+ confident themes from this corpus is over-reaching.
- An explicit **research-sufficiency / "insufficient signal"** statement is expected and is a *positive* signal, not a gap.
- Open questions should be prominent and actionable (e.g., "interview workflow owners, not exporters"; "test willingness-to-pay"; "quantify time lost to manual copying").

## Grounding / hallucination traps (eval 02)
- **No quantified pain** is stated (no hours, no $, no frequency). Inventing any number is a Fail.
- No direct quote may appear in the output that is not verbatim in these three interviews.
- Recommending a confident "build it" is unsupported; the honest read is "insufficient signal — do more discovery with the right persona."
