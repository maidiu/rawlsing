from __future__ import annotations

import hashlib

import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.prev3_structural_batch_control_plane import (
    BLOCKER_REF_KIND,
    STAGE_RECEIPT_REF_KIND,
    BatchStage,
    BlockerClass,
    CandidateBlockerRecord,
    CandidateKind,
    CandidateOutcome,
    CandidateQuarantineRecord,
    CandidateStage,
    CandidateStatusRecord,
    IdentityConflictError,
    MechanismRuleCandidateRoute,
    MutableSelectorError,
    PositionMaterializationRequest,
    PositionOccupantLeakError,
    PositionQualificationRoute,
    PositionSemanticCore,
    QuarantineReason,
    SemanticCandidateRecord,
    SourceLocalIntakeRecord,
    StageReceipt,
    StructuralBatchControlPlaneError,
    TopologyBoundaryError,
    blocker_applies_to,
    process_semantic_batch,
    quarantine_applies_to,
    reduce_semantic_candidates,
    route_mechanism_candidate,
    route_position_candidate,
)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _ref(kind: str, object_id: str, salt: str | None = None) -> ExactRef:
    return ExactRef(kind, object_id, _sha(salt or f"{kind}|{object_id}"))


def _authority(name: str = "AUTH", version: str = "1.0.0") -> AuthorityRef:
    return AuthorityRef(name, version, _sha(f"{name}@{version}"))


def _source_intake(tag: str = "a") -> SourceLocalIntakeRecord:
    return SourceLocalIntakeRecord(
        source_universe_ref=_ref("SOURCE_UNIVERSE", f"u-{tag}"),
        source_item_ref=_ref("SOURCE_ITEM", f"q-{tag}"),
        source_local_state_ref=_ref("SOURCE_STATE", f"state-{tag}"),
        routing_or_applicability_ref_or_exact_na=_ref("ROUTING", f"route-{tag}"),
        claim_refs=(_ref("CLAIM", f"claim-{tag}"),),
        evidence_status_ref=_ref("EVIDENCE_STATUS", f"evidence-{tag}"),
        provenance_refs=(_ref("PROVENANCE", f"prov-{tag}"),),
        producer_replay_ref=_ref("REPLAY", f"replay-{tag}"),
    )


def _position_core(tag: str = "shared") -> PositionSemanticCore:
    return PositionSemanticCore(
        semantic_class_ref=_ref("POSITION_CLASS", f"class-{tag}"),
        canonical_structural_meaning_ref=_ref("STRUCTURAL_MEANING", f"meaning-{tag}"),
        constitutive_objective_relation_refs=(
            _ref("OBJECTIVE_RELATION", f"relation-{tag}"),
        ),
        required_counterpart_or_context_role_refs=(
            _ref("CONTEXT_ROLE", f"role-{tag}"),
        ),
        semantic_negative_ceiling_ref=_ref("NEGATIVE_CEILING", f"ceiling-{tag}"),
    )


def _candidate(
    candidate_id: str,
    *,
    core_ref: ExactRef,
    kind: CandidateKind = CandidateKind.STRUCTURAL_POSITION,
    evidence: str | None = None,
    provenance: str | None = None,
    schema_ref: ExactRef | None = None,
    negative_ref: ExactRef | None = None,
    class_ref: ExactRef | None = None,
    generation: int = 0,
    predecessor: ExactRef | None = None,
) -> SemanticCandidateRecord:
    return SemanticCandidateRecord(
        candidate_namespace="fixture",
        candidate_id=candidate_id,
        snapshot_generation=generation,
        predecessor_candidate_ref=predecessor,
        candidate_kind=kind,
        semantic_core_ref=core_ref,
        semantic_schema_ref=schema_ref or _ref("SEMANTIC_SCHEMA", "shared-schema"),
        evidence_admission_refs=(
            _ref("EVIDENCE_ADMISSION", evidence or f"evidence-{candidate_id}"),
        ),
        negative_ceiling_ref=negative_ref or _ref("NEGATIVE_CEILING", "shared-negative"),
        type_class_ceiling_ref=class_ref or _ref("TYPE_CLASS_CEILING", "shared-class"),
        candidate_stage=CandidateStage.SEMANTIC_CORE_REDUCED,
        provenance_refs=(_ref("PROVENANCE", provenance or f"prov-{candidate_id}"),),
    )


