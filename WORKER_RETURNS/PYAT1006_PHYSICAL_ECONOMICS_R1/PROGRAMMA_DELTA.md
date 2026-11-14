# PROGRAMMA DELTA — PYAT #1006 measured physical/query economics

## Change class

HARNESS + TEST + RETURN FILES ONLY.  No `rawlsing_next` production or accepted
test file was edited, replaced, cherry-picked or merged.  No new architecture,
engine, authority store, codec, controller, timer or production producer was
created.  The only new writer/test/return files are under
`WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/`.

## What the baseline establishes

1. The accepted S2-C writer and S2-D cold I03/I05/Batch/normal/resume readers
   can consume one complete sourcefree 13-family release with exact native
   fact/replay parity at a qualified small oracle and exact old-root restore.
2. At 100k distinct respondents the complete 13-family writer finished on this
   host within the 6 GiB process-tree cap: 3,033.723 s writer, 295,211,008 B
   writer tree RSS, 310,163,264 B retained Parquet, 5,257,841,984 B observed
   staging peak, 4,385,796,096 B temporary I02 proof SQLite.
3. The same 100k release is not economically queryable at the measured
   workload: cold admission 1.520 s and session build 33.508 s are modest, but
   one selected I03 is 562.362 s, reverse F2 873.655 s, and the genuine
   same-respondent 3-way F4 is 908.507 s.  Query process-tree peak is
   3,690,455,040 B, still below 6 GiB.
4. The dominant writer cost is the direct I02 semantic/identity/SQLite proof
   (2,249.700 s, 74.2% of write), with the post-write full reread/re-encode
   proof at 761.224 s (25.1%) and `_row`/body_json 492.834 s overlapping both.
   Root hashing is only 11.101 s.
5. The dominant query cost is not the 33.508 s posting-index build.  A 1k
   profile puts most of a selected query in per-respondent family reads:
   `_ColdFamilyRows.__getitem__` -> `_respondent_family` repeatedly reads
   Parquet row groups in `ORDER BY ref`, which is not row-group order, so the
   single-row-group cache thrashes.  This is O(N) per query and explains the
   near-linear selected-query growth (1k 4.945 s, 10k 51.069 s, 50k 297.986 s,
   100k 562.362 s) despite a bounded cold session.

## One smallest owner-consistent proposal — NOT IMPLEMENTED

**Target:** `rawlsing_next/pre553_direct_estate_i03.py::_respondent_family`
(the same bounded-family read helper used for coordinate, routing and weight
rows).  The SQL cursor currently orders member rows by `ref`; those refs are
hash-ordered, not `(gid, off)`-ordered, so the one-row-group cache is evicted
on nearly every respondent.

**Proposal:** under an explicit narrow S2-C/S2-D owner lease, make the
family-row read row-group coherent — e.g. select the existing `members` rows
ordered by `(gid, off)` for the physical read (and, if the native consumer
requires canonical ref order, sort the already-bounded per-respondent result
by ref before yielding), or replace the single-row-group cache with a small
bounded LRU of row groups keyed by `gid`.  Preserve every exact membership,
value, state, routing, occurrence, denominator, fact and replay identity; do
not skip integrity checks and do not introduce a new persistent index.

**Why this is the one proposal:** it is a local, tested-shape-driven read-order
fix at the measured dominant query boundary.  It does not change writer
semantics, source authority, I02 proof, native science or the physical schema.
It must be implemented on a new descendant only after HQ grants the narrow
S2-C/D handoff, then re-run the exact small oracle, changed/restore, hostile
and 100k query courts plus independent G5.  This return does not edit it.

## Deliberately not proposed here

- No removal of the direct I02 proof or the reread/re-encode parity proof.
- No new Arrow IPC/DuckDB/SQLite primary store, query engine or codec.
- No change to the accepted writer schema, body_json preservation or root
  hashing policy.
- No attempt to make #997's source bridge, #998's joined vertical, #1001's
  100k/6 GiB whole-vertical court or #1007's source rights.

## Verdict

`BASELINE_MEASURED_MATERIAL_QUERY_COST_FAILURE`;
`STOP_PENDING_EXPLICIT_S2CD_HANDOFF`.  No production repair was attempted.
