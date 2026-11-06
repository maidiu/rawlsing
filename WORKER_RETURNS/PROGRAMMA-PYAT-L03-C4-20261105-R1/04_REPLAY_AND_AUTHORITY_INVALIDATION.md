# 04 — Replay, authority, release, weight, and cache invalidation evidence

All results below are sourcefree and were produced through the actual
`CarrierNeutralResearchExecutor.execute_i03` first consumer unless explicitly
stated. Exact machine-readable results are in
`03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl` under
`entry_kind=replay_authority_invalidation` and
`entry_kind=accelerator_cache_parity`, and in
`02_EXACT_COST_AND_MEMORY_RESULTS.jsonl` under
`entry_kind=accelerator_cache_behavior` and
`entry_kind=issued_revoked_negative`.

## Positive replay identity

On the N=200 synthetic source, one operation was executed twice through the same
executor and cached release index:

- fact ref equal: **true**
- replay ref equal: **true**
- exact fact ref:
  `EmpiricalFact@1.0.0|urn:rawlsing:pre553:EmpiricalFact:sha256:0211bcf10bf2b6dec8297af83fa371c5b7c5564d9e0c718a5978f55dc7a981bb|0211bcf10bf2b6dec8297af83fa371c5b7c5564d9e0c718a5978f55dc7a981bb`
- exact replay ref:
  `PRE553_I03_QUERY_REPLAY|urn:rawlsing:pre553:i03-query-replay:sha256:e9249fd69785907696739d43ba5ffcee45bb30c1b9a3f32927b009b60262a81b|e9249fd69785907696739d43ba5ffcee45bb30c1b9a3f32927b009b60262a81b`

`replay_empirical_query` with the first fact ref succeeded and returned the same
fact ref. Supplying a different operation's fact ref raised
`EmpiricalQueryExecutionError: deterministic replay mismatch: exact fact identities differ`.
This confirms replay is exact-fact-identity based, not checksum-only or
cache-identity based.

## Cached-index fault repair

The existing E3 same-identity fault path was exercised on the N=200 source:
one respondent was removed directly from the cached index payload, then the
same `execute_i03` call was repeated.

- returned fact ref equal to the pre-fault fact: **true**
- cached index respondents restored: **true**
- final index count: **1**
- final index token proves the same release/universe entry was re-attested and
  rebuilt from the sealed release.

This is the accepted PR684 behavior; it is not a new cache default.

## Authority invalidation

A query/predicate pair was built with a nonpositive `PREDICATE_GRAMMAR`
authority (`DENY`) and executed through the actual executor over its own C11
repository.

- typed state: `UNAVAILABLE`
- P02 failure state: `MISSING_REQUIRED_AUTHORITY`
- detail: `EmpiricalQuerySpec authority closure contains nonpositive exact snapshot`

The cached index and compact view do not bypass authority. A different authority
registry over the same source can reuse the index but cannot turn a denied
operation into a supported fact.

## Release and universe separation

- A `CarrierNeutralResearchExecutor` constructed with a release ref absent from
  its repository raised
  `CarrierExecutionBindingError: bound C11 release unavailable; no fallback permitted`.
- Direct `execute_empirical_query` with the same missing release returned a typed
  `UNAVAILABLE` fact with P02 `SOURCE_SCOPE_UNAVAILABLE` and detail
  `exact C11 release unavailable; no latest/default/fuzzy/nearest fallback permitted`.
- A combined repository holding two distinct releases produced **two** distinct
  `_i03_release_indices`; the two operations produced distinct facts
  (`fact_ref_equal: false`).
- A two-universe `SOURCE_INDEXED_MULTI_UNIVERSE` query over two releases produced
  **two** cached indices and **two** exact facts, one per universe; the universe
  refs were distinct and the facts were not collapsed.
- Risk set separation on one release/universe kept **one** cached index (the
  index is source topology, not a risk-result cache), but `R` and `S` produced
  different risk-member sets (200 vs 100 respondents), different denominator
  member sets, and different fact refs (`fact_ref_equal: false`).

No cross-release, cross-universe, cross-risk-set, cross-authority, or
cross-weight result sharing is present or used.

## Weight invalidation

A governed-weighted query over a source containing one `WEIGHT_MISSING`
respondent returned:

- typed state: `UNAVAILABLE`
- P02 failure state: `MEASURE_UNAVAILABLE`
- detail: `weighted query cannot use exact weight state 'WEIGHT_MISSING'`

No silent default weight of 1 was substituted.

## Existing compact accelerator cache behaviors

Route-B fixture (existing `_fixture`, 3 respondents), with the accelerator root
under the assigned checkout and isolated from production. All material
comparisons include release ref, replay manifest, exact facts, discovery
receipts, and the Route-B replay receipt.

