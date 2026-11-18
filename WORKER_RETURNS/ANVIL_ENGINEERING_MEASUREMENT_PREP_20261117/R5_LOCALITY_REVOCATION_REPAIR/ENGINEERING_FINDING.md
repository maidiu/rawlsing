# R5 ENGINEERING FINDING — PER-YIELD CURRENT GUARD RESTORES THE LOCALITY PROFILE

**Source:** product `347baec...`; cut1 G5 `092bf29...`; reviewer `07c2409...`; sealed R2 estate `c209d3a...`; contract `e928ebd...`; `pre553_direct_estate_i03.py` blob `8825832f...`. Product READONLY.

## Finding

The R4 locality mechanism was valid but the test-only adapter omitted `self._require_live()` between buffered yields. R5 adds one guard immediately before every yield. RED/GREEN on the sealed estate:

- R4 after first yield + revoke: second routing fact yielded, no error.
- R5 after first yield + revoke: `DirectEstateError: current source/operation authority refused`.
- Original product: same refusal.
- Live valid iteration: 600 routing refs, canonical sorted, exact original order; original method restored in `finally`.

Locality observation survives: row-group reads 3,965 → 50; rows 2,012,160 → 25,472; compressed bytes 634,219,540 → 7,942,218; uncompressed 6,011,490,388 → 76,150,826; profiled Q 18.296 → 7.583 s; full parity exact. One query, cProfile overhead, no production speedup.

## Reusable lesson

Buffering for canonical-order restoration changes generator exception timing and can bypass per-yield CURRENT unless the guard is repeated inside the yield loop. Any production adoption must carry both canonical-order restoration and `_require_live()` before every yield.

## Counterevidence / limits

- `family_object_materializations` counter is 0 due adapter import blind spot; cProfile records 9,637 reconstruction calls (9,600 routing + 37 event), disclosed.
- Per-respondent buffer 600 routing facts; not full estate.
- Streaming exception timing for malformed later rows differs because materialization precedes first yield; not separately executed.
- One sourcefree f4 query; no native/100k/science/actor/current/protected grant.

## Owner handoff

`rawlsing_next/pre553_direct_estate_i03.py::DirectEstateI03Session._respondent_family`; owner-granted physical gid/off traversal, canonical ref-order restoration, `_require_live()` before every yield, revocation-after-first-yield and full parity tests. S2-C direct-reader + native I03 evaluator owner. Grant `REQUESTED_NOT_GRANTED` (#1006 comment6969187403); product READONLY.
