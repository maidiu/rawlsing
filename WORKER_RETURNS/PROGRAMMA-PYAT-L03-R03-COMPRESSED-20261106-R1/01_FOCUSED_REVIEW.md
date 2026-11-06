# 01 — Focused review of bounded compressed event bodies

## Identities and isolation

- Frozen implementation/test: `02c1200b82b8397e551817e8e4cf2c6763413189`
- Evidence commit: `1f939152a3118e43e47c6f5799d7a1f7d5f356ff`
- Published head: `7ee1a21f9b2efc22146227292d8219b949f71bbe`
- Prior accepted capacity guard: `9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3`
  / review `0d3191b32df0ebed8ecdca10ee399e1b550a6997` — untouched.
- Prior P2 acceptance: `409be32f...` / `e2f6c164...`; prior phase-3 compact
  assessment `5dfef26d...` — preserved.

Production/test blobs are identical at `02c`, `1f939`, and `7ee`:

| File | Blob SHA |
|---|---|
| `rawlsing_next/_pre553_c11_execution_view.py` | `986f327aa18053edc61bd837cdded02bbf8388d9` |
| `rawlsing_next/tests/test_pre553_c11_execution_view.py` | `8e8effa58579af0c3326ecd4af7e159947abe4ec` |

`git diff --name-only 02c1200b8..1f939152a -- rawlsing_next/` is empty. The new
production/test delta is only the execution view and its test. The evidence commit
updates C4 artifacts/tools; the published head updates only `00_RETURN.md`.

Exact-head checks used isolated detached worktrees under
`.local-logs/pyat-l03-r03/` (`checkout-7ee`, and a pre-change `checkout-pre9a5` for
the N200 baseline). The review branch/history was not rewritten; no source
adoption or production edit occurred.

## Code delta reviewed

`_pre553_c11_execution_view.py`:

- Adds `_EVENT_BODY_CHUNK_EVENTS = 256`, `_EVENT_BODY_CODEC = "zstd"`.
- Adds `_CompressedBodies` with compressed chunks
  `(compressed_bytes, raw_size, start, count)`, sorted `starts`, total rows, and
  `body_bytes(row)`: `bisect_right` locates one chunk, decompresses that chunk,
  walks 4-byte length-prefixed canonical bodies to the exact row.
- `_EventLane.materialize` uses `_CompressedBodies.body_bytes` and otherwise
  retains the legacy Arrow-array path.
- `_read_bodies` still validates file type/mode, metadata key, exact binary
  schema, row count, and each raw body SHA against the selector ref before use;
  it then compresses bounded batches for the in-memory lane.
- `_BodyCacheWriter` streams raw canonical bodies into the existing Parquet/Zstd
  binary-column format, one row group per batch (≤256 rows), writes to a staged
  temp file, fsyncs, and atomically replaces; `abort()` cleans staged/temp state.
- `_compact_public_objects` builds bounded compressed chunks, optionally writes
  the same bodies through the bounded writer, and falls back to an exact
  in-memory compressed lane if the cache cannot be written.
- Selector v1 selection, `_RespondentEvents.select`, and full I02 validation are
  unchanged.

The old `_write_bodies` helper remains unused dead code; it is not on the compact
build path. This is a cleanliness observation, not a behavior defect.

## Focused tests

At exact `02c` production/test, using the author’s four-file focused set:

```
pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py
```

Result: **50 passed, 1 skipped in 13.84 s** (author claim reproduced).

Exact skip (not erased):

- `test_pre553_sr06_decoder_carrier.py::test_real_writer_dta_extended_missing_fixture_or_typed_dependency_limitation`
- Reason: installed pyreadstat writer/readback does not expose
  `missing_user_values` in metadata.

`test_pre553_carrier_execution.py`: **4 passed in 0.50 s**.

## Independent N200 full-material comparison

Fresh processes, same sealed source/projection/release, actual compact facade and
first consumer. Pre-change = `9a5` uncompressed body lane; current = `02c`/`7ee`
compressed lane. Both compare runs pass full fact/cache/source/release checks.

