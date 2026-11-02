# PROGRAMMA PYAT W1-H source lock

Canonical PRE-MAIN at intake: `9809203fd915a84bae056a67210e9213879840db`.
Common base: `acbe2326c8f52dfe8bfa200e87c5c07a62a5c93a`.

| Lane | Return SHA | Primary object | Rows |
|---|---|---|---:|
| A | `f2e043d61a34b20b0867adf7c725e3351d381620` | PLAN_CROSSWALK.jsonl | 656 |
| B | `b90f1a0322bf8c7995b0d89ce22e3478c6ce723e` | CURRENT_REALIZATION.jsonl | 28 |
| C | `b240d00f0cb3b962868d75a9d202cd2117952d87` | SEAMS.jsonl | 37 |
| D | `0a339445f80a78275e3dd63208de7d28e28ce419` | SOURCE35_COVERAGE.jsonl | 35 |
| E | `ed26b919a87855ecffcd21127c316429875cc4ee` | WORK_AND_AUTHORITY_STATE.jsonl | 22 |
| F | `85b532289ed60a82f7521a07adf4c4e546bf3dc1` | GRAPH_REFERENCE_CONTRACT.json | proposed sample |
| G | `9bec60dc8223e6f969a67a264bc45f82600a4a5a` | HISTORICAL_REALIZATIONS.jsonl | 29 |

All seven primary objects are under `WORKER_RETURNS/PROGRAMMA_PYAT_PREP_W1_<LANE>_20261101_R1/` at the corresponding immutable SHA. Their return reports and support artifacts must be fetched at the same cut.

These are source-bearing, non-adopted worker returns. The counts are different record grains and must not be summed as unique components. B, C and G performed selected S2 sourcefree tests, which are author-reported receipts, not native source or independent reviewer acceptance. No canonical PRE-MAIN write is authorized by this intake.
