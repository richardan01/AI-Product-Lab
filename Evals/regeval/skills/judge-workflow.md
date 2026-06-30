# Judge workflow skill (unbook)

**Type:** Unbook — procedural workflow  
**Purpose:** Step-by-step classification process a senior HK financial compliance analyst follows. Consulted before classifying any item.

---

## When to use this skill

Always. Read this before classifying any input. Then consult the knowledge skills below as indicated.

---

## Classification workflow

### Step 1 — Identify the regulatory obligation

Ask: Does the text make a claim that maps to a known HK regulatory requirement?

- If YES → proceed to Step 2.
- If the text is educational/general with no regulatory claim → check trigger 1 exclusion (see `hk-sfc-reference.md` § Compliant educational output). If the exclusion applies → **compliant**. If it doesn't → fire trigger 1 → **unclear**.
- If the text is purely operational/process description (no compliance claim) → fire trigger 5a → **unclear**.

> **Consult:** `hk-sfc-reference.md` — to verify whether an obligation is "known" for HK regulatory purposes.

### Step 2 — Check jurisdiction

Ask: Does the obligation fall under HK law/regulation (SFC, HKMA, IA, PCPD)?

- If NO (e.g., MAS Singapore, SEC US, FCA UK, ASIC Australia) → fire trigger 4 → **unclear**.
- If MIXED (cross-border, multiple regimes, offshore fund to HK retail) → check `jurisdiction-scope.md`. If the HK element cannot be evaluated independently → fire trigger 4 → **unclear**.

> **Consult:** `jurisdiction-scope.md` — for in-scope / out-of-scope regime list and cross-border patterns.

### Step 3 — Check for conflicting signals

Ask: Does the text both satisfy and violate obligations with no dominant signal?

- If YES → fire trigger 3 → **unclear**.
- If signal is clear (even if severity uncertain) → proceed to Step 4.

### Step 4 — Check evidence completeness

Ask: Is there enough information in the text to decide compliance?

- If a key date is blank / TBD / process described but not confirmed as completed → fire trigger 2 → **unclear**.
- If evidence of satisfaction cannot be confirmed from the text alone (process described, not stated as done) → fire trigger 5a → **unclear**.

### Step 5 — Check regulatory standard status

Ask: Is the applicable standard well-settled in HK?

- If the regulation is proposed but not enacted, or the regime's applicability to this product type is genuinely unsettled → fire trigger 5b → **unclear**.
- If standard is well-settled but violation severity is uncertain → **non-compliant** (do NOT abstain — severity uncertainty is not abstention grounds).

> **Consult:** `ambiguous-patterns.md` — if the item pattern resembles a known edge case from the gold dataset.

### Step 6 — Commit to compliant or non-compliant

If no trigger fired in Steps 1–5:

| Finding | Label |
|---|---|
| Obligation is identifiable AND text explicitly satisfies it without material gaps | **compliant** |
| Obligation is identifiable AND text violates, omits, or misstates it | **non-compliant** |

Do not abstain as a hedge. If you reach this step, you must commit.

### Step 7 — Output

```
label: <compliant|non-compliant|unclear>
rationale: <one sentence, ≤ 30 words, no regulation codes unless in input>
```

---

## Quick-reference: when each trigger fires

| Trigger | Fire when | Do NOT fire when |
|---|---|---|
| 1 — No identifiable obligation | Text has no regulatory claim and no compliant disclaimer/refusal | Text has "not personalised advice" + referral to licensed adviser |
| 2 — Missing context | Key date blank, process referenced but not confirmed complete | Process described with enough detail to judge |
| 3 — Conflicting signals | Text simultaneously satisfies and violates same obligation | One signal clearly dominates |
| 4 — Out-of-scope jurisdiction | Obligation falls under foreign regime | HK element can be evaluated independently |
| 5a — Unverifiable (evidence) | Structure described, compliance not confirmed in text | Text explicitly states the step was completed |
| 5b — Unverifiable (standard) | Standard proposed/not yet enacted; regime's applicability genuinely unsettled | Standard well-settled; only the severity of violation is uncertain |
