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