| behavior | wall s | cache read hits | misses | writes | exact material equal | cache bytes |
|---|---:|---:|---:|---:|---|---:|
| cold empty cache | 0.4794 | 0 | 1 | 1 | true | 17,963 |
| warm cache hit | 0.0771 | 1 | 0 | 0 | true | 17,963 |
| deleted cache, rebuild | 0.0838 | 0 | 1 | 1 | true | 17,963 |
| corrupted body, rebuild | 0.0701 | 0 | 1 | 1 | true | 17,963 |
| stale decoder key, new slot | 0.0754 | 0 | 1 | 1 | true | 35,926 (two slots) |
| original after stale | 0.0766 | 1 | 0 | 0 | true | 35,926 |

After delete and corruption, the original slot's bytes were restored exactly.
The stale key created a separate slot and did not alter the original slot. These
are the existing accelerator behaviors; no blanket cache default, retention, or
eviction change was made.

The scaled compact view at N=1,000 produced one `c11-events-*.parquet` slot of
**704,824 bytes** for 8,000 events whose full event-body JSON is **14,856,000
bytes**. Cold compact build was **4.2353 s**; the warm cross-process build was
**0.8205 s** with a cache read hit and no write. This is evidence for the
regenerable compact physical view, not for query grouping.

## Issued workload, Batch, I05, and revoked permission

The existing TEST_ONLY issued workload fixture produced three issued workloads;
all three completed through the Batch path with `COMPLETED` receipts. The first
run was a cache miss/write; the second and third were cache hits with no writes.
After replacing the first issuance's currentness with `REVOKED`:

- `execute_test_only_workload` raised
  `WorkloadAdmissionError: CURRENT_COMPETENT_SOURCE_AND_SCIENCE_DECISION_REQUIRED`;
- a patched `_read_bodies` that would fail if the warmed accelerator were opened
  was **not** called;
- re-executing the original issuance after restoration produced identical
  `output_refs` to the original run.

The existing Route-B test also exercises I05 discovery through the same compositor;
the P41 same-source test
(`test_same_source_r04_partial_resume_reaches_actual_p41`) passed independently
at 67.32 s. No native or original35 authority follows from these sourcefree
tests.

## What would falsify this baseline

- A cache hit that changes any exact fact/replay ref or any cell/denominator.
- A stale, corrupted, deleted, or revoked artifact that is used without rebuilding
  from the sealed release/authority.
- Reuse of an index across different release or universe refs, or reuse of a
  risk/weight/authority result across incompatible scopes.
- A grouped or indexed result that replaces the separate exact `EmpiricalFact`
  and replay construction rather than feeding it.

## Phase-2 grouped-scope invalidation

The Phase-2 implementation adds a finite execution-local core memo. The existing
Phase-1 replay/authority/cache evidence above is retained unchanged; the following
new focused cases were added in `rawlsing_next/tests/test_pre553_i03_grouping.py`
and passed at the candidate.

- **Poisoned core memo.** After a successful grouped operation, the cached core's
  `raw_cells` was replaced with forged counts while its stored fingerprint was left
  stale. The next operation detected the fingerprint mismatch, evicted the entry,
  fell back to the unshared path, and published the exact baseline fact
  (`fingerprint_failures >= 1`; no forged `SUPPORTED` fact).
- **Index rebuild / stale group.** A cached core was populated, then one respondent
  was removed from the repository's cached index payload. The next operation
  re-attested/rebuilt the index, saw a new index identity/key, built a new core, and
  published the exact baseline fact. The old group was not reused across the rebuild.
- **Runtime successor binding.** Under `bind_runtime(Pre553RuntimeAuthoritySet())`,
  the scope deliberately declined grouping (`core_builds == 0`, `core_hits == 0`,
  fallbacks > 0) and the existing unshared path produced the exact baseline fact.
  This is the conservative fallback for query-specific runtime risk issuance.
- **Authority DENY.** A nonpositive `PREDICATE_GRAMMAR` authority produced the same
  typed `UNAVAILABLE` / `MISSING_REQUIRED_AUTHORITY` fact with and without the
  grouped scope; grouping was not reached.
- **Weight invalidation and regime isolation.** A missing weight and a query with
  `weight_basis_id = W2` over `W` facts both matched the unshared negative exactly
  (`MEASURE_UNAVAILABLE`). RAW and governed-weighted operations may share only the
  measure-independent core; every weighted denominator/cell and `_weight_for`
  validation is recomputed per operation.
- **Release/universe/authority separation.** Two distinct releases and two distinct
  universes produced separate core keys (`core_builds == 2`, `core_hits == 0`) and
  exact per-scope facts. Two authority registries with different exact authority
  sets also produced separate keys (`core_builds == 2`, `core_hits == 0`) with unchanged
  facts.
- **Scope cleanup on error.** A scope used inside a failing `with` block cleared all
  groups and reported `closed: true`, `open_groups: 0`; no state survived the error.
- **Single-operation and incompatible work.** A single operation with an explicit
  scope built one core and published the exact baseline fact, with an honest measured
  cost of roughly +2% to +4% versus the unchanged unshared path. Seven mutually
  incompatible operations produced seven core builds, zero cross-operation hits, and
  exact baseline facts; first-pass cost was +0.8% to +3.9% at N=1,000/3,000 and
  +2.6% at N=200 in the final rerun.
