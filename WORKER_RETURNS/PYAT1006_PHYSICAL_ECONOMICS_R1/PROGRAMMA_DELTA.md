# PROGRAMMA DELTA — PYAT #1006 measured physical/query economics

## Change class

HARNESS + TEST + RETURN FILES ONLY.  No `rawlsing_next` production or accepted
test file was edited, replaced, cherry-picked or merged.  No new architecture,
engine, authority store, codec, controller, timer or production producer was
created.  New files are confined to
`WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/` and the follow-through
subdirectory `followthrough_r2/`.  Existing raw baseline logs and historical
committed cuts are preserved; only the current report, test-count/RSS labels,
causal explanation and proposal are corrected.

## Independent G5 reconciliation

The fresh nonauthor review at
`0169fac9f3840800796c664eee462bbb8984bb42` (draft PR #1034, Nov 13 ET)
returned **`REVISE_EXACT_DEFECT`**.  It independently reproduced the 100k
writer (2,943.177 s), selected query (543.026 s), census, representative
oracle/change/restore and guards, and correctly rejected this author's old
causal proposal.  The three exact report defects are corrected here:

- actual cross-respondent cause and measured candidate, not
  `_respondent_family` `ORDER BY ref`;
- RUNBOOK five-file S2-D group is 29, not 36; adding the separate 2-test
  partial-binding suite gives 31;
- 1k/10k table RSS values are whole-worker peaks; writer-only 1k is
  194,072,576 B and writer-only 10k is 214,261,760 B (review), while 50k/100k
  were already writer-only.

Known #999 native coherent body-poison RED remains external and is not
repaired, hidden, or promoted.

## What the baseline establishes

1. The accepted S2-C writer and S2-D cold I03/I05/Batch/normal/resume readers
   consume one complete sourcefree 13-family release with exact native
   fact/replay parity at a qualified small oracle and exact old-root restore.
2. At 100k distinct respondents the writer finished within the 6 GiB cap:
   3,033.723 s writer, 295,211,008 B writer-only tree RSS, 310,163,264 B
   retained Parquet, 5,257,841,984 B staging peak and 4,385,796,096 B
   temporary I02 proof SQLite.
3. The same release is not economically queryable as-is: 100k selected I03
   562.362 s, reverse F2 873.655 s, 3-way F4 908.507 s; 100k query phase tree
   RSS 3,690,455,040 B.
4. The direct I02 proof is 2,249.700 s inclusive.  A 2k profiled decomposition
   shows it contains first-pass `_Sink`/`_row` body construction, Parquet
   flush, `_insert_object`, object validation, relation checks, projection/
   replay hashing and SQLite work.  The reread/re-encode proof is 761.224 s;
   root hashing is 11.101 s.  SQLite execute is only about 4.2% of the
   inflated 2k profile wall; canonical projection/identity/object validation
   and body_json reconstruction dominate.  Full profile and honest scale
   limits: `followthrough_r2/WRITER_PROFILE.md`.

## Corrected measured query cause

Independent ROWGROUPREAD counters show measured repeated row-group
materialization, but the cause is **native respondent traversal in ref-key/hash
order** across physically ordered row groups:

- 10k: 10,043 routing reads in hash order versus 258 in physical order with the
  same per-respondent SQL; 1k: 917 versus 26.
- 100k selected: 101,438 routing reads and 100,050 event reads across
  distinct caches, zero consecutive-gid cache hits; 51.9M routing rows and
  51.2M event rows decoded.
- Within one respondent, side-family rows already occupy one gid (1,984/2,000
  routing; 2,000/2,000 coordinate/weight) and events one gid for 1,992/2,000,
  so per-respondent `(gid,off)` ordering cannot remove cross-respondent churn.

## One measured TEST_ONLY candidate — NOT IMPLEMENTED

`followthrough_r2/locality_probe.py` labels itself
**`EXPERIMENT_NOT_IMPLEMENTED`**.  It patches only the module-global `sorted`
lookup in `_pre553_query_eval` so native respondent traversal follows the
session's physical insertion order.  Every integrity/root/current/predicate/
risk/fact/replay owner remains the accepted code; no production file changed.

On the same reviewer-retained releases, exact fact, projection, replay and
release refs are equal:

| case | query | baseline | candidate | factor |
|---|---|---:|---:|---:|
| 100k | selected | 580.548 s / 204,125 reads | 265.680 s / 5,784 reads | 2.19x |
| 10k | selected | 49.066 s / 20,157 | 21.812 s / 588 | 2.25x |
| 10k | reverse F2 | 51.790 s / 20,153 | 21.116 s / 614 | 2.45x |
| 10k | 3-way F4 | 56.624 s / 20,161 | 24.665 s / 588 | 2.30x |
| 1k | selected | 4.390 s / 1,784 | 2.046 s / 61 | 2.15x |

The 100k candidate still spends about 247.8 CPU s in native object/predicate
evaluation and 1.3 GB temp SQLite; the read churn is removed, not the whole
vertical.  Candidate tree RSS is 2.81 GiB versus 2.95 GiB baseline.  This is a
candidate for a narrow S2-C/D handoff **after** the qualified S2-A native
body-truth descendant; it is not optimized-engine acceptance, owner approval
or G5.

The one smallest writer proposal is a per-build memo of the already-computed
immutable semantic projection/hash reused by validation and insertion, without
removing any check, source/I02 root, omission/body/locator proof or current/
authority check.  It is **not implemented**.  Removing the second full reread/
re-encode proof is a separate versioned proof/identity policy change and is
not proposed here.

## Deliberately not proposed here

- No removal of the direct I02 proof, reread/re-encode proof, body_json or any
  integrity check.
- No new Arrow IPC/DuckDB/SQLite primary store, query engine, codec or
  persistent cache authority.
- No #997 source bridge, #998 joined vertical, #1001 full 100k/6 GiB court,
  #1007 source rights or #999 native repair.
- No production edit, owner acceptance, SLA or architecture campaign.

## Verdict

`REVISE_EXACT_DEFECT_RECONCILED` / measured locality candidate available;
`CONDITIONAL_S2CD_HANDOFF_PENDING_QUALIFIED_S2A_NATIVE_BODY_TRUTH`.
No production repair was attempted.
