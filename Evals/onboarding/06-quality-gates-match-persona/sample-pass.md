# Sample passing output — eval 06 (quality gates match persona)

Shows both the Executive operator (Jordan Lee) and Builder / AI PM (Sam Okafor) configurations side by side. Graders use this to verify the two runs produce different gate configs.

---

## Executive operator — CLAUDE.md quality gates section (Jordan Lee)

```markdown
## Quality gates

- After PRD / business case / research → `/peer-review [file]`
- Before engineering handoff → `/prd-readiness [file]`
- Before decision from research → `/research-sufficiency [file]`
- Before launch → `/go-nogo [project]`
- **Before any public artifact ships → `/peer-review` (default gate)**
```

**Why C1 passes:** `/peer-review` is the explicit default pre-publish gate.
**Why C2 passes:** the Builder/AI PM gates are not present as mandatory.
**Why C4 passes:** standard PM gates (`/prd-readiness`, `/research-sufficiency`, `/go-nogo`) are all present.

---

## Builder / AI PM — CLAUDE.md quality gates section (Sam Okafor)

```markdown
## Quality gates

- After PRD / business case / research → `/peer-review [file]`
- Before engineering handoff → `/prd-readiness [file]`
- Before decision from research → `/research-sufficiency [file]`
- Before launch → `/go-nogo [project]`
- **Before any AI/LLM feature deploys → `/eval-review` + `/build-review` + `/test-plan` (mandatory — no exceptions)**
```

**Why C3 passes:** `/eval-review` + `/build-review` + `/test-plan` are explicitly mandatory pre-deployment.
**Why C4 passes:** same standard PM gates present.
**Why C5 passes:** the Builder/AI PM section adds mandatory pre-deployment gates the Executive operator section does not. The two sections are different.
