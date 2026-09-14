# S02 — PRE-V3 STRUCTURAL PIPELINE GENERALIZATION / BATCH-READINESS AUDIT R1

Repository: `maidiu/rawlsing`

Worker branch: `agent/rabochii-prev3-w17-s02-structural-pipeline-generalization-audit-r1`

Commission tip: `dc0b3a86c12e526371f1326116b11145fe303028`

Commission base / HQ authority: `8306aab9a3174f65c611f8157530307dabaf539c`

Exact grain: `PREV3_STRUCTURAL_POSITION_MECHANISM_PIPELINE_GENERALIZATION_AND_BATCH_READINESS_AUDIT_R1_ONLY`

Library: `NOT USED`

S01 output consumed: `NO`

S03 output consumed: `NO`

## Terminal

`S02_PASS__PQR_CANARY_GENERALIZES_TO_BATCHABLE_PREV3_PIPELINE__READY_FOR_GENERIC_BATCH_IMPLEMENTATION`

Binary recommendation:

`READY_FOR_GENERIC_BATCH_IMPLEMENTATION`

This means the adopted P/Q/R canary now exposes enough generic contract shape, identity law, authority law, currentness law and complete R4 field inventory to implement one shared batch pipeline. It does **not** mean that the current Q03 instance is repaired, that M10-M01 has a concrete/current rule, that any actor fact is current, or that topology is authorized.

## 1. Authority surface audited

This audit consumes only the adopted surface available at the commission base:

- P03 return `903079c179abca4eabd163c99b19efdef1855ce9`;
- Q01 PASS `aeb377d25f649d6743c4347709cf34a65238e330`;
- corrected Q02 blocker `ff277902459cbf786e8f7d839b4f786546bd5610`;
- Q03 PASS `e84eb2d35a9711fdf49ec984295cc7b5e3d0ef48`, subsequently qualified by adopted R01;
- R01 adopted blocker `c4066d35fc49364682fcf50df968918c7d5fccf3`;
- R02 adopted PASS `17320729b411f8e339d65c3491c1d30fe7364ea3`;
- R03 adopted PASS `0e9458a189d870406797564de7142f6a73a15ad2`;
- R03 complete 28-row matrix blob `a182df47286ece3fd2f27de0a1c2d4adac333a64`;
- generic R4 constructor `SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0`, blob `c94997f5c7f2bbee9cd99c570554fd48c0f47556`.

The source-local exact-identity substrate already present at the HQ state is also reusable: canonical `ExactRef` / `AuthorityRef` / semantic hashing in `rawlsing_next/pre553_empirical_objects.py` and fail-closed exact authority selection in `rawlsing_next/pre553_empirical_authority.py`. S02 does not widen those PRE553 contracts into structural authority; it reuses only their exact identity/state/replay discipline for intake.

## 2. Classification law

`GENERIC` means a reusable contract, state law, role pattern, identity law, stage boundary or field inventory whose meaning does not depend on Wright, M10-M01, Q73A, one source locus, one authority identity, one actor or one candidate hash.

`INSTANCE_SPECIFIC` means a concrete source, claim, semantic payload, candidate-class assignment, exact authority instance, exact scope/current-selection object, exact row status/basis, baseline comparison or candidate-specific content hash.

Where one artifact mixes reusable shape and concrete content, S02 classifies the shape and the instance material separately. The whole artifact is never called generic merely because part of its schema is reusable.

## 3. P/Q/R material classification

