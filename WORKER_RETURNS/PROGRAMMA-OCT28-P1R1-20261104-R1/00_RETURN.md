# OCT28-P1R1 — independent SOURCEFREE physical/cache review and P2 ABI qualification

**P1 verdict: `REVISE_EXACT_MATERIAL_DEFECTS`.**

**P2 ABI verdict: `P2_ABI_REVISE_EXACT_INTERFACE`.** Unmutated runs preserve the exercised C11/I03/I05 and joined R04→R05/P41 exact results, but a writable reference descendant in the compact selector silently changes a `SUPPORTED` fact's provenance. This is a material P1 integrity defect, not merely an annotation issue. The receiving owner must remove that alias, then freeze the selector/value-identity contract and amend the one existing Python instance-identity test assumption. This review makes no production repair, P2 implementation, protected receiving, or scientific acceptance.

## Exact custody and independence

| Item | Exact identity |
| --- | --- |
| Repository | private `maidiu/rawlsing` |
| Accepted PRE-MAIN and baseline | `f58c8400a024d108a8ab9fa814c87967d336ea47` |
| P1 implementation reviewed | `0a63e7c90cabcfd01dbb169d477f2d0ead5be22c` — direct child; exactly 11 code/test paths |
| P1 terminal packet, evidence input only | `f317741fa2b3c69f4098a0d5f00e86974b5c5dbb` |
| E3 repair / E4 independent evidence | `43d2b70ebae4d183aadbd9694624575857fd100f` / `7fb9a576fc5bf4d15e6bb91e5640ae50336ddb0c` |
| Selected October decision | `315251451a6d112fb312a6a2e80b096d345c5de6` |
| E1 fixture/harness | `cba713d229c2e8c1c3ae28f100ac8f995c6cd8c8` |
| E3 suite packet | `3de9db3f0632c23c3a5817d0526c2f42caf5ebd1` |
| P41 runtime | `f27d1101048638bba395143a48efb7ef00bfcda4` |
| Review-only branch | `review/programma-oct28-p1r1-compact-view-hostile-20261104-r1` |

PR #686 was independently fetched as OPEN/DRAFT, base `integration/pre-main-reconciliation-r1@f58c8400…`, implementation head `0a63e7…`, one commit, 11 files. PRE-MAIN remained exactly the starting pin at the execution checks. The repository's default `main@25830fe7462bb9e29bc4087e6ae14f3f84cec377` is a different branch, not a later PRE-MAIN receiving cut; an initial progress message confused those branches and was corrected. Neither main nor the author terminal return was substituted for the production comparison.

This was a single independent Codex reviewer session, with no P1 implementation authorship, no delegation, no protected CAS role, and no original35 issuance. Runtime/model effort metadata beyond the available Codex session is not independently exposed; no extra model qualification is claimed. S2 execution actually ran on **oldMac.lan**, macOS 13.7.8 x86_64, Python 3.11.3. The author used a different host, mainMac.lan. A disposable venv supplied Arrow 22.0.0, pyreadstat 1.3.2 and DuckDB 1.5.2; installed pandas is 3.0.6 and pytest 9.1.1, differing from the author's versions. Exact host, worktree, branch, input hash and command receipts accompany this return.

The review branch and return path were absent at launch. Detached baseline and candidate worktrees were created at their exact pins; all implementation/test source stayed unchanged. Only synthetic fixture owners and the pinned 12-row, 911-byte SAV were executed. SAV SHA256: `c5ec6abad7311118651e79986322d4300409f4303d92cb17ce9440d630a7d56b`. The program's original35, J52/W52, S3/native, N11/Sorok/science and protected adoption boundaries were preserved. The explicit isolated review grant covers this work and requires no new approval.

## Actual computation and custody

The candidate facade at `pre553_source_backed_c11_facade.py:657` calls the existing physical projection and full I02 validator before `_compact_public_objects`. Invalid source/projection binding was independently refused before cache access or directory creation. `execute_issued_workload` admits the current issuer before its source factory, checks the returned edition, checks currentness again, and sends both Route B and Batch through the existing facade. Both now pass current catalog authorities. The real imports are `CarrierNeutralResearchExecutor.execute_i03` → `execute_empirical_query` → `_resolve_release_indices` → `_release_index_for` → `_build_release_index`, followed by the existing predicate/evaluation/fact builders. I05 continues through the existing discovery owner; no second I03 engine appears.

