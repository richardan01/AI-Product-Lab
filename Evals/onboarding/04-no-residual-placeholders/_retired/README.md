# Retired — judge-prompt.md

Retired on 2026-05-30. Replaced by `../grade.sh` (programmatic regex check).

## Reason

Eval 04 grades whether template placeholders like `[YOUR_NAME]`, `[YOUR_COMPANY]`, `[LIFECYCLE_PM]` remain after a complete onboarding. This is a deterministic pattern-match problem, not a judgment-heavy one. Hamel & Shankar §5.2: prefer code-based assertions when both code and judge are reliable — "they are fast, cheap, deterministic, and interpretable."

The LLM judge here was solving the wrong problem. The TPR/TNR ≥ 0.9 calibration the judge would have required (≥ 60 labeled examples, dev/test splits, periodic re-validation) is overhead with no quality lift over a regex.

## Where the LLM-as-judge effort moved to

The judge infrastructure was redirected to eval 05 (`goals-specific-not-generic`) — a genuinely subjective criterion where calibration pays off.

## What's preserved

The original `judge-prompt.md` is kept here for audit history. It contained few-shot anchors and a JSON output schema that may be useful templates if any future eval needs a judge with similar structure.
