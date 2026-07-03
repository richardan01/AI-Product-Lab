# RegEval — Demo Run Sheet (v2: the integrity-catch story)

**Rewritten 2026-06-28** after the forward discovery pass. The prior run sheet (3-class,
κ=0.677/0.820, gold-correction story) is **retired** — it rested on a held-out set that turned out
to be a duplicate of the tuning set. The new story is stronger: *how I caught my own eval lying to
me, and what I did about it.* That's a rigor-and-honesty demo, which is the signal a rigorous
technical evaluator actually wants.

> ✅ **SCRIPT RE-GATED 2026-06-29.** This v2 script cleared **Riddler** (Conditional → 3 conditions
> applied) and **Vicki Vale** (SKIM → READ after 3 fixes applied) — fresh markers written, superseding
> the void 06-26 markers. **Still pending:** the *recorded video* is a separate public artifact and
> must clear Riddler + Vicki Vale again (AV-delivery spot-check) before it posts.

**Through-line:** "Most eval demos show you their best number. I'm going to show you how I found my
eval was broken, and the discipline that caught it." Every beat serves that line.

**Working directory for all commands:** `Evals/regeval/`

---

## Pre-flight — run before hitting record

```bash
python3 --version                                   # 1. python present
python3 -c "import json; print('ok')"               # 2. stdlib only — no API key, no deps
ls scaffolds/current.md inputs/gold.jsonl           # 3a. champion scaffold + in-sample gold present
                                                    #     (gold.jsonl ships in the public repo; 100 items, pre-split)
ls inputs/heldout_v2.jsonl                          # 3b. genuine held-out present (local working file —
                                                    #     not shipped; required for the held-out beats below)
python3 score.py --slug binary-v1 \
  --pred experiments/.preds/2026-06-28-binary-v1-holdout.jsonl \
  --gold inputs/heldout_v2.jsonl --mode holdout --binary   # 4. dry-run the headline number
```

Beat 4 must print `HOLDOUT-PASS kappa=1.000`. If it doesn't, stop — do not record.

---

## The 5-minute demo (~1 min per beat)

### Cold open (~20 s — before the first command)

**Say:** "When an LLM judge labels regulatory traces, the only number that matters is how often it
agrees with a trained human reviewer — Cohen's κ, where 1.0 is perfect and 0 is chance. Most demos
stop at 'here's my κ.' I'm going to show you something more useful: how this harness caught its own
κ being built on a broken foundation — and how I fixed it. Two integrity defects, one decision, one
clean result."

### Beat 1 — The integrity catch (~60 s — lead with this; it's the hook)

```bash
python3 -c "
import json
dev={json.loads(l)['id'] for l in open('inputs/gold.jsonl') if l.strip()}
test={json.loads(l)['id'] for l in open('inputs/gold_expansion.jsonl') if l.strip()}
ov=dev&test
print(f'tuning set: {len(dev)} items')
print(f'\"held-out\" set: {len(test)} items')
print(f'OVERLAP: {len(ov)}/{len(test)} — the held-out was {100*len(ov)//len(test)}% inside the tuning set')
"
```

**What the viewer sees:** `OVERLAP: 70/70 — the held-out was 100% inside the tuning set`

**Say:** "Here's the defect I'd been shipping. My 'held-out validation set' — the thing that's
supposed to prove the judge generalises — was a *byte-for-byte subset of my training set*. Every
out-of-sample number I'd reported was actually in-sample. I found this by running a forward error
analysis and noticing the tuning and held-out confusion matrices were identical — which is
impossible unless they're the same data. The lesson is now a hard check: a held-out set must be
proven disjoint, by id and text, before any κ is cited."

### Beat 2 — The class that wasn't real (~60 s)

```bash
# the IAA result from the discovery pass (open the doc; this is a reading beat)
sed -n '/Integrity finding 2/,/queued/p' discovery-pass-2026-06-28.md
```

**What the viewer sees:** the IAA table — compliant 13/13, non-compliant 13/13, **unclear 2/18**,
overall κ=0.48.

**Say:** "Second defect. My judge has three labels — compliant, non-compliant, and *unclear*. When I
ran an inter-annotator check with the unclear class included — which my original IAA had skipped — a
second blind annotator (a model, same limitation as my first IAA; a human re-run is queued) agreed on
the binary classes perfectly, but on *unclear* agreed on only 2 of 18. Two annotators can't agree
what 'unclear' means. That wasn't a judge defect — it was an unreliable gold label. You can't align a
judge to a category annotators don't share."

### Beat 3 — The decision (~30 s — say it, no command)

**Say:** "So the decision wrote itself: drop the broken class. Collapse to a binary judge —
compliant versus non-compliant — both of which have perfect inter-annotator agreement. Quarantine
the unclear items for human re-adjudication. And build a *genuine* held-out set: 36 brand-new
scenarios across 20 regulatory regimes the judge had never been tuned on — anti-money-laundering,
margin, virtual assets, short-selling, market manipulation, and more — generated by dimension
sampling, not copied from anything."

