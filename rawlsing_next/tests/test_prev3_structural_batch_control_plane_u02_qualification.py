from __future__ import annotations

from dataclasses import fields
import hashlib
import inspect

import pytest

import rawlsing_next.prev3_structural_batch_control_plane as cp
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.prev3_structural_batch_control_plane import (
    BlockerClass,
    CandidateBlockerRecord,
    CandidateKind,
    CandidateOutcome,
    CandidateQuarantineRecord,
    CandidateStage,
    CandidateStatusRecord,
    IdentityConflictError,
    PositionMaterializationRequest,
    PositionOccupantLeakError,
    PositionSemanticCore,
    QuarantineReason,
    SemanticCandidateRecord,
    SourceLocalIntakeRecord,
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


def _intake(tag: str = "x") -> SourceLocalIntakeRecord:
    return SourceLocalIntakeRecord(
        source_universe_ref=_ref("SOURCE_UNIVERSE", f"u-{tag}"),
        source_item_ref=_ref("SOURCE_ITEM", f"item-{tag}"),
        source_local_state_ref=_ref("SOURCE_LOCAL_STATE", f"state-{tag}"),
        routing_or_applicability_ref_or_exact_na=_ref("ROUTING_OR_APPLICABILITY", f"route-{tag}"),
        claim_refs=(_ref("CLAIM", f"claim-{tag}"),),
        evidence_status_ref=_ref("EVIDENCE_STATUS", f"evidence-{tag}"),
        provenance_refs=(_ref("PROVENANCE", f"provenance-{tag}"),),
        producer_replay_ref=_ref("REPLAY", f"replay-{tag}"),
    )


def _position_core(tag: str = "core") -> PositionSemanticCore:
    return PositionSemanticCore(
        semantic_class_ref=_ref("POSITION_CLASS", f"class-{tag}"),
        canonical_structural_meaning_ref=_ref("STRUCTURAL_MEANING", f"meaning-{tag}"),
        constitutive_objective_relation_refs=(_ref("OBJECTIVE_RELATION", f"relation-{tag}"),),
        required_counterpart_or_context_role_refs=(_ref("CONTEXT_ROLE", f"role-{tag}"),),
        semantic_negative_ceiling_ref=_ref("NEGATIVE_CEILING", f"core-negative-{tag}"),
    )


def _candidate(
    candidate_id: str,
    *,
    core_ref: ExactRef,
    kind: CandidateKind = CandidateKind.STRUCTURAL_POSITION,
    evidence_ref: ExactRef | None = None,
    provenance_ref: ExactRef | None = None,
    schema_ref: ExactRef | None = None,
    negative_ref: ExactRef | None = None,
    class_ref: ExactRef | None = None,
) -> SemanticCandidateRecord:
    return SemanticCandidateRecord(
        candidate_namespace="u02-fixture",
        candidate_id=candidate_id,
        snapshot_generation=0,
        predecessor_candidate_ref=None,
        candidate_kind=kind,
        semantic_core_ref=core_ref,
        semantic_schema_ref=schema_ref or _ref("SEMANTIC_SCHEMA", "shared-schema"),
        evidence_admission_refs=(evidence_ref or _ref("EVIDENCE_ADMISSION", f"e-{candidate_id}"),),
        negative_ceiling_ref=negative_ref or _ref("NEGATIVE_CEILING", "shared-negative"),
        type_class_ceiling_ref=class_ref or _ref("TYPE_CLASS_CEILING", "shared-class"),
        candidate_stage=CandidateStage.SEMANTIC_CORE_REDUCED,
        provenance_refs=(provenance_ref or _ref("PROVENANCE", f"p-{candidate_id}"),),
    )


def _status(candidate: SemanticCandidateRecord, outcome: CandidateOutcome = CandidateOutcome.CANDIDATE_ONLY) -> CandidateStatusRecord:
    return CandidateStatusRecord(
        candidate_ref=candidate.ref,
        outcome=outcome,
        basis_refs=(_ref("STATUS_BASIS", f"basis-{candidate.candidate_id}-{outcome.value}"),),
    )


def test_u02_source_local_identity_commits_every_governed_ref_without_widening():
    base = _intake("base")
    material = base.as_material()
    assert material["source_universe_ref"] == base.source_universe_ref.as_dict()
    assert material["source_item_ref"] == base.source_item_ref.as_dict()
    assert material["source_local_state_ref"] == base.source_local_state_ref.as_dict()
    assert material["routing_or_applicability_ref_or_exact_na"] == base.routing_or_applicability_ref_or_exact_na.as_dict()
    assert material["claim_refs"] == [base.claim_refs[0].as_dict()]
    assert material["evidence_status_ref"] == base.evidence_status_ref.as_dict()
    assert material["provenance_refs"] == [base.provenance_refs[0].as_dict()]
    assert material["producer_replay_ref"] == base.producer_replay_ref.as_dict()

    variants = [
        SourceLocalIntakeRecord(_ref("SOURCE_UNIVERSE", "u-other"), base.source_item_ref, base.source_local_state_ref, base.routing_or_applicability_ref_or_exact_na, base.claim_refs, base.evidence_status_ref, base.provenance_refs, base.producer_replay_ref),
        SourceLocalIntakeRecord(base.source_universe_ref, _ref("SOURCE_ITEM", "item-other"), base.source_local_state_ref, base.routing_or_applicability_ref_or_exact_na, base.claim_refs, base.evidence_status_ref, base.provenance_refs, base.producer_replay_ref),
        SourceLocalIntakeRecord(base.source_universe_ref, base.source_item_ref, _ref("SOURCE_LOCAL_STATE", "state-other"), base.routing_or_applicability_ref_or_exact_na, base.claim_refs, base.evidence_status_ref, base.provenance_refs, base.producer_replay_ref),
        SourceLocalIntakeRecord(base.source_universe_ref, base.source_item_ref, base.source_local_state_ref, _ref("ROUTING_OR_APPLICABILITY", "route-other"), base.claim_refs, base.evidence_status_ref, base.provenance_refs, base.producer_replay_ref),
        SourceLocalIntakeRecord(base.source_universe_ref, base.source_item_ref, base.source_local_state_ref, base.routing_or_applicability_ref_or_exact_na, (_ref("CLAIM", "claim-other"),), base.evidence_status_ref, base.provenance_refs, base.producer_replay_ref),
        SourceLocalIntakeRecord(base.source_universe_ref, base.source_item_ref, base.source_local_state_ref, base.routing_or_applicability_ref_or_exact_na, base.claim_refs, _ref("EVIDENCE_STATUS", "evidence-other"), base.provenance_refs, base.producer_replay_ref),
        SourceLocalIntakeRecord(base.source_universe_ref, base.source_item_ref, base.source_local_state_ref, base.routing_or_applicability_ref_or_exact_na, base.claim_refs, base.evidence_status_ref, (_ref("PROVENANCE", "provenance-other"),), base.producer_replay_ref),
        SourceLocalIntakeRecord(base.source_universe_ref, base.source_item_ref, base.source_local_state_ref, base.routing_or_applicability_ref_or_exact_na, base.claim_refs, base.evidence_status_ref, base.provenance_refs, _ref("REPLAY", "replay-other")),
    ]
    assert len({item.ref for item in [base, *variants]}) == 1 + len(variants)


def test_u02_source_execution_record_cannot_auto_become_semantic_authority():
    intake = _intake("portable")
    with pytest.raises(StructuralBatchControlPlaneError, match="SemanticCandidateRecord"):
        process_semantic_batch([intake])  # type: ignore[list-item]
    assert not hasattr(intake, "to_semantic_candidate")
    assert not hasattr(intake, "issue_authority")


def test_u02_exact_equal_core_reduction_is_lossless_and_deterministic():
    core = _position_core("shared").ref
    e1, e2 = _ref("EVIDENCE_ADMISSION", "e1"), _ref("EVIDENCE_ADMISSION", "e2")
    p1, p2 = _ref("PROVENANCE", "p1"), _ref("PROVENANCE", "p2")
    a = _candidate("a", core_ref=core, evidence_ref=e1, provenance_ref=p1)
    b = _candidate("b", core_ref=core, evidence_ref=e2, provenance_ref=p2)

    baseline = process_semantic_batch([a, b], shard_count=1, retry_ordinal=0, worker_identity="worker-a")
    replay = process_semantic_batch([b, a, a], shard_count=31, retry_ordinal=77, worker_identity="worker-b")
    assert baseline.aggregate_refs == replay.aggregate_refs
    assert baseline.quarantine_refs == replay.quarantine_refs == ()
    assert len(baseline.aggregates) == 1
    aggregate = baseline.aggregates[0]
    assert set(aggregate.candidate_refs) == {a.ref, b.ref}
    assert set(aggregate.evidence_admission_refs) == {e1, e2}
    assert set(aggregate.provenance_refs) == {p1, p2}


def test_u02_similarity_family_and_shared_provenance_cannot_create_semantic_equivalence():
    shared_evidence = _ref("EVIDENCE_ADMISSION", "same-source-family")
    shared_provenance = _ref("PROVENANCE", "same-author-family")
    a = _candidate(
        "near-label-a",
        core_ref=_position_core("manager-role-a").ref,
        evidence_ref=shared_evidence,
        provenance_ref=shared_provenance,
    )
    b = _candidate(
        "near-label-b",
        core_ref=_position_core("manager-role-b").ref,
        evidence_ref=shared_evidence,
        provenance_ref=shared_provenance,
    )
    result = reduce_semantic_candidates([a, b])
    assert not result.quarantines
    assert len(result.aggregates) == 2
    assert {item.semantic_core_ref for item in result.aggregates} == {a.semantic_core_ref, b.semantic_core_ref}


@pytest.mark.parametrize("extra_name", ["question_text", "raw_question", "embedding", "model_judgment", "source_author"])
def test_u02_free_text_embedding_model_or_author_inputs_are_not_semantic_oracle_fields(extra_name: str):
    kwargs = dict(
        candidate_namespace="u02",
        candidate_id="oracle-check",
        snapshot_generation=0,
        predecessor_candidate_ref=None,
        candidate_kind=CandidateKind.STRUCTURAL_POSITION,
        semantic_core_ref=_position_core("oracle").ref,
        semantic_schema_ref=_ref("SEMANTIC_SCHEMA", "s"),
        evidence_admission_refs=(_ref("EVIDENCE_ADMISSION", "e"),),
        negative_ceiling_ref=_ref("NEGATIVE_CEILING", "n"),
        type_class_ceiling_ref=_ref("TYPE_CLASS_CEILING", "c"),
        candidate_stage=CandidateStage.SEMANTIC_CORE_REDUCED,
        provenance_refs=(_ref("PROVENANCE", "p"),),
    )
    kwargs[extra_name] = "not-authority"
    with pytest.raises(TypeError):
        SemanticCandidateRecord(**kwargs)  # type: ignore[arg-type]


def test_u02_same_logical_core_different_hash_quarantines_every_contender_without_winner():
    core_a = _ref("POSITION_CORE", "same-logical", "governed-hash-a")
    core_b = _ref("POSITION_CORE", "same-logical", "governed-hash-b")
    a = _candidate("a", core_ref=core_a)
    b = _candidate("b", core_ref=core_b)
    result = reduce_semantic_candidates([a, b])
    assert result.aggregates == ()
    assert len(result.quarantines) == 2
    assert {q.candidate_ref for q in result.quarantines} == {a.ref, b.ref}
    assert {q.reason for q in result.quarantines} == {QuarantineReason.SEMANTIC_CORE_CONFLICT}


@pytest.mark.parametrize("conflict", ["schema", "negative", "type_class"])
def test_u02_exact_core_with_governed_ceiling_or_schema_conflict_quarantines_no_winner(conflict: str):
    core = _position_core(f"conflict-{conflict}").ref
    common = dict(core_ref=core)
    a = _candidate("a", **common)
    kwargs: dict[str, ExactRef] = {}
    if conflict == "schema":
        kwargs["schema_ref"] = _ref("SEMANTIC_SCHEMA", "different")
    elif conflict == "negative":
        kwargs["negative_ref"] = _ref("NEGATIVE_CEILING", "different")
    else:
        kwargs["class_ref"] = _ref("TYPE_CLASS_CEILING", "different")
    b = _candidate("b", **common, **kwargs)
    result = reduce_semantic_candidates([a, b])
    assert result.aggregates == ()
    assert len(result.quarantines) == 2


def test_u02_shared_blocker_or_quarantine_propagates_only_on_exact_shared_ref_hash():
    a = _candidate("a", core_ref=_position_core("local-a").ref)
    b = _candidate("b", core_ref=_position_core("local-b").ref)
    shared = _ref("SHARED_CONTRACT_BLOCKER", "contract-x", "exact-shared")
    same_logical_wrong_hash = _ref("SHARED_CONTRACT_BLOCKER", "contract-x", "wrong-shared")
    blocker = CandidateBlockerRecord(
        candidate_ref=a.ref,
        blocker_class=BlockerClass.CONTRACT_FIELD,
        field_path="contract",
        requirement="exact shared contract",
        basis_refs=(_ref("BASIS", "blocker"),),
        closure_requirement="repair exact shared contract",
        shared_contract_blocker_ref=shared,
    )
    quarantine = CandidateQuarantineRecord(
        candidate_ref=a.ref,
        reason=QuarantineReason.CONTRACT_BLOCKED,
        basis_refs=(_ref("BASIS", "quarantine"),),
        shared_contract_blocker_ref=shared,
    )
    assert not blocker_applies_to(blocker, b.ref)
    assert not blocker_applies_to(blocker, b.ref, exact_shared_contract_refs=(same_logical_wrong_hash,))
    assert blocker_applies_to(blocker, b.ref, exact_shared_contract_refs=(shared,))
    assert not quarantine_applies_to(quarantine, b.ref)
    assert not quarantine_applies_to(quarantine, b.ref, exact_shared_contract_refs=(same_logical_wrong_hash,))
    assert quarantine_applies_to(quarantine, b.ref, exact_shared_contract_refs=(shared,))


def test_u02_position_core_excludes_occupant_slots_and_materialization_stays_request_only():
    field_names = {field.name for field in fields(PositionSemanticCore)}
    assert not {"occupant_actor_or_entity_ref", "occupant_ref", "actor_ref", "entity_ref", "person_ref"}.intersection(field_names)

    material = {
        "semantic_class_ref": _ref("POSITION_CLASS", "c"),
        "canonical_structural_meaning_ref": _ref("STRUCTURAL_MEANING", "m"),
        "constitutive_objective_relation_refs": (_ref("OBJECTIVE_RELATION", "r"),),
        "required_counterpart_or_context_role_refs": (_ref("CONTEXT_ROLE", "role"),),
        "semantic_negative_ceiling_ref": _ref("NEGATIVE_CEILING", "n"),
        "actor_ref": _ref("ACTOR", "actor-1"),
    }
    with pytest.raises(PositionOccupantLeakError):
        PositionSemanticCore.from_material(material)

    core = _position_core("request")
    request = PositionMaterializationRequest(
        position_semantic_core_ref=core.ref,
        occupant_actor_or_entity_ref=_ref("ACTOR", "actor-1"),
        applicability_ref=_ref("APPLICABILITY", "a"),
        permission_authority_ref=_authority("POSITION_PERMISSION"),
        valid_time_currentness_ref=_ref("CURRENTNESS_EVIDENCE", "t"),
        provenance_dependency_refs=(_ref("PROVENANCE", "p"),),
        replay_authority_ref=_ref("REPLAY_AUTHORITY", "r"),
    )
    exported = request.as_material()
    assert exported["boundary"] == "REQUEST_ONLY__NO_ACTOR_FACT_MATERIALIZED"
    assert request.ref.kind == cp.POSITION_MATERIALIZATION_REQUEST_REF_KIND
    assert not any(name.startswith(("emit_", "materialize_", "create_fact")) for name in dir(request))


def test_u02_mechanism_route_preserves_admitted_core_and_type_ceiling_without_rule_or_currentness():
    core = _ref("NORMALIZED_MECHANISM", "m")
    candidate = _candidate(
        "m",
        core_ref=core,
        kind=CandidateKind.MECHANISM_RULE,
        class_ref=_ref("TYPE_CLASS_CEILING", "exact-class-ceiling"),
    )
    route = route_mechanism_candidate(
        candidate,
        _status(candidate),
        normalized_mechanism_ref=core,
        mechanism_class_values=("P1 MATERIAL_ACCESS_DEPENDENCY",),
        downstream_contract_ref=_ref("R4_GENERIC_BATCH_ENVELOPE_CONTRACT", "r4"),
        routing_basis_refs=(_ref("ROUTING_BASIS", "rb"),),
    )
    exported = route.as_material()
    assert exported["normalized_mechanism_ref"] == candidate.semantic_core_ref.as_dict()
    assert exported["type_class_ceiling_ref"] == candidate.type_class_ceiling_ref.as_dict()
    assert exported["boundary"] == "ROUTE_ONLY__NO_CONCRETE_RULE_OR_CURRENTNESS"
    forbidden = {"rule_identity", "rule_body", "current_selection_ref", "authority_ref", "authority_refs"}
    assert not forbidden.intersection(exported)

    with pytest.raises(IdentityConflictError, match="replace or widen"):
        route_mechanism_candidate(
            candidate,
            _status(candidate),
            normalized_mechanism_ref=_ref("NORMALIZED_MECHANISM", "neighbor"),
            mechanism_class_values=("P1 MATERIAL_ACCESS_DEPENDENCY",),
            downstream_contract_ref=_ref("R4_GENERIC_BATCH_ENVELOPE_CONTRACT", "r4"),
            routing_basis_refs=(_ref("ROUTING_BASIS", "rb"),),
        )


def test_u02_status_states_do_not_collapse_and_evidentiary_states_fail_closed():
    candidate = _candidate("status", core_ref=_position_core("status").ref)
    passed = _status(candidate, CandidateOutcome.PASS)
    candidate_only = _status(candidate, CandidateOutcome.CANDIDATE_ONLY)
    qualified = _status(candidate, CandidateOutcome.QUALIFIED)
    assert passed.outcome is CandidateOutcome.PASS
    assert passed.current_selection_refs == ()
    assert passed.ref != candidate_only.ref != qualified.ref

    with pytest.raises(StructuralBatchControlPlaneError, match="N/A basis"):
        _status(candidate, CandidateOutcome.NOT_APPLICABLE)
    with pytest.raises(StructuralBatchControlPlaneError, match="current-selection"):
        _status(candidate, CandidateOutcome.CURRENT)
    with pytest.raises(StructuralBatchControlPlaneError, match="prior selection"):
        _status(candidate, CandidateOutcome.HISTORICAL_NONCURRENT)

    prior = _ref("CURRENT_SELECTION", "prior")
    current = CandidateStatusRecord(
        candidate_ref=candidate.ref,
        outcome=CandidateOutcome.CURRENT,
        basis_refs=(_ref("BASIS", "current"),),
        current_selection_refs=(prior,),
    )
    historical = CandidateStatusRecord(
        candidate_ref=candidate.ref,
        outcome=CandidateOutcome.HISTORICAL_NONCURRENT,
        basis_refs=(_ref("BASIS", "historical"),),
        current_selection_refs=(prior,),
        noncurrent_disposition_refs=(_ref("NONCURRENT_DISPOSITION", "superseded"),),
    )
    assert current.ref != historical.ref


def test_u02_topology_boundary_rejects_position_and_mechanism_routes():
    position = _candidate("position", core_ref=_position_core("topology").ref)
    with pytest.raises(TopologyBoundaryError):
        route_position_candidate(
            position,
            _status(position),
            downstream_contract_ref=_ref("SOURCE_TO_RECEIVER_EDGE", "builder"),
            routing_basis_refs=(_ref("ROUTING_BASIS", "p"),),
        )

    core = _ref("NORMALIZED_MECHANISM", "topology")
    mechanism = _candidate("mechanism", core_ref=core, kind=CandidateKind.MECHANISM_RULE)
    with pytest.raises(TopologyBoundaryError):
        route_mechanism_candidate(
            mechanism,
            _status(mechanism),
            normalized_mechanism_ref=core,
            mechanism_class_values=("P1 MATERIAL_ACCESS_DEPENDENCY",),
            downstream_contract_ref=_ref("OBJECTIVE_WORLD_TOPOLOGY", "builder"),
            routing_basis_refs=(_ref("ROUTING_BASIS", "m"),),
        )


def test_u02_public_surface_contains_no_free_text_semantic_inference_or_person_state_constructor():
    exported = set(cp.__all__)
    forbidden_exact = {
        "infer_semantics",
        "infer_semantic_core",
        "semantic_oracle",
        "build_topology",
        "create_source_to_receiver_edge",
        "materialize_actor_fact",
        "create_person_state",
        "create_v3_state",
        "create_obl063_terminal",
    }
    assert not exported.intersection(forbidden_exact)

    function_names = {
        name
        for name in exported
        if callable(getattr(cp, name, None)) and inspect.isfunction(getattr(cp, name))
    }
    assert not any("infer" in name.lower() for name in function_names)
