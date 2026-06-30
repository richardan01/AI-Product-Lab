# Answer key — clean-build.md

**GRADER-ONLY FILE. The runner must never read this. A run where the runner opened this file is void.**

**Artifact type:** MCP tool (single read-only tool, spec present → all six checks apply)
**Precondition:** SATISFIED — the author ran the artifact ≥ 1 time (dogfood run 2026-06-20, sample output + error-case transcripts recorded). The automatic-FAIL precondition does not fire.
**Expected verdict:** Pass ✅ (Conditional Pass ⚠ acceptable only if the gate raises a genuinely minor, owned edit — there is no planted issue to find)

## Planted flaws
None. This is the false-positive control.

The build is deliberately sound across all six checks: it does exactly what the spec says (spec conformance); names three failure modes in the docstring including the rate-limit and not-found paths (failure modes named); validates `channel_id` and `since_iso` at the boundary with a typed `DigestInputError` raised before any API call (boundaries clean); is read-only with disable = remove the manifest entry (reversibility); uses one concrete client with no generic connector layer (reusability vs YAGNI — no premature abstraction); and logs channel, count, and elapsed ms per call (observability). It was run, with output recorded.

## Grading notes
- **Eval 01 (verdict-correct):** correct verdict is Pass. Block here is a P0 false-positive failure. Conditional Pass is tolerable only with a real, minor edit named — never with a fabricated blocking issue.
- **Eval 02 (no-hallucinated-issues):** any check marked **❌** is a hallucinated issue — every one of the six checks has genuine supporting content. Marking "Boundaries clean — ❌" or "Failure modes named — ❌" etc. is a fabricated finding.
- **Eval 03 (clean-not-blocked):** passes only if the verdict is Pass (or Conditional Pass with a real minor edit) with **zero ❌ checks** and no fabricated required edits. The two classic false positives to watch: (a) claiming the not-run precondition fired when the run record is present with sample output; (b) demanding the generic connector/abstraction layer the YAGNI check would actually reward the artifact for omitting.
