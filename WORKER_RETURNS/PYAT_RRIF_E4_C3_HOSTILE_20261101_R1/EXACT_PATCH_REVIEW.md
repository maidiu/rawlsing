# EXACT PATCH REVIEW — E1 C3 DECODER/R5 PATCH

## 1. Exact objects reviewed

| Object | Identity |
|---|---|
| Reviewer branch start/PREMAIN | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| E1 candidate head | `ffd03934d0a86c98ed095d973e45587bd5751013` |
| E1 implementation commits | `2edf5df01fd9de66abca2733c0878c4ea981707d`, `1401bc7e0f5988bdeda9250e56ffe9fe26e306b1`, `90c1c0eefc66263981ba9066faab22c35dc57f9f` |
| Original accepted C3 | `30686b185d4ceb2c94f61815ef70d8c8e76255d6` |
| Accepted D01 parent | `1f9990fec3d305ea89dfe25bdeae89a967adb21b` |
| PREMAIN decoder blob | `8732e34d0ea3f4cfffd7d33ee00f258dbc2d65dd` |
| E1 decoder blob | `d60e092f9ee0948acc79b32ebe8f2f5aa7096928` |
| PREMAIN R5 blob | `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540` |
| E1 R5 blob | `6000a1704d713f65e07610d81e9b3fd8bdd515ca` |
| C3 R5 blob | `6000a1704d713f65e07610d81e9b3fd8bdd515ca` (byte-equal) |
| E1 D01 test blob | `625f1d8b1f3fa8c24501addcaff7d70209598596` |
| E1 D02 test blob | `ac5f331322a69dab224eeeda14b05681918b432e` |
| E1 integration test blob | `bfa20f7a35ef9a399bec5380b6c3e6f9caad0115` |

Patch surface is exactly two production files (`+35/-4` decoder, `+44` R5) and three test files. No other production/test path differs from PREMAIN.

## 2. Hunk-by-hunk verdict

New-file line numbers are used for the repaired tree.

### Decoder `rawlsing_next/pre553_physical_decoder.py`

