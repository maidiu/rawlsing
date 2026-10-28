# P01-S3 — HQ definitive implementation map: exact validated C11 execution view

**Owner:** Browser Architecture HQ — personal direct investigation and decision; no independent worker or new semantic issuer.
**Date:** 2026-10-28. **Code base:** `maidiu/rawlsing`, pinned integration/pre-main-reconciliation-r1 at `299f41e97a43c67be9cc76a79fa49b48f4e12e54`. **Design branch:** `agent/pyat-final-production-architecture-hq-20261028-r1`.
**Status:** CODE-READY DESIGN SPECIFICATION / NOT PRODUCTION IMPLEMENTATION / NO ORIGINAL DATA EXECUTED / NO PHYSICAL SPEEDUP PROVEN. Qualification and approved integration remain for Codex.
**Binding architecture:** Source-authoritative compact regenerable hybrid. No A/B/C route competition. Source/semantic authority, exact identities, full I02 logical validation, I03/I05 semantics, and old accepted materialized releases remain controlling.
**Required reading:** P01-S0 exact current code audit + P01-S0 symbol census; P01-S1 view interface; P01-S2 every validation pass and source-free proof; 36-item high-resolution ledger; constitution 14; existing native I02 tests.

## 0. Decision, object ownership and precise build goal

The present code assembles all `RespondentEvent`/`RoutingEligibilityFact` and `ReplayManifest.closure_refs`, constructs `C11SourceReleaseCandidate`, calls `validate_c11_source_release`, stores tuple-backed `C11LogicalRelease` in `C11Repository`, and indexes all events again for I03. The SRC04 producer then emits a multi-GB Python pickle/JSON materialization. The old `pre553_parquet_carrier.py` similarly requires eager native objects when reading and writing. These facts are separately supported by code/receipts.

**We build two representations of THE SAME validated logical release:** existing concrete sealed `C11LogicalRelease` for old accepted/certification/audit consumers; new private **I02-certified exact source-backed execution view**, with compact row/event/occurrence/identity stores, deterministic replay-reference stream, bounded on-demand exact native object construction, and unchanged `ExactRef`/native query results. The latter is an implementation view, never public scientific truth or source permission. An unvalidated cache manifest cannot produce it.

## 1. Exact file/symbol change list — one integration plan

