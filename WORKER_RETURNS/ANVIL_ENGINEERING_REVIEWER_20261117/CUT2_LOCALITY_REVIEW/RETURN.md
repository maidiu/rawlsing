# ANVIL CUT2 R4 locality experiment — independent review

## Verdict

**`REVISE_EXACT_DEFECT`**

Target: `1cc507614496d79c4c546b066da17adf7175e328`
R4_LOCALITY_EXPERIMENT. Product remains `347baec...` / `a13d69c...`; cut1 G5
`092bf29...` remains accepted and untouched.

The **locality mechanism** is supported as one sourcefree instrumented
observation: physical `gid,off` traversal reduced row-group reads 3,965 → 50,
profile Q wall 18.296 → 7.690 s, with exact full semantic/identity/refs/member/
replay parity. This is **not a production speedup**.

The **test-only adapter is not production-ready**: it buffers objects before
yielding and never rechecks CURRENT between yields. A CURRENT revocation after
the first yielded object was bypassed for the second object.

## Exact defect

`locality_adapter.py::physical_order_respondent_family`:

1. materializes every selected row;
2. sorts by canonical ref key;
3. yields the sorted objects without `self._require_live()` per yield.

Observed against the sealed R2 estate, RoutingEligibilityFact family:

- first object yielded;
- CURRENT revoked;
- **second object yielded with no error**;
- original `DirectEstateI03Session._respondent_family` checks `_require_live()`
  per row and **refused** the same state with:
  `DirectEstateError: current source/operation authority refused`.

This is a material current-boundary bypass in the test-only adapter. If adopted
as production behavior it would be a SEV-0; at this test-only experiment grade it
is a **SEV-1 adapter defect**.

Smallest required correction:

```python
for obj in sorted(materialized, key=lambda item: item.ref.key):
    self._require_live()
    yield obj
```

Add a focused revocation-after-first-yield regression; re-run the one locality
observation and exact parity. Product adoption still requires the #1006 owner
grant and an owner-approved `_respondent_family` change.

## Verified locality observation

From target `RESULT.json`, `child_result.json`, `raw.prof`, and call tree:

- row-group reads: **3,965 → 50**
- row-group rows: 2,012,160 → 25,472
- compressed read: 634,219,540 → 7,942,218 B
- uncompressed read: 6,011,490,388 → 76,150,826 B
- profile Q wall: **18.296033755 → 7.690256591 s**
- full parity: identity/semantic/refs/member/replay **exact true**
- cProfile `_object_from_row`: **9,637** calls; raw adapter family-materialization
  counter is 0 because the adapter imports `_object_from_row` directly. The
  cProfile call tree substantiates the real reconstruction count.
- external supervision: exit 0, no abort, wall 11.932816951 s, sampled RSS
  128,036,864 B, sampled scratch 30,368,896 B, 42 samples; caps 120 s/2 GiB/2 GiB.

These are one instrumented query (`f4_three_raw`) on the sealed 16R/600Q
sourcefree estate. No 1/10/100, fresh Batch, native, 100k, original35, source,
science, actor, CURRENT, or production claim.

## Manifest / product identity

- R4 `MANIFEST.json`: **17** files; all SHA-256 hashes verified.
- Product source pins unchanged: `pre553_direct_estate_i03.py`
  `8825832f...`, `pre553_prepared_saved_i03.py` `bcb146ed...`,
  `pre553_parquet_carrier.py` `9dad6713...`; product candidate `347baec...`.
- R2 contract `e928ebd17016...`; estate manifest `c209d3a198...`.
- No product file edit; no new store/index/evaluator/schema/science/issuer.

## Ordering / memory / exception observations

- The adapter restores canonical ref order before yielding; the complete-query
  parity is exact.
- The materialized list is bounded per respondent/family (600 routing facts in
  this witness), not full-estate memory. No full-estate boundedness is claimed.
- Buffering changes generator exception timing: a later malformed row raises
  before the first yield, whereas the original can yield earlier objects. This
  is a code-level streaming difference and is not separately executed.
- Duplicate/ref/order/body/respondent/universe validation in the adapter is the
  same shape as the original; the defect is the missing per-yield CURRENT check.

## Owner handoff

Requested: `#1006` comment `6969187403` — **REQUESTED, NOT GRANTED**.
Product `rawlsing_next/pre553_direct_estate_i03.py::
DirectEstateI03Session._respondent_family` remains READONLY. The reusable
production correction is owner-granted physical gid/off traversal with canonical
ref-order restoration and `_require_live()` before every yield, plus the
revocation/parity regression. The reviewer did not repair product or the
author's adapter.

## Grades / limits

- Engineering: experiment supports the locality mechanism at one-query test-only
  grade; adapter fails the CURRENT-between-yields requirement.
- Scientific: no original35/native/science acceptance.
- Authority: no source/current/host/issuer/protected grant.
- Integration: UNMERGED.
- No 100k/6 GiB; no production speedup.

## Artifact

`REVIEW_VERDICT.json`, `RECOMPUTED_LOCALITY.json`, `SOURCE_CHECKS.tsv`,
`revocation_witness.py`, `evidence/locality_revocation_witness.json/.out`,
`snapshot/` frozen R4 payload, `commands.txt`, `MANIFEST.sha256`.