def _status(candidate: SemanticCandidateRecord, outcome: CandidateOutcome = CandidateOutcome.CANDIDATE_ONLY) -> CandidateStatusRecord:
    return CandidateStatusRecord(
        candidate_ref=candidate.ref,
        outcome=outcome,
        basis_refs=(_ref("STATUS_BASIS", f"basis-{candidate.candidate_id}"),),
    )


def test_exact_source_local_inputs_replay_deterministically():
    a = _source_intake("det")
    b = _source_intake("det")
    assert a.as_material() == b.as_material()
    assert a.ref == b.ref
    assert a.require_replay(b.ref) is a


def test_source_local_identity_changes_when_exact_source_item_changes():
    a = _source_intake("a")
    b = _source_intake("b")
    assert a.ref != b.ref


def test_same_governed_semantic_core_dedups_identity_and_preserves_all_evidence_and_provenance():
    core = _position_core().ref
    a = _candidate("a", core_ref=core, evidence="e1", provenance="p1")
    b = _candidate("b", core_ref=core, evidence="e2", provenance="p2")
    result = reduce_semantic_candidates([b, a])
    assert not result.quarantines
    assert len(result.aggregates) == 1
    aggregate = result.aggregates[0]
    assert aggregate.semantic_core_ref == core
    assert set(aggregate.candidate_refs) == {a.ref, b.ref}
    assert {r.object_id for r in aggregate.evidence_admission_refs} == {"e1", "e2"}
    assert {r.object_id for r in aggregate.provenance_refs} == {"p1", "p2"}


def test_exact_duplicate_retry_is_idempotently_deduplicated():
    core = _position_core("retry").ref
    candidate = _candidate("same", core_ref=core)
    once = reduce_semantic_candidates([candidate])
    retry = reduce_semantic_candidates([candidate, candidate, candidate])
    assert once.aggregate_refs == retry.aggregate_refs
    assert once.quarantine_refs == retry.quarantine_refs == ()


def test_semantically_nonidentical_cores_never_dedup_from_similar_labels():
    a = _candidate("a", core_ref=_position_core("near-a").ref)
    b = _candidate("b", core_ref=_position_core("near-b").ref)
    result = reduce_semantic_candidates([a, b])
    assert not result.quarantines
    assert len(result.aggregates) == 2
    assert {x.semantic_core_ref for x in result.aggregates} == {a.semantic_core_ref, b.semantic_core_ref}


def test_position_semantic_core_rejects_occupant_identity_field():
    material = {
        "semantic_class_ref": _ref("POSITION_CLASS", "c"),
        "canonical_structural_meaning_ref": _ref("STRUCTURAL_MEANING", "m"),
        "constitutive_objective_relation_refs": (_ref("OBJECTIVE_RELATION", "r"),),
        "required_counterpart_or_context_role_refs": (_ref("CONTEXT_ROLE", "role"),),
        "semantic_negative_ceiling_ref": _ref("NEGATIVE_CEILING", "n"),
        "occupant_actor_or_entity_ref": _ref("ACTOR", "actor-1"),
    }
    with pytest.raises(PositionOccupantLeakError):
        PositionSemanticCore.from_material(material)


def test_position_materialization_request_has_separate_actor_indexed_identity_and_is_not_a_fact():
    core = _position_core("request")
    common = dict(
        position_semantic_core_ref=core.ref,
        applicability_ref=_ref("APPLICABILITY", "a"),
        permission_authority_ref=_authority("POSITION_MATERIALIZATION_AUTH"),
        valid_time_currentness_ref=_ref("VALID_TIME", "v"),
        provenance_dependency_refs=(_ref("PROVENANCE", "p"),),
        replay_authority_ref=_ref("REPLAY_AUTHORITY", "r"),
    )
    a = PositionMaterializationRequest(
        occupant_actor_or_entity_ref=_ref("ACTOR", "actor-a"), **common
    )
    b = PositionMaterializationRequest(
        occupant_actor_or_entity_ref=_ref("ACTOR", "actor-b"), **common
    )
    assert a.ref != b.ref
    assert a.position_semantic_core_ref == b.position_semantic_core_ref == core.ref
    assert a.as_material()["boundary"] == "REQUEST_ONLY__NO_ACTOR_FACT_MATERIALIZED"