| File | Existing owner/symbol at cut | Mandated new delta | Prohibited change |
|---|---|---|---|
| **NEW** `rawlsing_next/_pre553_c11_journal.py` | no current file claim; new private I02 implementation | `JournalWriter`, immutable `PreparedC11Journal`, framed exact field/semantic object records, external section/global ref-sort readers, index build, checksums, scratch resource guard, abort/close/recover API | No semantic authority, no open-from-cache-as-sealed |
| **NEW** `rawlsing_next/_pre553_c11_stream_validation.py` | new private I02 implementation | `validate_prepared_journal`: pass-by-pass V01–V10 legacy I02 checks over authenticated journal; exact disposition precedence; issue I02-only private validated receipt AFTER source-admission check | No "count+hash" shortcut or section-dropping |
| **NEW** `rawlsing_next/_pre553_c11_execution_view.py` | new private I02 representation | immutable `C11VerifiedReleaseHeader`, `C11ExecutionView` protocol, `C11VerifiedSourceView`, bounded native row/target/source-ref resolution, exact closure enumeration; explicit legacy materialization method | No alternative C11 public ontology or query eligibility rules |
| `rawlsing_next/pre553_c11_ingest.py` | `_candidate_projection_semantic_hash` 280; `_all_nonmanifest_refs` 354; `_validate_*` 451–721; `validate_c11_source_release` 743; `ingest_c11_source_release` 791 | expose **private** semantic-hash/validator helpers for journal engine without modifying old exported behavior; I02-only `_admit_prepared_source_journal` checked receipt; same `IngestDisposition`; complete V01–V10 parity | Never replace old full-candidate validator with untested generator; no silent contract/version change |
| `rawlsing_next/pre553_c11_integrity.py` | `ReplayManifest` 305; `authority_snapshot_set_hash` 467; `ensure_distinct_event_occurrences` 487; `make_m01_m18_coverage` 510 | private bounded occurrence-key/coverage serialization helpers invoking exact old canonicalization; preserve `ReplayManifest@1.0.0` identity | No closure digest substitution; no binary floats or dedup |
| `rawlsing_next/pre553_source_backed_c11_facade.py` | `ExactPhysicalCellStream` 248; `GovernedC11Projection` 264; `cache_identity` 355; `project_c11_candidate_from_physical_cells` 498; `build_*release*_stream` 597; session cache 612; `build_source_backed_c11_repository` 642 | **new explicit** `build_validated_source_backed_execution_view` entry with source-byte admission receipt; stream row/slot+occurrence processing into journal; retain original public API full materialization for compatibility. Adapt source-backed repository/execute helpers only after exact view proof | Existing `ExactPhysicalCellStream.source_sha256` string MUST NOT count as proof bytes were read; existing cache identity insufficient for durable authority-sensitive cache |
| `rawlsing_next/pre553_physical_c11_bridge.py` | `build_validated_c11_release` | keep untouched; optionally add bounded adapter for source-incidence stream in same owner after source fixture equivalence | No claimed source rights from physical incidence |
| `rawlsing_next/pre553_c11_repository.py` | `C11LogicalRelease` 19; `C11Repository` 52; `resolve_*_exact` 73/81; `_commit_validated` 89 | keep same class and old exact API; add `_by_view_ref`, `_object_owners` or equivalent compact ref-to-release index, `resolve_execution_view_exact`, `verify_release_ref_exact`, private `_commit_i02_verified_view`. Exact collision/atomic publication across old+view; legacy materialization explicitly metered on old accessor if required | No public register-untrusted-view; no accidental full release build for query; no defaults/latest |
| `rawlsing_next/pre553_empirical_query.py` | `_resolve_release_indices` 65 at control cut; `execute_empirical_query` 373 | use verified execution view when registered; old sealed release adapter otherwise; exact multi-universe release-scope matching unchanged | No changed query estimand/authority/error state |
| `rawlsing_next/_pre553_query_predicate.py` | `_build_release_index` 19; predicate evaluators | split legacy/materialized indexed constructor from exact-view constructor; both return compatibility index with same respondent/target/routing semantics; P03 later optimizes grouping, NOT P01 | No flattening multiselect, no invented risk denominator |
| `rawlsing_next/_pre553_query_common.py` | `_ReleaseIndex` 158 at control | narrow `release` annotation/internal accessor to verified identity provider where necessary, preserve exact `release_ref` + replay `ref` behavior, all old fields and runtime authority | No generic object proxy silently triggering huge replay load |
| `rawlsing_next/_pre553_query_eval.py` | current control `_make_execution_replay_ref` ~516, `_build_fact` later; packet differs | prevent constructing giant `ReplayManifest` in hot path by use of **exact replay ref only** ONLY AFTER full audit of `_Evaluation.used_objects` and native provenance/ref creation. Maintain full existing ref membership, fact/replay hash and evidence semantics | No ref-only optimization if actual fields/authority/semantic path require full object; no new fact schema without competent issuer |
| `rawlsing_next/pre553_recursive_handoff.py` | `replay_recursive_branch_membership` 572–613 | use exact-view universe lookup and shared respondent/occurrence index; retain exact persisted branch membership and ancestry | No synthetic grouping or I05 semantic changes |
| `rawlsing_next/pre553_batch_runner.py` | `run` ~397–414 | use cheap `verify_release_ref_exact` for scope validation; I03 still enforces actual query/use permission | No treating existence as authority |
| SRC04 author branch: `campaign_src04_completion/release/full_runner.py`; `empirical/actual_carrier.py`, `native_workload.py`, `native_streaming.py`, `authorized_execution.py` | author-only packet, **NOT at these paths on current integration cut** | exact code SHA reconciliation and subsequent owner-granted runtime migration; preserve historical accepted 7.91GB artifact and receipts; avoid giant new build / all-pairs prerequisite | No source run or direct merge of unqualified author successors |
| `rawlsing_next/pre553_source_equivalence.py`, `pre553_replay_audit.py`, `pre553_parquet_carrier.py` | concrete `isinstance(C11LogicalRelease)`, full closure / public tuples | **NO initial mutation**; use separately metered `materialize_legacy_release_exact`, with source/certification access and resource check. Later optimize audits only by explicit applicable acceptance law | No substituting a header for an accepted full equivalence/certification test |