| ID | Material | Classification | Holding |
|---|---|---|---|
| P03-01 | M10 Wright source worker / ledger / documentary loci | `INSTANCE_SPECIFIC` | `0ebca9...`, ledger blob `606de007...`, Wright loci and their claims are one source corpus. |
| P03-02 | M10-M01 property-separation / wage-dependency mechanism kernel | `INSTANCE_SPECIFIC` | The exact inputs, derivation, outputs and ceilings are M10-M01 content. |
| P03-03 | Assignment of M10-M01 to `P1 MATERIAL_ACCESS_DEPENDENCY` | `INSTANCE_SPECIFIC` | P1-P5 is generic vocabulary; this candidate-to-class assignment is not. |
| P03-04 | `SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0` constructor | `GENERIC` | The constructor accepts exact rule, trace, authority and currentness material without an M10 identity. |
| P03-05 | `SOURCE_CITATION != CAUSAL_USE_AUTHORITY` | `GENERIC` | Applies to every source/candidate. |
| P03-06 | `CONSTITUTION_CURRENT != RULE_CURRENT != APPLICATION_CURRENT != FACT_CURRENT != WITNESS_CURRENT` | `GENERIC` | Currentness layers are candidate-agnostic. |
| Q01-01 | `RULE_OWNER` role / `BOUND` binding shape | `GENERIC` | Exact scope + AuthorityRef + nonempty authority-current-selection evidence is reusable. |
| Q01-02 | M10-M01 RULE_OWNER authority, scope, selection and binding refs | `INSTANCE_SPECIFIC` | Authority hash `80fd8e...` and its exact M10 scope/selection are one instance. |
| Q01-03 | Deterministic authority canonicalization / replay shape | `GENERIC` | Exact immutable hashing and replay are reusable; Q01's values are not. |
| Q01-04 | RULE_OWNER currentness does not imply CAUSAL_USE or rule currentness | `GENERIC` | Cross-role/currentness noncollapse is reusable. |
| Q02-01 | Mandatory exact `CAUSAL_USE` AuthorityRef + scope + explicit current-selection requirement | `GENERIC` | Required by the generic R4 constructor. |
| Q02-02 | M10-M01 Q02 missing-CAUSAL_USE blocker | `INSTANCE_SPECIFIC` | Historical M10 blocker; adopted R02 later closes that exact package positively. |
| Q03-01 | Structural-position semantic-admission stage | `GENERIC` | A position semantic candidate can be admitted without emitting an actor-indexed fact. |
| Q03-02 | `PRODUCTIVE_ASSET_SEPARATED_ACTIVE_WAGE_LABOUR_POSITION` payload | `INSTANCE_SPECIFIC` | Productive-asset/wage semantics are M10-specific. |
| Q03-03 | Q03 canonical identity material and candidate hash `e040ae...` | `INSTANCE_SPECIFIC` | It binds M10 source/commission/baseline material and contains the R01 occupant-identity defect. |
| Q03-04 | Q03 distinctness proof against Q73A / existing PREV3POS | `INSTANCE_SPECIFIC` | Q73A is a canary-specific contrast, not the generic position contract. |
| Q03-05 | Semantic-admission currentness does not imply fact/world currentness | `GENERIC` | Reusable stage noncollapse. |
| Q03-06 | Later position qualification/materialization gate shape | `GENERIC` | Occupant identity + applicability + permission + valid-time/currentness + provenance/dependency + replay belong at later fact materialization. |
| R01-01 | `POSITION_SEMANTIC_IDENTITY != OCCUPANT_ACTOR_INDEXED_OBJECTIVE_POSITION_FACT_IDENTITY` | `GENERIC` | HQ adopted this exact generic law. |
| R01-02 | Failure of Q03 candidate `e040ae...` because occupant identity is hashed into semantic identity | `INSTANCE_SPECIFIC` | The current Q03 artifact is a negative conformance fixture until separately repaired. |
| R02-01 | CAUSAL_USE construction pattern | `GENERIC` | Explicit source claim/evidence ceiling + competent project-side owner/scope + exact current selection + fail-closed contract; neither citation nor HQ desire alone suffices. |
| R02-02 | `RAWLSING_HQ_PREV3_SDTF_M10_M01_CAUSAL_USE@1.0.0` and exact hashes | `INSTANCE_SPECIFIC` | Authority `ebd955...`, scope `e102...`, selection `6687...`, binding `146537...` are M10-M01 values. |
| R02-03 | R02 permitted/prohibited M10-M01 causal-use payload | `INSTANCE_SPECIFIC` | Exact structural derivation and overclaim ceilings are claim-specific content. |
| R03-01 | 28-row R4 external constructor determinant field inventory | `GENERIC` | 3 rule-identity + 1 class + 1 constitution-current + 13 trace + 6 authority + 1 value-mode + 3 currentness fields. |
| R03-02 | R03 M10-M01 28-row classifications / bases / closures | `INSTANCE_SPECIFIC` | `SATISFIED_*`, `MISSING`, `BLOCKED`, `NOT_APPLICABLE` states and refs are the M10 canary snapshot. |
| R03-03 | Six-package workflow shape DEP-A through DEP-F | `GENERIC` | Rule identity/shape/value; causal use; auxiliary authorities; trace lift; qualification/time/portability; final current selection is reusable scheduling structure. |
| R03-04 | M10-M01 states of DEP-A through DEP-F | `INSTANCE_SPECIFIC` | Which package is open/closed/blocked is candidate-specific; HQ notes R02 later closes M10 DEP-B. |
| R03-05 | Derived-output law for mechanism-class composition ref, binding hash and final binding ref | `GENERIC` | Derived deterministically from complete input material; no hidden authority slot. |
| R03-06 | `CANDIDATE_NOT_CURRENT` / `CURRENT_ACCEPTED` / `HISTORICAL_NONCURRENT` state machine | `GENERIC` | Candidate-agnostic rule-currentness law. |
| R03-07 | Auxiliary authority disposition law | `GENERIC` | Explicit `BOUND` or exact `NOT_APPLICABLE`; calibration branches on explicit value mode. |
| R03-08 | M10 source/claim/evidence/mechanism/input/ceiling trace values | `INSTANCE_SPECIFIC` | Exact M10 values fill generic trace fields. |
| PQR-01 | ExactRef / AuthorityRef / content-addressed identity + no latest/default/fuzzy selection | `GENERIC` | Deterministic exact-reference discipline is reusable. |
| PQR-02 | PRE-V3 objective-world / V3 stop boundary | `GENERIC` | Applies across structural candidates. |
| PQR-03 | Topology composition boundary | `GENERIC` | Position/rule qualification never creates topology by implication. |
| PQR-04 | M10/Q03/Q73A names, paths, commits, blobs and candidate-specific authority names | `INSTANCE_SPECIFIC` | Provenance/fixture values stay in payloads, never generic field semantics. |

