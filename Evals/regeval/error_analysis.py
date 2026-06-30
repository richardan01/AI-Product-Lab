#!/usr/bin/env python3
"""
RegEval error-analysis helper — semi-automated open -> axial coding.

Philosophy (Shreya/Husain): the JUDGMENT (reading a trace, writing the open code) stays human.
This tool only removes the TOIL: it pulls every judge-vs-gold mismatch, groups them by confusion
cell, and emits a markdown WORKSHEET with the full scenario text + a blank `open_code:` field for
you to fill. It then drafts axial clusters BY CONFUSION CELL as a starting point you must review,
refine, and rename yourself. It never invents failure-mode names for you.

Usage:
  python3 error_analysis.py --pred <preds.jsonl> --gold <gold.jsonl> [--binary] \
      [--out experiments/discovery/<date>-worksheet.md]

Output: a worksheet file (one section per confusion cell; one card per mismatch with blank
open_code) + a draft axial summary table. You fill open_code, then cluster by hand.
"""
import argparse, json, re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REGEVAL_DIR = Path(__file__).parent

def load_jsonl(p):
    return [json.loads(l) for l in open(p) if l.strip()]

def norm(x):
    x = (x or "").strip().lower()
    return x if x in ("compliant", "non-compliant", "unclear") else "unclear"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", required=True)
    ap.add_argument("--gold", required=True)
    ap.add_argument("--binary", action="store_true",
                    help="drop non-binary gold; treat 'unclear' pred as a forced error")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    BINARY = ("compliant", "non-compliant")
    gold_items = load_jsonl(args.gold)
    if args.binary:
        gold_items = [g for g in gold_items if g["gold_label"] in BINARY]
    gold = {g["id"]: g for g in gold_items}
    pred = {p["id"]: norm(p.get("pred")) for p in load_jsonl(args.pred)}

    if args.binary:
        for i, g in gold.items():
            if pred.get(i) == "unclear":
                pred[i] = "non-compliant" if g["gold_label"] == "compliant" else "compliant"

    ids = [i for i in gold if i in pred]
    mism = [(i, gold[i]["gold_label"], pred[i]) for i in ids if gold[i]["gold_label"] != pred[i]]
    cells = defaultdict(list)
    for i, g, p in mism:
        cells[(g, p)].append(i)

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = Path(args.out) if args.out else REGEVAL_DIR / "experiments" / "discovery" / f"{date}-worksheet.md"
    out.parent.mkdir(parents=True, exist_ok=True)

    L = []
    L.append(f"# Error-analysis worksheet — {date}")
    L.append("")
    L.append(f"**Pred:** `{args.pred}`  ·  **Gold:** `{args.gold}`  ·  "
             f"**Mode:** {'binary' if args.binary else '3-class'}")
    L.append(f"**Scored:** {len(ids)}  ·  **Mismatches:** {len(mism)}  "
             f"({len(mism)/len(ids):.0%})" if ids else "")
    L.append("")
    L.append("> **How to use:** read each card, write a short `open_code:` (descriptive, "
             "let categories emerge — do NOT pick from a fixed list). When done, cluster the open "
             "codes by hand into the axial table at the bottom. The confusion-cell grouping below "
             "is a DRAFT starting point, not the answer.")
    L.append("")
    L.append("## Draft axial scaffold (confusion cells — rename/merge these yourself)")
    L.append("")
    L.append("| gold → pred | count | your axial cluster name |")
    L.append("|---|---|---|")
    for (g, p), lst in sorted(cells.items(), key=lambda kv: -len(kv[1])):
        L.append(f"| {g} → {p} | {len(lst)} | _(fill in)_ |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Open-coding cards (fill `open_code:` for each)")
    for (g, p), lst in sorted(cells.items(), key=lambda kv: -len(kv[1])):
        L.append("")
        L.append(f"### Confusion cell: gold=`{g}` → pred=`{p}`  ({len(lst)} items)")
        for i in lst:
            it = gold[i]
            txt = re.sub(r"\s+", " ", it.get("input", "")).strip()
            L.append("")
            L.append(f"- **{i}**")
            L.append(f"  - input: {txt}")
            if it.get("gold_rationale"):
                L.append(f"  - gold_rationale: {it['gold_rationale']}")
            L.append(f"  - `open_code:` ")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Axial summary (write after coding — promote stable clusters to failure-taxonomy.md)")
    L.append("")
    L.append("| cluster | open codes rolled up | count | hypothesis | → FM-id |")
    L.append("|---|---|---|---|---|")
    L.append("| _(fill in)_ | | | | |")
    out.write_text("\n".join(L) + "\n")

    print(f"Wrote {out}")
    print(f"Mismatches: {len(mism)}/{len(ids)} across {len(cells)} confusion cells:")
    for (g, p), lst in sorted(cells.items(), key=lambda kv: -len(kv[1])):
        print(f"  {g} -> {p}: {len(lst)}")

if __name__ == "__main__":
    main()