def test_mechanism_candidate_route_does_not_mint_rule_or_currentness():
    core = _ref("NORMALIZED_MECHANISM", "m")
    candidate = _candidate(
        "m",
        core_ref=core,
        kind=CandidateKind.MECHANISM_RULE,
        class_ref=_ref("TYPE_CLASS_CEILING", "p1"),
    )
    route = route_mechanism_candidate(
        candidate,
        _status(candidate),
        normalized_mechanism_ref=core,
        mechanism_class_values=("P1 MATERIAL_ACCESS_DEPENDENCY",),
        downstream_contract_ref=_ref("R4_GENERIC_BATCH_ENVELOPE_CONTRACT", "r4"),
        routing_basis_refs=(_ref("ROUTING_BASIS", "rb"),),
    )
    assert isinstance(route, MechanismRuleCandidateRoute)
    material = route.as_material()
    assert material["candidate_ref"] == candidate.ref.as_dict()
    assert material["boundary"] == "ROUTE_ONLY__NO_CONCRETE_RULE_OR_CURRENTNESS"
    assert "rule_identity" not in material
    assert "rule_currentness" not in material


def test_mechanism_route_rejects_semantic_core_substitution():
    core = _ref("NORMALIZED_MECHANISM", "m")
    candidate = _candidate("m", core_ref=core, kind=CandidateKind.MECHANISM_RULE)
    with pytest.raises(IdentityConflictError, match="replace or widen"):
        route_mechanism_candidate(
            candidate,
            _status(candidate),
            normalized_mechanism_ref=_ref("NORMALIZED_MECHANISM", "other"),
            mechanism_class_values=("P1 MATERIAL_ACCESS_DEPENDENCY",),
            downstream_contract_ref=_ref("R4_GENERIC_BATCH_ENVELOPE_CONTRACT", "r4"),
            routing_basis_refs=(_ref("ROUTING_BASIS", "rb"),),
        )


def test_position_route_is_specialized_routing_only():
    candidate = _candidate("p", core_ref=_position_core("route").ref)
    route = route_position_candidate(
        candidate,
        _status(candidate),
        downstream_contract_ref=_ref("POSITION_QUALIFICATION_CONTRACT", "q"),
        routing_basis_refs=(_ref("ROUTING_BASIS", "rb"),),
    )
    assert isinstance(route, PositionQualificationRoute)
    assert route.as_material()["boundary"] == "ROUTE_ONLY__NO_OCCUPANT_FACT"


def test_blocker_is_candidate_local_without_exact_shared_contract_ref():
    a = _candidate("a", core_ref=_position_core("block-a").ref)
    b = _candidate("b", core_ref=_position_core("block-b").ref)
    blocker = CandidateBlockerRecord(
        candidate_ref=a.ref,
        blocker_class=BlockerClass.AUTHORITY,
        field_path="authority",
        requirement="exact authority",
        basis_refs=(_ref("BASIS", "one"),),
        closure_requirement="supply exact authority",
    )
    assert blocker_applies_to(blocker, a.ref)
    assert not blocker_applies_to(blocker, b.ref)


def test_blocker_can_propagate_only_when_exact_shared_contract_blocker_is_named():
    a = _candidate("a", core_ref=_position_core("shared-a").ref)
    b = _candidate("b", core_ref=_position_core("shared-b").ref)
    shared = _ref("SHARED_CONTRACT_BLOCKER", "contract-x")
    blocker = CandidateBlockerRecord(
        candidate_ref=a.ref,
        blocker_class=BlockerClass.CONTRACT_FIELD,
        field_path="contract",
        requirement="shared contract available",
        basis_refs=(_ref("BASIS", "one"),),
        closure_requirement="repair shared contract",
        shared_contract_blocker_ref=shared,
    )
    assert not blocker_applies_to(blocker, b.ref)
    assert blocker_applies_to(blocker, b.ref, exact_shared_contract_refs=(shared,))