The classification is therefore not “make M10 generic.” It is “retain the generic contracts/laws and feed M10 only as one exact instance.”

## 4. M10-specific coupling still present

### 4.1 Generic R4 constructor

No M10-specific coupling is present in the generic R4 constructor surface itself. M10 enters only through supplied field values.

### 4.2 Q03 position artifact

The current Q03 object must **not** be copied wholesale as the generic structural-position identity template. It is deliberately an instance artifact and contains:

- an M10/Q03-specific schema/canonical name;
- exact Wright source worker, ledger and loci;
- exact commission/HQ identities;
- Q73A baseline distinctness material;
- and, unlawfully for reusable position semantics, hashed `EXACT_OBJECTIVE_ACTOR_OR_ENTITY_IDENTITY`.

Only the last item is the adopted R01 qualification failure. The other source/authority/baseline fields are not newly declared unlawful by S02; they show why the whole Q03 admission object is **instance-specific** rather than the reusable semantic core needed for many-to-few batch deduplication.

For generic batching, distinguish:

`POSITION_SEMANTIC_CORE`

from

`SOURCE_EVIDENCE / ADMISSION RECEIPTS FOR THAT CORE`

from

`OCCUPANT_ACTOR_INDEXED_OBJECTIVE_POSITION_FACT`.

That allows many source claims to support one reusable position meaning while preserving every source/evidence edge and keeping occupant identity out of the semantic core.

### 4.3 Q01/R02 authority objects

The RULE_OWNER and CAUSAL_USE **patterns** are generic. Their authority IDs, exact scopes, selection evidence and content hashes remain instance-specific and must never be baked into a generic batch schema.

### 4.4 R03 matrix

The 28 field names and constructor conditions are generic. The M10 row status, basis and closure content is instance-specific. A batch processor therefore instantiates the same 28-row checklist for every mechanism-rule candidate rather than cloning the R03 JSON and editing strings.

## 5. Required-domain audit

