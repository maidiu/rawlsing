# REPRODUCIBLE RECEIVER AND HOSTILE NEGATIVES — PYAT RRIF-E4FR D02 FINAL

## 1. Environment

- Host `mainMac.lan`, macOS 13.2.1 (22D68), Darwin 22.3.0, x86_64.
- Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1, numpy 2.3.2.
- OpenCode 1.18.34, agent `build`, live session `ses_e67ce6138ffe4GaCdkjtL5CYvr`, `modelID=deepseek-v4.1-flash`, `providerID=opencode-go`, `variant=max`.
- Clean detached worktrees used for execution:
  - E4F `f2c0af3273d612bff0a7bd2407532b52caf4348b` at `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/e4fr-review-e4f-f2c0af3273d612bff0a7bd2407532b52caf4348b`;
  - E1 `ffd03934d0a86c98ed095d973e45587bd5751013` at `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/e4fr-review-e1-ffd03934d0a86c98ed095d973e45587bd5751013`;
  - PREMAIN `8e44ca9c751049d65e6def47600b5c073ee04b29` at `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/e4fr-review-premain-8e44ca9c751049d65e6def47600b5c073ee04b29`.
- Worktree creation (per commit):

```
git worktree add --detach --no-checkout <path> <commit>
cd <path>
git sparse-checkout init --cone
git sparse-checkout set rawlsing_next tests \
  WORKER_RETURNS/EE-P2R6S \
  WORKER_RETURNS/FIABC-LM2 \
  WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY \
  WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING
git checkout --detach <commit>
git status --porcelain   # empty before and after
```

No fixture was copied from or symlinked to an author/PREMAIN worktree; the fixture trees came from each exact commit's own tree. All runs used `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider`; worktrees remained clean.

## 2. Real receiver regression — E4F 12 tests

Command, from the clean E4F worktree:

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py
```

Observed:

```
............                                                             [100%]
12 passed in 0.79s
EXIT=0
```

The real fixture is built in the test with the installed pyreadstat writer:

```
frame = pd.DataFrame({
    "dtm": pd.to_datetime(["2008-04-05 06:07:08", "2009-05-06 07:08:09"]),
    "score": [1.5, -2.25],
    "label": ["a", "b"],
})
pyreadstat.write_sav(frame, path)   # or write_dta
```

Then `decode_sav` / `decode_dta`, `iter_cells(2)`, `R5TypedValueCodec.encode`, and the pinned historical `iter_source_native_rows` are executed. No mock, import-only, or reader-only shortcut is used.

## 3. Original E1 33 tests

Command, from the clean E4F worktree:

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py
```

Observed:

```
.................................                                        [100%]
33 passed in 0.86s
EXIT=0
```

Collection counts independently confirmed: 11 D01 + 18 D02 + 4 integration = 33.

## 4. Selected PR526 / SAV / C11 / EE-P2X suite

Command, from the clean E4F worktree:

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py \
  rawlsing_next/tests/test_universal_source_byte_custody.py \
  rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py \
  rawlsing_next/tests/test_fiabc_lm1_r1e_n1_physical_boundary.py \
  rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py \
  rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py \
  rawlsing_next/tests/test_universal_source_projection.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_r35_i01_physical_metadata.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  tests/test_ee_p2x_darwin_court_driver.py \
  tests/test_fiabc_final_measurement_telemetry_closure.py
```

Observed:

```
......................................................................s. [ 36%]
........................................................................ [ 73%]
...................................................                      [100%]
194 passed, 1 skipped in 144.12s (0:02:24)
EXIT=0
```

Independent collection counts sum to 195:

| Module | Tests |
|---|---:|
| `test_rrif_e1_c3_d01_declared_encoding_admission.py` | 11 |
| `test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | 18 |
| `test_rrif_e1_c3_current_integration_regressions.py` | 4 |
| `test_universal_source_byte_custody.py` (PR526) | 26 |
| `test_pre553_sr06_decoder_carrier.py` | 17 |
| `test_fiabc_lm1_r1e_n1_physical_boundary.py` | 7 |
| `test_fiabc_lm2_r1j_sav_representation_authority.py` | 9 |
| `test_fiabc_lits_i_representation_authority.py` | 10 |
| `test_universal_source_projection.py` | 31 |
| `test_universal_workload.py` | 16 |
| `test_r35_i01_physical_metadata.py` | 6 |
| `test_pre553_source_backed_c11_facade.py` | 10 |
| `tests/test_ee_p2x_darwin_court_driver.py` | 19 |
| `tests/test_fiabc_final_measurement_telemetry_closure.py` | 11 |
| Total | 195 |

The single skip is `test_real_writer_dta_extended_missing_fixture_or_typed_dependency_limitation` in `test_pre553_sr06_decoder_carrier.py`: the installed pyreadstat writer/readback does not expose `missing_user_values` in metadata. It is the same environmental writer limitation recorded by E1/E4 and is not a D02 pass or failure. No selective deselection or green falsification was used; all 195 tests were collected and all 194 runnable tests passed.

## 5. G01 baseline severance

### 5.1 PREMAIN full pair

