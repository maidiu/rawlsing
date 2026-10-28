# P01-S1 — Chosen exact source-backed logical C11 execution view

**Owner:** Browser Architecture HQ (nondelegated executive decision). 
**Status:** S1 **INTERFACE-DESIGN FROZEN FOR P02/P03 INPUT**, subject to mechanical current-code/issuer compatibility and source-free positive/negative tests before Codex edits; no new semantic family, no execution grant, no new accepted I02 identity claimed.
**Predecessor:** `P01_S0_CURRENT_C11_CONSUMER_AND_IDENTITY_AUDIT_R1.md`.
**One destination:** SOURCE-AUTHORITATIVE_COMPACT_REGENERABLE_HYBRID_PRE553. No A/B/C decision tree.

## S2 authoritative engineering qualification (2026-10-28)

The selected S1 interface remains; `P01_S2_EXACT_I02_VALIDATION_JOURNAL_AND_HASH_PROOF_R1.md` gives the complete validator/journal design. Its 36-item `P01_HIGH_RESOLUTION_RETURN_LEDGER.json` binds all unresolved deep subpieces. **CRITICAL:** sourcefree negative reproduction establishes original I02 logical acceptance alone does NOT check `source_snapshot_retention_ref.content_hash == source_artifact_content_hash`; the `GovernedC11Projection` facade and physical bridge implement separate source checks. Thus the proposed C11VerifiedSourceView issuance MUST bind separately verified source admission/retention to full I02 internal validation, not a self-consistent journal/manifest hash. This is an interface prerequisite; no original source or streaming validator was executed.

## 1. Binding decision (smallest coherent seam)
**Keep existing `C11LogicalRelease` and its private validation seal unchanged as the exact public legacy materialized form. Keep `C11Repository` as the repository class. Add one PRIVATE, I02-validated `C11VerifiedSourceView` and one read-only `C11ExecutionView` interface, registered into the existing repository.** New hot-path I03/I05/recursive/workload code consumes the source-backed view and its exact-reference/columnar access. Existing materialized release/replay auditors can explicitly obtain the old `C11LogicalRelease` through a compatibility rehydration path. This is not another scientific/query engine, not a second canonical C11 publisher, and not a data model based on global dataframe uniqueness.

### Why this exact boundary
- Direct replacement of `public_objects` tuples inside `C11LogicalRelease` would break the concrete type, existing validators and equality/replay clients or silently generate millions of Python objects when iterated.
- Existing `pre553_parquet_carrier.py` persists/reloads a materialized C11 release, so simply choosing it does not remove eager creation/rebuild.
- `C11Repository` is already the accepted exact-reference namespace and I03 explicitly type-checks it; adapting internally avoids creating parallel authority and reduces the migration boundary.
- I02 must remain exclusive semantic validator/issuer. A physical cache without an I02-validated source-backed logical proof must not be registered as a valid release.
- The same logical release and replay identities must survive cache hit, deletion and full source rebuild where exact contract is unchanged.

## 2. Internal types and exact required behavior (proposed implementation names, NOT falsely claimed existing)

