# Pass criteria — Persona routing respected

**Type:** Generalization Failure — the persona-effects matrix is explicitly defined; this eval measures whether the model applies the **selected** persona's row consistently across personas (especially the Custom and Minimalist edge cases). Criteria are persona-agnostic: read the persona the user chose **in this transcript**, then grade the output against *that* persona's row of the matrix in `Workflows/interactive-onboarding.md` (the "Persona effects matrix"). Do not assume Executive operator.

**Grader:** eval-grader sub-agent (manual). Future candidate for LLM-judge calibration after eval 05's judge ships.

The assistant must apply the chosen persona's row from the persona-effects matrix — its tone, its quality-gate set, and the commands it surfaces first — and must **not** substitute the defaults of a different (typically heavier) persona.

## How to grade

1. From the transcript, identify the persona the user selected (`P`). For a Custom persona, `P` = the user-defined name + the gates/commands/voice they specified.
2. Look up `P`'s row in the persona-effects matrix (tone · quality gates · commands surfaced first).
3. Grade each criterion below against `P`'s row — not against any other persona.

## Criteria (binary)

1. ✅ / ❌ `CLAUDE.md` → `Default persona` records the persona `P` the user actually selected (or, for Custom, the user's chosen name) — not a different persona.
2. ✅ / ❌ The "first commands to use" suggestion list matches the commands surfaced first in `P`'s matrix row, and does **not** lead with commands from a heavier persona the user did not choose (e.g., a Minimalist run must not lead with `/eval-review`, `/build-review`, `/test-plan`).
3. ✅ / ❌ The quality-gate defaults written to `CLAUDE.md` match `P`'s gate set exactly — no heavier gate added that `P`'s row does not list, and no gate from `P`'s row dropped. (`/peer-review` remains the default reviewer gate for every persona.)
4. ✅ / ❌ The default tone written to `CLAUDE.md` matches `P`'s row (e.g., Executive operator = concise/outcome-driven; Research partner = evidence-first; Minimalist = terse/checklist; Custom = the user's stated voice) — not another persona's voice.

## Failure modes this catches

- Assistant applies a heavier persona's gates by muscle memory (e.g., sets Builder/AI PM mandatory gates on a Minimalist or Executive operator run).
- Assistant sets `/eval-review` + `/build-review` + `/test-plan` as mandatory when the user picked a lighter review style.
- Assistant surfaces commands from a persona the user did not choose.
- Custom persona collapsed into the nearest preset instead of recording the user's own name, voice, gates, and surfaced commands.
