# SI-R04 — V557→V558 Hostile Seam-Integrity Court

## Court identity

- **Worker:** SI-R04
- **Repository:** `maidiu/rawlsing`
- **Branch:** `agent/vozhd-dva-si-r04-v557-v558`
- **Exact base SHA:** `e5bf198a59b561b4db2f092c115d7a6e5cbf562d`
- **Mode:** independent hostile seam reconstruction; architecture/conformance audit only
- **Production edits:** none
- **Allowed verdicts:** `CONFIRM | HARDEN | REOPEN`
- **Verdict:** **CONFIRM**

## 1. Executive holding

The accepted V557→V558 replacement architecture survives hostile re-audit.

The decisive distinction is between **accepted seam architecture** and **current production implementation**:

1. **Accepted architecture:** `CONFIRM`. It does not lose any distinction the accepted V3 architecture now requires. V557 is correctly bounded as a lossless runtime-authorization/publication stage with no structural-domain reownership. V558 is correctly bounded as an immutable, stage-agnostic `StructuralPriorRepository` linker/index boundary with producer-preserving locators and references, not a replacement producer ontology.
2. **Current production implementation:** **NONCONFORMING / SUPERSEDED / NOT RELEASED**. Completion-grade V557 still projects current V556 material into renderer-oriented `slot_name` rows and governance/blocker surfaces; current V558 still normalizes renderer/readiness/governance state. It does not implement the accepted repository, collection registry, `ObjectLocator`, mixed-producer reference graph, required indexes, or standalone producer-material closure. The thin path is likewise not terminal authority.

This implementation failure does **not** reopen the accepted seam because the binding V557/V558 implementation ruling already explicitly supersedes those current shapes and blocks production implementation pending canonical producer completion and governance authority. `CONFIRM` here therefore means **the accepted replacement seam is sufficient and jurisdictionally correct**, not that current V557/V558 code is ready.

The hard standalone test is satisfied by the accepted contract in architecture: a V558 bundle must contain immutable producer material or content-addressed closure, exact producer IDs/hashes, a collection registry, producer-preserving locators, reference graph, required indexes, item governance, negative authority, and resolver-policy bindings, and must resolve with raw V553–V556 stage directories absent. Current code cannot pass that test and must not be promoted as terminal V558.

**Answer to the court question:**

> Does the accepted V557→V558 seam lose any distinction accepted V3 now needs?

**No.** Every listed V3-critical distinction has an explicit preservation, reference, state, locator/index, or epistemic/permission path in the accepted seam. The live superseded code loses many of them, but the replacement architecture already recognizes and forbids those losses.

---

## 2. Authorities independently reconstructed

The court treated accepted TD-R04 as a hostile hypothesis, not as its proof. The reconstruction was checked against:

- `TERMINAL_DEMAND_ENVELOPE.md`;
- `ARCHITECTURE_PASS_LAW.md`;
- `schematics/synthesis/RUNTIME_PRIOR_RESOLUTION_EXPLORATION.md`;
- accepted `TD_R03_V556/RESULT.md`;
- accepted `TD_R04_V557_V558/RESULT.md`;
- accepted `TD_R05_V3_DEVELOPMENTAL_RUNTIME/RESULT.md`;
- `integration/V556_COMPLETION_IMPLEMENTATION_RULING.md`;
- `integration/V557_V558_COMPLETION_IMPLEMENTATION_RULING.md`;
- `integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`;
- Wave-0 `R0_04_RUNTIME_CONTRACT/RESULT.md`;
- Wave-0 `R0_05_VERTICAL_HARNESS/RESULT.md`;
- current V557/V558 completion-grade builders, V558 review/graft/governance gates, thin end-to-end path, and continuity tests.

The governing backward derivation is:

```text
accepted V3 needs exact mixed-producer structural possibility
+ V556 owns F1/F2 but V555 routes remain canonical base edges
+ V554 owns affordance/applicability possibility
+ V553 owns evidence time / temporal limits / negative authority
+ earlier producers retain structural fact / position authority
- V3-owned experience, realization, generated positions and attractor state
- V2-owned rendered expression
= V557 lossless authorization/publication
  → V558 immutable linking/indexing/repository publication
```

No new structural semantic family is required at either V557 or V558.

---

## 3. Producer-owned objects V557 must publish without reownership

