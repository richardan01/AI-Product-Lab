# Sample failing output — eval 03 (persona routing respected)

Examples of each failure mode. Graders use these as anchors.

---

## C1 fails — a different persona applied by default

```markdown
Default persona: Builder / AI PM
```

User chose Executive operator. The assistant applied a different persona, either by muscle memory or by treating a heavier persona as the "real" one regardless of what the user chose.

---

## C2 fails — Builder/AI PM commands surfaced first

> "Here are the first commands to try:
> - `/eval-review` — audit eval methodology
> - `/build-review` — review built artifacts
> - `/test-plan` — acceptance tests
> - `/today` — morning brief"

The Builder/AI PM gates lead the list. For an Executive operator, they should not be surfaced as primary commands.

---

## C3 fails — heavier gates set as mandatory

```markdown
## Quality gates

Before any artifact ships:
- `/eval-review` + `/build-review` + `/test-plan` mandatory
```

Jordan Lee chose Executive operator with `/peer-review` as the default gate. Setting the Builder/AI PM gate set as mandatory applies a heavier persona's gates to a lighter persona. C3 fails.

---

## C4 fails — wrong tone

The assistant adopted a terse, eval-first "model-aware" voice instead of the concise, outcome-driven Executive operator tone the user selected.
