# P01-S0 — Exact C11 consumer and identity audit, owner: Browser Architecture HQ

**State:** SOURCE-CODE-GROUNDED S0 COMPLETE WITH EXPLICIT SURVEY BOUNDARY; no code edit, no original respondent data, no native test run, no full-repository static enumeration asserted. S1 companion: `P01_S1_SEALED_SOURCE_EXECUTION_VIEW_CONTRACT_R1.md`.
**Code control ref:** `integration/pre-main-reconciliation-r1@299f41e97a43c67be9cc76a79fa49b48f4e12e54`. 
**Packet:** `PYAT_SRC04_BROWSER_HQ_20261028.zip` SHA `94661c14548947bd1c540482841c7c81c7dfc4861b5907f18b91a9e34cd24a5b` containing 112 sourcefree entries.
**Date:** 2026-10-28.

## 1. Source identity verification
Git SHA-1 blob IDs of packet copies compared against *direct current-control* GitHub file blobs:

| File | Current-control blob | Packet Git blob | Identity |
|---|---|---|---|
| rawlsing_next/pre553_c11_repository.py | 67c6eb6494522cd11aab1b93d0e73f9cef6036f3 | same | SAME |
| rawlsing_next/pre553_c11_ingest.py | 37cd35fa2e3420a3eea272a2902e96ab9ba38aba | same | SAME |
| rawlsing_next/pre553_source_backed_c11_facade.py | 8a761119e4a8d68eb291fc4edfadb52e027f8284 | same | SAME |
| rawlsing_next/pre553_empirical_query.py | 03facecf70890bfd13b80418620d274cbcd69d02 | 0453f92c312cce488f8e86f96d1c9ecbd135ce12 | DIFFERENT |
| rawlsing_next/_pre553_query_predicate.py | 8590bacf464b2c61f319f581820a3af76ed1e60c | 17dde8bdf93c773bc8a472aa33e75d593b1009a6 | DIFFERENT |
| rawlsing_next/_pre553_query_eval.py | f808dfcd2008cc71e9203de3cadf1abe14223974 | bfc6be969adf71b0bedf491a62ff6a50160accb3 | DIFFERENT |

**Critical scope rule:** C11/ingest/source-backed code findings apply to direct current control as well as packet. Some recent empirical kernel behavior exists only on different SRC04 author/campaign branches in packet; do not characterize it as the exact current control implementation. Current-control I03 differences were directly fetched/read for `_resolve_release_indices` and `_build_release_index`. The current version additionally relies on concrete release objects and indexes respondent-grain lists. Packet version indexes an additional `events_by_target` map, so interface consumers must support both required access patterns as qualified by active implementer.

All 15 source-free `04_CURRENT_EXECUTION/rawlsing_next` Python files were successfully `ast.parse`-checked (syntax only); no fixture/runtime semantics claimed.

## 2. Bounded direct code census — exactly what was searched
Within all 112 extracted packet entries, a regex pass across every Python file on `C11LogicalRelease|C11Repository|resolve_release_exact|resolve_object_exact|.public_objects|.internal_records|.closure_refs|.replay_manifest|_make_validated_release|_build_release_index|validate_c11_source_release` found **21 Python files and 156 textual hits**. These are keyword hits, NOT 156 unique function callers, nor an exhaustive grep of the live private repo. GitHub search additionally found direct modern core code and tests on its default-branch search index; default-branch search is NOT proof of total absence on this control branch. All material current-core files below were also directly fetched against the exact control SHA. Other branches and unmounted locally running Macs are outside this census.

### Present production and SRC04 consumers — packet line locations
| Component | Exact relevant code / packet lines | Required meaning and migration |
|---|---|---|
| `03_SOURCE_PRODUCER/campaign_src04_completion/release/full_runner.py` | `_write_pickle_stream` 590; `persist_local_release` 609–631; `_state_coverage` 690; `run_with_grant` 717+; fields 751/799/810/816/848 | Currently constructs full objects, pickle.dump separately, writes giant JSON replay, consumes public object list for coverage/receipts; new path must collect certified section counts/special states and emit compact deterministic proof, not delete audits. Not present at same path on control branch; use packet and author commit ref only. |
| `04_CURRENT_EXECUTION/campaign_src04_completion/empirical/actual_carrier.py` | `load_actual_carrier_release` 164–279; `load_actual_carrier_view` 287+ | Reopens full pickle and reconstructs sealed release with `_make_validated_release`; bounded observed view retains every RespondentEvent. Historical accepted existing carrier must stay readable; new source production need not build it. |
| `.../empirical/authorized_execution.py` | `_target_events` 209; loops 234/242; `_make` etc 390–610 | Direct list traversal and `C11LogicalRelease` types; migrate original scientific query/author execution to verified event-view or explicit bounded legacy adapter, never fabricate exact snapshot. |
| `.../empirical/native_workload.py` | `_target_views` 220; `_branch_predicate_ast` 282; direct public/internal loops 316/325; repository 528–540 | Original operation planning constructs target catalog from all events; needs compact per-target metadata+event refs and exact respondent identities, no whole public tuple. |
| `.../empirical/native_streaming.py` | `execute_native_workload_stream` 94+; `isinstance(repository,C11Repository)` 114; resolves `release_ref` 116 | Retain repository class; migrate planning to access verified view; subsequent P05 fixes resume and consumer-before-all-pairs. |
| `.../empirical/consumer_bridge.py` | source native object family refs 199 | Consumer needs released native I03 fact/cells and exact scientific identities, not new public semantic object. |
| `.../consumers/consumer.py` | imports `C11LogicalRelease,C11Repository` 36; contract context 252–255 | Potential strict type consumer; explicit legacy materialization or qualified typed view contract required. |

