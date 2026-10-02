# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C4C3 — DARWIN/X86_64 ANCHOR RUNTIME QUALIFICATION + C3 55/55 — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq174-c4c3-darwin-anchor-runtime-r1`

Exact base:
`8f7efe690a161902e79358eb31650c238a4c0be8`

This is the exact C4A combined C1+C3 tree.

Governing evidence:

- Omega-1:
  `01762d7379be4e423dad3e21bcdcee47c536902d`
- C4A:
  `8f7efe690a161902e79358eb31650c238a4c0be8`
- C4C2:
  `f20d3e5a309e52a479e75d20430d2990e8de60c8`
- accepted historical C3 source-free execution:
  `257c2ebfd38d106f1669afbfd701a33e600cf4c5`
- accepted C3 review:
  `462e6bf1ed514056f9316dad761054e690a7755d`

## HQ adjudication

Omega-1 did **not** require a non-Mac execution surface.

Its law is:

- where relying on the retained physical reproducibility anchor, honor:
  - Darwin/x86_64
  - CPython 3.11.3
  - pyreadstat 1.3.6
  - pyarrow 25.0.1
- a different environment would require explicit equivalence qualification.

C4C2 independently proved:

`P2X_DARWIN_GATES_NOT_ON_C4_PATH`

Therefore no EE-P2X Darwin gate patch or waiver is required.

This lane intentionally qualifies the actual C4 path on the Darwin/x86_64 anchor.

No raw survey source access is authorized.

## Exact historical C3 environment seed

Accepted C3 source-free environment at commit `257c2ebf...`:

- CPython 3.11.3
- pytest 9.1.1
- pandas 2.3.3
- numpy 2.4.6
- pip 22.3.1
- Pygments 2.21.0
- iniconfig 2.3.0
- packaging 26.3
- pluggy 1.6.0
- python-dateutil 2.9.0.post0
- pytz 2026.4
- setuptools 65.5.0
- six 1.17.0
- tzdata 2026.4

Historical sorted pip-freeze SHA-256:

`9cde8e5ab9abba46a9e98826100ed084a0943a77fee7bc232a3c7643334da2eb`

For current C4 qualification also require:

- pyreadstat 1.3.6
- pyarrow 25.0.1

No duckdb unless exact call-path evidence shows it is needed. C4C2 says it is not on the actual path.

## Mission

Qualify the exact combined tree on the local Darwin/x86_64 runtime using only synthetic source-free fixtures and the authoritative six-file C3 court.

## PHASE 0 — exact tree and host

Verify:
- HEAD exactly `8f7efe690a161902e79358eb31650c238a4c0be8`;
- merge `9a5752a8ce4a119efd24cbbeedd8cbcda8abbadb` ancestor;
- 5 C1 owner blobs exact;
- 6 accepted C3 blobs exact;
- facade blob `8a761119e4a8d68eb291fc4edfadb52e027f8284` exact.

Record:
- macOS version;
- Darwin kernel;
- machine;
- Python executable and exact version.

Require:
- Darwin
- x86_64
- CPython 3.11.3

If any fail:
`C4C3_DARWIN_ANCHOR_MISMATCH__HQ_ADJUDICATION_REQUIRED`.

## PHASE 1 — isolated exact dependency environment

Create a fresh isolated venv outside the repository.

Freeze:
- pytest 9.1.1
- pandas 2.3.3
- numpy 2.4.6
- pyreadstat 1.3.6
- pyarrow 25.0.1
- supporting dependencies required by those packages

Do not install on import.

Record:
- exact pip freeze
- hashes of installed distributions/wheels where available
- Python executable
- environment location class
- no repo mutation.

If current package resolution requires transitive-version differences from the historical C3 freeze, record them explicitly and prove they do not alter the tested C3/C4 behavior. Do not silently hide them.

## PHASE 2 — actual C4 path confirmation

Reuse/independently confirm C4C2's static holding:

`P2X_DARWIN_GATES_NOT_ON_C4_PATH`

Trace from:
- decode_sav / decode_dta
- source-backed C11 facade
- empirical provider
- analytical composition
- named positioned-subject consumer

Do not run measured P2X.

## PHASE 3 — explicit pyreadstat option freeze

For pyreadstat 1.3.6, freeze every C4-relevant option and default actually relied upon, including:

