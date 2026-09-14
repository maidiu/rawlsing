# T03 — GENERIC PRE-V3 STRUCTURAL BATCH CONTROL-PLANE IMPLEMENTATION R1 — RETURN

Repository: `maidiu/rawlsing`

Worker branch: `agent/rabochii-prev3-w18-t03-generic-structural-batch-control-plane-impl-r1`

Commission tip: `608f45518cd4b6be7b3204caf0bc4d82a6301e00`

Commission base / HQ authority: `190e74d0266b6bc75bd24a34ff5a139590f0ce30`

Exact grain:

`PREV3_GENERIC_SOURCE_SEMANTIC_BATCH_CONTROL_PLANE_IMPLEMENTATION_R1_ONLY`

Library: `NOT USED`

## Terminal

**PASS**

`T03_PASS__GENERIC_PREV3_STRUCTURAL_BATCH_CONTROL_PLANE_IMPLEMENTED__READY_FOR_SEPARATE_INDEPENDENT_QUALIFICATION`

This PASS is only at the commissioned implementation/test-artifact grain. It does not independently qualify the implementation, adjudicate source semantics, issue authority, qualify a semantic candidate, materialize an actor fact, construct a concrete rule, select a rule current, or compose topology.

## Governed implementation

The generic control plane is implemented as a small public facade over four candidate-agnostic modules:

- `rawlsing_next/_prev3_structural_batch_base.py` — blob `4e785a8eba66f092e95abea39ad3948ec1c3e019`;
- `rawlsing_next/_prev3_structural_batch_records.py` — blob `988b0c03359d9bdf89408b46acec90118ee422fa`;
- `rawlsing_next/_prev3_structural_batch_status.py` — blob `ed892763978110f4254d4c36fb130e3f9a058e50`;
- `rawlsing_next/_prev3_structural_batch_runtime.py` — blob `aec8167eaeceb229c932e162b1f922dea33a119c`;
- public facade `rawlsing_next/prev3_structural_batch_control_plane.py` — blob `33011d6461ab2b07b2b9d74003f91b48cc4ec00b`.

Contract identity:

`PREV3_GENERIC_SOURCE_SEMANTIC_BATCH_CONTROL_PLANE_R1@1.0.0`

## Implemented generic records and boundaries

The implementation provides the commissioned shared control-plane types and behavior:

1. `SourceLocalIntakeRecord` preserves exact source universe, source item, local state, routing/applicability, claim/evidence, provenance and producer-replay refs as one deterministic source-local identity.
2. `SemanticCandidateRecord` keeps semantic-core identity separate from evidence/admission/provenance edges and has exact generation/predecessor identity.
3. `PositionSemanticCore` exposes only occupant-independent structural-position semantics. `PositionMaterializationRequest` is a distinct later actor-indexed request identity and explicitly remains request-only, not a fact.
4. `MechanismRuleCandidateRoute` routes an admitted mechanism semantic core to a separately governed downstream contract without creating a concrete rule or currentness state.
5. `CandidateBlockerRecord`, `CandidateQuarantineRecord`, and `CandidateStatusRecord` provide typed local status, blocker, quarantine, N/A and currentness evidence surfaces.
6. `SemanticCoreAggregate` plus `reduce_semantic_candidates` implements exact governed many-to-one semantic-core reduction while unioning every contributing candidate, evidence/admission and provenance ref.
7. `StageReceipt` provides deterministic content-addressed stage receipts with predecessor-stage ordering.
8. `PositionQualificationRoute` and `MechanismRuleCandidateRoute` explicitly route to specialized downstream contracts without embedding their authority logic.
9. Fail-closed errors cover malformed refs, mutable selectors, identity conflicts, replay mismatch, occupant leakage, missing admission/authority basis, quarantined candidates and topology-boundary crossing.

## Exact scaling law preserved

The implementation operationalizes the adopted S02 law:

`QUESTION_COUNT != POSITION_COUNT != RULE_COUNT != TOPOLOGY_COUNT`

Many exact source/evidence nodes may reduce to one semantic core only when the governed semantic-core ref and its schema/ceiling signature are exact-equal. Similar wording, common source family, author identity, labels or model judgment never trigger deduplication.

Dedup is lossless at the provenance layer: contributing evidence/admission refs and provenance refs are deterministically unioned into `SemanticCoreAggregate`.

Exact duplicate presentation/retry of the same candidate snapshot is idempotent. Same logical candidate snapshot with different governed hashes is quarantined. Same semantic-core logical identity with different hashes is quarantined. Same exact core with conflicting semantic schema/negative ceiling/type-class ceiling is quarantined. No winner is selected.

Batch order, shard count, retry ordinal and worker identity are validated only as execution metadata and never enter semantic identity.

## Candidate-local blocker law

A blocker or quarantine applies only to its exact candidate by default.

