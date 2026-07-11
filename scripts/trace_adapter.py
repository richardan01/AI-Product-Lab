#!/usr/bin/env python3
"""
Trace adapter — normalize agent-harness session logs into the eval trace schema.

Reads the JSONL a coding/agent harness writes to disk and emits a single
normalized trace JSON per session, conforming to Evals/_schema/trace-schema.md.
This is what turns "attach to Claude Code / Codex" from a slogan into an input
the agent-harness eval suite can actually grade.

No API key, no network, stdlib only.

Usage:
  # Claude Code — verified format (~/.claude/projects/<proj>/<session>.jsonl)
  python3 scripts/trace_adapter.py claude-code --input <session>.jsonl \
      --suite agent-harness [--trace-id ah-0001]

  # Codex CLI — documented format (~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl)
  python3 scripts/trace_adapter.py codex --input rollout-*.jsonl \
      --suite agent-harness [--trace-id ah-0001]

  # Discover the newest Claude Code session for a project instead of a path:
  python3 scripts/trace_adapter.py claude-code --latest --suite agent-harness

Options:
  --input PATH     source JSONL. Omit with --latest (claude-code only).
  --latest         pick the most-recently-modified session under ~/.claude/projects.
                   Caveat: if a Claude Code session is running right now, that live
                   file is usually the most recent — pass --input to grade a
                   specific finished session.
  --suite NAME     destination suite; output lands in Evals/<suite>/_traces/files/.
  --trace-id ID    override the auto-assigned <prefix>-NNNN id.
  --out PATH       write to an explicit path instead of the suite _traces dir.
  --stdout         print the normalized JSON to stdout instead of writing a file.

Version tolerance: unknown line/item types are counted in `skipped_lines`, never
fatal. Both harness formats are internal and change between releases (their own
docs say so), so a non-zero `skipped_lines.unknown` is the signal to update the
mapping below — not a crash.
"""

import argparse
import glob
import json
import os
import sys
from pathlib import Path

ADAPTER_VERSION = "1"

# Tools we heuristically treat as retrieval (FAQ's retrieval/generation split).
RETRIEVAL_TOOLS = {
    "Read", "Grep", "Glob", "WebFetch", "WebSearch",       # Claude Code
    "read_file", "grep", "search", "web_search", "fetch",  # codex-ish
}

# Codex's search/read intent is usually buried in a generic shell tool's `command`
# string, not in a dedicated tool name (unlike Claude Code's Read/Grep/Glob). These
# names carry no retrieval-vs-write signal on their own.
SHELL_TOOL_NAMES = {"shell", "local_shell_call", "custom_tool_call"}

# Conservative allowlist: a shell call is classed as retrieval only if its FIRST
# word is one of these read-only verbs. Deliberately excludes dual-use verbs (sed,
# awk, ...) that can also write. Known imprecision: this doesn't inspect flags, so
# e.g. `find . -delete` or `find . -exec rm {} \;` still matches on `find` and is
# misclassified as retrieval — a first-token allowlist, not a flag parser.
SHELL_RETRIEVAL_VERBS = {"grep", "rg", "find", "cat", "head", "tail", "ls"}


def _is_shell_retrieval(tc):
    if tc["name"] not in SHELL_TOOL_NAMES:
        return False
    command = tc["params"].get("command")
    if not isinstance(command, str) or not command.strip():
        return False
    first_word = command.strip().split(None, 1)[0].strip("'\"")
    return first_word in SHELL_RETRIEVAL_VERBS

# Claude Code harness plumbing that arrives as `user` turns WITHOUT an isMeta
# flag (verified against a real session: command echoes and task notifications
# are key-identical to genuine user messages). Filtered by leading tag only —
# a real user message quoting one of these mid-text is kept.
CLAUDE_PLUMBING_TAGS = (
    "<local-command-caveat>", "<command-name>", "<local-command-stdout>",
    "<system-reminder>", "<task-notification>",
)