`_CompactPublicObjects.exact_entries()` supplies locators to repository commit. `_build_release_index` takes respondents from the complete I02 internal identity records and groups event selectors by exact universe and respondent ref. Coordinate, routing, weight and source-relation families retain their native eager paths. Public event iteration/indexing and `resolve_object_exact` materialize native `RespondentEvent` values through the existing materializer, which checks their exact content identity. Full native capture intentionally uses that reconstruction path. The measured I03/I05 hot runs construct **zero** native event envelopes after the validated release is compacted. This does not erase the earlier eager physical projection/I02 realization.

The existing `SourceBackedC11SessionCache` remains a distinct in-process release cache. An explicit hit there skips the rebuild branch, as in the baseline. The finding “fresh I02 before Parquet effect” concerns construction/loading of this new disposable persistent accelerator; it is not a new claim that every use of an already sealed session release reruns I02.

## Material finding — writable compact reference aliases corrupt supported provenance

**[P1] `_EventRead.ref` and interned dimension refs are not deeply immutable.** At `_pre553_c11_execution_view.py:248–253`, the view retains `ExactRef` instances directly. `ExactRef` is a frozen dataclass **with a writable `__dict__`**, so freezing the enclosing slotted selector does not freeze its reference descendants. Unlike native `RespondentEvent.ref`, which constructs a detached ref on each access, a compact selector exposes its retained identity object. E3's attestation retains the same index/map identities and does not detect this nested write.

Independent deterministic SOURCEFREE reproduction obtains the selector through the proposed `_select_respondent_events` handoff, without `object.__setattr__`, ctypes, file changes, index replacement, or forged attestations:

```python
selector.ref.__dict__["content_hash"] = "f" * 64
# Re-execute through CarrierNeutralResearchExecutor.execute_i03.
```

The original fact `b83fce1581ecc4594d3cf2dcfadbb9425610b2a15de0f37ccfa50ec9d6bb48c6` became **`SUPPORTED`** fact `086b033d672287920af92b221b8e829faf97a3608f6c35cabd1c61a0301cdc04`, with the forged event hash in its provenance. Its original event ref hash was `53ed8c02e8681acb64d341a158734b5b8d9aff7ad0b613d79c51b3b118f6e7fe`. The sealed native body was unchanged. Restoring the descendant restored the original exact fact. A second probe changed `selector.native_question_ref.__dict__["object_id"]`; the existing query then changed from its original supported result to `UNRESOLVED`, and restoration again recovered the exact result. The dimension refs are interned, so a shared ref can affect multiple rows.

The native baseline control mutates a returned event-ref dictionary and confirms the native event identity and exact fact stay unchanged: the returned ref is detached. The candidate owner regression deliberately requires the same exact fact after the fault and is **RED**. Receipts: `selector-ref-alias.log`, `native-ref-control.log`, `selector-ref-regression-RED.log`; executable probes and regression accompany them. This reachable descendant fault is inside the requested selector/reference integrity court; a general disclaimer about hostile memory does not qualify it away.

**Smallest owner correction:** ensure every identity-bearing ref retained/exposed by the compact selector has truly immutable backing, or expose detached refs derived from immutable stored primitive identity material. Cover the retained event ref and shared native/canonical/component dimension refs, not only the outer `_EventRead` dataclass. Preserve `ExactRef` equality/hash/serialization and exact native resolver behavior. Do not add an evaluator or carrier. The owner chooses the local representation; this reviewer writes no fix. Require the supplied provenance regression to become PASS, normal selector/dimension mutation refusal or harmless detachment, exact restored captures/replay, and existing negative/gate checks on the corrected SHA before receiving or using P2.

## Exact P2 handoff and smallest owner correction

The comparison scope is the implementation SHA above. After correcting the material reference-alias defect, the owner must freeze the following **proposed contract v1** at the corrected SHA. This label is a review specification, not an already exported runtime API or an authority grant. P2 must not treat `_CACHE_SCHEMA` as a public computation ABI version.

```python
_select_respondent_events(
    index: _ReleaseIndex,
    respondent_key: str,       # exact RespondentIdentity.ref.key in this index
    target: ExactRef,
    *, native_only: bool = False,
    include_component: bool = False,
    states: frozenset[str] | None = None,
) -> Iterator[RespondentEvent | _EventRead]
```

The native fallback yields original native events. The compact path yields outer-frozen `_EventRead` values; its retained reference descendants have the material defect above. **`events_by_respondent` remains `Mapping[str, Sequence[RespondentEvent]]` for ordinary indexing/iteration**: `_RespondentEvents.__getitem__` really reconstructs native events, including slices. Its separate `.select()` yields selectors and is not part of `Sequence[RespondentEvent]`. Calling ordinary sequence iteration to implement grouped P2 would eagerly reconstruct the events and forfeit the claimed hot-lane benefit. The selector helper's union return is real; annotating its outputs as all-native would be wrong.

