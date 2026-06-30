# DEPRECATED — gold_expansion.jsonl is NOT a held-out set

**Found 2026-06-28.** `gold_expansion.jsonl` (70 items, reg-0031..reg-0100) is an **exact
id + text + label subset** of the tuning set `gold.jsonl` (reg-0001..reg-0100). Verified: 70/70
identical text and labels.

It was treated everywhere as a "never-tuned held-out validation set." It is not. Any κ measured on
it (e.g. the 2026-06-28 "held-out confirm" κ=0.661) is **in-sample** and must not be cited as
out-of-sample / anti-overfit evidence.

**Replacement:** `heldout_v2.jsonl` — 36 genuinely net-new binary items across 20 regulatory
regimes the tuning set never covered, built by dimension sampling. Use that as the test set.

Do not delete `gold_expansion.jsonl` without the maintainer's approval (per repo DO-NOT rules); it is kept
for lineage. This note marks it dead. See [[Evals/regeval/discovery-pass-2026-06-28]] (FM-11).