### Sourcefree/current-owner consumers — exact control paths
| Component | Verified code locations | Current required behavior |
|---|---|---|
| `rawlsing_next/pre553_c11_repository.py` | `C11LogicalRelease` 19–49; `C11Repository` 52–111; `_make_validated_release` 114 | Immutable validated class has private module seal; public_objects/internal_records are tuples. Repository `_commit_validated` copies entire object dict then inserts every public/internal/replay member before atomic publication. `resolve_release_exact` and `resolve_object_exact` must remain exact, no default/latest. |
| `rawlsing_next/pre553_source_backed_c11_facade.py` | `project_c11_candidate_from_physical_cells` 498–573; `build_validated_source_backed_c11_release_from_stream` 597–603; `SourceBackedC11SessionCache` 612–635; `build_source_backed_c11_repository` 642–653 | Source SHA and governed projection checked; `events/coords/weights` accumulate Python native objects; candidate/replay/validated C11 are eagerly materialized. Session cache stores full `C11LogicalRelease`, not native vectors/masks. Existing cache_identity is source SHA, projection ref, required authority refs and slot owner sets (355–377); new cache key must also capture all derivation determinants/versions. |
| `rawlsing_next/pre553_c11_ingest.py` | candidate tuple fields 161–177; streaming candidate projection hash 280–351; closure generation 354–399; validations 485–721; sealing 743–788 | Important: existing candidate hash streams SHA bytes but materializes sorted ref list **per section**. ReplayManifest contains sorted closure_refs of entire candidate; validator compares complete tuple, authority, respondent scope, topology and exact metadata, then builds full sorted public/internal tuples and calls private validated release factory. Streaming validator must preserve **every** check before minting new view. |
| `rawlsing_next/pre553_c11_integrity.py` | ReplayManifest 304–330; internal .ref hash 130–167; `canonical_section_refs` 475–484; `ensure_distinct_event_occurrences` 487+ | ReplayManifest semantic projection includes entire closure tuple; identity hash must be byte-identical, not replaced by a mere closure digest under existing @1.0.0. Event occurrence uniqueness is semantic. |
| `rawlsing_next/_pre553_query_predicate.py` | `_build_release_index` 30–90 at control cut | Enumerates concrete `release.public_objects` to find universe, event, coordinate, routing, weight and relations; enumerates `release.internal_records` for RespondentIdentity; maps per respondent and sorts object refs. Could use verified provider enumerations but remains expensive unless P03 reworks query hot path. |
| `rawlsing_next/pre553_empirical_query.py` | `_resolve_release_exact` 56; `_resolve_release_indices` 77–108; query execution typed repository checks ~389+ | Finds each universe by scanning every `public_objects` tuple of every supplied release and rebuilds index. New read-only execution view can substitute without changing query scope checks or exact I03 fact contract. |
| `rawlsing_next/_pre553_query_common.py` | `_ReleaseIndex` 167–180 | Types `release: C11LogicalRelease`, `respondents` object dict and event/route/coordinate/weight lists. P03 must replace hot index with efficient view, while retaining legacy adapter where exact same algorithm required. |
| `rawlsing_next/pre553_recursive_handoff.py` | `replay_recursive_branch_membership` ~572–613 | Enumerates universe public objects then calls `_build_release_index`; must be migrated to shared provider alongside I03, otherwise recursion recreates whole release or repeats population indexing. |
| `rawlsing_next/pre553_batch_runner.py` | `run` ~397–414 | Expects `C11Repository` and resolves releases by exact ref. Add cheap exact verified descriptor check for routine scheduling; preserve reject on nonexistent/unapproved/out-of-scope refs. |
| `rawlsing_next/pre553_source_equivalence.py` | `CertificationRequest.c11_release` ~392; strict `isinstance(C11LogicalRelease)` ~416; source/replay/closure/authority proof ~568–649; `certify_source_to_c11` 712 | Strong legacy certification consumer; retain explicit original sealed `C11LogicalRelease` path or separately approved certification protocol, no quiet new view substitution. |
| `rawlsing_next/pre553_replay_audit.py` | `assert_release_replay_closure` 170–191; `assert_repository_exact_only` 193+ | Demands concrete C11LogicalRelease and iterates all public objects. Compatibility audit may be bounded cold/materialization path, not hot query path. |
| `rawlsing_next/pre553_parquet_carrier.py` | `ParquetC11Carrier.persist` ~249; `reopen` 279–358 | **Existing** Parquet+Zstd physical carrier, uses pyarrow and per-object relation rows, requires full validated release on input, reconstructs all relations and all native objects on reopen. Demonstrates reusable encoding, integrity, atomic path; DOES NOT remove object-materialization cost and is not yet proposed hybrid columnar hot engine. |
| `rawlsing_next/pre553_source_relations.py` | `resolve_object_exact` consumer (GitHub search) | Preserve exact relation/object resolution even when source-backed view is registered; inspect exact current call and expected type in coding phase. |