```python
@dataclass(frozen=True)
class C11VerifiedReleaseHeader:
    release_ref: ExactRef                 # kind C11LogicalRelease, same old semantic hash
    source_artifact_ref: ExactRef         # exact SOURCE_ARTIFACT SHA
    source_release_manifest_hash: str
    semantic_release_hash: str
    replay_manifest_ref: ExactRef         # same old replay identity
    m01_m18_coverage: Mapping[str, tuple[str, ...]]
    universe_refs: tuple[ExactRef, ...]   # exact, complete, canonical
    # private I02 validation binding to source/decoder/projection/authority/algorithm

class C11ExecutionView(Protocol):
    @property
    def header(self) -> C11VerifiedReleaseHeader: ...
    def universe_refs_exact(self) -> tuple[ExactRef, ...]: ...
    def resolve_universe_exact(self, ref: ExactRef) -> EmpiricalUniverse: ...
    def iter_respondent_identities(self, universe_ref: ExactRef) -> Iterable[RespondentIdentity]: ...
    def iter_native_events(self, universe_ref: ExactRef,
                           target_ref: ExactRef | None = None) -> Iterable[RespondentEvent]: ...
    def iter_coordinates(self, universe_ref: ExactRef) -> Iterable[EmpiricalCoordinateFact]: ...
    def iter_routing(self, universe_ref: ExactRef) -> Iterable[RoutingEligibilityFact]: ...
    def iter_weights(self, universe_ref: ExactRef) -> Iterable[WeightMeasureFact]: ...
    def iter_source_relations(self, universe_ref: ExactRef) -> Iterable[SourceUniverseRelation]: ...
    def resolve_object_exact(self, ref: ExactRef) -> CanonicalSemanticObject | C11InternalRecord: ...
    def replay_manifest_ref_exact(self) -> ExactRef: ...
    def materialize_legacy_release_exact(self, *, resource_budget) -> C11LogicalRelease: ...

class C11Repository:
    # existing resolve_release_exact() and resolve_object_exact() continue to work;
    # legacy path may rehydrate a verified lazy release, but must be explicit/
    # instrumented in production to prevent accidental full materialization.
    def resolve_execution_view_exact(self, release_ref: ExactRef) -> C11ExecutionView: ...
    def verify_release_ref_exact(self, release_ref: ExactRef) -> C11VerifiedReleaseHeader: ...
    # only I02-validated private source-view factory may commit; no public
    # register_untrusted_view(), no constructor that sets a seal from cache bytes.

# Additional private implementation-only method provided to P03, not a
# replacement for exact scientific predicate semantics:
class C11ExecutionColumns(Protocol):
    def exact_respondent_ordinals(self, universe_ref: ExactRef): ...
    def exact_event_locator_index(self, universe_ref: ExactRef): ...
    def typed_value_state_column(self, universe_ref: ExactRef, component_ref: ExactRef): ...
    def verified_source_order_and_topology(self): ...
```

These methods are semantic-agnostic evidence accessors; they do not select eligible denominators, authorize joins or compute population facts. `C11ExecutionColumns` arrays are non-authoritative physical representations; P03 authors efficient computations inside existing I03 scientific rules.

### Behavior by call type
1. **Hot I03/I05/discovery:** `repository.resolve_execution_view_exact(ref)` -> verified header/universe/indices -> shared computation. Never call `release.public_objects` to discover one universe, never enumerate every object to answer one target unless a legitimate topology requires it.
2. **Exact object resolution:** `repository.resolve_object_exact(ref)` finds a prevalidated native object or reconstructs from the source-backed, exact-internal lookup. Reconstructed object's `ref` and semantic projection must equal requested ref, otherwise fail closed. No latest/default/fuzzy fallback, no unqualified cache-only source.
3. **Legacy materialized consumers:** keep `resolve_release_exact` returning `C11LogicalRelease` including for a verified view by a *bounded, explicit, audited* compatibility materialization; use `materialize_legacy_release_exact` in source/equivalence/replay-audit tests if acceptance protocols allow. It is never the routine hot query call. Existing materialized releases continue unchanged.
4. **Batch scheduler:** `verify_release_ref_exact` checks legitimate exact released identity and current permission without inflating public object tuples. It must not equate repository presence to scientific authority.
5. **Native I03 evidence:** `replay_manifest_ref_exact` provides exact identity; a consumer requiring the full `ReplayManifest` object may request exact rehydration. P03/P04 need to preserve current `_Execution.used_objects` and native fact hash semantics, or separately escalate a versioned change. No ref-only substitution is silently assumed to preserve identity.

## 3. How the validator exclusively mints a source view
**Selected approach:** two-phase bounded, deterministic I02 streaming validation with external-sortable reference/event records, not an ad hoc cache hash or public view constructor.

