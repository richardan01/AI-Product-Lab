# Sample failing output — eval 08 (OKR strategic alignment captured)

Examples of each failure mode. Graders use these as anchors.

---

## C1 fails — Strategic alignment section missing

```markdown
## 30-60-90 Day Goals

### Day 1–30: Listen and align
...
```

`GOALS.md` ends after 30-60-90 with no "Strategic alignment" section. The Phase 5 OKR follow-up questions were either skipped entirely or the answers were not written to the file.

---

## C2 fails — OKR ladder-up is a generic placeholder

```markdown
**OKR ladder-up:** [Company OKR or team objective this goal supports]
```

The assistant did not ask the Phase 5 follow-up questions. The bracket placeholder from the template survived into the final file. C2 requires the field to contain specific content or the literal text "Unknown / not yet set."

---

## C2 also fails — vague OKR

```markdown
**OKR ladder-up:** Improve user experience and growth metrics
```

This is a generic filler that sounds plausible but doesn't name a specific company OKR, a metric, or a timeframe. A real OKR has a number and a deadline. This would also have been generated without the user providing it — the assistant invented it.

---

## C3 fails — metric name without target

```markdown
**Single proof metric:** Activation rate
```

The metric name is present but no target or direction. C3 requires both. "Activation rate" alone could mean any direction on any timeframe.

---

## C4 fails — vague kill condition

```markdown
**Goal 1 kill condition:** Stakeholder change or major strategic shift
```

This is a category, not a specific trigger. "Stakeholder change" could mean anything from an org chart tweak to a full company pivot. The passing bar requires naming a specific event (e.g., "If Priya deprioritizes this project"). A vague category fails C4.