def _is_plumbing(text):
    return isinstance(text, str) and text.lstrip().startswith(CLAUDE_PLUMBING_TAGS)


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def _read_jsonl(path):
    """Yield (lineno, obj) for each parseable line; count unparseable ones."""
    bad = 0
    with open(path, encoding="utf-8") as fh:
        for n, raw in enumerate(fh):
            raw = raw.strip()
            if not raw:
                continue
            try:
                yield n, json.loads(raw)
            except json.JSONDecodeError:
                bad += 1
    if bad:
        sys.stderr.write(f"warn: {bad} unparseable line(s) in {path}\n")


def _stringify(content):
    """Collapse a tool_result / message content (str | list | dict) to text."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                # Check key PRESENCE, not truthiness — an empty "text": "" is a
                # real (empty) value, not "key absent, fall back to dumping the
                # whole block." Conflating the two previously turned a genuinely
                # empty text block into a misleading json.dumps(block) string.
                if "text" in block:
                    parts.append(block["text"])
                elif "content" in block:
                    parts.append(block["content"])
                else:
                    parts.append(json.dumps(block))
            else:
                parts.append(str(block))
        return "\n".join(p for p in parts if p)
    if isinstance(content, dict):
        return content["text"] if "text" in content else json.dumps(content)
    return str(content)


def _wall_seconds(first_ts, last_ts):
    """ISO8601 delta in seconds, or None if either timestamp is missing/unparseable."""
    if not first_ts or not last_ts:
        return None
    try:
        from datetime import datetime

        def _p(s):
            return datetime.fromisoformat(s.replace("Z", "+00:00"))

        return round((_p(last_ts) - _p(first_ts)).total_seconds(), 1)
    except (ValueError, AttributeError):
        return None


def _assemble(source_harness, session_id, captured_from, goal,
              turns, tool_calls, final_output, first_ts, last_ts, skipped):
    """Build the normalized trace dict from mapped pieces."""
    retrievals = [
        {"tool_call_index": tc["i"], "name": tc["name"],
         "query": tc["params"].get("query") or tc["params"].get("pattern")
                  or tc["params"].get("file_path") or tc["params"].get("url")
                  or tc["params"].get("command")}
        for tc in tool_calls
        if tc["name"] in RETRIEVAL_TOOLS or _is_shell_retrieval(tc)
    ]
    tool_err = sum(1 for tc in tool_calls if tc["ok"] is False)
    return {
        "trace_id": None,  # filled by caller
        "source_harness": source_harness,
        "session_id": session_id,
        "captured_from": captured_from,
        "adapter_version": ADAPTER_VERSION,
        "goal": goal,
        "turns": turns,
        "tool_calls": tool_calls,
        "retrievals": retrievals,
        "final_output": final_output,
        "metrics": {
            "turn_count": len(turns),
            "tool_call_count": len(tool_calls),
            "tool_error_count": tool_err,
            "input_tokens": skipped.pop("_in_tokens", None),
            "output_tokens": skipped.pop("_out_tokens", None),
            "wall_seconds": _wall_seconds(first_ts, last_ts),
        },
        "skipped_lines": skipped,
    }


# ----------------------------------------------------------------------------
# claude-code adapter (verified against a real session file)
# ----------------------------------------------------------------------------

def adapt_claude_code(path):
    turns, tool_calls, results_by_id = [], [], {}
    goal, final_output = None, ""
    first_ts = last_ts = None
    in_tokens = out_tokens = 0
    skipped = {}

    def skip(kind):
        skipped[kind] = skipped.get(kind, 0) + 1

    for _, obj in _read_jsonl(path):
        # Exclude sub-agent sidechains — we grade the main trajectory.
        if obj.get("isSidechain"):
            skip("sidechain")
            continue
        # Exclude harness plumbing (slash-command caveats, command stdout,
        # system-reminders) — these are not user/assistant turns.
        if obj.get("isMeta"):
            skip("meta")
            continue
        ts = obj.get("timestamp")
        if ts:
            first_ts = first_ts or ts
            last_ts = ts
        typ = obj.get("type")

        if typ == "assistant":
            msg = obj.get("message") or {}
            usage = msg.get("usage") or {}
            in_tokens += usage.get("input_tokens") or 0
            out_tokens += usage.get("output_tokens") or 0
            for block in msg.get("content") or []:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type")
                if btype == "text":
                    text = block.get("text", "")
                    turns.append({"i": len(turns), "role": "assistant", "text": text, "ts": ts})
                    if text.strip():
                        final_output = text
                elif btype == "tool_use":
                    tool_calls.append({
                        "i": len(tool_calls), "name": block.get("name", "?"),
                        "params": block.get("input") or {}, "result": None,
                        "ok": None, "ts": ts, "turn_index": len(turns),
                        "_id": block.get("id"),
                    })
                elif btype == "thinking":
                    pass  # reasoning is not part of the gradable trajectory
                else:
                    skip(f"assistant.{btype}")

        elif typ == "user":
            msg = obj.get("message") or {}
            content = msg.get("content")
            if isinstance(content, str):
                if _is_plumbing(content):
                    skip("meta")
                    continue
                if not goal:
                    goal = content
                turns.append({"i": len(turns), "role": "user", "text": content, "ts": ts})
            elif isinstance(content, list):
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "tool_result":
                        results_by_id[block.get("tool_use_id")] = {
                            "result": _stringify(block.get("content")),
                            "ok": not bool(block.get("is_error")),
                        }
                    elif block.get("type") == "text":
                        text = block.get("text", "")
                        if _is_plumbing(text):
                            skip("meta")
                            continue
                        if not goal:
                            goal = text
                        turns.append({"i": len(turns), "role": "user",
                                      "text": text, "ts": ts})
        else:
            skip(typ or "unknown")

    # Stitch tool results onto their calls by id.
    for tc in tool_calls:
        res = results_by_id.get(tc.pop("_id", None))
        if res:
            tc["result"], tc["ok"] = res["result"], res["ok"]

    skipped["_in_tokens"] = in_tokens or None
    skipped["_out_tokens"] = out_tokens or None
    return _assemble("claude-code", None, str(path), goal, turns, tool_calls,
                     final_output, first_ts, last_ts, skipped), \
        _first_session_id(path)


def _first_session_id(path):
    for _, obj in _read_jsonl(path):
        if obj.get("sessionId"):
            return obj["sessionId"]
    return Path(path).stem


# ----------------------------------------------------------------------------
# codex adapter (documented format; validate against a real rollout before trusting)
# ----------------------------------------------------------------------------

def adapt_codex(path):
    """Codex rollout-*.jsonl → normalized trace.

    Defensive mapping over the documented Codex item types. Codex wraps each item
    as {"type": <kind>, "payload": {...}} or emits the payload flat; we handle both.
    Known kinds: message (role/content), function_call (name/arguments), function_
    call_output (call_id/output), reasoning (dropped).

    Retrieval classification: Codex's search/read intent is usually buried inside a
    generic shell tool's `command` string (see SHELL_TOOL_NAMES/SHELL_RETRIEVAL_VERBS
    above), not in a dedicated tool name. The heuristic is a first-token allowlist,
    not a flag parser — it will misclassify a destructive invocation like
    `find . -delete` as retrieval since it only looks at the leading verb.

    Codex real-rollout validation: NOT yet validated against a local file — this
    environment has no Codex CLI installed and no ~/.codex directory (confirmed via
    `which codex` + filesystem search), so no real rollout was available to test
    against. Repro recipe for a future session with Codex CLI access: (1) install
    Codex CLI, (2) run one real session (`codex exec "<simple task>"`), (3) locate
    ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl, (4) run this adapter against it,
    (5) confirm skipped_lines.unknown == 0, reconciling any nonzero bucket by
    updating the kind-matching branches below.
    """
    turns, tool_calls, results_by_id = [], [], {}
    goal, final_output = None, ""
    first_ts = last_ts = None
    session_id = Path(path).stem
    skipped = {}

    def skip(kind):
        skipped[kind] = skipped.get(kind, 0) + 1

    for _, obj in _read_jsonl(path):
        payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else obj
        ts = obj.get("timestamp") or obj.get("ts") or payload.get("timestamp")
        if ts:
            first_ts = first_ts or ts
            last_ts = ts
        kind = payload.get("type") or obj.get("type")

        # session header line
        if kind in ("session_meta", "session", "config"):
            session_id = payload.get("id") or payload.get("session_id") or session_id
            skip(kind)
            continue

        if kind == "message":
            role = payload.get("role", "assistant")
            text = _stringify(payload.get("content"))
            if role == "user" and not goal:
                goal = text
            turns.append({"i": len(turns), "role": role, "text": text, "ts": ts})
            if role == "assistant" and text.strip():
                final_output = text
        elif kind in ("function_call", "local_shell_call", "custom_tool_call"):
            args = payload.get("arguments") or payload.get("action") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {"raw": args}
            tool_calls.append({
                "i": len(tool_calls),
                "name": payload.get("name") or kind,
                "params": args, "result": None, "ok": None,
                "ts": ts, "turn_index": len(turns),
                "_id": payload.get("call_id") or payload.get("id"),
            })
        elif kind in ("function_call_output", "local_shell_call_output", "custom_tool_call_output"):
            out = payload.get("output")
            results_by_id[payload.get("call_id") or payload.get("id")] = {
                "result": _stringify(out),
                "ok": not bool((out or {}).get("is_error") if isinstance(out, dict) else False),
            }
        elif kind == "reasoning":
            pass
        else:
            skip(kind or "unknown")

    for tc in tool_calls:
        res = results_by_id.get(tc.pop("_id", None))
        if res:
            tc["result"], tc["ok"] = res["result"], res["ok"]

    return _assemble("codex", session_id, str(path), goal, turns, tool_calls,
                     final_output, first_ts, last_ts, skipped), session_id


# ----------------------------------------------------------------------------
# io
# ----------------------------------------------------------------------------

def _repo_root():
    return Path(__file__).resolve().parents[1]


def _next_trace_id(suite):
    prefix = "".join(w[0] for w in suite.split("-"))[:3] or suite[:2]
    files = _repo_root() / "Evals" / suite / "_traces" / "files"
    n = 0
    if files.is_dir():
        for f in files.glob(f"{prefix}-*.json"):
            try:
                n = max(n, int(f.stem.split("-")[-1]))
            except ValueError:
                continue
    return f"{prefix}-{n + 1:04d}"


def _find_latest_claude_session():
    base = Path.home() / ".claude" / "projects"
    cands = list(base.glob("*/*.jsonl"))
    if not cands:
        sys.exit(f"error: no Claude Code sessions under {base}")
    return max(cands, key=lambda p: p.stat().st_mtime)


def main():
    ap = argparse.ArgumentParser(description="Normalize harness logs to the eval trace schema.")
    ap.add_argument("harness", choices=["claude-code", "codex"])
    ap.add_argument("--input")
    ap.add_argument("--latest", action="store_true")
    ap.add_argument("--suite", default="agent-harness")
    ap.add_argument("--trace-id")
    ap.add_argument("--out")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()

    if args.latest and args.harness == "claude-code":
        path = _find_latest_claude_session()
    elif args.input:
        matches = sorted(glob.glob(os.path.expanduser(args.input)))
        if not matches:
            sys.exit(f"error: no file matches --input {args.input}")
        path = Path(matches[-1])
    else:
        sys.exit("error: pass --input PATH (or --latest for claude-code)")

    trace, session_id = (adapt_claude_code(path) if args.harness == "claude-code"
                         else adapt_codex(path))
    trace["session_id"] = session_id
    trace["trace_id"] = args.trace_id or _next_trace_id(args.suite)

    payload = json.dumps(trace, indent=2, ensure_ascii=False)
    if args.stdout:
        print(payload)
    else:
        out = Path(args.out) if args.out else (
            _repo_root() / "Evals" / args.suite / "_traces" / "files" / f"{trace['trace_id']}.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
        m = trace["metrics"]
        print(f"wrote {out}")
        print(f"  trace_id={trace['trace_id']} harness={trace['source_harness']} "
              f"turns={m['turn_count']} tool_calls={m['tool_call_count']} "
              f"errors={m['tool_error_count']} skipped={dict(trace['skipped_lines'])}")


if __name__ == "__main__":
    main()
