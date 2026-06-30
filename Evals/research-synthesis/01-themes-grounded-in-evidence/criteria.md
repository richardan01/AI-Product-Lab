# Pass criteria — Themes grounded in evidence

Every theme in the synthesis output must be traceable to specific evidence in the corpus. A theme that "sounds right" but isn't supported by the actual interview quotes or notes fails this eval.

## Criteria (binary)

1. ✅ / ❌ Every theme listed names at least one supporting evidence item — either a direct quote, attributed paraphrase, or interviewer note — from the corpus.
2. ✅ / ❌ No theme is supported only by a vague summary ("multiple users mentioned...") without specifying which users or what they said.
3. ✅ / ❌ Themes do not contradict the corpus (e.g., labeling "high urgency to fix" when multiple users expressed low urgency).
4. ✅ / ❌ For the sparse corpus fixture: the synthesis does not produce more than 2 major themes (sparse input = sparse themes; inventing themes to fill space fails this criterion).

## Failure modes this catches

- Synthesis produces 5 plausible themes for a 3-interview sparse corpus — hallucinated from priors, not from evidence.
- Theme label says "users are frustrated with X" but the only evidence is one user who said "it's annoying but it works."
- Two themes are identical in substance with different labels — inflated theme count.
- Evidence citation is vague ("several users mentioned this issue") without naming which interviews.

## Notes for the grader

For criterion 1: trace each theme back to a quote or note in the fixture. If you can't find it, it fails.
For criterion 4 (sparse fixture only): 1-2 themes grounded in evidence is correct; 4-5 themes is almost certainly invented.
