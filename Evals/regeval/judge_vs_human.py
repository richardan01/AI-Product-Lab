#!/usr/bin/env python3
"""
RegEval human-vs-judge CLI (REV-009) — the κ-live session runner.

The gold panel's `gold_label` IS the human label. So "human vs judge" is exactly
what Cohen's κ already measures. This module's job is to make that comparison
*visible, item-by-item, and live* — and to self-audit by reconciling the κ it
recomputes against the κ the experiment logged.

Framing C (chosen): replay an already-logged judge run as if the human is labeling
it now. Stream items in order; after each, recompute Cohen's κ over everything seen
so far; end with a confusion matrix + per-class κ that MUST reconcile to the logged
κ. If it doesn't reconcile, that's a real finding surfaced on camera — not papered
over.

No judge calls, no API key. Reconstructs from on-disk artifacts. Pure stdlib.
Imports loaders from `provenance.py` (same dir) — does not re-implement them.

Subcommands
-----------
  replay <experiment> --gold-snapshot <snap> [--mismatches-only] [--no-anim]
      Stream the human-vs-judge comparison, κ recomputed live, ending with a
      confusion matrix, per-class κ, and a RECONCILES ✓/✗ self-audit vs logged κ.

  card <experiment> <item-id> --gold-snapshot <snap>
      Human-vs-judge adjudication card for one item. If the item appears in
      inputs/corrections-log.md, renders the adjudication OUTCOME (relabel /
      scaffold defect / noted) — "the human sat in judgment over the judge."

  summary <experiment> --gold-snapshot <snap>
      One-screen scoreboard: N, agree/mismatch, κ (recomputed + logged +
      reconcile), TPR/TNR/abstention, per-class κ, corrections-log entry count.

  adjudicate <experiment> <item-id> --gold-snapshot <snap>  (optional, Framing A)
      Blind moment: print item text + MASKED judge verdict, read ONE human label
      from stdin, then reveal judge + gold and report agree/disagree. Scriptable
      (`echo unclear | ... adjudicate ...`). Does NOT persist — prints a hint to
      log it to corrections-log.md instead.

Refusal guard
-------------
  A "selected mismatches" / prose table (e.g. rubric-graded-v4, N=13, col-4 prose)
  is NOT a full per-item stream. `replay`/`summary` detect it and REFUSE to quote a
  full-set κ — they print a partial-table banner instead of a meaningless number.
  (The embarrassment scenario is silently computing κ≈0 over 13 all-mismatch rows.)
"""

import argparse
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# Reuse the REV-008 loaders — do not re-implement.
from provenance import (
    parse_raw_outputs,
    parse_experiment_header,
    load_gold_snapshot,
    resolve,
    REGEVAL_DIR,
)

CORRECTIONS_LOG = REGEVAL_DIR / "inputs" / "corrections-log.md"
REVIEW_QUEUE = REGEVAL_DIR / "review-queue.md"

# metric.md maps compliant→accept, non-compliant→reject, unclear→abstain. κ is
# label-permutation-invariant, so we compute directly on the raw labels and still
# match the logged κ (verified: 0.6768 == logged 0.677 on fable-judge-v1).
ABSTAIN_LABELS = {"unclear", "abstain"}
ACCEPT_LABELS = {"compliant", "accept"}
REJECT_LABELS = {"non-compliant", "reject"}


# ---------------------------------------------------------------------------
# Metric (inline, from metric.md — the canonical formula, no deps)
# ---------------------------------------------------------------------------
def cohen_kappa(gold, pred):
    """Cohen's κ. Verbatim from metric.md (pure stdlib)."""
    classes = sorted(set(gold) | set(pred))
    n = len(gold)
    if n == 0:
        return float("nan")
    p_o = sum(g == p for g, p in zip(gold, pred)) / n
    g_marg = Counter(gold)
    p_marg = Counter(pred)
    p_e = sum((g_marg[c] / n) * (p_marg[c] / n) for c in classes)
    return (p_o - p_e) / (1 - p_e) if p_e < 1 else 1.0


def per_class_kappa(gold, pred, cls):
    """One-vs-rest κ for a single class (per metric.md diagnostics)."""
    g = [cls if x == cls else "_other" for x in gold]
    p = [cls if x == cls else "_other" for x in pred]
    return cohen_kappa(g, p)


def recall(gold, pred, cls):
    """Per-class recall (TPR for accept, TNR for reject)."""
    denom = sum(1 for g in gold if g == cls)
    if denom == 0:
        return float("nan")
    hit = sum(1 for g, p in zip(gold, pred) if g == cls and p == cls)
    return hit / denom


