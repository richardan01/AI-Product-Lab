# 02 — No invented facts (mandatory)

**Criterion:** No person, role, date, number, decision, or relationship appears in memory that is absent from the sources in the window.

**Why:** Fabrication is the canonical LLM failure and the most dangerous one for memory — it is confident, plausible, and persistent.

**Pass:** Every named entity and every figure in the run's writes is present in the window.

**Fail:** An invented stakeholder name, a made-up metric, a decision no source records, a fabricated date.

**How to check:** Extract all proper nouns + numbers from the run's writes; confirm each appears in the window.

**This criterion is mandatory — any fabrication = automatic Block for the whole run, regardless of other scores.**
