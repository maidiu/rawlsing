# EXACT REVIEWED HUNKS AND SOURCE BLOBS — PYAT RRIF-E4FR D02 FINAL

## 1. Frozen and live basis

- Reviewer branch: `review/pyat-rrif-e4fr-d02-corrected-consumer-hostile-20261101-r1`.
- Branch start / live PREMAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29` on `refs/heads/integration/pre-main-reconciliation-r1`.
- E1 parent / correction base: `ffd03934d0a86c98ed095d973e45587bd5751013`.
- E4F corrected head: `f2c0af3273d612bff0a7bd2407532b52caf4348b`.
- E4 previous hostile return: `5dc00a1eb0d2881a9d74661b7a94d436cc7b7c60`.
- Live E4F remote: `refs/heads/agent/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1` = `f2c0af3273d612bff0a7bd2407532b52caf4348b`.
- Live `main`: `25830fe7462bb9e29bc4087e6ae14f3f84cec377`.
- E4F parent verified: `git rev-parse f2c0af32^` = `ffd03934d0a86c98ed095d973e45587bd5751013`.

The correction is a direct child of E1. No rebase, merge, or unrelated history is involved.

## 2. Exact changed-file allowlist at E4F

`git diff --name-only ffd03934 f2c0af32`:

```
WORKER_RETURNS/PYAT_RRIF_E4F_D02_20261101_R1/00_RETURN.md
WORKER_RETURNS/PYAT_RRIF_E4F_D02_20261101_R1/COMPATIBILITY_AND_G01_BASELINE.md
WORKER_RETURNS/PYAT_RRIF_E4F_D02_20261101_R1/EXACT_PATCH_AND_SOURCE_BLOBS.md
WORKER_RETURNS/PYAT_RRIF_E4F_D02_20261101_R1/FANIN_SCOPE.md
WORKER_RETURNS/PYAT_RRIF_E4F_D02_20261101_R1/REAL_SAV_DTA_AND_SUBCLASS_FAULT_TESTS.md
rawlsing_next/pre553_physical_decoder.py
rawlsing_next/pre553_r5_codec.py
rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py
```

No other file is changed. The five return documents are documentary; the only production changes are the two `rawlsing_next/pre553_*.py` files; the only new test is the bounded D02 file.

## 3. Git blob and sha256 identities

| Path at E4F | Git blob | sha256 |
|---|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `4b89c4598f324834de064c1200c63698a20e3c5c` | `f9794976aef51c418e8152850a7b0143df6790d0596549ea7f0991fc1f4501e9` |
| `rawlsing_next/pre553_r5_codec.py` | `f5f64d9b8b6c9af1d1b755f86b44fe43a8e741b7` | `fc3aaec95d1ea6b396afb7484e5b58a242a878f9a003b47a30d7f35d48eaa9ae` |
| `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` | `c07c2019455e6264b4297c1c1d782bd887b96bdd` | `1042789d92c94dd5ef983299f4cbc46b40bc55e2d556f055f6777ada11254737` |

E1 STARTUP production blobs, confirmed as the parent state:

| Path at E1 | Git blob |
|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `d60e092f9ee0948acc79b32ebe8f2f5aa7096928` |
| `rawlsing_next/pre553_r5_codec.py` | `6000a1704d713f65e07610d81e9b3fd8bdd515ca` |

Original E1 test allowlist, unchanged and green at E4F (33 tests):

| Path | Git blob at E4F | Tests |
|---|---|---|
| `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py` | `625f1d8b1f3fa8c24501addcaff7d70209598596` | 11 |
| `rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | `ac5f331322a69dab224eeeda14b05681918b432e` | 18 |
| `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py` | `bfa20f7a35ef9a399bec5380b6c3e6f9caad0115` | 4 |

Pinned historical first-consumer blobs, test-only, loaded from the local Git object database:

| Object | Git blob | sha256 |
|---|---|---|
| `rawlsing_next/pre553_r5_seam.py` at owner `0b96b8de9aac774566f872cf0630ebd4ddeb70e6` | `cef326ebbc40468428378f7fdbe76e4756179f39` | `626f74200a11dd8f749bead1ebd904eae22b65246636395a16df60d33d2b052f` |
| `rawlsing_next/pre553_r5_model.py` at same owner | `62ce608829c3d9c2fb7c999aefe40188637edf80` | `cdb8a2581aeed7f24acd668f3b93ca23244f64820266e5d282fb65915c17ac3a` |

`pre553_r5_seam.py` is absent from the E4F tree; the test-only loader is described in §6 of `00_RETURN.md`.

## 4. Reviewed hunks — `rawlsing_next/pre553_physical_decoder.py`

`git diff --unified=0 ffd03934 f2c0af32` hunk headers:

```
@@ -429 +429,8 @@ def _physical_value(value: Any) -> Any:
@@ -431 +438 @@ def _physical_value(value: Any) -> Any:
@@ -439 +446 @@ def _physical_value(value: Any) -> Any:
@@ -570,2 +577,12 @@ def classify_physical_value(...)
@@ -852 +868,0 @@ __all__ = [
```

### 4.1 `_physical_value`, lines 428–448 — ACCEPT at bounded scope

Actual reviewed code:

- Direct gate changed from exact `type(value) in {datetime, date, time}` to `isinstance(value, (datetime, date, time))`, then `normalize_decoder_physical_value(value)`.
- One-level `.item()` unwrap unchanged except the returned item gate is now `isinstance(...)`.
- If the one-level item is not a date-like, control falls to `_jsonable(value)` exactly as at E1.
- Direct aware built-ins/subclasses and one-level wrapped aware values therefore reach the codec canonicalizer and refuse with `R5CodecError`; they cannot reach `_jsonable`.
- A two-or-more-level `.item()` chain is still not chased by `_physical_value`; `_jsonable` itself recursively calls `.item()`, so a hidden aware value at depth ≥2 can still be stringified. This is the disclosed bounded-scope residual; see `00_RETURN.md` §5. It is not reachable from the real pyreadstat SAV/DTA cell route and is not a blocker for the accepted one-level D02 promise.
- The docstring phrase "they never fall through to the string lane" is accurate for the direct and one-level argument it handles, but should not be read as a recursive-depth guarantee. The return's `FANIN_SCOPE.md` explicitly disclaims recursive chains.

### 4.2 `classify_physical_value`, lines 569–589 — ACCEPT

For `kind == "range"`, `lo`/`hi` are read once and the comparison is wrapped:

```
try:
    in_range = lo <= value <= hi
except TypeError as exc:
    raise DecoderError(
        "physical value cannot be compared with a declared missing range "
        f"(value_type={type(value).__name__})"
    ) from exc
```

Review:

- An `R5OpaqueValue` date/time carrier versus numeric `lo`/`hi` now raises typed `DecoderError`, not uncontrolled `TypeError`.
- The message names `R5OpaqueValue`; `from exc` preserves cause.
- Discrete/extended branches and the final observed-storage return are unchanged.
- Only `TypeError` is converted. A non-`TypeError` from a hostile comparison implementation would still propagate; no current source path constructs one, and the mandate's opaque-vs-numeric case is covered.

### 4.3 `__all__`, lines 853–869 — ACCEPT

`_physical_value` is removed from `__all__`. The private helper remains callable by the decoder route and direct tests; `classify_physical_value` remains public. This resolves the E4 secondary API-surface HOLD without changing behavior.

## 5. Reviewed hunks — `rawlsing_next/pre553_r5_codec.py`

`git diff --unified=0` hunk headers:

```
@@ -39,4 +39,16 @@ class R5OpaqueValue:
@@ -43,0 +56,47 @@ def opaque_decoder_value(value: Any) -> R5OpaqueValue:
@@ -46,2 +105,2 @@ def opaque_decoder_value(value: Any) -> R5OpaqueValue:
@@ -50 +109 @@ def opaque_decoder_value(value: Any) -> R5OpaqueValue:
@@ -53 +112 @@ def opaque_decoder_value(value: Any) -> R5OpaqueValue:
@@ -55,3 +114 @@ def opaque_decoder_value(value: Any) -> R5OpaqueValue:
@@ -59 +116,2 @@ def opaque_decoder_value(value: Any) -> R5OpaqueValue:
@@ -67 +125 @@ def normalize_decoder_physical_value(value: Any) -> Any:
```

