# WSC000E — WHOLE-SPINE BUILD HANDOFF FROM CHETIRI / PRE-V3 R1

This file translates the recovered N010/N011/N012 inheritance into constraints for the later whole-spine builder. It is **not** an architecture-selection ruling.

## 1. Build invariants that must cross central fan-in

### BHE-01 — Conserve governed semantics, not historical storage shape

The builder must preserve semantic stage identity, producer ownership, information sufficiency, authority, provenance, exact source/release identity, and replay requirements independently of physical packaging.

A persistent carrier, source-backed virtual facade, or hybrid/cache layout may implement the same governed semantic function. Physical co-location or persistence cannot transfer semantic ownership. Conversely, source-backed reconstruction cannot bypass the semantic obligations previously carried by a transformed object.

Current successor law: Authority31 (`daffee545fc60a8cd635aee9aafbe77a920f4c19`) explicitly provides the PRE-V3 producer-ownership / logical-physical-neutrality theorem and does not select a physical winner.

### BHE-02 — Preserve THE PAST / THE LEARNED WORLD / THE LIFE

The whole spine must retain distinct authority domains:

1. **THE PAST** — exact empirical source/release evidence and source semantics.
2. **THE LEARNED WORLD** — governed empirical-social inference, structural products, learned releases/services, publication/replay, and bounded caches.
3. **THE LIFE** — V3 actor-specific generated/developmental realization.

No optimization, source-backed facade, structural repository, possibility service, or peer-prior mechanism may cause a learned-world product to become V3-owned life before the V3 boundary.

The following noncollapse must remain true in data model, API permissions, validation, and tests:

`SOURCE INCIDENCE != DISCOVERED CANDIDATE != VALIDATED EMPIRICAL RELATION != POSITIONED-SUBJECT POSSIBILITY FIELD != STRUCTURAL PRIOR != V3 ACTOR STATE != ACTOR BELIEF/RESPONSE`

### BHE-03 — Reconstructibility requires a proof surface; it is not permission to delete

Before a transformed carrier or cache is made disposable, the build must establish at the affected semantic grain:

- exact authoritative source/release identity;
- a content-addressed lossless source capsule **or** formally proven information-equivalent source projection;
- explicit source-universe membership and linkage/pooling/backfill authority;
- exact deterministic derivation/reconstruction code/version identity;
- preserved authority roots and determinant/version bindings;
- semantic-equivalence proof against the omitted carrier/service contract;
- replay/read-path/routing receipts as required by consumers;
- complete reference closure for every governed consumer;
- preservation of typed absence/noncomparability/not-asked/missing semantics;
- preservation of empirical sufficiency fields required by existing/future lawful workloads.

If any required element is absent, carrier retirement must fail closed. `OBL029` remains the competent unresolved carrier-equivalence/retirement return.

### BHE-04 — Cache status never implies semantic ownership

A normalized respondent substrate, CED-like interface, source-backed C11 facade, persistent database table, Parquet carrier, in-process object, publication repository, or other physical service layer may be useful or necessary for a workload. None becomes semantic authority merely because it is the fastest, most persistent, easiest to query, or currently consumed.

Derived caches can be regenerated only behind BHE-03. Removing a cache may change performance; it must not silently change the semantic invalidation set.

### BHE-05 — Exact identity beats lexical resemblance

Identity resolution and currentness surfaces must reject semantic repair by:

- string similarity;
- shared field/value labels;
- `latest`, `default`, wildcard, nearest, or fuzzy selectors;
- geography alone;
- prevalence/correlation/signature similarity;
- structural labels without an exact governed mapping;
- adjacency of releases or objects.

If the exact mapping/currentness/source-universe authority is absent, the result is typed defer/deny/fail-closed, not guessed binding.

### BHE-06 — Population evidence cannot become actor first-person truth

The builder must enforce these negative edges:

- population prevalence → actor membership: **forbidden**;
- conditional population distribution → actor belief probability: **forbidden**;
- empirical field/value string → generated-position binding: **forbidden without exact mapping authority**;
- empirical possibility/proxy → exact actor fact: **forbidden**;
- empirical possibility/proxy → actor belief/response/psyche: **forbidden**;
- structural peer eligibility → V3 state mutation: **forbidden**;
- structural context → first-person expression: **forbidden without actor-safe claim authority**.

This is not merely a modeling preference. It is the inherited learned-world/life jurisdiction boundary and the current expression/identity firewall.

### BHE-07 — Preserve exact M4 → M5 → M6 ownership and permission boundaries

At the commissioned PRE-MAIN head, reusable current seams already embody the surviving guard:

