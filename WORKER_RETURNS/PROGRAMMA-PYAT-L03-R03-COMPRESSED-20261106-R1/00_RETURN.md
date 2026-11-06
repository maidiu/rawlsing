# PROGRAMMA PYAT L03 R03 — focused compressed-body review

**Status:** `ACCEPT_FOCUSED_COMPRESSED_BODY_DELTA` for
`02c1200b82b8397e551817e8e4cf2c6763413189`.
**Reviewer:** same independent R03 reviewer. Earlier accepted capacity guard
`9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3` / review
`0d3191b32df0ebed8ecdca10ee399e1b550a6997` remains untouched and accepted. Earlier
P2 acceptance `409be32f...` / `e2f6c164...` and phase-3 assessment `5dfef26d...`
are preserved.
**Frozen implementation/test:** `02c1200b82b8397e551817e8e4cf2c6763413189`
**Evidence commit:** `1f939152a3118e43e47c6f5799d7a1f7d5f356ff`
**Published head:** `7ee1a21f9b2efc22146227292d8219b949f71bbe`
**Exact-head checkout:** detached isolated worktree(s) under
`.local-logs/pyat-l03-r03/`; no source/protected branch edit or source adoption.

## Verdict

| Field | Verdict | Basis |
|---|---|---|
| Frozen production/test delta | **PASS** | Only `_pre553_c11_execution_view.py` and `test_pre553_c11_execution_view.py` changed; production/test blobs identical at `02c`, `1f939`, `7ee` |
| Exact reconstruction / canonical body / ref / provenance / replay | **PASS** | Independent N200 full `as_dict` equality for 13 facts across V0/V1/V2-cold/V2-warm and pre-vs-new; chunk gate reconstructed all 2,700 events exactly |
| Chunk boundary / last partial / random repeated lookup / order-rank / detached refs | **PASS** | 11 chunks for 2,700 events: 10×256 + 140; contiguous starts; shuffled/repeated exact lookups; multiplicity/order/rank rows; selector refs stable |
| Selector-v1 hot query path / no body materialization | **PASS** | `_RespondentEvents.select` unchanged; existing selector tests and the 50-test focused suite pass |
| Cache format / old-reader compatibility | **PASS_SCOPED** | Still raw canonical-body Parquet/Zstd binary column; new writer uses bounded row groups; old-style single-row-group rewrite reread exactly; old reader code itself not executed |
| Bounded row groups / atomic failure cleanup | **PASS** | New N200 cache has 8 row groups (`256×7 + 8`); injected commit failure and atomic-replace failure leave no final/staged file and no broken in-memory lane |
| Read authentication / wrong key / poison / stale / delete / revoked | **PASS** | Existing compact/cache tests in the 50-test focused suite pass; no rerun regression |
| New authority / global default | **PASS** | Diff adds only private compressed-lane code/tests; cache remains caller-configured; no authority/default change |
| Focused author suite | **PASS** | 50 passed, 1 skipped in 13.84 s; exact skip identified below |
| Independent N200 functional/economic check | **PASS_SCOPED** | Fresh pre-change (9a5) and current (02c/7ee) processes; all 13 full facts identical; compact RSS/body materially reduced |
| W03/W04 scoped economic capability | **PASS_SCOPED** | Genuine improvement relative pre-change compact baseline; native-memory negative remains visible but no requirement to beat native every metric/size |
| Whole-L03 status | **NOT_COMPLETE / OWNER QUESTION** | Author engineering coverage for authorized sourcefree S2 is complete; default persistent activation and original35/S3 remain outside this evidence |
| New code disposition | **ACCEPT** | No wrong-fact, cache-authentication, boundary, or atomic-cleanup defect found |
| Next work | **STOP / OWNER DEFAULT QUESTION** | No new architecture court, broad repair, or default policy |

## Exact delta

Between `9a5cfd2a`/`ba5783cbc` and `02c1200b`:

- `rawlsing_next/_pre553_c11_execution_view.py` (+194/−36): private
  `_CompressedBodies`, bounded 256-event Zstd chunks, on-demand exact body
  lookup; `_BodyCacheWriter` with bounded row groups and atomic staging; reader
  validates raw bodies before compressing; selector v1 and I02 validation
  unchanged.
- `rawlsing_next/tests/test_pre553_c11_execution_view.py` (+43): compressed-body
  exact/bounded/old-cache-read test.
- No other production/test files changed. Production/test blobs at `02c`,
  `1f939`, and `7ee` are identical.

## Independent N200 full-material result

Fresh processes, same sealed source/projection/release, actual compact facade and
first consumer. Pre-change = `9a5` (uncompressed body lane); current = `02c`/`7ee`
(compressed lane). The author’s compare driver at `7ee` was used (its evidence-tool
probe counts the new writer commit; the stale `02c` tool copy does not).