1. **Source-local evidence/state intake — GENERIC.** Preserve exact source universe, native item/question identity, source-local state, routing/applicability, claim/evidence state, provenance and replay. A source question remains evidence even when its semantic content deduplicates downstream.
2. **Structural-position semantic candidate contract — GENERIC SHAPE, INSTANCE PAYLOAD.** A reusable semantic core contains objective structural meaning, not occupant identity. The current Q03 object is a canary instance, not the generic template.
3. **Occupant-independent semantic identity vs actor-indexed fact — GENERIC LAW ADOPTED.** R01/HQ closes the architectural question exactly.
4. **Position qualification/materialization gate — GENERIC.** Actor/entity identity enters only at later fact materialization with applicability, permission, valid-time/currentness, provenance/dependency and replay authority.
5. **Mechanism/source-claim normalization — GENERIC STAGE.** Source claims normalize to content-addressed mechanism semantic cores while source/evidence refs remain attached separately.
6. **RULE_OWNER authority pattern — GENERIC.** Q01 is one successful instance.
7. **CAUSAL_USE authority pattern — GENERIC.** Q02 proves fail-closed absence; R02 proves lawful positive construction without citation laundering.
8. **G1+G6 28-row mechanism-rule envelope — GENERIC FINITE FIELD SURFACE.** R03 proves there are no hidden post-matrix external authority slots.
9. **Currentness separation — GENERIC.** Candidate/current/application/fact/witness and authority/rule currentness remain separate.
10. **Batch intake/replay/status/error/blocker — GENERIC CONTROL-PLANE SCHEMA BELOW.** Batch order is nonsemantic.
11. **18,000+ questions to a smaller governed semantic DAG — GENERIC MANY-TO-FEW MODEL.** Preserve 18,000+ source evidence nodes if present; do not require 18,000 positions or rules.
12. **Topology composition — SEPARATE GENERIC BOUNDARY.** No batch intake, admission, qualification, authority or rule-currentness stage creates topology automatically.

## 6. Proposed generic batch-candidate input schema

This is a **control-plane audit freeze**, not a new runtime ontology and not an implementation.

### A. `SourceLocalIntakeRecord`

Required slots:

```text
source_universe_ref
source_item_ref
source_local_state_ref
routing_or_applicability_ref_or_exact_na
claim_refs[]
evidence_status_ref
provenance_refs[]
producer_replay_ref
```

Law: source-local identity is never replaced by normalized semantic identity and is never discarded merely because another source item supports the same semantic core.

### B. `SemanticCandidateRecord`

Required slots:

```text
candidate_kind = STRUCTURAL_POSITION | MECHANISM_RULE
semantic_core_ref
semantic_schema_ref
evidence_admission_refs[]
negative_ceiling_ref
candidate_stage
```

Semantic identity must exclude:

- batch ID, shard ID, ingest ordinal, retry count and worker identity;
- source question number as semantic meaning;
- mutable latest/default/fuzzy selectors;
- actor/entity occupant identity for a structural-position semantic core.

Source/evidence provenance attaches through evidence/admission refs. It is preserved without forcing duplicate semantic cores.

### C. Generic structural-position semantic core

Required semantic slots:

```text
semantic_class_ref
canonical_structural_meaning_ref
constitutive_objective_relation_refs[]
required_counterpart_or_context_role_refs[]
semantic_negative_ceiling_ref
```

Forbidden semantic-identity slot:

`occupant_actor_or_entity_ref`

A **separate later** materialization request, if independently authorized, must carry:

```text
position_semantic_core_ref
occupant_actor_or_entity_ref
applicability_ref
permission_authority_ref
valid_time_currentness_ref
provenance_dependency_refs[]
replay_authority_ref
```

S02 creates no such fact.

### D. Generic mechanism-rule candidate

Required generic slots:

```text
normalized_mechanism_ref
mechanism_class_values[]
r4_28_row_input_or_disposition_map
rule_currentness_requested_state
```

Every R03 constructor determinant must be represented as one of:

- exact value/ref;
- typed blocker;
- unavailable;
- exact `NOT_APPLICABLE` only where the governing contract permits it.

Silence never means N/A.

## 7. Batch output/status schema

Each stage emits a content-addressed receipt with:

```text
batch_item_ref
stage
object_kind
outcome
input_refs[]
output_refs[]
authority_refs[]
replay_ref
```

Allowed control-plane outcomes:

```text
PASS
BLOCKED
UNAVAILABLE
NOT_APPLICABLE
CANDIDATE_ONLY
QUALIFIED
CURRENT
HISTORICAL_NONCURRENT
QUARANTINED
```

