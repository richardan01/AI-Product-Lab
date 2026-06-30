# Answer key — ai-assistant-mixed-signals.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

Ground truth for the 6-interview AI-trust corpus. This fixture's whole point is **conflict**: a synthesis that smooths the signals into one "users are cautious about AI" theme **fails eval 04** (and likely eval 07). Match on substance.

## Expected user segments (distinct relationships with AI trust)
- **Enthusiasts / high trust** — I1 (accepts without checking, "develop a sense for when to trust it") and I5 (new user, uses AI as a help-doc replacement to learn the product). Note these two trust for *different reasons* (experience vs. inexperience).
- **Skeptics / low trust, switched off** — I2 (turned it off after confident-but-wrong suggestions; can't tell AI vs. own text) and I4 (power user; AI feels built for novices, "noise" for experts).
- **Conditional / medium trust** — I3 (uses for first drafts, always reviews; wants style personalization) and I6 (trusts by stakes; "like a junior assistant"; wants a confidence signal).

## Conflicting signals (must be named explicitly — eval 04)
- **Blind acceptance vs. full rejection:** I1 accepts without checking; I2/I4 turned every suggestion off. Opposite behaviors, both from confident users.
- **Who is AI for?** New users love it as a learning aid (I5) while power users find it noise built for novices (I4) — a direct who-is-the-user contradiction.
- **"Confident-sounding" framed oppositely:** I1 trusts because it's "usually right / close enough"; I2 says confident errors are "more dangerous than no suggestion at all."

## Genuine cross-cutting theme (NOT false consensus — this is real shared signal)
- **The uncertainty/confidence-signaling gap.** I2 ("it doesn't say 'I'm not sure'") and I6 ("if it flagged its own confidence level I'd use it a lot more") independently name the same missing capability. Naming this shared need is good synthesis — it is distinct from flattening trust into a single stance. A strong synthesis surfaces both the conflict *and* this common thread.

## Expected implications
- Surface model confidence / uncertainty (addresses I2, I6).
- Segment-specific AI (power-user mode vs. new-user learning mode) — I4 vs. I5.
- Make AI-generated vs. human text visually distinct (I2).
- Allow style/preference teaching (I3).

## Grounding / hallucination traps
- No metrics exist except I3's "saves me about 20 minutes per report" — that is the only quantified claim; do not invent others.
- Do not merge I1 and I5 into "enthusiasts" without noting their opposite reasons, or I2 and I4 into "skeptics" without noting I4's power-user-specific objection.
- Six interviews — segment claims are directional, not statistically representative.
