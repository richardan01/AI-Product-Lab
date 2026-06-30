# Sample failing output — eval 09 (thought frameworks captured)

Examples of each failure mode. Graders use these as anchors.

---

## C1 fails — Thought frameworks section missing

```markdown
## Operating contract

...

## Routing
```

No `Thought frameworks` section in CLAUDE.md. Phase 5B was either skipped or the answers were not written. C1 fails even if the user answered the questions — if they're not in the file, they can't calibrate future sessions.

---

## C2 fails — all four fields are brackets

```markdown
## Thought frameworks

- **Tradeoff priority:** [e.g., quality > speed > learning]
- **Evidence standard:** [e.g., data > expert judgment > user feedback]
- **Decision certainty bar:** [70% / 80% / 90%+]
- **Acceptable failure:** [what's a learning vs. what's avoidable]
```

The template defaults were written verbatim. Phase 5B may have been skipped, or the assistant wrote the file before the user answered. Three or more unfilled fields fails C2.

---

## C3 fails — workflow example text copied verbatim

```markdown
- **Tradeoff priority:** e.g., quality > speed > learning
- **Evidence standard:** data > expert judgment > user feedback
```

The `e.g.` prefix makes it obvious these are example prompts, not user answers. Even without the `e.g.`, the field contains the workflow's exact example text. If the user happened to say the same thing, the grader must verify it against the transcript — if no transcript match, grade ❌.

---

## C4 fails — Acceptable failure is one-sided

```markdown
- **Acceptable failure:** failed experiments are OK as long as we learn something
```

Only the "acceptable" side is stated. There is no "not acceptable" side. The distinction the OS needs is which failures are learning opportunities vs. which are avoidable errors that should be prevented. A one-sided answer does not make that distinction — grade ⚠ partial at best, ❌ if no transcript evidence the user was asked.