After eliminating writable retained reference aliases, the owner should freeze a read-only structural selector contract (or an explicit native/selector union alias) with only these available fields:

| Field | Contract |
| --- | --- |
| `schema_id` | constant `"RespondentEvent"` |
| `ref` | exact original event `ExactRef`; provenance uses this ref |
| `typed_state` | exact original typed response state |
| `native_question_ref` | `ExactRef` |
| `canonical_question_ref_if_authorized` | `ExactRef | None` |
| `component_or_subitem_ref` | `ExactRef | None` |
| `authority_snapshot_refs` | immutable tuple of exact `AuthorityRef` |
| `raw_response_value` | original recursively frozen canonical semantic value |
| `canonical_response_value_if_authorized` | same frozen value contract, possibly `None` |
| `multiplicity_order_rank_fields` | original frozen topology/order/rank material |
| `response_event_id_or_deterministic_index` | original frozen occurrence identity material |

Native reference-valued attributes may be frozen dictionaries; compact reference fields are normalized `ExactRef`s. Shared code must normalize through existing exact-ref helpers or a structural adapter, not compare raw representation types. `_EventRead` does not offer the full native object's `as_dict`, `semantic_projection`, `schema_version`, respondent/universe/source fields, or arbitrary native extensions. Those remain available through the sealed index/release context and native exact resolver. No `isinstance(selector, RespondentEvent)` or Python `is` identity assumption is valid for this iterator.

Selection matches exact native refs first; canonical matching is added unless `native_only`; component matching is added only when `include_component` and not `native_only`. `states=None` means no state filter and an empty frozenset yields no rows. Missing respondent keys retain `KeyError`. Both paths preserve exact-ref sort order because I02 sorts public objects, retain occurrences/multiplicity without value deduplication, and leave semantic order/rank processing to the existing evaluator. Unknown or eventless respondents remain in the complete respondent universe. Risk membership, authoritative scope, weights, zero cells, negative domains, typed failures, fact and replay construction remain existing I03 responsibilities.

**Invalidation/gates:** obtain indices only from the exact repository/release/universe resolution under the current I03 entrypoint. `_release_index_for` preserves E3's independent identity attestation and rebuilds a replaced same-release payload, missing attestation or foreign index. A direct call to `_build_release_index` is a builder, not a substitute authority gate. Sharing grouped work must be bounded to the same exact repository, sealed release object/ref, universe, query/predicate/target plan, risk/weight/design/source-scope and authority determinants; predicate or evaluated-result sharing requires those extra determinants even when topology can be reused. Current query/catalog/issuance checks still run per authorized execution. Do not reuse a cached positive as permission after authority change or revocation.

**First consumer:** implement any grouped computation behind the existing `CarrierNeutralResearchExecutor.execute_i03` / `execute_empirical_query` boundary, consuming the helper in `_pre553_query_predicate.py:16` and the existing `_target_component_value`/predicate evaluation logic. Retain I05 → Batch/R04 → R05/P41 as the terminal parity court. P2 may not depend on private Parquet files, `_EventLane.bodies`, `_CompactPublicObjects.entries`, Arrow, environmental storage paths, or unsealed identifiers.

**Demonstrated adjustment:** when all repositories in the existing I03/frontier/I05 suite are compacted, **59 tests pass and one fails** at `test_pre553_empirical_query.py:1133`, `assert resolved_event is event`. Reconstruction preserves native type, ref, exact exported body and immutability but not the Python allocation. The full original immutability test passes when that one assertion is replaced in memory by native type + exact-ref + exact-body equality; all its original descendant mutation/export/requery checks remain. Receipts: `forced-compact-semantics.log`, `qualified-identity.log`, and `check_qualified_identity.py`. No tracked test was edited.

**Owner action:** C11/I03 receiving owner first corrects the retained reference-alias defect, then adopts/version-pins the structural/union contract and value identity rule, makes that exact identity-test amendment plus compact/native selector and descendant-fault coverage part of the owner cut, and has P2 consume the selector helper behind current gates. Do not memoize native envelopes merely to make `is` pass. No additional carrier or semantic engine is required. P2 remains **REVISE**, and P1 is **not recommended for protected receiving at this SHA**.

## Independent execution, faults and exact results

