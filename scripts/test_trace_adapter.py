#!/usr/bin/env python3
"""
Regression coverage for trace_adapter.py and make_n1_fixture.py.

No test framework — this repo has none (no tests/ dir, no pytest/unittest, no
python dependency manifest anywhere). Matches the existing convention
(Evals/regeval/*.py's informal `assert` guards): stdlib-only, assert-based,
prints one PASS/FAIL line per case, exits 1 if anything failed.

Run: python3 scripts/test_trace_adapter.py

Focus: tool_calls[].turn_index semantics (forward-pointing, not backward-
referencing — see Evals/_schema/trace-schema.md), N-1 truncation edge cases,
plumbing/sidechain filtering, the goal-lock fix, and the Codex shell-retrieval
heuristic. Also smoke-tests the two committed sample fixtures so a future
edit that regresses their behavior is caught.
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import trace_adapter as ta          # noqa: E402
import make_n1_fixture as n1        # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLES = REPO_ROOT / "Evals" / "agent-harness" / "samples"


def _write(tmpdir, name, lines):
    path = Path(tmpdir) / name
    with open(path, "w", encoding="utf-8") as fh:
        for obj in lines:
            fh.write(json.dumps(obj) + "\n")
    return path


# ----------------------------------------------------------------------------
# turn_index semantics
# ----------------------------------------------------------------------------

def test_claude_code_multiple_tool_use_same_turn_index(tmpdir):
    """Two tool_use blocks in one message, no intervening text, share turn_index."""
    path = _write(tmpdir, "a.jsonl", [
        {"type": "user", "timestamp": "t0", "message": {"role": "user", "content": "do the thing"}},
        {"type": "assistant", "timestamp": "t1", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "x1", "name": "Read", "input": {"file_path": "a.py"}},
            {"type": "tool_use", "id": "x2", "name": "Grep", "input": {"pattern": "foo"}},
        ]}},
    ])
    trace, _ = ta.adapt_claude_code(path)
    assert len(trace["tool_calls"]) == 2
    assert trace["tool_calls"][0]["turn_index"] == trace["tool_calls"][1]["turn_index"] == 1


def test_claude_code_text_then_tool_use_points_past_text(tmpdir):
    """A text block followed by tool_use in the same message: tool_use turn_index
    is one past the text turn's own index, not equal to it."""
    path = _write(tmpdir, "b.jsonl", [
        {"type": "user", "timestamp": "t0", "message": {"role": "user", "content": "do the thing"}},
        {"type": "assistant", "timestamp": "t1", "message": {"role": "assistant", "content": [
            {"type": "text", "text": "Looking into it."},
            {"type": "tool_use", "id": "x1", "name": "Read", "input": {"file_path": "a.py"}},
        ]}},
    ])
    trace, _ = ta.adapt_claude_code(path)
    text_turn = next(t for t in trace["turns"] if t["role"] == "assistant")
    assert trace["tool_calls"][0]["turn_index"] == text_turn["i"] + 1


def test_codex_consecutive_function_calls_share_turn_index(tmpdir):
    """Two function_calls with no message between them share turn_index (same
    forward-pointing semantics as Claude Code)."""
    path = _write(tmpdir, "c.jsonl", [
        {"type": "response_item", "payload": {"type": "message", "role": "user",
         "content": [{"type": "text", "text": "do it"}], "timestamp": "t0"}},
        {"type": "response_item", "payload": {"type": "function_call", "name": "shell",
         "arguments": "{\"command\": \"ls\"}", "call_id": "c1", "timestamp": "t1"}},
        {"type": "response_item", "payload": {"type": "function_call", "name": "shell",
         "arguments": "{\"command\": \"cat x\"}", "call_id": "c2", "timestamp": "t2"}},
    ])
    trace, _ = ta.adapt_codex(path)
    assert len(trace["tool_calls"]) == 2
    assert trace["tool_calls"][0]["turn_index"] == trace["tool_calls"][1]["turn_index"] == 1


def test_codex_sample_fixture_turn_index_matches_hand_trace(tmpdir):
    """Regression guard against the committed fixture: the one function_call in
    codex-rollout-sample.jsonl has turn_index == 1 (hand-traced: one user turn
    appended before it, no message appended between)."""
    trace, _ = ta.adapt_codex(SAMPLES / "codex-rollout-sample.jsonl")
    assert len(trace["tool_calls"]) == 1
    assert trace["tool_calls"][0]["turn_index"] == 1


def test_dangling_turn_index_at_end_of_trace(tmpdir):
    """A tool_call that is the very last item (no further turn ever appended)
    legitimately gets turn_index == len(turns) — one past the last real index.
    This is correct, not corruption."""
    path = _write(tmpdir, "d.jsonl", [
        {"type": "user", "timestamp": "t0", "message": {"role": "user", "content": "goal"}},
        {"type": "assistant", "timestamp": "t1", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "x1", "name": "Bash", "input": {"command": "run"}},
        ]}},
    ])
    trace, _ = ta.adapt_claude_code(path)
    assert trace["tool_calls"][0]["turn_index"] == len(trace["turns"])