**Dependency note:** Existing `pre553_parquet_carrier.py` is an eager *canonical relational carrier*, not the new non-authoritative computational cache. The latter is a P02-only later integration; it cannot register a view.

## 2. Chosen internal interfaces — implementation-level types, errors, and use

Use these types as **proposed private APIs**, to be finalized in reviewed code without new externally published scientific families:

```python
# _pre553_c11_journal.py
@dataclass(frozen=True)
class JournalSourceBinding:
    source_artifact_ref: ExactRef        # EXACT observed source SHA, not user assertion alone
    source_retention_ref: ExactRef
    source_read_receipt_ref: ExactRef    # actual qualified source-owner verification
    projection_identity_ref: ExactRef
    projection_derivation_digest: str   # MUST cover complete value/slot/row topology, not only facade.cache_identity
    decoder_implementation_digest: str
    authorization_roots: tuple[AuthorityRef, ...]
    declared_family_counts: Mapping[str, int]
    transport_kind: str

class PreparedC11Journal(Protocol):
    def section_status(self, name: str) -> SectionStatus: ...
    def iter_section_exact(self, name: str): ...      # verified native reconstruction
    def iter_section_ref_sorted(self, name: str): ... # multiset, no dedup
    def iter_global_closure_sorted(self): ...         # includes source & retention refs
    def lookup_exact_native(self, ref: ExactRef): ... # checks content hash on decode
    def iter_occurrences_sorted(self): ...
    def read_identity_header(self): ...
    def verify_physical_integrity(self): ...
    def close(self): ...

# _pre553_c11_stream_validation.py
def _validate_prepared_journal(
    journal: PreparedC11Journal, source_attestation: QualifiedSourceAdmission
) -> I02VerifiedJournalReceipt: ...
# Can only be called from qualified I02 private issuance path.
# No public constructor that accepts a saved checksum/manifest as the receipt.

# _pre553_c11_execution_view.py
@dataclass(frozen=True)
class C11VerifiedReleaseHeader:
    release_id: str
    release_ref: ExactRef
    source_artifact_ref: ExactRef
    source_release_manifest_hash: str
    semantic_release_hash: str
    replay_manifest_ref: ExactRef
    m01_m18_coverage: Mapping[str, tuple[str, ...]]
    universe_refs: tuple[ExactRef, ...]
    # internal nonsemantic source/decoder/projection/version/validation receipt identity

class C11ExecutionView(Protocol):
    @property
    def header(self) -> C11VerifiedReleaseHeader: ...
    def contains_universe_exact(self, ref: ExactRef) -> bool: ...
    def resolve_universe_exact(self, ref: ExactRef) -> EmpiricalUniverse: ...
    def iter_respondent_identities(self, universe_ref: ExactRef): ...
    def iter_native_events(self, universe_ref: ExactRef, target_ref: ExactRef | None = None): ...
    def iter_routing(self, universe_ref: ExactRef): ...
    def iter_coordinates(self, universe_ref: ExactRef): ...
    def iter_weights(self, universe_ref: ExactRef): ...
    def iter_source_relations(self, universe_ref: ExactRef): ...
    def iter_exact_object_refs(self, *, include_internal: bool = True): ...
    def resolve_object_exact(self, ref: ExactRef): ...
    def iter_replay_closure_exact(self): ...
    def materialize_legacy_release_exact(self, *, budget: ResourceBudget) -> C11LogicalRelease: ...

# pre553_c11_repository.py — ADDED, not existing today
def resolve_execution_view_exact(self, release_ref: ExactRef) -> C11ExecutionView: ...
def verify_release_ref_exact(self, release_ref: ExactRef) -> C11VerifiedReleaseHeader: ...
def _commit_i02_verified_view(self, view, receipt): ...
# existing resolve_release_exact(ExactRef) RETURNS C11LogicalRelease, old behavior
# existing resolve_object_exact(ExactRef) RETURNS actual native object
```