V557 cannot lawfully be a serial “V556 payload adapter.” Its runtime-publication input is the **mixed-producer transitive DAG** required to interpret every admitted runtime object.

At minimum, where present and runtime-authorized, publication must retain exact producer identity for:

| Producer | Producer-owned meaning V557 must preserve or make transitively reachable | V557 jurisdiction |
|---|---|---|
| V552 / accepted earlier owner | structural facts, positions, relation endpoints, finite-stratum/native-geography authority and other exact structural references needed by later objects | authorize/publish/reference only |
| V553 | `TEMPORAL_KEY`, `TEMPORAL_OBSERVATION`, `TEMPORAL_RELATION`, `TEMPORAL_LIMIT / NEGATIVE_AUTHORITY`, exact evidence/support time and comparability state | preserve exact authority; attach runtime-use/proxy governance without mutating evidence time |
| V554 | `BOUNDED_STRUCTURAL_AFFORDANCE`, `STRUCTURAL_MEDIATION_APPLICABILITY_CONDITION` | preserve possibility/condition identity; never convert affordance into actor experience |
| V555 | `STRUCTURAL_MEDIATION_ROUTE_CANDIDATE`, route conditions and governed unary route effects where any exist | preserve exact V555 route ID as canonical atomic graph-edge identity |
| V556 F1 | `STRUCTURAL_PRESSURE_INTERACTION_RELATION` | preserve exact F1 ID, participant route IDs, roles/order/cardinality/direction, conditions and rule/provenance refs |
| V556 F2 | `STRUCTURAL_ATTRACTOR_PREREQUISITE_TOPOLOGY` | preserve exact F2 ID, exact V555 route and V556 F1 participants, motif/path/cycle roles, structural prerequisites and actor-history requirement refs |
| owning producer | uncertainty, absence, denied, noncomparable, missing-authority, rule/predicate and provenance objects required for interpretation | preserve typed negative/limit authority and exact references |

A later locator or index key is infrastructure only. It may never become the semantic identity of a V555 route, V556 F1/F2 object, V554 affordance, or V553 temporal object.

---

## 4. V557 hostile grain audit

### 4.1 `RUNTIME_AUTHORIZED_OBJECT_RECORD` grain — PASS

Required grain is **one authoritative producer object × one V557 runtime-publication decision**, retaining at minimum:

- producer collection identity;
- authoritative object ID and object/content hash;
- producer family/build/schema/compiler/version identity;
- producer-native permission/authority state;
- V557 narrowed item-use state;
- epistemic class;
- temporal-proxy eligibility rule reference or explicit missing/denied authority where applicable;
- exact negative/uncertainty/noncomparability references;
- admission/denial reason;
- immutable governance/policy versions.

This grain is sufficient because V557 decides runtime use of **producer-owned objects** rather than creating a new semantic aggregate. A collection-only permission would be too coarse; a field/slot-only projection would be lossy.

### 4.2 `RUNTIME_AUTHORIZED_COLLECTION_MANIFEST` grain — PASS

Required grain is **one authoritative logical producer collection/build tranche**, preserving:

- logical collection kind and producer;
- schema/compiler/build identity and hashes;
- authoritative object count;
- publication/admitted/denied counts as appropriate;
- collection state distinguishing at least valid-nonempty, governed valid-empty, denied/no-runtime-admission, missing authority and integrity/version failure;
- item-governance completeness;
- referential-closure status;
- manifest/content hash.

This prevents `0 rows` from meaning whatever a consumer finds convenient.

### 4.3 Valid-empty semantics — PASS

The accepted seam preserves producer valid-empty state as typed collection authority. This is essential for accepted V556, whose F1/F2 first tranches may be `VALID_EMPTY_NO_GOVERNED_RULE` or `VALID_EMPTY_NO_ELIGIBLE_AUTHORIZED_BASIS`.

Required distinctions remain separate:

```text
VALID_EMPTY
≠ DENIED
≠ NOT_APPLICABLE
≠ MISSING_AUTHORITY
≠ INTEGRITY_FAILURE
≠ CORRUPT / VERSION-INCOMPATIBLE
```

No downstream component may infer that an empty F1/F2 collection proves that no structural interaction/topology exists in reality.

### 4.4 Monotone permission narrowing — PASS

Permission law is correctly one-way:

```text
producer permission
    ≥ V557 publication/use permission
    ≥ V558 resolver query-relative permission
```

