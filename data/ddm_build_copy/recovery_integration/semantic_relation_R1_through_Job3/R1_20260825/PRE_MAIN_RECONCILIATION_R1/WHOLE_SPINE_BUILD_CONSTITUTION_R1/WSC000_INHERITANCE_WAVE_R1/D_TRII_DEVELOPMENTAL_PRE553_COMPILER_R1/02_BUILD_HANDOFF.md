# WSC000D — Build Handoff to Whole-Spine Central Fan-In

## What this lane contributes

This handoff does **not** propose a new architecture. It provides the inherited Trii developmental / PRE553 / learned-world / vertical-compiler constraints that the central whole-spine design must either preserve directly or explicitly supersede at a competent grain.

The key distinction is:

> The project already possesses a strong logical-function graph and a large body of executable compiler/seam/replay assets, while the parent end-to-end composition, publication topology, source-composition, PSEPF-production, and lifecycle/economics decisions remain open.

Central design should therefore reuse the machine's accumulated work instead of treating PRE553→PRE-V3 as a blank slate, but it must not convert the existence of that work into false closure.

## A. Mandatory whole-spine constraints

### A1. Preserve semantic earliest-owner boundaries independent of packaging

Current Authority31 governs this point directly:

- exact upstream semantic objects should be reused rather than re-authored downstream;
- a new producer owns only genuinely new semantic meaning;
- physical publication/co-location does not transfer semantic ownership;
- logical stage identity and information sufficiency survive independently of physical packaging;
- no persistent/virtual/source-backed/hybrid physical winner follows from this theorem.

The historical R03 V553–V558 DAG is therefore useful as an inherited **function map**, not as an immutable deployment diagram.

### A2. Keep PRE553 publication topology as an explicit unresolved decision

`OBL002` remains `RETURN_REQUIRED`.

Central fan-in may express requirements common to either candidate topology—producer identity, exact reference closure, replay, permissions, typed negative states, deterministic resolution—but must not silently decide `staged seam` versus `continuous producer DAG` from file layout, module names, or historical stage sequencing.

A future topology court must preserve information equivalence and producer ownership.

### A3. Do not declare source→PRE-V3 compiler closure by component arithmetic

`OBL004` remains `RETURN_REQUIRED` even though there are exact-base implementations and tests for many component stages.

Closure requires one explicit composed source→PRE-V3 proof demonstrating, for the exact intended production workload:

1. source identity and carrier/reconstruction sufficiency;
2. exact query/discovery authority;
3. operation-scoped source relation/composition authority;
4. measurement/comparability premises where required;
5. structural-admission authority at exact use;
6. preservation of producer identities and typed negative states through transformation;
7. replay and determinant closure;
8. publication/use permission and deterministic context resolution;
9. no actor-state leakage before V3;
10. fail-closed behavior for missing/mismatched/unknown authority.

The existing `test_whole_machine_integration.py` and `test_pre553_whole_machine_hostile_acceptance.py` are reusable starting points, not substitutes for this parent proof.

### A4. Keep the PSEPF lane separate from the structural learned-world lane

The lawful conceptual split is:

```text
structural learned-world lane
source / empirical evidence
    -> separately governed structural admission
    -> V553/V554/V555/V556 producer objects as required
    -> V557 publication governance
    -> V558 repository/resolution
    -> ResolvedStructuralContext
    -> V3

positioned-subject empirical-possibility lane
lawful V3-owned objective actor fact refs
    -> predicate ancestry / ActorComparabilityService
    -> exact governed empirical possibility query
    -> source-indexed PSEPF
    -> thin V3 intake/metabolism boundary
    -> V3 developmental owner
```

PSEPF is not a V553–V558 structural object and must not become actor belief, orientation, position, memory, biography, persona, or response.

`OBL031` and `OBL032` remain real gates. Any whole-spine design that elides the comparator or metabolism boundary recreates the statistical-puppet failure that the Trii lineage explicitly rejected.

### A5. Preserve source plurality; composition is none-by-default

Current P3 law is binding and more current than historical source-equivalence intuition.

Central compilation may not treat any of the following as interchangeable:

- semantic relation;
- respondent linkage;
- sample overlap control;
- source pooling/composition;
- measurement portability;
- common labels/scales/estimands;
- provenance reachability.

