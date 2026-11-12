# PROGRAMMA PYAT R3 · S1-A only · Agent B adversarial construction handoff

**Disposition:** `IMPLEMENTED_REPAIR_CANDIDATE / SOURCEFREE S2`, **not** `ACCEPT_SCOPED`. One genuinely independent nonauthor receiving is pending. No S1-B/C/D/E, protected merge, original35, source/science/current-issuer/host grant or W03/W04 pause override.

## 1. Exact artifact and provenance
- Governing R3 S1-A complete G1–G5 contract: [issue #918](https://github.com/maidiu/rawlsing/issues/918), R3 latest issue body; selected Oct28 physical route remains unchanged.
- Original B predecessor: draft [#922](https://github.com/maidiu/rawlsing/pull/922) @ `b0ebb531bc61d7ce0435eb6e0a2d85d66f5c3819`.
- A's independently corrected successor: draft [#926](https://github.com/maidiu/rawlsing/pull/926) exact report HEAD `4ec042b2139dafabe386b6cdb24a4275d5b816f5`; tested code HEAD `4edc8eb1b5a4d6d490604350424f5cc914630f74`.
- This B return: [draft PR #935](https://github.com/maidiu/rawlsing/pull/935) on exclusive isolated branch `review/pyat-r3-s1a-agent-b-cache-conflict-20261112-r1`, directly descendant from A's report commit. RED test-only `5c0da6d028af719c212d7dd3b5f5feb1079adfce`; GREEN tested code+test `a88c0fd87268b04c1f2213eb0c8c1f1b96196843`. This documentation commit alone follows green code. Check live PR HEAD before any receiving.
- Protected read baseline: `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e`. Not modified. A's branch #926, B's old branch #922 and paused W03/W04 were not modified.
- Actual changed functional files: `rawlsing_next/pre553_source_backed_c11_facade.py` (+16 lines) and `rawlsing_next/tests/test_c1_agent_b_cache_differential.py` (+36 lines), nothing else before this report.

## 2. Independently established inherited strengths
B's complete semantic projection preimage / row-respondent ownership / physical decoder and authority-context cache partition survived source inspection, and A's nested-detachment freeze and mandatory cache/no-cache postbuild checks were preserved exactly. Neither A nor B needed a replaced C11 builder, semantic registry or query engine. The inherited real `execute_empirical_query` changed-value and exact restoration test remains in the focused suite; it verifies a different R1 Y-cell with correct denominator 1, not only distinct key strings. A's 31 focused tests and 136 wider preservation tests were retained.

## 3. New established defect — conflicting valid-release cache rebind
Current `SourceBackedC11SessionCache.put` admitted any `C11LogicalRelease` whose `source_artifact_ref.content_hash` matched `key.source_sha256`. Two **independently I02-validated** releases from the same source but different respondent row ownership therefore passed that check even when they had different exact `release_ref` values. Calling public `cache.put(key_for_A, release_for_B)` overwrote the existing A entry; a later cache.get(key_for_A) could serve B under A's full governed key. This is a *cache mutation/fault-injection* defect, not evidence the ordinary builder spontaneously computes wrong keys.

**RED evidence:** test-only SHA `5c0da6d028af719c212d7dd3b5f5feb1079adfce`, [Actions #43177931836](https://github.com/maidiu/rawlsing/actions/runs/43177931836): **1 failed, 31 passed**. The sole failure was `test_c1_session_cache_rejects_conflicting_valid_release_rebind`: `Failed: DID NOT RAISE SourceBackedC11FacadeError`. Sourcefree witness uses identical source SHA, two valid releases, different row ownership; it exercises `cache.put` after ordinary builder-admitted A.

## 4. Construction made
The same `SourceBackedC11SessionCache.put` now refuses a second insertion for an occupied key unless the existing and proposed releases have the same exact `release_ref`, `source_release_manifest_hash`, and `replay_manifest.ref`, plus the correct original stored key/source. Otherwise it raises `SourceBackedC11FacadeError("conflicting cache rebind")` **before mutation**. Idempotent identical reinsertion remains permitted. `get`, I02, C11 identity, governed projection freeze, source decoding, compact Parquet acceleration, and I03 semantics are unchanged. There is no additional persistent index, issuer, verifier, source read or stored payload.

## 5. Actual proof and conservation
**GREEN tested exact SHA `a88c0fd87268b04c1f2213eb0c8c1f1b96196843`**: [GitHub Actions #43178092614](https://github.com/maidiu/rawlsing/actions/runs/43178092614) **success**, 32/32 focused sourcefree tests in 2.48s and 136/136 preserved source-equivalence, governed workload/custody, joined-resume and source-byte-custody tests in 87.24s; 0 failures. The new test proves refusal, original entry unchanged, exactly one entry, and idempotent reinsertion. CI workflow ran against the branch's exact code+test SHA; report-only addition after it makes no code changes. The existing B/A positive, changed-value and restoration tests remain passing.

Commands as in unchanged workflow:
```bash
PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider rawlsing_next/tests/test_c1_agent_b_cache_differential.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py
PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider rawlsing_next/tests/test_pre553_source_equivalence.py rawlsing_next/tests/test_universal_workload.py rawlsing_next/tests/test_universal_workload_custody.py rawlsing_next/tests/test_universal_source_byte_custody.py
```
No new 100k RSS/latency test or original source test was run. Per conflicting put, the change adds constant-size exact ref and manifest comparisons and retains no new entry/index. That is an algorithmic observation, not a measured performance claim. Existing full projection hash remains O(projection size).

## 6. Challenges investigated but refuted/narrowed
- The A nested freeze is **not** defeated by ordinary mutation of caller-owned canonical dictionaries: it correctly detaches them at projection construction. No regression was found there in this scope.
- A's entry/exit rehash alone had a known mutate-and-restore weakness, but A did not stop there: the actual frozen rule descendants address that normal case. Do not re-open that repaired defect as though A omitted it.
- Same source SHA does **not** prove two *governed* releases equivalent; two genuinely different row bindings legitimately produce different validated releases. They must not share a cache-key slot.
- Our first RED is specifically a cache overwrite fault, **not** a demonstrated natural collision in the complete semantic-preimage hashing algorithm.

## 7. New attack surface and self-critique
The patch closes conflicting **replacement of an occupied entry**, not malicious **first insertion** of a wrong release, direct mutation of `_entries`, forged `C11LogicalRelease` fields inside hostile Python memory, or mutation of a physical source falsely claiming the same source SHA. A client with arbitrary process-memory control is outside this local cache contract. It is not enough to treat `put` acceptance as source/scientific/current-use authority; external source custody and proof of source semantics still rule. Repeated existing-key `put` now checks three identities; equivalence of refs is not a revalidation of every event byte. No falsely universal cache-poisoning closure is asserted.

## 8. Surviving disagreements and external holds
Whether a **fresh empty cache** may trust a caller-provided release at all requires an explicit trusted producer→cache admission/custody contract. That belongs to a concrete subsequent owner/ABI decision, not a pretend cryptographic self-certification by this patch. Original35 source/read rights, actual current issuer, external semantic/QSM grants, upstream physical stream authenticity and full-size economics remain separately held. The user has not authorized this agent to begin S1-B/C/D/E. Sourcefree engineering evidence is not full scientific acceptance.

## 9. Challenge back to Agent A and independent receiver
Try a valid but wrong `C11LogicalRelease` inserted **before** any legitimate owner output. Demonstrate whether the current C11 producer/consumer contract can prevent an actual I03 changed-value misserve without a fresh I02 recomputation and without inventing a second authority database. Distinguish an ordinary cache fault from a malicious same-process issuer. Also try source mismatch, wrong routing, occurrence and physical decoder contexts and demand a measured cost if recommending additional per-lookup validation. If proposing a patch, make its first-consumer negative and restoration executable. Verify this new conflicting-rebind test runs RED at `5c0da6d` and GREEN at `a88c0fd`; challenge the identical-reinsert invariant and any genuine historical operation regression. Issue **one** independent `ACCEPT_SCOPED` / `REVISE_EXACT_DEFECT` / `HOLD_EXTERNAL` at a frozen HEAD, not a review-of-review chain.

**Three-axis grade:** engineering `S2_SOURCEFREE_CANDIDATE_TESTED`, scientific `NOT_CLAIMED_ORIGINAL35`, authority `NO_NEW_SOURCE_HOST_ACTOR_ISSUER_GRANTS`. Protected integration `UNMERGED`.