A. `SOURCE_ACCEPTED`: verify original source SHA, source snapshot retention ref, decoder/config and all required governed projection/authority owners, scope. Physical cache missing/stale requires trustworthy source redecoding; cache is nonauthority.
B. `PROJECTED_STREAM`: from explicit GovernedC11Projection and physical cells emit exact native semantic sections in canonical projection format, plus compact respondent-scoped columns and exact event/occurrence locators. Preserve ALL physical slots and multi-occurrence topology; incomplete/unbound cells fail as in current `project_c11_candidate_from_physical_cells`.
C. `VALIDATION_SPOOL`: stream encoded exact canonical object refs and any determinants needed by existing I02 validators to bounded externally sorted scratch partitions. Maintain exact source/universe/respondent namespace, per-question binding, occurrence uniqueness, topology, counts, authority closure, typed absence, weights and source relations. Never validate an incomplete generator by iterating it twice; design each original validation pass explicitly.
D. `HASH_AND_REPLAY`: reproduce **byte-identical** `_candidate_projection_semantic_hash`; reproduce all closure_refs in canonical sorted ExactRef order and hash the *same* `ReplayManifest@1.0.0` canonical projection **including its full logical closure list**. No shortcut that replaces list semantics with a SHA-only Merkle root under current version. Compute same source_release_manifest hash and exact M01–M18 coverage.
E. `ATOMIC_VERIFY`: independently check deterministic projection/hash, complete closure, source/semantic authority and negative states; bind full proof into a private immutable I02 receipt. Only after all checks succeed call the I02-owned private source-view factory, which issues the verified header and view. Only the accepted I02 private commit method can register it in `C11Repository`.
F. `CACHE_PUBLISH`: after I02 validation, atomically publish regenerable columnar cache and proof manifest (separate nonauthority identity). Corrupt/missing/stale optional cache never mints I02 validation; on cold rebuild, re-derive from source and revalidate. Other derived products keep their own native release/canonical identities.

**Important technical concession:** full deterministic I02 validation and replay identity still require O(number of original occurrence/ref records) work once per changed source/projection. The improvement sought is avoiding O(number) *live Python semantic objects and repeated verbose serialized material* in ordinary stored/hot views, NOT magically obtaining accepted scientific closure without a complete proof.

## 4. ReplayManifest constraint, fully explicit
Current `ReplayManifest` is a concrete `C11InternalRecord`; `closure_refs: tuple[ExactRef,...]` is hashed as part of its semantic projection. Thus **a 'small manifest with only a closure hash' is NOT byte-equivalent** to `ReplayManifest@1.0.0`. The source-backed view persists the deterministic, ordered closure ref stream and the exact replay ref/digest as a compact **physical** representation. On legacy `ReplayManifest` resolution it reconstructs the full logical tuple and exact original object, verifies ref equality and observes resource limits.

The *streamed SHA-256 of an exact canonical serialization of that tuple* is semantically equivalent only after a source-free byte-for-byte oracle proves it, including all dictionary order, escaped strings, Unicode, stable sort and duplicate refs. Do not infer identity from matching aggregate counts or current release hash alone.

## 5. Migration map — named current code owners

| New source/adapter work | Existing file and exact change |
|---|---|
| I02 streaming projection/validation, private sealed view | `pre553_c11_ingest.py` (candidate hash, closure and all validators), `pre553_c11_integrity.py` (read-only proof helpers), `pre553_source_backed_c11_facade.py` (streaming producer); preserve old APIs/semantics. |
| Repository-view registration and exact fallback resolution | `pre553_c11_repository.py` adds _verified_views / exact view accessor and private I02 commit hook; retains old sealed `C11LogicalRelease` and materialized input compatibility. |
| I03 user of verified view | `pre553_empirical_query.py::_resolve_release_indices`; `_pre553_query_predicate.py::_build_release_index`; `_pre553_query_common.py::_ReleaseIndex` physical type; P03 owns vectorized calculation under same accepted query contract. |
| Recursive I05 reuse | `pre553_recursive_handoff.py::replay_recursive_branch_membership` uses same exact view/membership semantics, no new caller-invented branch truth. |
| Runtime scheduling | `pre553_batch_runner.py` uses `verify_release_ref_exact`; source author `campaign_src04_completion/.../full_runner.py`, `native_workload.py`, `native_streaming.py`, `authorized_execution.py` migrated by qualified source owner to view and correct op receipts. |
| Optional physical data | P02 will build Parquet/Zstd columnar/cache backing and manifest. Existing `pre553_parquet_carrier.py` is EAGER canonical relational carrier and not the new hot path. Reuse exact encoding/integrity where valid. |
| Legacy certification/audit | `pre553_source_equivalence.py`, `pre553_replay_audit.py`, `pre553_parquet_carrier.py` keep old type and optionally use verified legacy materialization, not replaced by signature-incompatible view or skipped. |
| Native evidence/replay | P04 `_pre553_query_eval.py` + native `EmpiricalFact` issuer; no output-schema change without separate authority. |

**Writer collision:** This is one architecture contract across I02, repo and I03. Codex must designate single integration owner for C11/I02; parallel P03/query editor starts after S1 API freeze and independently verifies the interface. Do not let P02 cache workers directly modify I02 private validator.

