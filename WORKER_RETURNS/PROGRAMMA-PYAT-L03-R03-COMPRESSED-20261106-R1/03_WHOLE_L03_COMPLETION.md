# 03 — Whole-L03 coverage, remaining limit, and owner question

## Completion criterion applied

The actual C4/user criterion is: same facts/replay plus a genuine measured
economic improvement relative the current PR686 compact / PR684 indexed pre-change
baseline, or a valid complete equivalence, across full functional cases rather
than a single favorable operation. Native-memory parity is not required on every
metric or size, and no production budget is invented here.

On that criterion, the compressed-body delta is a **scoped PASS**:

- same full facts/replay/cells/refs/provenance in independent N200 pre-vs-current
  and author N1000 comparisons;
- genuine compact-body/RSS/wall improvement relative the pre-change compact
  baseline;
- full functional cases exercised: 16-operation grouped oracle, 50-test focused
  suite, cache HIT/DELETE/CORRUPT/STALE/REVOKED tests, selector hot path, chunk
  boundary/reconstruction gate;
- native remains an alternative with a visible memory negative, not a required
  benchmark target.

## Coverage table

| Requirement | Status | Evidence |
|---|---|---|
| Exact source-backed compact first-reader function | **PRESENT / PASS** | V0 native, V1 compact, V2 cold/warm full facts equal; selector v1/I02 validation unchanged |
| Exact canonical bodies / refs / provenance / replay | **PASS** | Independent N200 full `as_dict` equality (13 facts, all variants, pre-vs-current); all 2,700 chunk-gate events exact |
| Bounded compressed body lane, no uncompressed full-body retention | **PASS_SCOPED** | 256-event Zstd chunks; compressed chunks retained; one chunk decompressed per lookup; N200 5.94 MB raw→0.301 MB compressed; N1000 author 29.7 MB→1.58 MB |
| Chunk boundaries / last partial / random repeated / order-rank / detached refs | **PASS** | 2,700 events, chunks 256×10+140; shuffled/repeated exact lookups; order/rank rows; selector refs stable |
| Selector-v1 hot query path | **PASS** | Selection code unchanged; existing selector tests and 50-suite pass; no body materialization on selector path |
| Cache raw-body Parquet/Zstd format and old-reader compatibility | **PASS_SCOPED** | Same raw-body binary column; bounded row groups; old-style single-row-group rewrite reread exactly; old-reader code itself not executed |
| Bounded row-group write and atomic failure cleanup | **PASS** | New N200 cache row groups `256×7 + 8`; injected commit and `os.replace` failures leave no final/staged file and exact in-memory lane |
| Read authentication / wrong key / poison / stale / delete / revoked | **PASS** | Existing cache/compact tests in the 50-test suite pass; 1 environmental skip unrelated |
| Configured workload-owned persistent capability | **PRESENT / PASS** | Env-gated authenticated Parquet/Zstd cache; V2 cold miss/write and warm HIT; old-reader-compatible format |
| W04 default persistent activation | **OWNER QUESTION** | Not default; no blanket cache/default policy added or accepted |
| Grouped economy / capacity guard | **PASS (prior scope)** | `409be` P2 and `9a5` capacity guard accepted earlier and untouched |
| Whole-L03 formal status | **NOT_COMPLETE / OWNER DEFAULT + ORIGINAL35** | Author S2 engineering coverage complete for this delta; owner default question and original35/S3 authorization outside evidence |
| Original35/native/S3 | **NOT_RUN** | No S3 rights or actor/human/native claim; absence is not an engineering defect |

## Remaining physical limit (visible, not a blocker)

The new lane removes the large retained uncompressed Arrow body and materially
reduces compact current/peak memory relative pre-change compact. The cold path
still fully materializes the native I02 candidate/validation before compact
conversion, so at N=1,000 the author allocation control still shows compact
current 274.5 MB versus native 233.0 MB. N=200 independent compact/native is
155.6/151.0 MB. Native peak was 315.3 MB versus compact 294.5 MB at N=1,000 in
the author run, but native peak varied in repeats.

This is a visible native-memory negative, explicitly allowed by the mission; it
is not a wrong-fact, cache, or threshold failure. No source repair is warranted by
this evidence. A streaming/lazy I02 candidate would be a different, broad
architecture choice, not a small repair; it is not proposed or authorized here.

## W04 default/owner question

The exact current configured workload-owned persistent capability exists:
caller-set `RAWLSING_C11_ACCELERATOR_DIR`, authenticated raw-body Parquet/Zstd
cache, cold miss/write and warm HIT, old-reader-compatible format, no authority
grant. It is not on by default. The only remaining functional/default obligation
is a competent-owner decision:

**Does W04 require default activation of the existing authenticated persistent
cache, or does the owner accept the current explicit caller-configured
workload-owned capability as the selected equivalent?**

No new default, blanket cache policy, or policy grant is made by this review.

## Whole-L03 disposition

- Scoped new code `02c1200b8`: **ACCEPT**.
- Author engineering coverage for authorized sourcefree S2: **COMPLETE for this
  delta** (exact function, compressed body, configured cache, grouped/capacity
  behavior, full functional parity).
- Whole L03: **NOT_COMPLETE** as a formal whole-estate declaration because the
  owner default/acceptance question and original35/native/S3 remain outside this
  evidence. There is no remaining code deficit identified for the selected
  sourcefree compact economy.
- Original35/S3 not run is an authorization/evidence boundary, not unfinished
  authorized S2 implementation.

## Non-claims

- No full functional-equivalence declaration beyond the measured sourcefree
  N=200/1,000 fixture.
- No original35, production, native-source, cross-machine, actor/human, Sorok, or
  scientific-owner claim.
- No new architecture court, broad repair, cache default, or policy grant.
- No source/test/guide/protected branch edit or merge.
