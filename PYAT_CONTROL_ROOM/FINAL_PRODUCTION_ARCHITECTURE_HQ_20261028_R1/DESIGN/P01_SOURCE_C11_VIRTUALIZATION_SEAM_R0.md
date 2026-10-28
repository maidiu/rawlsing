# P01 — SOURCE→C11 EXACT LOGICAL VIRTUALIZATION / STREAMING SEAM

**SUCCESSOR RECONCILIATION 2026-10-28:** This is a preliminary R0 kickoff docket. Actual HQ S0 bounded source/callsite audit is `DESIGN/P01_S0_CURRENT_C11_CONSUMER_AND_IDENTITY_AUDIT_R1.md`; exact control SHA 15-file/131-symbol register is `DESIGN/P01_S0_CONTROL_SYMBOL_CENSUS.json`; settled HQ S1 internal interface decision is `DESIGN/P01_S1_SEALED_SOURCE_EXECUTION_VIEW_CONTRACT_R1.md`. These three supersede R0 on verified source/callsite specifics. S0 scoped complete; S1 design chosen but not implemented/test-parity-proved. Continue to S2 validator proof, not an A/B/C discussion.
**State:** R0 source-code-grounded HQ DIRECT INVESTIGATION, not a worker assignment, final code-ready adapter or running change. 14_NONDELEGATION_AND_CLAIM_VERIFICATION_CONSTITUTION.md controls delegation: HQ itself must choose and validate the exact logical C11 seam; a worker may conduct only a bounded per-file callsite census or other corroborating proof.
**Parent stages:** W02/W03; F1/EE01/EE02/EE03/EE04; N1/N4; dependent later W04/W05.
**Purpose:** eradicate routine multi-GB physical/object duplication and preserve exact accepted C11, native I03, replay, source identity and later consumer guarantees. One selected hybrid architecture; no A/B/C design alternatives.

## 1. Actual source-code chain (from sha-verified redacted packet)
```
03_SOURCE_PRODUCER/.../full_runner.py
  run_with_grant (717)
    -> _join_and_select/_slice_config
    -> build_validated_c11_release_from_config (748)
    -> release.public_objects / internal_records (751)
    -> persist_local_release (609; invoked 799)
       -> _write_pickle_stream (590) pickle.dump each object (595)
       -> replay_manifest.as_dict() full JSON (619)
    -> release receipt / current local carrier
04_CURRENT_EXECUTION/.../actual_carrier.py
  load_actual_carrier_release (164)
  load_actual_carrier_view (287)
04_CURRENT_EXECUTION/rawlsing_next/pre553_source_backed_c11_facade.py
  project_c11_candidate_from_physical_cells (498)
     -> for source cells, allocate events/coords/weights lists (515–517)
     -> per-value _event/_coordinate/_weight, events.extend (539) (all object creation)
     -> complete original row/slot check (551–553)
     -> sorted full tuples (554–556)
     -> C11SourceReleaseCandidate (563–570)
     -> build_candidate_replay_manifest (571)
  build_validated_source_backed_c11_release_from_stream (597–603)
     -> validate_c11_source_release(candidate)
  SourceBackedC11SessionCache (612–634)
     -> caches complete C11LogicalRelease in a dictionary, NOT compact event indexes
  build_source_backed_c11_repository (642–653)
     -> C11Repository((release,))
04_CURRENT_EXECUTION/rawlsing_next/pre553_c11_ingest.py
  _candidate_projection_semantic_hash (280) ALREADY HASHES IN CHUNKS
  build_candidate_replay_manifest (380)
     -> _all_nonmanifest_refs(candidate) complete closure_refs tuple
  validate_c11_source_release (743)
     -> validation functions (source, identity, authority, events, topology, replay)
     -> make_m01_m18_coverage
     -> tuple(sorted(_iter_public_objects/...)) (777–778)
     -> _make_validated_release (779), exact semantic release hash
04_CURRENT_EXECUTION/rawlsing_next/pre553_c11_repository.py
  C11LogicalRelease (19–49)
     -> public_objects and internal_records are concrete tuples
     -> validator-only _C11_VALIDATION_SEAL; no arbitrary constructors
  C11Repository (52–111)
     -> _commit_validated stages dict(self._objects) and every public/internal/replay member
     -> resolve_release_exact/resolve_object_exact use exact identity, no fuzzy fallback
04_CURRENT_EXECUTION/rawlsing_next/pre553_empirical_query.py
  _resolve_release_indices (77–108)
     -> loops release.public_objects to match universe (95)
     -> _cached_release_index -> _build_release_index
04_CURRENT_EXECUTION/rawlsing_next/_pre553_query_predicate.py
  _build_release_index consumes release representation; must inspect exact loops before coding
```

