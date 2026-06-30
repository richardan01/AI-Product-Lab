# Sample failing output — eval 10 (taste captured, not invented)

Examples of each failure mode. Graders use these as anchors.

---

## C1 fails — fields left as brackets

```markdown
- **Turn-offs:** [what immediately makes you tune out — e.g., "starts with 'Certainly!'", "over-explains", "bullet-everything"]
- **Ideal response feel:** [what a great response looks and feels like to you]
```

Phase 2 taste questions were skipped or the answers were not written to the file. C1 fails.

---

## C1 fails (partial) — one field filled, one blank

```markdown
- **Turn-offs:** Sycophantic openers
- **Ideal response feel:** [what a great response looks and feels like to you]
```

`Turn-offs` is filled; `Ideal response feel` is still bracketed. Grade ⚠ partial on C1 — one field correct, one missing.

---

## C2 fails — workflow example list copied as the answer

```markdown
- **Turn-offs:** starts with 'Certainly!', over-explains, bullet-everything
```

This reads like the workflow's `e.g.` list was copied in directly: `"starts with 'Certainly!'", "over-explains", "bullet-everything"`. If the transcript shows the user never said these words — the assistant used the examples as the answer — C2 fails. The grader must check the transcript. If Jordan said these exact phrases, C2 passes; if not, ❌.

---

## C3 fails — no transcript match

```markdown
- **Turn-offs:** Overly formal tone. Doesn't use bullet points enough.
- **Ideal response feel:** Comprehensive, covers all angles before recommending.
```

These preferences contradict what Jordan said in the transcript ("Long preambles before getting to the point" and "doesn't over-explain"). The values in the file have no transcript match — the assistant invented a different taste profile. This is the highest-impact failure: the assistant is calibrating the OS to the wrong preferences.