Conditional material:

- `BLOCKED`: blocker class, exact field/path, exact requirement, basis refs, closure requirement;
- `UNAVAILABLE`: missing/unavailable requirement + basis refs; unavailable is not negative proof;
- `NOT_APPLICABLE`: exact N/A-basis ref; omission is never N/A;
- `CURRENT`: domain-specific current-selection evidence refs;
- `HISTORICAL_NONCURRENT`: prior selection refs + noncurrent disposition refs;
- `QUARANTINED`: failed identity/contract ref + exact reason/basis.

Generic blocker classes may be represented at the control plane as source/evidence, semantic-identity, contract-field, authority, scope, qualification, temporal/portability, currentness, replay/integrity and topology-boundary failures. These classes organize failures; they do not replace the exact blocker text/refs.

Noncollapse laws:

```text
PASS != CURRENT
CANDIDATE_ONLY != QUALIFIED
QUALIFIED != CURRENT
UNAVAILABLE != NEGATIVE_EVIDENCE
MISSING_OR_BLOCKED != NOT_APPLICABLE
AUTHORITY_CURRENT != RULE_CURRENT != FACT_CURRENT != APPLICATION_CURRENT != WITNESS_CURRENT
QUARANTINED != VALID_SEMANTIC_CORE
```

## 8. Deduplication / canonicalization law

The required scaling law is not lossy deduplication. It is layered identity.

### Level 1 — source item

Identity is exact source universe + source-local item/question identity + source semantics/provenance. Distinct source items remain distinct evidence nodes.

### Level 2 — reusable semantic core

Identity is canonical schema/version + constitutive structural meaning. Exact semantic equality may collapse many source claims onto one semantic core, but every supporting source/evidence admission remains as a separate ref/edge.

### Level 3 — position fact

Identity, when independently materialized later, includes position semantic core + exact occupant/entity + applicability/permission + valid time/currentness + required provenance/dependency. Two occupants never deduplicate merely because they occupy the same semantic position.

### Level 4 — mechanism rule body

Identity is exact immutable rule ID/version/body content hash. Rule-body identity is distinct from its evidence/authority envelope.

### Level 5 — R4 rule envelope

Identity is the complete canonical R4 binding material, including exact trace and authority bindings. Only exact complete binding equality deduplicates.

### Level 6 — topology

Topology has a separate authorized composition identity. It is never inferred from shared source, semantic core, actor coordinate, mechanism class or count.

Therefore:

`QUESTION_COUNT != POSITION_COUNT != RULE_COUNT != TOPOLOGY_COUNT`

means there is no required one-to-one cardinality mapping. Accidental numerical equality carries no semantic force.

Canonicalization requirements:

- deterministic UTF-8 canonical JSON/material projection;
- lexicographically ordered mapping keys;
- deterministic sorting of set-like exact refs;
- exact immutable IDs/hashes;
- no latest/default/fuzzy/nearest/range selection where exact refs are required;
- batch order, shard, retry order, wall-clock time and worker identity do not enter semantic identity.

## 9. Execution model for 18,000+ source questions

The correct execution model is a content-addressed staged map/reduce pipeline, not one bespoke worker chain per source question.

### Stage A — source-local intake

Highly parallel validation of source identity/state/routing/evidence/provenance. Emit exact intake receipts.

### Stage B — bounded claim normalization

Parallel production of claim / position / mechanism candidate payload refs. No authority, fact or currentness is inferred here.

### Stage C — semantic-core reduction

Map candidates to canonical semantic-core keys; deterministic reduce clusters exact-equal cores and unions **refs**, not prose, to their evidence/admission sets. Provenance is not dropped.

### Stage D — generic contract validation

For positions, enforce occupant-independent semantic identity and the later fact split. For mechanism rules, instantiate the same 28-row R4 determinant map for every candidate.

### Stage E — authority closure

Resolve exact authority instances or typed blocker/N/A results per role. RULE_OWNER and CAUSAL_USE remain independent. Citation, class membership and downstream need never manufacture authority.

### Stage F — qualification / envelope validation

Positions may become qualified semantic candidates only under their generic gate. Rule envelopes may validate as candidate-not-current when their required fields close. Batch processing itself emits no actor fact.