## 6. Exact acceptance / falsifiers
C11-S1-T01: accepted sourcefree fixture logical release ref EXACT equals materialized baseline, replay manifest ref and `closure_refs` equal, all family refs identical, source hash and M01–M18 identical.
T02: cache delete/rebuild and one changed compatible implementation representation yield same native refs and learned fact identifiers under same authority; different source/projection/authority results in fail-close or exact new release.
T03: duplicated physical slot, missing declared cell, invalid/held source value, duplicate respondent pair, duplicate response occurrence, wrong topology or missing authority reject pre-commit, no partial visible view.
T04: special missingness, routing unknown and multiselect/rank/repeat information preserved; no implicit one-event-per-question assumption.
T05: `resolve_object_exact` on every required source/grain exact ref matches materialized owner; nonexistent/collision refs reject; source SHA mismatch does not silently use a cached ref.
T06: full legacy `C11LogicalRelease` can be explicitly reconstructed for source-equivalence/audit and passes old exact validators; if insufficient local RAM, clean resource-bound refusal without invalid semantic state.
T07: native I03 query with **same authority/risk/missingness and verified view** yields same exact fact/replay bytes and same supported zeros/negatives; no selected-question equality claim substituted for generality.
T08: recursive handoff same-position membership/ancestry equal; I05/consumer launch without full pair-queue dependency.
T09: old accepted 7.91-GB release remains valid/readable and no new routine full pickle/JSON release required for newly qualified pipeline source.
T10: cold process, corrupt intermediate, partial cache write, source revoked/unavailable and invalid snapshot/ref all fail closed with correct distinction between unavailability and zero support.
T11: actual host wall, RAM, temp and permanent bytes per phase measured on original qualified host; no hypothetical 2-byte-per-position estimate used as output claim.
T12: no new source/science/FF/actor grant assumed from this physical implementation.

## 7. Explicit unresolved engineering qualifications — NOT architectural forks
**Q-VAL-01:** Factoring every current I02 validator into a bounded streaming proof engine without altering semantic/replay identity must be demonstrated by exact source-free oracle. Current version expects complete tuple candidates and does multiple passes. If byte parity fails, do not fake validation or silently mint view; return the exact failing projection and required I02 owner decision.
**Q-REPLAY-02:** Full `ReplayManifest@1.0.0` materialization on a native I03 hot query may remain a high-cost path due to `_Execution.used_objects`. P03/P04 must eliminate routine eager use without changing native fact meaning; there may be a narrow separately authorized evidence schema change if mathematically impossible otherwise.
**Q-EXT-03:** `pre553_source_equivalence` certification and `pre553_replay_audit` require concrete release and full closure. Legacy materialization is intentionally a **full audit path**, and its memory/scratch budget must be qualified instead of falsely claiming every audit becomes constant-memory immediately.
**Q-SOURCE-04:** End-to-end source author SRC04 execution still has post-accepted code and grant boundaries. Exact release golden refs can be reproduced only on properly authorized source host, not by pretending redacted packet contains raw cells.
**Q-CACHE-05:** `pre553_parquet_carrier` existing eager path has reusable Parquet integrity but cannot be reused unchanged as columnar direct engine. P02 must qualify event-topology, source identity, compression/dependency and cache lifecycle; same chosen hybrid design remains.
**Q-CONTROL-06:** Some SRC04 native query versions differ between packet and current PRE-MAIN; version the consuming adapter at exact actually selected author branch, not a blended fictitious source.

## 8. S1 disposition / next technical stage
**DECIDED (HQ):** new internal sealed source-backed verified view inside existing repository; old `C11LogicalRelease` unchanged; hot I03/I05 and workload must consume exact view; deterministic full replay identity reconstructed from source-validated closure, cache nonauthority; explicit legacy path for certification and audits; no second query/science owner.

**NOT IMPLEMENTED OR PROVED:** I02 streaming validator, new repository API, exact canonical replay streaming, hot I03 adapter and cache; no executable parity or host improvement has been demonstrated. S2 will produce precise validator pass-by-pass design and an independently checked sourcefree parity harness. A failed parity test is a concrete implementation/authority issue, NOT license to skip it.

**Codex handoff threshold:** sourcefree double-implementation oracle for canonical digests, resolver, M01–M18, exact object/schema, collision/negative cases; reviewed code-owner API; then engineering build orders. No code edits by Browser HQ in this stage.
