#!/usr/bin/env python3
"""
RegEval provenance traces (REV-008).

Builds an auditable provenance record for every judge verdict by joining
three on-disk artifacts that already exist in the suite:

  1. an experiment file's `## Raw outputs` table   (the judge verdicts)
  2. the gold snapshot for that run                 (gold label + rationale)
  3. the scaffold file under test                   (content-hashed for reproducibility)

The output answers the Day-60 reproducibility question — "the variant is
reproducible from the log" — at the granularity of a single verdict:
  given a verdict, what produced it, against what gold, under which scaffold.

This module does NOT call the judge. It reconstructs traces from artifacts,
so it runs with no API key. (None is available in the build env.)

Usage
-----
  # Build the full trace sidecar (machine-readable JSONL) for an experiment:
  python3 provenance.py build experiments/2026-06-10-01-fable-judge-v1.md \
      --gold-snapshot inputs/snapshots/2026-06-04.jsonl

  # Print a human-readable trace card for one item:
  python3 provenance.py card experiments/2026-06-10-01-fable-judge-v1.md reg-0088 \
      --gold-snapshot inputs/snapshots/2026-06-04.jsonl

  # Show only the mismatches (the audit short-list):
  python3 provenance.py mismatches experiments/2026-06-10-01-fable-judge-v1.md \
      --gold-snapshot inputs/snapshots/2026-06-04.jsonl

Writes (build): traces/<experiment-stem>.jsonl  — one trace record per item.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REGEVAL_DIR = Path(__file__).parent
TRACES_DIR = REGEVAL_DIR / "traces"
SCAFFOLDS = REGEVAL_DIR / "scaffolds"

# Trigger vocabulary used by rubric-graded-v4 / judge-workflow.md.
# Used to attribute *which* abstention trigger a rationale implies. Best-effort
# only: the live judge does not emit a structured step path, so this field is
# parsed from the rationale text and marked low-confidence.
TRIGGER_PATTERNS = {
    "trigger-1": [r"\btrigger[- ]?1\b", r"no identifiable obligation", r"no regulatory claim", r"educational"],
    "trigger-2": [r"\btrigger[- ]?2\b", r"missing (applicability )?context", r"\bTBD\b", r"not confirmed"],
    "trigger-3": [r"\btrigger[- ]?3\b", r"conflicting signals?"],
    "trigger-4": [r"\btrigger[- ]?4\b", r"out[- ]of[- ]scope", r"jurisdiction", r"foreign regime", r"cross[- ]border"],
    "trigger-5a": [r"\btrigger[- ]?5a\b", r"unverifiable", r"cannot be confirmed", r"not stated as (done|complete)"],
    "trigger-5b": [r"\btrigger[- ]?5b\b", r"not yet enacted", r"proposed", r"standard.*in flux", r"in question"],
}


def sha8(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def resolve(p: str) -> Path:
    """Resolve a path relative to the regeval dir if it isn't absolute."""
    path = Path(p)
    return path if path.is_absolute() else (REGEVAL_DIR / path)


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------
def parse_raw_outputs(experiment_path: Path):
    """Extract the `## Raw outputs` per-item table.

    Returns list of dicts: {id, gold, judge, note}. `note` is whatever sits in
    the 4th column (a tick, or a free-text rationale fragment in some files).
    Keys off the canonical header `| id | gold | judge | match |`.
    """
    text = experiment_path.read_text()
    rows = []
    for line in text.splitlines():
        m = re.match(r"\|\s*(reg-\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|", line)
        if m:
            rows.append(
                {
                    "id": m.group(1),
                    "gold": m.group(2).strip(),
                    "judge": m.group(3).strip(),
                    "note": m.group(4).strip(),
                }
            )
    return rows


def parse_experiment_header(experiment_path: Path):
    """Pull verdict / kappa / scaffold slug from the experiment file header."""
    text = experiment_path.read_text()
    header = {}
    h1 = re.search(r"#\s*(?:RegEval )?[Ee]xperiment\s+([0-9-]+)\s*—\s*(\S+)", text)
    if h1:
        header["experiment_id"] = h1.group(1)
        header["scaffold_slug"] = h1.group(2)
    v = re.search(r"\*\*Verdict:\*\*\s*(.+)", text)
    if v:
        header["verdict"] = v.group(1).strip()
    k = re.search(r"\*\*κ:\*\*\s*([0-9.]+)", text)
    if k:
        header["kappa"] = float(k.group(1))
    return header