### Stage G — independent current selection

Only a separately competent selector may move a complete eligible object to its domain's current state. Currentness is never copied across layers.

### Stage H — topology composition

Outside the automatic candidate batch by default. Requires a separately authorized composition contract over exact eligible objective-world nodes/relations.

Sharding law: shard by stable content-addressed source-item or semantic-core key prefix. Deterministic reduction sorts exact refs, so shard count does not affect identity.

Retry/resume law: each stage receipt is a content-addressed checkpoint. Retry uses the same exact inputs/contracts/authorities. Replay mismatch quarantines the item rather than silently generating a replacement identity.

Partial failure law: one blocked/unavailable/quarantined item does not invalidate unrelated items. Batch summaries must report exact counts by state without treating unresolved items as negatives.

Minimum batch coverage counters:

```text
source_items_seen
source_items_valid
claim_candidates_emitted
semantic_cores_unique
position_cores_unique
rule_candidates_unique
blocked_count_by_class
unavailable_count
not_applicable_count
candidate_only_count
qualified_count
current_count
historical_noncurrent_count
quarantined_count
```

## 10. Topology composition boundary

Hard law:

`NO_BATCH_STAGE_BEFORE_SEPARATE_TOPOLOGY_AUTHORITY_MAY CREATE A SOURCE_TO_RECEIVER_EDGE_OR OBJECTIVE_WORLD_TOPOLOGY`

The following do **not** imply topology:

- same source question;
- same semantic core;
- position qualification;
- rule qualification/currentness;
- shared actor coordinate;
- mechanism-class membership.

A future topology/composition contract must separately bind exact eligible nodes/relations, direction/roles, applicability, provenance and currentness.

## 11. Exact remaining generalization blockers

At the S02 **architecture-audit** grain:

`NONE`

No unresolved *shape* question requires another bespoke source/candidate worker before generic batch infrastructure can be implemented. The adopted canary has already supplied:

- exact content-addressed identity/replay discipline;
- the generic position-vs-occupant split law from R01/HQ;
- positive RULE_OWNER and CAUSAL_USE authority patterns from Q01/R02 plus Q02 fail-closed evidence;
- the complete finite 28-row R4 constructor determinant surface from R03;
- layer-separated currentness;
- an explicit topology stop boundary.

The following remain real work but are **not** reclassified as generalization blockers:

1. Q03 candidate `e040ae...` remains unqualified/quarantined until independently repaired and replay-qualified. S02 did not consume S01.
2. M10-M01 still lacks a concrete rule body and multiple candidate-specific R03 envelope closures; R02 closes only the adopted M10 CAUSAL_USE package.
3. No M10-M01 rule is `CURRENT_ACCEPTED`.
4. No actor-indexed objective-position fact exists.
5. No topology exists.
6. This proposed batch interface is an audit freeze, not an implementation.
7. S03 output was not consumed, presumed or used as proof.

Those are instance or implementation tasks. They do not justify returning to one-worker-per-question architecture.

## 12. Readiness decision

`READY_FOR_GENERIC_BATCH_IMPLEMENTATION`

Implementation is ready to target the generic source-intake / semantic-core / evidence-admission / status / replay pipeline and shared position/rule contract processing **provided** it conforms to these gates:

- reject or quarantine any structural-position semantic core containing occupant actor/entity identity;
- keep source/evidence admissions separate from reusable semantic-core identity;
- account explicitly for all 28 R4 determinant fields;
- use exact immutable `AuthorityRef` / `ExactRef` and explicit current-selection evidence;
- never infer authority from source citation, class membership or HQ desire alone;
- preserve every currentness separation;
- keep topology outside automatic batch candidate processing.

This readiness is deliberately narrower than candidate success. Generic batch implementation can begin while individual candidates remain blocked, unavailable, candidate-only or quarantined. That is the scaling property the 18,000-question universe requires.

## Boundary preservation

- No source semantics were added.
- No M10 rule was minted.
- No Q03 repair or replacement candidate was minted.
- No actor-indexed fact was emitted.
- No topology was created.
- No V3/person state or OBL063 semantics were used.
- No S01 or S03 output was consumed.
- Library was not used.
- MAIN and PRE-MAIN were not mutated.