| Hunk | Lines | Verdict | Reason |
|---|---|---|---|
| D-1 | 28 | ACCEPT | Imports `normalize_decoder_physical_value` from the current R5 codec. No cycle; decoder and codec load cleanly. |
| D-2 | 32 | ACCEPT | Adds `SOURCE_DECLARED_ENCODING_ONLY = "SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY"`, identical to accepted C3. The string is a physical-decoding status, not a rights or text-semantics grant. |
| D-3 | 45-49 | ACCEPT | Three exact 64-hex SHA-256 pairs. Byte-identical to C3 and C3 parent `1f9990f` (block sha256 `b9b82cab7246699c74bb33731a272b934c83c7999b9ee4ba48313247159c2713`). Disjoint from the compatibility allowlist; no wildcard, prefix, family, or fallback matching. |
| D-4 | 172 | ACCEPT (call site) | `iter_batches` now calls `_physical_value(value)` rather than `_jsonable(value)`. The routing intent is correct; the defect is inside the callee (D-5). |
| D-5 | 428-441 | **RED** | Exact-type gate plus `_jsonable` fallback. Real current decoder `DATETIME` is pandas `Timestamp` (a `datetime` subclass); it is not in `{_dt.datetime, _dt.date, _dt.time}`, has no `.item()`, and is passed to `_jsonable`, which returns `str(value)`. An aware `Timestamp`, and an item wrapper returning an aware `Timestamp`/`AwareDT`, likewise become strings instead of raising the carrier-authority refusal. |
| D-6 | 528-539 | ACCEPT | Preserves `encoding is None`, forbids `auto`/`guess`/`fallback`, preserves the exact compatibility lane, adds only exact declared SHA+encoding, and refuses everything else. Error-message change has no code/test consumer (the old literal survives only in E1's own return documents). |
| D-7 | 839-840 | ACCEPT | Exports the two new public constants. No behavioral effect. |
| D-8 | 852 | HOLD | Exports the private `_physical_value` helper in `__all__`. The tests import it directly; star-import surface expansion is unnecessary and not part of the accepted C3 contract. Remove unless a public API is deliberately intended. |

### R5 codec `rawlsing_next/pre553_r5_codec.py`

| Hunk | Lines | Verdict | Reason |
|---|---|---|---|
| R-1 | 10 | ACCEPT | Imports `datetime` for the carrier implementation. |
| R-2 | 39-62 | ACCEPT at accepted built-in grain / HOLD for current decoder | `opaque_decoder_value` correctly packs exact built-in naive date/time with exact type ids and fold, and refuses aware exact built-ins. It rejects `pandas.Timestamp` and other `datetime` subclasses with `unsupported opaque decoder value type ...`, so it cannot by itself complete the current-decoder D02 route. |
| R-3 | 65-78 | ACCEPT at accepted built-in grain / HOLD for current decoder | Recursive normalization of tuple/list/mapping is correct for exact built-ins and preserves mapping keys/values and fold. Exact-type checks leave subclasses unchanged; if `_physical_value` were widened to pass a `Timestamp`, this function would return it unchanged and the R5 encoder would reject it. |
| R-4 | 272 | ACCEPT | Exports the two new documented helper names. |

The R5 file is byte-for-byte accepted C3 blob `6000a1704…`; its primitives are not independently wrong. The current-decoder failure arises because the decoder gate and the codec primitive both use exact built-in types, while the actual reader yields a subclass.

## 3. D01 attack matrix

All D01 attacks passed.

- Exact declared map equals:

```
ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2 -> BIG5
5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2 -> WINDOWS-1252
66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec -> WINDOWS-1252
```

- Same literals verified at C3 parent `1f9990f`, C3 accepted `30686b1`, and E1.
- Declared pairs are disjoint from the six `latin1` compatibility pairs.
- Exact declared pair returns `SOURCE_DECLARED_ENCODING_ONLY`.
- Wrong SHA with declared encoding refuses; declared SHA with wrong declared encoding refuses; declared SHA with `latin1`/`UTF-8` refuses; lowercase encoding names refuse; unknown 64-hex SHA refuses.
- `auto`, `guess`, `fallback` refuse with the guessing/fallback message.
- `encoding is None` remains unprivileged (`encoding=None`, `authority_status=None`).
- Existing compatibility pairs still return `COMPATIBILITY_ONLY`.
- Synthetic end-to-end SAV and DTA decode under both `BIG5` and `WINDOWS-1252` succeeds using a test-only in-memory SHA binding. No production pair was added; no raw source was opened.
- Authority string contains `PHYSICAL_DECODING_ONLY`; it does not grant text semantics, family/wave inheritance, source permission, rights, issuer/use, or science.

## 4. D02 attack matrix

### Passes

- Exact built-in naive carrier bytes and fold:
  - `date` -> `python.datetime.date@1`, `>HBB`.
  - `time` -> `python.datetime.time@1`, `>BBBIB`; fold bit exact.
  - `datetime` -> `python.datetime.datetime@1`, `>HBBBBBIB`; fold bit exact.
- Direct aware built-in `datetime`/`time` refuse at both `opaque_decoder_value` and decoder `_physical_value`.
- One-level item-wrapped aware built-in refuses.
- One-level item-wrapped naive built-in becomes an opaque carrier.
- Two-level item chain is not recursively chased and falls back to the prior string behavior (intended).
- Nested tuple/list/mapping normalization, including date mapping keys, works and round-trips through R5.
- Date/time strings (`"2008-04-05"`, `"06:07:08"`, `"2008-04-05T06:07:08"`, `"2008/04/05"`) remain `str`; they are not reinterpreted as dates and their binding keys differ from opaque carriers.
- Bare `R5TypedValueCodec.encode(date/time/datetime)` still refuses with `date/time meaning may not be invented`.

### Failures

Current SAV and DTA decoders return pandas `Timestamp` for `DATETIME`, while returning built-in `date` for `DATE` and built-in `time` for `TIME` in this environment. Direct pyreadstat observation:

```
SAV: dtm -> Timestamp('2008-04-05 06:07:08')
DTA: dtm -> Timestamp('2008-04-05 06:07:08')
```

Decoder cells and pinned real consumer:

```
SAV decoder: date=opaque, time=opaque, datetime=str '2008-04-05 06:07:08'
DTA decoder: date=opaque, time=opaque, datetime=str '2008-04-05 06:07:08'
Pinned seam: {'d':'opaque','t':'opaque','dtm':'str','f':'float64_finite'}  (both formats)
```

Subclass witness independent of pandas:

```
NaiveDT(dt.datetime) -> decoder._physical_value: str '2008-04-05 06:07:08'
AwareDT(dt.datetime, tzinfo=UTC) -> decoder._physical_value: str '2008-04-05 06:07:08+00:00'
ItemWrapper(AwareDT(..., tzinfo=UTC)) -> decoder._physical_value: str '2008-04-05 00:00:00+00:00'
opaque_decoder_value(AwareDT(...)) -> R5CodecError: unsupported opaque decoder value type AwareDT
```

The aware cases do not reach the explicit `separate explicit decoder carrier authority` refusal because `_physical_value` uses exact `type(...)`, skips the carrier, and calls `_jsonable`. The classifier then sees an observed string, so the timezone authority boundary is not enforced; the value leaks into the ordinary string lane.

`pyreadstat` options tested: default, `apply_value_formats=False`, `user_missing=True`, and `dates_as_pandas_datetime=False` all return `Timestamp` for datetime in this installed version. `disable_datetime_conversion=True` returns numeric offsets, not built-in datetime objects, and is not used by E1. A minimal correction must either canonicalize this subclass at the decoder/codec gate or explicitly refuse it before any string fallback; widening only `opaque_decoder_value` is insufficient while `_physical_value` still stringifies first.

### Secondary classifier boundary

`classify_physical_value` performs `lo <= value <= hi` for range declarations. With an opaque date carrier and a range declaration it raises:

```
TypeError: '<=' not supported between instances of 'int' and 'R5OpaqueValue'
```

Locations: `pre553_physical_decoder.py:173` (cell classification) and `:570` (range comparison). This was already reachable for stringified date values at PREMAIN, so it is recorded as a pre-existing `HOLD`, not the primary new blocker. Any rework that makes date/time carriers more common should address or guard it.

## 5. Custody, consumer, float, and G01 review

- PR526 custody: content-bound snapshot; hash while copying; construction fd privatized to 0400; reader fd opened `O_RDONLY|O_CLOEXEC|O_NOFOLLOW`; path unlinked; reader and construction inode/size cross-checked; `nlink == 0`; post-unlink fd hash rechecked; `reader_path == /dev/fd/<fd>`; `access_mode == O_RDONLY`; close is idempotent. Independent synthetic test confirmed all fields and post-close state.
- Tamper: changing the original path after acquisition does not alter snapshot identity or decoded cells; changing it before governed decode with the old expected SHA refuses `source sha256 mismatch before governed decode`; malformed expected SHA values refuse.
- Real consumer: exercised pinned `pre553_r5_seam.iter_source_native_rows`/`normalize_decoder_batch` from owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6` (blobs `cef326ebbc40468428378f7fdbe76e4756179f39` and `62ce608829c3d9c2fb7c999aefe40188637edf80`), not just an import. It encodes cells through `R5TypedValueCodec`; opaque date/time carriers are accepted by design, while the stringified datetime enters the `str` lane.
- `ee_p2x_darwin_stage_backend._decode` was exercised by E1's integration test (selected suite) and by the 194/1 run; source counters, READ event object id, variables, and float cells passed.
- SAV float representation: finite SAV cells remain Python `float`, encode `float64_finite`, and preserve exact bits; no int/float coercion was added. G01 int/float authority is unaffected.
- G01: E1 `2 failed, 7 passed`; PREMAIN `2 failed, 6 deselected` under the same `-k`. Exact keys are identical (`47f141e4…` vs `b9b72033…`; missing int special-state rule). Not repaired, not claimed in scope, G01 authority HELD.

## 6. API and security analysis

- No `auto`/guessing/fallback bypass was introduced.
- No cross-source, family, wave, or prefix inheritance in D01; only exact full SHA+encoding.
- The declared mapping is a normal mutable Python mapping, as was the pre-existing compatibility mapping. The in-memory monkeypatch used by tests is test-only; production code contains no runtime mutation path. No new external input is accepted into the mapping.
- `SOURCE_DECLARED_ENCODING_ONLY` explicitly says physical decoding only. It does not authorize source use, rights, text semantics, or science.
- `_physical_value` in `__all__` is unnecessary public API expansion (HOLD), not a security weakening by itself.
- The exact-type gate is the authority-relevant weakening: it fails open to a string for `datetime` subclasses, including aware ones, rather than refusing. This is a representation-authority defect, not a raw-source rights grant.
- No new dependency, network path, subprocess, native execution, or raw-source reader was introduced.

## 7. Engineering conclusion

`D01`: ACCEPT.
`PR526/custody/SAV-float/C11/EE-P2X`: ACCEPT.
`D02 exact built-in carrier`: ACCEPT at accepted C3 grain.
`D02 current-decoder datetime and aware subclass`: RED.
`Exact full sourcefree fan-in`: BLOCK pending the minimal correction, because a required decoder capability on the current reader is not delivered and a fail-closed timezone boundary is bypassed by subclasses.

The patch is exact C3 source fidelity but not exact current-decoder D02 semantics. The minimal defect and negative witness are named in `FANIN_ACCEPT_OR_BLOCK.md`.
