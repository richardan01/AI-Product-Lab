# Research synthesis — New-merchant support ticket study

**Author:** PM, Payments Activation
**Method:** Thematic coding of new-merchant support tickets (first 30 days after signup), April–May 2026. Analyzed 412 tickets across onboarding, verification, and payouts categories.
**Status:** Draft for stakeholder share-out

## Summary

New-merchant support load is dominated by verification-status confusion, not by product defects. Most tickets are answerable by better in-product state communication rather than support headcount.

## Themes

### Theme 1 — Verification status is a black box

The single largest cluster. Merchants do not know whether their verification is progressing, stalled, or rejected.

- 38% of all 380 tickets in the study window mention verification status (145 tickets)
- Representative tickets: #20431 ("submitted documents 6 days ago, no update"), #20518, #21002
- Merchants who received a proactive status email filed 60% fewer follow-up tickets (comparison of the two April batches)

### Theme 2 — Payout timing expectations are set wrong at signup

Merchants expect payouts on the card-settlement schedule, but first payouts are gated on verification, and nothing at signup says so. The gap between expectation and the first payout experience drives the angriest ticket cluster and most of the threatened-churn language.

### Theme 3 — Document re-submission loops

Rejected documents produce a re-submission request that doesn't say *why* the document failed.

- 22% of verification tickets are second or third submissions of the same document type (32 of 145)
- Representative tickets: #20677 ("third time uploading the same utility bill"), #20691
- 78% of merchants abandon after a second rejection

## Recommendations

1. Ship a verification-status tracker in the dashboard (states: received / in review / action needed / approved) — Owner: Activation squad, target Q3. Expected impact: removes the Theme 1 cluster's top driver, ~145 tickets/quarter.
2. Add payout-timing disclosure to the signup flow and the first payment-link screen — Owner: Onboarding squad, target Q3.
3. Rejection reasons should be improved.

[TODO: insert ticket-volume chart by week]

## Open questions

1. Does the proactive status email effect (60% fewer follow-ups) replicate in a controlled test? — Owner: PM, design experiment by 2026-06-25
2. What share of Theme 2 tickets convert to churn within 60 days? — Owner: Data science, due 2026-07-01
