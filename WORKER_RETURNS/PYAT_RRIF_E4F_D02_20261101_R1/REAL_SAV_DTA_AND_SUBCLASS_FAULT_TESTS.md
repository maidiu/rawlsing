# REAL SAV/DTA AND SUBCLASS FAULT TESTS — RRIF-E4F D02

## 1. Purpose and execution surface

This receipt records the source-free real pyreadstat fixtures that reach the actual decoder cell route and the actual pinned first R5 seam consumer, plus the subclass/aware/lossy negative tests.

Execution environment:

- Host `mainMac.lan`, macOS 13.2.1 (22D68), Darwin 22.3.0, x86_64.
- Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1, numpy 2.3.2.
- Worktree `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1`.
- No raw survey source, native source, Sorok, PROGRAMMA, R9, actor, or production route was opened.

## 2. Real SAV and DTA fixture

The test builds an in-memory pandas frame and writes a temporary source-free file with the installed pyreadstat writer:

```python
frame = pd.DataFrame({
    "dtm": pd.to_datetime(["2008-04-05 06:07:08", "2009-05-06 07:08:09"]),
    "score": [1.5, -2.25],
    "label": ["a", "b"],
})
pyreadstat.write_sav(frame, path)   # SAV case
pyreadstat.write_dta(frame, path)   # DTA case
```

The pyreadstat reader returns pandas `Timestamp` for the `DATETIME` column, which is the E4-decoded real type. The test then calls:

- `decoder.decode_sav(path)` / `decoder.decode_dta(path)`,
- `PhysicalSourceIncidence.iter_cells(2)`,
- `R5TypedValueCodec.encode`,
- and the pinned seam `iter_source_native_rows`.

No raw source bytes or survey files are used.

## 3. Pinned first R5 seam consumer

`rawlsing_next/pre553_r5_seam.py` and `rawlsing_next/pre553_r5_model.py` are not tracked at STARTUP_SHA `ffd03934d`. The accepted historical first consumer is pinned at:

- Owner commit: `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`
- `rawlsing_next/pre553_r5_seam.py` Git blob: `cef326ebbc40468428378f7fdbe76e4756179f39`
- seam sha256: `626f74200a11dd8f749bead1ebd904eae22b65246636395a16df60d33d2b052f`
- `rawlsing_next/pre553_r5_model.py` Git blob: `62ce608829c3d9c2fb7c999aefe40188637edf80`
- model sha256: `cdb8a2581aeed7f24acd668f3b93ca23244f64820266e5d282fb65915c17ac3a`

The test helper `_pinned_seam()`:

1. uses an importable `rawlsing_next.pre553_r5_seam` if one exists;
2. otherwise reads the exact pinned seam and model sources from the local Git object database with `git cat-file -p`;
3. verifies both Git blob hashes with `git hash-object --stdin`;
4. verifies both SHA-256 digests;
5. loads them as test-only modules and executes the actual `iter_source_native_rows`.

This is a test-only historical-object read. It adds no production seam file, invents no seam source, and reads no network or survey source. If the objects are absent, the test fails with a precise message rather than silently skipping the real-consumer requirement.

## 4. Passing D02 tests

Exact command:

```
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  --junitxml=/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif_e4f_new12.xml \
  rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py
```

Result: `12 passed in 0.84s`; exit `0`.

Tests:

1. `test_real_sav_and_dta_datetime_cells_are_opaque_at_cells_and_first_seam[sav-write_sav-decode_sav]`
2. `test_real_sav_and_dta_datetime_cells_are_opaque_at_cells_and_first_seam[dta-write_dta-decode_dta]`
3. `test_real_datetime_custody_and_wrong_source_tamper_remain_content_bound`
4. `test_naive_timestamp_and_subclasses_canonicalize_to_exact_carrier`
5. `test_naive_date_time_subclasses_and_nested_fold_are_preserved`
6. `test_recursive_item_chasing_is_not_manufactured_into_a_carrier`
7. `test_aware_datetime_subclasses_and_item_wrappers_refuse_explicitly[value0]` (plain aware `datetime` subclass)
8. `test_aware_datetime_subclasses_and_item_wrappers_refuse_explicitly[value1]` (aware pandas `Timestamp`)
9. `test_aware_time_subclass_refuses_explicitly`
10. `test_lossy_date_like_subclasses_refuse_before_any_string_fallback`
11. `test_opaque_datetime_range_declaration_refuses_with_typed_decoder_error`
12. `test_private_physical_value_is_not_exported_but_public_classifier_remains`

