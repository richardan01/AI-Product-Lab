#!/usr/bin/env python3
"""
RegEval queue reader — the loop's "what runs next".

Single source of truth = research-goal.md's candidate queue table.
A candidate is RUNNABLE when ALL hold:
  - its row status contains 'pending'
  - scaffolds/candidates/<slug>.md exists
  - <slug> has no row yet in results.tsv  (results.tsv IS the done-state)

Usage:
  python3 queue.py next   -> prints "<slug>\t<parent>" for the next runnable, or nothing
  python3 queue.py list   -> prints all runnable "<slug>\t<parent>", one per line
  python3 queue.py why     -> prints every queue row with a runnable/skip reason (debug)
"""

import re
import sys
from pathlib import Path

REGEVAL_DIR = Path(__file__).parent
GOAL   = REGEVAL_DIR / "research-goal.md"
CANDS  = REGEVAL_DIR / "scaffolds" / "candidates"
TSV    = REGEVAL_DIR / "results.tsv"

def done_slugs():
    if not TSV.exists():
        return set()
    out = set()
    for line in TSV.read_text().splitlines()[1:]:
        cols = line.split("\t")
        if len(cols) >= 3:
            out.add(cols[2].strip())
    return out

def parse_queue():
    """Return list of (slug, status, parent_guess) from the Candidate queue table."""
    text = GOAL.read_text()
    # isolate the section between '## Candidate queue' and the next '## '
    m = re.search(r"##\s*Candidate queue.*?\n(.*?)(?:\n##\s|\Z)", text, re.DOTALL)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        if not line.strip().startswith("|"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        # header / separator rows
        if len(cols) < 3 or cols[0] in ("#", "") or set(cols[0]) <= set("-: "):
            continue
        # slug is the first backticked token in the row
        sm = re.search(r"`([a-z0-9][a-z0-9._-]*)`", line)
        if not sm:
            continue
        slug = sm.group(1)
        # status column is the one containing pending/queued/done
        status = next((c.lower() for c in cols if re.search(r"pending|queued|done", c.lower())), "")
        rows.append((slug, status))
    return rows

def runnable():
    done = done_slugs()
    out = []
    for slug, status in parse_queue():
        if "pending" not in status:
            continue
        if not (CANDS / f"{slug}.md").exists():
            continue
        if slug in done:
            continue
        out.append((slug, "current"))
    return out

def reasons():
    done = done_slugs()
    lines = []
    for slug, status in parse_queue():
        if "pending" not in status:
            r = f"skip (status='{status or 'none'}')"
        elif not (CANDS / f"{slug}.md").exists():
            r = "skip (no scaffold file — author it)"
        elif slug in done:
            r = "skip (already has a results.tsv row)"
        else:
            r = "RUNNABLE"
        lines.append(f"{slug}\t{r}")
    return lines

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "next"
    if cmd == "next":
        r = runnable()
        if r:
            print(f"{r[0][0]}\t{r[0][1]}")
    elif cmd == "list":
        for slug, parent in runnable():
            print(f"{slug}\t{parent}")
    elif cmd == "why":
        for line in reasons():
            print(line)
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        raise SystemExit(2)

if __name__ == "__main__":
    main()
