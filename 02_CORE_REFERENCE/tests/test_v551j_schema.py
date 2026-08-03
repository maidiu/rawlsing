from __future__ import annotations

from data.ddm_build_copy.ddm_v551j_schema import (
    V551J_AUTHORITY_STATUSES,
    V551J_DIRECTIONALITY_STATUSES,
    V551J_FORBIDDEN_CLAIM_IDS,
    V551J_FUTURE_TARGET_AFFORDANCES,
    V551J_PACKET_CANDIDATE_TRACE_SCHEMA,
    V551J_PACKET_STATUSES,
    V551J_REVIEW_PRIORITIES,
    V551J_REVIEW_SURFACE_SCHEMA,
    V551J_REVIEW_SURFACE_STATUSES,
    V551J_REVIEWABLE_EVIDENCE_SIDECAR_SCHEMA,
    V551J_RUNTIME_USE_CLASSES,
)


def test_schema_required_columns_exist():
    required = V551J_PACKET_CANDIDATE_TRACE_SCHEMA["required_columns"]
    assert "packet_id" in required
    assert "runtime_use_class" in required
    assert "forbidden_claim_ids_json" in required
    assert "v552_context_status" in required


def test_schema_enums_include_phase_a_values():
    assert "candidate" in V551J_PACKET_STATUSES
    assert "not_runtime_consumable" in V551J_RUNTIME_USE_CLASSES
    assert "runtime_safe_after_v552j" in V551J_RUNTIME_USE_CLASSES
    assert "exact_registry" in V551J_AUTHORITY_STATUSES
    assert "known_directional" in V551J_DIRECTIONALITY_STATUSES
    assert "joint_morphology_support" in V551J_FUTURE_TARGET_AFFORDANCES


def test_forbidden_claim_ids_non_empty():
    assert len(V551J_FORBIDDEN_CLAIM_IDS) >= 5
    assert "do_not_render_as_actor_orientation" in V551J_FORBIDDEN_CLAIM_IDS


def test_review_surface_schema_present():
    required = V551J_REVIEW_SURFACE_SCHEMA["required_columns"]
    assert "review_surface_status" in required
    assert "review_priority" in required
    assert "certification_candidate" in required
    assert "v551j_evidence_certification_status" in required
    assert "v552_handoff_readiness" in required
    assert "v552_context_status" in required
    assert "reviewable" in V551J_REVIEW_SURFACE_STATUSES
    assert "high" in V551J_REVIEW_PRIORITIES


def test_review_sidecar_schema_has_no_duplicate_required_columns():
    required = V551J_REVIEWABLE_EVIDENCE_SIDECAR_SCHEMA["required_columns"]
    assert len(required) == len(set(required))