# ----------------------------------------------------------------------------
# goal handling
# ----------------------------------------------------------------------------

def test_empty_first_goal_does_not_lock_claude_code(tmpdir):
    path = _write(tmpdir, "e.jsonl", [
        {"type": "user", "timestamp": "t0", "message": {"role": "user", "content": ""}},
        {"type": "user", "timestamp": "t1", "message": {"role": "user", "content": "the real goal"}},
    ])
    trace, _ = ta.adapt_claude_code(path)
    assert trace["goal"] == "the real goal"


def test_empty_first_goal_does_not_lock_codex(tmpdir):
    path = _write(tmpdir, "f.jsonl", [
        {"type": "response_item", "payload": {"type": "message", "role": "user",
         "content": [{"type": "text", "text": ""}], "timestamp": "t0"}},
        {"type": "response_item", "payload": {"type": "message", "role": "user",
         "content": [{"type": "text", "text": "the real goal"}], "timestamp": "t1"}},
    ])
    trace, _ = ta.adapt_codex(path)
    assert trace["goal"] == "the real goal"


def test_no_qualifying_turn_yields_null_goal_no_crash(tmpdir):
    path = _write(tmpdir, "g.jsonl", [
        {"type": "user", "timestamp": "t0", "isMeta": True,
         "message": {"role": "user", "content": "<system-reminder>noise</system-reminder>"}},
        {"type": "assistant", "timestamp": "t1", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "x1", "name": "Bash", "input": {"command": "run"}},
        ]}},
    ])
    trace, _ = ta.adapt_claude_code(path)
    assert trace["goal"] is None


# ----------------------------------------------------------------------------
# meta / plumbing / sidechain filtering
# ----------------------------------------------------------------------------

def test_meta_plumbing_sidechain_all_filtered(tmpdir):
    path = _write(tmpdir, "h.jsonl", [
        {"type": "user", "timestamp": "t0", "message": {"role": "user", "content": "real goal text"}},
        {"type": "user", "timestamp": "t1", "isMeta": True,
         "message": {"role": "user", "content": "<system-reminder>noise</system-reminder>"}},
        {"type": "user", "timestamp": "t2", "isMeta": False,
         "message": {"role": "user", "content": "<command-name>/model</command-name>"}},
        {"type": "assistant", "timestamp": "t3", "isSidechain": True,
         "message": {"role": "assistant", "content": [{"type": "text", "text": "sidechain noise"}]}},
        {"type": "assistant", "timestamp": "t4", "message": {"role": "assistant",
         "content": [{"type": "text", "text": "real reply"}]}},
    ])
    trace, _ = ta.adapt_claude_code(path)
    texts = [t["text"] for t in trace["turns"]]
    assert texts == ["real goal text", "real reply"]
    assert trace["goal"] == "real goal text"
    assert trace["skipped_lines"].get("meta", 0) == 2
    assert trace["skipped_lines"].get("sidechain", 0) == 1


# ----------------------------------------------------------------------------
# degenerate traces
# ----------------------------------------------------------------------------

def test_zero_tool_calls_no_crash(tmpdir):
    path = _write(tmpdir, "i.jsonl", [
        {"type": "user", "timestamp": "t0", "message": {"role": "user", "content": "goal"}},
        {"type": "assistant", "timestamp": "t1", "message": {"role": "assistant",
         "content": [{"type": "text", "text": "done, no tools needed"}]}},
    ])
    trace, _ = ta.adapt_claude_code(path)
    assert trace["tool_calls"] == []
    assert trace["metrics"]["tool_call_count"] == 0
    assert n1.find_first_error(trace) is None


def test_zero_turns_all_tool_calls_get_turn_index_zero(tmpdir):
    path = _write(tmpdir, "j.jsonl", [
        {"type": "user", "timestamp": "t0", "isMeta": True,
         "message": {"role": "user", "content": "<system-reminder>noise</system-reminder>"}},
        {"type": "assistant", "timestamp": "t1", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "x1", "name": "Bash", "input": {"command": "one"}},
            {"type": "tool_use", "id": "x2", "name": "Bash", "input": {"command": "two"}},
        ]}},
    ])
    trace, _ = ta.adapt_claude_code(path)
    assert trace["turns"] == []
    assert all(tc["turn_index"] == 0 for tc in trace["tool_calls"])


# ----------------------------------------------------------------------------
# make_n1_fixture truncation
# ----------------------------------------------------------------------------

