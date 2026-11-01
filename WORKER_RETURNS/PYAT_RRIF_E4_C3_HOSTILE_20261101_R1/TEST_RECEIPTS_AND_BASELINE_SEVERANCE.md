# TEST RECEIPTS AND BASELINE SEVERANCE

## 1. Environment and isolation

- Host: mainMac.lan, macOS 13.2.1 (22D68), Darwin 22.3.0, x86_64.
- Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1, numpy 2.3.2.
- OpenCode 1.18.34. Live argv: `--model opencode-go/deepseek-v4.1-flash --variant max --agent build`.
- Session DB read-only: `ses_e6a83623fffem6ygKUq43tr0q1`, `{"id":"deepseek-v4.1-flash","providerID":"opencode-go","variant":"max"}`, agent `build`, version `1.18.34`, directory equal to this worktree.
- Test worktree: `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-e4-e1-ffd03934`, detached HEAD `ffd03934d0a86c98ed095d973e45587bd5751013`.
- Test worktree was sparse (code/tests plus required fixture paths) because the full checkout was blocked by disk pressure. `rawlsing_next` was 8.6 MB and top-level `tests` 120 KB.
- The 83,340,882-byte R1F carrier fixture was symlinked read-only from the E1 worktree only after content identity was verified: blob `665fb2ae2f254e2e66014ede840ca55d275296d5`, sha256 `1aea888d8d576fc8606d56dd7a3b1a552411b8f8126ea27a54c36ff6d551dd7e`.
- The E1 worktree was never run in or modified. Its HEAD remained `ffd03934d0a86c98ed095d973e45587bd5751013` and its status was clean. The canonical main worktree remained at `25830fe7462bb9e29bc4087e6ae14f3f84cec377`.
- Pytest was run with `PYTHONDONTWRITEBYTECODE=1 -p no:cacheprovider` where noted to avoid writing caches into the temporary worktree.

Important transparency note: the first 194-file attempt failed five `test_fiabc_lm2_r1j_sav_representation_authority.py` cases because the sparse checkout lacked `WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py` and `WORKER_RETURNS/FIABC-LM2/wvs7_projection_structural_input.json`. These were fixture-availability failures, not code failures. The required fixture trees were added from the same E1 tree and the whole suite was rerun. The clean final run is the authoritative receipt below.

## 2. Targeted 33-test receipt

Exact command (run from the E1 detached worktree):

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4_33.xml \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py
```

stdout:

```
.................................                                        [100%]
33 passed in 1.20s
```

Exit: `0`.
Log: `rrif_e4_33.log`, size 99, sha256 `c1fe0cc579d54b5941b97d3b5f61aebf88dcda4c44b5cba4ed8e7f4398c3e96a`.

Per-file:

| File | Tests |
|---|---|
| `test_rrif_e1_c3_d01_declared_encoding_admission.py` | 11 |
| `test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | 18 |
| `test_rrif_e1_c3_current_integration_regressions.py` | 4 |
| Total | 33 |

Coverage limitation: the D02 file exercises exact built-in date/time and one-level item wrappers directly. It does not exercise a real pyreadstat-decoded `DATETIME` (`pandas.Timestamp`) or an aware `Timestamp`/`datetime` subclass. The 33 green cases therefore do not contradict the real-consumer RED in `00_RETURN.md`.

## 3. Selected 194-pass / 1-skip suite receipt

Exact command (run from the E1 detached worktree):

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4_194_final.xml \
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

stdout:

```
......................................................................s. [ 36%]
........................................................................ [ 73%]
...................................................                      [100%]
194 passed, 1 skipped in 158.03s (0:02:38)
```

Exit: `0`.
Log: `rrif_e4_194_final.log`, size 283, sha256 `7ecee21f46cdc8fd52697d24608c4233972cf80598c1193a91a3f0b726daaa6f`.

Per-module counts parsed from JUnit XML:

| Module | Tests | Pass | Skip | Fail |
|---|---:|---:|---:|---:|
| `test_rrif_e1_c3_d01_declared_encoding_admission.py` | 11 | 11 | 0 | 0 |
| `test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | 18 | 18 | 0 | 0 |
| `test_rrif_e1_c3_current_integration_regressions.py` | 4 | 4 | 0 | 0 |
| `test_universal_source_byte_custody.py` (PR526) | 26 | 26 | 0 | 0 |
| `test_pre553_sr06_decoder_carrier.py` | 17 | 16 | 1 | 0 |
| `test_fiabc_lm1_r1e_n1_physical_boundary.py` (SAV boundary) | 7 | 7 | 0 | 0 |
| `test_fiabc_lm2_r1j_sav_representation_authority.py` (SAV representation) | 9 | 9 | 0 | 0 |
| `test_fiabc_lits_i_representation_authority.py` | 10 | 10 | 0 | 0 |
| `test_universal_source_projection.py` (C11/projection) | 31 | 31 | 0 | 0 |
| `test_universal_workload.py` | 16 | 16 | 0 | 0 |
| `test_r35_i01_physical_metadata.py` | 6 | 6 | 0 | 0 |
| `test_pre553_source_backed_c11_facade.py` | 10 | 10 | 0 | 0 |
| `tests/test_ee_p2x_darwin_court_driver.py` | 19 | 19 | 0 | 0 |
| `tests/test_fiabc_final_measurement_telemetry_closure.py` | 11 | 11 | 0 | 0 |
| Total | 195 | 194 | 1 | 0 |

The skip is `test_real_writer_dta_extended_missing_fixture_or_typed_dependency_limitation` in `test_pre553_sr06_decoder_carrier.py:268`: installed pyreadstat writer/readback does not expose `missing_user_values` in metadata. It is an environmental writer limitation, unrelated to D01/D02 and not counted as a pass.

## 4. G01 hostile baseline severance

### E1 tree, full G01 pair

Command (run from the E1 detached worktree):

```
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 \
  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4_pytest_gcoff.py \
  -q -p no:cacheprovider --tb=line \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4_g01_e1_gcoff.xml \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_inventory.py \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py
```

Result:

```
2 failed, 7 passed in 287.93s (0:04:47)
PYTEST_MAIN_RETURN 1
```

Exit: `1`.
Log: `rrif_e4_g01_e1_gcoff.log`, size 28252, sha256 `77b45bcd5e5c936afff525b2bbeabc01689ff5b610fd4866e6b8b63384d9e937`.

Exact failures:

- `test_native_to_canonical_mapping_authority_does_not_bridge_physical_representation`:
  `assert '47f141e43fb2a330ebd2286a0bb658eaa6320768d1bb75a0b969761731ace7bd' == 'b9b720335f373dc4f7874f32acd003732ba7947b22b9d3dbb6bc77cc283bf6e8'`.
- `test_special_states_remain_noncanonical_and_mapping_authority_does_not_leak`:
  `StopIteration` when looking up the int special-state rule.

### E1 tree, hostile-only control

```
2 failed, 6 passed in 235.46s (0:03:55)
PYTEST_MAIN_RETURN 1
```

Log: `rrif_e4_g01_hostile_e1_gcoff.log`, sha256 `c141a195667239a8da362222974f780449b109605e6b08cdcb878474cf5e4cda`.

### PREMAIN baseline worktree

A separate detached worktree was created at PREMAIN `8e44ca9c751049d65e6def47600b5c073ee04b29` with the same sparse code/tests and fixture trees. Its HEAD and the carrier blob were verified (`665fb2ae…`). No E1 worktree was used for this baseline.

Command:

```
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 \
  /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4_pytest_gcoff.py \
  -q -p no:cacheprovider --tb=short \
  -k "native_to_canonical or special_states" \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py
