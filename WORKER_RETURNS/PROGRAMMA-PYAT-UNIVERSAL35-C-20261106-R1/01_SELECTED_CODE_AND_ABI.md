# Selected code vs donor/current and frozen ABI

## Donor/current fate

| Item | Current base `d119045…` | Selected `30bd02a…` | Fate |
|---|---|---|---|
| `_pre553_c11_execution_view.py` | blob `de561330…`, uncompressed chunk arrays | blob `986f327…`, exact donor `02c1200…` blob | REUSE exact accepted body |
| compact view test | blob `ac59e38…` | blob `e6c0023…` | donor test plus author multi-shape coverage |
| P2 grouped I03 | already received `409be32…` | unchanged | NO_BUILD / preserve |
| capacity guard | already received `9a5cfd…` | unchanged | NO_BUILD / preserve |
| #702 / current L01/L02 code | present | unchanged | preserve; no overwrite |
| global/home default cache | absent | absent | preserve explicit caller-only policy |

The selected production view file is byte-identical to the independently accepted donor view. The test file deliberately differs by adding current-base multi-shape coverage; it is not claimed as independently reviewed donor text.

## Private ABI (unchanged public callers)

- `_compact_public_objects(release, *, physical_binding, projection_binding) -> _CompactPublicObjects | None`
  - Input: sealed `C11LogicalRelease`, exact physical binding callable, projection binding identity.
  - Output: unchanged selector/event/non-event view, now backed by bounded `_CompressedBodies` when compressed in memory.
- `_CompressedBodies.body_bytes(row: int) -> bytes`
  - Exact canonical event JSON bytes for the selected row; raises `IndexError` outside the bounded lane/chunk.
- `_EventLane.materialize(row) -> RespondentEvent`
  - Same event materialization and exact refs.
- Cache schema remains `PRE553_I02_EVENT_ACCELERATOR@1`; env remains `RAWLSING_C11_ACCELERATOR_DIR`; no new default root.
- Event chunk bound: `256` events; codec: Zstd; cache file remains the existing raw-body Parquet/Zstd format, so old cache files are still readable and re-chunked.
- No signature, schema, object identity, authority, risk, weight, fact, or replay ABI changes. `execute_i03`, Route B, issued workload, I05/Batch, and P41 callers are unchanged.

## Current first consumer

`CarrierNeutralResearchExecutor.execute_i03` at `rawlsing_next/pre553_carrier_execution.py:430`; Route B at `pre553_route_b_production.py:495`; issued workload at `pre553_issued_workload.py:280`; test-only source adapter at `pre553_native_workload_binding.py:423`.

## Selection decision

- Compressed-body code: `REUSE_ADAPT` exact accepted donor on current base; no new compression design.
- P2/capacity: `PRESENT_COMPOSED_NO_BUILD` on current base.
- Multi-shape author test: `TEST_QUALIFY`; sourcefree only.
- Real-source performance: `HOLD` for A/D current adapters; not replaced by synthetic measurements.
- No second engine, no default persistent cache, no semantic or source-specific branch.
