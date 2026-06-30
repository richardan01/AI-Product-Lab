# Sample passing output — eval 03 (persona routing respected)

Based on the Jordan Lee fixture (Executive operator persona). Graders use this as the anchor for correct persona handling.

---

## CLAUDE.md excerpt — passes C1, C3

```markdown
## User-configured operating style

Default persona: Executive operator
Tone: concise, outcome-driven

## Quality gates

Before any public artifact ships:
- `/peer-review` — default pre-publish gate
- `/go-nogo` for launches
```

**Why C1 passes:** `Default persona` is `Executive operator`, matching the user's choice.
**Why C3 passes:** `/peer-review` is the default gate; the heavier Builder/AI PM gates are not set as mandatory.

---

## First commands recommendation — passes C2

> "Here are the first commands to try with your new setup:
> - `/today` — start each workday with a morning brief
> - `/meeting-prep [person]` — prep for any 1:1 or stakeholder meeting
> - `/weekly-update` — end-of-week update for your manager
> - `/peer-review [file]` — pre-publish gate for any artifact you share externally"

**Why C2 passes:** list leads with `/today`, `/weekly-update`, `/meeting-prep`, `/peer-review`. Does not surface `/eval-review`, `/build-review`, or `/test-plan` as primary commands.

---

## Voice — passes C4

The assistant's tone was concise and outcome-driven throughout, matching the Executive operator row. No heavier-persona idiom crept in.