**Compatibility adaptation:** A materialized release is wrapped in a no-new-authority `C11ExecutionView` adapter. A new source-backed view can rehydrate a full legacy release, but this must be **explicit and resource-limited**, never incidental to calling `resolve_execution_view_exact`. Existing legacy `resolve_release_exact` may rehydrate it to preserve old type, but the method and callsite must be instrumented so hot execution cannot silently invoke it.

**Replay ref:** `header.replay_manifest_ref` alone is enough only for consumers that need solely that exact ref. Any native fact path retaining a whole object for semantic/provenance reasons must either obtain a verified exact object or preserve equivalent legacy behavior. A cheap proxy with a counterfeit `ReplayManifest` must NOT be introduced.

**No public scientific surface is added.** `JournalSourceBinding`, I02 receipt, physical-view headers and cache metadata are implementation records and cannot substitute for a source manifest or an empirical fact.

## 3. Detailed source-read/project/validate/publish flow

```text
qualified source byte access
  -- actual source SHA verified by source owner / decoder / projection authority
  -> qualified source-admission receipt (separately established; never by user-supplied string)
  -> governed row & slot rules + exact source-cell iterator
  -> private journal staged outside repository visibility
      append exact reconstructible semantic event and internal records
      note section status and typed absence
      preserve row, question, occurrence, topology and authority determinants
      build ref/namespace/occurrence indexes with bounded spill
      hash/checksum staged physical frames
  -> I02 private validation (ALL legacy V01–V10, original failure priority)
      sections and declared counts/multisets
      exact authority closure and full object validation
      respondent namespace / occurrence / question / relation checks
      canonical candidate hash and ReplayManifest exact full closure multiset
      M01–M18 and exact release root
  -> issue in-process I02 receipt linked to exact source-admission receipt
  -> single repository atomic check + register verified view; snapshot identity stays exact
  -> physically publish immutable verified journal for cold read
  -> optional P02 cache becomes an acceleration derived from journal/source
  -> hot query resolves execution view, old auditors resolve full legacy materialization
```

**Cold reopen:** persist journal frames/physical indexes + proof manifest + original source-authority/source-admission receipt reference. On reopen validate physical checksums, source/decoder/projection version binding, source-admission receipt validity, complete saved proof and exact ref inventory. **Saved I02 self-asserted receipt is not automatically trusted.** Re-establish authenticated I02 approval by re-executing full logical validator on the source journal if proof/custody cannot independently authenticate an exact prior accepted release; if source rights or files unavailable, fail closed. There is no automatic source-byte re-read permission from possession of a cache.

**Critical original data limit:** `ExactPhysicalCellStream(source_sha256=...)` can carry a claimed digest, not verified source bytes. It is valid as a source-free or caller-authorized transport but **NOT by itself sufficient to mint a new cold-replay qualified verified view**; source admission must independently supply verified byte custody and matching retention.

## 4. Exact validator coupling rules (from S2, required for implementation)

- `_validate_sections` requires **nonempty universes, respondents, questions, events, routing, coordinates, authority snapshots**. Optional family typed-absence values differ, not generic null.
- `_validate_declared_manifest` compares **multisets** (sorted tuples) of universe and authority refs, requires seven core count declarations and matches all declared counts; does not require every optional family count to be present.
- `_validate_authorities` validates each authority snapshot, `validate_public_carrier_object` on **every** public object, nested authority refs on public semantic fields and internal record projections, and positive replay protocol.
- `_validate_universe_and_respondent_scope` enforces exact universe namespace, distinct respondent (universe,key) and every respondent-grain event/route/coord/weight binding.
- `_validate_questions_and_events`: event exact (universe,native question) binding; duplicate occurrence material includes universe, respondent, native question, component, event group, event id/index. A value collision is NOT occurrence collision; duplicate occurrence can happen even for different object hashes.
- `_validate_question_authorities`: exact mapping, topology and identity-map authority.
- `_validate_source_relations`: explicit DISTINCT_BY_DEFAULT or per-ref declared scope; no inferred pool.
- `_validate_replay`: candidate hash exact, authority set hash exact, source substrate singleton, global closure **sorted multiset with duplicates** (source artifact and source retention refs included), replay authority exact. `ReplayManifest@1.0.0` still hashes full logical closure; a digest-only substitute is a new contract and NOT authorized.
- M01–M18 exact original coverage labels and presence policy; same C11 root `semantic_hash({candidate_projection_hash, replay_manifest_ref, m01_m18})`.
- Existing `_make_validated_release` is importable and called by existing Parquet reopening; private seal is not cryptographic. The **new view** needs a private I02 validated-admission path and authentic source byte/retention binding, not a physical-certificate constructor.