# ---------------------------------------------------------------------------
# Table classification — full stream vs selected-mismatches (refusal guard)
# ---------------------------------------------------------------------------
def classify_table(rows):
    """Return (kind, reason).

    kind == "full"    : col-4 is all ✓/✗ ticks → a real per-item judge stream.
    kind == "partial" : col-4 carries prose (mismatch type / rationale) → a
                        SELECTED-mismatches table; full-set κ is NOT computable.
    """
    if not rows:
        return "empty", "no per-item table found"
    all_ticks = all(r["note"].startswith(("✓", "✗")) for r in rows)
    if all_ticks:
        return "full", f"col-4 all ticks, N={len(rows)}"
    n_agree = sum(r["gold"] == r["judge"] for r in rows)
    return (
        "partial",
        f"col-4 carries prose (selected mismatches); N={len(rows)}, "
        f"{n_agree} agree — not a full per-item stream",
    )


# ---------------------------------------------------------------------------
# Corrections-log parser (small regex over the markdown table)
# ---------------------------------------------------------------------------
def load_corrections_log(path=CORRECTIONS_LOG):
    """Parse the corrections-log table + the scaffold-defect notes.

    Returns {item_id: {"date","judge","human","trigger","rationale","action","outcome"}}.
    `outcome` is a short tag: 'relabel', 'scaffold-defect', or 'noted'.
    Also scans the prose Notes section for item ids flagged as scaffold defects
    (e.g. reg-0088's trigger-5a false-abstain), which live in narrative, not the table.
    """
    out = {}
    if not path.exists():
        return out
    text = path.read_text()

    # Table rows: | Date | Item ID | Judge | Human | Trigger | Rationale | Action | δκ |
    for line in text.splitlines():
        m = re.match(
            r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(reg-\d+)\s*\|\s*([^|]+?)\s*\|"
            r"\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|",
            line,
        )
        if not m:
            continue
        action = m.group(7).strip()
        outcome = "relabel" if re.search(r"relabel", action, re.I) else "noted"
        out[m.group(2)] = {
            "date": m.group(1),
            "judge": m.group(3).strip(),
            "human": m.group(4).strip(),
            "trigger": m.group(5).strip(),
            "rationale": m.group(6).strip(),
            "action": action,
            "dk": m.group(8).strip(),
            "outcome": outcome,
        }

    # Prose notes: harvest scaffold-defect / confirmed flags for ids not in the table,
    # or annotate ids that are. Keyed on the bolded note lead "**reg-NNNN ...:**".
    for nm in re.finditer(r"\*\*(reg-\d+)[^:]*:\*\*\s*(.+)", text):
        iid, note = nm.group(1), nm.group(2).strip()
        low = note.lower()
        if iid not in out:
            if "scaffold defect" in low or "false-abstain" in low or "trigger 5a" in low:
                tag = "scaffold-defect"
            elif "confirm" in low:
                tag = "noted"
            else:
                tag = "noted"
            out[iid] = {
                "date": "",
                "judge": "",
                "human": "",
                "trigger": "",
                "rationale": note,
                "action": note,
                "dk": "",
                "outcome": tag,
            }
        else:
            out[iid].setdefault("note", note)
    return out


# Experiments whose `## Raw outputs` table is a SELECTED-mismatches table with
# col-4 prose. These prose cells are the human-review characterization of WHY the
# judge erred (e.g. reg-0088: "trigger 5a fires") — the scaffold-defect record that
# does NOT live in corrections-log.md. We harvest them so `card` can surface a
# scaffold-defect outcome sourced from real logged data, not invented.
PARTIAL_TABLE_EXPERIMENTS = [
    REGEVAL_DIR / "experiments" / "2026-05-30-01-rubric-graded-v4.md",
]


def load_partial_table_notes(experiments=None):
    """Return {item_id: {"src","gold","judge","prose"}} from selected-mismatch tables."""
    experiments = experiments or PARTIAL_TABLE_EXPERIMENTS
    out = {}
    for exp in experiments:
        if not exp.exists():
            continue
        rows = parse_raw_outputs(exp)
        kind, _ = classify_table(rows)
        if kind != "partial":
            continue
        for r in rows:
            out.setdefault(
                r["id"],
                {"src": exp.name, "gold": r["gold"], "judge": r["judge"], "prose": r["note"]},
            )
    return out


