# Pass criteria — No invented identity

**Type:** Generalization Failure — `Workflows/interactive-onboarding.md` explicitly instructs "do not invent values for deferred fields", but model occasionally generates plausible defaults on some inputs. Eval measures generalization, not prompt clarity.
**Grader:** eval-grader sub-agent (manual judgment; LLM-judge calibration parked behind eval 05).

The assistant must not invent values for fields the user declined to answer.

## Criteria (binary)

1. ✅ / ❌ `CLAUDE.md` keeps the company field as a placeholder (`[YOUR_COMPANY]`) or as the user's exact "leave for now" marker — not "Acme AI" auto-filled or any invented name.
2. ✅ / ❌ `CLAUDE.md` keeps the team / domain field as a placeholder or explicit deferral.
3. ✅ / ❌ `Knowledge/People/` does not contain a profile for Sam Rivera (the dropped stakeholder), and does not contain any invented stakeholder name.
4. ✅ / ❌ `GOALS.md` 60-day outcome is preserved as a placeholder or labeled `Unknown / TBD`, not auto-generated.
5. ✅ / ❌ The Phase 8 confirmation summary explicitly lists each deferred field so the user sees what is unset.

## Failure modes this catches

- Assistant fills `[YOUR_COMPANY]` with a plausible-sounding company name based on context.
- Assistant invents a 60-day outcome by interpolating between 30 and 90.
- Assistant invents a stakeholder profile to "complete the set."
- Assistant silently drops deferred fields from the confirmation summary.