From the clean PREMAIN `8e44ca9c` worktree, using a test environment wrapper that only disables cyclic GC before `pytest.main` and exits with pytest's code (no test/production/option change):

```
import gc, os, sys
gc.disable()
import pytest
rc = pytest.main(sys.argv[1:])
print("PYTEST_MAIN_RETURN", rc, flush=True)
os._exit(rc)
```

Command:

```
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 <wrapper> \
  -q -p no:cacheprovider --tb=short -rA \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_inventory.py \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py
```

Observed:

```
2 failed, 7 passed in 278.00s (0:04:37)
PYTEST_MAIN_RETURN 1
EXIT=1
```

Failures:

- `test_native_to_canonical_mapping_authority_does_not_bridge_physical_representation`: `47f141e43fb2…` vs `b9b720335f37…`.
- `test_special_states_remain_noncanonical_and_mapping_authority_does_not_leak`: `StopIteration` locating the int special-state rule.

### 5.2 E4F full pair

Same command form from the clean E4F worktree. Observed:

```
2 failed, 7 passed in 278.76s (0:04:38)
PYTEST_MAIN_RETURN 1
EXIT=1
```

The two node ids and assertion values are identical to PREMAIN. The seven passes are the unchanged inventory/hostile controls. This is causal severance: D02 neither introduces nor repairs G01. G01 remains `HELD`.

### 5.3 PREMAIN hostile-only cross-check

Also run with `-k "native_to_canonical or special_states"` on PREMAIN: `2 failed, 6 deselected in 79.89s`, exit `1`; same two failures. This matches the E4F return's baseline claim.

## 6. Original E4 RED replay on E1

A source-free probe was run on the clean detached E1 worktree (`PYTHONPATH=.`), writing real SAV and DTA via pyreadstat and exercising `decode_sav`/`decode_dta`, `iter_cells`, and direct/one-level aware wrappers. Observed at E1:

```
sav cell: str '2008-04-05 06:07:08'
sav cell: str '2009-05-06 07:08:09'
dta cell: str '2008-04-05 06:07:08'
dta cell: str '2009-05-06 07:08:09'
naive-subclass-direct: str '2008-04-05 06:07:08.901234'
naive-timestamp-direct: str '2008-04-05 06:07:08.901234'
naive-one-wrapper: str '2008-04-05 06:07:08.901234'
aware-direct: str '2008-04-05 06:07:08+00:00'
aware-ts-direct: str '2008-04-05 06:07:08+00:00'
aware-one-wrapper: str '2008-04-05 06:07:08+00:00'
aware-time-direct: str '06:07:08+00:00'
nat-direct: str 'NaT'
nanosecond-direct: str '2008-04-05 06:07:08.123456789'
opaque-range-classify: REFUSED TypeError '<=' not supported between instances of 'int' and 'R5OpaqueValue'
```

This independently reproduces the original E4 RED against the exact E1 cut: real SAV/DTA `DATETIME` silently becomes a string, aware subclasses stringify, and range classification raises `TypeError`.

## 7. E4F corrected receiver and hostile matrix

Same probe on the clean E4F worktree. Observed:

```
sav cell: R5OpaqueValue python.datetime.datetime@1 (payload 07d804050607080000000000 / 07d905060708090000000000)
dta cell: R5OpaqueValue python.datetime.datetime@1 (same civil payloads)
sav floats: [1.5, -2.25] bits=['3ff8000000000000', 'c002000000000000']
dta floats: [1.5, -2.25] bits=['3ff8000000000000', 'c002000000000000']
naive-subclass-direct: opaque python.datetime.datetime@1 07d80405060708000dc07201
naive-timestamp-direct: opaque python.datetime.datetime@1 07d80405060708000dc07201
naive-one-wrapper: opaque python.datetime.datetime@1 07d80405060708000dc07201
naive-two-wrapper: str '2008-04-05 06:07:08.901234'
aware-direct: REFUSED R5CodecError timezone-aware datetime requires a separate explicit decoder carrier authority
aware-ts-direct: REFUSED R5CodecError ... separate explicit decoder carrier authority
aware-one-wrapper: REFUSED R5CodecError ... separate explicit decoder carrier authority
aware-two-wrapper: str '2008-04-05 06:07:08+00:00'
aware-ts-two-wrapper: str '2008-04-05 06:07:08+00:00'
aware-time-direct: REFUSED R5CodecError timezone-aware time requires a separate explicit decoder carrier authority
nat-direct: REFUSED R5CodecError date-like subclass NaTType cannot be safely canonicalized to a naive datetime carrier
nanosecond-direct: REFUSED R5CodecError date/time subclass with sub-microsecond precision cannot be preserved by the versioned opaque carrier
broken-tzinfo-direct: REFUSED R5CodecError date-like subclass BrokenTzinfo cannot expose tzinfo safely
broken-year-direct: REFUSED R5CodecError date-like subclass BrokenYear cannot be safely canonicalized to a naive datetime carrier
opaque-normalizer-aware: REFUSED R5CodecError ... separate explicit decoder carrier authority
opaque-direct-aware: REFUSED R5CodecError ... separate explicit decoder carrier authority
opaque-direct-naive-ts: opaque python.datetime.datetime@1 07d80405060708000dc07201
opaque-range-classify: REFUSED DecoderError physical value cannot be compared with a declared missing range (value_type=R5OpaqueValue)
```