## 3. Exact current identity mathematics (existing accepted contract)
At `pre553_c11_ingest.py`:
- SourceReleaseManifest hash = `semantic_hash(manifest.semantic_projection())`, includes source SHA, source IDs, declared family counts, exact universe/authority/retention refs (138–158).
- Candidate projection hash = sorted canonical ref projection of all declared C11 sections plus ingest version and manifest projection (`_candidate_projection_semantic_hash` 280–351).
- ReplayManifest has `semantic_projection_hash` = candidate projection hash, authority set hash, protocol/tie refs, source refs and **entire** `closure_refs` sorted candidate nonmanifest refs (354–399).
- ReplayManifest.ref hash = hash of its entire canonical semantic projection, including `closure_refs`; cannot silently swap content-addressed closure digest into same family/version.
- C11LogicalRelease.semantic_release_hash = `semantic_hash({candidate_projection_hash, replay_manifest_ref, m01_m18})` (772–788); seal private to I02.
- New cache physical hashes/roots MUST be independent and NEVER alter these already accepted logical identifiers.
- Source equivalence and replay auditors have exact full-materialization APIs and retain concrete release path unless explicit newly authorized successor.

## 4. Scientific risk and implementation economics
An optimizer that only replaces pickle files leaves `C11SourceReleaseCandidate`, `ReplayManifest.closure_refs`, I02 validator public tuples, repository global object dict and I03 per-respondent object maps. The giant materialization arises *before and after* serialization.
A streaming I02 validator is nontrivial: current validators iterate candidate sections multiple times, maintain respondent namespace and occurrence sets, verify authority of every public/internal object, compare replay closure and package counts. Replacing tuples with one-pass generators directly is **not sound**. Design must explicitly spool canonical externally sorted data, apply all validation passes and commit only after full exact proof.
The existing ParquetC11Carrier is not a drop-in compact execution view. It reopens every native object. The old R5 Compact-V2 codec and V550 grouped substrate are design capital, not source-science authority.
Returning source SHA alone or a compressed Parquet hash as proof of I02 validation is forbidden. Native source-backed query must respect same universe, routing and exact grant; cache only affects cost.

## 5. Findings vs proven tests
DIRECT_SOURCE_CODE: current listed modules, SHA snapshots, concrete type/tuples and algorithmic sections, replay hash equation, strict certification clients. 
SOURCEFREE_STATIC_TEST: 15 snapshot modules AST parsed successfully. This is syntax, not execution parity.
INFERENCE: streaming/external sorting plus lazy resolution can plausibly reduce peak memory and serialized bloat; actual exact correctness, costs, required memory, object identity and native consumer success NOT PROVED.
NOT INSPECTED: all executable tests on current control branch; all cross-branch variants/local Mac processes; complete 35-wave actual source records; all direct code callsites throughout huge repo outside bounded search; actual P01 refactor/benchmarks.
**S0 disposition:** sufficient verified consumer/identity map to choose S1 API, NOT sufficient to claim refactor implemented, source-certified or performance measured.

## 6. Concrete present location and source cuts
Repository: `maidiu/rawlsing` (PRIVATE), current control `299f41e97a43c67be9cc76a79fa49b48f4e12e54`.
Source proof blobs: repo `67c6eb6494522cd11aab1b93d0e73f9cef6036f3`; ingest `37cd35fa2e3420a3eea272a2902e96ab9ba38aba`; facade `8a761119e4a8d68eb291fc4edfadb52e027f8284`; Parquet `9dad6713a3aae66717d4ab046e802a72c9b2aa90`; replay audit `86e0b9c518633735f2527b89fb72fca1a40dc2cc`; source equivalence `0e7f9f6d77ef6efe2c66b04f0527bb1ab99f4ef8`; recursive `868f43bf9869af5501fd67c3de7a2703ba4cb1b4`; current I03 `03facecf70890bfd13b80418620d274cbcd69d02`; current predicate `8590bacf464b2c61f319f581820a3af76ed1e60c`.
Historical source-author export code is available within the attached SHA-qualified packet and pinned author/reviewer refs in `03_EXACT_SOURCE_AND_CODE_LOCATORS.md`. 