def test_quarantine_is_candidate_local_without_exact_shared_contract_ref():
    a = _candidate("a", core_ref=_position_core("qa").ref)
    b = _candidate("b", core_ref=_position_core("qb").ref)
    q = CandidateQuarantineRecord(
        candidate_ref=a.ref,
        reason=QuarantineReason.CONTRACT_BLOCKED,
        basis_refs=(_ref("BASIS", "q"),),
    )
    assert quarantine_applies_to(q, a.ref)
    assert not quarantine_applies_to(q, b.ref)


def test_batch_order_shard_retry_and_worker_identity_do_not_change_semantic_outputs():
    core = _position_core("stable").ref
    a = _candidate("a", core_ref=core, evidence="e1")
    b = _candidate("b", core_ref=core, evidence="e2")
    baseline = process_semantic_batch([a, b])
    changed_execution = process_semantic_batch(
        [b, a, a], shard_count=17, retry_ordinal=9, worker_identity="worker-x"
    )
    assert baseline.aggregate_refs == changed_execution.aggregate_refs
    assert baseline.quarantine_refs == changed_execution.quarantine_refs


def test_mutable_selectors_fail_closed_in_source_refs_and_candidate_identity():
    with pytest.raises(MutableSelectorError):
        SourceLocalIntakeRecord(
            source_universe_ref=_ref("SOURCE_UNIVERSE", "LATEST"),
            source_item_ref=_ref("SOURCE_ITEM", "q"),
            source_local_state_ref=_ref("SOURCE_STATE", "state"),
            routing_or_applicability_ref_or_exact_na=_ref("ROUTING", "route"),
            claim_refs=(_ref("CLAIM", "claim"),),
            evidence_status_ref=_ref("EVIDENCE_STATUS", "e"),
            provenance_refs=(_ref("PROVENANCE", "p"),),
            producer_replay_ref=_ref("REPLAY", "r"),
        )
    with pytest.raises(MutableSelectorError):
        _candidate("LATEST", core_ref=_position_core("mutable").ref)


def test_same_candidate_snapshot_key_with_conflicting_governed_material_quarantines_both():
    core = _position_core("identity-conflict").ref
    a = _candidate("same", core_ref=core, evidence="e-a")
    b = _candidate("same", core_ref=core, evidence="e-b")
    result = reduce_semantic_candidates([a, b])
    assert not result.aggregates
    assert len(result.quarantines) == 2
    assert {q.reason for q in result.quarantines} == {QuarantineReason.IDENTITY_CONFLICT}
    assert {q.candidate_ref for q in result.quarantines} == {a.ref, b.ref}


def test_same_semantic_core_logical_key_with_different_hashes_quarantines_without_winner():
    core_a = _ref("POSITION_CORE", "same-logical", "hash-a")
    core_b = _ref("POSITION_CORE", "same-logical", "hash-b")
    a = _candidate("a", core_ref=core_a)
    b = _candidate("b", core_ref=core_b)
    result = reduce_semantic_candidates([a, b])
    assert not result.aggregates
    assert len(result.quarantines) == 2
    assert {q.reason for q in result.quarantines} == {QuarantineReason.SEMANTIC_CORE_CONFLICT}


def test_same_exact_core_with_conflicting_governed_schema_or_ceiling_quarantines():
    core = _position_core("governance-conflict").ref
    a = _candidate("a", core_ref=core, schema_ref=_ref("SEMANTIC_SCHEMA", "a"))
    b = _candidate("b", core_ref=core, schema_ref=_ref("SEMANTIC_SCHEMA", "b"))
    result = reduce_semantic_candidates([a, b])
    assert not result.aggregates
    assert len(result.quarantines) == 2
    assert {q.reason for q in result.quarantines} == {QuarantineReason.SEMANTIC_CORE_CONFLICT}


def test_quarantined_or_blocked_candidate_cannot_route():
    candidate = _candidate("q", core_ref=_position_core("blocked").ref)
    blocker = _ref(BLOCKER_REF_KIND, "b")
    status = CandidateStatusRecord(
        candidate_ref=candidate.ref,
        outcome=CandidateOutcome.BLOCKED,
        basis_refs=(_ref("BASIS", "b"),),
        blocker_refs=(blocker,),
    )
    with pytest.raises(StructuralBatchControlPlaneError):
        route_position_candidate(
            candidate,
            status,
            downstream_contract_ref=_ref("POSITION_QUALIFICATION_CONTRACT", "q"),
            routing_basis_refs=(_ref("ROUTING_BASIS", "rb"),),
        )


