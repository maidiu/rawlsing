# R2 repair and parity evidence

## Observed change

`rawlsing_next/pre553_original35_physical_stream.py` changed only in the selected-reader module:

- `_selected_frame_cells` initializes `row_ordinal = 0`, so a zero-row frame returns empty instead of an unbound-local error.
- `_selected_chunk_cells` keeps SAV on the unchanged `read_file_in_chunks` branch.
- DTA now rewinds the same content-bound snapshot per window and calls `pyreadstat.read_dta(snapshot.reader_path, usecols=..., row_offset=..., row_limit=...)`.
- Each DTA window checks snapshot stability and selected-column set before emitting; final row count and snapshot SHA are checked.
- No decoder, facade, factory, admission, A/B/D/E, guide, progress, controller, or protected code changed.

## Old-cut reproduction

Running the frozen `89a41589…` module against a valid sourcefree DTA fixture gave:

`ReadstatError: Unable to read from file`

This reproduces the prior REVISE finding at the old selected DTA boundary.

## New-cut DTA probe

Valid sourcefree DTA: 7 rows, columns `A`, `B`, `C`; selected `A,B`; missing values in `A` and `B`; source SHA matched.

| Window rows | Selected cells | Exact vs full decode | Two-pass replay | Row ordinals | States observed |
|---:|---:|---|---|---|---|
| 1 | 14 | yes | yes | 1–7 | observed + system missing |
| 2 | 14 | yes | yes | 1–7 | observed + system missing |
| 3 | 14 | yes | yes | 1–7 | observed + system missing |
| 4 | 14 | yes | yes | 1–7 | observed + system missing |
| 10 | 14 | yes | yes | 1–7 | observed + system missing |
| 100 | 14 | yes | yes | 1–7 | observed + system missing |

The stream retained full `row_count`, exact source SHA, and the decoder metadata digest from the incidence. Values and missing states came from the existing decoder helpers.

## Empty frame

Sourcefree incidence with `row_count=0`, one variable, empty `_frame`:

- full stream: 0 cells;
- projected stream (`include_variables=("a",)`): 0 cells;
- no `UnboundLocalError`.

## Custody and truncation

- Snapshot closed after constructing a selected stream: 0 cells yielded, then `SOURCE_IDENTITY_UNAVAILABLE`.
- Source SHA replaced with a wrong SHA: `SOURCE_CUSTODY_SHA_MISMATCH` at construction.
- Declared `row_count=8` over a 7-row DTA: all 7 rows yielded, then `SILENT_PHYSICAL_GRID_TRUNCATION`; the stream did not silently complete.
- Original DTA path overwritten after decode: selected stream still exact and source SHA preserved, confirming the snapshot boundary rather than a live-path reopen.

## Reused SAV / first-consumer evidence

R1 evidence remains valid because the SAV branch was not functionally changed:

- SRC31: 574,056 all cells, 33,768 selected, exact selected sequence/digest `2461996e…`, 2.36 s -> 0.173 s; NativePackage release `73700af5…`, replay `b7f2736d…`, semantic hash and 59,102 public objects equal.
- SRC09: 41,334 selected cells, digest `1d23d781…`, 0.404 s; author all-cell baseline 5,972,763 / 46.4–47.6 s retained.
- Fixture C11 factory full-grid and NativePackage parity passed previously and in the current 37-test focused suite.
- The old 226 MB tuple-versus-101 MB diagnostic is preserved as diagnostic-only, not the D baseline.

## Proof limits

- DTA fixtures are sourcefree; original SRC27–SRC30 DTA files were not opened, so original DTA scale/identity is **NOT_RUN**.
- Genuine C11 SRC31/SRC16 refusal remains A-owned; actual D `execute_native_compiler_source`, 600 s end-to-end, all35, and 16-GiB remain **NOT_RUN**.
- No native/scientific authority, protected merge, or source/config inference is added.
- Adapter tests: 7 PASS. Focused suite: 37 PASS.