### 5.1 New `_canonical_naive_date_time`, lines 39–96 — ACCEPT

Actual reviewed behavior:

- `isinstance(value, datetime)` branch:
  - accesses `tzinfo` inside `try`; any access failure becomes `R5CodecError("date-like subclass … cannot expose tzinfo safely")`;
  - any non-`None` `tzinfo` becomes `R5CodecError("timezone-aware datetime requires a separate explicit decoder carrier authority")`;
  - reads `nanosecond`; a nonzero non-bool integer becomes `R5CodecError("date/time subclass with sub-microsecond precision cannot be preserved by the versioned opaque carrier")`;
  - rebuilds exact built-in `datetime(year, month, day, hour, minute, second, microsecond, fold=fold)` inside `try`; field/constructor exceptions become typed `R5CodecError`;
  - `R5CodecError` is re-raised unchanged.
- `isinstance(value, date)` branch rebuilds exact built-in `date(year, month, day)`; exceptions become typed refusal.
- `isinstance(value, time)` branch checks `tzinfo`, refuses aware time with the explicit authority error, then rebuilds exact built-in `time(hour, minute, second, microsecond, fold=fold)`; exceptions become typed refusal.
- Unsupported types raise the existing `unsupported opaque decoder value type …` refusal.

No new type id, payload layout, timezone representation, or semantic interpretation is introduced.

### 5.2 `opaque_decoder_value`, lines 99–120 — ACCEPT

- Calls the canonicalizer first.
- Packs the existing exact formats:
  - `python.datetime.datetime@1` `>HBBBBBIB`;
  - `python.datetime.date@1` `>HBB`;
  - `python.datetime.time@1` `>BBBIB`.
- The type test is on the exact canonical built-in type, so the canonicalizer cannot smuggle a subclass into the packer.
- Existing `R5OpaqueValue` validation is unchanged.

Verified payloads:

- naive subclass / pandas `Timestamp` with `microsecond=901234, fold=1` → `07d80405060708000dc07201` (civil tuple `(2008, 4, 5, 6, 7, 8, 901234, 1)`).
- date subclass `2008-04-05` → `07d80405`.
- time subclass `06:07:08.901234, fold=1` → `060708000dc07201`.

### 5.3 `normalize_decoder_physical_value`, lines 123–135 — ACCEPT

- Gate changed from exact types to `isinstance(value, (datetime, date, time))`.
- Tuple/list/mapping recursion is unchanged.
- A nested aware value inside a normalizer container reaches `opaque_decoder_value` and refuses.
- An arbitrary custom object with `.item()` inside a normalizer container is left unchanged by the normalizer; that is the pre-existing E1 non-carrier behavior, not a new carrier route. Direct `_physical_value` on a nested wrapper is the separate bounded residual discussed above.

### 5.4 `R5TypedValueCodec.encode` direct date/time branch — UNCHANGED

The direct codec still refuses date/time objects (including subclasses) with:

```
date/time meaning may not be invented by the R5 codec; use an explicit opaque decoder value
```

This preserves the E1 separation between decoder carriage and codec invention. The E4F change is decoder-side canonicalization, not codec-side date interpretation.

## 6. D01 / PR526 / float-bit non-changes

Independently extracted source-block sha256 comparisons, E1 versus E4F:

| Source block | sha256 at E1 and E4F | Equal |
|---|---|---|
| `DECLARED_ENCODING_ALLOWLIST` | `051ea39a048d93ebef123429a47df326e4ef69044374ce4919060b41daf44eab` | yes |
| `COMPATIBILITY_ALLOWLIST` | `64131d172918dad450517a5b0c34962951aaa2450c6ff5602fd37d1d29062878` | yes |
| `_compatibility_config` | `6e6aeca563e39b9c4d57e521edb166f57c624dcfdcd5f4f3f9c73562f973bcff` | yes |
| `_SourceSnapshot` | `7a4d0ea4e7d3428a60893333f58d625a90b6b94d3400d1033544cee42bcdc5e2` | yes |
| `_acquire_source_snapshot` | `1e267242fd39ead8365f711bc67b09a9e6e841d5c84f3f6a86f6f2259c7e5511` | yes |
| `_float64_bits` | `326b8def532424b709bf7ce21fd32751d14eb03619c677ec6db0231b023f6d1c` | yes |
| `_bits_float64` | `842f27333da07b839cb9fb3eab6450e2fd5fcb52988a564b36c7302bee94c30f` | yes |

- D01 exact pairs at E4F: `ac0b8bc1…` BIG5, `5b703173…` WINDOWS-1252, `66252a92…` WINDOWS-1252. Each `_compatibility_config` returns the exact `SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY` status; declared and compatibility lanes are disjoint.
- PR526 custody source is unchanged: source fd `O_RDONLY | O_CLOEXEC`, private construction `O_RDWR | O_CREAT | O_EXCL` then `fchmod 0400`, reader `O_RDONLY | O_CLOEXEC | O_NOFOLLOW`, `/dev/fd` path, inode/identity checks, unlink, nlink zero, `O_RDONLY` fcntl check, SHA verification, idempotent close. The selected 26 custody tests pass.
- SAV finite float representation is unchanged: Python `float`, `float64_finite`, exact big-endian bit hex. Observed `1.5 -> 3ff8000000000000`, `-2.25 -> c002000000000000` in the real SAV/DTA fixtures.
- No R9 broker, G01 numeric-coercion bridge, native-source grant, aware-carrier authority, source-use grant, or public scientific meaning is added by the diff. The new code is confined to date/time physical canonicalization/refusal and typed range classification.

## 7. Test file review

`rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` is 314 lines and contains 12 collected tests (10 test functions, two of which are two-way parametrized):

1. real SAV and DTA `DATETIME` through `iter_cells` plus pinned seam (`sav`, `dta` parametrizations);
2. real `DATETIME` PR526 custody, post-acquisition tamper, pre-decode tamper;
3. naive `Timestamp`/subclass canonicalization with fold/microseconds across direct/carrier/normalizer/wrapper;
4. naive date/time subclasses and nested fold;
5. recursive item chain non-manufacture (naive two-level fallback);
6. aware plain subclass and aware `Timestamp` refusal, direct/carrier/nested-list/wrapper;
7. aware `time` subclass refusal;
8. lossy `NaT`, sub-microsecond, hostile `tzinfo`, hostile civil-field refusal;
9. opaque carrier versus range declaration typed `DecoderError`;
10. `_physical_value` not exported, public classifier retained.

The test imports only stdlib, pandas, pyreadstat, pytest, and the reviewed production modules. It uses synthetic source-free files, temporary directories, and local Git object reads for the pinned seam. It contains no raw/native survey data, no network access, no private source copy, and no unrelated production code. The two-level wrapper test intentionally asserts only the naive non-carrier fallback; it does not assert aware-depth refusal, consistent with the disclosed scope boundary.

## 8. Hunk verdict

- Decoder `_physical_value` subclass gate and one-level wrapper: ACCEPT at bounded direct/one-level scope; nested ≥2 aware stringification recorded as non-blocking residual.
- Decoder typed range comparison: ACCEPT.
- Decoder `__all__` private-helper removal: ACCEPT.
- Codec canonicalizer: ACCEPT.
- Codec opaque packer: ACCEPT; formats/type ids unchanged.
- Codec normalizer subclass gate: ACCEPT.
- Codec direct date/time refusal: UNCHANGED/ACCEPT.
- D01/PR526/float/G01/native blocks: UNCHANGED; selected suites green; G01 severance preserved.

Terminal: `E4FR_EXACT_HUNKS__TWO_PRODUCTION_FILES_PLUS_BOUNDED_TEST__D01_PR526_FLOAT_UNCHANGED__NESTED_ITEM_BOUNDARY_RECORDED`