- All 13 full fact dictionaries are exactly equal:
  - V1/V2-cold/V2-warm equal V0 in both runs;
  - pre-change V0/V1/V2-cold/V2-warm equal current equivalents;
  - full-material SHA-256 `9a2f0a1589d48174b80be59cb9d2940323699a61fdde26da41a13951ddd31d13`.
- Facts include cells, denominators/risk refs, provenance/dependency refs,
  authority refs, fact ref, and replay ref; this is not a checksum-only oracle.
- Cache checks pass: V2 cold miss/write, warm HIT, same cache files.
- Whole-process Darwin `ru_maxrss` (bytes/1e6 MB):

| Variant | Pre 9a5 | Current 02c | Delta |
|---|---:|---:|---:|
| V0 native | 63.4 MB | 64.4 MB | +1.6% |
| V1 compact | 134.0 MB | 86.4 MB | −35.5% |
| V2 cold | 140.7 MB | 132.0 MB | −6.2% |
| V2 warm | 107.0 MB | 98.0 MB | −8.4% |
| Cache bytes | 318,780 | 429,814 | +34.8% |

N200 wall direction was mixed/noisy (V1 8.74→7.13 s, V2-warm 6.80→6.29 s,
V2-cold 8.14→8.14 s, V0 10.53→7.12 s; single fresh process per variant), so the
defensible N200 result is the full-fact equality plus RSS/body/cache direction,
not a precise wall speedup.

Independent N200 allocation control (`--mode alloc`):

- Fixed Arrow after import 60.9 MB, after runtime 110.5 MB.
- Native 151.0 MB current / 151.0 MB peak; compact 155.6 MB current / 155.7 MB
  peak in this run.
- Compact body lane 301,031 compressed bytes vs 5,940,064 raw bytes; compact
  conversion high-water delta 4.2 MB; retained Arrow body bytes 0; compact
  tracemalloc +1.19 MB.
- Our post-snapshot lookup microbenchmark: 1.61 ms decompress + 2.23 ms
  materialize per event; a separate warm repeated-chunk microbenchmark measured
  0.24 ms decompress + 0.60 ms materialize. Lookup cost is non-zero and bounded;
  selector-based query execution does not materialize bodies.

Author N1000 evidence (inspected, not independently rerun): compact current
327.9→274.5 MB, peak 335.2→294.5 MB; body 29,701,433→1,575,621 bytes (36 chunks);
V1 wall 21.76→19.55 s, V2-warm 21.03→19.41 s, V2-cold 21.55→21.21 s; cache
1,716,950→2,184,216 bytes; native current 233.0 MB / peak 315.3 MB in that run;
author lookup ≈0.96 ms decompress +1.27 ms materialize.

## Independent chunk/cache boundary gate

`reproducers/chunk_gate.py` at `7ee`, fixture N=300 (2,700 events):

- `_CompressedBodies` with 11 chunks, counts `256×10 + 140`, contiguous starts,
  sum 2,700; last partial verified.
- All 2,700 rows materialized in a deterministic shuffled order and compared to
  the native I02 event `as_dict()`; canonical body bytes matched.
- Repeated lookups returned equal independent objects; selector refs stayed
  stable; order/rank/multiplicity rows checked; out-of-range rows raise
  `IndexError`.
- Raw bodies 8,896,644 bytes → compressed 458,480 bytes (19.4×).
- Injected writer-commit failure and injected `os.replace` failure both degraded
  to no-cache with no final/staged files and an exact in-memory lane.
- Old-style single-row-group raw-body Parquet rewrote/read back exactly.

Memory bound: **at most 256 events per compressed chunk**; one chunk is
decompressed per exact lookup. Total retained bytes are the sum of compressed
chunks, not a universal fixed-byte cap. Reading a pre-existing legacy cache with
a very large row group may transiently materialize that row group; new writes are
bounded and the endstate is compressed.

## Focused tests and exact skip

Command at exact `02c` production/test:

```
pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py
```

Result: **50 passed, 1 skipped in 13.84 s**, reproducing the author’s 50/1.

Exact skip (environmental, not erased):

- `rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py::test_real_writer_dta_extended_missing_fixture_or_typed_dependency_limitation`
- Reason: installed pyreadstat writer/readback does not expose
  `missing_user_values` in metadata.

`test_pre553_carrier_execution.py`: **4 passed in 0.50 s**.

## W03/W04 completion and remaining boundary

Completion criterion applied: same facts/replay plus genuine measured economic
improvement relative the current PR686 compact / PR684 indexed pre-change compact
baseline, with full functional cases, not a single favorable operation.