- **Issued Batch/I05 integration.** A real two-query plus discovery workload through
  `execute_issued_workload` produced 2 core builds and 2 core hits in the grouped
  scope and identical output refs, receipts, facts, and discovery receipts versus a
  closed scope acting as the unshared baseline.

No blanket cache default/change was made. The existing accelerator HIT/DELETE/
CORRUPT/STALE/REVOKED evidence above remains the current physical-cache evidence.

## Phase-3 preparation: compact comparison cache status

`tools/bench_compact_current.py` is prepared but **not run for timings** here.
Its V2 variant uses an `ExactPhysicalCellStream` with a non-empty
`decoder_metadata_digest`; the coordinator requires a cold cache miss/write and a
warm cache HIT. A legacy in-memory `PhysicalSourceIncidence` whose
`physical_binding()` is `None` is explicitly not counted as a cache HIT.

The driver's cold/warm commands are in `05_OPTION_MATRIX_AND_MINIMAL_DELTA.md`.
Delete, corrupt, stale, and revoked cache behavior remain covered by existing
functional tests and are **NOT_RUN** in this preparation:

- `rawlsing_next/tests/test_pre553_c11_execution_view.py::test_cache_hit_delete_and_rehashed_same_key_poison_rebuild`
- `...::test_stale_cache_and_torn_publication_keep_previous_complete_slot`
- `...::test_revoked_workload_never_opens_warmed_accelerator`
- `rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py` carrier persist/reopen corruption and stale-root tests

No blanket cache default, retention policy, extra bitmap/index, new carrier, or
persistent truth is introduced by the driver. Cache presence still does not grant
authority; source/permission/revocation checks remain outside it.

## Phase-3 measured compact cache/grouped evidence

The prepared compact comparison ran at N=200/N=1,000. V2 used an `ExactPhysicalCellStream`
with non-empty `decoder_metadata_digest`; cold wrote one authenticated Parquet/Zstd
slot and warm read it with no write, while a legacy `PhysicalSourceIncidence` with
`physical_binding=None` was not used. V0/V1/V2-cold/V2-warm full fact/cell/ref/
provenance/replay equality passed; release/source/projection identity equality passed.

Compact cache bytes were 318,780 at N=200 and 1,716,950 at N=1,000. Warm compact
conversion fell from 1.97→0.33 s and 2.27→0.74 s versus V1, but total wall remained
dominated by validation/query/fact. Compact peak RSS remained higher than V0 at both
sizes. Delete/corrupt/stale/revoked behavior remains existing functional-test
coverage and was **NOT_RUN** in this measurement.

The same compact release was then measured with no scope versus bounded
`I03GroupedExecutionScope`: cold/warm/single/incompatible/capacity full facts matched,
independent row oracle PASS, and counters showed actual routing/predicate/target work
removal. Capacity fallback (`max_groups=1`) was exact but slower, so it is reported as
unproven, not a basis for production repair. R03's 82–92 P41 fallbacks remain a
nonblocking limit.

## Capacity-miss guard (new implementation/test)

At `9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3`, a cache MISS checks only
already-exhausted group/member capacity before invoking the core builder. HITs are
unchanged and still reuse at full capacity. The unknown prospective member size
still follows the existing post-build member fallback; no eviction/LRU/estimate or
default change exists. N=200 exact paired capacity-full result: before 0.3383 s,
after 0.2001 s, no-scope 0.1989 s; before build attempts 2 / builds 1 / early
fallbacks 0, after attempts 1 / builds 1 / early fallbacks 1. Full facts/refs/replay
matched no-scope. R03 `e2f6c164...` remains scoped to `409be...` and does not accept
this new code.

## Allocation incision (no physical code change)

Allocation incisions at N=200/N=1,000 used fresh processes, same fixture and first
consumer, with native control carrying the same Arrow import/runtime. Native and
compact first-query facts/refs/replay matched exactly. Fixed Arrow runtime current
RSS was 118.0/116.6 MB; native endstate 154.6/228.6–278.2 MB current and
154.7/258.0–305.4 MB highwater; compact 169.5/327.9–328.1 MB current and
169.5/335.2–336.4 MB highwater.

At N=1,000 compact conversion added 37.7 MB current, 13.9 MB highwater; Arrow body
array 29.7 MB, live Python `tracemalloc` +4.9 MB. Compact live Python endstate was
lower than native (82.6 vs 100.2 MB); native validation current RSS varied while
live tracemalloc was identical. The remaining resident gap is conversion
overlap/allocator retention plus required Arrow bodies, not a redundant retained
Python copy. No physical code was changed; no capacity/cache default changed.
A material reduction requires a streaming/lazy I02 candidate/replay or incremental
compact ABI, preserved selector v1/I02/refs/replay. N=3000 and delete/corrupt/stale/
revoke were NOT_RUN here.