def classify_defect(prose):
    """Tag a partial-table prose cell as scaffold-defect vs gold-calibration."""
    low = prose.lower()
    if "trigger" in low and ("fires" in low or "5a" in low or "5b" in low):
        return "scaffold-defect"
    return "noted"


# ---------------------------------------------------------------------------
# Shared: build the aligned (item, human, judge) stream from a full table
# ---------------------------------------------------------------------------
def build_stream(experiment_path, snapshot_path):
    """Return (rows, header, kind, reason). rows preserve experiment-table order.

    Each row dict gains `human` (= gold label from the snapshot, falling back to the
    table's gold col) and `judge`. The snapshot gold is authoritative — it carries
    relabel history — but we cross-check against the table gold and note any drift.
    """
    rows = parse_raw_outputs(experiment_path)
    header = parse_experiment_header(experiment_path)
    kind, reason = classify_table(rows)
    snap = load_gold_snapshot(snapshot_path)
    drift = []
    for r in rows:
        snap_gold = snap.get(r["id"], {}).get("gold_label")
        r["human"] = snap_gold if snap_gold is not None else r["gold"]
        r["table_gold"] = r["gold"]
        r["gold_rationale"] = snap.get(r["id"], {}).get("gold_rationale", "")
        r["input"] = snap.get(r["id"], {}).get("input", "")
        if snap_gold is not None and snap_gold != r["gold"]:
            drift.append((r["id"], r["gold"], snap_gold))
    header["_gold_drift"] = drift
    return rows, header, kind, reason


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------
TICK = "✓"  # ✓
CROSS = "✗"  # ✗


def _tty():
    return sys.stdout.isatty()


def render_partial_banner(experiment_path, reason, header):
    n = "?"
    m = re.search(r"N=(\d+)", reason)
    if m:
        n = m.group(1)
    return "\n".join(
        [
            "┌─ PARTIAL TABLE — κ NOT COMPUTABLE OVER FULL SET ───────────",
            f"│ experiment : {experiment_path.name}",
            f"│ detected   : {reason}",
            f"│ logged κ   : {header.get('kappa')}  (over the FULL gold set, N≈100)",
            "│",
            "│ This experiment logged only SELECTED mismatches (col-4 is prose,",
            "│ not a ✓/✗ per-item stream). Recomputing κ over these rows would",
            "│ produce a meaningless number (all-mismatch ⇒ κ≈0), so this CLI",
            "│ refuses to quote it. Use `card <id>` to inspect individual rows,",
            "│ or point `replay` at a full per-item run (e.g. fable-judge-v1).",
            "└────────────────────────────────────────────────────────────",
        ]
    )


def render_confusion(gold, pred):
    classes = sorted(set(gold) | set(pred))
    width = max(len(c) for c in classes + ["judge→"]) + 1
    header = "human↓ \\ judge→".ljust(16) + "".join(c.rjust(width) for c in classes)
    lines = [header]
    for g in classes:
        row = g.ljust(16)
        for p in classes:
            n = sum(1 for gg, pp in zip(gold, pred) if gg == g and pp == p)
            row += str(n).rjust(width)
        lines.append(row)
    return "\n".join(lines)


def reconcile_line(recomputed, logged):
    if logged is None:
        return f"  (no logged κ in header to reconcile against; recomputed κ={recomputed:.3f})"
    delta = abs(recomputed - logged)
    if delta <= 0.001:
        return f"  RECONCILES {TICK}  recomputed κ={recomputed:.3f} == logged κ={logged:.3f}  (Δ={delta:.4f})"
    return (
        f"  RECONCILES {CROSS}  recomputed κ={recomputed:.3f} != logged κ={logged:.3f}  "
        f"(Δ={delta:.4f}) — investigate gold drift / table edit"
    )


