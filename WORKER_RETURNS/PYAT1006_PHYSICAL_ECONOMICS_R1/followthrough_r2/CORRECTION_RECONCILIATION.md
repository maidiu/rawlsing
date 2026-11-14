# #1006 report correction and independent-G5 reconciliation

## Controlling review

- Independent nonauthor G5: `0169fac9f3840800796c664eee462bbb8984bb42`
  (draft PR #1034), verdict **`REVISE_EXACT_DEFECT`**, dated 2026-11-13 ET.
- Reviewed author cut: `51aabffef90399359008e00890f551a1e56c0da9`
  (`05e9ceacfd1a43aa8c21ff3144502550916deadd` code/tests).
- Frozen production: `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`.
- Review data reused read-only:
  `/Users/matthewsmith/.codex/worktrees/pyat1007-dual-series-prep/Rawlsing/WORKER_REVIEWS/PYAT1006_PHYSICAL_ECONOMICS_G5_R1/data/`.

## Exact corrections

### 1. Test count

- Withdrawn claim: "36 passed" for the S2-D saved/adversarial/five-reader/
  source-scope group.
- Actual RUNBOOK five-file command: **29 passed**
  (`evidence/accepted_s2d_five_file_29.txt`).
- Separate partial-binding-order suite: **2 passed**
  (`evidence/accepted_s2d_partial_binding_2.txt`); 29 + 2 = 31.
- S2-C/S2-D focused group: **31 passed**
  (`evidence/accepted_s2c_s2d_focused_31.txt`).
- Own original fixture tests: **6 passed**; follow-through locality tests:
  **2 passed**.
- No 36-test selection exists; no raw log was rewritten to fabricate one.

### 2. RSS labels

- The old 1k/10k "writer process-tree RSS" rows were whole shape-worker peaks
  including queries/native readers.
- Corrected writer-only measurements: 1k `194,072,576 B` (own monitored
  writer-only run, `evidence/writer_only_1k_monitored.json`); 10k
  `214,261,760 B` (independent review).
- 50k/100k rows remain writer-only because those runs stopped after write.

### 3. Causal claim and proposal

Old claim: `_respondent_family`'s per-respondent `ORDER BY ref` plus a small
row-group LRU caused the measured churn.  That is disproved:

- the same per-respondent SQL gives 10k routing reads `10,043` in native
  ref-key respondent order versus `258` in physical insertion order;
- 100k selected had `101,438` routing reads and `100,050` event reads with zero
  consecutive-gid cache hits;
- within one respondent, routing rows occupy one gid for 1,984/2,000,
  coordinate/weight for 2,000/2,000, and events for 1,992/2,000.

The actual cause is the native evaluator's
`sorted(index.respondents.values(), key=lambda item: item.ref.key)` traversal
(`rawlsing_next/_pre553_query_eval.py`) across physically ordered row groups,
with a separate event-row cache.  A per-respondent `(gid,off)` sort cannot fix
cross-respondent order or the event cache.

## Corrected follow-through

The runtime candidate in `locality_probe.py` is labeled
`EXPERIMENT_NOT_IMPLEMENTED` and patches only that module-global sort to use the
session's physical insertion order.  It preserves exact fact/projection/replay/
release refs on the same reviewer-retained releases:

| case | query | baseline | candidate | factor | exact |
|---|---|---:|---:|---:|---|
| 100k | selected | 580.548 s / 204,125 reads | 265.680 s / 5,784 reads | 2.19x | yes |
| 10k | selected | 49.066 s / 20,157 | 21.812 s / 588 | 2.25x | yes |
| 10k | reverse F2 | 51.790 s / 20,153 | 21.116 s / 614 | 2.45x | yes |
| 10k | 3-way F4 | 56.624 s / 20,161 | 24.665 s / 588 | 2.30x | yes |
| 1k | selected | 4.390 s / 1,784 | 2.046 s / 61 | 2.15x | yes |

Writer profile correction: the direct-I02 inclusive stage is not "SQLite
proof" in the dominant sense.  At the 2k call-boundary profile, canonical
projection/identity/object validation and body_json reconstruction dominate;
SQLite execute is about 4.2% of the inflated profile wall.  The smallest
owner-consistent writer proposal is a bounded per-build memo of the already
computed immutable semantic projection/hash reused by validation and insertion,
with every check retained.  It is not implemented.

## Preserved limits

- 100k reverse F2/F4 and candidate I05/grouped execution: `NOT_RUN`.
- 100k all-seven, 10/10 repetitions, #997 source bridge, #998 joined vertical,
  #1001 full 100k/6 GiB and #1007 rights: held.
- Known #999 coherent native body-truth RED remains external; no blanket
  native correctness is claimed.
- Candidate is not a production patch, owner acceptance, optimized engine or
  independent G5.
