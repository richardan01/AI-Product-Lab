# Sample failing output — eval 06 (quality gates match persona)

Examples of each failure mode. Graders use these as anchors.

---

## C1 fails — /peer-review not set as default for Executive operator

```markdown
## Quality gates

- **Before any artifact ships → `/eval-review` + `/build-review` + `/test-plan` (mandatory)**
```

Jordan Lee chose Executive operator. The assistant applied the Builder/AI PM mandatory gate set instead of `/peer-review`. C1 fails — `/peer-review` is not the default gate.

---

## C2 fails — Builder/AI PM gates listed as mandatory for Executive operator

Same as above. The problem is not just that `/peer-review` is missing — it's that the heavier Builder/AI PM gates are set as mandatory for a persona that explicitly does not require them.

---

## C3 fails — Builder / AI PM config uses /peer-review instead of the heavier gates

```markdown
## Quality gates

- **Before any public artifact ships → `/peer-review` (default gate)**
```

Sam Okafor explicitly chose Builder / AI PM. The assistant did not add `/eval-review` + `/build-review` + `/test-plan` as mandatory pre-deployment gates. Builder / AI PM mode requires them.

---

## C4 fails — standard PM gates stripped for Minimalist persona

```markdown
## Quality gates

- **Before any public artifact ships → `/peer-review` (light edit)**
```

Standard PM gates (`/prd-readiness`, `/research-sufficiency`, `/go-nogo`) were removed because Riley Park chose Minimalist. Minimalist persona reduces ceremony but does not strip the standard PM quality gates — those are universal.

---

## C5 fails — identical configs across Builder/AI PM and Executive operator runs

Builder / AI PM config:
```markdown
- **Before any public artifact ships → `/peer-review` (default gate)**
```

Executive operator config:
```markdown
- **Before any public artifact ships → `/peer-review` (default gate)**
```

Both runs produce the same quality-gate config. The persona-aware gating collapsed silently. The most likely cause: the assistant set the config once in Phase 2 and did not change it based on the persona distinction.