```

Result:

```
2 failed, 6 deselected in 78.53s (0:01:18)
PYTEST_MAIN_RETURN 1
```

Exit: `1`.
Log: `rrif_e4_g01_premain_baseline.log`, size 1577, sha256 `f8ef7864b470a4efd44b03e2839248537046ad8342b72a2bdd02a324a5c9ba93`.

The failed assertions and observed key values are identical to E1. This is causal severance: the two G01 failures are pre-existing at PREMAIN and are not repaired or claimed in scope by E1. G01 authority remains HELD.

### GC execution note

The plain G01 invocation (without the wrapper) completed all nine case results and then spent beyond a 300 s tool limit in repeated Python GC traversal. Native `sample` showed the main thread in `gc_collect_main` / `_PyObject_GC_Link`, with a 552 MB physical footprint; this was not an I/O or assertion hang.

The final G01 receipts use a wrapper that calls `gc.disable()` before `pytest.main(...)`, prints `PYTEST_MAIN_RETURN`, and `os._exit`s. It changes no test file, no test option, and no production code. The test bodies and assertions are unchanged. The wrapper is an execution-environment workaround only; the failure values are identical in the hostile-only and baseline runs.

## 5. Independent adversarial probe receipts

Probe scripts were written outside the repository. They are not production artifacts and are not part of the fan-in.

### D01 probe

- Exact C3/C3-parent/E1 allowlist equality.
- Wrong SHA/encoding, cross-pair, lowercase, `latin1`, `UTF-8`, `auto`, `guess`, `fallback` refusal.
- Compatibility lane conservation.
- Synthetic SAV and DTA end-to-end for both `BIG5` and `WINDOWS-1252` with in-memory test-only SHA binding.

Result: all D01 probes passed. Probe source sha256 `e204fd60924472c1c1341980e0f881b5177307a43ed9994ca55481783b9ac085` (matrix including D02/custody probes).

### D02 built-in and nested probe

- Exact carrier payloads and fold for date/time/datetime.
- Aware exact built-in and one-level item-wrapped aware refusal.
- One-level naive item unwrap.
- Recursive item chain not manufactured into a carrier.
- Nested tuple/list/mapping and date mapping key normalization, R5 round-trip.
- Date strings not reinterpreted; bare codec date refusal.

Result: all built-in probes passed.

### D02 real consumer and subclass probe

Real SAV and DTA files with `date`, `time`, `datetime`, float columns, decoded by E1 and then passed through pinned `pre553_r5_seam.iter_source_native_rows`:

```
SAV tags: {'d': 'opaque', 't': 'opaque', 'dtm': 'str', 'f': 'float64_finite'}
DTA tags: {'d': 'opaque', 't': 'opaque', 'dtm': 'str', 'f': 'float64_finite'}
```

Plain subclass controls:

```
NaiveDT(2008,4,5,6,7,8) -> str '2008-04-05 06:07:08'
AwareDT(2008,4,5,6,7,8,tzinfo=UTC) -> str '2008-04-05 06:07:08+00:00'
ItemWrapper(AwareDT(..., tzinfo=UTC)) -> str '2008-04-05 00:00:00+00:00'
```

`opaque_decoder_value` rejects these as `unsupported opaque decoder value type ...`; the decoder route never reaches that refusal because it stringifies first. Probe source sha256 `3280edd6299bb3aa98be7817726502dd2dcab23ca8ca04fb4bb8f64a5d5ea9fa`.

Secondary classifier probe:

```
classify_physical_value(opaque_decoder_value(date), ({"kind":"range","lo":1,"hi":2},))
-> TypeError: '<=' not supported between instances of 'int' and 'R5OpaqueValue'
```

A synthetic real SAV date column with a user-missing range could not be written by this pyreadstat version (`missing_ranges` requires numeric or string values), so this is an API-level witness; it is recorded as a pre-existing HOLD.

### Custody / tamper / float probe

- Snapshot sha equals source sha; `reader_binding == OPEN_FD_VIA_POSIX_DEV_FD`; `reader_access_mode == O_RDONLY`; `snapshot_path_unlinked == True`; `content_bound == True`.
- `fcntl(F_GETFL) & O_ACCMODE == O_RDONLY`; reader fd is a regular file; `reader_path == /dev/fd/<fd>`; path gone.
- Original path tamper after acquisition: cells and identity unchanged.
- Tamper before decode with expected SHA: `source sha256 mismatch before governed decode`.
- Malformed expected SHA: refused.
- SAV finite floats: Python `float`, R5 tag `float64_finite`, exact values `[1.5, -2.25, 0.0]`.
- Close: access mode `CLOSED`, idempotent.

Result: all custody/float probes passed. pyreadstat read of a fresh synthetic SAV retained `["score","label"]`, 3 rows.

## 6. NOT_RUN

- No raw survey source was opened or decoded under any of the three declared encodings. D01 end-to-end uses synthetic bytes and a test-only in-memory binding only. Actual source-use qualification remains HELD.
- No actual WVS7/LITS raw source was read; no raw-source date/time presence claim is made.
- No full-repository test suite was run; only the mandated 33, selected 194/1, G01, and the independent probes above.
- No timezone-aware carrier authority was granted or exercised; aware built-ins are refused, aware subclasses currently fail open to string and are the RED.
- No G01 repair or representation-coercion change was attempted.
- No PREMAIN/main/Sorok/native/protected source/actor/R9/S3 execution, merge, PR, force push, adoption, or self-review occurred.