V557 may narrow, contextualize or deny. It may not create causal permission absent producer authority. A globally healthy build never promotes an individually denied item.

Dependencies required only for interpretation/audit may remain context-only while the dependent object is causal, provided their exact semantic identity remains present and the dependency role is preserved. Missing/corrupt indispensable dependencies block admission rather than licensing reconstruction.

### 4.5 Transitive reference closure — PASS

For every admitted object, V557 must prove reachability to all indispensable producer authority needed to interpret it, including as applicable:

- V556 F2 → exact V556 F1 and V555 route participants;
- V556 F1 → exact role-qualified V555 route participants;
- V555 route → exact V554 affordance/conditions and upstream structural/temporal refs;
- V554 → exact V553/V552 authority;
- V553 observation/relation/limit → exact temporal key and governed structural references;
- finite-stratum/native-geography/AH refs;
- rule/predicate/negative-authority/provenance refs.

Closure is semantic, not merely “referenced file exists.” The accepted implementation court correctly requires hash/identity and topology preservation.

### 4.6 Immutable V557→V558 publication identity — PASS

`V557_V558_RUNTIME_PUBLICATION_HANDOFF` must bind:

- immutable publication bundle ID;
- collection/object manifest hashes;
- source producer build identities/hashes;
- item-governance and proxy-policy versions;
- referential-closure audit identity;
- publication content hash.

A changed producer object/hash, changed V557 authorization decision, changed bound policy, or changed publication material creates a new publication identity. V558 must never discover a mutable “latest” V557 tree behind an unchanged identity.

---

## 5. V558 hostile repository audit

### 5.1 Collection registry — PASS

The accepted V558 contract requires a stage-agnostic collection registry mapping logical collection kinds to immutable repository-resident material. V3 discovers `structural facts`, `temporal authority`, `affordances`, `mediation routes`, `pressure interactions`, `attractor-prerequisite topologies`, negative authority, and governed Horizon/AH material as logical collections—not by stage-directory probing.

### 5.2 Producer-preserving `ObjectLocator` — PASS

Required locator law:

```text
ObjectLocator {
  locator_id,
  logical_collection_kind,
  authoritative_object_id,
  authoritative_object_hash,
  authoritative_producer_family,
  authoritative_build_id,
  repository_bundle_id,
  storage_locator,
  provenance_locator
}
```

`locator_id` is a nonsemantic lookup alias. Authoritative producer ID/hash remain first-class and reversible.

### 5.3 Reference graph — PASS

V558 materializes **reference arcs**, not new domain-semantic edges. The reference graph must preserve exact mixed-producer dependency structure and participant identity. It cannot infer a V556 F1 because two routes coexist, cannot decompose n-ary F1 without authority, and cannot flatten an F2 motif into an unordered bag of IDs.

### 5.4 Required indexes — PASS

The accepted repository requires or permits canonical indexes sufficient for deterministic stage-blind lookup while remaining reversible to authoritative objects:

- **temporal:** evidence/support time, temporal key/relation/limit, proxy eligibility metadata;
- **geographic:** native governed geography/scope without down-imputation;
- **stratal:** finite-stratum roles and distinct AH/Horizon references where governed;
- **position:** generated-position requirement IDs and applicability predicates;
- **relation/topology participant:** exact V555 route / V556 F1/F2 participant roles/order/cardinality;
- **negative authority:** denied/absence/noncomparable/missing/limit states;
- **provenance/permission:** producer identity/hash/build, epistemic class, item-use state, rule/policy versions.

Indexes are lookup projections. None acquires semantic authority independent of the producer object.

### 5.5 Immutable bundle/content hashes — PASS

A `StructuralPriorRepository` binds at minimum:

- repository bundle ID and schema version;
- source V557 publication manifest hash;
- source producer build/manifest hashes;
- publication policy and resolver policy versions;
- collection registry;
- locators/reference graph/index identities;
- collection fidelity/negative-state manifest;
- immutable producer material or content-addressed closure;
- repository content hash.

Any change to accepted producer material, V557 admission/governance, policy binding, locator/reference/index material, or repository contents yields a new immutable bundle. Atomic/stale-safe publication is required; a partial repository cannot become a valid bundle.

### 5.6 Standalone closure — PASS in architecture / FAIL in current code