`OBL033` and `OBL012` remain open exactly because positive operation-specific authority is not universal.

### A6. Preserve learned-world replay as proof material

A complete learned object/service needs sufficient immutable information to explain and replay what was produced, not merely enough data to regenerate some equivalent-looking output.

Carry forward as applicable:

- release identity;
- scenario/execution identity;
- exact source content refs;
- exact authority id/version/hash tuples;
- routing/read-path receipts;
- subtree/output evidence receipts;
- determinant/version bindings;
- governing roots;
- build/reconstruction instructions;
- typed negative/noncomparable/valid-empty states;
- exact historical interpretation under the authority active for that replay.

`rawlsing_next/pre553_replay_audit.py` is a high-value reusable inspectorate for these invariants.

### A7. Preserve V557/V558 logical distinction and permission monotonicity

Central architecture may fuse V557/V558 physically if desired later, but must preserve:

- producer-owned semantic identity;
- V557 publication/use admission;
- permission narrowing;
- V558 immutable repository/index/resolution;
- deterministic exact lookup;
- prohibition on repository-presence-as-permission;
- no latest/default/fuzzy repair.

`rawlsing_next/m4_v557_v558_publication_repository.py` is strong reusable implementation capital at this function grain.

### A8. Preserve terminal discovery as a service even when no generic runtime consumer exists

`DiscoveryResultReceipt` is not structural truth, but it remains useful for bounded discovery, authoring, subsequent exact query formation, audit/replay, and separately governed structural admission.

Do not retire discovery merely to simplify the runtime diagram. Conversely, do not let discovery self-authorize downstream semantics.

## B. Existing assets central build should try to reuse first

### B1. Logical structural producer / publication stack

- `rawlsing_next/m1_temporal_v554_admission_dedup.py`
- `rawlsing_next/m2_v555_atomic_route.py`
- `rawlsing_next/m3_v556_higher_order_structural.py`
- `rawlsing_next/m4_v557_v558_publication_repository.py`

Reuse/adapt these before writing replacements. Their exact interfaces may need central recomposition, but their ownership, identity, deduplication, permission, and failure-state machinery directly encode inherited constraints.

### B2. PRE553 exact empirical/query/authority machinery

- `_pre553_query_common.py`
- `_pre553_query_eval.py`
- `_pre553_query_predicate.py`
- `pre553_empirical_objects.py`
- `pre553_empirical_authority.py`
- `pre553_empirical_query.py`
- `pre553_discovery_exact.py`
- `pre553_discovery_adaptive.py`
- `pre553_structural_admission.py`
- `pre553_source_relations.py`
- `pre553_source_equivalence.py`

These should be evaluated function-by-function against current P3/Authority31 law rather than accepted or discarded wholesale.

### B3. C11/source-backed/replay capital

- `pre553_c11_ingest.py`
- `pre553_c11_integrity.py`
- `pre553_c11_repository.py`
- `pre553_source_backed_c11_facade.py`
- `pre553_recursive_handoff.py`
- `pre553_replay_audit.py`
- `pre553_component_authority_vector.py`

Preserve logical C11 exact serviceability regardless of eventual physical choice.

### B4. PSEPF capital

- `source_backed_positioned_subject_possibility.py`
- `v3_psepf_zero_positive_guard.py`

These are particularly valuable for preserving the empirical-possibility versus actor-truth firewall. They do not, by themselves, close OBL031/OBL032.

### B5. Physical/carrier helpers

- `pre553_parquet_carrier.py`
- `pre553_duckdb_direct.py`
- `pre553_physical_decoder.py`
- `pre553_physical_c11_bridge.py`
- `pre553_r4_compaction.py`

Treat these as **adaptable candidate implementations**, never as authority for the unresolved physical winner or source retirement.

### B6. Tests

The existing `rawlsing_next/tests/` tree should be harvested aggressively. It already contains dedicated tests for M1–M6, whole-machine integration/hostile acceptance, PRE553 queries, source relations/equivalence, replay, C11, PSEPF, structural admission, authority, and discovery.

Central build should add tests only for genuinely uncovered composition seams or newly selected interfaces.

## C. Return-required production work central design must leave visible

### C1. `OBL002` — PRE553 seam versus continuous producer DAG

Status: `RETURN_REQUIRED`.

Do not settle during inheritance fan-in unless a competent later current authority already exists at exactly this topology grain. None was found.

