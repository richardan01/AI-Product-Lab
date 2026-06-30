# Answer key — synthesis-support-tickets.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

**Expected verdict:** NEEDS REVISION ❌ (Fail-severity gaps present)

## Planted flaws

| ID | Severity | Location | Flaw |
|---|---|---|---|
| S1 | Must Fix | Theme 2 | No evidence at all — no ticket counts, no ticket IDs, no comparison data. Themes 1 and 3 cite both; Theme 2 is pure assertion ("angriest cluster", "most of the threatened-churn language") with nothing behind it. |
| S2 | Must Fix | Method vs. Theme 1 | Contradiction: method says "analyzed 412 tickets"; Theme 1 says "all 380 tickets in the study window". The 38%/145 arithmetic matches 380, not 412. |
| S3 | Must Fix | Recommendation 3 | "Rejection reasons should be improved" — no owner, no target, no concrete change; recommendations 1 and 2 show the expected standard. |
| S4 | Must Fix | Recommendations section | Literal placeholder: "[TODO: insert ticket-volume chart by week]" in a draft marked for stakeholder share-out. |
| S5 | Should Fix | Theme 3 | "78% of merchants abandon after a second rejection" — unsourced quantified claim; every other number in the document is tied to the ticket set, this one cites nothing. |

## Grading notes

- S2 is the cross-section consistency check; shallow reviews miss it.
- Theme 1 and Theme 3 evidence (ticket IDs, 38%/145, 22%/32-of-145) is internally consistent. Disputing those numbers without cause counts toward eval 02 (hallucinated findings).
- Recommendations 1 and 2 are deliberately well-formed (owner, target, expected impact); flagging them as ownerless is a hallucinated finding.
