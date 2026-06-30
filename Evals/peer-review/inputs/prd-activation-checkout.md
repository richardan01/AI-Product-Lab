# PRD — Express checkout for first-time merchants

**Author:** PM, Payments Activation
**Status:** Draft for engineering handoff
**Last updated:** 2026-06-01

## Executive summary

First-time merchants abandon checkout setup at high rates because the current flow requires bank verification, KYC, and storefront configuration before a single test transaction can run. Express checkout lets a new merchant accept a first live payment within 10 minutes of signup, deferring full verification until payout. We target GA by end of Q3 2026.

## Problem

Merchant activation data shows setup friction concentrated in the verification step:

- Median time from signup to first transaction: 4.2 days (cohort: May 2026 signups, n=1,840)
- 61% of merchants who stall at verification never return (same cohort)
- Top-3 support ticket driver for new merchants is "verification pending" status confusion

The opportunity: decouple *accepting* a payment from *receiving* a payout. Funds can be held until verification completes, which is the model used by the two competitors who lead our churn-loss interviews.

## Goals and success metrics

| Metric | Target |
|---|---|
| Time from signup to first transaction | < 30 minutes (median) |
| Checkout completion rate | improve significantly |
| Verification completion within 7 days of first transaction | ≥ 80% |

## User stories

**US-1: First payment without full verification**
As a new merchant, I want to accept a card payment immediately after signup, so that I can validate my store works before investing time in verification.

*Acceptance criteria:*
- Merchant can generate a payment link within 10 minutes of account creation
- Funds are held in a pending balance, clearly labeled, until KYC completes
- Holding period and reason are stated on the balance screen

**US-2: Deferred verification prompt**
As a new merchant with held funds, I want a clear path to complete verification, so that I can receive my payout.

*Acceptance criteria:*
- Verification prompt appears after first successful transaction with expected review time
- Merchant receives a reminder at 48h and 5 days if verification is incomplete
- Payout releases automatically within 1 business day of verification passing

**US-3: Risk review for held balances**
As a risk analyst, I want held balances above a threshold to enter manual review, so that we don't accumulate exposure from unverified merchants.

## Scope

**In scope:** card payments via payment links; single-currency accounts; held-balance ledger; verification reminder flow.

**Out of scope (V1):** POS terminals, multi-currency, marketplace sub-merchants, payout scheduling changes.

## Dependencies

- Risk engine threshold API — confirmed available (Risk team, 2026-05-20)
- Held-balance ledger changes — TBD
- Compliance sign-off on deferred KYC model — meeting scheduled 2026-06-12

## Timeline

| Milestone | Date |
|---|---|
| Design complete | 2026-07-04 |
| Beta (50 merchants) | 2026-09-01 |
| GA | 2026-10-30 |

## Open questions

1. What is the held-balance threshold that triggers manual risk review? — Owner: Risk team, due 2026-06-20
2. Do we cap the number of transactions an unverified merchant can accept?
