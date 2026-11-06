# R2 — projected DTA and zero-row frame repair

**FINDING:** The independent review's two defects are repaired in the existing new module. DTA selected reads now use the existing content-bound `/dev/fd` snapshot with windowed `read_dta(row_offset, row_limit, usecols=...)`, not `read_file_in_chunks` on the snapshot. Zero-row frame projection now initializes `row_ordinal=0` and returns an exact empty stream instead of `UnboundLocalError`.

**INTERPRETATION:** SAV physical parity/economy and NativePackage parity from r1 are preserved. DTA projection is now operational on a sourcefree DTA fixture; no original DTA source was opened. The fix does not change decoder semantics, source identity/custody, full-grid behavior, or any A/D/facade code.

**ACTION:** HQ can route the frozen `7a404b0d…` head to independent G for exact frozen repair closure. No new A/D/native/all35 claim.

**OWNER:** Independent G for review closure; HQ for receiving; A/D remain owners of source mapping and native consumer behavior.

## Exact code identity

- Branch: `codex/pyat-universal35-physical-stream-20261106-r1`
- Base: `d129eebdb0472b0c3625efa281826a858bd0a384`
- Prior reviewed target: `89a41589c7541f625c6d2f9346436629d374b93e`
- R2 code head: `7a404b0dcaac0e4dd027b9edb98c9038d89dbd9a`
- Files changed only: `rawlsing_next/pre553_original35_physical_stream.py`, its matching test.
- No decoder/facade/factory/admission/A/B/D/E/guide/controller/shared permission edits.

## DTA repair

- Selected DTA path: `snapshot.rewind()` -> `pyreadstat.read_dta(snapshot.reader_path, usecols=selected, row_offset=..., row_limit=rows_per_chunk, ...)` -> bounded selected frame -> exact cells.
- No mutable original path reopened; no full-source persistent copy; no giant frame.
- Each window `snapshot.check_stable()`, final `snapshot.verify()`, full declared `row_count` and source SHA preserved.
- Exact decoder `_physical_value` / `classify_physical_value` and `PhysicalVariable` metadata/labels reused; no raw-type or missing-state coercion.
- `read_file_in_chunks` remains for SAV; DTA no longer relies on it.

## Zero-row repair

- `_selected_frame_cells` initializes `row_ordinal=0`.
- Zero-row frame returns empty selected/full streams with `row_count=0`; no unbound variable.
- Existing full-grid and SAV checks unchanged.

## Tests and limitations

- Adapter tests: **7 passed** (adds DTA multi-window/full-decode parity and zero-row frame).
- Focused suite: **37 passed**.
- DTA sourcefree fixture only; SRC27–SRC30 original DTA **NOT_RUN**.
- SRC13 latin1 full-frame decode, A-owned unbound mapping, D 600 s end-to-end, native/all35 and 16-GiB tests remain separate **NOT_RUN**.
- No native/scientific authority or protected merge.

## PROGRAMMA_DELTA

| Field | Value |
|---|---|
| Identity | Sourcefree selected-reader repair at `7a404b0d…`, prior target `89a41589…`. |
| Function | Exact bounded selected-column physical-cell stream for SAV and DTA over an already permitted `PhysicalSourceIncidence`. |
| Input -> output | permitted incidence + unique selected columns -> `ExactPhysicalCellStream` with full row_count/source SHA/metadata digest; selected cells only; typed refusals. |
| Root/schema | caller-owned incidence; no source root in module; existing `ExactPhysicalCellStream` contract. |
| First consumer | current C11 factory full-grid; D `execute_native_compiler_source` / NativePackage selected input. |
| Evidence | 7 adapter PASS, 37 focused PASS; DTA sourcefree exact parity; zero-row empty; SAV r1 parity/economy retained. |
| Next | independent G review of `7a404b0d…`; then D/A end-to-end dependencies. |

No second engine, index, canonical copy, global cache, or authority grant.
