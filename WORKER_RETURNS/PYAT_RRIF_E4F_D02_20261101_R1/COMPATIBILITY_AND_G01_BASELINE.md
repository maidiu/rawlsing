# COMPATIBILITY AND G01 BASELINE — RRIF-E4F D02

## 1. Environment

- Host `mainMac.lan`, macOS 13.2.1 (22D68), Darwin 22.3.0, x86_64.
- Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1, numpy 2.3.2.
- OpenCode 1.18.34, agent `build`.
- Session DB read-only: `ses_e680bf28effeGdJ4hyA8lvBrk7`, `{"id":"deepseek-v4.1-flash","providerID":"opencode-go","variant":"max"}`.
- Corrected cut worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1`, branch `agent/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1`.
- PREMAIN baseline worktree: `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-e4f-premain-8e44ca9c`, detached `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- STARTUP RED probe worktree: `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-e4f-startup-ffd03934`, detached `ffd03934d0a86c98ed095d973e45587bd5751013`.
- Each worktree was sparse but included `rawlsing_next/`, `tests/`, and the required `WORKER_RETURNS` fixture trees. The canonical main worktree was not run in or modified.

## 2. Original E1 33-test receipt

Exact command (corrected cut):

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4f_e1_33.xml \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py
```

Result:

```
.................................                                        [100%]
33 passed in 0.89s
```

Exit `0`. JUnit: 33 tests, 0 failures, 0 skips.

Per module:

| Module | Tests | Pass | Fail | Skip |
|---|---:|---:|---:|---:|
| `test_rrif_e1_c3_d01_declared_encoding_admission.py` | 11 | 11 | 0 | 0 |
| `test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | 18 | 18 | 0 | 0 |
| `test_rrif_e1_c3_current_integration_regressions.py` | 4 | 4 | 0 | 0 |

Log: `rrif_e4f_e1_33.log`, 99 bytes, sha256 `dcb9a811bf7600c20479f572ecc990bcd8a4e91041e7c6dde3d3d5e64e13a804`.
JUnit: `rrif_e4f_e1_33.xml`, 6041 bytes, sha256 `19c112c0d8196f20a23c104b4a73dc73d7ccb974fa227c27fafa0a296aeb0f8e`.

## 3. New E4F D02 receipt

Exact command:

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4f_new12.xml \
  rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py
```

Result:

```
............                                                             [100%]
12 passed in 0.84s
```

Exit `0`. Log: `rrif_e4f_new12.log`, 99 bytes, sha256 `56e704d95947c3e8b5ccb43e1447bc0ef78d83d58fd44ecd76bd4b7fa1fa15c0`.
JUnit: `rrif_e4f_new12.xml`, 2373 bytes, sha256 `659494df5f95c2056b8a1770a10462923c4ecf97eef800b5419d6abb4077fe5f`.

## 4. Selected 194-pass / 1-skip compatibility receipt

Exact command (corrected cut):

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4f_selected_194.xml \
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

Result:

```
......................................................................s. [ 36%]
........................................................................ [ 73%]
...................................................                      [100%]
194 passed, 1 skipped in 142.18s (0:02:22)
```

Exit `0`. JUnit: 195 tests, 0 failures, 1 skip.

Per module:

| Module | Tests | Pass | Fail | Skip |
|---|---:|---:|---:|---:|
| `test_rrif_e1_c3_d01_declared_encoding_admission.py` | 11 | 11 | 0 | 0 |
| `test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | 18 | 18 | 0 | 0 |
| `test_rrif_e1_c3_current_integration_regressions.py` | 4 | 4 | 0 | 0 |
| `test_universal_source_byte_custody.py` (PR526) | 26 | 26 | 0 | 0 |
| `test_pre553_sr06_decoder_carrier.py` | 17 | 16 | 0 | 1 |
| `test_fiabc_lm1_r1e_n1_physical_boundary.py` | 7 | 7 | 0 | 0 |
| `test_fiabc_lm2_r1j_sav_representation_authority.py` | 9 | 9 | 0 | 0 |
| `test_fiabc_lits_i_representation_authority.py` | 10 | 10 | 0 | 0 |
| `test_universal_source_projection.py` | 31 | 31 | 0 | 0 |
| `test_universal_workload.py` | 16 | 16 | 0 | 0 |
| `test_r35_i01_physical_metadata.py` | 6 | 6 | 0 | 0 |
| `test_pre553_source_backed_c11_facade.py` | 10 | 10 | 0 | 0 |
| `tests/test_ee_p2x_darwin_court_driver.py` | 19 | 19 | 0 | 0 |
| `tests/test_fiabc_final_measurement_telemetry_closure.py` | 11 | 11 | 0 | 0 |
| Total | 195 | 194 | 0 | 1 |

