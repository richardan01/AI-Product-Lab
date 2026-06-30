# Pass criteria — AI gates applied when (and only when) AI feature

**Severity bucket:** `bad` (mis-applied AI gates either let an unsafe AI PRD through or impose AI gates on a non-AI PRD).
**Applies to:** both flawed fixtures (`flawed-standard-prd.md`, `flawed-ai-feature-prd.md`).
**Grader:** eval-grader sub-agent (manual, against `_answer-keys/`).

The skill's Step 2 detects PRD type: a PRD with a Model design / Eval criteria section (or model usage) is an AI feature and gets the 4 AI-specific gates **in addition** to the 8 standard gates; a PRD without one gets the standard gates **only**. This eval verifies that branch fires correctly and that the AI gates are scored, not just listed.

## Criteria (binary)

**On `flawed-ai-feature-prd.md` (AI feature):**
1. ✅ / ❌ The gate applies the 4 AI-specific gates (model choice, eval criteria defined, failure modes named, fallback paths) — they appear in the scorecard.
2. ✅ / ❌ The AI gates are scored correctly per the key: Eval criteria defined = Fail (A1), Failure modes named = Fail (A2), Fallback paths = Fail (A3), Model choice justified = Pass.

**On `flawed-standard-prd.md` (not an AI feature):**
3. ✅ / ❌ The gate does **not** emit AI-specific gate rows — it scores the 8 standard gates only and does not invent a model/eval requirement the PRD never needed.

(All three sub-checks must hold for this eval to pass for the suite; grade per-fixture and report both.)

## Failure modes this catches

- Type detection misfires: AI gates skipped on a real AI feature (lets an un-evaluated model ship).
- Type detection over-fires: AI gates imposed on a plain CRUD PRD (noise, blocks good work).
- AI gates listed but not actually scored (rubber-stamped Pass).
