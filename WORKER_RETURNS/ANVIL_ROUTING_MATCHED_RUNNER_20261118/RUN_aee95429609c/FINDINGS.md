# ROUTING MATCHED TRIAL — aee95429609c vs 68aa7cac7

**Status:** `MATCHED_TRIAL_EXACT_PARITY`; one measured pair only, not production speedup acceptance.

- Baseline: `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`; product sha `6dcb875b...`
- Candidate: `aee95429609c372564e996c2d3d3eb30e9253cbf`; product sha `0f0a7395...`
- Estate: sealed WIDTH128 `4d9604dc...`; contract `89645891...`
- Operations: exact `f2_forward` + `f2_reverse`; separate fresh processes/sessions.

| Metric | Baseline | Candidate |
|---|---:|---:|
| H admission | 0.393 s | 0.412 s |
| S prepared/index | 26.106 s | 43.702 s |
| Q forward/reverse | 25.295 / 22.614 s | 0.234 / 0.214 s |
| O serialization | 0.0084 s | 0.0079 s |
| H+S+Q+O | 74.417 s | 44.570 s |
| External child wall | 75.177 s | 45.542 s |
| Sampled RSS peak | 194,965,504 B | 157,671,424 B |
| Sampled estate scratch peak | 386,700,816 B | 323,143,200 B |
| Routing objects, setup / Q | 0 / 153,600 | 76,800 / 256 |
| Row-group reads, setup / Q | 422 / 811 | 422 / 5 |
| Family objects, setup / Q | 68,960 / 153,600 | 145,760 / 256 |
| Routing lookup calls / seconds | 256 / 47.088 s | 256 / 0.108 s |

Full payloads, fact/replay/provenance refs, cells and risk/denominator identity sets: **exact** for both operations. Candidate adds 17.615 s setup (S) and removes 47.462 s Q in this pair; total H+S+Q+O is 29.847 s lower. One pair only; no linear 100k/full-width claim. OS page cache uncontrolled; per-child caps 600 s, total 900 s, RSS 6 GiB, scratch 4 GiB; no abort. The candidate locator setup is reflected in S and routing reconstruction; no adapter-disabled same-session comparison.
