#!/usr/bin/env python3
"""PostToolUse hook: register a pending eval re-run when a source file mapped
in Evals/_ci-map.md is edited or written.

Spec: .claude/skills/eval-ci/SKILL.md, "Automating registration with a hook".
Must always exit 0 -- a bug here must never block normal editing.
"""
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path


def parse_table_rows(text):
    """Yield stripped cell lists for markdown table rows, skipping header/separator lines."""
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or set(cells[0]) <= {"-", ":"}:
            continue
        yield cells


def find_affected_suites(ci_map_path, rel_path):
    if not ci_map_path.exists():
        return []
    for cells in parse_table_rows(ci_map_path.read_text()):
        if len(cells) < 2 or cells[0] in ("Source file",):
            continue
        if cells[0] == rel_path:
            return [s.strip() for s in cells[1].split(",") if s.strip()]
    return []


def has_uncleared_pending(pending_text, suite, rel_path):
    for cells in parse_table_rows(pending_text):
        if len(cells) < 5 or cells[0] in ("Suite",):
            continue
        if cells[0] == suite and cells[1] == rel_path and cells[4] == "pending":
            return True
    return False


def git_head(project_dir):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_dir, capture_output=True, text=True, timeout=5,
        )
        return result.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def main():
    payload = json.load(sys.stdin)

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or ".").resolve()
    file_path = payload.get("tool_input", {}).get("file_path")
    if not file_path:
        return

    try:
        rel_path = str(Path(file_path).resolve().relative_to(project_dir))
    except Exception:
        rel_path = file_path

    ci_map_path = project_dir / "Evals" / "_ci-map.md"
    suites = find_affected_suites(ci_map_path, rel_path)
    if not suites:
        return

    pending_path = project_dir / "Evals" / "_pending-reruns.md"
    if not pending_path.exists():
        return
    pending_text = pending_path.read_text()

    commit_sha = git_head(project_dir)
    today = date.today().isoformat()

    registered = [
        suite for suite in suites
        if not has_uncleared_pending(pending_text, suite, rel_path)
    ]
    if not registered:
        return

    new_rows = "".join(
        f"| {suite} | {rel_path} | {commit_sha} | {today} | pending | — |\n"
        for suite in registered
    )
    with pending_path.open("a") as f:
        if not pending_text.endswith("\n"):
            f.write("\n")
        f.write(new_rows)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"eval-ci: registered pending re-run for {', '.join(registered)} "
                f"(source: {rel_path})"
            ),
        }
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
