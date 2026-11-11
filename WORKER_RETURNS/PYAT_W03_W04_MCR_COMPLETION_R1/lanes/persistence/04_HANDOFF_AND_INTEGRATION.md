# Persistence lane handoff

## Delivered

- `W04-COLD-PERSIST-REOPEN`: canonical carrier fsync/atomic publish and existing
  cold-reopen I03/I05 tests preserved.
- `W04-GOVERNED-DEFAULT`: explicit host policy activation, private root and
  sourcefree permission gate, retention budget.
- `W04-AUTHORITY-INVALIDATION`: cache envelope binding to source, projection,
  authority, release, replay, schema and trusted policy root; safe misses.
- `W04-ATOMIC-LIFECYCLE`: staged/fsynced/atomic cache and canonical publication;
  interrupted publication and delete/rebuild tests.
- `W34-PRODUCT-BOUNDARIES`: canonical Parquet carrier remains distinct and
  survives accelerator deletion; no second store/query engine.

## Cross-lane integration still required

- W03 cold high-water and selected-cell/canonical-hash lanes remain owned by the
  cold/bench lanes; their measurements and changes are not claimed here.
- The full 12-ID MCR-C contract remains incomplete until HQ integration,
  independent code review and independent economic review at one immutable
  candidate head.
- A real deployment host must still supply an authorized policy root and
  retention budget. The sourcefree pytest temp root used in this lane is not a
  deployment grant.
- No original35, SAV/DTA/DB, source bytes, native/science/actor, FF/N11/Sorok,
  protected merge or peer/HQ artifact was touched.

## Rollback

The accelerator is derived. An operator may delete the policy root cache files
or disable/remove the policy; canonical `ParquetC11Carrier` releases and their
I03/I05 consumers remain. The code changes are confined to the two listed
production files, one new helper and one new focused test file; no facade/ingest/
repository/benchmark ABI was changed.

## Receiving boundary

Author status is `DELIVERED_PENDING_RECEIVING`. This lane does not claim whole
W03/W04 or whole MCR completion, protected adoption, economic PASS or final
acceptance. A separate qualified receiver must evaluate the immutable candidate
and cross-lane integration.
