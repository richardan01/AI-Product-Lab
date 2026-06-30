#!/usr/bin/env python3
"""
RegEval experiment runner.
Usage: python3 run_experiment.py <scaffold-slug>
e.g.:  python3 run_experiment.py skills-v2

Reads:  scaffolds/candidates/<slug>.md  (or scaffolds/current.md if slug == "current")
        inputs/gold.jsonl
Writes: experiments/<date>-<NN>-<slug>.md
        experiments/log.md  (appends one row)
Prints: verdict + κ + diagnostics
"""

import json
import sys
import os
import re
import time
import math
import random
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REGEVAL_DIR = Path(__file__).parent
GOLD_PATH   = REGEVAL_DIR / "inputs" / "gold.jsonl"
SCAFFOLDS   = REGEVAL_DIR / "scaffolds"
EXPERIMENTS = REGEVAL_DIR / "experiments"
LOG_PATH    = EXPERIMENTS / "log.md"
TEMPLATE    = EXPERIMENTS / "_template.md"
BUDGET_PATH = REGEVAL_DIR / "budget.md"

CHAMPION_KAPPA = 0.820   # rubric-graded-v4 gold-cal-v1
KEEP_THRESHOLD = 0.80
SUSPICIOUS_ABST= 0.50
HARD_KILL_SECS = 8 * 60  # 8 minutes

MODEL = "claude-sonnet-4-5"   # default judge model; override via env REGEVAL_MODEL

# ---------------------------------------------------------------------------
# Kappa computation
# ---------------------------------------------------------------------------
CLASSES = ["compliant", "non-compliant", "unclear"]

def cohen_kappa(gold_labels, pred_labels):
    n = len(gold_labels)
    assert n > 0
    p_o = sum(g == p for g, p in zip(gold_labels, pred_labels)) / n
    g_cnt = Counter(gold_labels)
    p_cnt = Counter(pred_labels)
    p_e = sum((g_cnt[c] / n) * (p_cnt[c] / n) for c in CLASSES)
    if p_e >= 1.0:
        return 1.0
    return (p_o - p_e) / (1 - p_e)

def bootstrap_ci(gold_labels, pred_labels, n_resamples=1000, ci=0.95):
    n = len(gold_labels)
    pairs = list(zip(gold_labels, pred_labels))
    kappas = []
    for _ in range(n_resamples):
        sample = random.choices(pairs, k=n)
        gs, ps = zip(*sample)
        kappas.append(cohen_kappa(list(gs), list(ps)))
    kappas.sort()
    lo_idx = int((1 - ci) / 2 * n_resamples)
    hi_idx = int((1 - (1 - ci) / 2) * n_resamples)
    return kappas[lo_idx], kappas[min(hi_idx, n_resamples - 1)]

def per_class_kappa(gold_labels, pred_labels, cls):
    """One-vs-rest kappa for a single class."""
    g_bin = ["yes" if x == cls else "no" for x in gold_labels]
    p_bin = ["yes" if x == cls else "no" for x in pred_labels]
    n = len(g_bin)
    p_o = sum(g == p for g, p in zip(g_bin, p_bin)) / n
    g_cnt = Counter(g_bin); p_cnt = Counter(p_bin)
    p_e = sum((g_cnt[c] / n) * (p_cnt[c] / n) for c in ["yes", "no"])
    if p_e >= 1.0:
        return 1.0
    return (p_o - p_e) / (1 - p_e)

def tpr(gold_labels, pred_labels):
    """True positive rate on 'compliant' class."""
    tp = sum(g == "compliant" and p == "compliant" for g, p in zip(gold_labels, pred_labels))
    total = sum(g == "compliant" for g in gold_labels)
    return tp / total if total else float("nan")

def tnr(gold_labels, pred_labels):
    """True negative rate on 'non-compliant' class."""
    tn = sum(g == "non-compliant" and p == "non-compliant" for g, p in zip(gold_labels, pred_labels))
    total = sum(g == "non-compliant" for g in gold_labels)
    return tn / total if total else float("nan")

