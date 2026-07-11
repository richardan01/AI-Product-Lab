#!/usr/bin/env python3
"""
make_n1_fixture — truncate a normalized trace at its first error → an N-1 fixture.

Shankar & Husain's N-1 protocol: to regression-test a failure, don't replay the whole
session — capture the trajectory *up to the turn before the failure* and re-run just the
next turn against the target. This script produces that prefix from a normalized trace
(Evals/_schema/trace-schema.md). Re-running the next turn is target-dependent and out of
scope here (for repo workflows, feed the prefix to eval-runner).

No API key, no network, stdlib only.

Usage:
  python3 scripts/make_n1_fixture.py --trace Evals/agent-harness/_traces/files/ah-0001.json
  python3 scripts/make_n1_fixture.py --trace <t>.json --error-index 5   # explicit tool_call index
  python3 scripts/make_n1_fixture.py --trace <t>.json --stdout

Options:
  --trace PATH       normalized trace JSON (required).
  --error-index N    tool_calls index to truncate before. Default: first tool_call ok==false.
  --out PATH         output path. Default: alongside the trace as <id>.n1.json.
  --stdout           print instead of writing.
"""

import argparse
import json
import sys
from pathlib import Path


def find_first_error(trace):
    for tc in trace.get("tool_calls", []):
        if tc.get("ok") is False:
            return tc["i"]
    return None


def truncate(trace, error_index):
    """Keep everything strictly before the failing tool call."""
    failing = next((tc for tc in trace["tool_calls"] if tc["i"] == error_index), None)
    if failing is None:
        sys.exit(f"error: no tool_call with index {error_index} in trace")

    # The turn that issued the failing call is its boundary; keep turns before it.
    turn_cut = failing.get("turn_index", len(trace.get("turns", [])))
    kept_turns = [t for t in trace.get("turns", []) if t["i"] < turn_cut]
    kept_calls = [tc for tc in trace["tool_calls"] if tc["i"] < error_index]

    n1 = dict(trace)
    n1["trace_id"] = f"{trace['trace_id']}.n1"
    n1["derived_from"] = trace["trace_id"]
    n1["n1_cut_before"] = {
        "tool_call_index": error_index,
        "tool": failing.get("name"),
        "params": failing.get("params"),
        "turn_index": turn_cut,
    }
    n1["turns"] = kept_turns
    n1["tool_calls"] = kept_calls
    n1["retrievals"] = [r for r in trace.get("retrievals", [])
                        if r.get("tool_call_index", 1e9) < error_index]
    n1["final_output"] = ""  # the whole point: the next turn is what gets re-run
    m = dict(trace.get("metrics", {}))
    m["turn_count"] = len(kept_turns)
    m["tool_call_count"] = len(kept_calls)
    m["tool_error_count"] = sum(1 for tc in kept_calls if tc.get("ok") is False)
    n1["metrics"] = m
    return n1


def main():
    ap = argparse.ArgumentParser(description="Truncate a trace at its first error → N-1 fixture.")
    ap.add_argument("--trace", required=True)
    ap.add_argument("--error-index", type=int)
    ap.add_argument("--out")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()

    trace = json.loads(Path(args.trace).read_text(encoding="utf-8"))

    idx = args.error_index if args.error_index is not None else find_first_error(trace)
    if idx is None:
        sys.exit("error: trace has no ok==false tool_call; pass --error-index to choose a cut point")

    n1 = truncate(trace, idx)
    payload = json.dumps(n1, indent=2, ensure_ascii=False)

    if args.stdout:
        print(payload)
    else:
        out = Path(args.out) if args.out else Path(args.trace).with_suffix(".n1.json")
        out.write_text(payload, encoding="utf-8")
        print(f"wrote {out}")
        print(f"  cut before tool_call #{idx} ({n1['n1_cut_before']['tool']}); "
              f"kept {n1['metrics']['turn_count']} turns, "
              f"{n1['metrics']['tool_call_count']} tool_calls")


if __name__ == "__main__":
    main()