def test_truncate_error_index_zero_yields_empty_prefix(tmpdir):
    trace = {
        "trace_id": "t-0001",
        "turns": [{"i": 0, "role": "user", "text": "goal", "ts": "t0"}],
        "tool_calls": [
            {"i": 0, "name": "Bash", "params": {}, "result": "boom", "ok": False, "turn_index": 1},
            {"i": 1, "name": "Bash", "params": {}, "result": "ok", "ok": True, "turn_index": 1},
        ],
        "retrievals": [],
        "metrics": {},
    }
    assert n1.find_first_error(trace) == 0
    out = n1.truncate(trace, 0)
    assert out["tool_calls"] == []
    assert out["metrics"]["tool_call_count"] == 0
    assert len(out["turns"]) == 1  # turn_cut == 1, keeps turn i=0


def test_truncate_coding_retry_fixture_regression():
    """Locks in the currently-passing behavior verified in PR #20: the fixture's
    one ok:false call is at tool_calls index 4, and truncation cuts before it."""
    trace = json.loads((SAMPLES / "coding-retry.json").read_text(encoding="utf-8"))
    idx = n1.find_first_error(trace)
    assert idx == 4
    out = n1.truncate(trace, idx)
    assert out["metrics"]["tool_call_count"] == 4
    assert out["metrics"]["tool_error_count"] == 0
    assert out["final_output"] == ""


def test_truncate_dangling_turn_index_keeps_all_turns():
    """A failing call whose turn_index is one past the last real turn (the
    legitimate end-of-trace case) should keep every existing turn — there is
    nothing after it to cut."""
    trace = {
        "trace_id": "t-0002",
        "turns": [
            {"i": 0, "role": "user", "text": "goal", "ts": "t0"},
            {"i": 1, "role": "assistant", "text": "trying", "ts": "t1"},
        ],
        "tool_calls": [
            {"i": 0, "name": "Bash", "params": {}, "result": "boom", "ok": False, "turn_index": 2},
        ],
        "retrievals": [],
        "metrics": {},
    }
    out = n1.truncate(trace, 0)
    assert len(out["turns"]) == 2  # turn_cut == 2 == len(turns); all kept, correctly


# ----------------------------------------------------------------------------
# Codex shell-retrieval heuristic
# ----------------------------------------------------------------------------

def test_codex_sample_grep_classified_as_retrieval():
    trace, _ = ta.adapt_codex(SAMPLES / "codex-rollout-sample.jsonl")
    assert len(trace["retrievals"]) == 1
    assert trace["retrievals"][0]["name"] == "shell"
    assert trace["retrievals"][0]["query"] == "grep -n upload src/api.py"


def test_codex_shell_write_verb_not_classified_as_retrieval(tmpdir):
    path = _write(tmpdir, "k.jsonl", [
        {"type": "response_item", "payload": {"type": "message", "role": "user",
         "content": [{"type": "text", "text": "clean up"}], "timestamp": "t0"}},
        {"type": "response_item", "payload": {"type": "function_call", "name": "shell",
         "arguments": "{\"command\": \"rm -rf /tmp/x\"}", "call_id": "c1", "timestamp": "t1"}},
    ])
    trace, _ = ta.adapt_codex(path)
    assert len(trace["tool_calls"]) == 1  # still captured as a tool call
    assert trace["retrievals"] == []      # but not classified as retrieval


# ----------------------------------------------------------------------------
# runner
# ----------------------------------------------------------------------------

TESTS = [
    test_claude_code_multiple_tool_use_same_turn_index,
    test_claude_code_text_then_tool_use_points_past_text,
    test_codex_consecutive_function_calls_share_turn_index,
    test_codex_sample_fixture_turn_index_matches_hand_trace,
    test_dangling_turn_index_at_end_of_trace,
    test_empty_first_goal_does_not_lock_claude_code,
    test_empty_first_goal_does_not_lock_codex,
    test_no_qualifying_turn_yields_null_goal_no_crash,
    test_meta_plumbing_sidechain_all_filtered,
    test_zero_tool_calls_no_crash,
    test_zero_turns_all_tool_calls_get_turn_index_zero,
    test_truncate_error_index_zero_yields_empty_prefix,
    test_truncate_coding_retry_fixture_regression,
    test_truncate_dangling_turn_index_keeps_all_turns,
    test_codex_sample_grep_classified_as_retrieval,
    test_codex_shell_write_verb_not_classified_as_retrieval,
]


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for fn in TESTS:
            name = fn.__name__
            try:
                # tests that don't need scratch files take no args
                if fn.__code__.co_argcount == 0:
                    fn()
                else:
                    fn(tmpdir)
                print(f"PASS  {name}")
            except AssertionError as e:
                failures.append(name)
                print(f"FAIL  {name}: {e}")
            except Exception as e:  # noqa: BLE001 — surface any unexpected crash as a failure
                failures.append(name)
                print(f"ERROR {name}: {type(e).__name__}: {e}")

    print(f"\n{len(TESTS) - len(failures)}/{len(TESTS)} passed")
    if failures:
        print("Failed:", ", ".join(failures))
        sys.exit(1)


if __name__ == "__main__":
    main()
