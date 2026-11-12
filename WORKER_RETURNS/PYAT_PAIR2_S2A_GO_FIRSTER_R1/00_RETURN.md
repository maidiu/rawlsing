# PYAT Pair 2 — Agent A S2-A adversarial first handoff

**Status:** DELIVERED_SOURCEFREE_S2A_CANDIDATE / INDEPENDENT_RECEIVING_PENDING.  
**Original commission:** #919 HQR-20261112-R3 (S2-A only), controlled by #909 comment 6817019151.  
**Source cut:** protected PRE-MAIN 6a5c12f04323d74001f9632063ec907f4fc4468e.  
**Prior challenge:** #923 fc6b75ec83795931df5d8f47d7a31553198ca05a, object-ref root not semantic-selector-range proof.  
**Exact tested source-code HEAD:** 41cc75f7c99a33879099417335ba5ea21a358fca (this report is a later doc-only commit).  
**Branch:** agent/pyat-pair2-go-firster-s2a-semantic-range-20261112-r1; draft PR #932. No protected merge.

## 1. Artifact and execution

Changed source: rawlsing_next/_pre553_verified_semantic_range.py (new); rawlsing_next/_pre553_query_predicate.py (minimal selector adapter). Added rawlsing_next/tests/test_pre553_verified_semantic_range.py and .github/workflows/pyat-pair2-s2a-semantic-range.yml.

Run sourcefree suite (Python 3.11, pytest + pyarrow):

    PYTHONPATH=. python -m pytest -q -o addopts='' -p no:cacheprovider \
      rawlsing_next/tests/test_pre553_verified_semantic_range.py \
      rawlsing_next/tests/test_pre553_empirical_query.py \
      rawlsing_next/tests/test_pre553_c11_repository_ingest.py

Exact GitHub runner: https://github.com/maidiu/rawlsing/actions/runs/43176273939 — **56 PASS** on code HEAD 41cc75f7c99a33879099417335ba5ea21a358fca. Prior bounded corrections: invalid dataclass replace on a native query object, and an I02-only multiplicity fixture without required I03 ROUTING_RISK_SET authority. Both repaired without weakening native authority checks.

## 2. Governing conservation

Complete I02 M01–M18 and replay are still owned by pre553_c11_ingest.py / pre553_c11_integrity.py. Source-equivalence P01–P20/T01–T18 remains a distinct source court. Existing native _select_respondent_events demands native, authorized canonical and optionally component matching, native_only precedence, states, occurrence multiplicity and exact ref order. Risk, denominator, weighting, math, authority and replay are unchanged in the native I03 executor. No carrier, W03/W04 paused branch or protected PRE-MAIN was edited.

The specific #923 defect is that a complete object-ref inventory proves nothing about completeness of a derived semantic selector. A self-hash of that incomplete selector is not proof.

## 3. Strongest achieved working result

I02SemanticRangeWitness.from_validated_release independently scans the actual I02-sealed sourcefree corpus and commits each scoped respondent / alias-kind / exact target range to a count and streaming occurrence/content digest. The complete semantic keyspace and release/source/replay/universe bind into the witness root. The caller holds that root outside candidate postings. The verifier checks the whole requested range before filtering states or emitting a result. Alias union uses a lazy sorted merge with duplicate suppression; per-query digest memory is bounded.

The actual I03 selector recognizes CertifiedRespondentEvents and delegates to its checked range operation. The tests install this index in the original repository cache under its existing attestation, and then invoke production execute_empirical_query. Intact root: identical full native QueryExecutionResult. Poison one native binding, canonical binding, or a same-value second occurrence while canonical I02 events remain untouched: exact range refuses. H26 native query gives INTEGRITY_FAILURE, not a smaller supported fact. Restore: original full native QueryExecutionResult compares exactly equal, including its fact and replay-relevant fields; no independent byte-serialization comparison is claimed.