- 13 facts per variant; V1/V2-cold/V2-warm equal V0 in both runs.
- Pre-change vs current full material equal for V0/V1/V2-cold/V2-warm.
- Full-material SHA-256 (all variants/both runs):
  `9a2f0a1589d48174b80be59cb9d2940323699a61fdde26da41a13951ddd31d13`.
- Full material includes cells, risk/denominator refs, provenance/dependency
  refs, authority refs, fact ref, and replay ref; not checksum-only.

Whole-process Darwin `ru_maxrss` (bytes/1e6):

| Variant | Pre 9a5 | Current 02c | Delta |
|---|---:|---:|---:|
| V0 native | 63.4 MB | 64.4 MB | +1.6% |
| V1 compact | 134.0 MB | 86.4 MB | −35.5% |
| V2 cold | 140.7 MB | 132.0 MB | −6.2% |
| V2 warm | 107.0 MB | 98.0 MB | −8.4% |
| Cache bytes | 318,780 | 429,814 | +34.8% |

N200 wall was mixed/noisy (V1 8.74→7.13 s, V2-warm 6.80→6.29 s, V2-cold
8.14→8.14 s, V0 10.53→7.12 s; one fresh process per variant). The defensible N200
result is exactness plus RSS/body/cache direction, not a precise wall speedup.

Independent N200 allocation control:

- Fixed Arrow after import 60.9 MB / after runtime 110.5 MB.
- Native 151.0 MB current/peak; compact 155.6 MB current / 155.7 MB peak.
- Compact bodies 301,031 compressed vs 5,940,064 raw bytes; conversion high-water
  delta 4.2 MB; retained compact Arrow bytes 0; compact tracemalloc +1.19 MB.
- Post-snapshot lookup microbenchmark: 1.61 ms decompress + 2.23 ms materialize
  per event. A separate warm repeated-chunk microbenchmark measured 0.24 ms
  decompress + 0.60 ms materialize. Lookup cost is non-zero/bounded; selector hot
  paths do not materialize bodies.

Author N1000 evidence inspected (not independently rerun): compact current
327.9→274.5 MB, peak 335.2→294.5 MB; bodies 29,701,433→1,575,621 bytes (36
chunks); V1 21.76→19.55 s, V2-warm 21.03→19.41 s, V2-cold 21.55→21.21 s; cache
1,716,950→2,184,216 bytes; native current 233.0 MB / peak 315.3 MB; author lookup
≈0.96 ms +1.27 ms.

## Independent chunk/cache gate

Fixture N=300 (2,700 events), exact current head:

- 11 chunks: `256×10 + 140`; contiguous starts; total 2,700; last partial
  verified.
- All rows materialized in shuffled order and compared to native I02 event
  `as_dict()`; canonical body bytes matched.
- Repeated lookups returned equal independent events; selector refs stable;
  order/rank/multiplicity rows checked; out-of-range rows raise `IndexError`.
- Raw 8,896,644 bytes → compressed 458,480 bytes (19.4×).
- Injected commit failure and injected `os.replace` failure both left no
  final/staged files and preserved an exact in-memory lane.
- Old-style single-row-group raw-body Parquet rewrote/read back exactly.
- New N200 cache has 8 bounded row groups `[256×7, 8]`.

## Measurement/caveat notes

- New memory bound is **256 events per compressed chunk**, not a universal fixed
  byte cap. One chunk is decompressed per exact lookup; total retained bytes are
  the compressed chunks. A pre-existing legacy cache with a huge row group may
  transiently materialize that row group on read; new writes are bounded.
- The `02c` artifact copy of `bench_compact_current.py` still probes old
  `_write_bodies`; running compare directly at `02c` can falsely report
  `v2_cold_miss_write=false` even though the file is written. The evidence tool at
  `1f939`/`7ee` probes `_BodyCacheWriter.commit` and passes. Our candidate N200 run
  used the updated `7ee` tool. This is an evidence-tool staleness issue, not a
  production defect.
- Old-reader compatibility was checked at format/readback level; the old reader
  code itself was not executed.
- No original35, production, cross-machine, or S3/native run.

## NOT_RUN

- No independent N1000 measurement; N1000 claims are author-grade inspected.
- No whole-estate, P41, route-B, or original35 run.
- No source/test/guide/protected branch edit, merge, or default-policy change.
- No new architecture court or broad repair.
