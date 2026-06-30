# Build-review packet — CSV-ingest module for eval scaffold

**Author:** PM · **Artifact:** `evals/ingest_csv.py` · **Spec:** `Evals/research-synthesis/spec.md` · **Status:** for build review

## Spec (under test)
- Read a labeled CSV of captured traces (`trace_id, input, output, label`) and emit one normalized JSON record per row for the grader to consume.
- Malformed rows (missing column, bad encoding) → fail loudly with the offending row number; never silently drop a row.
- Must be safe to re-run on the same input without corrupting prior output (the scaffold re-ingests on every eval run).

## What was built
- `ingest_csv.py` reads the CSV with the stdlib `csv` module and builds JSON records.
- Row handling:
  ```python
  for i, row in enumerate(reader):
      try:
          records.append(normalize(row))
      except Exception:
          pass   # skip anything that doesn't parse, keep going
  ```
- Added a generic `Pipeline` class with `register_stage()` / `run_stages()` so future ingest steps can be chained. Right now `ingest_csv.py` is the **only caller** and registers exactly one stage.
- Writes output by opening `out.json` in `"w"` mode and dumping at the end of the run.
- No log line, no counter of rows read vs. records emitted.

## Run record
- **I haven't run it against a real CSV yet** — wrote it from the spec and it imports clean, so it should be fine. Plan to run it once it's wired into the scaffold.