## 2. Main technical fact and proper diagnosis
The multi-GB bundle is NOT just an inefficient pickle writer. Existing ingest, logical-release class, object repository and I03 indexing all assume a full materialized object collection. The replay manifest itself holds a tuple of explicit `closure_refs`; avoiding repeated object construction and persistence while preserving the existing logical hash requires a streaming, reconstructible proof. Simply deleting `persist_local_release` or storing the same tuples as Parquet would leave much of the work intact. Reusing A69's lazy C11 facade without verifying I03 releases and exact replay likewise does not prove capability.

## 3. Selected target implementation (conceptual seam, to be made exact by P01)
**Verified release determinant capsule:** exact source SHA, row/physical-slot and event topology manifest, decoder/version, source config/projection/authority roots, expected exact C11 semantic release/ref, canonical section ordering, ReplayManifest exact_ref/projection root/closure proof, M01–M18 coverage, existing accepted seal evidence. Source/authority retain primary truth.

**Private logical event resolver:** accepted exact event/ref syntax resolves to governed C11 object reconstructed from immutable verified source-backed columns/events/authority. Preserve `C11Repository.resolve_release_exact` and `resolve_object_exact` semantics without inventing new public scientific objects. Logical release view supports exact refs, universe ownership, event traversal, section counts and topology. Existing materialized C11 release remains a read/compatibility path for historical artifacts.

**Streaming validation:** validation and canonical release/replay digest must work without holding all events/routing facts and full closure in live Python tuples/dict. Reuse the already existing incremental `_candidate_projection_semantic_hash` technique and A69 single-pass audit/integrity concepts where semantically equivalent. Separate *proof of completeness and identical logical identity* from *massive public-object persistence*. The existing validator-only release seal must remain enforced; DO NOT create `C11LogicalRelease` directly with a fake validation seal.

**Hybrid physical engine:** read authorized source/immutable cache as typed columnar/event data; build compact source-keyed representation once per exact determinant context; maintain correct special/missing/routing, potential multiple occurrence. Regenerable Parquet+Zstd source-backed on-disk cache is not canonical source or new semantic release. Native objects are reconstructed per actual consumer need, potentially in bounded streams.

**C11/I03 boundary:** I03 index and universe binding must use a logical release view rather than scanning an enormous public_objects tuple merely to find one universe. This is an *implementation API adaptation* within existing semantic owner. New version/interface needs explicit validation/owner review; cannot silently mutate accepted fact/replay hashes or source semantics.