### C2. `OBL003` — learned-world functional coverage

Status: `RETURN_REQUIRED`.

Required closure artifact: explicit finite inventory of functions classified as current owner, successor-owned, competently retired, or still missing.

### C3. `OBL004` — complete source→PRE-V3 compiler

Status: `RETURN_REQUIRED`.

Required closure artifact: explicit end-to-end composed proof. Local tests and local stage PASS results are insufficient.

### C4. `OBL012` — measurement portability where required

Status: `RETURN_REQUIRED`.

Current P3 law proves the absence of a universal owner. The compiler must fail closed at any operation that needs portability without exact positive authority.

### C5. `OBL029` — source→carrier equivalence / source retirement

Status: `OPEN`.

Reconstructibility does not authorize source retirement.

### C6. `OBL030` — production discovery authority / execution / validation

Status: `OPEN`.

Prototype/executable discovery machinery does not self-authorize production discovery.

### C7. `OBL031` — predicate ancestry / actor comparator

Status: `OPEN`.

Must close before production PSEPF.

### C8. `OBL032` — production PSEPF transition/metabolism

Status: `OPEN` with strong return required.

Must consume lawful joint/comparator evidence and preserve the actor-opacity ceiling.

### C9. `OBL033` — source composition/linkage/backfill and carrier-neutral replay/completeness

Status: `OPEN`.

This is a major direct blocker of OBL004 and prerequisite of a competent OBL002 topology choice.

### C10. `OBL034` — learned-product lifecycle/economics

Status: `OPEN`.

Do not let prototype performance or storage cost select architecture in the absence of governed workload/lifecycle economics.

### C11. `OBL035` / `OBL036` — Chetiri production I05 and final reconciliation

Status: `RETURN_REQUIRED`.

These remain dependencies of final architecture/compiler closure if the selected path requires the corresponding source-backed capability.

## D. Explicit no-decisions inherited into fan-in

Central WSC000 fan-in must preserve these as unresolved unless another authorized worker produces exact later authority at the appropriate grain:

1. staged PRE553 publication seam versus continuous producer DAG;
2. persistent versus source-backed/virtual versus hybrid physical architecture;
3. source retirement;
4. universal source composition/pooling;
5. universal measurement portability;
6. learned-product lifecycle/economic policy;
7. V3 empirical-possibility metabolism algorithm;
8. retirement of terminal discovery or learned-world services solely because a current generic runtime consumer is absent.

## E. Suggested central ownership placement

This is a functional placement recommendation, not a topology selection.

| Inherited function | Whole-spine placement |
|---|---|
| exact empirical query/discovery | empirical/source compiler service before structural admission |
| structural empirical admission | empirical→structural authority seam |
| V553 temporal/comparability meaning | conditional PRE-V3 producer function |
| V554 affordance/applicability | PRE-V3 structural producer function |
| V555 atomic mediation route | PRE-V3 structural producer function |
| V556 higher-order topology | conditional PRE-V3 structural producer function |
| V557 publication/use governance | PRE-V3 publication permission function |
| V558 repository/resolution | PRE-V3 learned-world repository/resolver function |
| source composition / replay | cross-cutting source/compiler service with explicit authority |
| ActorComparabilityService / PSEPF | separate empirical-possibility side lane into V3 |
| V3 metabolism / actor realization | V3 developmental owner, never PRE-V3 learned world |

Physical co-execution, storage, and process boundaries remain intentionally unspecified.

## F. Fan-in acceptance criterion for this lane

Central fan-in has correctly inherited WSC000D only if its resulting whole-spine design:

- preserves current Authority31 producer ownership and physical-neutrality law;
- preserves current P3 source/composability/measurement ceilings;
- keeps the PSEPF-to-V3 lane distinct from structural learned-world publication;
- retains exact replay/provenance/negative-state obligations;
- explicitly carries OBL002/003/004/031/032/033/034 and relevant dependencies rather than hiding them;
- inventories and reuses/adapts existing `rawlsing_next` compiler/seam/test assets where functionally equivalent;
- and does not call the vertical compiler closed until an end-to-end proof exists.

`PASS__WSC000D_TRII_DEVELOPMENTAL_PRE553_COMPILER_INHERITANCE_RECOVERED__READY_FOR_CENTRAL_FANIN`
