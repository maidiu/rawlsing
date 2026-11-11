import dataclasses

import pytest

from rawlsing_next.wsc_gt0_protocol import (
    GT0ConservationEnvelope,
    GT0ExactRef,
    GT0IntegrityError,
    GT0PermissionError,
    GT0ReferenceError,
    GT0StageReceipt,
    GT0StageStatus,
    assert_permission_narrowing,
    gt0_content_hash,
    validate_exact_upstream_ref,
)


F0 = "cssu.r1.afrobarometer.r1.005b474d6eb4253cb166"
J01 = "ba23b0fc1d22bb35abb8a6e8f9ab6100df8f7564"
ZERO = "0" * 64
ONE = "1" * 64


def ref(kind, value, content_hash=None):
    return GT0ExactRef(kind, value, content_hash)


def envelope(status=GT0StageStatus.PASS, permissions=("READ_SOURCE_STRUCTURE",)):
    return GT0ConservationEnvelope(
        semantic_owner_ref=ref("J01_A_CURRENT_SOURCE_OWNER", J01),
        object_refs=(ref("CURRENT_SOURCE_STRUCTURE", F0),),
        authority_refs=(ref("GIT_COMMIT", J01),),
        current_selection_refs=(ref("GIT_COMMIT", J01),),
        scope_refs=(ref("SOURCE_SCOPE", "rawlsing:afrobarometer:r1"),),
        relation_query_refs=(),
        permission_ceiling=permissions,
        status=status,
        dependency_refs=(ref("GIT_COMMIT", J01),),
        provenance_refs=(ref("GIT_COMMIT", J01),),
        replay_refs=(ref("REPLAY_ROOT", "urn:rawlsing:gt0:fixture", ZERO),),
        information_loss="NONE__REFERENCE_PRESERVING",
    )


def test_required_status_surface_is_frozen():
    required = {
        "PASS",
        "OBSERVED_ZERO",
        "VALID_EMPTY",
        "UNDEFINED_FOR_OBJECT",
        "BLOCKED_EXPLICIT_AUTHORITY",
        "BLOCKED_COMPARATOR_ANCESTRY",
        "BLOCKED_POSITIVE_TRANSITION_AUTHORITY",
        "BLOCKED_NAMED_AUTHORITY_REQUIRED",
        "NONCOMPARABLE",
        "UNRESOLVED",
        "DENIED",
        "INTEGRITY_FAILURE",
    }
    assert required <= {status.value for status in GT0StageStatus}


def test_hash_is_deterministic_and_mapping_order_independent():
    left = {"b": [2, 1], "a": {"x": "y"}}
    right = {"a": {"x": "y"}, "b": [2, 1]}
    assert gt0_content_hash(left) == gt0_content_hash(right)
    assert len(gt0_content_hash(left)) == 64
    with pytest.raises(GT0IntegrityError):
        gt0_content_hash({"forbidden_float": 1.5})


def test_exact_reference_validation_accepts_pre553_shape_and_rejects_fallbacks():
    pre553_shape = {
        "kind": "EmpiricalFact@1.0.0",
        "object_id": "urn:rawlsing:fact:1",
        "content_hash": ZERO,
    }
    got = validate_exact_upstream_ref(pre553_shape)
    assert got.kind == "EmpiricalFact@1.0.0"
    assert got.value == "urn:rawlsing:fact:1"
    assert got.content_hash == ZERO

    assert validate_exact_upstream_ref(J01).value == J01
    assert validate_exact_upstream_ref(F0).value == F0

    for bad in ("latest", "default", "urn:rawlsing:latest:thing", "foo/default/bar", "*"):
        with pytest.raises(GT0ReferenceError):
            validate_exact_upstream_ref(bad)

    with pytest.raises(GT0ReferenceError):
        validate_exact_upstream_ref("untyped-bare-token")