- **M4** owns V557/V558 publication/repository exact resolution and immutable current context. Logical V557 and V558 remain distinct even if implemented in one process. M4 does not admit actor/V3 semantic classes into structural publication ownership.
- **M5** consumes/replays exact M4 resolution and may produce structural peer/RSC eligibility under exact currentness. M5 has no authority to mutate actor state or synthesize empirical probability into actor belief.
- **M6** is the actor-accessible semantic ceiling / V2 ingress firewall. Positive expression authority comes only through a current verified actor-safe claim entry inside its current verified envelope. M5/RSC, raw structural objects, empirical negatives, PSEPF material, and replay/audit objects are not direct positive expression authority.

There must be no direct positive semantic edge `M5 -> M6` that bypasses actor-safe claim authorization.

### BHE-08 — A/B/C remains unresolved

The builder must carry all three physical candidate families as architecturally possible until a competent court decides otherwise:

- **A** — persistent canonical event/carrier design;
- **B** — source-backed virtual logical service;
- **C** — source-backed hybrid with regenerable accelerators/caches.

Neither historical D15 persistence nor Chetiri source-backed feasibility selects the winner.

The selection gate is `OBL037` returning into `OBL001`, under competent VOZHD/HQ architecture-selection authority, using **equal governed workloads** and only after prerequisite carrier/source/replay/lifecycle evidence is sufficient.

### BHE-09 — Current consumer absence is not a deletion criterion

The statement “current V3 does not read this object” is insufficient for disposal. Legitimate consumers include:

- compiler/discovery;
- learned-world inference services;
- structural production;
- DDM/analytics;
- audit/replay;
- historical release verification;
- future lawful V3 inputs;
- architecture-comparison workloads.

Deletion/reference-closure analysis must therefore be whole-consumer, not current-V3-only.

### BHE-10 — Recompilation must follow exact determinants and dependency closure

When a source/release/determinant changes, recomputation must be bounded by the exact changed determinant scope plus transitive dependency closure under current producer ownership. Physical monolith shape must not broaden semantic invalidation. Historical accepted learned/structural releases and realized V3 life are immutable historical objects; new recompilation produces new governed successors rather than rewriting historical identity.

## 2. Existing executable assets to reuse, adapt, and test

All refs below are pinned to the commissioned working head `5bfcb9ddfc30a9f0958e675a5af6c611978284bf`. Existence of an asset is **implementation capital**, not architecture-selection authority.

| Asset | Blob SHA | Reusable function | Test capital | Build disposition |
|---|---|---|---|---|
| `rawlsing_next/pre553_source_backed_c11_facade.py` | `fe4147853f9a42bd36dc2b5017ed05d7bc9ebf1b` | Source-backed logical C11 serviceability/facade | `rawlsing_next/tests/test_pre553_source_backed_c11_facade.py` (`aaa38306558bc9ad0a87c959d777d3f3d87c8395`) | Reuse behind source/equivalence/replay authority; do not infer B/C victory. |
| `rawlsing_next/pre553_source_equivalence.py` | `0e7f9f6d77ef6efe2c66b04f0527bb1ab99f4ef8` | Source/carrier semantic-equivalence machinery | `rawlsing_next/tests/test_pre553_source_equivalence.py` (`8a72cbbbf9b5be7b14f66df611410957e848608d`) | Reuse as OBL029 proof machinery; local pass is not carrier-retirement authority. |
| `rawlsing_next/pre553_replay_audit.py` | `86e0b9c518633735f2527b89fb72fca1a40dc2cc` | Deterministic replay/audit integrity | `rawlsing_next/tests/test_pre553_replay_audit.py` (`4030999bf4a206f487b826c3781a072230e375be`) | Reuse across A/B/C; representation-neutral requirement. |
| `rawlsing_next/pre553_discovery_exact.py` | `b2b99460cc5991bc26aa2ffe5bda129b408fc197` | Authority-before-search deterministic exact discovery, full frontier/evaluate-all invariants | `rawlsing_next/tests/test_pre553_discovery_exact.py` (`308a582c012f20824bc2dceb530b1c9652395f93`); `test_pre553_query_frontier_hostile.py` (`d18f1411e9a3c6f6126e38dd0e3ea2fb4694691e`) | Reuse exact bounded core; OBL030/035 production authority remains open. |
| `rawlsing_next/source_backed_positioned_subject_possibility.py` | `62e5eced47b64512f47b004e3e13a6ef3fe21de7` | Source-backed learned-world positioned-subject possibility; explicit exact/proxy lane; deterministic provenance/replay | `rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py` (`c48342fc5b9d7ae6701b5399c656d3c300cc407a`) | Reuse with epistemic ceiling `PROXY != EXACT FACT != ACTOR BELIEF`; never persist as actor life. |
| `rawlsing_next/m4_v557_v558_publication_repository.py` | `9005308fb06686b593783666e77d06619645b2bb` | Immutable publication/repository boundary and exact current resolution | `rawlsing_next/tests/test_m4_v557_v558_publication_repository.py` (`f29a06ba2d3e43786a5562cae86a356721c6b922`) | Reuse as learned-world publication/structural repository seam. |
| `rawlsing_next/m5_runtime_rsc_peer_prior.py` | `18735bdb31a220aed032aa722574d685e2bdddf5` | Currentness-bound structural peer/RSC eligibility without actor mutation authority | `rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py` (`ef4faaa84b24b9b6ca62ae7eaa29018d57439c0c`) | Reuse; preserve negative mutation/psyche boundary. |
| `rawlsing_next/m6_actor_safe_expression.py` | `74d9701cdc7dabccf61eb5089498db290c1efd9c` | Actor-safe positive expression ingress firewall / semantic ceiling | `rawlsing_next/tests/test_m6_actor_safe_expression.py` (`a8e5b466a118413104783728aac3733416893993`) | Reuse as V3→V2 authority boundary; no upstream learned-world shortcut. |
| `rawlsing_next/render_bounded_expression.py` | `eef88095d1d647b5332aa5186a3a5df218fcf9f8` | Bounded downstream expression rendering | `rawlsing_next/tests/test_render_bounded_expression.py` (`80bdec5d9dc66603c1bc0fcbdf7506a56b2b0f35`) | Reuse downstream of M6; renderer may not repair missing semantic authority. |
| Whole-machine integration capital | n/a | End-to-end seam tests | `rawlsing_next/tests/test_whole_machine_integration.py` (`e5fb1c4f5cc1979bbd0bbc38b48a2f03d318f72d`) | Extend rather than replace when composing final spine. |