# ---------------------------------------------------------------------------
# Subcommand: replay
# ---------------------------------------------------------------------------
def cmd_replay(experiment_path, snapshot_path, mismatches_only, no_anim):
    rows, header, kind, reason = build_stream(experiment_path, snapshot_path)
    if kind != "full":
        print(render_partial_banner(experiment_path, reason, header))
        return 2

    logged = header.get("kappa")
    print(f"REPLAY  {experiment_path.name}   (human = gold panel; judge = scaffold under test)")
    print(f"  streaming N={len(rows)} items in logged order; κ recomputed after each\n")

    seen_gold, seen_judge = [], []
    n_mismatch = 0
    for r in rows:
        seen_gold.append(r["human"])
        seen_judge.append(r["judge"])
        agree = r["human"] == r["judge"]
        if not agree:
            n_mismatch += 1
        k = cohen_kappa(seen_gold, seen_judge)
        mark = TICK if agree else CROSS
        if mismatches_only and agree:
            continue
        line = (
            f"  {r['id']}  human={r['human']:>14s}  judge={r['judge']:>14s}  "
            f"{mark}   κ_so_far={k:.3f}"
        )
        print(line)
        if not no_anim and _tty():
            sys.stdout.flush()

    final_k = cohen_kappa(seen_gold, seen_judge)
    n = len(rows)
    print("\n" + "─" * 60)
    print(f"  final: N={n}  agree={n - n_mismatch}  mismatch={n_mismatch}")
    print(reconcile_line(final_k, logged))
    if header.get("_gold_drift"):
        print(f"  ⚠ gold drift (table vs snapshot): {header['_gold_drift']}")

    print("\n  confusion matrix")
    for ln in render_confusion(seen_gold, seen_judge).splitlines():
        print("    " + ln)

    print("\n  per-class κ (one-vs-rest)")
    for cls in sorted(set(seen_gold) | set(seen_judge)):
        flag = "  ← abstain class" if cls in ABSTAIN_LABELS else ""
        print(f"    {cls:>14s}: {per_class_kappa(seen_gold, seen_judge, cls):.3f}{flag}")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: summary
# ---------------------------------------------------------------------------
def cmd_summary(experiment_path, snapshot_path):
    rows, header, kind, reason = build_stream(experiment_path, snapshot_path)
    if kind != "full":
        print(render_partial_banner(experiment_path, reason, header))
        return 2

    gold = [r["human"] for r in rows]
    judge = [r["judge"] for r in rows]
    n = len(rows)
    n_agree = sum(g == j for g, j in zip(gold, judge))
    k = cohen_kappa(gold, judge)
    logged = header.get("kappa")

    accept = (ACCEPT_LABELS & set(gold)).pop() if (ACCEPT_LABELS & set(gold)) else "compliant"
    reject = (REJECT_LABELS & set(gold)).pop() if (REJECT_LABELS & set(gold)) else "non-compliant"
    tpr = recall(gold, judge, accept)
    tnr = recall(gold, judge, reject)
    abst = sum(1 for j in judge if j in ABSTAIN_LABELS) / n

    corr = load_corrections_log()
    corr_here = [r["id"] for r in rows if r["id"] in corr]

    print(f"SUMMARY  {experiment_path.name}   (human-vs-judge scoreboard)")
    print("─" * 60)
    print(f"  N = {n}    agree = {n_agree}    mismatch = {n - n_agree}")
    print(f"  κ (recomputed) = {k:.3f}    κ (logged) = {logged}")
    print(reconcile_line(k, logged))
    print(f"  TPR (recall on {accept}) = {tpr:.3f}")
    print(f"  TNR (recall on {reject}) = {tnr:.3f}")
    print(f"  abstention rate            = {abst:.3f}")
    print("\n  per-class κ (one-vs-rest)")
    for cls in sorted(set(gold) | set(judge)):
        flag = "  ← abstain class" if cls in ABSTAIN_LABELS else ""
        print(f"    {cls:>14s}: {per_class_kappa(gold, judge, cls):.3f}{flag}")
    print(f"\n  corrections-log entries among these items: {len(corr_here)}  {corr_here}")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: card