def test_envelope_is_immutable_hashable_and_reference_preserving():
    env = envelope()
    assert env.semantic_owner_ref.value == J01
    assert env.object_refs[0].value == F0
    clone = GT0ConservationEnvelope(
        semantic_owner_ref=env.semantic_owner_ref,
        object_refs=tuple(reversed(env.object_refs)),
        authority_refs=tuple(reversed(env.authority_refs)),
        current_selection_refs=env.current_selection_refs,
        scope_refs=env.scope_refs,
        permission_ceiling=tuple(reversed(env.permission_ceiling)),
        status=env.status,
        dependency_refs=env.dependency_refs,
        provenance_refs=env.provenance_refs,
        replay_refs=env.replay_refs,
        information_loss=env.information_loss,
    )
    assert env.content_hash == clone.content_hash
    assert isinstance(hash(env), int)
    with pytest.raises(dataclasses.FrozenInstanceError):
        env.status = GT0StageStatus.DENIED


def test_permission_ceiling_can_narrow_but_not_widen():
    upstream = ("READ_SOURCE_STRUCTURE", "QUERY_EXACT")
    assert assert_permission_narrowing(upstream, ("QUERY_EXACT",)) == ("QUERY_EXACT",)
    with pytest.raises(GT0PermissionError):
        assert_permission_narrowing(upstream, ("QUERY_EXACT", "STRUCTURAL_PROMOTION"))


def test_stage_receipt_hashes_output_and_exact_upstreams_without_owner_transfer():
    env = envelope(status=GT0StageStatus.UNDEFINED_FOR_OBJECT)
    receipt = GT0StageReceipt(
        stage_id="GT0_PREV3",
        status=GT0StageStatus.UNDEFINED_FOR_OBJECT,
        input_envelope_hashes=(ONE,),
        output_envelope=env,
        upstream_refs=(ref("CURRENT_SOURCE_STRUCTURE", F0),),
        authority_refs=(ref("GIT_COMMIT", J01),),
        replay_refs=env.replay_refs,
        detail_code="F0_SOURCE_STRUCTURE_HAS_NO_SUBSTANTIVE_STRUCTURAL_ADMISSION",
    )
    assert receipt.output_envelope.semantic_owner_ref == env.semantic_owner_ref
    assert receipt.identity_material()["output_envelope_hash"] == env.content_hash
    assert len(receipt.content_hash) == 64
    assert isinstance(hash(receipt), int)

    same = GT0StageReceipt(
        stage_id="GT0_PREV3",
        status="UNDEFINED_FOR_OBJECT",
        input_envelope_hashes=(ONE,),
        output_envelope=env,
        upstream_refs=(ref("CURRENT_SOURCE_STRUCTURE", F0),),
        authority_refs=(ref("GIT_COMMIT", J01),),
        replay_refs=env.replay_refs,
        detail_code="F0_SOURCE_STRUCTURE_HAS_NO_SUBSTANTIVE_STRUCTURAL_ADMISSION",
    )
    assert same == receipt
    assert same.content_hash == receipt.content_hash


def test_stage_receipt_rejects_status_drift_and_non_sha256_input_envelope_hash():
    env = envelope(status=GT0StageStatus.PASS)
    with pytest.raises(GT0IntegrityError):
        GT0StageReceipt(
            stage_id="BAD_STATUS",
            status=GT0StageStatus.DENIED,
            input_envelope_hashes=(ZERO,),
            output_envelope=env,
        )
    with pytest.raises(GT0IntegrityError):
        GT0StageReceipt(
            stage_id="BAD_HASH",
            status=GT0StageStatus.PASS,
            input_envelope_hashes=("f" * 40,),
            output_envelope=env,
        )


def test_information_loss_and_status_participate_in_envelope_identity():
    pass_env = envelope(status=GT0StageStatus.PASS)
    blocked_env = envelope(status=GT0StageStatus.UNRESOLVED)
    assert pass_env.content_hash != blocked_env.content_hash

    lossy = GT0ConservationEnvelope(
        semantic_owner_ref=pass_env.semantic_owner_ref,
        object_refs=pass_env.object_refs,
        authority_refs=pass_env.authority_refs,
        current_selection_refs=pass_env.current_selection_refs,
        scope_refs=pass_env.scope_refs,
        permission_ceiling=pass_env.permission_ceiling,
        status=pass_env.status,
        dependency_refs=pass_env.dependency_refs,
        provenance_refs=pass_env.provenance_refs,
        replay_refs=pass_env.replay_refs,
        information_loss="LOSS_DECLARED__TEST_ONLY",
    )
    assert lossy.content_hash != pass_env.content_hash
