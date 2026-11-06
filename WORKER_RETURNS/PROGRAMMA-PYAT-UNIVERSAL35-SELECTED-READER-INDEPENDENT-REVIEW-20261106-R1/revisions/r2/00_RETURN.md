# UNIVERSAL35 selected-reader independent r2 closure

**VERDICT: ACCEPT_SCOPED_ENGINEERING** at frozen target head `12d44c9d2418d7ab0cbcb92b4daa48d6a2cf20f3`.

- R2 code: `7a404b0dcaac0e4dd027b9edb98c9038d89dbd9a`
- Prior reviewed target: `89a41589c7541f625c6d2f9346436629d374b93e`
- Prior independent review: `20dee3499bea3cc1f13131568b50dd079fcee8cd` (`REVISE`)
- Frozen branch: `codex/pyat-universal35-selected-reader-r2-review-20261106-r1`
- Published review head: the commit containing this directory; exact SHA reported in final delivery.
- Author r2 return is the existing root `00_RETURN.md` plus `04_R2_DTA_AND_EMPTY_FRAME_REPAIR.md`; author files were read, not edited.

## FINDING

The two prior material defects are repaired in the observed code. The old cut reproduces the DTA snapshot failure; the new cut projects DTA with windowed `read_dta(row_offset, row_limit, usecols=...)` over the same content-bound `/dev/fd` snapshot and matches full-decode selected cells exactly across multi-row windows, including missing states, row/column order, replay, source SHA and metadata digest. The zero-row frame path now returns an empty exact stream instead of raising `UnboundLocalError`.

No new material defect was found in the observed repair. SAV selected parity/economy and NativePackage parity are unchanged and reused from the r1 review; the SAV branch was not functionally altered beyond the surrounding branch split.

## GRADES

- **Code: PASS_SCOPED.** DTA selected windows are bounded and exact; SAV path unchanged; zero-row fix present; custody/closure/truncation checks remain.
- **Cell: PASS_SCOPED_DTA_SAV.** DTA sourcefree 14/14 selected cells exact for window sizes 1,2,3,4,10,100 with observed and system-missing states; prior SAV 33,768/41,334 selected-cell evidence unchanged.
- **Parity: PASS_SCOPED_DTA_SAV.** DTA full-decode selected parity, two-pass replay, source SHA and metadata digest exact; prior SRC31 NativePackage release/replay/semantic/public-object parity and SRC09 selected digest retained.
- **Economy: PASS_SCOPED_SAV.** Prior SRC31 574,056 all cells -> 33,768 selected, 2.36 s -> 0.173 s; SRC09 41,334 selected / 0.404 s, with author all-cell baseline 5,972,763 / 46.4–47.6 s retained as author measurement. DTA repair was not benchmarked for original scale.
- **First consumer: PASS_SCOPED_NATIVE_PACKAGE.** Prior SRC31 NativePackage parity retained; actual D end-to-end, genuine C11, and all35 remain **NOT_RUN**.

## BOUNDARY CHECKS

- Old cut `89a4158` DTA selected path reproduced `ReadstatError: Unable to read from file`.
- New cut window sizes 1–100 all yielded exactly 14 selected DTA cells over 7 rows, in row order `1..7`, with exact two-pass replay and missing-state parity.
- Closed snapshot: 0 cells yielded, then `Original35PhysicalStreamError: SOURCE_IDENTITY_UNAVAILABLE`.
- Wrong custody SHA: `Original35PhysicalStreamError: SOURCE_CUSTODY_SHA_MISMATCH`.
- Declared row_count 8 over a 7-row DTA: all seven rows yielded, then `SILENT_PHYSICAL_GRID_TRUNCATION`; no silent completion.
- Original DTA file path changed after decode: snapshot-based selected stream still exact and source SHA preserved.
- Empty frame: full and projected streams both return 0 cells.

## LIMITS / PRESERVATION

- DTA sourcefree fixtures only; SRC27–SRC30 original DTA files **NOT_RUN**.
- No original35 scale, D 600 s end-to-end, native/scientific, all35, or 16-GiB claim. Sourcefree repair does not establish those.
- No A/D source-mapping or native-consumer edits; no product/guide/progress/controller/protected merge; no native/science authority.
- Prior old 226 MB tuple-versus-101 MB wrapper comparison remains a diagnostic negative only, not the D baseline.
- No raw respondent rows, native keys, source bytes, or absolute source root in Git.
- Tests rerun: 7 adapter PASS; 37 focused PASS. The author's 2-test r2 log is consistent.
