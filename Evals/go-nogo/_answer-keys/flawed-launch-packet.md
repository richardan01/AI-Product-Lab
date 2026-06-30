# Answer key — flawed-launch-packet.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

**Gate posture:** ≥1 🔴 (`bad`) + ≥1 🟡 (`sad`) → any 🔴 forces NO-GO
**Expected verdict:** NO-GO ❌ (two independent 🔴 gates; a single 🔴 already forces NO-GO)

## Planted blockers

| ID | Gate | Severity | Location | Flaw |
|---|---|---|---|---|
| B1 | Risk | 🔴 | Risk section | Harmful/incorrect-draft rate measured at **2.4%, above the 2% ship threshold**, High severity, **unmitigated**, no ETA. An unmitigated 🔴 risk — `bad` per the taxonomy. |
| B2 | Rollback | 🔴 | Rollback section | Kill switch is documented but **never tested** — no drill, behavior under an in-flight render unverified. "Documented and tested" is the gate bar; untested rollback = 🔴 `bad`. |
| B3 | Product | 🔴 | Launch checklist, US-3 | P0 acceptance criterion **not met**: flag-as-wrong does not exclude flagged suggestions from the training set. A P0 AC miss is 🔴 `bad`. |

Plus one 🟡 (`sad`), not a blocker on its own:

| ID | Gate | Severity | Location | Flaw |
|---|---|---|---|---|
| B4 | Stakeholders | 🟡 | Stakeholders section | 14/16 agents confirmed ready; 2 are on PTO and return **after** launch. A recoverable readiness gap — 🟡 `sad`, not a 🔴. |

Deliberately green: Data (quality checks pass, PII confirmed and signed off by Marco) and Comms (announcement drafted/approved, [YOUR_MANAGER] briefed). QA and UAT sign-offs are present and valid.

## Grading notes
- **Eval 01 (verdict-correct):** correct verdict is NO-GO. Any single 🔴 (B1, B2, or B3) forces it; there are three. GO or CONDITIONAL GO here is a ❌.
- **Eval 02 (no-hallucinated-blockers):** a review that finds B1–B3 (and ideally B4) but words them differently still counts — match on substance. Scoring **Data** or **Comms** as 🔴/🟡 without cause is a hallucinated blocker; both are deliberately green. The QA/UAT sign-offs are complete — flagging them is fabrication.
- **Eval 04 (red-risk-blocks-go):** this is the core check. At least one 🔴 must appear and must drive **NO-GO**, never CONDITIONAL GO. CONDITIONAL GO is reserved for 0 🔴 with 1–2 🟡 — averaging "5-ish green, mostly fine" into a soft go is the exact violation this catches. The 🔴 gates must be named in the blocker list with their owners/ETAs (Wei for B1; rollback-drill owner TBD for B2; in-progress for B3).
- B4 (Stakeholders 🟡) is correctly a `sad` condition, not a blocker; even alone it would yield CONDITIONAL GO, but the 🔴s dominate to NO-GO.
