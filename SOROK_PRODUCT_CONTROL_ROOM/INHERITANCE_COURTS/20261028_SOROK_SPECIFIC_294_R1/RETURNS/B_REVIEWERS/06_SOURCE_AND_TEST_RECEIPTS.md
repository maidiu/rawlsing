# B67 GitHub source and test receipts — inspection scope

**GitHub repository:** private `maidiu/rawlsing`. **Pinned manifest:** `MANIFEST_B_REVIEWERS.json` Git blob `45e79e72de3d3c686f99289e4c1b658e7321582b`, commission pack `bf69287f62f05a0b61bc54b4c79b6bd7f2d90b89`; historical PRE-MAIN control `299f41e97a43c67be9cc76a79fa49b48f4e12e54`.

## Machine evidence inventory

| Receipt class | Observed scope | Exact file |
|---|---|---|
| Pinned original reviewer branches | 67 unique original branch names / 67 SHA heads | `01_BRANCH_ROWS.json` |
| Actual reviewer source document fetches | 67 Git blobs, pinned by exact path+commit; moved Sorok08 R2 read separately | `01_BRANCH_ROWS.json`, `STAGING/REVIEW_SOURCE_CORRECTIONS.json` |
| Actual review-side Python source content reads | 29 Git blobs; source definitions/assertions, not only names | `07_CODE_SOURCE_INSPECTION.json` |
| Reviewer claim records | 67 typed source/negative/unknown-consumer findings | `02_CAPABILITY_FINDINGS.json` |
| Candidate author/preimage mentions | 67 records; SHA mentions never themselves grant author/test identity | `08_REVIEW_AUTHOR_SOURCE_GRAPH.json` |
| Current remote HEAD freshness | 66 unchanged, 1 moved, 0 absent | `05_FRESH_BRANCH_TAIL.json` |
| Supplemental pinned discovery | Ten source-inspection batches; five corrected first-source selections | `STAGING/INDEX_*.json`, `STAGING/REVIEW_SOURCE_CORRECTIONS.json` |

## What was actually executed during THIS audit

- Authenticated GitHub file/commit/ref/compare reads and bounded machine enumeration: **EXECUTED**; no private survey/production bytes touched.
- Repository-side `create_file` and `update_file` on own B return subtree: **EXECUTED**; commit receipts are GitHub commits on `agent/rabochii-sorok-20261028-294-b-reviewers-r1`.
- Local `pytest`, imported private modules, subprocess, cold SQLite, new code faults/mutations, Mac/Git worktree test: **NOT RUN**.
- Original independent reviewer returns frequently contain JUnit, logs, cold process and test measurements; here these remain **original attributed historical reports**, not newly observed execution. No pass totals are pooled into new acceptance.
- No authoritative actor, original human learning law, native CAN008/CAN011/ADP/SCI05, Pyat N11/N12, C11/C12, A5 or original source/grant was issued.

## Validation

`01_BRANCH_ROWS.json` contains the exact original 67 names, no duplicates; `05_FRESH_BRANCH_TAIL.json` preserves the single R1→R2 movement with the original immutable source still accessible. Reviewer source changed-path lists ending at 300 are explicitly labeled potentially truncated. Full commit-level object/true merge-base equivalence, exact imported original author code and PRE-MAIN consumer closure remain unproved; they must not be silently inferred from the source inspection.

**Meaning:** this is a qualified, complete **B-reviewer source retrieval and archival evidence ledger**, not a complete 67-function original-code acceptance court and not authorization to integrate code.
