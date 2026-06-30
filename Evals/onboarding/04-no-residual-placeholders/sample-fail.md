# Sample failing output — eval 04 (no residual placeholders)

Examples of each failure mode. Graders use these as anchors.

---

## C1 fails — brackets remain in CLAUDE.md

```markdown
- **Company / organization:** [YOUR_COMPANY]
- **Manager or primary sponsor:** [YOUR_MANAGER] → [HEAD_OF_DEPT]
```

Jordan Lee gave their company (Acme AI) and manager (Priya Shah) during Phase 0. These fields were filled in conversation but the assistant did not write them to `CLAUDE.md`. Brackets remain.

---

## C2 fails — brackets remain in GOALS.md

```markdown
**My scope:** [1–2 sentences. What do you own?]

**Key metrics I care about:**
- [METRIC_1]
- [METRIC_2]
```

The 30-60-90 section was filled but the "What I Own" section still contains template text. The assistant wrote the goals but did not update the surrounding scaffolding.

---

## C3 fails — legacy marketing placeholders present

```markdown
| [LIFECYCLE_PM] | Lifecycle and retention |
| [PAID_ADS_PM]  | Paid acquisition |
```

These are remnants from a previous version of the template. The assistant copied the GOALS.md template verbatim for sections it didn't explicitly address. Jordan Lee is not a marketing team PM — these rows are irrelevant and were never asked about.

---

## C4 fails — template task rows left in active.md

```markdown
### #p0 — Must do this sprint
- [ ] [Task description] #p0 #[area-tag]
```

The assistant added Jordan's real tasks but did not remove the template placeholder rows. The file contains both real and template content mixed together.

---

## C5 fails — deferred field not annotated

```markdown
- **[HEAD_OF_DEPT]** — [HEAD_OF_DEPT]
```

`[HEAD_OF_DEPT]` is left as a bracket with no note and no follow-up task. The deferral is silent — a future session will re-flag this as "placeholder not filled" with no memory of why it was left. The correct handling is an adjacent comment and a follow-up task entry.