def load_gold_snapshot(snapshot_path: Path):
    """Return {id: {gold_label, gold_rationale, input}} keyed by item id."""
    gold = {}
    with open(snapshot_path) as f:
        for line in f:
            line = line.strip()
            if line:
                d = json.loads(line)
                gold[d["id"]] = d
    return gold


def attribute_trigger(judge_label: str, rationale: str):
    """Best-effort attribution of which abstention trigger a verdict implies.

    Only meaningful for judge_label == 'unclear'. Returns (trigger, confidence).
    confidence is always 'low' — this is parsed from prose, not a structured
    step path. Marked so the demo doesn't overclaim.
    """
    if judge_label != "unclear":
        return None, None
    hay = rationale.lower()
    for trig, pats in TRIGGER_PATTERNS.items():
        for pat in pats:
            if re.search(pat, hay):
                return trig, "low"
    return "unattributed", "low"


# ---------------------------------------------------------------------------
# Trace construction
# ---------------------------------------------------------------------------
def build_traces(experiment_path: Path, snapshot_path: Path, scaffold_path: Path):
    rows = parse_raw_outputs(experiment_path)
    if not rows:
        raise SystemExit(
            f"No `## Raw outputs` table found in {experiment_path.name}. "
            "This experiment was an analytical re-score with no per-item table; "
            "point at an experiment file that logged per-item verdicts."
        )
    header = parse_experiment_header(experiment_path)
    gold = load_gold_snapshot(snapshot_path)
    scaffold_text = scaffold_path.read_text()
    scaffold_hash = sha8(scaffold_text)
    snapshot_hash = sha8(snapshot_path.read_text())

    # Integrity check: does the scaffold file passed in actually correspond to
    # the scaffold the run used? The experiment header names a slug; if the
    # hashed file's own slug line disagrees, the hash is NOT provenance for the
    # named run — flag it rather than imply a false match.
    run_slug = header.get("scaffold_slug")
    file_slug_m = re.search(r"\*\*Slug:\*\*\s*(\S+)", scaffold_text)
    file_slug = file_slug_m.group(1) if file_slug_m else None
    scaffold_verified = (run_slug is not None and file_slug == run_slug)

    built_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    traces = []
    for r in rows:
        g = gold.get(r["id"], {})
        judge_label = r["judge"]
        # In files that store a rationale in col 4, use it; else fall back to gold.
        rationale = r["note"] if not r["note"].startswith(("✓", "✗")) else ""
        trigger, trig_conf = attribute_trigger(judge_label, rationale or "")
        traces.append(
            {
                "trace_id": f"{header.get('experiment_id', experiment_path.stem)}::{r['id']}",
                "item_id": r["id"],
                # --- verdict ---
                "judge_label": judge_label,
                "judge_rationale": rationale,
                "gold_label": g.get("gold_label", r["gold"]),
                "gold_rationale": g.get("gold_rationale", ""),
                "agreement": judge_label == g.get("gold_label", r["gold"]),
                # --- best-effort decision attribution (Framing B, low-confidence) ---
                "abstention_trigger": trigger,
                "trigger_confidence": trig_conf,
                # --- reproducibility envelope (Framing C) ---
                "experiment_id": header.get("experiment_id"),
                "experiment_file": experiment_path.name,
                "scaffold_slug": header.get("scaffold_slug"),
                "scaffold_file": scaffold_path.name,
                "scaffold_sha8": scaffold_hash,
                "scaffold_hash_verified": scaffold_verified,
                "gold_snapshot_file": snapshot_path.name,
                "gold_snapshot_sha8": snapshot_hash,
                "verdict_of_run": header.get("verdict"),
                "kappa_of_run": header.get("kappa"),
                "input_excerpt": (g.get("input", "")[:160] + "…") if g.get("input") else "",
                "built_at": built_at,
                "built_by": "provenance.py (REV-008)",
                "reconstructed": True,  # not a live judge call; rebuilt from artifacts
            }
        )
    return traces, header


