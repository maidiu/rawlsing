from dataclasses import dataclass, replace
from enum import Enum

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.wsc_gt0_source_preff import (
    F0_ADMITTED_UPSTREAM_GIT_SHA,
    F0_CANDIDACY,
    F0_EXECUTABLE_J_CEILING,
    F0_INFORMATION_LOSS,
    F0_MEMBERS,
    F0_MINIMAL_GOVERNED_FIXTURE,
    F0_R2_IDENTITY_SHA256,
    F0_SOURCE_STRUCTURE_ID,
    GT0SourcePreFFError,
    bind_gt0_f0,
    run_gt0_preff,
)


class _Status(Enum):
    PASS = "PASS"


@dataclass(frozen=True)
class _Envelope:
    stage_id: str
    semantic_owner: str
    producer_refs: tuple[ExactRef, ...]
    upstream_refs: tuple[str, ...]
    scope_ref: str
    permission_ceiling: str
    typed_state: str
    dependency_refs: tuple[str, ...]
    information_loss: str
    replay_hash: str
    payload_hash: str
    metadata: dict


@dataclass(frozen=True)
class _Receipt:
    stage_id: str
    status: _Status
    semantic_owner: str
    producer_refs: tuple[ExactRef, ...]
    upstream_refs: tuple[str, ...]
    input_envelope_hash: str | None
    output_envelope_hash: str
    replay_hash: str
    details: dict
    receipt_hash: str


class _Protocol:
    """Independent common-candidate API double; no sibling WSC002 code consumed."""

    GT0StageStatus = _Status
    GT0ConservationEnvelope = _Envelope
    GT0StageReceipt = _Receipt


def test_bind_gt0_f0_verifies_exact_governed_seed_without_respondent_values():
    result = bind_gt0_f0(protocol=_Protocol)
    assert result.producer_ref.object_id == F0_SOURCE_STRUCTURE_ID
    assert result.producer_ref.content_hash == F0_R2_IDENTITY_SHA256
    assert result.envelope.stage_id == "GT0_F0_BINDING"
    assert result.envelope.semantic_owner == "J01A_CURRENT_JOINT_SOURCE_CANDIDACY"
    assert result.envelope.typed_state == F0_CANDIDACY
    assert result.envelope.metadata["members"] == F0_MEMBERS
    assert result.envelope.metadata["executable_j_authorized"] is False
    assert result.envelope.metadata["respondent_values_present"] is False
    assert result.receipt.status is _Status.PASS
    assert result.receipt.details["authority_ceiling"] == F0_EXECUTABLE_J_CEILING


def test_preff_preserves_owner_permission_reference_and_candidate_ceiling():
    bound = bind_gt0_f0(protocol=_Protocol)
    preff = run_gt0_preff(bound, protocol=_Protocol)
    assert preff.producer_ref == bound.producer_ref
    assert preff.envelope.semantic_owner == bound.envelope.semantic_owner
    assert preff.envelope.permission_ceiling == bound.envelope.permission_ceiling
    assert preff.envelope.upstream_refs == (
        F0_ADMITTED_UPSTREAM_GIT_SHA,
        bound.producer_ref.key,
    )
    assert preff.envelope.information_loss == F0_INFORMATION_LOSS
    assert preff.receipt.details["producer_ownership_transferred"] is False
    assert preff.receipt.details["executable_j_authorized"] is False
    assert preff.receipt.details["respondent_values_read"] is False
    assert preff.receipt.details["respondent_values_fabricated"] is False
    assert preff.receipt.details["joint_distribution_asserted"] is False
    assert preff.receipt.details["measurement_portability_asserted"] is False


def test_binding_fails_closed_on_any_governed_seed_tamper():
    bad = dict(F0_MINIMAL_GOVERNED_FIXTURE)
    bad["source_native_member_identities"] = "pfesol|pfrsay"
    with pytest.raises(GT0SourcePreFFError, match="source_native_member_identities"):
        bind_gt0_f0(bad, protocol=_Protocol)


def test_current_j_candidate_never_self_promotes_to_executable_j():
    bound = bind_gt0_f0(protocol=_Protocol)
    preff = run_gt0_preff(bound, protocol=_Protocol)
    assert preff.envelope.typed_state == "CURRENT_J_CANDIDATE"
    assert preff.envelope.metadata["authority_ceiling"] == (
        "CURRENT_J_CANDIDATE != EXECUTABLE_J"
    )
    assert preff.receipt.details["operation"] == "PRODUCER_PRESERVING_REFERENCE_ONLY"


def test_replay_hashes_are_deterministic_and_stage_specific():
    first = bind_gt0_f0(protocol=_Protocol)
    second = bind_gt0_f0(protocol=_Protocol)
    assert first.replay_hash == second.replay_hash
    assert first.envelope_hash == second.envelope_hash
    assert first.receipt.receipt_hash == second.receipt.receipt_hash

    preff_a = run_gt0_preff(first, protocol=_Protocol)
    preff_b = run_gt0_preff(second, protocol=_Protocol)
    assert preff_a.replay_hash == preff_b.replay_hash
    assert preff_a.envelope_hash == preff_b.envelope_hash
    assert preff_a.receipt.receipt_hash == preff_b.receipt.receipt_hash
    assert preff_a.envelope_hash != first.envelope_hash


def test_preff_rejects_substituted_producer_reference():
    bound = bind_gt0_f0(protocol=_Protocol)
    substituted = replace(
        bound,
        producer_ref=ExactRef(
            kind=bound.producer_ref.kind,
            object_id="cssu.r1.afrobarometer.r1.not-f0",
            content_hash=bound.producer_ref.content_hash,
        ),
    )
    with pytest.raises((GT0SourcePreFFError, AssertionError)):
        run_gt0_preff(substituted, protocol=_Protocol)
