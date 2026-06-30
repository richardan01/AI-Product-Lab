# (tool-test artifact — safe to delete)

This file was generated as a **test of `error_analysis.py`** against the now-deprecated 3-class
`gold_expansion.jsonl`. It is not a real analysis. The canonical forward discovery pass is
[[Evals/regeval/discovery-pass-2026-06-28]].

To regenerate a real worksheet on the current binary task:

```
python3 error_analysis.py --pred <preds.jsonl> --gold inputs/heldout_v2.jsonl --binary
```

(Sandbox could not delete this file; remove it locally: `rm experiments/discovery/2026-06-28-worksheet.md`)