def render_card(t: dict) -> str:
    flag = "AGREE" if t["agreement"] else "MISMATCH"
    lines = [
        "┌─ provenance trace ─────────────────────────────────────────",
        f"│ trace_id   : {t['trace_id']}",
        f"│ verdict    : judge={t['judge_label']}  gold={t['gold_label']}  → {flag}",
    ]
    if t["abstention_trigger"]:
        lines.append(
            f"│ attributed : {t['abstention_trigger']} (confidence={t['trigger_confidence']}; parsed from rationale)"
        )
    lines += [
        "│",
        f"│ judge says : {t['judge_rationale'] or '(no rationale in source table)'}",
        f"│ gold says  : {t['gold_rationale'] or '(none)'}",
        "│",
        "│ reproducibility envelope",
        f"│   scaffold      : {t['scaffold_slug']}  ({t['scaffold_file']} @ {t['scaffold_sha8']})"
        + ("" if t["scaffold_hash_verified"] else "  ⚠ hash is of passed file, NOT verified against run slug"),
        f"│   gold snapshot : {t['gold_snapshot_file']} @ {t['gold_snapshot_sha8']}",
        f"│   run           : {t['experiment_id']}  verdict={t['verdict_of_run']}  κ={t['kappa_of_run']}",
        f"│   built         : {t['built_at']}  (reconstructed from artifacts, no live judge call)",
        "│",
        f"│ input excerpt : {t['input_excerpt']}",
        "└────────────────────────────────────────────────────────────",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="RegEval provenance traces (REV-008)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    for name in ("build", "card", "mismatches"):
        sp = sub.add_parser(name)
        sp.add_argument("experiment", help="path to an experiment .md file (relative to regeval/ ok)")
        if name == "card":
            sp.add_argument("item_id", help="e.g. reg-0088")
        sp.add_argument(
            "--gold-snapshot",
            required=True,
            help="path to the gold snapshot .jsonl used for this run",
        )
        sp.add_argument(
            "--scaffold",
            default="scaffolds/current.md",
            help="scaffold file under test (default: scaffolds/current.md)",
        )

    args = ap.parse_args()
    exp = resolve(args.experiment)
    snap = resolve(args.gold_snapshot)
    scaf = resolve(args.scaffold)
    for label, p in (("experiment", exp), ("gold-snapshot", snap), ("scaffold", scaf)):
        if not p.exists():
            raise SystemExit(f"{label} not found: {p}")

    traces, header = build_traces(exp, snap, scaf)

    if args.cmd == "build":
        TRACES_DIR.mkdir(exist_ok=True)
        out = TRACES_DIR / f"{exp.stem}.jsonl"
        with open(out, "w") as f:
            for t in traces:
                f.write(json.dumps(t) + "\n")
        n = len(traces)
        n_agree = sum(t["agreement"] for t in traces)
        print(f"Built {n} traces → traces/{out.name}")
        print(f"  agree={n_agree}  mismatch={n - n_agree}  (run κ={header.get('kappa')})")
        verified = traces[0]["scaffold_hash_verified"]
        vmark = "verified" if verified else "⚠ UNVERIFIED (passed file slug ≠ run slug)"
        print(f"  scaffold {header.get('scaffold_slug')} @ {traces[0]['scaffold_sha8']} [{vmark}]  "
              f"snapshot @ {traces[0]['gold_snapshot_sha8']}")

    elif args.cmd == "card":
        for t in traces:
            if t["item_id"] == args.item_id:
                print(render_card(t))
                return
        raise SystemExit(f"item {args.item_id} not in {exp.name}")

    elif args.cmd == "mismatches":
        mm = [t for t in traces if not t["agreement"]]
        print(f"{len(mm)} mismatches in {exp.name} (run κ={header.get('kappa')}):\n")
        for t in mm:
            trig = f"  [{t['abstention_trigger']}]" if t["abstention_trigger"] else ""
            print(f"  {t['item_id']}: judge={t['judge_label']:>14s}  gold={t['gold_label']:>14s}{trig}")


if __name__ == "__main__":
    main()
