# PYAT C-2 — independent construction challenge R1

**Verdict: REVISE_EXACT_ABI_DEFECT / PRESERVE VERIFIED S1.** This is an isolated sourcefree counterexample and corrected implementer contract, not an accepted C11 read-store, not a native PYAT test, and not protected integration.

**Original commission:** [#919](https://github.com/maidiu/rawlsing/issues/919) under [#909](https://github.com/maidiu/rawlsing/issues/909). **Agent A artifact:** `WORKER_RETURNS/PYAT_C2_GO_FIRSTER_EXACT_I02_SAVED_READ_S05_R1/00_RETURN.md@4616a1f411550c26914faf31a21d4444382a9b99`, blob `fb7ebb65140febda2b3462cb4df4a89f06bc8787`. **Frozen source:** `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e`. The challenge branch derives from Agent A's exact immutable return, so no source/production files are changed. No local Mac/qualified Rawlsing runtime or worker lease is asserted. The C-2 original commission expressly permits read-only/sourcefree investigation and isolated artifacts **only**; it does not authorize a production-store implementation. Agent A's admission that it violated a duty to implement production code misreads #919's authority and scope.

## 1. Independently confirmed strengths

Agent A correctly locates the private `C11LogicalRelease` I02 seal, eager whole-relation `ParquetC11Carrier.reopen()`, three dispersed `C11Repository` type barriers, `_ReleaseIndex` respondent/event/routing/weight materialization, `_pre553_query_eval` exhaustive respondent/risk/denominator/used-ref material, `resume_joined_workloads()` stale historical `_resolver_for(item)`, and B5 external currentness limitations. Its H01–H25 tests are *proposals*, not claimed passed tests. Its insistence on external trusted roots, full exact replay, negative and I05/Batch first consumers is sound. Preserve the scientific and host holds. These facts were independently checked by reading exact source, not by assuming the predecessor was wrong.

## 2. Consequential defect: object-ref proof is not semantic-selector-range proof

Agent A's proposed `CertifiedC11ReadStore` offers `prove_member(ref)`, `prove_nonmember(ref)`, `select_events(universe, respondent, native_question, states=...)` and `full_ref_keyspace_root`; §D specifies a sorted **ref → location** index and authenticated ref-range exclusion. That contract omits an indispensable binding: the complete multimap from **semantic selector** to **all canonical event occurrence refs** must itself be authenticated against the sealed corpus, including native and independently authorized canonical question matching, component/subitem selection, typed states, respondent and universe scopes, event group and occurrence/rank. The event store can be completely intact and every individual object-ref membership proof valid while a corrupted *secondary selector index* silently omits a response. `prove_nonmember(other_ref)` says nothing about the lookup `(universe, respondent, question/component, states)`.

Direct source: [`_pre553_query_predicate.py::_select_respondent_events` lines 18–55](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/_pre553_query_predicate.py#L18-L55) matches native/canonical/component with optional states; [`_build_release_index` lines 63–123](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/_pre553_query_predicate.py#L63-L123) builds the per-respondent collections from the entire sealed object corpus. [`pre553_c11_ingest.py::_validate_questions_and_events` lines 623–643](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/pre553_c11_ingest.py#L623-L643) and [`pre553_c11_integrity.py::ensure_distinct_event_occurrences` lines 487–508](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/pre553_c11_integrity.py#L487-L508) are global occurrence constraints. Agent A's H02 checks a *missing page* and H03 checks duplicate occurrence; neither establishes honest completeness of each query's **derived** semantic selector range.

**Executable sourcefree counterexample:** `tests/test_semantic_range_contract.py` creates three fully content-addressed events, preserves the complete event/ref inventory and full object-ref root, but drops the second occurrence from the derived `(U1,R1,native,NQ7)` selector range. All object-ref membership checks still pass, while the query returns one answer instead of two. A separately anchored semantic-selector binding root correctly refuses the modified range and restores the exact two-event selection. Other tests cover independently mapped canonical question, cross-universe namespace, uncertain routing not equal to observed zero, and local self-rehash versus externally fixed root. **Six tests run locally and pass against this independent simplified proof model.** This is *not* a test of native Rawlsing Python modules, nor proof that any unimplemented disk reader currently makes this mistake.

## 3. Necessary corrected ABI, minimal rather than another engine

Replace unqualified `prove_nonmember(ref)` as a sufficient negative-read operation with an I02-owned **verified semantic range** operation. The existing native selector, routing and evaluator remain the mathematics; neither SQL nor a second source authority may issue a fact.

```python
class VerifiedC11IndexView(Protocol):
    def iter_respondents(self, *, universe_ref, ordered=True): ...  # bounded cursor, full-root tied
    def select_event_range(self, *, universe_ref, respondent_ref, target_ref,
                           selector_kind, include_states=None): ...
    def select_routing_range(self, *, universe_ref, respondent_ref, target_ref, risk_set_ref): ...
    def select_coordinate_range(self, *, universe_ref, respondent_ref): ...
    def select_weight_range(self, *, universe_ref, respondent_ref): ...
    def assert_complete_range(self, range_receipt): ...
    def resolve_object_exact(self, ref): ...
```

The `range_receipt` must identify (1) accepted I02 semantic/replay/source root and sealed universe; (2) selector index algorithm and codec versions; (3) exact selector key, canonical-map authorization and state filter; (4) complete ordered multiset of response **occurrence identities** and their object refs (or a cryptographically equivalent authenticated range proof); (5) proof of index completeness against a **separately held root** computed from the entire certified canonical corpus, not the index's self-hash. A query may yield `EMPTY_CERTIFIED` only after authenticated full-range exclusion. Missing/corrupt page, unknown selector topology, unissued canonical mapping or incomplete routing is `UNKNOWN/REFUSE`, never `OBSERVED_ZERO`, `NOT_APPLICABLE`, `ZERO_OVERLAP` or `NO_CURRENT` by default. Exact native routing and risk qualification remain separate and necessary: an event-free range alone cannot establish eligibility.

Construction order: approved complete source projection and I02 proof → external canonical sort of the *canonical* event/ref/semantic-selector multiset (include duplicate-preserving occurrence keys) → per-family ref-keyspace and per-selector binding roots in the same accepted **I02 proof transaction** → persisted Parquet/Zstd and bounded locator/range pages → outside-the-candidate publisher anchor → requested-range/page verification with a fixed source/universe/authority current-read decision → original I03/I05/Batch evaluation and full fact/replay identity. A row locator or replay hash alone is not that binding. A `CertifiedReleaseHandle` must not be caller-instantiable as proof of this transaction.

**Secondary economy defect:** `inventory_refs() -> tuple[ExactRef, ...]` is explicitly all-at-once and therefore O(all refs) memory. Replace it with a bounded cursor plus a separately authenticated root/count projection; do not make downstream callers enumerate all refs to perform selective access. Existing `_respondent_root`, `_evaluate_index_group`, full-domain `plan.full_domain`, inline exact evidence arrays and used-ref material impose further public-ABI lower bounds; a bounded Parquet reader cannot by itself guarantee a 6 GiB native query. Agent A already flags much of this, but its suggested method signature remains contradictory to the resource contract.

## 4. Minimum nonduplicative hostile tests to add to A's H court

- **H26 — selector-poison with intact corpus:** all persisted object refs and native event bytes survive and verify. Remove exactly one secondary native-question/occurrence index binding; native I03 MUST refuse or recover the missing event and produce the original full native fact/ref/replay. Correct hash-ref lookup alone must not green.
- **H27 — canonical mapping subset:** omit one authorized canonical-question or component selector binding while all native events remain. A canonical-question I03 request MUST refuse/rebuild, never return a supported partial denominator. Rebuild from the accepted I02 origin; missing authority refuses mapping, not unrelated valid native RAW.
- **H28 — ambiguous event absence:** exact empty selector range + one `UNKNOWN` routing/applicability fact. The native first consumer must not infer `OBSERVED_ZERO`, `NOT_APPLICABLE` or support-zero; preserve its typed uncertainty.
- **H29 — wrong-release range substitution:** a valid semantic range proof from another universe/source or wrong as-of index root must fail when the selected request/root/clock differ, even if the event objects share labels and values.
- **H30 — constrained O(N) materialization:** actual native saved-reader first consumer under 6 GiB process-tree cap must prove it does not eagerly call `inventory_refs()` or sort/materialize the full corpus unless such complete vectors are unavoidable for the public exact fact; measure both cold and repeated reads.

Unlike H01–H25, these explicitly attack the *secondary semantic index* with the canonical persisted corpus unchanged. The independent six-test model establishes the logical necessity; native H26–H30 remain **NOT_RUN**.

## 5. Honest status and independent judgments

| Court | Result |
|---|---|
| Engineering, Agent A source reconnaissance | **PRESERVE S1** source-grounded legitimate gaps and scope boundaries; not an implementation acceptance |
| Engineering, Agent A proposed read-store ABI | **REVISE** missing selector-range/root binding and unbounded inventory method; cannot claim ready-for-implementation without resolving these source semantics |
| This challenge's six-test proof model | **PASS at model scope only**, not native Rawlsing S2 or 100k economics |
| Full external-memory I02 + real normal I03/I05/Batch first-consumer | **HOLD / NOT_IMPLEMENTED / NOT_RUN**, as originally admitted |
| Scientific/original35 & P05 | **HELD**, no new source/measurement/causal grant |
| Source/host/worker/protected integration | **HELD**, no local Mac lease, authorization or protected merge claim |

## 6. Refuted attacks, newly exposed risks, and Agent A's strongest counterattack

**Refuted:** "Agent A was supposed to implement production code" is contrary to #919. "The whole investigation is worthless" contradicts the precise source findings. "A new database or SQL statistics engine is the required solution" is contradicted by existing native math and chosen architecture. "A full object-ref-root alone proves exact negative query answers" is false by a working bounded model.

**New risks created by this correction:** building a semantic selector index can duplicate persisted event bytes, multiply postings for canonical/component aliases, make state-filter ranges expensive, and create an index-canonical mismatch window. The proposed proof commitment must be integrated into the original I02 completion/custody transaction and be measured for total bytes and native exact replay. Index-specific root does not grant current source rights, and a whole-table hash model is not a production Merkle/range proof. Neither standalone model passes a native S2 first reader.

**Challenge to Agent A:** implement or specify a bounded verified selector read that reproduces the real `_select_respondent_events` native/canonical/component/state behavior, including all occurrence identities, against the existing I02 replay hash without a second full object estate. Prove false-negative index poisoning RED at actual I03, I05 and Batch first readers, while source/mapping/routing negative semantics remain intact. Then demonstrate complete original I02 global proof and native fresh-process memory, first under sourcefree tests and later under independently issued source-native permission. If the proposed method can do this without an extra semantic selector commitment, exhibit the equivalent binding explicitly; do not argue from hashes by name alone.

**No production source file was edited, no native PYAT test was run, and no independent court accepted this challenge.** This is a concrete, executable, bounded sourcefree *architectural* correction inside #919's actual authority, not a fake "built the damn thing" claim.