- H26: real I02 multievent source, actual I03 two-occurrence output; missing second occurrence RED, restore PASS.
- H27: real I02-accepted canonical mapping authority and component alias; dropping either alias binding refuses; native_only takes precedence; unissued alias cannot be invented.
- H28: certified event EMPTY with native ROUTING_UNKNOWN remains nonpositive at actual I03, never OBSERVED_ZERO.
- H29: wrong source/release/universe/root and forged witness keyspace refuse.
- H30: small 64-respondent bounded-page + memory witness and no full-inventory API. NOT a 100k/6GiB saved-reader proof.

## 4. Hostile findings repaired

- Complete object refs do not prove complete semantic range: added separately held full-keyspace witness.
- State filtering before verification hides missing typed events: whole range checked before states.
- Native/canonical/component alias union could duplicate one physical event: lazy ref-ordered merge with dedup; native_only precedence.
- Whole-range JSON signature list and alias dictionary created O(range) query overhead: replaced with incremental length-prefixed SHA-256 and heap merge.
- Real I03 test initially used routing authority inadequate for I03: rebuilt authentic sourcefree I02 fixture with explicit ROUTING_RISK_SET and replay; no production bypass.
- Native EmpiricalQuerySpec is not a dataclass: construct exact authorized query object rather than an invalid replace.

## 5. Unresolved challenges and likely attacks

1. **Not S2-B external-memory seal.** Witness construction scans and indexes a whole already-I02-validated release in memory and rechecks complete origin at adapter setup. This is a sourcefree S2-A pilot only. It does not deliver globally sorted external-memory I02 validation or genuinely bounded release-building RSS.
2. **No saved durable root/reader.** The caller holds the witness root separate from a derived index *in memory*. No external trusted CAS publisher, cross-process sealed page/nonmembership proof, disk row-group integrity, crash recovery, fresh current issuer, or permissions decision. If the attacker can forge both root and candidate and the accepted source, this pilot alone does not defend it.
3. **Actual I03 integration is test-injected, not production-default.** Existing _build_release_index still builds current native/compact index by default. H27 proves selection against authorized I02 aliases but not end-to-end canonical-target routing on every native I03 query shape; the native routing fact remains independently qualified.
4. **Resource boundary:** per-query incremental digest and alias merge are bounded extra memory, but witness generation, source index and native fact/used-ref vectors remain O(N). No retained disk, scratch, full 100k, restart, or 6GiB native saved-query measurement was performed. S2-C/D own that separate proof.
5. **Scientific/authority boundary:** Sourcefree I02 and I03 contracts untouched. No original35 or P05 source equivalence, native survey semantics, source/host license, independent scientific issuer, causal/actor grant or protected CAS. No independent nonauthor receiving yet.
6. **Attack surface:** exact alias overlap, same-ref body tampering, mixed typed-state ranges, scope collisions across universes, currentness after authority revocation and legitimate empty populations. Test these directly against the exact source/first reader rather than accepting the success narrative.

## 6. Rejected alternatives

- Ref-only proofs: #923 demonstrates missing selector occurrence despite complete intact ref corpus.
- Self-hashed derived cache: cannot certify its own omissions; external witness is indispensable.
- New SQL/science computation: conflicts with existing native I03 scientific and replay contract.
- Full C11 writer rewrite in this task: violates S2-A authorized pilot, collides with physically distinct W03/W04 ownership and skips S2-B/Pair 1 qualified input.
- Standalone toy test: cannot establish real I03 downstream effect.

## 7. Proof courts and adversarial relay

**ENGINEERING:** S2-A sourcefree implementation candidate; 56/56 at immutable tested code head; actual native I03 changed-value/refusal/restore demonstrated; independent receiving PENDING.  
**SCIENTIFIC:** current mathematical semantics conserved; original35/source-native and causal/structural inference HELD.  
**AUTHORITY:** isolated GitHub ref and compare-and-swap writes, no paused work touched, no local source rights or protected-merge grant.

**For successor B:** reconstruct #923 from the original source, inspect this exact new reader and adapter, independently exercise positive, omission, alias, zero and wrong-root tests, then attempt a consequential falsification. No automatic S2-B–G execution or protected merge follows from this return.
