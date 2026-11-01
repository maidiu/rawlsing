# POSITIVE AND NEGATIVE TESTS

## Environment

- Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1.
- S2 exclusive local Git worktree; sourcefree execution only.
- All generated SAV/DTA fixtures are synthetic `tmp_path` bytes. No raw survey source, native/protected source, or S3 execution was used.

## New frozen test files

| File | Blob | Cases |
|---|---|---|
| `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py` | `625f1d8b1f3fa8c24501addcaff7d70209598596` | 9 functions / 11 cases |
| `rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | `ac5f331322a69dab224eeeda14b05681918b432e` | 14 functions / 18 cases |
| `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py` | `bfa20f7a35ef9a399bec5380b6c3e6f9caad0115` | 4 functions |

The D01 and D02 accepted oracles are ported from original accepted tests (`105246b33` and `5fbf9cc56`) and frozen against the current receiver. New fault cases are added without changing the accepted positive oracle.

## Positive evidence

### D01 positives

- `test_declared_encoding_allowlist_is_exact_and_distinct_from_compatibility_lane`
- `test_declared_encoding_admission_is_sha_and_encoding_exact`
- `test_no_encoding_override_remains_unprivileged`
- `test_existing_exact_sha_compatibility_lane_is_conserved`
- `test_declared_lane_does_not_authorize_text_semantics_or_cross_source_inheritance`
- `test_declared_lane_decodes_end_to_end_with_test_only_synthetic_binding`

The end-to-end positive binds a synthetic SHA to the declared lane only inside the test, then exercises `decode_sav` through the current PR526 snapshot and full-read path. It confirms `encoding == "BIG5"` and `authority_status == SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY`. It does not add a production pair or authorize raw source use.

### D02 positives

- Exact built-in date/time values require the explicit opaque carrier; bare codec encoding still fails.
- Payload bytes and `fold` are exact for date, time, and datetime.
- Nested tuple/list/mapping normalization works, including a date-valued mapping key and a fold-bearing datetime value.
- Direct and one-level `.item()` unwrapped naive values become `R5OpaqueValue`.
- The unchanged facade can bind opaque carriers directly; distinct carrier payloads produce distinct 64-hex binding keys.
- D01 and D02 compose on the same current decoder without cross-authority.

### Current integration positives

- `test_current_pr526_custody_and_sav_float_representation_survive_repair`
  - private content-bound snapshot, `snapshot_sha256 == source_sha256`, `reader_binding == OPEN_FD_VIA_POSIX_DEV_FD`, `reader_access_mode == O_RDONLY`, snapshot path unlinked, `verify_source_identity()` stable;
  - SAV float cells remain Python `float` and encode in the `float64_finite` R5 lane.
- `test_pr526_snapshot_survives_original_path_tamper`
  - tampering the original path after acquisition does not change the bound snapshot identity or its decoded cells.
- `test_actual_decoder_consumer_decode_regression`
  - calls the real `ee_p2x_darwin_stage_backend._decode` consumer, verifies source counters, READ evidence, variables, and decoded float cells.

## New frozen negative fault cases

### Wrong hash plus wrong encoding

- `test_fault_wrong_hash_and_wrong_encoding_remain_closed`
  - `BIG5` SHA with `WINDOWS-1252` is refused.
  - `WINDOWS-1252` SHA with `BIG5` is refused.
  - unknown 64-hex SHA with either encoding is refused.
- `test_fault_synthetic_source_is_refused_by_declared_lane_end_to_end`
  - a real synthetic SAV whose SHA is not in the exact declared map is refused end-to-end with `exact SHA/config representation allowlist`.
  - `auto` is refused with `automatic encoding guessing/fallback is forbidden`.
- `test_automatic_encoding_guessing_remains_forbidden` covers `auto`, `guess`, and `fallback`.

### Source tamper

- `test_fault_source_tamper_before_decode_is_refused`
  - the source SHA is captured, one byte is changed, and `decode_sav(..., expected_source_sha256=<old>)` refuses with `source sha256 mismatch before governed decode`.
- `test_pr526_snapshot_survives_original_path_tamper` is the positive custody control: after content-bound acquisition, path tampering cannot rebind the original identity or cells.

### Timezone-aware datetime/time

- `test_timezone_aware_values_fail_closed_at_carrier_and_decoder_route` covers aware datetime and aware time at both `opaque_decoder_value` and `_physical_value`.
- `test_item_unwrapped_timezone_aware_values_fail_closed` covers the same aware values behind a one-level `.item()` wrapper.
- Expected refusal: `separate explicit decoder carrier authority`.

### Date-as-string

- `test_fault_date_as_string_is_not_reinterpreted_as_date` covers `"2008-04-05"`, `"06:07:08"`, `"2008-04-05T06:07:08"`, and `"2008/04/05"`.
- Strings remain strings through normalization and the decoder route, encode in the `str` R5 lane, and their binding key differs from the opaque date carrier.

### Recursion misuse

- `test_fault_recursive_item_unwrapping_does_not_manufacture_opaque_carrier`
  - a two-level `.item()` chain that eventually reaches a date is not recursively chased; the original one-level seam stringifies through `_jsonable`, exactly as the accepted code does.
- `test_fault_codec_normalization_does_not_expand_item_wrappers`
  - `normalize_decoder_physical_value` recurses only through tuple/list/mapping; it does not expand arbitrary `.item()` wrappers into opaque carriers.
- The positive nested normalization test keeps the intended container recursion for tuple/list/mapping and fold carriage.

### Original-current behavior

- `test_fault_original_current_jsonable_and_scalar_lanes_are_unchanged`
  - `_jsonable(date)` still returns `"2008-04-05"` (the generic helper is unchanged);
  - `_physical_value` preserves `None`, `bool`, `int`, `float`, `str`, tuple-to-list, and mapping behavior for non-date values;
  - codec int/float/bool distinctions remain;
  - bare `R5.encode(date)` still raises `date/time meaning may not be invented`.
- `test_string_masquerade_and_unrelated_scalar_lanes_remain_distinct` freezes the string/opaque distinction.
- `test_existing_exact_sha_compatibility_lane_is_conserved` freezes the pre-existing `latin1` lane.

## Executed commands and return codes

### New targeted files

```
python3 -m pytest -q \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py
```

`33 passed`, exit `0`.

### Final combined selected suite

```
python3 -m pytest -q \
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

