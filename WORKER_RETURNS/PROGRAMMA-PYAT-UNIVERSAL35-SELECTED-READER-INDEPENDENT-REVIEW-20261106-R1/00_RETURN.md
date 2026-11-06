# UNIVERSAL35 selected-reader independent review — r1

**VERDICT: REVISE** at frozen target head `89a41589c7541f625c6d2f9346436629d374b93e`.

- Review branch: `codex/pyat-universal35-selected-reader-review-20261106-r1`
- Implementation reviewed: `fd18faf0340f9d3751ffd9042799a0b7d58519bb`
- Prior wrapper retained: `be7e831f41e1c699890b7987cd2fea25be3f65d3`
- Base: `d129eebdb0472b0c3625efa281826a858bd0a384`
- Published review head: the commit containing this return; exact SHA is reported in final delivery.

## FINDING

The SAV selected-reader path passes actual SRC31 and SRC09 cell/parity/economy checks. The new module is not yet an original35-format-complete selected reader: its DTA branch is non-operational.

`_selected_chunk_cells` selects `pyreadstat.read_dta` for `reader_kind == "DTA"` and calls:

```python
pyreadstat.read_file_in_chunks(
    pyreadstat.read_dta, snapshot.reader_path, chunksize=..., usecols=[...], ...
)
```

`snapshot.reader_path` is an open `/dev/fd/<n>` binding. On a valid sourcefree DTA fixture, `decode_dta` and the full `iter_cells` path succeed, and `read_file_in_chunks` on a regular DTA path succeeds, but the new selected path raises `ReadstatError: Unable to read from file` before producing a cell. SRC27–SRC30 are configured DTA originals. No actual DTA original was opened in this review; the failure is established at the frozen reader boundary without publishing rows or bytes.

A second, minor frame-boundary defect exists: `_selected_frame_cells` reads `row_ordinal` after the loop; a zero-row compatibility/sourcefree frame with `row_count == 0` raises `UnboundLocalError` instead of returning an empty exact stream.

## GRADES

- **Code: REVISE.** SAV selected path uses the content-bound snapshot, `usecols`, decoder value/missing helpers, global row/column ordinals, replay, metadata digest, and custody checks. DTA selected path fails; zero-row frame fallback is untested/broken.
- **Cell: PASS_SCOPED_SAV.** SRC31 574,056 all cells versus 33,768 selected, exact sequence/digest; SRC09 41,334 selected, exact author digest `1d23d781…`.
- **Parity: PASS_SCOPED_SAV.** SRC31 NativePackage release ref, replay ref, semantic release hash, and 59,102 public-object count match current-filter baseline; fixture factory/native-package parity passes.
- **Economy: PASS_SCOPED_SAV.** SRC31 2.36 s -> 0.173 s; SRC09 selected pass 0.404 s with author all-cell baseline 5,972,763 / 46.4–47.6 s retained as author measurement. Native-package build itself remains ~33–34 s on SRC31; no 600 s end-to-end claim.
- **First consumer: PASS_SCOPED_NATIVE_PACKAGE.** Existing NativePackage consumer parity was exercised. Actual D `execute_native_compiler_source` end-to-end remains **NOT_RUN**. Genuine C11 SRC31/SRC16 remains refused at A-owned unbound response mapping.

## PRESERVED HISTORY / LIMITS

- The earlier 226 MB tuple-versus-101 MB wrapper comparison remains only an eager diagnostic; it is **not** the D baseline.
- The corrected comparison is current D filter-every-cell versus actual column pushdown.
- Adapter tests: 5 PASS. Focused suite: 35 PASS (adapter, source-read admission, original35 operations, source configuration).
- Closed source snapshot refused before yielding any cell (`SOURCE_IDENTITY_UNAVAILABLE`); wrong package/source SHA refused by the NativePackage consumer before cell use (`WRONG_SOURCE_EDITION`).
- No unselected `PhysicalCell` objects are constructed by the new selected path; the reader may still parse physical records internally. The existing full-grid path and sourcefree frame fallback were not redefined.
- No product/test/guide/progress/controller/protected edits, no protected merge, no native/science grant, no raw respondent rows/native keys/bytes in Git.
- Scope is S2 engineering physical I/O only. Genuine end-to-end C11/native, all35, 16-GiB, and scientific/original native adoption remain **NOT_RUN**.

## ACTION

Return to the author for a bounded repair: make the DTA selected path use a functioning existing snapshot/read route (or explicitly refuse DTA with a typed `COLUMN_PROJECTED_READER_UNAVAILABLE` while preserving full-grid behavior), guard zero-row frame projection, and add DTA plus zero-row tests. D/A pending semantics are not requested as code changes here.