# ---------------------------------------------------------------------------
def cmd_card(experiment_path, snapshot_path, item_id):
    rows, header, kind, reason = build_stream(experiment_path, snapshot_path)
    row = next((r for r in rows if r["id"] == item_id), None)
    if row is None:
        raise SystemExit(f"item {item_id} not in {experiment_path.name}")

    corr = load_corrections_log()
    entry = corr.get(item_id)
    agree = row["human"] == row["judge"]
    flag = "AGREE" if agree else "MISMATCH"

    lines = [
        "┌─ human-vs-judge adjudication card ─────────────────────────",
        f"│ item     : {item_id}   ({experiment_path.name})",
        f"│ verdict  : human={row['human']}  judge={row['judge']}  → {flag}",
        "│",
        f"│ human (gold) says : {(row['gold_rationale'] or '(none in snapshot)')[:120]}",
        f"│ judge        says : {(row['note'] if not row['note'].startswith((TICK, CROSS)) else '(tick-only table; no rationale)')[:120]}",
    ]
    if entry:
        lines += [
            "│",
            "│ ── adjudication outcome (corrections-log) ──",
        ]
        if entry["outcome"] == "relabel":
            if entry["judge"] == entry["human"]:
                # Human sided WITH the judge against a miscalibrated gold panel —
                # the gold label was the error, not the judge.
                lines += [
                    f"│   human review confirmed the judge and corrected the gold panel:",
                    f"│   {entry['date']}  judge={entry['judge']} = human={entry['human']}  (prior gold label was the error)",
                    f"│   trigger : {entry['trigger']}",
                    f"│   action  : {entry['action']}  (δκ {entry['dk']})",
                ]
            else:
                lines += [
                    f"│   the human sat in judgment over the judge and WON:",
                    f"│   {entry['date']}  judge={entry['judge']} → human={entry['human']}",
                    f"│   trigger : {entry['trigger']}",
                    f"│   action  : {entry['action']}  (δκ {entry['dk']})",
                ]
        elif entry["outcome"] == "scaffold-defect":
            lines += [
                f"│   SCAFFOLD DEFECT confirmed by human review:",
                f"│   {entry['rationale'][:160]}",
            ]
        else:
            lines += [f"│   noted: {entry['rationale'][:160]}"]
    else:
        # No corrections-log row. Cross-reference selected-mismatch tables (e.g.
        # rubric-graded-v4) — that's where reg-0088's scaffold-defect record lives.
        pt = load_partial_table_notes().get(item_id)
        if pt:
            tag = classify_defect(pt["prose"])
            lines += ["│", "│ ── adjudication outcome (mismatch-table review) ──"]
            if tag == "scaffold-defect":
                lines += [
                    f"│   SCAFFOLD DEFECT (human-reviewed in {pt['src']}):",
                    f"│   judge={pt['judge']} vs gold={pt['gold']} — {pt['prose'][:150]}",
                ]
            else:
                lines += [f"│   reviewed in {pt['src']}: {pt['prose'][:150]}"]
        else:
            lines += [
                "│",
                "│ (no corrections-log entry for this item — not adjudicated)",
            ]
    lines += [
        "│",
        f"│ input excerpt : {(row['input'][:140] + '…') if row['input'] else '(none)'}",
        f"│ run : {header.get('experiment_id')}  verdict={header.get('verdict')}  logged κ={header.get('kappa')}",
        "└────────────────────────────────────────────────────────────",
    ]
    print("\n".join(lines))
    return 0


# ---------------------------------------------------------------------------
# Subcommand: adjudicate (optional — Framing A blind moment, scriptable)
# ---------------------------------------------------------------------------
def _append_correction(date, item_id, judge, human, trigger, rationale, action):
    """Append one row to the corrections-log table, after the last data row."""
    if not CORRECTIONS_LOG.exists():
        raise SystemExit(f"corrections-log not found: {CORRECTIONS_LOG}")
    lines = CORRECTIONS_LOG.read_text().splitlines()
    row = (f"| {date} | {item_id} | {judge} | {human} | {trigger} "
           f"| {rationale} | {action} | TBD |")
    # insert after the last existing data row (lines beginning '| 20YY-'); else
    # after the table separator (|---).
    last_data = max((i for i, l in enumerate(lines) if re.match(r"\|\s*20\d\d-", l)),
                    default=None)
    if last_data is None:
        sep = max((i for i, l in enumerate(lines) if re.match(r"\|\s*-{2,}", l)), default=None)
        if sep is None:
            raise SystemExit("could not locate the corrections-log table to append to.")
        last_data = sep
    lines.insert(last_data + 1, row)
    CORRECTIONS_LOG.write_text("\n".join(lines) + "\n")

def _flip_queue_item(item_id, human, date):
    """Flip the first PENDING checkbox for item_id in review-queue.md to RESOLVED."""
    if not REVIEW_QUEUE.exists():
        return False
    lines = REVIEW_QUEUE.read_text().splitlines()
    pat = re.compile(rf"^- \[ \] \*\*{re.escape(item_id)}\*\*")
    for i, l in enumerate(lines):
        if pat.match(l):
            lines[i] = (l.replace("- [ ]", "- [x]", 1)
                        + f" → ✅ RESOLVED ({human}, {date})")
            REVIEW_QUEUE.write_text("\n".join(lines) + "\n")
            return True
    return False