| Court | Actual result |
| --- | --- |
| Pinned E3 related suite, candidate | **209 passed, 1 skipped**; skip is installed-library Stata extended missing capability |
| Focused compact/facade/Route B suite | **40 passed** |
| Independent added courts | **9 passed**; includes 13 pinned native/compact query executions and selector field/filter comparisons |
| Existing I03/frontier/I05 courts forced onto compact repositories | **59 passed, 1 nominal instance-identity failure**, preserved verbatim |
| Exact proposed value-identity amendment, in memory only | **PASS**, full original immutability test |
| Fresh-process joined R04 partial resume → actual P41 | **1 passed** |
| Cache hash-check sever/restoration | **PASS → expected RED → restored PASS**; no source file mutation |
| Retained selector ref fault | **Material RED**: different `SUPPORTED` fact with forged provenance; restoration exact; native baseline control PASS |
| Independent baseline/candidate full native capture | **byte-identical**, including fact/receipt/provenance/replay and checkpoint material |

Native capture: **53,463,055 B**, SHA256 `8048dee503f5d42079bae0b4cd43e944b4de60114b3efdd19b7929e70077254b`.

Checkpoint: **28,017 B**, SHA256 `bbc9a626f1045a22e3f4b0f95b44ef62bc434dd593c55cfd818986978d850f9c`.

Selected P41 view: `c6aaef3c9816cdd63601703f4de52adf58d86ef0382adccb7cb6764f53812cf5`.

Resource-run native parity digest: `5dd623dbfd4eb6b837644f84ccf4a2579d7403462d0c08fe26c4aff3d98e5287`.

The pinned E4 capture was executed independently on both worktrees. It changes the actual checkpoint `source_sha256` to `b…b`, recomputes internal entry/checkpoint hashes and requires `JOINED_CHECKPOINT_PIN_MISMATCH` against the original external pin. Restoring the original reaches the exact P41 view. Same-release event-index replacement and cross-source index substitution independently rebuilt the correct compact result. The pinned related suite and compact semantic courts retain authority, source, response topology, route/risk/weight, typed negative and zero-domain cases. The additional in-memory hash-check sever makes the independent same-key content-corruption court fail instead of rebuilding; restoring that comparison restores PASS. That RED is kept as negative evidence, not counted as an implementation failure.

## Cache fault model and boundaries

The new cache uses `PRE553_I02_EVENT_ACCELERATOR@1`, exact source ref/SHA, decoder metadata/transport, facade and R5 contracts, projection identity, sorted current authority refs, release ref/manifest, replay ref and ordered member-ref root. Actual file-decoder receipts include reader/version/configuration witnesses. Legacy exact streams can have a null decoder receipt, and legacy in-memory incidence without a file receipt avoids persistence. Fresh I02 members and per-body SHA256 verification remain the truth in either case. Version strings are explicit contracts, not a digest of all implementation source code; changes to serialization/decoder/projection semantics require owner version/invalidation discipline.

Independently tested: cold/warm cross-process reuse; exact regenerated member bytes; same-key altered content with preserved metadata; foreign metadata key; truncated file; deletion/rebuild; relative or public-mode root rejection; terminal directory symlink rejection; member symlink no-follow/replacement without touching its outside target; `0700` root and `0600` member; changed decoder/authority/projection keys producing misses; all **16 slots** and **80 actual distinct-key collisions** producing misses; no staging remnants after completed writes. The focused P1 tests were also independently rerun, including interrupted `os.replace`, preservation of the prior committed slot, warm no-reserialization, current revocation before cache read, exact native lookup, and in-memory compatibility. Unsupported Arrow was separately injected and the native fallback preserved results.

Only expected schema, metadata, row count and body hashes are admissible. Staged private files are flushed/fsynced before atomic replace. Failed publication is disposable and the live view remains source-derived. The tested interruption is an injected rename failure, not a power failure or a killed-process filesystem durability proof. Crash-orphaned staging files are ignored by name; a crash-orphan retention bound was not proved. Sixteen slots bound committed member count, not bytes for arbitrary event sizes.

There is no claim of security against a malicious concurrent same-UID process or hostile Python memory. Final-component root/member symlink checks were tested; ancestor-component swaps and directory replacement races were not. Normal attribute setters and frozen semantic mapping writes are rejected, and E3's specified index substitutions recover. However, retained `ExactRef.__dict__` writes are not rejected and cause the material corruption above; deep reference integrity is not established. These are private disposable-cache limits, not authority grants. No bypass of source/I02/current query checks was demonstrated.

## Resource evidence and scope

See `SERIAL_MEASUREMENTS.json` for the final six-process series without overlapping reviewer test/capture jobs; `MEASUREMENTS.json` retains the first series, which overlapped regression work and is not used to establish a speedup. Both use the identical source, pinned harness/runtime and baseline/candidate cuts. Exact counts/bytes and outputs, rather than an extrapolated performance percentage, are the supported capability result.

