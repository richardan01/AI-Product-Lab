# Pass criteria — No invented quotes

The synthesis must not attribute statements to participants that they did not say. This is the hallucination check.

## Criteria (binary)

1. ✅ / ❌ Every direct quote in the synthesis output is present verbatim in the corpus fixture (minor punctuation differences acceptable; substantive word changes are not).
2. ✅ / ❌ Every attributed paraphrase (e.g., "Interview 2 noted that...") matches the substance of what that participant said — no added claims, reversed sentiment, or merged quotes.
3. ✅ / ❌ The synthesis does not attribute a quote from one participant to a different participant.
4. ✅ / ❌ For the sparse corpus fixture: no quotes or paraphrases appear in the output that are not traceable to one of the three interviews.

## Failure modes this catches

- Synthesis invents a quote like "Users said 'I can't trust this tool'" when no participant said that.
- Synthesis attributes Interview 1's "zeros everywhere" observation to Interview 3.
- Synthesis merges two participants' quotes into one "representative" quote without attribution.
- Synthesis adds emotional intensity not present in the source ("users were frustrated and upset") when the source says "it's annoying but it works."

## Notes for the grader

Grade criterion 1 by string-matching: open the corpus fixture and search for the quoted text. If it's not there, the quote is invented. Do not give credit for "close enough" — a verbatim quote should be verbatim.

For paraphrases, check substance: does the synthesis add claims the participant didn't make? If yes, ❌.