def cmd_adjudicate(experiment_path, snapshot_path, item_id, do_log=False):
    rows, header, kind, reason = build_stream(experiment_path, snapshot_path)
    row = next((r for r in rows if r["id"] == item_id), None)
    if row is None:
        raise SystemExit(f"item {item_id} not in {experiment_path.name}")

    print("┌─ blind adjudication ───────────────────────────────────────")
    print(f"│ item : {item_id}")
    print(f"│ input: {(row['input'][:200] + '…') if row['input'] else '(none)'}")
    print("│ judge verdict: [MASKED — label it yourself first]")
    print("└────────────────────────────────────────────────────────────")
    print("Enter your human label (compliant / non-compliant / unclear): ", end="")
    sys.stdout.flush()

    human_label = sys.stdin.readline().strip()
    if not human_label:
        raise SystemExit("no label read from stdin — aborting (nothing persisted).")

    judge = row["judge"]
    gold = row["human"]
    print("\n── REVEAL ──")
    print(f"  your label  : {human_label}")
    print(f"  judge label : {judge}")
    print(f"  gold label  : {gold}")
    print(f"  you vs judge : {'AGREE' if human_label == judge else 'DISAGREE'}")
    print(f"  you vs gold  : {'AGREE' if human_label == gold else 'DISAGREE'}")

    if not do_log:
        if human_label != judge:
            print(
                "\n  → You disagreed with the judge. Re-run with --log to record this to "
                "inputs/corrections-log.md (relabel-gold vs refine-scaffold). (Not persisted here.)"
            )
        return 0

    # --log: capture the decision into corrections-log + flip the review queue.
    print("\n── LOG (--log) ──")
    print("One-line rationale: ", end=""); sys.stdout.flush()
    rationale = (sys.stdin.readline().strip() or "(none given)").replace("|", "/")
    print("Action [relabel-gold / refine-scaffold / noted-no-action]: ", end=""); sys.stdout.flush()
    action = (sys.stdin.readline().strip() or "noted-no-action").replace("|", "/")

    if human_label == judge:
        trigger = "No — judge correct"
    elif judge in ABSTAIN_LABELS and human_label not in ABSTAIN_LABELS:
        trigger = "Yes — judge over-abstained, human resolved"
    elif human_label in ABSTAIN_LABELS:
        trigger = "No — genuine ambiguity (human also abstains)"
    else:
        trigger = "Yes — judge/human class disagreement"

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    _append_correction(date, item_id, judge, human_label, trigger, rationale, action)
    flipped = _flip_queue_item(item_id, human_label, date)
    print(f"  ✓ appended to inputs/corrections-log.md (δκ=TBD until next scored run)")
    print(f"  ✓ review-queue.md: {item_id} → RESOLVED" if flipped
          else f"  · review-queue.md: no pending entry for {item_id} (nothing to flip)")
    print("  · gold.jsonl and scaffolds/current.md untouched — relabel/promote stay manual.")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="RegEval human-vs-judge CLI (REV-009)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    for name in ("replay", "card", "summary", "adjudicate"):
        sp = sub.add_parser(name)
        sp.add_argument("experiment", help="experiment .md (path relative to regeval/ ok)")
        if name in ("card", "adjudicate"):
            sp.add_argument("item_id", help="e.g. reg-0088")
        sp.add_argument("--gold-snapshot", required=True, help="gold snapshot .jsonl for this run")
        if name == "replay":
            sp.add_argument("--mismatches-only", action="store_true",
                            help="print only ✗ rows (κ still computed over full stream)")
            sp.add_argument("--no-anim", action="store_true",
                            help="no per-line flush — clean pipeable output for recording")
        if name == "adjudicate":
            sp.add_argument("--log", action="store_true", dest="do_log",
                            help="persist the decision: append to corrections-log.md + "
                                 "flip the item in review-queue.md (default: do not persist)")

    args = ap.parse_args()
    exp = resolve(args.experiment)
    snap = resolve(args.gold_snapshot)
    for label, p in (("experiment", exp), ("gold-snapshot", snap)):
        if not p.exists():
            raise SystemExit(f"{label} not found: {p}")

    if args.cmd == "replay":
        return cmd_replay(exp, snap, args.mismatches_only, args.no_anim)
    if args.cmd == "summary":
        return cmd_summary(exp, snap)
    if args.cmd == "card":
        return cmd_card(exp, snap, args.item_id)
    if args.cmd == "adjudicate":
        return cmd_adjudicate(exp, snap, args.item_id, do_log=args.do_log)


if __name__ == "__main__":
    sys.exit(main() or 0)
