# 02 — Exact execution ABI and three nonconflated DAGs

**Status:** design proposal, not an existing implementation, source/native science, I02 seal reissuance or accepted API. **Code cut:** [protected PRE-MAIN `1f77f2036427a410429184780ef884ec4f253ad0`](https://github.com/maidiu/rawlsing/tree/1f77f2036427a410429184780ef884ec4f253ad0). Refer to [01](01_REQUIREMENTS_REUSE.md) for functional conservation and historical grades. The selected October 28 target is fixed. Existing W03/W04 author lanes own their scoped writer and saved-access design decisions until independent return.

## A. DAG 1 — scientific meaning and authority; not an execution scheduler

```text
original bytes/administration/instruments/rights ──(S01 independent source owner)──┐
QSM, response, route, identity, measure, time, mapping ──(applicable rule selection)─┤
                                                                                 ↓
eligible U_item/U_unit/U_app/E_pre + scientific/host-purpose issuer (S02) ──→ admitted native envelope
                                                                                 ↓
governed projection + complete I02 validation ──→ canonical C11 release, semantic/replay roots (S03)
                                                                                 ↓
      per-query exact source/risk/condition/response/measure authorization
                          ↓                        ↓
                    I03 native facts          I05 frozen frontier, candidate fates
                          └─────────┬──────────────┘
                                    ↓
          S04 F1/F2/F3/F4 eligible empirical products + negative/held coverage
                ├──→ direct authorized empirical possibility (N10E)
                ├──→ M1/M2/B5 learned lifecycle, when applicable (S05)
                └──→ FF01 exact empirical count/support ingress (S06)
                         └──(only competent structural/position authority)──→ FF02/N5/N6
     optional F6 independent source composition; F7 wave/time comparison; N9 served world
     N9 AND N10E → N10W for selected world-conditioned possibility; N11 → separate N12/Sorok
```

The inclusion of a source in the 35-wave fixed estate is not its current eligible operation permission. A valid C11 I02 seal says that the declared projection was validated, not that all historical source semantics/QSM selections were recovered. A sourcefree negative result is not an original35 fact. Observed empirical relation does not imply causality, objective class power or personality. **No physical index or SQL planner may issue any of these authorities.**

## B. DAG 2 — actual protected code/call graph at frozen source cut

```text
pre553_physical_decoder.py:825/839 decode_sav/decode_dta
        → PhysicalSourceIncidence / ExactPhysicalCellStream
pre553_source_backed_c11_facade.py:268 GovernedC11Projection
        → :502 project_c11_candidate_from_physical_cells
        → pre553_c11_ingest.py:743 validate_c11_source_release
        → pre553_c11_repository.py:26 C11LogicalRelease
        → facade.py:656 build_source_backed_c11_repository
             [optional _pre553_c11_execution_view.py:239 _compact_public_objects]
        → C11Repository._commit_validated (:115) object dict + I03 index slots
        → pre553_carrier_execution.py:403 CarrierNeutralResearchExecutor
             → :430 execute_i03 → pre553_empirical_query.py:685 execute_empirical_query
                  → _pre553_query_predicate.py:63 _build_release_index / :18 _select_respondent_events
                  → _pre553_query_eval.py:626 _evaluate_index_group → :879 _build_fact
             → :457 execute_i05 → pre553_discovery_exact.py:1052 exact bounded discovery
        → pre553_route_b_production.py:495 execute_route_b_production [full route/replay]
pre553_issued_workload.py:219 admit → :280 execute_issued_workload
        → :332 Batch execute callback, :... BatchExecutionRunner in pre553_batch_runner.py:385
        → retained results/receipts; :614 capture, :686 restore, :767 resume
S04 factual I03/I05 output
        → pre553_analytical_composition.py:1064 compose_positioned_subject_possibility
        → pre553_empirical_possibility_provider.py:531 provide_empirical_possibility_slice
        → field_forge_conditional_support.py:467 produce_exact_conditional_support_profile
        → gt12_c_to_d_relation_bridge.py:93 bridge_gt12_c_relation_to_d_evidence [bounded Q86 test]
        → pre553_structural_admission.py:529 evaluate_structural_empirical_admission [own rule]
```

**Confirmed duplicate construction path:** `execute_issued_workload` lines 301–310 invokes `execute_route_b_production` **once per discovery** (including its own `build_source_backed_c11_repository` at `pre553_route_b_production.py` 555–582), then calls `build_source_backed_c11_repository` again at issued-workload lines 310–312. With **one or more discoveries**, at least two repository/release constructions can occur from the same issued source without shared cache; with no discoveries that redundant Route B build does **not** occur. This is a real conditional duplicate, not a blanket claim that every query builds twice. Separate I03/Batch routing and source/context checks must remain equivalent.

**Confirmed eager saved reopen:** `pre553_parquet_carrier.py::persist` L249 and `reopen` L279–360; `_relation_objects` L212 materializes all relation object lists; `_write_tables` L228 forms all per-relation row dicts, sorted lists and one Arrow Table; `reopen` L294–347 loads/validates every relation, builds objects, calls private `_make_validated_release`. Current `C11LogicalRelease` requires hidden I02 seal (`pre553_c11_repository.py` L44–51), and `CarrierNeutralResearchExecutor.__post_init__` L410 requires a genuine `C11Repository`. A lazy proxy cannot pass either legitimate boundary.

## C. DAG 3 — physical persistence, derived calculation and crash recovery

```text
immutable source snapshot + exact governed projection/authority
    ↓ successful complete canonical writer / I02 accepted release
    ↓ canonical Parquet C11 release + member/logical digests + manifest + release identity
    ├── authenticated read session [NEW VERSIONED PRIVATE ABI; no counterfeit seal]
    │      ├── bounded on-demand canonical exact-event/ref resolution
    │      ├── optional computed typed projection [derivative, source/version keyed]
    │      └── optional specialized postings / Arrow batches / DuckDB physical aggregation
    ├── issued operation identities + current-source/host/purpose admission
    │      └── Batch unit manifest
    │             ├── qualified physical evaluation evidence [transient]
    │             ├── native I03/I05 exact finalization and replay
    │             └── staged immutable output + verified receipt (per unit)
    └── retained necessary scientific products (S04, learned, FF01)
                └── exact consumer/value-read receipt
crash: discover stage/commit/orphan → verify expected input+unit, bytes/authority+semantic result
       → adopt valid completed unit or recompute exact missing dependency only
source/issuer/codec/schema invalidation: derived physical accelerators and completed-result entitlement
        invalidated independently of historic semantic validity
```

This is **not** the historical respondent/semantic relation DAG and **not** a new scheduler. The existing native Batch work units remain the only operation identity. Materialization/eviction never changes semantic availability.

## D. Proposed private ABIs — contracts to be negotiated with present owners, not implemented aliases

### D1. One validated release for one normal issued workload

Current `execute_issued_workload` must be refactored behind its own owner so a single scoped, exact *prepared source execution context* supplies both optional Route B receipts and Batch I03/I05. A shape sufficient for author/reviewer discussion:

```python
@dataclass(frozen=True)
class PreparedNativeSourceSession:
    issued_envelope_sha256: str
    source_sha256: str
    release_ref: ExactRef
    projection_binding_identity: str
    replay_ref: ExactRef
    repository: C11Repository          # initial implementation, real sealed repo
    executor: CarrierNeutralResearchExecutor
    catalog: RuntimeObjectCatalog
    current_decision_ref: ExactRef      # never a permanent grant

def prepare_issued_source_once(
    *, admitted: IssuedWorkloadRecord, source, projection, catalog,
    existing_accepted_release=None
) -> PreparedNativeSourceSession: ...

def execute_route_b_from_prepared(
    *, prepared: PreparedNativeSourceSession, requests, discovery_authority_ref
) -> RouteBProductionResult: ...
```

**Compatibility requirement:** the initial refactoring must preserve `execute_route_b_production`'s graph, learned/replay receipt, exact binding IDs and `execute_issued_workload` Batch outputs, unit hashes and negatives. It must not simply skip Route B receipts to save work. Establish exactly when source factory may be avoided: only after current `admit`, and only if an authorized saved-release identity matches the selected original source, projection and scientific envelope.

**Lifetime:** one issued-workload invocation or bounded compatible execution batch; existing `I03GroupedExecutionScope` remains request-local, finite and explicitly closed. Any sharing beyond a live current-decision scope requires separate acceptance.

### D2. Saved-C11 read interface (a genuine I02-owned evolution)

```python
@dataclass(frozen=True)
class VerifiedSavedReleaseIdentity:
    release_ref: ExactRef
    source_artifact_ref: ExactRef
    source_release_manifest_hash: str
    semantic_release_hash: str
    replay_ref: ExactRef
    canonical_member_root: str
    i02_admission_proof_ref: ExactRef   # proposal: verify accepted historic I02 result

class VerifiedC11ReadSession(Protocol):
    @property
    def identity(self) -> VerifiedSavedReleaseIdentity: ...
    def resolve_exact(self, ref: ExactRef) -> CanonicalSemanticObject | C11InternalRecord: ...
    def iter_respondents(self, universe_ref: ExactRef): ...
    def iter_routing(self, universe_ref: ExactRef, respondent_ref: ExactRef, target_ref: ExactRef): ...
    def select_events(self, universe_ref, respondent_ref, target_ref, *, include_component, states): ...
    def iter_coordinates_weights(self, universe_ref, respondent_ref): ...
    def close(self) -> None: ...

def admit_saved_release(
    *, exact_external_pin, carrier_root, expected_release_ref,
    accepted_i02_proof, current_host_purpose
) -> VerifiedC11ReadSession: ...
```

**No such public API exists at the inspected cut.** These signatures are *proposed private contracts*. Source owner supplies the trustworthy I02 proof and current-use permission; physical code verifies release/manifest/segment membership, schema, root and selected exact-object integrity. An untrusted `manifest.json` cannot self-issue the `i02_admission_proof_ref`: this must be anchored to an independently accepted complete I02 result. An externally trusted root and exact historical release identity alone do not guarantee present entitlement.

**Two compatible routes:** (a) initial safe baseline: existing `ParquetC11Carrier.reopen` returns an actual verified `C11LogicalRelease` and a normal `C11Repository`; (b) after independent ABI acceptance: native I03/I05 receive **explicitly typed** `C11Repository | VerifiedC11ReadSession`, or a named shared repository-access protocol with separately verified constructors. No duck-typed object pretending to be `C11Repository`, no call to `_make_validated_release` from the new handle, and no bypass of `CarrierNeutralResearchExecutor`'s exact binding. The semantic owner must decide how certified canonical coverage, full member integrity and the accepted original I02 proof coexist without eager reopen.

**Read semantics:** exact refs, universe/row/respondent identities, occurrence/order/rank/duplicate multiplicity; native and independently authorized canonical values; source-specific physically missing vs response missing vs routing states; coordinates, weights/design and authority snapshots; stable iteration and replay. Read buffers have bounded lifespan; absence of fetched row is never semantic absence. Invalid or absent selected member must refuse or trigger authorized rebuild, never produce an empty selection.

### D3. Qualification-before-columnar-calculation contract

```python
@dataclass(frozen=True)
class QualifiedOperationScope:
    exact_release_and_universe_refs: tuple[ExactRef, ...]
    exact_query_ref: ExactRef
    exact_predicate_ref: ExactRef
    exact_risk_set_ref: ExactRef
    target_plan_identity: str
    measure_basis_ref: ExactRef
    authority_snapshot_identity: str
    risk_and_routing_validation_ref: ExactRef
    respondent_complete_qualification_root: str
    current_decision_ref: ExactRef

@dataclass(frozen=True)
class PhysicalEvaluationStream:
    qualified_scope: QualifiedOperationScope
    # exact selected respondent contributions, zero-domain determinants,
    # used source/event/authority references, rational weight identities,
    # unsupported/negative states and repeat-event topology.
    contribution_batches: object

def qualify_exact_operation(*, session, query, predicate, registry, issuer): ...
def plan_physical_operation(*, qualified_scope, capability_manifest): ...
def compute_physical_evidence(*, physical_plan, session): ...
def finalize_native_fact(*, evidence_stream, query, predicate, native_owner): ...
```

This is a design surface, not an instruction to define a new public `EmpiricalFact`. The existing `_Evaluation` in `_pre553_query_eval.py` L626–821 remains the first exact comparator: `risk_members`, `denominator_members`, `raw_denominator`, `raw_resolved_target_support`, complete `raw_cells`, `weighted_cells` using `Fraction`, `used_objects` and `used_authority_refs`. The native `_build_fact` L879 and replay L848 own public identity. The initial fast capability manifest should allow only explicitly tested scalar RAW cases under fully resolved routing, response topology and exact authority; otherwise native. No SQL or Arrow count is permitted to decide risk-set scope, known-zero eligibility, numerator/denominator meaning, source comparison, causality or publication.

**Qualification must examine respondents whose *invalid* routing/authority/missing evidence would force refusal, including rows that an efficient SQL filter would otherwise drop.** Only after complete qualification may selection pushdown run. Qualification witnesses may be shared only when exact scope, authority, risk/topology/measure and currentness dependencies are demonstrably identical. The existing grouped cache explicitly disables reuse under `current_runtime_binding` and runtime index authorities (`pre553_empirical_query.py` L543–579); preserve this.

### D4. One independent current issuer across **COMPLETED / PARTIAL / ABSENT** resume and protected output

**R2 D1 root cause (verified):** `pre553_issued_workload.py::resume_joined_workloads` L767–836 has **three** branches. The COMPLETED branch calls `_completed_entry_view` L741 without `admit`. PARTIAL and absent/new branches call `execute_issued_workload(item.workload, _resolver_for(item), ...)`, where `_resolver_for` L832 returns the supplied `item.record`, not an independently current issuer decision. Therefore **adding `admit()` to COMPLETED alone is not a fix**; partial/new would keep self-authenticating stale `CURRENT_GRANTED` historical records. `restore_joined_checkpoint` L686's external pin authenticates past bytes only, not present permissions.

**Proposed existing-owner signature and processing contract (not implemented):**

```python
def resume_joined_workloads(
    *, workloads, source_factory, host: str, purpose: str,
    checkpoint, expected_checkpoint_ref: str,
    current_resolver: CurrentDecisionResolver,  # REQUIRED; competent independent issuer
    allow_test_only: bool = False,
    expected_waves_by_decision=None,  # when original35 scope binds exact expected wave
) -> JoinedWorkloadResumeResult: ...

def restore_completed_unit_currently(
    *, workload, checkpoint_entry, exact_expected_pin,
    current_resolver: CurrentDecisionResolver, host, purpose,
    trusted_storage_root, expected_wave=None
): ...  # verify current grant BEFORE restoring/serving protected native payload
```

1. **Independent issuer provenance:** `current_resolver` must be acquired from the competent **live issuer/authority service** independently of `item.record`, checkpoint materials, restored fact, caller-updated metadata or cache. The existing `CurrentDecisionResolver` is a structural Protocol, so passing another adapter that merely returns `item.record` is **not sufficient**. The owner must define/enforce a trusted resolver provisioning boundary (including host/purpose/issuer provenance and genuinely current decision lookup or signed authority-root verification). Absent unavailable/invalid trusted resolver → **HOLD/REFUSE before source-open or protected payload materialization**. No new parallel science authority.
2. **Universal admission BEFORE branching:** for **each** `item`, call existing `admit(item.workload, trusted_current_resolver, host=host, purpose=purpose, allow_test_only=..., expected_wave=...)` before any `_completed_entry_view`, `_restore_output_material`, `source_factory`, optional spill access, derived cache or first-consumer exposure. Verify exact decision ref, source SHA, original-wave identity, native universes, scientific/source permissions, full envelope SHA, prospective U/E_pre roots and expected job multiset against the **fresh** `IssuedWorkloadRecord`; independently match checkpoint entry's source/envelope/unit manifest/receipts to that admitted envelope. Never use `item.record.scope` to set returned authority; use freshly admitted scope only.
3. **All three branches** share the same trusted resolver, not one resolver per checkpoint state. **COMPLETED:** verify current grant, then integrity/semantic replay of full cached fact+receipt, then serve only permitted material. **PARTIAL:** current grant *before* restoring prior outputs and opening source; prior receipts may be adopted only under exact valid native/issuer/operation match, then run with the **same trusted resolver** and check again per actual unit and before output publication. **ABSENT:** current grant before source factory; execute with the same trusted resolver. Never fall back to `_resolver_for(item)`.
4. **Currentness TOCTOU:** the native `execute_issued_workload` already performs `check_current()` around source/read and units, but this protection is worthless when its resolver just returns frozen `item.record`. Keep independently fresh checks before source-open, per unit, after computation and **immediately before any serve/commit**. If issuer revokes during a long computation, refuse publication of a protected positive; preserve honest partial/held custody without legitimizing stale use. If changed decision changes the immutable admitted envelope, do not silently reuse results under the old operation grant.
5. **Exact result integrity separate from rights:** retained `COMPLETED` native fact, negative, replay, Batch receipt and original checkpoint can be historically valid even when current entitlement is DENIED. Do not rewrite their history or delete scientific lineage merely to refuse their present use; apply authorized payload retention/deletion rules separately. The source factory must not be called on an entitlement failure, and protected result bytes must not be returned.
6. **Negative oracle (one test, three branches):** freeze `item.record.currentness='CURRENT_GRANTED'`, authenticated historical checkpoint/result, and current external issuer `REVOKED`; run with (a) completed entry, (b) partial entry, (c) no entry. Each must fail in **the same named current-admission/first-reader assertion**, with **zero** protected output, zero source_factory invocations, zero native calculation/positive receipt. Repeat wrong host/purpose and issuer identity; a fake resolver wrapping the historical item must be rejected at trusted provisioning boundary. Current positive independent grant must still restore completed native results and resume truly incomplete units.

**The trust boundary is the *whole* joined resume.** Patch the existing `pre553_issued_workload.py` owner once. No new checkpoint authority store, new scheduler or alternate permission issuer.

### D5. Frozen Q86 producer-source binding **before** GT12 source-bearing relation evidence

**R2 D2 verified source seam:** `field_forge_conditional_support.py::_validate_common_closure` L194–270 authenticates internal exact fact/query/risk/replay/provenance references, but **not** their originating source release. `gt12_c_to_d_relation_bridge.py::_source` L41 always constructs a fixed source ref, and `bridge_gt12_c_relation_to_d_evidence` L93 accepts only `ExactConditionalSupportProfile` with no authenticated origin. Frozen expected canary:
- source family/edition `Afrobarometer / R5`, path `Data/Afro Barometer Round 5.sav`, exact source SHA **`c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`**;
- risk `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`, member-set SHA **`0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`**;
- conditioner **Q86B**, target **Q86A**, RAW one-source scope.

**An independently verified source release is required, not a constant put on the output.** Existing `ExactConditionalSupportProfile` lacks a trusted source-release witness; therefore the privileged GT12 bridge's single-parameter API cannot itself prove producer origin. The competent producer/bridge owner must add one **enforced** origin-binding seam, either a qualified privately verified origin parameter/receiver or a versioned native producer→bridge contract (with exact legacy consumer migration). Conceptually:

```python
@dataclass(frozen=True)
class VerifiedJointProducerOrigin:  # proposed private, never caller-self-issued
    source_artifact_ref: ExactRef
    c11_release_ref: ExactRef
    universe_ref: ExactRef
    joint_query_ref: ExactRef
    selected_fact_ref: ExactRef
    replay_ref: ExactRef
    risk_set_ref: ExactRef
    issuer_binding_ref: ExactRef

def bridge_gt12_c_relation_verified(
    *, relation: ExactConditionalSupportProfile,
    joint_fact: EmpiricalFact, joint_query: EmpiricalQuerySpec,
    origin: VerifiedJointProducerOrigin, current_permission
): ...  # actual source→I02/C11→I03 provenance must be independently resolved
```

**Enforced invariants:** derive the origin witness from trusted exact sealed C11 original source/release and native issued result (not `relation.ref`, user-provided metadata, a nonempty provenance list or `_source()`); prove the fact/query/replay/source-release/universe provenance chain and selected fact equality; match `origin.source_artifact_ref.content_hash` to the *fixed* GT2 SHA, risk-set ID/member-set exact identity to the fixed GT2 risk, and Q86 role/conditioner/target to the frozen source-qualified operation. Check present source/use/FF permission before publishing. A wrong original source producing internally valid Q86-like facts and matching copied risk label MUST refuse. Missing origin or a direct legacy `bridge_gt12_c_relation_to_d_evidence(relation)` call cannot publish authority-bearing positive evidence; retain it only as an explicitly non-serving compatibility/test path until migrated. Preserve typed negative transport without falsely attributing the wrong source.

**First consumer and falsifier:** real selected native I03 F4 joint `EmpiricalFact` → exact Q86 `produce_exact_conditional_support_profile` → source-verified GT12 C→D evidence/receipt. A changed Q86 original value must change/refuse the *same* reader; swap the entire internally consistent fact/query/release for a second source while retaining Q86 roles and risk ref must fail at source-origin admission **before** the frozen source is stamped. The Q86 path is a **bounded canary**, *not* general source-neutral FF1 importer, S06 scientific coverage or authorized structural/causal relation. Keep generic S04→S06 ingress OPEN.

### D6. Canonical path-containment contract, shared by persist and reopen

**R2 D3 verified code path:** `SourceReleaseManifest.__post_init__` L99–113 only requires nonempty `release_id` and rejects fuzzy selection tokens; it does not apply path containment. `ParquetC11Carrier.release_dir` L209 constructs `root / "releases" / source_sha / release_id / semantic_hash` and `persist` L249 calls it *before any selector validation*. Absolute release IDs override the prefix in `pathlib`; `../` and separators can escape the carrier root. In contrast `reopen` L279–285 rejects separators. This is a **static vulnerable write-path possibility**, not an executed exploit.

The existing W03 owner must define **one shared release-selector validator and contained-path builder**, used in writer `release_dir` **before any filesystem inspection, mkdir, staging, symlink traversal, or source-derived write**, and in `reopen`. Deny absolute/relative escapes, dot/dotdot path components, slash/backslash and Windows drive/UNC encodings (plus invalid/control names). If any historical legitimate ID cannot be used as one safe filesystem component, use an explicitly accepted reversible physical encoding while retaining immutable *logical* release ID and backwards-compatible read migration; do not silently rewrite C11 identity. Resolve/anchor to a trusted canonical root, reject symlinks in source-derived parent/member paths, use handle-based no-follow or equivalent safe directory primitives as the supported OS allows, and reverify at atomic publication to close path TOCTOU. A `Path.resolve()` check alone is not a race-proof promise. Fail closed on path escape with **zero writes outside the carrier root**. Apply the same boundary to staging, manifest member names and orphan adoption; no fallback to user-supplied arbitrary paths. Do not modify W03 code from this architecture branch.

## E. Lossless semantic invariants that cannot be optimized away

1. **Same-person**: one respondent in one source-scoped universe; no cross-wave identity stitching or multiplication of marginals. Repeat events retain native source cell, occurrence, component, multiplicity, ranking and order.
2. **Risk and denominator**: `_routing_fact_for` (`_pre553_query_eval.py` L51) errors if missing; `_risk_membership` L88 errors on unresolved state rather than converting it to nonmembership. Query-conditioned denominator is distinct from full eligible risk membership.
3. **Value**: physical raw token/state ≠ authorized canonical value; no label-based mapping; typed absent/unknown/inapplicable are distinct. Do not collapse a multi-response question into one scalar unless governed.
4. **Full domain**: `_parse_target_plan` (`_pre553_query_common.py` L315–391) constructs the declared joint domain and its identity. Observed zero under complete qualification is not routing NOT_APPLICABLE, ZERO_SUPPORT, UNRESOLVED, VALID_EMPTY or unsupported topology.
5. **Measure**: `GOVERNED_WEIGHTED` uses exact `Fraction` (`_pre553_query_eval.py` L626–821). SQL float sums never become the estimator; exact weight identity group contributions may be reduced by native rational arithmetic only after equivalence.
6. **Proof**: `EmpiricalFact` includes exact used objects/authorities, risk/denominator membership, cells, source/replay and specific negative states. Retained native object may be served after fresh entitlement; summary is not a fact replacement.
7. **Discovery**: complete frozen frontier/candidate ancestry, reversal/minority/contrary tests and partial/held fates. A faster subset is not an undisclosed complete I05 search.
8. **Scope**: independent surveys remain source-indexed unless separately authorized composition; F5 empirical associations are not causal assertions.

## F. Admission/consumer negotiation and decisive falsifiers

| Claim to prove | Initial positive | Claim-specific RED |
|---|---|---|
| Single prepared source | Normal `execute_issued_workload` with a discovery emits byte/exact-equivalent Route B, Batch I03/I05 receipts and calls one underlying C11 build | Spy on actual builder; deleting prepared-context edge reintroduces two builds **and** fails named integration assertion |
| Saved read is legitimate | Fresh-process exact pinned release selected with an independently accepted I02 provenance, native I03/I05 values and negative parity | Corrupt one nonrequested member or change exact root; admission must refuse under selected whole-release integrity law, not issue unauthenticated handle |
| Physical plan semantics | Selected RAW scalar, conditioned and event-topology hostiles match full native `EmpiricalFact`/replay | Missing routing for a respondent excluded by predicate must refuse rather than SQL-filter it away |
| All-branch joined-resume currentness | Completed historic result and partial/absent resume pass a genuinely independent live issuer; only completed skips source | External issuer REVOKED but historical item says CURRENT_GRANTED: COMPLETED, PARTIAL and ABSENT must all refuse before protected output/source-open; a resolver returning item.record is rejected |
| GT12 bounded FF first reader | Source-verified Afrobarometer R5/Q86 selected fact changes the actual GT12 canary count/bridge and current permission succeeds | Internally valid **different-source** fact/query with copied risk+Q86 roles MUST be refused before frozen `_source()` attribution; missing source witness or severed I03 fact binding makes same reader RED |

**Unresolved ABI/implementation decisions (not permission requests):** accepted I02 reopen certificate and selective segment-root law; stable streaming canonical hash over exact sorted rows; whether the saved-session repository protocol can be accepted without violating current exact sealed-index attestation; how the existing native replay identity embeds full domain material at very high arity. Owner decisions belong to C11/I02/I03, not a new architecture executive. The original implementation and native scientific proofs remain for later independent courts.
