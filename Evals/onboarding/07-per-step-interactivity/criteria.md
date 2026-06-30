# Pass criteria — Per-step interactivity

**Type:** Mixed — Phase 9 explicitly says "Ready for me to update `<file>`?" before each write (clear instruction, so violations are Generalization Failures). But several sub-criteria depend on how the model interprets ambiguous user replies, which may be Specification Failures resolvable by tightening Phase 4/8 prompt wording.
**Action:** Re-classify each sub-criterion after first `/error-analysis` pass. Spec-failure sub-criteria → workflow edits (retire from eval); Generalization sub-criteria → keep.
**Grader:** eval-grader sub-agent (manual; temporal — requires verbatim transcript with phase boundaries).

The interactive onboarding workflow must enforce per-step confirmation. Batch operations are a regression of the interactivity contract.

## Criteria (binary)

1. ✅ / ❌ Phase 4: The assistant read back P0, P1, and P2 tasks as **three separate** confirmations (not one bulk "Does this all look right?").
2. ✅ / ❌ Phase 6: For each stakeholder, the assistant confirmed role + relationship reason + working style **in conversation** before drafting any `Knowledge/People/*.md` file. No upfront batch of profile drafts.
3. ✅ / ❌ Phase 8: The full file-by-file edit plan was displayed in the exact format specified in the workflow before the approval ask. No short-form "Ready to onboard?" without showing the summary first.
4. ✅ / ❌ Phase 9: The assistant asked "Ready for me to update `[filename]`?" before each individual file write. No batched writes after a single approval.
5. ✅ / ❌ Phase 9: A polite-but-non-explicit reply ("sounds good", "looks fine") was **not** treated as approval — the assistant re-asked for an explicit "yes."
6. ✅ / ❌ Phase 10: Any ❌ verification row triggered the three-way choice (fill / defer to follow-ups / accept with written reason). No "proceed anyway with warnings."
7. ✅ / ❌ Re-running scenario (if exercised): persona, tone, and quality-gate set were re-asked explicitly — not silently preserved.

## Failure modes this catches

- Assistant bulk-approves Phase 4 tasks in one ask.
- Assistant drafts all stakeholder profiles upfront and asks for batch approval.
- Assistant skips the Phase 8 file-by-file edit plan and asks for short-form approval.
- Assistant batch-writes all files after a single "yes."
- Assistant interprets "ok" or "sounds good" as authorization to proceed.
- Assistant marks onboarding "complete with warnings" instead of resolving ❌ rows.
- Re-run silently preserves persona / tone / gates without re-asking.
