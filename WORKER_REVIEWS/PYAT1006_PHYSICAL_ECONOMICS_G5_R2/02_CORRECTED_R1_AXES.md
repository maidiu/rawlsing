# Corrected R1 disposition axes

Historical R1 review remains `0169fac9f3840800796c664eee462bbb8984bb42`
(`REVISE_EXACT_DEFECT`).  This is the finite follow-through recheck of its three
named report defects.

## Axis 1 — causal claim and proposed fix

**R1 finding:** `_respondent_family` reading member rows `ORDER BY ref` with a
single row-group cache was the dominant cause; a per-respondent `(gid,off)`
ordering or small LRU was proposed.

**R2 disposition: CORRECTED.**

- Author `CORRECTION_RECONCILIATION.md` and top-level `00_RETURN.md` withdraw
  the old cause and state the actual cause: native respondent traversal in
  ref-key order across physically ordered row groups, plus a separate event-row
  cache.
- R1 counter evidence remains independently verified: 10k routing reads 10,043
  hash-order versus 258 physical-order; 100k selected baseline 101,438 routing
  reads and 100,050 event reads with zero consecutive-gid cache hits.
- R2 candidate confirms: 100k selected reads fall from 204,125 to 5,784; events
  fall to one read per 634 gids, routing to 2,513 reads over 977 gids (2.57 per
  gid).  Within-respondent ordering is unchanged.
- The old proposal is explicitly not implemented and not accepted.

## Axis 2 — test count

**R1 finding:** claimed 36 S2-D tests for the named five-file group; exact
RUNBOOK command reproduced 29.

**R2 disposition: CORRECTED.**

- Author `test_counts_reconciliation.json` and reconciliation text now state:
  five-file group **29**, separate partial-binding **2** (29+2=31), focused
  **31**, own fixture **6**, follow-through **2**.  The “36” selection is
  withdrawn.
- R1 independently ran 29 and 2; R2 logs preserve the same counts.  No raw log
  was rewritten.

## Axis 3 — RSS labels

**R1 finding:** 1k/10k “writer process-tree RSS” rows were whole shape-worker
peaks, not writer-only.

**R2 disposition: CORRECTED.**

- Author report now labels the 1k/10k values as whole-worker peaks and records
  writer-only 1k `194,072,576 B`; 50k/100k were already writer-only.
- R1 independently measured writer-only 10k `214,261,760 B` versus the old
  whole-worker table value `1,394,810,880 B`; R1 writer-only 1k was
  `216,109,056 B` (different monitor/run, same correction).
- The correction does not change any cost verdict.

## Preserved R1 axes

The independently reproduced R1 axes are not reopened: 43/43 author manifest
identity, 100k distinct respondents / 324,477 events / 2,841 row groups, 100k
writer 2,943.177 s, staging 5,209,185,593 B, retained 310,178,695 B, cold
admission 1.669 s, selected baseline 543.026 s, 13-family/typed-absence census,
representative native oracle, changed/restore and guard suites.  The 50-minute
100k writer and the old test estate were deliberately not rerun.