- metadataonly
- apply_value_formats
- user_missing
- encoding
- formats_as_category
- dates_as_pandas_datetime
- disable_datetime_conversion
- row_limit
- row_offset
- output_format
- extra_date_formats
- extra_datetime_formats
- extra_time_formats
- ordered-category behavior

Separate:
- explicit repository arguments;
- verified pyreadstat 1.3.6 defaults.

No unidentified default may govern C4.

## PHASE 4 — synthetic source-free reader probes

Generate only synthetic SAV/DTA files in a temporary directory.

Exercise the exact accepted combined-tree decoder/codec/facade path.

Required:

### D01
- BIG5 exact-SHA admission
- WINDOWS-1252 exact-SHA admission
- encoding=None behavior
- metadata-only path
- wrong SHA/encoding rejection
- no auto/guess/fallback widening

### G01
- native-int storage through pyreadstat/pandas
- float64 arrival
- user-missing versus observed-storage states
- exact R5 big-endian float tokens

### D02
- naive datetime/date/time arrival types
- opaque carrier normalization
- timezone-aware rejection
- item-wrapped timezone-aware hostile propagation

### DTA / LiTS physical layer
- synthetic DTA through `decode_dta(..., encoding="latin1")`
- relevant user/extended missing carrier behavior
- repeat-decode stability

No real survey file may be opened, hashed, statted or decoded.

## PHASE 5 — authoritative C3 six-file court

Run exactly:

1. `test_closed35_g01_sav_numeric_representation_authority.py`
2. `test_closed35_d01_declared_encoding_admission.py`
3. `test_closed35_d02_opaque_datetime_carrier.py`
4. `test_fiabc_lm2_r1j_sav_representation_authority.py`
5. `test_r35_i01_physical_metadata.py`
6. `test_pre553_source_backed_c11_facade.py`

Expected exact total:
`55`

Required:
`55 passed / 0 failed / 0 errors / 0 skipped`

Assert all paths exist before running.

The three failures from C4A's wider mechanical compatibility sweep are outside this authoritative acceptance court and are not part of the denominator.

## PHASE 6 — resource/identity law

Freeze:
- actual Darwin/x86_64 environment identity;
- pyreadstat reader_version = 1.3.6 in physical metadata identity;
- pyarrow 25.0.1;
- host byte order and R5 explicit big-endian behavior;
- Darwin ru_maxrss unit = bytes for this execution surface;
- repeat synthetic decode stability.

## PHASE 7 — C1 preservation

Verify:
- all five C1 owner blobs exact;
- C4A's 454/454 receipt belongs to this exact combined lineage;
- qualification introduced no tracked production changes.

No need to rerun all 454 unless a runtime incompatibility appears.

## Return

Write only:

`WORKER_RETURNS/PYAT-C4C3-DARWIN-ANCHOR-RUNTIME-R1/**`

Required:
- `00_RETURN.md`
- `01_ENVIRONMENT_LOCK.json`
- `02_ACTUAL_C4_CALL_PATH.json`
- `03_READER_OPTION_FREEZE.json`
- `04_SYNTHETIC_READER_PROBES.json`
- `05_AUTHORITATIVE_C3_COURT.json`
- `06_RESOURCE_IDENTITY_LAW.json`
- `07_EXECUTION_RECEIPT.json`
- `08_FINAL_DISPOSITION.json`

Allowed:
- `PASS_C4C3_DARWIN_ANCHOR_RUNTIME_QUALIFIED__C3_55_OF_55__FANIN_READY`
- `C4C3_DARWIN_ANCHOR_MISMATCH__HQ_ADJUDICATION_REQUIRED`
- `C4C3_DEPENDENCY_ENVIRONMENT_BLOCKER__HQ_ADJUDICATION_REQUIRED`
- `C4C3_SYNTHETIC_READER_BEHAVIOR_BLOCKER__HQ_ADJUDICATION_REQUIRED`
- `C4C3_AUTHORITATIVE_C3_COURT_FAILURE__HQ_ADJUDICATION_REQUIRED`

No raw survey access.
No C4 live production.
No self-adoption.

Terminal:
`C4C3_DARWIN_ANCHOR_RUNTIME_RETURNED__HQ_FANIN_REQUIRED`
