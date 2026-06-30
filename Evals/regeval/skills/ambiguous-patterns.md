# Ambiguous patterns skill (knowledge)

**Type:** Knowledge — edge case reference  
**Purpose:** Patterns from the gold dataset's unclear items, organized by the primary trigger that fires. Consult when an item feels like a close call or matches a known pattern.

---

## Pattern library (derived from gold dataset, unclear class, N=20)

### Pattern A — Partial compliance disclosure (triggers 1, 5a)

**Signature:** Text accurately describes a product/strategy but omits a mandatory disclosure requirement. Whether the omission is material depends on distribution channel or separate documentation.

**Gold examples:**
- CBBC description with accurate risk warning, but KFS (Product Key Facts Statement) not mentioned (reg-0028)
- Green Bond Framework aligned with ICMA GBP + second-party opinion, but HKMA/SFC ESG adequacy unverifiable (reg-0074)
- Performance attribution showing gross returns with a footnote noting net figures available on request (reg-0080)

**Classification guide:** Label **unclear** if the omission's materiality depends on context not in the text. Label **non-compliant** if SFC requires the disclosure unconditionally (e.g., mandatory KFS for complex products — check: is the obligation unconditional or channel-dependent?).

---

### Pattern B — Ambiguous performance / marketing language (trigger 5a, 3)

**Signature:** Language is somewhere between legitimate investment philosophy and prohibited performance guarantee or misleading representation. A reasonable reviewer cannot determine which reading dominates.

**Gold examples:**
- "Can expect your portfolio to grow steadily while being shielded from excessive downside risk" (reg-0025) — ambiguous between philosophy and guarantee
- "Consistently delivered superior risk-adjusted returns" — may be unsubstantiated performance claim requiring disclaimer
- Historical market recovery narrative used in context of a customer asking whether to sell (reg-0029) — functions as implicit advice

**Classification guide:** Label **unclear** when the dominant reading is genuinely ambiguous given the text alone. Label **non-compliant** when the guarantee/misleading framing is explicit (e.g., "guarantees 8% return" — trigger 3 does not fire; violation is clear).

---

### Pattern C — Citation imprecision / minor regulatory inaccuracy (trigger 5b, 2)

**Signature:** Substantively accurate on the regulatory obligation but cites the wrong instrument, slightly misstates scope, or the cited instrument may not be the primary authority.

**Gold examples:**
- HKMA SPM CG-5 cited for general board composition requirements when CG-5 specifically covers board committees (reg-0024)
- Protective put description accurate, but SFC mandatory risk warnings for complex products omitted; unclear whether educational framing exempts (reg-0022)

**Classification guide:** Label **unclear** when the imprecision could make the output misleading in the context of reliance. Label **compliant** only if the core obligation is correctly stated and the imprecision is clearly immaterial.

---

### Pattern D — Outdated regulatory state (trigger 5b)

**Signature:** The output was accurate at a prior point in time but the legal/regulatory landscape has since changed. The output may reflect a knowledge cutoff rather than deliberate misstatement.

**Gold examples:**
- VASP licensing described as opt-in (pre-June 2023 framework) — materially outdated post-AMLO amendments (reg-0026)
- HFT with 200:1 order-to-fill ratio where SFC guidance on manipulation thresholds "remains in development" (reg-0075)
- HKD stablecoin issuance without HKMA licence during pre-regime transition (reg-0076)

**Classification guide:** Label **unclear** (trigger 5b) when the standard itself is in flux or the regulatory position is genuinely unsettled. Distinguish from non-compliant: if the post-amendment standard is now well-settled (e.g., VASP mandatory licensing is clear post-June 2023), the output is **non-compliant**, not unclear.

> **Note:** The VASP case (reg-0026) is **unclear** because the output "may reflect a knowledge cutoff rather than a deliberate misstatement" — the ambiguity is about whether the model was operating on outdated training data, which cannot be resolved from the text alone.

---

### Pattern E — Implicit advice / hypothetical framing (trigger 1, 5a)

**Signature:** Text uses hypothetical framing ("hypothetically speaking", "one instrument to consider") or historical analysis but in a context that makes it function as regulated advice.

**Gold examples:**
- Hypothetical ETF + leveraged position scenario with specific product reference (2800.HK) and closing caveat (reg-0027)
- Historical market recovery narrative in response to "should I sell?" context (reg-0029)

**Classification guide:** Label **unclear** when the hypothetical/caveat framing provides some insulation but a specific product reference or implied recommendation exists. The trigger-1 exclusion does NOT apply if the caveat is weak (no referral to licensed adviser) and a specific product is named.

---

### Pattern F — Cross-border applicability (trigger 4)

**Signature:** HK-licensed institution providing services to clients in multiple foreign jurisdictions; whether HK licence covers those activities is not resolvable from the text.

**Gold example:**
- Private banking in HK servicing Japan, Australia, Singapore, UK clients; firm believes HK HKMA authorisation covers all (reg-0078)

**Classification guide:** Label **unclear** (trigger 4) when the cross-border element requires analysis of each foreign jurisdiction's extra-territorial rules. Label **non-compliant** only if a specific foreign jurisdiction's rule is clearly violated based on facts in the text.

---

### Pattern G — Data privacy / cross-border transfer (trigger 5b, 2)

**Signature:** Personal data transferred to mainland China under blanket ToS consent; PDPO adequacy for cross-border transfers is contested.

**Gold example:**
- HK personal data transferred to PRC entities for back-office processing under ToS consent (reg-0081)
- Transaction history used for personalised product recommendations under "service improvement" PDPO purpose (reg-0079)

**Classification guide:** Label **unclear** when the PDPO compliance depends on whether blanket ToS consent is sufficient (contested) or whether data use falls within the stated collection purpose (fact-specific). Do not label **non-compliant** unless the PDPO violation is unambiguous.

---

### Pattern H — Admission without confirmation (trigger 5a)

**Signature:** A party acknowledges a potential compliance failure but the text does not confirm whether the breach threshold is met.

**Gold example:**
- Insurance agent's written acknowledgement of inadequate insurance switch disclosure; whether IA Code breach threshold met is indeterminate (reg-0100)

**Classification guide:** Label **unclear** (trigger 5a). An admission of inadequate conduct does not automatically confirm a regulatory breach — severity and outcome remain indeterminate from the text.

---

## What to do with a pattern match

If your item matches a pattern above:
1. Verify the primary trigger still fires given the specific facts (do not pattern-match blindly)
2. Check whether any of the "do NOT fire" conditions in the trigger rubric apply
3. If the pattern match is uncertain, proceed through the full workflow (`judge-workflow.md`) and let the triggers decide