def test_topology_route_is_rejected_from_automatic_candidate_processing():
    candidate = _candidate("p", core_ref=_position_core("topology").ref)
    with pytest.raises(TopologyBoundaryError):
        route_position_candidate(
            candidate,
            _status(candidate),
            downstream_contract_ref=_ref("OBJECTIVE_WORLD_TOPOLOGY", "edge-builder"),
            routing_basis_refs=(_ref("ROUTING_BASIS", "rb"),),
        )


def test_stage_receipt_identity_is_deterministic_and_execution_metadata_is_absent():
    candidate = _candidate("receipt", core_ref=_position_core("receipt").ref)
    kwargs = dict(
        batch_item_ref=candidate.ref,
        stage=BatchStage.SEMANTIC_CORE_REDUCTION,
        object_kind="SEMANTIC_CANDIDATE",
        outcome=CandidateOutcome.CANDIDATE_ONLY,
        input_refs=(candidate.ref,),
        output_refs=(candidate.semantic_core_ref,),
        authority_refs=(),
        basis_refs=(_ref("RECEIPT_BASIS", "basis"),),
    )
    a = StageReceipt(**kwargs)
    b = StageReceipt(**kwargs)
    assert a.ref == b.ref
    material = a.as_material()
    for forbidden in ("batch_id", "shard", "retry", "wall_clock", "worker_identity"):
        assert forbidden not in material


def test_stage_receipt_predecessor_must_be_earlier_stage():
    item = _ref("ITEM", "x")
    predecessor = _ref(STAGE_RECEIPT_REF_KIND, f"{item.content_hash}:AUTHORITY_CLOSURE")
    with pytest.raises(IdentityConflictError):
        StageReceipt(
            batch_item_ref=item,
            stage=BatchStage.GENERIC_CONTRACT_VALIDATION,
            object_kind="SEMANTIC_CANDIDATE",
            outcome=CandidateOutcome.CANDIDATE_ONLY,
            input_refs=(item,),
            output_refs=(),
            authority_refs=(),
            basis_refs=(_ref("BASIS", "r"),),
            predecessor_receipt_ref=predecessor,
            predecessor_stage=BatchStage.AUTHORITY_CLOSURE,
        )


def test_current_status_requires_explicit_current_selection_evidence():
    candidate = _candidate("current", core_ref=_position_core("current").ref)
    with pytest.raises(StructuralBatchControlPlaneError, match="current-selection"):
        CandidateStatusRecord(
            candidate_ref=candidate.ref,
            outcome=CandidateOutcome.CURRENT,
            basis_refs=(_ref("BASIS", "current"),),
        )


def test_not_applicable_status_requires_exact_na_basis():
    candidate = _candidate("na", core_ref=_position_core("na").ref)
    with pytest.raises(StructuralBatchControlPlaneError, match="N/A basis"):
        CandidateStatusRecord(
            candidate_ref=candidate.ref,
            outcome=CandidateOutcome.NOT_APPLICABLE,
            basis_refs=(_ref("BASIS", "na"),),
        )


def test_position_candidate_rejects_mechanism_route_and_mechanism_candidate_rejects_position_route():
    position = _candidate("p", core_ref=_position_core("cross-route").ref)
    with pytest.raises(StructuralBatchControlPlaneError):
        route_mechanism_candidate(
            position,
            _status(position),
            normalized_mechanism_ref=position.semantic_core_ref,
            mechanism_class_values=("P1 MATERIAL_ACCESS_DEPENDENCY",),
            downstream_contract_ref=_ref("R4_GENERIC_BATCH_ENVELOPE_CONTRACT", "r4"),
            routing_basis_refs=(_ref("BASIS", "route"),),
        )

    mechanism_core = _ref("NORMALIZED_MECHANISM", "cross-route")
    mechanism = _candidate("m", core_ref=mechanism_core, kind=CandidateKind.MECHANISM_RULE)
    with pytest.raises(StructuralBatchControlPlaneError):
        route_position_candidate(
            mechanism,
            _status(mechanism),
            downstream_contract_ref=_ref("POSITION_QUALIFICATION_CONTRACT", "q"),
            routing_basis_refs=(_ref("BASIS", "route2"),),
        )
