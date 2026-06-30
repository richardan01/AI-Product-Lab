# 04 — Dedup + canonicality

**Criterion:** The routine updated existing memory files rather than creating near-duplicates, and wrote nothing that contradicts `Knowledge/People/` or `Knowledge/Reference/` (the workspace source of truth).

**Why:** Duplicates fragment memory and split retrieval; contradicting the canon corrupts it.

**Pass:** New facts about an existing topic landed as updates to the existing file. On any conflict with a `Knowledge/People|Reference` page, memory matches the canon (or explicitly flags the divergence).

**Fail:** A second file covering a topic an existing memory already owns; or a memory claim that silently contradicts a canonical profile/reference.

**How to check:** Scan for topic overlap across memory files. Cross-check stakeholder and company claims against `Knowledge/`.