- **Exactness:** PASS — independent N200 full material; author N1000 full facts;
  chunk gate all 2,700 events.
- **Economic improvement:** PASS_SCOPED — compact body/current/peak RSS materially
  lower than pre-change compact at N200 (independent) and N1000 (author evidence);
  warm cache wall improves; cache bytes rise modestly (N200 +34.8%, N1000
  +27.2%); lookup adds bounded decompression. This is a genuine improvement relative
  pre-change compact, not merely a toy operation.
- **Native-memory negative remains visible:** N1000 compact current 274.5 MB vs
  native 233.0 MB; N200 compact 155.6 vs native 151.0 MB. Peak at N1000 was
  294.5 MB compact vs 315.3 MB native in the author run, but native peak varied
  across runs. No issued requirement to beat native on every metric/size and no
  production budget is invented.
- **W04 default no-blanket-cache:** exact configured workload-owned persistent
  capability exists and is old-reader compatible; it remains env-gated and not
  default. The only remaining functional/default obligation is the competent
  owner’s decision: accept the current explicit caller-configured capability as
  the selected W04 equivalent, or require default activation. That is a policy
  question, not a missing codec/engine; this review does not grant a new default.
- **Whole L03:** author engineering coverage for the authorized sourcefree S2 scope
  is **complete for this delta**: exact function, grouped economy/capacity guard,
  compressed compact bodies, configured persistent cache, full facts/replay, and
  functional cache negatives. `WHOLE_L03_NOT_COMPLETE` remains as a formal
  whole-estate status because the owner default/acceptance question and
  original35/native/S3 authorization are outside this evidence. That absence is
  not a code defect and is not conflated with unfinished authorized S2
  implementation.
- **Remaining physical limit:** cold construction still fully materializes the
  native I02 candidate/validation before compact conversion; compressed bodies
  remove the large retained Arrow body and reduce compact current/peak, but the
  cold overlap remains. No code deficit is proven for the selected sourcefree
  compact economy; this is a visible native-memory negative and a possible future
  owner/engineering choice, not a blocker under the stated mission.

**Exact indispensable owner question:** Does W04 require default activation of
the existing authenticated persistent cache, or does the owner accept the current
explicit env-root workload-owned capability? No new default or policy grant is
made here.

## PROGRAMMA_DELTA (ordinary return)

- `ROADMAP:S03.2`, W03/P01: **exact compact function and bounded compressed-body
  reconstruction accepted; selector v1/I02 validation preserved.**
- `ROADMAP:S03.2`, W04/P02: **exact configured workload-owned persistent capability
  present and old-reader compatible; compressed body materially improves compact
  current/peak memory and wall relative pre-change compact; default activation
  remains the owner question, no blanket default.**
- `ROADMAP:S03.3`, W05/P03: **accepted grouped P2 and capacity guard remain intact;
  no change to facts/replay or authority/index behavior.**
- Completion: **scoped new code ACCEPT; sourcefree S2 author engineering coverage
  complete for this delta; whole L03 formally not complete pending owner
  default/acceptance and original35/S3 (not an engineering defect).**
- No new architecture court, broad repair, cache default, source adoption,
  protected merge, or native/original35/Sorok/human claim.

## Limits

- N=1,000 economic/memory numbers are author-grade, inspected from the retained
  `compressed_bodies_summary`; independent repetition was N=200 only, as scoped.
- The `02c` tree’s artifact copy of `bench_compact_current.py` still probes the old
  `_write_bodies`; running compare directly there can falsely report
  `v2_cold_miss_write=false` even though the cache file is written. The evidence
  tool at `1f939`/`7ee` probes `_BodyCacheWriter.commit` and passes. This is an
  evidence-tool staleness issue, not a production defect; our candidate N200 run
  used the updated `7ee` tool.
- Old-reader compatibility is format-level and new-reader old-style readback;
  old reader code was not executed.
- Pre-existing legacy cache with a huge row group may transiently materialize that
  row group; new writes are bound to 256-event row groups.
- No original35, production, cross-machine, or S3/native run is claimed.

## Artifacts

- `01_FOCUSED_REVIEW.md` — exact identities, code review, test/measurement detail.
- `02_COMMANDS_AND_NOT_RUN.jsonl` — commands and explicit NOT_RUNs.
- `03_WHOLE_L03_COMPLETION.md` — coverage, remaining physical limit, owner question.
- `evidence/independent_compressed_run.json` — independent N200 pre/current full
  material, alloc, chunk results.
- `evidence/chunk_gate.json` — independent boundary/reconstruction/atomic receipts.
- `evidence/focused_tests.json` — 50/1 result and exact skip.
- `evidence/author_compressed_claims.json` — extracted author N200/N1000 receipts.
- `reproducers/chunk_gate.py` — independent boundary gate.
