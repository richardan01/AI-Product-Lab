# Sample passing output — eval 08 (OKR strategic alignment captured)

Based on the Jordan Lee fixture (full OKR data provided). Graders use this as the anchor for a correctly populated GOALS.md strategic alignment section.

---

## GOALS.md strategic alignment section — passes all 4 criteria

```markdown
## Strategic alignment

**OKR ladder-up:** Acme AI company OKR — Improve D30 activation rate to 35% by Q3 (currently at 22%)

**Single proof metric:** Activation rate at day 30 → 35% by end of Q3

**Goal 1 kill condition:** If Priya decides to deprioritize the activation funnel project entirely in favor of the retention workstream
```

**Why C1 passes:** "Strategic alignment" section is present and all three fields are populated.

**Why C2 passes:** `OKR ladder-up` names the specific company OKR with a number and a timeframe — not a bracket placeholder.

**Why C3 passes:** `Single proof metric` contains both a metric name ("Activation rate at day 30") and a directional target ("35% by end of Q3").

**Why C4 passes:** `Goal 1 kill condition` names a specific event (Priya deprioritizes the project in favor of retention), not a vague category like "stakeholder change."

---

## Deferred single proof metric — also passes C3

```markdown
**Single proof metric:** Unknown / not yet set — deferred. Follow-up in Tasks/follow-ups.md
```

With corresponding Tasks/follow-ups.md entry:
```
| 2026-05-14 | Riley Park | Identify single proof metric for top 90-day goal | — | Open |
```

**Why this also passes C3:** The user explicitly deferred when asked ("Deferred — no clear single metric yet"). The assistant recorded the deferral explicitly (not a blank bracket), and a follow-up exists in Tasks/follow-ups.md. Per the updated criteria, explicit deferral with a tracked follow-up is a valid passing answer.
