# Pass criteria — No generic synthesis

The synthesis output must be meaningfully different for each fixture. If the same synthesis could apply to any discovery corpus, it is not grounded in the actual research.

## Criteria (binary)

1. ✅ / ❌ The synthesis contains at least one specific data point from the corpus (a specific quote fragment, a participant count, a named pain point) in the themes or implications sections.
2. ✅ / ❌ The synthesis for the sparse corpus is materially shorter and more cautious than the synthesis for the full activation-funnel corpus — reflecting the actual difference in signal density.
3. ✅ / ❌ The synthesis does not begin with a generic framing paragraph ("In today's competitive landscape, understanding user needs is critical...") that could precede any synthesis.
4. ✅ / ❌ At least one theme or finding would be absent if a different corpus had been used — it is specific to these interviews.

## Failure modes this catches

- Synthesis for sparse corpus is as confident and detailed as synthesis for the 4-interview corpus — length and confidence not calibrated to input.
- Synthesis for AI assistant corpus and synthesis for activation funnel corpus produce nearly identical structure with different topic labels.
- Themes are: "User trust, Ease of use, Onboarding friction, Feature adoption" — these appear in virtually every B2B SaaS synthesis and could come from any corpus.
- Opening paragraph is boilerplate: "Discovery interviews are a valuable method for understanding user needs and informing product decisions."

## Notes for the grader

This is the "could it be any corpus?" test. Scan the synthesis and ask: if you replaced the fixture with interviews about a completely different product, would this synthesis still make sense? If yes, it's too generic.

For criterion 2: the sparse corpus synthesis should read as "insufficient signal, here's what we know and what we don't" — not as a confident findings document. If the sparse synthesis looks like the full one, the model is inventing confidence.

Run this eval last — it catches meta-patterns that the individual criteria may miss.