Adjacent current physical-carrier implementations (`pre553_c11_repository.py`, `pre553_c11_ingest.py`, `pre553_physical_c11_bridge.py`, `pre553_physical_decoder.py`, `pre553_parquet_carrier.py`, `pre553_duckdb_direct.py`) are implementation evidence/capital. Their existence does not re-establish a universal persistent-carrier law and does not defeat the source-backed/hybrid candidates.

## 3. Required validation matrix for the whole-spine builder

The final composed build should include explicit tests at these seams. These are inheritance-derived acceptance requirements, not a claim that all are currently closed.

| Test ID | Required test | Failure that must be caught |
|---|---|---|
| CHT-V01 | Run persistent and source-backed/hybrid implementations over the **same governed semantic workload** and compare exact outputs/authority/provenance/replay at the contract grain. | Declaring equivalence from row counts, local smoke tests, or different workloads. |
| CHT-V02 | Remove a regenerable cache and rebuild solely through the declared exact source/equivalence/replay path. | Cache contains hidden semantic authority or missing source information. |
| CHT-V03 | Attempt carrier retirement with one unresolved reference consumer. | Deletion proceeds without reference closure. |
| CHT-V04 | Attempt reconstruction from raw source bytes lacking governed source-universe/release/semantic authority. | “Raw bytes exist” is treated as complete semantic authority. |
| CHT-V05 | Mutate one exact determinant and verify only its transitive semantic dependency closure is recomputed. | Physical monolith shape broadens invalidation or historical releases are rewritten. |
| CHT-V06 | Replay historical learned/structural release and historical V3 life after a current source/cache change. | Recompilation mutates immutable historical identity/life. |
| CHT-V07 | Query exact ID/currentness with `latest`, `default`, wildcard, nearest, fuzzy, or string-similar substitute. | Mutable/fuzzy selector is accepted as semantic authority. |
| CHT-V08 | Present an empirical source-universe mismatch without an explicit governed bridge. | Source universes are silently pooled or mapped. |
| CHT-V09 | Present a broader proxy positioned-subject slice where exact conditions are unavailable. | Proxy loses its explicit authority/specificity-loss markers or becomes exact fact. |
| CHT-V10 | Feed population prevalence/conditional evidence into actor belief/membership/response logic. | Population evidence becomes actor psyche or first-person truth. |
| CHT-V11 | Feed RSC/structural peer eligibility into V3 mutation. | M5 context silently becomes actor state/disposition/action authority. |
| CHT-V12 | Feed M5/RSC/PSEPF/raw structural/replay material directly into M6 positive expression. | Upstream learned-world material becomes first-person expression without actor-safe claim authorization. |
| CHT-V13 | Verify M4 V557 and V558 logical identities remain separate even when physically co-located/in-process. | Physical packaging collapses semantic producer ownership. |
| CHT-V14 | Verify source-backed facade/cache and persistent repository return identical typed absence/not-asked/missing/support/weight/time/geography semantics where the governed contract requires them. | “Equivalent” implementation silently drops negative/absence semantics. |
| CHT-V15 | Verify no local implementation/test pass sets `architecture_selected=true` or closes OBL001/OBL037. | Evidence branch self-promotes into architecture verdict. |