## 5. Real fixture assertions

For both SAV and DTA:

- `dtm` cells from `iter_cells` are exactly `R5OpaqueValue`.
- They are not `str`.
- `type_id == "python.datetime.datetime@1"`.
- `struct.unpack(">HBBBBBIB", payload)` equals the exact civil tuple, including zero fold.
- `R5TypedValueCodec.encode(cell.raw_value)` has `t == "opaque"` and the same `type_id`.
- The pinned seam `source_physical_cells` rows for `dtm` have `payload["raw_value"]["t"] == "opaque"` and are asserted not to be `"str"`.
- The `score` cells remain Python `float`, and encoded bits equal the exact IEEE-754 `struct.pack(">d", value).hex()` for `1.5` and `-2.25`.

The custody test additionally verifies:

- expected-SHA decode succeeds and the content-bound snapshot survives tamper of the original path;
- the `dtm` cells remain opaque after that tamper;
- a pre-decode tamper refuses with `source sha256 mismatch before governed decode`;
- the snapshot closes with `access_mode == "CLOSED"`.

## 6. Pre-patch RED witness at STARTUP_SHA

A detached sparse worktree at `ffd03934d0a86c98ed095d973e45587bd5751013` was executed separately from this branch. It reproduced the E4 defect on the same real fixtures:

```
sav str '2008-04-05 06:07:08' str
dta str '2008-04-05 06:07:08' str
AwareDT str '2008-04-05 00:00:00+00:00'
Wrapper str '2008-04-05 00:00:00+00:00'
```

Log: `rrif_e4f_startup_red_probe.log`, 148 bytes, sha256 `7abd279823b2871fd08d5530e6e1355f08e736cce46e3deadac0a09df579caa0`.

## 7. Corrected GREEN witness

Same probe on the corrected cut:

```
sav R5OpaqueValue python.datetime.datetime@1 opaque
dta R5OpaqueValue python.datetime.datetime@1 opaque
AwareDT REFUSED timezone-aware datetime requires a separate explicit decoder carrier authority
Wrapper REFUSED timezone-aware datetime requires a separate explicit decoder carrier authority
```

Log: `rrif_e4f_corrected_probe.log`, 294 bytes, sha256 `b96fd08b6ecf8d885654995c01d4fb562f7dae6204a78b9c1d316e8799713bd4`.

## 8. Subclass, fold, and precision boundary

- Plain naive `datetime` subclass with `microsecond=901234, fold=1`: carrier payload `(2008, 4, 5, 6, 7, 8, 901234, 1)`.
- pandas `Timestamp` built from the same civil fields: identical payload.
- One-level `.item()` wrapper returning that naive value: identical carrier.
- Nested list/dict/mapping-key normalization: naive subclasses carry; date keys carry.
- Aware plain subclass, aware `Timestamp`, aware `time` subclass, and one-level wrappers returning them: explicit `R5CodecError` authority refusal at direct, carrier, and recursive-normalizer routes.
- pandas `Timestamp` with nonzero `nanosecond`: typed refusal `sub-microsecond precision cannot be preserved by the versioned opaque carrier`.
- `pandas.NaT`: typed refusal `cannot be safely canonicalized to a naive datetime carrier`.
- Hostile subclass whose `tzinfo` property raises: typed `cannot expose tzinfo safely`.
- Hostile subclass whose `year` property raises: typed `cannot be safely canonicalized to a naive datetime carrier`.
- Recursive item chain around a naive date: not converted to a carrier; the accepted E1 non-carrier fallback is preserved.

## 9. Opaque carrier vs range declaration

`classify_physical_value(opaque_decoder_value(datetime(2008, 4, 5, 6, 7, 8)), ({"kind": "range", "lo": 1, "hi": 2},))` now raises:

```
DecoderError: physical value cannot be compared with a declared missing range (value_type=R5OpaqueValue)
```

The test asserts this is a `DecoderError`, not a `TypeError`, and that the message names `R5OpaqueValue`. This resolves the E4 secondary HOLD by typed refusal rather than guessing range membership.

## 10. Export boundary

The test asserts:

- `"_physical_value" not in decoder.__all__`
- `"classify_physical_value" in decoder.__all__`

Direct tests still call the private helper, as E1 did; the private name is no longer public API surface.

## 11. No string fallback for tested date-like cases

The new tests assert `not isinstance(raw_value, str)` for real DATETIME cells and for naive subclass carriers, and assert explicit `R5CodecError` for each aware/lossy date-like case. No test accepts a stringified date/time as a pass condition for the repaired route.