Cross-candidate propagation is possible only when an exact `shared_contract_blocker_ref` is named and the target processing context explicitly presents that same exact shared-contract ref. No textual similarity or common blocker class causes propagation.

## Position / occupant split

`PositionSemanticCore.from_material(...)` rejects occupant/actor/person identity slots from reusable position semantic identity.

`PositionMaterializationRequest` separately requires:

- position semantic core ref;
- occupant actor/entity ref;
- applicability ref;
- exact permission AuthorityRef;
- valid-time/currentness ref;
- provenance/dependency refs;
- replay-authority ref.

Its material is stamped:

`REQUEST_ONLY__NO_ACTOR_FACT_MATERIALIZED`

No actor-indexed objective-position fact constructor exists in this control plane.

## Mechanism routing / R4 separation

A mechanism candidate route must preserve the exact admitted `semantic_core_ref`; substitution/widening is rejected. The route carries mechanism-class values and the exact type/class ceiling to the specialized downstream contract, but it carries no rule identity, rule body, R4 envelope, current-selection proof or `CURRENT_ACCEPTED` state.

This preserves the separation commissioned between T03 control-plane plumbing and T02's separately owned R4 batch-envelope adapter.

## Currentness and N/A fail-closed law

`CandidateStatusRecord` preserves the adopted noncollapse surface:

- `PASS != CURRENT`;
- `CANDIDATE_ONLY != QUALIFIED`;
- `QUALIFIED != CURRENT`;
- `NOT_APPLICABLE` requires exact N/A-basis refs;
- `CURRENT` requires exact current-selection refs and forbids noncurrent disposition refs;
- `HISTORICAL_NONCURRENT` requires both prior current-selection and noncurrent-disposition refs.

The control plane does not manufacture any of those evidentiary refs.

## Topology boundary

Automatic routing rejects downstream refs whose exact kind/object identity targets topology or source-to-receiver edge construction.

`process_semantic_batch(...)` only reduces governed semantic candidates. It cannot emit topology.

The implementation therefore preserves:

`NO_BATCH_STAGE_BEFORE_SEPARATE_TOPOLOGY_AUTHORITY_MAY_CREATE_A_SOURCE_TO_RECEIVER_EDGE_OR_OBJECTIVE_WORLD_TOPOLOGY`

## Deterministic test artifacts

Two local pytest suites are committed:

- `rawlsing_next/tests/test_prev3_structural_batch_control_plane.py` — blob `8cd39bd44f27ce50d2ec2e26f9cb1738212c2236`;
- `rawlsing_next/tests/test_prev3_structural_batch_control_plane_edges.py` — blob `de4142ca6a006a521fe729a12fa8be969626f00d`.

Together they contain **29 deterministic tests** covering the commissioned proof surface, including:

- exact source-local replay;
- exact-equal semantic-core dedup with all evidence/provenance retained;
- non-equal cores not deduped from similar labels;
- occupant identity rejected from reusable position-core material;
- actor-indexed materialization request identity remaining separate;
- mechanism routing without concrete-rule minting/currentness;
- candidate-local blocker/quarantine propagation unless exact shared contract blocker is named;
- order/shard/retry/worker invariance;
- malformed refs and mutable selectors failing closed;
- same-key candidate conflicts quarantined rather than winner-selected;
- semantic-core logical conflicts quarantined;
- governed schema/ceiling conflicts quarantined;
- blocked candidates not routed;
- topology routes rejected;
- deterministic stage receipts and predecessor ordering;
- exact current-selection requirement for `CURRENT`;
- exact N/A basis requirement;
- cross-route kind mismatch rejection;
- no free-text source-semantic inference surface;
- exact semantic-core/type-ceiling preservation without authority widening.

The tests are committed as the deterministic local qualification surface requested by the commission. T03 does not claim independent qualification of its own implementation; that is the explicitly separate successor gate.

## Static implementation audit

The branch delta from commission tip consists only of the five implementation/public-surface files, the two T03 test files, and this governed return. No S18 sibling output was consumed.

The control plane contains no M10-, Wright-, Q03-, source-author-, survey-family-, or candidate-specific default/path. M10/Q03 were not used as implementation inputs.

No source semantic inference from raw question text exists. The control plane consumes already-governed exact refs and semantic candidates only.

## Boundary preservation

- No new source semantic adjudication.
- No automatic semantic inference from question text.
- No concrete M10 rule.
- No `CURRENT_ACCEPTED` rule selection.
- No actor-indexed objective-position fact.
- No topology.
- No V555/M2 use.
- No V3/person state.
- No OBL063 semantics.
- No Library use.
- No MAIN/PRE-MAIN mutation.
- No T01/T02 provisional output consumed.

Successor gate:

`T03_PASS__GENERIC_CONTROL_PLANE_IMPLEMENTED__WAKE_SEPARATE_INDEPENDENT_QUALIFICATION_ONLY`
