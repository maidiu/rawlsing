# ROUTING 10K MATCHED TRIAL — aee954 vs 68aa

**Status:** `MATCHED_10K_F2_TRIAL_EXACT_PARITY`; one measured pair, no extrapolation or production speedup acceptance.

- Baseline `68aa7cac...` / product `6dcb875b...`
- Candidate `aee95429609c...` / product `0f0a7395...`
- Retained 10k/5-role estate `e192dc25...`; contract `d2a7ffa8...`; **10,000 respondents at five roles**, not full survey width
- Exact `f2_forward_raw` and `f2_reverse_raw`, separate fresh processes and sessions, actual public prepared I03

| Metric | Baseline | Candidate |
|---|---:|---:|
| H admission | 0.566 s | 0.401 s |
| S prepared/index | 12.997 s | 28.024 s |
| Q forward / reverse | 23.803 / 22.446 s | 13.390 / 12.987 s |
| O serialization | 0.731 s | 0.713 s |
| H+S+Q+O | 60.543 s | 55.516 s |
| External child wall | 63.642 s | 58.795 s |
| Sampled RSS peak | 534,695,936 B | 511,090,688 B |
| Sampled estate scratch peak | 132,392,464 B | 224,376,352 B |
| Routing objects, setup / Q | 0 / 100,000 | 50,000 / 20,000 |
| Routing lookup calls / seconds | 20,000 / 30.678 s | 20,000 / 10.107 s |

Full payloads, fact/replay/provenance refs, cells and risk/denominator identity sets are **exact** for both operations. Candidate added **14.862 s** setup and removed **19.872 s** Q in this pair; total H+S+Q+O is 5.027 s lower. One pair only; no linear 100k/full-width claim. OS page cache uncontrolled; per-child 600 s, total 900 s, RSS 6 GiB, scratch 4 GiB; total external 122.437 s; no abort. No build, fallback matrix, retry after start, or native source.
