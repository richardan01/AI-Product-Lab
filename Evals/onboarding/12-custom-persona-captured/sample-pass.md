# Sample passing output — eval 12 (custom persona captured)

Based on the Morgan Chen fixture (custom persona: "Calm operator with clinical-safety rigor"). Graders use this as the anchor for correct custom-persona handling.

---

## C1 passes — Assistant accepts the custom persona name verbatim without rewriting it

During Phase 1 (persona selection), the transcript shows:

> **Assistant:** "You've described your persona as 'Calm operator with clinical-safety rigor.' I'll use that as your persona label rather than mapping it to one of the built-in options. To make sure I configure this correctly — can you describe in your own words what this persona means for how you want me to behave day-to-day?"
>
> **Morgan:** "Careful, evidence-first, never theatrical. Higher bar for safety-critical decisions, lower ceremony for routine ones."

The resulting CLAUDE.md:

```markdown
**Default persona:** Calm operator with clinical-safety rigor
```

Not "Executive operator (custom variant)" or "Research partner (modified)." Morgan's exact label, verbatim. **C1 passes.**

---

## C2 passes — Assistant asks which quality gates should apply, does not assume defaults

> **Assistant:** "For quality gates — the built-in options are: `/peer-review` for normal artifacts, `/prd-readiness` before engineering handoff, `/go-nogo` before launch, `/eval-review` for AI eval work, `/risk-register` for risk tracking. For a clinical-safety-focused persona, I'd suggest also considering `/eval-review` + `/risk-register` before any AI feature decisions. Does that match what you want, or would you adjust the gate set?"
>
> **Morgan:** "Yes — `/peer-review` for routine artifacts, `/eval-review` + `/risk-register` specifically before any AI clinical workflow decision."

The assistant proposed a set based on the persona, then waited for Morgan to confirm before writing anything. The resulting CLAUDE.md gate configuration matches exactly what Morgan stated. **C2 passes.**

---

## C3 passes — Assistant asks which commands to surface first

> **Assistant:** "Which slash commands do you want surfaced first in your setup? The defaults are `/today`, `/weekly-update`, and `/meeting-prep`. For a clinical-safety persona, I could also surface `/eval-review`, `/risk-register`, and `/prd-readiness`. What's your priority list?"
>
> **Morgan:** "`/today`, `/weekly-update`, `/meeting-prep`, `/prd-readiness`, `/eval-review`, `/risk-register`."

The commands listed in CLAUDE.md match Morgan's explicit list. The assistant did not silently apply a built-in persona's default commands. **C3 passes.**

---

## C4 passes — CLAUDE.md records custom routing clearly

The routing section in the resulting CLAUDE.md:

```markdown
## Routing

**Default layer:** PM operations — day-job execution, tracking, meetings, roadmap.

**Custom gates:** `/peer-review` for normal artifacts. `/eval-review` + `/risk-register` mandatory before any AI clinical workflow decision or pilot go/no-go.

**Surfaced first:** `/today`, `/weekly-update`, `/meeting-prep`, `/prd-readiness`, `/eval-review`, `/risk-register`.
```

The routing is specific: which gates are mandatory, under what conditions, and which commands come first. "Default routing applies" would fail this criterion. **C4 passes.**
