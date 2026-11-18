# SEMANTIC CLOSURE — 10K, FOUR REMAINING OPERATIONS

**Status:** `FULL_SEMANTIC_TRUTH_CLOSURE_FOUR_OPS`  
**Estate:** retained 10k/5 estate `e192dc25e55528101b6116f81aa7bce49c170a9a72f61386e97d20a9f9e09619`; no rebuild.  
**Executed:** `selected_weighted`, `f2_forward_raw`, `f2_reverse_raw`, `repeated_mr_raw` once each. **F4 not rerun** (independently verified).

## Actual values / full payloads

| Op | Q s | O s | State | Raw num/denom | Weighted num/denom | Risk / denom members |
|---|---:|---:|---|---:|---:|---:|
| selected_weighted | 24.320 | 0.441 | SUPPORTED | 5000 / 5000 | 15000/1 / 15000/1 | 10,000 / 5,000 |
| f2_forward_raw | 21.868 | 0.379 | SUPPORTED | 5000 / 5000 | — | 10,000 / 5,000 |
| f2_reverse_raw | 21.392 | 0.358 | SUPPORTED | 3333 / 3333 | — | 10,000 / 3,333 |
| repeated_mr_raw | 16.105 | 0.161 | SUPPORTED | 385 / 385 | — | 770 / 385 |

- H admission: **0.575 s**; S prepared index: **12.651 s**; external supervised wall **106.187 s**; RSS 722,276,352 B; scratch 122,591,630 B; exit 0, no abort.
- O is a separate timer around `canonical_json(f.as_dict())` for each full payload; it is not added to Q.
- Full `as_dict` payloads are exported as `*.payload.json.gz`; full cells, risk/denominator member refs, provenance, ref/replay and expected truth are frozen in `RESULT.json` / `EXPECTED_TRUTH.json`.
- Source-open instrumentation captured **1** Python `builtins.open`/`os.open` event. Arrow C++/SQLite internal opens and mmap are not fully observable via Python hooks; no hardcoded zero is claimed.
- No original/raw source read.

## Controlled truth

`EXPECTED_TRUTH.json` derives full cells, weighted masses, exact risk/denominator member sets and states from the controlled 10k A/B/C/MR pattern and weights `1+(i%4)`. All four operations match: cells, weighted cells, risk set, denominator set, raw numerator/denominator, state. This is a fixture truth comparison, not a new production evaluator.

No F4 rerun; no prior baseline/profiler/test adapter; no 100k/full-width/science/source/actor/CURRENT acceptance.