## 5. Delivery phases within S3/S4 (strict dependency, no false stage closure)

**S3-A: freeze new private schema and complete native golden fixtures, before changing production path.** Design/implement fixture builder for every mandatory/optional family, multiuniverse, Unicode, exact numerics, multiselect/rank, routed/unknown/zero, weighted and all tolerated absences. Old I02 produces golden refs and refusal classes. Record source/expected hashes independently.

**S3-B: deterministic physical journal, indexing and canonical byte oracle.** Add new private journal module only; run existing sourcefree accepted fixture through new writer/reader. Distinguish ref-kind/object-family and occurrence identity; reject corruption/truncation/duplicate physical row-slot. Native object round-trip exact. No repository adoption.

**S3-C: full journal-native I02 validation equivalence.** Add internal validator; re-use original helpers via bounded native rehydration where needed. For every fixture, compare old/new `IngestDisposition`, release hash, replay manifest hash, exact reference inventory and M01–M18. Multi-fault error ordering preserved. Still no deployment.

**S3-D: source-attested private view and atomic repository integration.** Add explicit verified source-admission type/factory, private I02 receipt and exact-view registry; preserve old C11 type and all historical releases. Test rollback, collisions, committed snapshot equality, forged receipt, stale authority, interrupted cold reopen and missing source.

**S3-E: I03/I05 consuming seam.** Only after D, shift internal query/discovery release lookup. Preserve original field/query contracts, all risk states and native fact/replay identities. If full ReplayManifest is needed in I03 provenance, first independently prove ref-only equivalence; otherwise retain exact legacy object materialization for that narrow use and defer optimization to P04; do NOT lie that hot-path bloat is already eliminated.

**S3-F: source producer/other engines and real host.** Exact SRC04 author branch/owner rebase, qualified source grant and original result acceptance; source-first cache and P02/P03 later. Current accepted original pickle release untouched and directly resolvable. Benchmark all phases, but not a route bakeoff.

## 6. Resource/atomicity safeguards and rollback

- A true 16-GiB host cannot rely on simultaneously retaining native materialized release, journal, query index, and full replay JSON; every phase must state upper bound and sampled peak RSS/scratch/CPU, configurable safe stop and cleanup before mutating accepted state.
- Journal scratch outside repo, per-run locked namespace, immutable staging; digests per frame and durable manifest; recover incomplete staging as **not admitted**. Never commit partially verified release or partial per-object indexes.
- Atomic publication across view, legacy ref namespace, object-ref owner map and release_id rule. Stage all collision decisions before any visible map changes. On error: `release_refs`, `snapshot_identity`, object lookup and source attestation unchanged. Cold crash before completed durable publish cannot register a ghost release.
- Runtime authority is checked on every query/consumer operation through existing owner. Repository presence and source/cache availability do NOT grant scientific interpretation.
- Rollback switches production calls to **unchanged materialized implementation**; accepted artifacts and external native fact refs are never rewritten by rollback. No force-push, migration of all 35 waves or historical source retirement as prerequisite.
- Source-free and original-data tests remain distinct. An original-source run requires actual current custody/issuer/workload permission, not this design branch.

## 7. Acceptance standard for this S3 specification and future code

S3 is accepted as a *design* when: exact files/functions/ordering, types and error modes, proof inputs/outputs, identity formulas, stage interfaces, old/new compatibility, source-attestation requirements, test cases, resource ceiling, writer collisions, code-owner rights and rollback are all explicit; all 36 high-resolution findings are mapped to owner and tests. This document and the linked machine-readable tickets meet the organizational aim, not execution proof.

**Actual P01 code acceptance** requires all S3-A–E sourcefree tests + hostile independent review; actual production scientific acceptance subsequently requires authorized real-source provenance/equality/consumption. If any test detects a logical hash drift, typed negative drift or unqualified source/authority, stop and report the exact counterexample; never relax old validation to force PASS.
