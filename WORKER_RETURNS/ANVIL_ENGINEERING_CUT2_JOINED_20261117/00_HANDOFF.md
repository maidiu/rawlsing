# ANVIL CUT2 — joined sourcefree qualification

## Status

**`EXACT_JOINED_DEFECT_OR_OWNER_SEAM`**

- Branch: `agent/anvil-engineering-cut1-20261117-r1`
- Worktree: `/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER`
- Current code/test descendant: `a13d69cf5636de5541660cd60115f8b61d66261b`
- Candidate: `347baec696c8b395d750ac3b9e74417a6490c223`
- Cut1 G5: `092bf29ffa6724d477abb4ccfc770e3bc492250d` /
  `ACCEPT_SCOPED_PREPARED_SAVED_BATCH_CUT1`
- Product/code/test edits this turn: **NONE**
- Protected/source/science/current/issuer/merge: **NONE**

## Targeted courts — 38 PASS

Command:

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  --basetemp=WORKER_RETURNS/ANVIL_ENGINEERING_CUT2_JOINED_20261117/tmp/pytest \
  rawlsing_next/tests/test_pyat997_r03_governed_query_issuer_v2.py \
  rawlsing_next/tests/test_pyat997_s1e_source_saved_body_bridge.py \
  rawlsing_next/tests/test_pyat919_s2e_a_whole_native_batch.py \
  rawlsing_next/tests/test_universal_world_binding.py
```

**38 passed, 0 failed, 0 errors, 0 skipped, exit 0, 300.69 s.**

- R03 v2 issuer: 8
- source/saved body bridge: 6
- S2E native Batch: 6
- universal world binding: 18

Logs: `evidence/targeted_courts.txt`,
`evidence/node_inventory.txt`.

This is a new relative-cut1 court; the earlier 70-node cut1 matrix was not
repeated for confidence.

## Actual base joined path — PASS

Return-local witness `evidence/joined_probe.py` uses the existing sourcefree Q2
fixture through `s1e._full`, the actual R03 v2 issued workload, the exact base
`SavedC11Admission`, actual `execute_saved_batch`, and the genuine
`join_saved_source_operation_fates`.

- Admission class: **`SavedC11Admission`**
- Compiler: v1 **0 QUERY / 1 DISCOVERY**
- R03 v2 TEST_ONLY issuance: **12 QUERY / 1 DISCOVERY**
- Batch: **13 COMPLETED units**
- Prepared index builds in the prepared case: **1**
- Join hash: `e074010a80157b71c2b28ffdec419efe3b3406a8384ad1476bc3ff92a5cbfbba`
- Operations: **22**
- Fates: **8 ELIGIBLE / 14 HELD**
- Positive native-linked operations: **6**
- Discovery candidates exactly joined: **8**
- Pending eligible operations: **2**
- Issue grants created: **0**
- Preconsumer handoff unchanged: **true**

Source/estate pins:

- source SHA:
  `7303078bbf946831004807be306b1a24d6b3d686b9765934d01313ae4cce566c`
- manifest SHA:
  `62289c3aa41f90af5b3455e0e4ecd9c41847891bc3791c9e0bb8f011d80dbc9b`
- roots and replay are in `evidence/joined_probe.json`.

## Prepared path through actual caller — exact GAP

When the same persisted estate is reopened as:

**`PreparedSavedC11Admission`**

the cut1 wrapper accepts it and executes the actual 13-unit Batch with **one**
prepared index build and **13 COMPLETED** receipts. This is the accepted cut1
path.

However, the genuine postconsumer join:

```text
rawlsing_next/pre553_source_postconsumer_receipts.py
join_saved_source_operation_fates
line 272
if type(admission) is not SavedC11Admission:
```

returns:

```text
EXACT_ACCEPTED_PRODUCER_AND_NATIVE_TYPES_REQUIRED
```

The prepared Batch itself is valid; the **postconsumer join has not yet
accepted the exact prepared subclass**. This is the next owner seam, not a
failure of the cut1 Batch feature.

Observed case matrix:

| Stage | Admission | Result |
|---|---|---|
| actual R03 v2 issuer + saved Batch + postconsumer | `SavedC11Admission` | **PASS** |
| same actual issued Batch through cut1 prepared wrapper | `PreparedSavedC11Admission` | **13 COMPLETED, one build** |
| same prepared admission into postconsumer join | `PreparedSavedC11Admission` | **typed GAP** |

## Exact next owner handoff

- File: `rawlsing_next/pre553_source_postconsumer_receipts.py`
- Function: `join_saved_source_operation_fates`
- Current condition: `type(admission) is not SavedC11Admission`
- Current owner: S1-E/postconsumer receipt owner
- Minimum grant: exact `PreparedSavedC11Admission` whitelist in that join,
  preserving unchanged compiler/workload/receipt/fate/current checks.
- No product edit is made in this turn; no owner request is inferred.
- No new QUERY issuance, source/science authority, production CURRENT, or
  original35 permission is created.

## Cold/fresh, change/restore, refusals

Covered by the targeted 38:

- universal world-binding **cold subprocess replay** and **fresh P41** paths;
- actual same-source partial resume to P41;
- source/saved body bridge changed source cell and exact restore;
- wrong pinned root and revoked CURRENT refusals;
- R03 v2 actual saved Batch no source reopen;
- v1 postconsumer guards reject v2 query injection;
- v2 changed bindings and unissued manifest query refusals;
- S2E F1/F4/I05 native Batch and conservation negatives;
- no fabricated eligibility or QUERY issuance.

The base joined witness and the prepared GAP are separate classes in the
receipt; legacy `SavedC11Admission` success is not presented as prepared
integration.

## Bounded resource observation

`evidence/joined_probe_resource.time`:

- wall **2.59 s**
- user **3.16 s**, sys **0.45 s**
- parent max RSS **124,575,744 B**
- one process; no subprocess
- staging memory: **NOT_MEASURED**
- 13 Batch receipts / one prepared index build in the probe
- 100k/6 GiB: **NOT_RUN**

This is a small TEST_ONLY fixture, not real-width economics.

## Limits

- No original35/source/respondent/science, production CURRENT, issuer, actor,
  protected merge, or #998/#1009 integration claim.
- No 100k/6 GiB.
- No full K3/202 matrix; only the 38 targeted nodes plus the exact base/prepared
  joined witness.
- R3 independent archive and prior returns remain unchanged.

## Stop

**`EXACT_JOINED_DEFECT_OR_OWNER_SEAM`**

Base legacy joined path is scoped PASS. Prepared cut1 Batch is scoped PASS.
Prepared postconsumer join is the exact next owner seam. No self-acceptance,
no product patch, no protected/source/science/current grant. STOP for HQ and
the rightful S1-E/postconsumer owner.
