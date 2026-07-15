# Pending eval re-runs

Each row was registered when a mapped source file changed. A row is cleared only when a fresh eval run lands in `Evals/<suite>/results/` with date ≥ the source file's last edit date.

`/peer-review` and `/go-nogo` block any artifact citing a `pending`-status suite.

## Schema

- **Suite**: the affected suite
- **Source file changed**: the file that triggered registration
- **Source commit SHA**: `git rev-parse HEAD` at registration time
- **Registered date**: YYYY-MM-DD
- **Status**: `pending` | `cleared`
- **Cleared by run**: path to the result file that cleared it (filled when status flips to `cleared`)

## Ledger

| Suite | Source file changed | Source commit SHA | Registered date | Status | Cleared by run |
|---|---|---|---|---|---|
| onboarding | Evals/onboarding/04-no-residual-placeholders/grade.sh | 101a4e5e88fc28924b6ab3cd16b248c1fd71b2eb | 2026-06-07 | cleared | onboarding/results/2026-06-10_claude-fable-5.md |
| peer-review | .claude/skills/peer-review/SKILL.md | 14a45ec59af781ab41f53f36139476d4b853ed44 | 2026-06-11 | cleared | peer-review/results/2026-06-12_claude-sonnet-4-6_r2.md |

(append-only; no row deletion; status `pending` → `cleared` only)

<!-- 2026-06-22 eval-hardening batch -->
| onboarding | Workflows/interactive-onboarding.md (HEAD_OF_DEPT, Phase 7 content-exclusion, Phase 6 explicit-yes, Phase 8 deferred/privacy) + grade.sh + eval-03 criteria | 2026-06-22 | **cleared** (content 2026-06-23; temporal 02/07 run 2026-07-05 on eval-runner/eval-grader pair) | onboarding/results/2026-06-23_claude-opus-4-8.md (content 0 ❌, 7✅/2⚠) + onboarding/results/2026-07-05_claude-sonnet-5.md (temporal 02/07: 0 ❌ — 02: 14✅/1⚠; 07: 16✅ scorable, C6 exercised; C7 unexercised — coverage gap logged) — 3 fixtures, author/grader separation held; see run-log 2026-07-05 |
| peer-review | .claude/skills/peer-review/SKILL.md (per-story AC check; narrowed degraded-mode cap) | 2026-06-22 | **cleared** (2026-06-23 r2, post-fix) | peer-review/results/2026-06-23_claude-opus-4-8_r2.md — CITABLE after adding Pass-3 cross-cutting risk checks (cross-section consistency + rollback-plan); F3/F5 now caught, no clean-control regression |
| prd-readiness | new suite added — needs a runner/grader pass for CITABLE | 2026-06-22 | **cleared** (2026-06-23 r2, post-fix) | prd-readiness/results/2026-06-23_claude-opus-4-8_r2.md — CITABLE after D1–D4 skill remediation (r1 found defects; r2 clean: 01/02/03/04 all ✅) |
| gate-group | Agents/Gotham/Computer/vicki-vale.md | ba4ea795d21dc26928029e75c17a7002c90b3bd6 | 2026-07-06 | **cleared** | gate-group/results/2026-07-06_post-remediation.md (r2, 7/8, C2+C4 clean) |
| gate-group | Agents/Gotham/_shared/gate-response.schema.md | 7d016e9ac4bb6219bdfd33ff1e42c76d84b481d5 | 2026-07-06 | **cleared** | gate-group/results/2026-07-06_post-remediation.md (r2, 7/8, C2+C4 clean) |
| gate-group | Agents/Gotham/Computer/henri-ducard.md | 7d016e9ac4bb6219bdfd33ff1e42c76d84b481d5 | 2026-07-06 | **cleared** | gate-group/results/2026-07-06_post-remediation.md (r2, 7/8, C2+C4 clean) — C7 residual: Ducard prose-preamble before JSON not yet fixed, tracked as follow-up in failure-log.md |
| go-nogo | .claude/skills/go-nogo/SKILL.md | de4a9d4dd2df103a8622a56312ca34c177db510e | 2026-07-14 | **cleared** | go-nogo/results/2026-07-14_claude-sonnet-5.md (first-ever run, 18/18, CITABLE PASS) |
| peer-review | .claude/skills/peer-review/SKILL.md | de4a9d4dd2df103a8622a56312ca34c177db510e | 2026-07-14 | **cleared** | peer-review/results/2026-07-14_claude-sonnet-5.md (fresh run landed; suite verdict is NOT CITABLE — clearing means "not stale," not "passing." See run-log.md and failure-log.md for the 3 open ❌ findings.) |
| peer-review | .claude/skills/peer-review/SKILL.md | f8d303f1bde0069c03383041537f6e22a1cb4b8b | 2026-07-14 | **cleared** | peer-review/results/2026-07-14_claude-sonnet-5_r2.md (r2 post-fix verification at commit e206533; regression closed — clean control 0/3→3/3, rollback hallucination eliminated) |
| peer-review | _Registry/reviewer-verdict-schema.md | de4a9d4dd2df103a8622a56312ca34c177db510e | 2026-07-14 | **cleared** | peer-review/results/2026-07-14_claude-opus-4-8.md (local — results/ gitignored; opus re-run after the `Reviewed-by` verdict-schema field added in the batch-2 gate-hardening PR. 11/11 ✅ / 0 ❌ → CITABLE. Schema change is verdict-file metadata only; `/peer-review` review logic unaffected, confirmed by the clean grid.) |