## 4. Open returns that gate architecture or full compiler closure

Central fan-in must preserve these as open rather than converting them into implementation TODOs with assumed answers:

### OBL024 — source-backed role in final architecture

Capability exists. Its final role remains unresolved and returns to the physical architecture court. A working source-backed facade is evidence, not selection.

### OBL029 — carrier equivalence / retirement

Must establish exact production equivalence/retirement authority before discarding a carrier because “it is reconstructible.” This is the primary anti-disposability gate.

### OBL030 — production discovery authority/execution/validation

The exact deterministic discovery core is reusable, but production search still needs its exact authority, source facade, grammar/frontier and validation conditions. Prototype/bounded discovery is not governed production closure.

### OBL033 — source composition/linkage/backfill + carrier-neutral replay/completeness

No silent pooling of source universes. Composition requires explicit governed linkage, pooling/backfill rules and replay/completeness evidence.

### OBL034 — learned-product lifecycle and economics

Publication, supersession, withdrawal, retention, replay and economics must have explicit learned-world ownership. Storage implementation and prototype cost do not provide that authority.

### OBL035 — C05R2B production I05

Still return-required and depends on production discovery/source authority. Complete only if the selected final architecture requires that production path.

### OBL036 — C08 final reconciliation

Still return-required. Historical C08 was explicitly pre-reconciliation evidence with `final_reconciliation=false` and `architecture_selected=false`.

### OBL037 / OBL001 — equal-governed-workload physical architecture selection

This is the competent A/B/C selection surface. It cannot be replaced by historical D15, by current persistent code, by source-backed feasibility, or by one benchmark. It should run only after prerequisite carrier/source/replay/lifecycle/Chetiri evidence is ready.

### OBL004 — complete source→PRE-V3 compiler composition

Current components and local tests do not establish full vertical composition. The end-to-end proof must be composed after source/replay/lifecycle/reconciliation interfaces are explicit.

## 5. Anti-resurrection constraints for the builder

- **AR09:** never treat PostgreSQL (or any backend) as canonical empirical truth.
- **AR10:** never infer semantic ownership from persistent DB storage/co-location.
- **AR16:** never resurrect historical D15 persistence as universal current physical law.
- Historical N010/N011/N012 mechanisms are preserved as constraints/evidence unless current authority explicitly adopts them. Their campaign status remains historical/nonruntime.
- Authority31 may be used for current PRE-V3 producer ownership and logical/physical neutrality at its recorded grain; it still does not authorize a physical winner.

## 6. Minimum whole-spine interface contract derived from WSC000E

A later source→PRE-V3→V3→V2 composition should expose, at minimum, enough explicit metadata/typed state to enforce the following interfaces:

### Source evidence interface

Must carry exact source/release/universe identity, source semantic/codebook/version authority, provenance/hash identity, typed absence/missing/not-asked routing, and lawful weight/time/geography fields where required.

### Learned-product interface

Must carry producer identity, exact upstream semantic references, release/currentness identity, authority ceiling, source-universe/comparability state, determinant/version bindings, lifecycle state, and replay reconstruction identity. A cache locator may be present but may not substitute for producer/authority identity.

### Positioned-subject possibility interface

Must distinguish exact from proxy results; record conditioning/source-universe identity, comparability authority, specificity/authority loss for proxy results, provenance/replay, and an explicit epistemic ceiling prohibiting conversion to actor belief/fact.

### Structural-to-V3 interface

Must distinguish structural eligibility/context from mutation permission. RSC/peer priors may inform a permitted context surface but cannot themselves write V3 actor state.

### V3-to-V2 expression interface

Must require exact current actor-safe claim authority. Learned-world objects, PSEPF, structural priors, empirical negatives, replay/audit records, and raw structural evidence are non-positive ingress unless separately transformed/admitted by the proper producer/authority seam.

### Replay/retirement interface

Must make source-equivalence, reference-closure, reconstruction/replay identity and authority roots inspectable so physical storage decisions can be tested without changing semantic truth.

## 7. Central fan-in disposition

WSC000E returns the following compact doctrine to the whole-spine integrator:

> **Keep the information, authority, identity, jurisdiction, and replay law; do not fossilize the historical physical implementation.** Source-backed reconstruction is lawful only when it proves the obligations carried by the omitted carrier. Persistent storage is lawful but does not own the semantics. The learned world may characterize possibilities and structural context, but it may not manufacture actor life or first-person truth. The persistent/source-backed/hybrid question remains open until an equal-governed-workload competent architecture court resolves it.

`PASS__WSC000E_CHETIRI_PREV3_INHERITANCE_RECOVERED__READY_FOR_CENTRAL_FANIN`