The architectural rule is exact: raw V553–V556 stage directories may be physically absent after publication. The V558 bundle must contain or content-address every object needed for stage-blind resolution and audit. Hidden stage-directory discovery, mutable `latest_*_root`, or raw survey/DDM access is a seam failure.

Current V558 code cannot meet this because it reads the current V557 renderer bundle and governance material and publishes readiness/gate products, not a standalone structural-prior repository.

---

## 6. Accepted V3 hard-requirement matrix

The court tested the standalone V558 contract against every distinction named in the launch order.

| V3-required distinction | What must survive V557 | What V558 must retain/expose | Court result |
|---|---|---|---|
| structural possibility vs actor fact | producer object epistemic class + actor-realization prohibition; no generated history | repository prior remains `SOURCE_EVIDENCE` / `DERIVED_STRUCTURAL_PRIOR` / limit authority; generated V3 bindings are external `GENERATED_RUNTIME_FACT` query inputs | PASS |
| V554 affordance vs experience | exact `BOUNDED_STRUCTURAL_AFFORDANCE` and applicability-condition ID/hash, no realization claim | separate logical collection/reference; resolver may activate/defer applicability only; V3 creates encounter/exposure/experience | PASS |
| exact V555 route | exact canonical route ID/hash and route conditions; no V556/V557 re-ID | producer-preserving locator + route/reference indexes; route ID remains V3 experience identity | PASS |
| exact V556 F1 | exact F1 ID/hash; participant V555 route IDs; cardinality, roles/order/direction, conditions/rule refs | locator + reference graph retain n-ary structured relation and exact participants | PASS |
| exact V556 F2 | exact F2 ID/hash; exact V555/F1 participants; motif roles/order/cycles, conditions/rules | locator + reference graph retain the producer topology, not a slot/prose projection | PASS |
| F1 realization prerequisites | exact V556 F1 applicability/runtime-position/predicate/condition refs and upstream dependencies | resolver returns governed structural applicability/deferred state and preserves requirements; V3 alone creates `F1 realization` when generated history satisfies its own governed runtime rule | PASS |
| F2 satisfaction prerequisites | exact V556 F2 structural prerequisites plus actor-history requirement predicate IDs and dependency refs | resolver returns exact F2 topology/prerequisites; V3 satisfaction record remains downstream-generated and cannot rewrite F2 | PASS |
| unresolved generated position | runtime-position requirement refs; no prevalence/geography inference | position-requirement index + `UNBOUND_REQUIRES_RUNTIME_POSITION`; Phase B re-resolves same immutable bundle after V3 provides generated binding | PASS |
| proxy time vs evidence time | immutable V553 evidence/support refs + separate proxy-eligibility authority | SelectionRecord retains query time, evidence/support time, observation time, signed lag, proxy rule/version, `historical_observation_at_query_time=false`; no default interpolation | PASS |
| negative / missing / noncomparable | exact typed producer state and negative/limit refs; collection valid-empty state | negative-authority index + typed selection/rejection state; no zero/neutral coercion | PASS |
| exact provenance | authoritative object ID/hash/build/schema/rule/predicate references plus publication hashes | ObjectLocator + provenance index + bundle/content hashes + SelectionRecord | PASS |
| exact permission | producer permission plus V557 monotone narrowed item-use state | item-level permission survives into resolver decision; global status cannot widen it | PASS |

**Hard-requirement verdict:** the accepted repository contains enough information to make all required distinctions with raw producer directories absent.

---

## 7. Current implementation terrain: explicit nonconformance

### 7.1 Current completion-grade V557

`ddm_v557_renderer_contract.py` is still renderer-oriented. Its `_build_requirements()` reads `pressureflow_contract_slots`, extracts principally `slot_name`, and produces renderer-boundary, render-blocker, audit-requirement and V558-handoff rows. This cannot preserve the accepted mixed-producer graph.

It does not implement canonical:

- `RUNTIME_AUTHORIZED_OBJECT_RECORD`;
- `RUNTIME_AUTHORIZED_COLLECTION_MANIFEST`;
- producer-object transitive closure;
- exact V555 route / V556 F1/F2 preservation;
- item-level producer→V557 permission binding;
- immutable mixed-producer publication content hash.

The prompt-audit aggregation defect remains visible: the completion-grade builder can convert existence of a clean baseline audit row into packet-level prompt-shape detection/violation. The accepted architecture correctly demotes this audit to an operational sidecar and requires repair rather than weakening V558 fail-closed behavior.

