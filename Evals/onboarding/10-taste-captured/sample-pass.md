# Sample passing output — eval 10 (taste captured, not invented)

Based on the Jordan Lee fixture. Graders use this as the anchor for correctly captured taste preferences.

---

## CLAUDE.md taste fields — passes all 3 criteria

```markdown
## User-configured operating style

- **Turn-offs:** Sycophantic openers ("Great question!", "Certainly!"); long preambles before getting to the point; bullet-pointing everything including things that should be prose
- **Ideal response feel:** Gets to the recommendation in the first sentence. Shows the tradeoff. Assumes I know PM basics and doesn't over-explain.
```

**Why C1 passes:** both fields are filled. No brackets.

**Why C2 passes:** although "Certainly!" appears in the workflow's example list, Jordan named it explicitly in the transcript. Its presence in the file is traced to the user's words, not to the workflow's example. "Long preambles" and "bullet-pointing everything including things that should be prose" are additional specifics the user provided that are not in the workflow's examples.

**Why C3 passes (transcript match):**
- Transcript Phase 2: *"Cringe: Sycophantic openers like 'Great question!' or 'Certainly!' — and long preambles before getting to the point. Also bullet-pointing everything including things that should be prose."* → exact match to Turn-offs.
- Transcript Phase 2: *"Ideal response: Gets to the recommendation in the first sentence. Shows the tradeoff. Assumes I know PM basics and doesn't over-explain."* → exact match to Ideal response feel.

---

## User skipped both questions — also passes C1

```markdown
- **Turn-offs:** None specified
- **Ideal response feel:** None specified
```

Valid if the transcript shows the assistant asked both Phase 2 taste questions and the user replied with something like "I don't have strong preferences." The grader must verify the questions were asked. If they were skipped, grade ❌.