## 4. Exact incompatibility questions P01 MUST answer before code
P01-Q1: Can `validate_c11_source_release` validate in a bounded streaming mode using the same exact canonical projection, event/authority topology and complete closure? Specify every validator phase/side effect, order and exact duplicate/missing detection.
P01-Q2: `ReplayManifest.closure_refs` is an identity-bearing tuple of ExactRef; what exact reconstruction/ordering/digest mechanism emits identical logical manifest identity without materializing that tuple resident? May be unavoidable to create it briefly or use a versioned authorized compact reference; DO NOT assume either route.
P01-Q3: Where is `C11LogicalRelease` concrete type/field access required in other owners? Enumerate every `release.public_objects`, `release.internal_records`, `replay_manifest.closure_refs`, `isinstance(release,C11LogicalRelease)` and direct object iteration call site.
P01-Q4: How can the native validator's private seal be preserved without creating a second, more permissive release-construction authority? Exact signed/checked streaming ingest proof needed.
P01-Q5: How does `_build_release_index` obtain complete universe/event/respondent topology, and can it consume verified iterators/compact columns while producing identical exact query facts?
P01-Q6: Which event fields and hashes are deterministic source+authority derivations, which are irreducible stored semantic state, and which require exact source-cell replay? Prove on special/multiselect/rank/repeated and source-universe cases.
P01-Q7: Can cache and source decoding be revoked or missing while a previously accepted logical result still be replayed? Define sealed snapshot availability/refusal and physical cache deletion cases.
P01-Q8: Which current 7.91GB bundle accesses require entire replay material vs one exact ref? Identify end-to-end consumer and cold restore behavior.
P01-Q9: Which schema/version changes (if any) are unavoidable for a lazy logical view? Identify exact owner/issuer and compatibility adapter, not a general theoretical court.
P01-Q10: Which of A69 `pre553_r5_compact_carrier.py`, `pre553_r5_c11.py`, `pre553_r5_single_pass_audit69.py`, and V550 shared substrate code can be reused WITHOUT mutating current scientific source/authority semantics?

## 5. One ordered implementation strategy — not alternative architectures
P01-S0: exact callsite inventory, type/identity contract and current leak/cost profile (source-free; current validated archive).
P01-S1: define internal sealed logical release/resolver interface with full exact-ref behavior; source- and authority-bound deterministic validation receipt. Freeze compatibility before writing adapter.
P01-S2: design bounded streaming candidate/closure creation retaining same semantic digests and source-read gates. Confirm identical replay manifest and full negative states with old baseline.
P01-S3: implement read-through compatibility for accepted C11 materialized releases (never rewrite historical accepted output); new stream-produced releases use compact view.
P01-S4: integrate I03 universe/event index with the resolver; still keep native query/evaluation/issuer/authority contracts unchanged.
P01-S5: remove mandatory per-object pickle and full JSON manifest from routine new source production. Keep optional bounded exact audit/export capability if independent acceptance actually requires full object materialization.
P01-S6: compare exact old vs new outcomes on source-free fixture, then actual authorized SRC04 and a topology-hostile second family, including cold open and cache deletion.
P01-S7: integrate P02 cache and P03 shared I03 kernel only after interface seam stable; no duplicated owner writes.

## 6. Acceptance and risks
- Sealed source/canonical release refs and ReplayManifest exact identity same where existing contract unchanged; if impossible, isolate exact required owner-approved versioned change, no unreviewed hash mismatch.
- Source respondent/event/occurrence binding, routing/missingness/held states, zero/empty, weight/design, authority provenance and selective risk/denominator unchanged.
- Invalid authority/source/read, duplicate or missing physical cell, corrupt cache and invalid historical object ref reject without changing current accepted repository.
- At least one exact native I03 fact and real consumer recovered from cold cache/source. No all-pairs barrier.
- Bounded RAM/disk with actual measurements on Mac; no declared speedup from theoretical array size.
- Independent old path/source oracle plus change/restoration tests, no synthetic fixture promoted to original scientific truth.

## 7. Immediate P01 returned artifact standard
A complete symbol-level source→candidate→C11 repository→I03 index + replay ledger, one exact chosen adapter shape, signature and types, pseudocode for streaming identity/validation and on-demand resolution, no source-read permissions assumed, a concrete module-by-module patch plan and regression suite, plus actual resource accounting design. This R0 is the starting docket: do NOT call P01 done until those details are returned and independently reviewed.

## 8. Owner and coordination
Browser HQ personally owns this design and must verify every decisive claim against original source; current source/repository semantic owners retain authority. Any worker is a limited fact-finder, not a replacement architect. P02 physical cache and P03 query-kernel authors may work in parallel but C11 view API is a shared contract dependency. Once P01 interfaces freeze, Codex assigns one source/ingest/repo integration editor and a distinct I03 interface editor; hostile P11 tests exact cross-boundary semantics. Source-free coding and original source execution remain separate scope grants.