| Process | Joined wall | Peak RSS (B) | Hits / misses / publications |
| --- | ---: | ---: | ---: |
| base-a | 29.690 s | 250,925,056 | 0 / 0 / 0 |
| compact-cold | 32.019 s | 241,418,240 | 4 / 2 / 2 |
| compact-warm | 24.552 s | 251,150,336 | 6 / 0 / 0 |
| base-b | 25.940 s | 240,480,256 | 0 / 0 / 0 |
| compact-corrupt | 22.255 s | 254,128,128 | 4 / 2 / 2 |
| compact-deleted | 24.037 s | 254,816,256 | 4 / 2 / 2 |

Every process opened one 911-byte source snapshot and committed six repository instances. The measured release contains 92 public and 15 internal objects, with 36 compact events and 118,512 B of Arrow body material. Candidate hot runs reconstructed zero native events. Two Parquet members occupy **41,708 B**; largest staged member **20,854 B**; maximum active-plus-staged bytes across corruption recovery **41,727 B**. P41 runtime scratch remains **651,993 B**. Warm construction across six builds took **25.61 ms**, versus **92.13 ms** cold; this is a phase observation on this fixture, not an estimated production gain. Baseline wall and RSS vary materially even within this serial series. RSS does not show a stable reduction: warm is higher than both baseline readings. No reviewer jobs overlapped this second series; other host load was not controlled.

The author's ~23.8 s baseline / ~23.3 s warm and +3.61 MB cold / +8.22 MB warm RSS remain author-host observations. This review neither adopts them as its own measurements nor erases their reported RSS increase. A different host/library combination cannot establish their precise reproducibility. Whole-process memory reduction, 16-GiB operation and production-scale speedup remain unproved. The compact lane is real: native event envelopes are absent from the retained event representation, exact resolution works, and warm members avoid repeated canonical event-body serialization. Current source still opens on warm runs, cold projection and I02 remain eager, and all other record families remain eager.

## Historical succession, receiving and residual work

The adopted five-test law was read at `PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_HISTORICAL_FUNCTION_SUCCESSION_AND_WORK_SELECTION_LAW_R1.md`. Its disposition here is: (1) current selected W03/P01 and W04/P02 require compact execution/reusable physical acceleration; (2) E3 index reuse and canonical Parquet persistence alone do not provide that event hot view; (3) the actual receiver is existing I03/I05 and R04/P41; (4) reuse of the current native materializer/R5/canonical byte semantics preserves current extensions and authority boundaries; (5) adapting that machinery fills the narrow gap without porting the narrower historical R4 carrier, adding another canonical carrier, or replacing the semantic evaluator. Existing R4 tests were rerun as regression evidence, not promoted into a new owner or an extra build requirement. Disposition: `REUSE_OR_ADAPT_CANDIDATE`, material reference-integrity correction and exact ABI revision required before receiving. The existence of real compact/cache behavior does not make the unsafe reference handoff acceptable.

**Protected receiving conditions:** do not receive `0a63e7…` as accepted P1. The implementation owner returns the minimal reference-integrity correction at a new exact SHA, with the supplied RED regression passing, value-identity test/contract corrected and the same capture/gate/resource courts appropriately rechecked. The independent/receiving owner then refreshes PRE-MAIN, verifies the exact original 11-path delta plus only the required correction, and makes the separate CAS decision. An unrelated default main branch is not that cut. If the owner changes code/contracts, this report qualifies only the reviewed pin and its stated value semantics. No self-merge or original35 promotion is authorized or performed.

**Residual W03:** bounded/streaming physical projection and complete I02 validation without the current eager peak; economical working views/exact resolver qualification for other material record families; representative larger-source memory evidence. **Residual W04:** placement/grant and measured retention policy at real scale; independently accepted authenticated projection/preimage custody if a future warm path is to avoid source reopening/projection/I02. P1 does not implement that bypass. P2's grouped computation must use the qualified selector seam and existing authority/risk/weight/provenance engine. Original scientific/source owners retain U/E_pre, original35 N9/N11, FF, actor/Sorok and S3 rights.

**DONE:** isolated independent S2 review, exact captures, material RED and fault/resource receipts, and owner-usable P2 contract. **REMAINING/BLOCKER:** P1 owner must eliminate writable retained selector refs; C11/I03 owner must freeze the selector/value-identity interface and amend the exact test assumption. **LARGEST PRODUCTIVE TRANCHE:** that bounded correction and qualification, followed by separately authorized grouped I03 behind the existing entrypoint. **DELTA:** real compact/cache behavior is demonstrated, but P1 reference integrity fails; full October hybrid and broad memory benefit are unproved. Terminal stop: return this review-only branch; no production repair or P2 implementation.
