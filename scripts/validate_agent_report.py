#!/usr/bin/env python3
"""Validate the public/private agent-evaluation report contract."""

import json
import re
import sys
from pathlib import Path

ALLOWED_VERDICTS = {"pass", "fail", "partial", "insufficient-evidence"}
ALLOWED_SEVERITIES = {"bad", "sad", None}
EXPECTED_IDS = [
    "00-task-success", "01-tool-choice", "02-parameter-extraction",
    "03-error-recovery", "04-context-retention", "05-efficiency",
    "06-goal-checkpoints",
]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_agent_report.py <report.json>")
    report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    required = {
        "schema_version", "trace_id", "run_kind", "run_date", "repo_commit",
        "grader_runner", "grader_model", "author_grader_separation", "provenance_note",
        "source_harness", "task_success", "overall_verdict", "bad_count", "sad_count",
        "axes", "recommendation",
    }
    missing = sorted(required - report.keys())
    assert not missing, f"missing report fields: {missing}"
    assert report["schema_version"] == "1.1"
    assert report["grader_runner"] in {"claude-code", "codex-review"}

    # Provenance block. A published verdict must be able to say when it ran, against which
    # commit, on which model, and whether author/grader separation held. Unknown provenance
    # is recorded as an explicit null and explained — never omitted, never invented.
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", report["run_date"] or ""), \
        f"run_date must be YYYY-MM-DD, got {report['run_date']!r}"
    assert isinstance(report["repo_commit"], str) and len(report["repo_commit"]) >= 7, \
        "repo_commit must be a commit SHA of at least 7 characters"
    grader_model = report["grader_model"]
    assert grader_model is None or (isinstance(grader_model, str) and grader_model.strip()), \
        "grader_model must be a non-empty string or an explicit null"
    assert isinstance(report["author_grader_separation"], bool), \
        "author_grader_separation must be a boolean"
    note = report["provenance_note"]
    assert isinstance(note, str) and note.strip(), "provenance_note must be a non-empty string"
    if grader_model is None:
        assert "not recorded" in note.lower(), \
            "grader_model is null, so provenance_note must say the model was not recorded"
    assert report["task_success"] in ALLOWED_VERDICTS
    assert report["overall_verdict"] in ALLOWED_VERDICTS
    assert [axis.get("eval_id") for axis in report["axes"]] == EXPECTED_IDS
    for axis in report["axes"]:
        assert axis.get("verdict") in ALLOWED_VERDICTS
        assert axis.get("severity") in ALLOWED_SEVERITIES
        assert isinstance(axis.get("evidence"), str) and axis["evidence"].strip()
    bad_count = sum(1 for axis in report["axes"] if axis["verdict"] != "pass" and axis["severity"] == "bad")
    sad_count = sum(1 for axis in report["axes"] if axis["verdict"] != "pass" and axis["severity"] == "sad")
    assert report["bad_count"] == bad_count
    assert report["sad_count"] == sad_count
    expected_overall = "pass" if report["task_success"] == "pass" and bad_count == 0 else "fail"
    if report["task_success"] == "insufficient-evidence":
        expected_overall = "insufficient-evidence"
    assert report["overall_verdict"] == expected_overall
    print("Agent report schema passed.")


if __name__ == "__main__":
    main()