def abstention_rate(pred_labels):
    return sum(p == "unclear" for p in pred_labels) / len(pred_labels)

# ---------------------------------------------------------------------------
# Scaffold loading
# ---------------------------------------------------------------------------
def load_scaffold(slug):
    if slug == "current":
        path = SCAFFOLDS / "current.md"
    else:
        path = SCAFFOLDS / "candidates" / f"{slug}.md"
    if not path.exists():
        raise FileNotFoundError(f"Scaffold not found: {path}")
    return path.read_text()

def extract_system_prompt(scaffold_text):
    """
    The scaffold markdown IS the system prompt — pass it in full.
    The judge sees the entire scaffold as its instructions.
    """
    return scaffold_text

# ---------------------------------------------------------------------------
# Gold dataset
# ---------------------------------------------------------------------------
def load_gold():
    items = []
    with open(GOLD_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items

# ---------------------------------------------------------------------------
# Judge call
# ---------------------------------------------------------------------------
def run_judge(client, system_prompt, input_text, model):
    """Call the judge scaffold once. Returns (label, rationale, raw_text)."""
    response = client.messages.create(
        model=model,
        max_tokens=256,
        system=system_prompt,
        messages=[{"role": "user", "content": input_text}],
    )
    raw = response.content[0].text.strip()

    # Parse "label: X\nrationale: Y"
    label_match = re.search(r"label\s*:\s*(compliant|non-compliant|unclear)", raw, re.IGNORECASE)
    rat_match   = re.search(r"rationale\s*:\s*(.+)", raw, re.IGNORECASE | re.DOTALL)

    label     = label_match.group(1).lower() if label_match else "unclear"   # default unclear on parse failure
    rationale = rat_match.group(1).strip()[:120] if rat_match else raw[:120]

    # Normalise label
    if label not in ("compliant", "non-compliant", "unclear"):
        label = "unclear"

    return label, rationale, raw

# ---------------------------------------------------------------------------
# Experiment file helpers
# ---------------------------------------------------------------------------
def next_nn(date_str):
    """Return the next NN suffix for today's experiments (zero-padded 2 digits)."""
    existing = list(EXPERIMENTS.glob(f"{date_str}-*.md"))
    nums = []
    for p in existing:
        m = re.match(rf"{date_str}-(\d+)-", p.name)
        if m:
            nums.append(int(m.group(1)))
    return f"{max(nums) + 1:02d}" if nums else "01"

def write_experiment_file(date_str, nn, slug, results, verdict, kappa, ci_lo, ci_hi,
                          tpr_val, tnr_val, abst_val, wall_secs, scaffold_slug, hypothesis,
                          delta_bullets, narrative, next_suggestion):
    fname = f"{date_str}-{nn}-{slug}.md"
    path  = EXPERIMENTS / fname

    row_lines = "\n".join(
        f"| {r['id']} | {r['gold']} | {r['pred']} | {'✓' if r['match'] else '✗'} |"
        for r in results
    )

    mins = int(wall_secs // 60)
    secs = int(wall_secs % 60)

    content = f"""# RegEval experiment {date_str}-{nn} — {slug}

**Verdict:** {verdict}
**κ:** {kappa:.3f} (95% CI [{ci_lo:.3f}, {ci_hi:.3f}])  vs champion {CHAMPION_KAPPA:.3f}
**Diagnostics:** TPR={tpr_val:.3f} · TNR={tnr_val:.3f} · abst={abst_val:.3f} · N={len(results)}
**Wall clock:** {mins}:{secs:02d}

## Hypothesis
{hypothesis}

## Scaffold delta vs champion
{delta_bullets}

## Result narrative
{narrative}

## Why this verdict
{"κ=" + f"{kappa:.3f}" + (" ≥ 0.80 KEEP bar, CI lower bound " + f"{ci_lo:.3f}" + " ≥ 0.70, abst < 50%" if verdict == "KEEP" else f" {'above' if kappa > CHAMPION_KAPPA else 'below'} champion {CHAMPION_KAPPA:.3f}; {'HOLD — directional improvement' if kappa >= 0.60 else 'DISCARD — κ below 0.60 or regression'}")}

## Next experiment suggestion
{next_suggestion}

## Raw outputs
<details>
<summary>Per-item judge outputs (N={len(results)})</summary>

| id | gold | judge | match |
|---|---|---|---|
{row_lines}

</details>
"""
    path.write_text(content)
    return fname

def append_log(date_str, nn, slug, verdict, kappa, tpr_val, tnr_val, abst_val, n, why):
    line = f"| {date_str} | {nn} | {slug} | **{verdict}** | κ={kappa:.3f} (CI [{0:.3f}, {0:.3f}]) | TPR={tpr_val:.3f} TNR={tnr_val:.3f} abst={abst_val:.3f} N={n} | {why} |"
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_experiment.py <scaffold-slug>")
        sys.exit(1)

    slug   = sys.argv[1]
    model  = os.environ.get("REGEVAL_MODEL", MODEL)
    client = anthropic.Anthropic()

    print(f"\n{'='*60}")
    print(f"  RegEval experiment runner")
    print(f"  Scaffold : {slug}")
    print(f"  Model    : {model}")
    print(f"  Gold N   : (loading...)")
    print(f"{'='*60}\n")

    # Load resources
    scaffold_text = load_scaffold(slug)
    system_prompt = extract_system_prompt(scaffold_text)
    gold_items    = load_gold()
    n             = len(gold_items)
    print(f"  Gold items loaded: {n}")

    # Extract hypothesis from scaffold (first "> **Hypothesis:**" block)
    hyp_match = re.search(r"Hypothesis\*\*:?\s*(.+?)(?:\n\n|\n>)", scaffold_text, re.DOTALL)
    hypothesis = hyp_match.group(1).strip().replace("\n", " ") if hyp_match else "(see scaffold)"

    # Extract delta
    delta_match = re.search(r"Scaffold delta[^\n]*\n(.+?)(?:\n---|\n##)", scaffold_text, re.DOTALL)
    delta_bullets = delta_match.group(1).strip() if delta_match else "(see scaffold vs current.md)"

    # Run
    start_time  = time.time()
    results     = []
    parse_fails = 0

    for i, item in enumerate(gold_items):
        elapsed = time.time() - start_time
        if elapsed > HARD_KILL_SECS:
            print(f"\n  HARD KILL at {elapsed:.0f}s — experiment logged as FAIL")
            verdict = "FAIL"
            # Write partial log and exit
            date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            nn = next_nn(date_str)
            append_log(date_str, nn, slug, "FAIL", 0.0, 0.0, 0.0, 0.0, i, f"Budget exceeded at {elapsed:.0f}s after {i} items")
            sys.exit(1)

        print(f"  [{i+1:3d}/{n}] {item['id']} ...", end="", flush=True)
        try:
            pred_label, rationale, raw = run_judge(client, system_prompt, item["input"], model)
        except Exception as e:
            print(f" ERROR: {e}")
            pred_label = "unclear"
            parse_fails += 1

        match = pred_label == item["gold_label"]
        results.append({
            "id":   item["id"],
            "gold": item["gold_label"],
            "pred": pred_label,
            "match": match,
            "rationale": rationale,
        })
        print(f" {item['gold_label']:>15s} → {pred_label:>15s}  {'✓' if match else '✗'}")

    wall_secs = time.time() - start_time

    # Compute metrics
    gold_labels = [r["gold"] for r in results]
    pred_labels = [r["pred"] for r in results]

    kappa    = cohen_kappa(gold_labels, pred_labels)
    ci_lo, ci_hi = bootstrap_ci(gold_labels, pred_labels)
    tpr_val  = tpr(gold_labels, pred_labels)
    tnr_val  = tnr(gold_labels, pred_labels)
    abst_val = abstention_rate(pred_labels)
    pk = {c: per_class_kappa(gold_labels, pred_labels, c) for c in CLASSES}

    # Verdict
    suspicious = abst_val > SUSPICIOUS_ABST and kappa >= KEEP_THRESHOLD
    if kappa >= KEEP_THRESHOLD and ci_lo >= 0.70 and abst_val <= SUSPICIOUS_ABST:
        verdict = "KEEP"
    elif kappa >= CHAMPION_KAPPA:
        verdict = "HOLD"
    elif kappa >= 0.60:
        verdict = "HOLD"
    else:
        verdict = "DISCARD"
    if suspicious:
        verdict += "*SUSPICIOUS"

    # Result narrative (auto-generated summary)
    correct  = sum(r["match"] for r in results)
    misses   = [r for r in results if not r["match"]]
    miss_ids = ", ".join(r["id"] for r in misses[:8]) + ("..." if len(misses) > 8 else "")
    narrative = (
        f"{correct}/{n} correct. κ={kappa:.3f} vs champion {CHAMPION_KAPPA:.3f} "
        f"(Δ={kappa - CHAMPION_KAPPA:+.3f}). "
        f"Per-class κ: compliant={pk['compliant']:.3f} · non-compliant={pk['non-compliant']:.3f} · unclear={pk['unclear']:.3f}. "
        f"{'Mismatches: ' + miss_ids if misses else 'No mismatches — perfect agreement.'}"
        + (f" Parse failures: {parse_fails}." if parse_fails else "")
    )
    next_suggestion = "(leave blank — assess after reviewing mismatches)"

    # Write experiment file
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    nn = next_nn(date_str)
    fname = write_experiment_file(
        date_str, nn, slug, results, verdict, kappa, ci_lo, ci_hi,
        tpr_val, tnr_val, abst_val, wall_secs, slug,
        hypothesis, delta_bullets, narrative, next_suggestion
    )

    # Append log
    why = f"κ={kappa:.3f} Δ={kappa - CHAMPION_KAPPA:+.3f}; TPR={tpr_val:.3f} TNR={tnr_val:.3f} abst={abst_val:.3f}"
    append_log(date_str, nn, slug, verdict, kappa, tpr_val, tnr_val, abst_val, n, why)

    # Print summary
    print(f"\n{'='*60}")
    print(f"  VERDICT  : {verdict}")
    print(f"  κ        : {kappa:.3f}  (95% CI [{ci_lo:.3f}, {ci_hi:.3f}])  vs champion {CHAMPION_KAPPA:.3f}  Δ={kappa - CHAMPION_KAPPA:+.3f}")
    print(f"  TPR      : {tpr_val:.3f}   TNR : {tnr_val:.3f}   Abst : {abst_val:.3f}")
    print(f"  Per-class: compliant={pk['compliant']:.3f}  non-compliant={pk['non-compliant']:.3f}  unclear={pk['unclear']:.3f}")
    print(f"  Wall     : {int(wall_secs//60)}:{int(wall_secs%60):02d}")
    print(f"  Written  : experiments/{fname}")
    print(f"  Log      : appended to experiments/log.md")
    print(f"{'='*60}\n")

    if verdict == "KEEP":
        print("  *** KEEP — overwrite scaffolds/current.md? (y/N): ", end="", flush=True)
        ans = input().strip().lower()
        if ans == "y":
            import shutil
            src = SCAFFOLDS / "candidates" / f"{slug}.md"
            dst = SCAFFOLDS / "current.md"
            shutil.copy2(src, dst)
            # Patch status line
            txt = dst.read_text()
            txt = re.sub(r"\*\*Status:\*\*.*", f"**Status:** current (KEEP — {date_str}, κ={kappa:.3f})", txt)
            dst.write_text(txt)
            print(f"  scaffolds/current.md updated to {slug}.")
        else:
            print("  current.md unchanged. Update manually if you accept the KEEP.")

if __name__ == "__main__":
    main()