`194 passed, 1 skipped` in 151.98s, exit `0`.

Per-module passed counts: new files `33`; PR526 custody `26`; SR06 `16` plus `1 skipped`; SAV physical boundary `7`; SAV representation authority `9`; LITS representation authority `10`; universal source projection `31`; universal workload `16`; R35 physical metadata `6`; source-backed C11 facade `10`; EE-P2X court driver `19`; final measurement telemetry `11`.

### Pre-existing G01 hostile red, not a D01/D02 regression

```
python3 -m pytest -q \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_inventory.py \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py
```

Repaired tree: `2 failed, 7 passed`, exit `1`.

```
python3 -m pytest -q rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py \
  -k "native_to_canonical or special_states"
```

Startup baseline `8e44ca9c751049d65e6def47600b5c073ee04b29` with the two production files stashed: `2 failed, 6 deselected`, exit `1`. Identical assertion values. Stash pop exit `0`.

The two failures are G01 int/float hostile expectations:

- expected int key `b9b720335f373dc4f7874f32acd003732ba7947b22b9d3dbb6bc77cc283bf6e8`, observed projection float key `47f141e43fb2a330ebd2286a0bb658eaa6320768d1bb75a0b969761731ace7bd`;
- no int-key special-state rule.

G01 authority remains HELD; numeric coercion was not broadened.

## Test limitation

The exact three D01 source SHA values cannot be exercised against their real raw source files in this sourcefree envelope. The positive lane is therefore tested with a test-only synthetic binding, and the exact production pairs are frozen by equality of the mapping, not by raw-source decode. Actual raw-source qualification remains with the PRE-MAIN physical-decoder/source-rights owner.
