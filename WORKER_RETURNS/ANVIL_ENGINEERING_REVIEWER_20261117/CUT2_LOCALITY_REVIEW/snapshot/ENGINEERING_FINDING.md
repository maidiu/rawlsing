# R4 ENGINEERING FINDING — PHYSICAL GID/OFF TRAVERSAL REMOVES ROW-GROUP THRASH

**Source:** product `347baec...`; cut1 G5 `092bf29...`; sealed R2 estate manifest `c209d3a...`; contract `R2_PILOT/fixture_contract_pilot.json` `e928ebd...`; `pre553_direct_estate_i03.py` blob `8825832f...`; `_pre553_query_eval.py` and `pre553_parquet_carrier.py` unchanged.  
**Scope:** sourcefree TEST_ONLY, one query, one locality condition. No product edit.

## Finding

Changing only the test-only member traversal from `ORDER BY ref` to physical `ORDER BY gid,off`, then restoring canonical ref order before yield, reduced:

- row-group reads 3,965 → 50;
- row-group rows 2,012,160 → 25,472;
- compressed read bytes 634,219,540 → 7,942,218;
- uncompressed read bytes 6,011,490,388 → 76,150,826;
- profiled Q wall 18.296 → 7.690 s (cProfile/wrapper context).

All full semantic/identity/refs/member/replay digests stayed exact; object reconstruction remained 9,637 calls (9,600 routing + 37 events). The residual cost is now exact object construction/validation/canonical hash, not row-group thrash.

## Reusable lesson

The one-row-group cache is effective only when member order follows physical row groups. Ref-key order gives semantic stability but thrashes the cache. A test-only adapter can read gid/off and restore canonical order before yield; production adoption needs owner proof that every consumer tolerates the restored order and that exact validation/parity remain.

## Counterevidence / limits

- cProfile overhead; not a production speedup.
- One f4 query, 16R/600Q sourcefree geometry; not all queries, not native/100k.
- The test adapter bypassed the instrumentation's family-object wrapper (counter 0); cProfile count 9,637 is the actual reconstruction count. Row-group counters are valid.
- No validation/hash/current/ordering weakening; no new store/engine.
- Production method remains READONLY; owner grant absent.

## Handoff

`rawlsing_next/pre553_direct_estate_i03.py:398 DirectEstateI03Session._respondent_family`: owner-granted physical `gid,off` member order plus canonical ref-order restoration, or a verified equivalent cache. S2-C direct-reader + native I03 evaluator owner. If ordering cannot be proven for all consumers, hold instead of changing it.