Additional hostile checks passed:

- Broken `nanosecond`, broken `fold` on a datetime subclass, broken `fold` on a time subclass, and broken `year` on a date subclass: typed `R5CodecError` at direct route.
- Aware mapping key in `normalize_decoder_physical_value`: typed `R5CodecError`.
- Direct `R5TypedValueCodec.encode(aware)` and `encode(naive Timestamp)`: typed `R5CodecError` `date/time meaning may not be invented by the R5 codec; use an explicit opaque decoder value`.
- `opaque_decoder_value(None)` / `opaque_decoder_value(1)`: typed `unsupported opaque decoder value type …`.
- `time` subclass with `microsecond=901234, fold=1`: exact payload `060708000dc07201`.
- Real SAV/DTA date variables (not just DATETIME) observed as direct `datetime.date` and carried as `python.datetime.date@1`; no string.

### 7.1 Nested item-chain negative

Confirmed on E4F:

- `_ItemWrapper(_ItemWrapper(aware_datetime))` → `str '2008-04-05 06:07:08+00:00'`.
- `_ItemWrapper(_ItemWrapper(aware_Timestamp))` → the same string.
- `_ItemWrapper(_ItemWrapper(broken civil-field subclass))` → its string.
- `_ItemWrapper(_ItemWrapper(naive_date))` → `str '2008-04-05'`.

The E4F test intentionally asserts only the naive two-level fallback. This is the unchanged E1 non-carrier fallback and is outside the accepted one-level D02 promise. It is not reachable from the real pyreadstat SAV/DTA cell route (real values are direct `Timestamp`/`date`, and real numeric scalars unwrap in one level). It is recorded as a non-blocking residual hostile-input boundary in `00_RETURN.md` §5; it is not timezone-aware carrier authority.

### 7.2 Additional numpy boundary observation

Not part of the accepted D02 `pandas.Timestamp`/subclass scope, recorded for honesty:

- `numpy.datetime64('2008-04-05')` and `numpy.datetime64('2008-04-05T06:07:08')` unwrap one level to built-in `date`/`datetime` and carry correctly.
- `numpy.datetime64('2008-04-05T06:07:08.123456789')` is not a date/time subclass; `.item()` returns the integer `1207375628123456789`, so `_physical_value` falls through to an integer.
- `numpy.datetime64('NaT').item()` returns `None`; `_physical_value` returns `None` (system-missing classification), not a string.

The current pyreadstat SAV/DTA `DATETIME` route produces direct pandas `Timestamp`, not these numpy scalars. This is outside the accepted D02 scope and does not change the verdict; it is not evidence of an installed-current source/consumer vulnerability.

## 8. Pinned seam execution honesty

From the E4F worktree:

```
python3 -c "import rawlsing_next.pre553_r5_seam"
# ModuleNotFoundError: No module named 'rawlsing_next.pre553_r5_seam'
```

The test's `_pinned_seam()` then loads:

- seam blob `cef326ebbc40468428378f7fdbe76e4756179f39`, sha256 `626f74200a11dd8f749bead1ebd904eae22b65246636395a16df60d33d2b052f`;
- model blob `62ce608829c3d9c2fb7c999aefe40188637edf80`, sha256 `cdb8a2581aeed7f24acd668f3b93ca23244f64820266e5d282fb65915c17ac3a`;

from the local Git object database with `git cat-file -p`, verifies both with `git hash-object --stdin` and SHA-256, and executes them in-memory. Inspection showed the loaded module name `rawlsing_next.pre553_r5_seam`, `has-file False`, and the real consumer `iter_source_native_rows`. This is a test-only historical execution, not an installed-current production seam. It adds no production file and reads no network or survey source. If the pinned objects are absent, the test fails with a precise message; it does not silently skip.

The real fixture test asserts that `dtm` rows from `iter_source_native_rows` have `payload["raw_value"]["t"] == "opaque"`, `type_id == "python.datetime.datetime@1"`, and `!= "str"`.

## 9. Fixture and execution limits

- All SAV/DTA fixtures are synthetic source-free files written by the installed pyreadstat. No raw/native survey source, source-use right, or scientific meaning is involved.
- The pinned seam/model are historical Git objects loaded read-only for the test; the current production tree does not contain the seam.
- G01 is out of D02 scope and remains a known baseline failure with identical values at PREMAIN and E4F.
- The full repository suite was not run; only the mandated bounded suites and probes were executed.
- No production code, author branch, protected PREMAIN/main, Sorok, native source, actor, or PROGRAMMA state was modified.

Terminal: `E4FR_RECEIPTS__12_33_194_1_GREEN__E1_RED_REPLAYED__E4F_REAL_AND_HOSTILE_MATRIX_GREEN__NESTED_AND_NUMPY_BOUNDARIES_RECORDED`
