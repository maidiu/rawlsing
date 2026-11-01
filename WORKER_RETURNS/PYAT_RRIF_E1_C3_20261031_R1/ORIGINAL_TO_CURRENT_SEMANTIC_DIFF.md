# ORIGINAL TO CURRENT SEMANTIC DIFF — D01 AND D02

## Pinned identities

| Role | Commit | Blob |
|---|---|---|
| Startup/current PREMAIN decoder | `8e44ca9c751049d65e6def47600b5c073ee04b29` | `8732e34d0ea3f4cfffd7d33ee00f258dbc2d65dd` |
| Startup/current PREMAIN R5 codec | `8e44ca9c751049d65e6def47600b5c073ee04b29` | `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540` |
| Original combined C3 semantic candidate | `3cefb4ebf61ccdb6a8c5a03815438bdcda021292` | decoder `37013eb52efb8b61ef202b0d686f729f459d79c5` |
| Accepted D01 decoder integration | `1f9990fec3d305ea89dfe25bdeae89a967adb21b` | decoder `d3d828c171ea9fdd0e90563aff6ef705f5aae2cf` |
| Accepted D02 codec integration | `30686b185d4ceb2c94f61815ef70d8c8e76255d6` | codec `6000a1704d713f65e07610d81e9b3fd8bdd515ca` |
| Original D01 accepted test | `105246b33` | `8fc05965386055a208e5b3988112e67a2e6333e2` (`rawlsing_next/tests/test_closed35_d01_declared_encoding_admission.py`) |
| Original D02 accepted test | `5fbf9cc56` | `3901f10a487856f5f232ae6700fff407ac99725e` (`rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py`) |
| Repaired current decoder | `90c1c0eefc66263981ba9066faab22c35dc57f9f` | `d60e092f9ee0948acc79b32ebe8f2f5aa7096928` |
| Repaired current R5 codec | `90c1c0eefc66263981ba9066faab22c35dc57f9f` | `6000a1704d713f65e07610d81e9b3fd8bdd515ca` |

## D01 — original semantics

The original accepted D01 lane binds exactly three full source SHA-256 identities to declared decoder encodings:

```
ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2 -> BIG5
5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2 -> WINDOWS-1252
66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec -> WINDOWS-1252
```

The original `_compatibility_config` kept the compatibility-only lane independent and returned `SOURCE_DECLARED_ENCODING_ONLY` only for an exact declared SHA+encoding match. `auto`, `guess`, and `fallback` were refused; no absent or deviant declaration could inherit a neighboring source's encoding; text semantics and family/wave inheritance were not authorized.

## D01 — current loss before repair

At `8e44ca9c`, the decoder had only the six-entry `COMPATIBILITY_ALLOWLIST` (all `latin1`). `_compatibility_config` rejected every declared pair with `encoding override is not in the frozen exact SHA/config allowlist`. The three accepted declared pairs were absent.

## D01 — current repair

The current decoder now carries the exact original three-pair mapping as `DECLARED_ENCODING_ALLOWLIST` and `SOURCE_DECLARED_ENCODING_ONLY`. The compatibility lane is unchanged and remains disjoint from the declared lane. The admission order is:

1. `encoding is None` — unprivileged, no encoding override.
2. `auto` / `guess` / `fallback` — forbidden.
3. Exact compatibility SHA+encoding — `COMPATIBILITY_ONLY`.
4. Exact declared SHA+encoding — `SOURCE_DECLARED_ENCODING_ONLY`.
5. Anything else — `DecoderError`; no fallback.

The current PR526 source snapshot remains the only source reader. `_decode` still hashes the source before governed decode, uses the content-bound snapshot, and records `encoding` plus `authority_status` in `reader_configuration`.

## D02 — original semantics

The original accepted D02 codec (exact blob `6000a1704`) provides:

```
datetime.datetime -> python.datetime.datetime@1, >HBBBBBIB
datetime.date     -> python.datetime.date@1,     >HBB
datetime.time     -> python.datetime.time@1,     >BBBIB
```

The datetime/time payloads include `fold`; `datetime.date` has no time or timezone. Timezone-aware datetime/time values with `tzinfo is not None` fail closed. `normalize_decoder_physical_value` recursively handles nested tuples, lists, and mappings, preserving tuple/list container type and normalizing mapping keys and values.

The original decoder seam `_physical_value` routes exact built-in date/time values and one-level `.item()` unwrapped date/time values through the opaque carrier; everything else goes through `_jsonable`. Bare date/time objects remain rejected by `R5TypedValueCodec.encode`; only explicit `R5OpaqueValue` crosses the R5 seam.

## D02 — current loss before repair

At `8e44ca9c`, the codec had no `opaque_decoder_value` and no `normalize_decoder_physical_value`; `encode` rejected date/time objects. The decoder `iter_batches` called `_jsonable(value)` directly, which stringified `date(2020, 1, 2)` to `"2020-01-02"` and lost the typed date/time identity. This was genuine current loss, not only a missing test.

## D02 — current repair

The current R5 codec now equals accepted C3 blob `6000a1704` byte-for-byte. The current decoder `iter_batches` now calls `_physical_value(value)` instead of `_jsonable(value)`. Direct and one-level item-unwrapped naive built-ins become explicit opaque carriers; non-date scalar/container behavior is unchanged through `_jsonable`. No date/time stringification occurs in the decoder cell route.

## Exact equivalence and intentional receiver differences

| Item | Original accepted C3 | Current repair |
|---|---|---|
| D01 three pairs | exact | exact |
| D01 authority status | `SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY` | exact |
| D01 compatibility lane | independent, exact SHA+encoding | conserved unchanged |
| D02 codec | blob `6000a1704` | blob `6000a1704` byte-for-byte |
| D02 type ids and payloads | exact and fold-preserving | exact and fold-preserving |
| D02 nested normalization | tuple/list/mapping | exact |
| D02 aware values | fail closed | fail closed |
| Bare R5 date/time | rejected | rejected |
| Source custody | pre-PR526 source path | current PR526 snapshot, `O_RDONLY`, `/dev/fd`; not reverted |
| Decoder identity | `d3d828c1` older receiver | current `8732e34d` receiver plus minimal D01/D02 seam; not a historical transplant |

The current decoder is intentionally not the historical decoder. The only historical production code imported is the exact D01 lane and the D02 seam; PR526 custody, `expected_source_sha256`, lazy chunk reading, source snapshot stability, and the current public contract remain in force.

## G01 boundary

G01 is not changed. The current G01 hostile tests have two pre-existing failures at startup and at the repaired tree:

- projection float key `47f141e43fb2a330ebd2286a0bb658eaa6320768d1bb75a0b969761731ace7bd` versus int key `b9b720335f373dc4f7874f32acd003732ba7947b22b9d3dbb6bc77cc283bf6e8`;
- no matching int-based special-state rule.

These are the documented G01 native-int/float representation conflict, not D01/D02 regressions. G01 authority remains HELD and numeric coercion was not broadened. The exact baseline reproduction is recorded in `POSITIVE_AND_NEGATIVE_TESTS.md`.
