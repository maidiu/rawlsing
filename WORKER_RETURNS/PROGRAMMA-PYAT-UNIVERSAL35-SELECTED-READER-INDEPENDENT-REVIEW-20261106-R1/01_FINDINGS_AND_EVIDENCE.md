# Findings and evidence

## Frozen inputs

- Target: `89a41589c7541f625c6d2f9346436629d374b93e` on `codex/pyat-universal35-selected-reader-review-20261106-r1`.
- Production change: `fd18faf0340f9d3751ffd9042799a0b7d58519bb`; only
  `rawlsing_next/pre553_original35_physical_stream.py` and its test module changed.
- Prior wrapper: `be7e831f41e1c699890b7987cd2fea25be3f65d3`.
- Runtime root came only from `.local-logs/pyat-universal35/source-runtime-binding.local.json`.
- No source root, raw rows, native keys, or source bytes are included here.

## Blocking finding: selected DTA path fails at the frozen snapshot boundary

`_selected_chunk_cells` (`rawlsing_next/pre553_original35_physical_stream.py:110`) chooses
`pyreadstat.read_dta` and passes `snapshot.reader_path` (an unlinked inode exposed as
`/dev/fd/<n>`) to `pyreadstat.read_file_in_chunks` with `usecols`.

Reproduction used a valid three-row, three-column sourcefree DTA fixture written by
`pyreadstat.write_dta`, then decoded with `decode_dta` and a matching SHA. Results:

- full decoder/grid: 9 cells, OK;
- full `read_dta` on the rewound snapshot path: OK;
- `read_file_in_chunks(read_dta, regular_path, chunksize=1, usecols=...)`: OK;
- new `bounded_physical_cell_stream(..., include_variables=("id", "x"))`: `ReadstatError: Unable to read from file` before any selected cell.

SRC27–SRC30 are configured DTA originals in the source roster. No actual DTA original was
opened in this review, so the exact original-file behavior is not claimed; the failure at the
new module's snapshot/read call is deterministic on the sourcefree valid DTA contract.

## Minor finding: zero-row frame fallback

`_selected_frame_cells` (`rawlsing_next/pre553_original35_physical_stream.py:88`) references
`row_ordinal` after the loop. With a sourcefree zero-row frame and `row_count == 0`, the selected
stream raises `UnboundLocalError` instead of yielding an empty selected stream. No current
original35 source is zero-row; this is a boundary defect, not a cause of the SRC09/SRC31 result.

## SAV selected-cell parity

Independent SRC31 run, selection `d18c,c13a,b8,d18k`:

- source SHA `de7b51f9abf455b072555a84c5592e3ac46bb32c4f9f61bc055160f7d871e571`, 8,442 rows;
- current filter-every-cell: 574,056 cells created, 33,768 selected, 2.36 s;
- projected selected path: 33,768 cells, 0.173 s;
- selected tuples exact (same sequence), digest `2461996eaf82ca3015476951c8d471d3bdbc44c69c50f5c8bc0b6e7daa1d912b` on both.

Independent SRC09 selected pass, selection `q74,ir2b`:

- 20,667 rows, 41,334 selected cells, 0.404 s;
- digest `1d23d7813ca7a24eda8c7c6538cae6485c53d0320dab2bb0740398621f2381d4`, matching the
  author's reported exact digest;
- first `(1, 87, q74)`, last `(20667, 259, ir2b)`.
- The author's all-cell SRC09 baseline (5,972,763 / 46.4–47.6 s) is retained as author evidence;
  the reviewer did not repeat that 47-second all-cell pass.

## First-consumer parity

On genuine SRC31, the existing NativePackage consumer produced the same values from the current
filtered baseline and the projected stream:

- release ref `73700af58720b487c45234f0d50cf13e1d3e52b761e33f88862b1c6bae06071a`;
- replay ref `b7f2736d9a33a95d53f6880acd95fef09f61df85ada9406aa023a61945bcd12e`;
- semantic release hash equal to the release content hash;
- 59,102 public objects;
- native-package build wall ~33.19 s vs ~34.43 s, so this is not an end-to-end speed claim.

The fixture test exercised the existing C11 factory full-grid route. The full-grid path was not
changed; genuine C11 SRC31/SRC16 still refuses at A-owned unbound response mapping.

## Refusal and lifecycle checks

- Closed the source snapshot before iterating a constructed selected stream: zero cells yielded,
  then `Original35PhysicalStreamError: SOURCE_IDENTITY_UNAVAILABLE`.
- Wrong package SHA at the NativePackage consumer: `NativePreimageRefusal: WRONG_SOURCE_EDITION`
  before cell consumption.
- Source-read admission tests (including revocation/currentness refusal) are part of the passing
  35-test focused suite.
- The new selected path does not call `incidence.iter_batches`; the sourcefree adapter test
  monkeypatches it to fail if the all-cell generator is used. The underlying reader may still
  parse unselected physical records internally.

## Preservation / proof limits

- 5 adapter tests PASS; 35 focused tests PASS.
- No product/test/guide/progress/controller/protected edits; no source or native grant.
- The old 226 MB versus 101 MB diagnostic negative is preserved as diagnostic-only.
- Genuine end-to-end C11/native execution, all35, 16-GiB, and D `execute_native_compiler_source`
  remain NOT_RUN. No S3/current-fact claim is made from pipeline artifact names.
