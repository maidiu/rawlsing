from __future__ import annotations

import hashlib

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.prev3_structural_batch_control_plane import (
    CandidateKind,
    CandidateOutcome,
    CandidateStage,
    CandidateStatusRecord,
    MalformedExactRefError,
    SemanticCandidateRecord,
    SourceLocalIntakeRecord,
    StructuralBatchControlPlaneError,
    process_semantic_batch,
    route_mechanism_candidate,
)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _ref(kind: str, object_id: str, salt: str | None = None) -> ExactRef:
    return ExactRef(kind, object_id, _sha(salt or f"{kind}|{object_id}"))


def _candidate() -> SemanticCandidateRecord:
    core = _ref("NORMALIZED_MECHANISM", "m")
    return SemanticCandidateRecord(
        candidate_namespace="fixture",
        candidate_id="m",
        snapshot_generation=0,
        predecessor_candidate_ref=None,
        candidate_kind=CandidateKind.MECHANISM_RULE,
        semantic_core_ref=core,
        semantic_schema_ref=_ref("SEMANTIC_SCHEMA", "mechanism"),
        evidence_admission_refs=(_ref("EVIDENCE_ADMISSION", "e"),),
        negative_ceiling_ref=_ref("NEGATIVE_CEILING", "n"),
        type_class_ceiling_ref=_ref("TYPE_CLASS_CEILING", "p1"),
        candidate_stage=CandidateStage.SEMANTIC_CORE_REDUCED,
        provenance_refs=(_ref("PROVENANCE", "p"),),
    )


def test_non_exact_ref_input_fails_closed():
    with pytest.raises(MalformedExactRefError):
        SourceLocalIntakeRecord(
            source_universe_ref="not-an-exact-ref",  # type: ignore[arg-type]
            source_item_ref=_ref("SOURCE_ITEM", "q"),
            source_local_state_ref=_ref("SOURCE_STATE", "s"),
            routing_or_applicability_ref_or_exact_na=_ref("ROUTING", "r"),
            claim_refs=(_ref("CLAIM", "c"),),
            evidence_status_ref=_ref("EVIDENCE_STATUS", "e"),
            provenance_refs=(_ref("PROVENANCE", "p"),),
            producer_replay_ref=_ref("REPLAY", "x"),
        )


def test_control_plane_does_not_infer_source_semantics_from_free_text():
    with pytest.raises(TypeError):
        SemanticCandidateRecord(  # type: ignore[call-arg]
            candidate_namespace="fixture",
            candidate_id="m",
            snapshot_generation=0,
            predecessor_candidate_ref=None,
            candidate_kind=CandidateKind.MECHANISM_RULE,
            semantic_core_ref=_ref("NORMALIZED_MECHANISM", "m"),
            semantic_schema_ref=_ref("SEMANTIC_SCHEMA", "mechanism"),
            evidence_admission_refs=(_ref("EVIDENCE_ADMISSION", "e"),),
            negative_ceiling_ref=_ref("NEGATIVE_CEILING", "n"),
            type_class_ceiling_ref=_ref("TYPE_CLASS_CEILING", "p1"),
            candidate_stage=CandidateStage.SEMANTIC_CORE_REDUCED,
            provenance_refs=(_ref("PROVENANCE", "p"),),
            question_text="infer a semantic core for me",
        )


def test_route_carries_exact_admitted_core_without_authority_or_semantic_widening():
    candidate = _candidate()
    status = CandidateStatusRecord(
        candidate_ref=candidate.ref,
        outcome=CandidateOutcome.CANDIDATE_ONLY,
        basis_refs=(_ref("STATUS_BASIS", "b"),),
    )
    route = route_mechanism_candidate(
        candidate,
        status,
        normalized_mechanism_ref=candidate.semantic_core_ref,
        mechanism_class_values=("P1 MATERIAL_ACCESS_DEPENDENCY",),
        downstream_contract_ref=_ref("R4_GENERIC_BATCH_ENVELOPE_CONTRACT", "r4"),
        routing_basis_refs=(_ref("ROUTING_BASIS", "rb"),),
    )
    material = route.as_material()
    assert material["normalized_mechanism_ref"] == candidate.semantic_core_ref.as_dict()
    assert material["type_class_ceiling_ref"] == candidate.type_class_ceiling_ref.as_dict()
    assert "authority_ref" not in material
    assert "authority_refs" not in material
    assert "semantic_inference" not in material


def test_execution_metadata_validation_is_nonsemantic_and_fail_closed():
    candidate = _candidate()
    with pytest.raises(StructuralBatchControlPlaneError):
        process_semantic_batch([candidate], shard_count=0)
    with pytest.raises(StructuralBatchControlPlaneError):
        process_semantic_batch([candidate], retry_ordinal=-1)
    a = process_semantic_batch([candidate], shard_count=1, retry_ordinal=0)
    b = process_semantic_batch([candidate], shard_count=64, retry_ordinal=99, worker_identity="w")
    assert a.aggregate_refs == b.aggregate_refs
