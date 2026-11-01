# EXACT PATCH AND SOURCE BLOBS — RRIF-E4F D02

## 1. Frozen basis

- STARTUP_SHA: `ffd03934d0a86c98ed095d973e45587bd5751013`
- PREMAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29`
- E4 hostile return: `5dc00a1eb0d2881a9d74661b7a94d436cc7b7c60`
- Branch: `agent/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-e4f-d02-real-datetime-fix-20261101-r1`

The two STARTUP blobs match the E4 review:

| Path | STARTUP blob | STARTUP sha256 |
|---|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `d60e092f9ee0948acc79b32ebe8f2f5aa7096928` | — |
| `rawlsing_next/pre553_r5_codec.py` | `6000a1704d713f65e07610d81e9b3fd8bdd515ca` | — |

D01 files and behavior were not edited. `DECLARED_ENCODING_ALLOWLIST`, `_compatibility_config`, the three exact SHA/encoding pairs, PR526 custody, and the E1 33-test file set are unchanged.

## 2. Corrected source identities

| Path | Corrected Git blob | Corrected sha256 | Lines |
|---|---|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `4b89c4598f324834de064c1200c63698a20e3c5c` | `f9794976aef51c418e8152850a7b0143df6790d0596549ea7f0991fc1f4501e9` | 871 |
| `rawlsing_next/pre553_r5_codec.py` | `f5f64d9b8b6c9af1d1b755f86b44fe43a8e741b7` | `fc3aaec95d1ea6b396afb7484e5b58a242a878f9a003b47a30d7f35d48eaa9ae` | 332 |
| `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` | `c07c2019455e6264b4297c1c1d782bd887b96bdd` | `1042789d92c94dd5ef983299f4cbc46b40bc55e2d556f055f6777ada11254737` | 314 |

The test file is new at this branch point.

## 3. `pre553_r5_codec.py`

### 3.1 New private canonicalizer

`_canonical_naive_date_time(value)` accepts only `isinstance(value, (datetime, date, time))` and projects the value onto an exact built-in civil object:

- `datetime`: checks `tzinfo` first; any non-`None` authority refuses with `timezone-aware datetime requires a separate explicit decoder carrier authority`. A nonzero integer Python attribute `nanosecond` (pandas sub-microsecond identity) refuses as `date/time subclass with sub-microsecond precision cannot be preserved by the versioned opaque carrier`. Civil fields are then rebuilt as `datetime(year, month, day, hour, minute, second, microsecond, fold=fold)`.
- `date`: rebuilt as `date(year, month, day)`.
- `time`: checks `tzinfo`; then rebuilds `time(hour, minute, second, microsecond, fold=fold)`.
- Unsupported types retain the existing `unsupported opaque decoder value type ...` refusal.
- Field-access, `tzinfo`-access, constructor, and out-of-range failures are converted to typed `R5CodecError`; no exception is swallowed into a string.

The returned object is then packed by `opaque_decoder_value` using the unchanged versioned type ids and struct formats:

- `python.datetime.datetime@1`: `>HBBBBBIB`
- `python.datetime.date@1`: `>HBB`
- `python.datetime.time@1`: `>BBBIB`

No new type id, no changed payload layout, and no timezone-aware representation was invented.

### 3.2 Normalizer

`normalize_decoder_physical_value` changes its gate from exact `type(value) in {...}` to `isinstance(value, (datetime, date, time))`. Recursive tuple/list/mapping normalization is otherwise unchanged. Nested naive subclasses canonicalize; nested aware subclasses refuse at the same authority gate.

### 3.3 Direct codec encode

`R5TypedValueCodec.encode` still refuses direct date/time objects (including subclasses) with `date/time meaning may not be invented by the R5 codec; use an explicit opaque decoder value`. The decoder route must canonicalize first. This preserves the E1 D02 separation between decoder carriage and codec invention.

## 4. `pre553_physical_decoder.py`

### 4.1 `_physical_value`

The exact-type gate is replaced with an `isinstance` gate:

- direct supported date/time subclasses go to `normalize_decoder_physical_value`;
- one-level `.item()` unwrapping uses the same subclass-aware gate;
- recursive item chasing is still not performed;
- non-date-like values keep the unchanged `_jsonable` fallback.

Aware direct values and aware one-level `.item()` returns therefore raise the explicit carrier-authority `R5CodecError`. Unsupported date-like subclasses (`NaT`, sub-microsecond precision, broken civil fields) raise typed `R5CodecError`. They cannot reach `_jsonable` and cannot be stringified.

### 4.2 `classify_physical_value`

Range declarations now compare inside a `try` block. A `TypeError` is converted to:

```
DecoderError("physical value cannot be compared with a declared missing range (value_type=<type>)")
```

The cause is chained. An `R5OpaqueValue` date/time carrier with a numeric range declaration therefore yields a typed decoder refusal, not an uncontrolled Python `TypeError`. Discrete and extended declarations are unchanged.

### 4.3 `__all__`

`_physical_value` is removed from `pre553_physical_decoder.__all__`. It remains a private helper. `classify_physical_value` remains public and exported.

## 5. New test file

`rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` contains 12 tests:

1. parametrized real SAV and DTA `DATETIME` fixtures through `iter_cells` and the pinned first R5 seam;
2. real `DATETIME` PR526 custody, post-acquisition tamper, and pre-decode tamper;
3. naive `Timestamp`/subclass canonicalization with fold and microseconds, direct/carrier/nested/wrapper;
4. naive date/time subclasses and nested fold;
5. recursive item chain non-manufacture;
6. parametrized aware `datetime` subclass and aware `Timestamp` refusal, direct/carrier/nested/wrapper;
7. aware `time` subclass refusal;
8. lossy `NaT`, sub-microsecond, hostile `tzinfo`, hostile civil field refusal;
9. opaque carrier vs range declaration typed refusal;
10. `__all__` export boundary.

The test loads the absent-at-STARTUP pinned seam and model sources from the local Git object database read-only, verifies Git blob identity and SHA-256, and executes them. See `REAL_SAV_DTA_AND_SUBCLASS_FAULT_TESTS.md`.

## 6. Diff scale

```
rawlsing_next/pre553_physical_decoder.py | 28 ++++++++---
rawlsing_next/pre553_r5_codec.py         | 84 +++++++++++++++++++++++++++-----
2 files changed, 93 insertions(+), 19 deletions(-)
```

Plus the new 314-line bounded D02 test. No other production or test file changed.

## 7. Non-changes explicitly verified

- `DECLARED_ENCODING_ALLOWLIST` unchanged.
- `_compatibility_config` unchanged.
- D01 exact three SHA/encoding pairs unchanged and green.
- PR526 snapshot/custody code unchanged and green.
- SAV finite-float representation unchanged and green.
- C11/projection and EE-P2X selected tests unchanged and green.
- G01 representation authority unchanged; the same two pre-existing failures remain.
