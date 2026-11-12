# HQR-20261112-R3 / PYAT Pair 1 S1-A — Agent A reciprocal construction against B #935

**Disposition:** `IMPLEMENTED_REPAIR_CANDIDATE / SOURCEFREE S2`. Independent nonauthor receiving remains required: `ACCEPT_SCOPED / REVISE_EXACT_DEFECT / HOLD_EXTERNAL`. This is **S1-A ONLY**. No original35 right/science/actor/host grant, W03/W04 resumption, protected merge, S1-B/C/D/E implementation, or new semantic/issuer system.

## 1. Exact artifact and frozen provenance

- Controlling HQ: [HQR-20261112-R3](https://github.com/maidiu/rawlsing/issues/909#issuecomment-6817019151), first Pair 1 S1-A packet. Underlying prepared C-1 [#918](https://github.com/maidiu/rawlsing/issues/918). Oct28 source-authoritative compact regenerable-hybrid selection and rights boundaries preserved.
- Protected PRE-MAIN observed `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e` (unchanged).
- Inherited A #926 `4ec042b2139dafabe386b6cdb24a4275d5b816f5` contains deep-freeze and TOCTOU repair; B #935 frozen `f3c18b4920bebc77e803dcb67abc380c4f9fcaa5`, exact [B nine-part return](https://github.com/maidiu/rawlsing/blob/f3c18b4920bebc77e803dcb67abc380c4f9fcaa5/WORKER_RETURNS/PYAT_R3_S1A_AGENT_B_R1/00_ADVERSARIAL_CONSTRUCTION_HANDOFF.md).
- This writer's isolated successor: `repair/pyat-r3-s1a-agent-a-producer-cache-20261112-r1`; [draft PR #937](https://github.com/maidiu/rawlsing/pull/937) **stacked on B's branch**, not a second protected-pre-main patch. Tested **production+tests** HEAD `906ac2875f91664e5f3e0f7280d127b49b48ddf6`. The subsequent handoff-only commit must be obtained from the live PR before independent receiving.
- Only new functional changes against #935: `rawlsing_next/pre553_source_backed_c11_facade.py` (at tested HEAD blob `9a61ee41aec8bbc1eba751ecd83b7875fb617f63`) and `rawlsing_next/tests/test_c1_agent_b_cache_differential.py` (at tested HEAD blob `988ab3639bc27ef64860724798de018fc32ec552`). This record is the only new nonfunctional file. No second C11 engine/carrier/semantic registry/issuer, or broader R3 packet work.

## 2. Governing S1-A contract and preserved accomplishments

A current governed C11 projection's *complete semantic response, respondent ownership, routing, occurrence, coordinate, weight and authority preimage*, plus the physical transport/decoder/current-authority context, controls source-backed cache reuse. An I02-valid **same-source** logical C11 release is not necessarily a valid release for *another* projection key. A cached C11 miss must be built by the trusted source-backed facade and its one existing I02 validator, then must have exact initial/final preimage coherence before first admission. A cache hit must serve the corresponding release, never a sibling result. Actual I03 first reader must demonstrate changed respondent Y fact and unchanged eligible denominator with exact restore.

**Legitimate B victories preserved:** #922 full governed-preimage key and physical/authority contexts, one-shot authority iterable, actual I03 changed-value/row-owner test; #926 deep immutable nested semantic input snapshot and cached/uncached TOCTOU checks; #935 first-admitted **occupied-key rebind refusal** with idempotent same-result reinsertion. These were sourcefree tests, not native source or science issuance. No reason to rewrite them.

## 3. New independently established defect and RED execution

**S1-A A-R2-D01 / poisoned empty slot:** B's `SourceBackedC11SessionCache.put(key,release)` checks the release's C11 logical type/seal and `source_artifact_ref.content_hash == key.source_sha256`, and rejects an *occupied* conflicting binding. An **empty** cache has no prior binding to check, so public `put(key_for_A, release_for_B)` accepts a separately I02-validated release B with the **same source SHA** but a different row→respondent mapping, producing a distinct `release_ref` and a distinct actual R1/Y I03 distribution. The later builder reads the wrong C11 from cache before constructing A. This is a public cache API fault-injection defect, **not** proof that the existing source builder naturally collides or original35 source read is illicit.

RED test-only commit `719c99f9c568bd4297543140ef8ce4d44583654c`. [Independent GitHub Actions #43179180781](https://github.com/maidiu/rawlsing/actions/runs/43179180781) **1 FAIL / 32 PASS**; exact failure `test_c1_empty_cache_rejects_unowned_valid_release_and_preserves_i03`: `Failed: DID NOT RAISE SourceBackedC11FacadeError`. Both releases passed independent validated-sourcefree C11 construction. The test's R1 predicate and query verify legitimate A has Y=`1` support 1/denominator 1 while foreign B yields Y=`0` support 1/denominator 1. It also asserts exact returned fact and restore.

## 4. Actual repair, positive and negative

The existing local `SourceBackedC11SessionCache.put` now permits **only replay/check of an already producer-established slot**. For a virgin slot it raises `SourceBackedC11FacadeError("producer-only cache admission")` *before mutation*, including when an externally supplied release is a perfectly valid and even the correct I02 release. Thus a caller may no longer claim the first governed cache binding by holding a validated release with the same source SHA.

The existing facade's `build_source_backed_c11_repository` remains the **sole trusted first-admission owner**. It invokes private `cache._admit_from_source_backed_producer(key,release)` only after its existing one I02 build/validation, compact public-view derivation and final complete governed/physical/authority identity recheck. An optional cache must be a `SourceBackedC11SessionCache` instance, not an arbitrary duck-typed object claiming `get`/`put`. No new I02 computation, data copy, semantic encoder, schema, persistence channel or authority issuer is added. The private producer method delegates to B's `put` conflicting-rebind check whenever the key already exists; B's idempotent reinsertion is unchanged and never replaces the previously stored object.

**Positive:** ordinary cache-miss builds via the existing producer and subsequent hit retains the correct exact release and I03 fact; `clear` followed by the producer rebuild restores it. **Negative:** public first-insert of same-source/different-row-owner validated release or even a legitimate but external same-key release is refused, with entry count zero. **Prior negatives preserved:** rebind against an occupied slot refuses; changed values, routing, occurrence, decoder metadata, authority set, transient mutation/restore, uncached mutation, and one-shot authority input remain in inherited green suite.

## 5. Executed proof, command, practical cost

- Final tested code+test HEAD `906ac2875f91664e5f3e0f7280d127b49b48ddf6`: [Actions #43179403447](https://github.com/maidiu/rawlsing/actions/runs/43179403447), **33 focused PASS** in 3.09s and **136 wider sourcefree preservation PASS** in 91.78s; zero failures.
- Reproduction command (the unchanged inherited Action workflow):
```bash
PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_c1_agent_b_cache_differential.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py

PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_source_equivalence.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_universal_workload_custody.py \
  rawlsing_next/tests/test_universal_source_byte_custody.py
```
- The new checks are O(1) for each cache admission, not an extra O(N) projection scan; earlier B full-preimage hashing and A freeze/postbuild checks remain. There is **no** independent 100k/all35 peak RSS, full-size cache economics or protected canonical-tree run asserted for this new code cut.

## 6. Hostile challenges adjudicated

- **Genuine B victory:** B proved and fixed conflicting *replacement* of a filled slot. Preserve it unchanged; B expressly identified but did not repair empty-slot poisoning.
- **Incomplete B victory:** before this patch a forged first admission could make the first `get` return an independently valid but wrong C11 release. The cache's I02 seal and source SHA cannot bind a release to a different full governed projection.
- **False generalization:** B did *not* claim malicious native source reads or a naturally occurring SHA collision. Neither does A. A sourcefree poisoned local cache object proves a local session API flaw, not a new external current source right or violation.
- **Rejected alternatives:** (a) rerun I02 on each hit, which destroys caching and repeats expensive producer work; (b) make an independent semantic/issuer authority DB, which violates Oct28 selected architecture; (c) trust any `C11LogicalRelease` seal or source hash as a proxy for the full source→administration projection; (d) trust first claimant merely because it was the first writer; (e) expose an opaque new security token and call it an authenticated native-source certificate. None is necessary or defensible at this scope.

## 7. New or residual defects, no proof inflation

1. **Python same-process threat:** `_admit_from_source_backed_producer` and `_entries` are private **contract boundaries**, not language-enforced or cryptographic isolation. Malicious code with full Python reflection/memory/module access can bypass them. A client-provided subclass could override `get` or the internal method. A genuinely hostile multi-tenant cache requires a separate isolation/permission boundary, not a fake scientific source issuer. The public `put` attack demonstrated here is genuinely closed for ordinary supported API use.
2. **Concurrency:** a contested first-writer interleaving across separate concurrent builders has not been independently falsified here; this local cache currently has no explicit lock around full admission. Authentic identical inputs should emit the same release, but a dishonest/changed stream could expose a race. Test before claiming thread safety.
3. **Release seal semantics:** a code actor that can forge or mutate sealed objects inside this process is outside this local transport contract. This repair does not revalidate every response event or authenticate an arbitrary caller-held C11, and such validation must not silently become a second full engine.
4. **External physical/source/science:** no original35 native source, original U/Epre, current external issuer, QSM authorization, original release equivalence, 100k 6-GiB proof or all35 I03 output has been established. Full currentness, source byte read and rights remain separate work owned outside S1-A.
5. **Other R3 scope:** S1-B/C/D/E are **NOT STARTED**. W03/W04 paused work and protected PRE-MAIN are unchanged. Do not treat this branch as accepted or source-native.

## 8. Exact next adversary targets and requested receiving

The next nonauthor reviewer should run the RED commit and GREEN cut, inspect the code/test blobs, attempt a different same-source I02-valid respondent/occurrence/routing sibling via public first `put`, challenge a hostile cache subclass or reflective `_entries` mutation (distinguishing that external attacker from ordinary API misuse), check concurrency/linearizability of two competing builders, and measure total large-projection cache economics separately from this O(1) admission repair. Confirm the first reader produces original R1 Y=1, foreign R1 Y=0, the fixed pipeline refuses poisoning, and clearing/restoring A returns the identical release/fact.

**Final decision belongs solely to independent nonauthor receiving:** `ACCEPT_SCOPED` / `REVISE_EXACT_DEFECT` / `HOLD_EXTERNAL`. Engineering: S2 sourcefree candidate; science: UNISSUED original35; authority: NO new source/host/actor rights; protected merge: NO.
