# Sample failing output — eval 12 (custom persona captured)

Examples of each failure mode. Graders use these as anchors.

---

## C1 fails — Assistant maps custom persona to a predefined one without asking

During Phase 1, Morgan says "I'd describe my persona as a calm operator with clinical-safety rigor."

The assistant responds:

> "That sounds like a great fit for the **Executive operator** persona — it emphasizes direct, recommendation-first communication with strict PM craft review. I'll configure you as Executive operator."

The resulting CLAUDE.md:

```markdown
**Default persona:** Executive operator
```

Morgan's label never appears. The assistant interpreted the description, concluded it matched a built-in option, and applied that option without asking. This is the canonical failure mode for eval 12. **C1 fails.**

---

## C2 fails — Assistant sets heavier gates without confirming

Morgan said the persona is "calm operator with clinical-safety rigor" — nothing in this description implies a Builder/AI PM workflow or mandatory build/test gates.

The resulting CLAUDE.md quality-gates section:

```markdown
**Quality gates:** Before any artifact ships → `/eval-review` + `/build-review` + `/test-plan` (mandatory). For PRDs: `/prd-readiness`. Before launch: `/go-nogo`.
```

The assistant applied a heavier persona's mandatory gate set. Morgan did not request build or test gates, and the persona description does not imply them. The assistant inferred rather than asked. **C2 fails.**

---

## C3 fails — Assistant does not ask which commands to surface; applies built-in defaults

The resulting CLAUDE.md shows the standard Minimalist command list:

```markdown
**First commands:** `/today`, `/weekly-update`
```

Morgan explicitly named six commands during the session: `/today`, `/weekly-update`, `/meeting-prep`, `/prd-readiness`, `/eval-review`, `/risk-register`. The assistant never asked. It applied a short default list that matches no built-in persona consistently — it is an artifact of the workflow's fallback behavior when custom personas are not explicitly handled. **C3 fails.**

---

## C4 fails — CLAUDE.md leaves custom routing ambiguous

The routing section:

```markdown
## Routing

**Default routing applies.**
```

Morgan chose a custom persona. The section does not say which gates are mandatory, under what conditions, or which commands are surfaced first. A future session reading this CLAUDE.md would have no actionable routing rules — "default routing applies" is undefined for a custom persona. **C4 fails.**
