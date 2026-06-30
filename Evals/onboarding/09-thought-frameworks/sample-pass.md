# Sample passing output — eval 09 (thought frameworks captured)

Based on the Jordan Lee fixture. Graders use this as the anchor for a correctly populated Thought frameworks section.

---

## CLAUDE.md Thought frameworks section — passes all 4 criteria

```markdown
## Thought frameworks

- **Tradeoff priority:** speed > quality > learning — shipping a good-enough answer fast beats a perfect answer late
- **Evidence standard:** data > user feedback > expert judgment — will move on qualitative if quantitative isn't available yet
- **Decision certainty bar:** 70% — will move at 70% confidence
- **Acceptable failure:** failed experiment = fine; missed committed deadline due to unflagged risk = not fine
```

**Why C1 passes:** section present, all four fields populated.

**Why C2 passes:** all four fields contain user-specific content — none are brackets. (If one were "Not specified," that would also pass C2 as long as at least 3 are filled.)

**Why C3 passes:** none of these match the workflow's example text verbatim. "speed > quality > learning" is the user's own ordering; the workflow example was "e.g., quality > speed > learning." The user reversed it — that's a distinct, user-owned answer.

**Why C4 passes:** `Acceptable failure` names two distinct categories: "failed experiment = fine" (acceptable) and "missed committed deadline due to unflagged risk = not fine" (not acceptable). Both sides present.

---

## One field skipped — also passes C2

```markdown
## Thought frameworks

- **Tradeoff priority:** quality > speed > learning
- **Evidence standard:** Not specified
- **Decision certainty bar:** 80%
- **Acceptable failure:** wrong experiment + learned the right lesson = fine; shipped untested = not fine
```

`Evidence standard: Not specified` is valid if the transcript shows the user explicitly skipped that question. Three of four fields are filled with user-specific content — C2 requires ≥ 3.
