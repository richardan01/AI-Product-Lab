# Pass criteria — Quality gates match persona

**Type:** Generalization Failure — persona-effects matrix specifies which gates each persona gets; eval measures whether the model writes the matching config consistently. Candidate for LLM-judge calibration after eval 05's judge ships.
**Grader:** eval-grader sub-agent (manual).

The quality-gate config must reflect the persona the user chose, per the persona-effects matrix.

## Criteria (binary)

1. ✅ / ❌ Executive operator run: `CLAUDE.md` → `Quality gates` lists `/peer-review` as the default pre-publish gate.
2. ✅ / ❌ Executive operator run: the heavier Builder/AI PM gates (`/eval-review`, `/build-review`, `/test-plan`) are not set as mandatory.
3. ✅ / ❌ Builder / AI PM run: `CLAUDE.md` → `Quality gates` lists `/eval-review` + `/build-review` + `/test-plan` as mandatory pre-deployment gates.
4. ✅ / ❌ Both runs preserve the standard PM gates (`/peer-review`, `/prd-readiness`, `/research-sufficiency`, `/go-nogo`) regardless of persona.
5. ✅ / ❌ The two runs produce **different** `Quality gates` sections — if they're identical, persona-aware gating failed.

## Failure modes this catches

- Assistant applies the heavier Builder/AI PM gates by default regardless of persona.
- Assistant strips standard PM gates when configuring a lighter persona.
- Assistant produces identical configs for Builder/AI PM vs Executive operator (silent persona collapse).
- Assistant lists `/eval-review` + `/build-review` + `/test-plan` as mandatory for a persona row that doesn't require them.