### 7.2 Current V558

`ddm_v558_runtime_input_gate.py` reads current V557 readiness/renderer/audit artifacts and emits `normalized_runtime_input` dominated by statuses, prompt flags, renderer/runtime-wiring contracts, separation prose, blockers and global permissions.

It does not implement:

- `StructuralPriorRepository`;
- collection registry;
- producer-preserving `ObjectLocator` index;
- mixed-producer reference graph;
- temporal/geographic/stratal/position/negative/provenance indexes;
- immutable producer-object closure for standalone use;
- deterministic `ContextResolver` / `SelectionRecord` / `CoverageFidelityProfile`.

`ddm_v558_runtime_graft_readiness.py` is explicitly a review decision only and states that downstream continuity is intentionally untested. `ddm_v558_plus_governance.py` layers further governance over the current gate products; it cannot restore upstream structural distinctions already absent from those products.

### 7.3 Current producer-consumer shape mismatch

Current V558 handoff logic still expects fields including `future_consumer_notes` and `app_wiring_boundaries` from the V557 payload. Those belong to the older/thin-oriented shape and are not canonical fields of completion-grade V557. The accepted ruling correctly forbids thin-only prose fields from becoming semantic dependencies.

### 7.4 Thin versus completion-grade authority

`ddm_v5_thin_end_to_end.py` declares itself a thin boundary/readiness scaffold. Its V557/V558 specs are renderer/runtime-graft gate shapes, not terminal structural-prior publication semantics. It also contains older temporal/interpolated and slot-oriented expectations superseded by accepted V553–V558 architecture.

Therefore:

```text
accepted integration rulings / accepted terminal architecture
> future canonical completion implementation
> compatibility/reference facades
> current thin/scaffold semantic-ish payloads
```

Thin and completion-grade legacy paths may remain only as compatibility/test mechanics after they cease competing for semantic authority.

### 7.5 Global readiness versus item authority

Current code relies heavily on stage/global status and readiness booleans/scores. Those can remain operational diagnostics only.

Accepted V3 requires item-level distinctions. A collection/build may be healthy while one object is denied, noncomparable, context-only or unresolved. Conversely, a valid-empty collection may be semantically lawful. No `ready_for_v558`, `ready_for_runtime_graft_review`, readiness score, or global `generated_not_evidenced_flag` can replace item authority.

**Current production conformance verdict:** `FAIL__SUPERSEDED_NOT_RELEASED`.

---

## 8. Hostile seam cases

| Hostile case | Required accepted-seam behavior | Verdict |
|---|---|---|
| V555 route R17 is reissued under a V558 semantic edge ID | reject; locator alias may exist but R17 remains canonical | PASS |
| V556 n-ary F1 is decomposed into dyads by indexer | fail unless producer authority explicitly licenses decomposition | PASS |
| F2 survives but one required V555 route/F1/condition ref is missing | V557 closure fails; F2 not runtime-admissible | PASS |
| V556 F1/F2 collection is governed valid-empty | publish typed valid-empty collection manifest, not missing/error | PASS |
| healthy collection contains one denied item | denied item remains denied; collection health cannot widen permission | PASS |
| V553 point observation is rewritten as an interval | fail authority verification | PASS |
| forward temporal proxy is attempted without explicit proxy authority | no lawful anchor / missing authority | PASS |
| resolver chooses future evidence over an available lawful prior merely because it is closer | reject; latest lawful prior outranks ordinary forward proxy | PASS |
| class/sect/party-conditioned prior queried before generated binding exists | `UNBOUND_REQUIRES_RUNTIME_POSITION` | PASS |
| national value is copied and relabeled as locality value | reject; national may apply only at native national scope | PASS |
| V554 affordance is presented as actor encounter/experience | reject; V3 owns realization | PASS |
| V556 F1 is created because two routes co-resolve | reject; resolver may only select producer-created F1 | PASS |
| V556 F2 is treated as prerequisite satisfaction or final attractor | reject; V3 owns satisfaction and attractor trajectory | PASS |
| negative/noncomparable value is converted to numeric zero | reject | PASS |
| same authoritative ID appears with changed evidence time/content hash | fail closed | PASS |
| same bundle/query/policy/bindings resolves differently | fail deterministic replay court | PASS |
| raw V553–V556 directories removed | standalone V558 resolution remains identical | PASS required by architecture; FAIL current code |
| thin-only prose field absent | terminal V557→V558 seam still functions | PASS required by architecture; FAIL current legacy gate shape |