The skip is `test_real_writer_dta_extended_missing_fixture_or_typed_dependency_limitation` in `test_pre553_sr06_decoder_carrier.py`: installed pyreadstat writer/readback does not expose `missing_user_values` in metadata. It is the same environmental writer limitation recorded by E1/E4 and is unrelated to D02.

Log: `rrif_e4f_selected_194.log`, 283 bytes, sha256 `af22e18d73fe5669072fd020a9c3062efbffe2255829dac1fcc885f634a339e8`.
JUnit: `rrif_e4f_selected_194.xml`, 32695 bytes, sha256 `ae104d2bbefcddbd428918625fb7f7256245c887fde59b25e1d1887e19fb3d5f`.

## 5. G01 hostile baseline severance

The G01 tests are out of D02 scope. They were run to prove the corrected cut does not change the two known hostile failures.

### 5.1 PREMAIN `8e44ca9c` hostile-only

Exact command (from the PREMAIN detached worktree):

```
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 \
  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4f_pytest_gcoff.py \
  -q -p no:cacheprovider --tb=short -rA \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4f_g01_baseline.xml \
  -k "native_to_canonical or special_states" \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py
```

Result:

```
FF                                                                       [100%]
...
2 failed, 6 deselected in 75.46s (0:01:15)
PYTEST_MAIN_RETURN 1
```

Exit `1`.

Failures:

- `test_native_to_canonical_mapping_authority_does_not_bridge_physical_representation`:
  `assert '47f141e43fb2a330ebd2286a0bb658eaa6320768d1bb75a0b969761731ace7bd' == 'b9b720335f373dc4f7874f32acd003732ba7947b22b9d3dbb6bc77cc283bf6e8'`.
- `test_special_states_remain_noncanonical_and_mapping_authority_does_not_leak`:
  `StopIteration` while locating the int special-state rule.

Log: `rrif_e4f_g01_baseline.log`, 1577 bytes, sha256 `9600e366ae6b2a585f313a47cf1d887baa69f30c1f0d64be93fc52bfb73aff51`.
JUnit: `rrif_e4f_g01_baseline.xml`, 1748 bytes, sha256 `4b0955e0a1ced79a7a6fb5f4efc504f4cdb328afb220806e5b0e3aaa47e40f93`.

### 5.2 Corrected cut full pair

Exact command (from the corrected worktree):

```
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 \
  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4f_pytest_gcoff.py \
  -q -p no:cacheprovider --tb=short -rA \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4f_g01_corrected_final.xml \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_inventory.py \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py
```

Result:

```
...F.F...                                                                [100%]
...
2 failed, 7 passed in 275.29s (0:04:35)
PYTEST_MAIN_RETURN 1
```

Exit `1`.

The two failures are the same test ids and identical assertion values as PREMAIN. The seven passes are the unchanged inventory/hostile controls.

Log: `rrif_e4f_g01_corrected_final.log`, 29567 bytes, sha256 `ddb76559db9a828d24e3479c5c76e467548e81048e7cf67e3df64792467dd5e2`.
JUnit: `rrif_e4f_g01_corrected_final.xml`, 2932 bytes, sha256 `97556167e91b8797fd8f41123db28c8d43bf239fc0eb9c0cf04766a3ec726060`.

### 5.3 G01 conclusion

`2 failed` on both PREMAIN and corrected cut, with the same node ids and assertion values. This is causal severance: D02 did not introduce, repair, or claim the G01 representation-authority defect. G01 authority remains `HELD`.

The GC wrapper disables cyclic GC before `pytest.main` and exits with the pytest return code. It changes no test file, test option, production code, or assertion. It is an execution-environment workaround for the long GC traversal observed by E4.

## 6. Compatibility conclusion

- D01 exact declared-encoding admission: green.
- PR526 content-bound custody: green.
- SAV finite-float exact representation: green.
- C11/projection and EE-P2X selected integration: green.
- Original E1 33: green.
- Selected 194/1: green.
- G01: two pre-existing failures unchanged, `HELD`.

## 7. NOT_RUN

- No actual raw survey source decode was performed.
- No WVS7/LITS raw source was opened.
- No full repository suite was run.
- No G01 repair was attempted.
- No PREMAIN merge, PR, force push, adoption, or self-review occurred.