### Beat 4 — The clean result, reproducible from artifacts (~75 s — centrepiece)

```bash
# in-sample (binary scorer drops the 18 quarantined-unclear automatically)
python3 score.py --slug binary-v1 \
  --pred experiments/.preds/2026-06-28-binary-v1-insample.jsonl \
  --gold inputs/gold.jsonl --mode holdout --binary

# genuine net-new held-out — the real generalization test
python3 score.py --slug binary-v1 \
  --pred experiments/.preds/2026-06-28-binary-v1-holdout.jsonl \
  --gold inputs/heldout_v2.jsonl --mode holdout --binary
```

**What the viewer sees:**
```
HOLDOUT slug=binary-v1 kappa=1.000 ... n=82 covered=82/82
HOLDOUT slug=binary-v1 kappa=1.000 ... n=36 covered=36/36
```

**Say:** "Two 1.000s — and yes, that should make you suspicious; I'll defuse it before I move on.
These are author-constructed items with unambiguous labels by design, so perfect agreement on
clear-cut cases is what you'd *expect* — this is not a production number, and I come back to that in
the close. What it *does* prove: binary judge, κ=1.000 in-sample on 82 items, and κ=1.000 on the
genuine held-out — 36 scenarios it had never seen, across regimes it was never tuned on. And this is
run by the *committed* scorer against the *committed* scaffold — `scaffolds/current.md` plus
`score.py --binary`. The in-sample number is reproducible from the committed gold snapshot
(`inputs/snapshots/2026-06-28_gold_pre-split.jsonl`); the held-out gold labels are a local working
file (predictions ship in `experiments/.preds/`, the labels stay local), so the held-out run
reproduces on my machine and on request, not from the public clone alone.
Notice the scorer also drops the 18 quarantined items automatically and would penalise any hedge —
there's no abstaining your way to a good score."

### Beat 5 — The honest caveat + the next gap (~45 s — close here, don't oversell)

```bash
# deliberately on the RETIRED 3-class set — the binary set has zero mismatches to code,
# so the demo of the TOOL runs on the very data that exposed the duplication
python3 error_analysis.py --pred experiments/.preds/2026-06-28-rubric-graded-v4-holdout.jsonl \
  --gold inputs/gold_expansion.jsonl --out /tmp/worksheet.md
```

**What the viewer sees:** `Mismatches: 15/70 across 4 confusion cells` — the semi-automated
open→axial coding worksheet generator listing the confusion structure.

**Say first (don't skip this):** "One note on what's on screen: I'm running this worksheet against
the *retired* 3-class set on purpose. The clean binary set has zero mismatches — nothing to code — so
to show you the *tool*, I point it at the very data that exposed the duplication. The mechanism is the
point here, not the number.

Two things I won't oversell. First — κ=1.000 is on author-constructed items with clear
labels. That means 'perfect on clear-cut cases,' not 'perfect in production.' The next gap is
deliberately borderline items and real production traffic — both scoped in the design docs. Second —
this is how I keep finding the next failure: a tool that pulls every disagreement and groups it for
me to *read and code by hand*. It removes the grunt work, not the judgement — because the whole point
of error analysis is building the intuition yourself. The honest version of this project isn't a high
number. It's a loop that catches itself."

---

## If probed — honesty flags (say these, don't hedge them)

- **"κ=1.000 looks too good."** "It is — on clean-construct items. Both gold sets have unambiguous
  labels by design, so 1.000 means the binary distinction is genuinely easy when the case is clear.
  It is *not* a production number. I have not yet tested borderline cases or real traffic — that's the
  named next gap, with a CD-monitoring design already written."
- **"Your second annotator is a model, not a human."** "Correct — and the direction is so large, 2
  of 18 on the unclear class, that I'd expect a human to land in the same place. Human re-adjudication
  is the queued next step; the protocol is already written."
- **"How do you know the held-out is really novel now?"** "It's generated by dimension sampling
  across 20 regulatory regimes absent from the tuning set, and I id+text-diff it against the tuning
  set — zero overlap. That diff is the check Beat 1 shows failing on the old set."
- **"Why did you collapse instead of fixing the unclear class?"** "Because the problem wasn't the
  judge — it was the label. You can re-tune a judge; you can't optimise against a category two
  experts don't share. Binary is the honest task. Abstention can come back later as a *calibrated
  confidence flag* measured separately, not as a gold class."

---

## What NOT to demo

- **The old 3-class replay / provenance reconciliation beats** — still real and worth a one-line
  mention ("the harness also reconciles every published κ against on-disk artifacts"), but they
  belong to the retired story; don't re-centre the demo on them.
- **The IAA annotation run live** — it needs a subagent pass; show the logged result, don't run it.

---

## After the recording

The recorded demo is a **public artifact** — it must clear both **Riddler + Vicki Vale gates**
before posting. The *script* gates are already cleared (re-gated 2026-06-29, see banner at top);
what remains is an **AV-delivery spot-check on the recording** (pacing / audio / legibility).