No hostile case exposes a missing **architectural** distinction at the V557→V558 seam.

---

## 9. Why `HARDEN` is not required

The court actively searched for a narrower defect that would justify `HARDEN`, especially in:

- dependency permissions versus dependent-object permission;
- collection valid-empty versus all-items-denied state;
- locator alias versus authoritative identity;
- F1 participant cardinality/order preservation;
- F2 structural prerequisites versus V3 satisfaction state;
- runtime-position unbound state;
- evidence-time versus proxy-time dual recording;
- raw-stage-independent standalone closure;
- bundle immutability and content hashing;
- negative/missing/noncomparable indexing;
- global readiness versus item authority.

Each already has an explicit accepted law. Further schema-level details belong to implementation packetization, not to a new semantic jurisdiction or architecture amendment. No concrete V3 starvation remains that cannot be implemented under the accepted V557/V558 jurisdiction.

`HARDEN` would therefore add redundant architecture prose rather than cure a missing seam distinction.

## 10. Why `REOPEN` is not required

`REOPEN` requires concrete starvation, duplication/bloat, jurisdiction error, or a producer-consumer mismatch that **cannot be cured under the accepted jurisdiction**.

The current producer-consumer mismatch is severe but already classified as superseded implementation terrain. It is precisely curable by the accepted packets:

```text
V557 P1 mixed-producer admission/collection manifests
→ P2 item governance
→ P3 closure/losslessness court
→ P4 immutable publication handoff
→ P5 compatibility cleanup

V558 P1 immutable linker
→ P2 stage-agnostic indexes
→ P3 deterministic resolver
→ P4 context/replay/fidelity/refresh
→ P5 standalone stage-blind V3 consumer court
```

No new semantic owner or extra numbered stage is needed. Reopening would confuse unimplemented accepted architecture with defective accepted architecture.

---

## 11. Implementation-release conditions preserved by this court

This `CONFIRM` does not release production work. A future implementation court must demonstrate at minimum:

1. one canonical V557 publication contract, with thin/legacy semantics demoted;
2. exact mixed-producer object and collection manifests;
3. item-level monotone permission and epistemic governance;
4. complete transitive reference closure for every admitted dependent object;
5. preservation of governed valid-empty collection states;
6. immutable V557 publication identity/content hash;
7. immutable V558 repository bundle with resident/content-addressed producer closure;
8. collection registry, producer-preserving locators and reference graph;
9. temporal/geographic/stratal/position/relation-topology/negative/provenance indexes;
10. deterministic resolver with item authority, tie/no-anchor/proxy/native-geography/progressive-binding law;
11. exact V555 route, V556 F1 and V556 F2 identity preservation into resolved context;
12. standalone reference-consumer proof with raw V553–V556 directories absent;
13. semantic loss tests that distinguish artifact/readiness success from actual continuity;
14. prompt baseline aggregation repair and current V557/V558 shape mismatch removal;
15. no global status/readiness scalar used as a substitute for item authority.

Until those are green, current V557/V558 remain non-terminal implementation terrain.

---

## 12. Final court disposition

### ACCEPTED SEAM IS RESPONSIBLE FOR

**V557:** lossless mixed-producer runtime authorization/publication, object- and collection-grain governance, monotone permission narrowing, exact transitive reference closure, typed valid-empty/negative states, immutable publication identity and hashes.

**V558:** immutable stage-agnostic linking/publication into `StructuralPriorRepository`, producer-preserving locators/reference graph/indexes, content-addressed standalone closure, deterministic resolver policy binding and stage-blind access.

### ACCEPTED SEAM IS NOT RESPONSIBLE FOR

- creating or re-owning V552–V556 structural semantics;
- generating actor positions, encounters, experience or biography;
- realizing V555 routes or V556 F1 relations;
- satisfying V556 F2 or forming actor attractors;
- mutating evidence time through runtime proxying;
- rendering V2 voice/dialogue/persona.

### STARVATION VERDICT

No accepted V3-required distinction is lost by the accepted V557→V558 architecture. Current implementation loses distinctions, but those surfaces are explicitly superseded and blocked from terminal promotion.

**V557_V558_SEAM_INTEGRITY = CONFIRM**
