# PYAT W03/W04 MCR-C — cold lane implementation

**Lane status: DELIVERED_PENDING_RECEIVING. Whole W03/W04 is NOT complete.**

- Branch: `agent/pyat-w03-w04-mcr-cold-r2`
- Base/anchor: `1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc`
- Frozen PR895: `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`
- Implementation commit: `6d3e7439d9001e0b87cd3dbd2450ce811fa41469`
- Owned obligations: W03-COLD-HIGHWATER, W03-SELECTED-CELLS-CANON,
  W03-SEMANTIC-TOPOLOGY, W03-FIRST-CONSUMERS.

## Exact implementation

The cold path is selected by `build_source_backed_c11_repository(..., cold=True)`
or automatically for an `ExactPhysicalCellStream` when no
`RAWLSING_C11_ACCELERATOR_DIR` disk root is configured.  The eager path remains
available with `cold=False` or when a disk accelerator root is configured.

Changed files:

- `rawlsing_next/pre553_source_backed_c11_facade.py`
  - added `build_cold_source_backed_c11_release`;
  - added row-invariant response/coordinate/weight rule maps (no per-cell dict
    rebuild);
  - added bytearray duplicate/completeness tracking instead of one Python set
    of boxed row integers per selected slot;
  - added exact event material caching and one-pass event template construction;
  - `build_source_backed_c11_repository` gains additive `cold: bool | None`.
- `rawlsing_next/pre553_c11_ingest.py`
  - additive optional `event_refs` overrides on the internal projection-hash,
    closure-ref, replay-manifest and replay-validation helpers.  Default
    behavior is byte-identical.
- `rawlsing_next/_pre553_w03_cold_compact.py` (new)
  - streams exact events into the existing private `_CompactPublicObjects`
    selector/compressed-body lane.  It is a physical compaction helper, not a
    second C11 store, query engine or semantic authority.
- `rawlsing_next/tests/test_pre553_w03_w04_cold.py` (new)
  - exact cold/eager parity, compact-lane materialization, repeated/ordered/
    zero/missing topology, weight-missing/valid-empty, and refusal tests.

Untouched by this lane: `_pre553_c11_execution_view.py`,
`pre553_parquet_carrier.py`, and `pre553_c11_repository.py`.

## Why the cold peak improves

The previous path built every eager `RespondentEvent` in a tuple, validated the
full tuple, then built a second compact selector/body lane.  The cold path:

1. constructs one exact event from precomputed governed material;
2. verifies its exact semantic projection once;
3. validates its authority/topology/scope/occurrence identity;
4. extracts its selector and canonical body;
5. drops the event before the next cell.

The release still contains the exact same release ref, replay manifest,
public-object refs/`as_dict`, internal records and M01–M18 coverage.  The first
I03/I05 consumers use the existing compact lane; no consumer ABI changed.

## Evidence

- `01_STAGE_COST.json` — paired development profiles at 2k/5k/10k rows.
  At 10k rows / 60k events: eager **622.8 MiB** vs cold **521.5 MiB**
  (**16.3% lower** median process peak RSS), wall **80.63s → 72.17s**
  (**10.5% lower**).  These are development profiles, not the frozen 100k
  bench matrix.
- `02_TEST_RECEIPTS.json` — `43 passed` sourcefree court and `62 passed`
  focused cold/topology/consumer suite.
- `03_CHANGED_BLOBS.txt` — exact implementation blobs.
- `proof_43_sourcefree_junit.xml`, `proof_focused_tests.txt`.

## Remaining cross-lane integration

1. **Benchmark lane:** run the frozen `--scenario cold,cells-and-hash,
   full-matrix --profiles narrow,wide,repeat --rows 100000 --repetitions 3`
   matrix with `cold=True` (or no disk accelerator root) against the frozen
   protected baseline and the integrated candidate.  This lane does not claim
   the final 100k PASS.
2. **Persistence lane:** the disk accelerator path still uses the eager/compact
   path; ensure governed default/root/invalidation/atomic tests cover that path.
3. **HQ:** combine this cold implementation with persistence and benchmark
   lanes at one immutable integrated head; all 12 obligations remain HQ-owned.
4. **Independent receiving:** separate code and economic review at the final
   immutable head; this lane does not self-accept.

## Boundary

Sourcefree S2 only. No original35/SAV/DTA/DB/source bytes, no source workload,
rights, science, actor, FF/N11/Sorok authority, no protected merge, no second
canonical store, no query engine, no `NativeSourcePackage` mandate.
