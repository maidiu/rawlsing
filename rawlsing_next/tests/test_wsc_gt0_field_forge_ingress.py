import hashlib
import json
import sys
import types
from dataclasses import asdict, dataclass
from enum import Enum

import pytest

from rawlsing_next.wsc_gt0_field_forge_ingress import (
    GT0FieldForgeIngressError,
    INFORMATION_LOSS,
    STAGE_ID,
    run_gt0_field_forge_ingress,
)


def _h(label):
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


class _Status(str, Enum):
    PASS = "PASS"
    OBSERVED_ZERO = "OBSERVED_ZERO"
    VALID_EMPTY = "VALID_EMPTY"
    UNDEFINED_FOR_OBJECT = "UNDEFINED_FOR_OBJECT"
    BLOCKED_EXPLICIT_AUTHORITY = "BLOCKED_EXPLICIT_AUTHORITY"
    NONCOMPARABLE = "NONCOMPARABLE"
    UNRESOLVED = "UNRESOLVED"
    DENIED = "DENIED"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"


@dataclass(frozen=True)
class _Envelope:
    object_id: str
    object_type: str
    semantic_owner: str
    scope: object
    consumer_permission: tuple[str, ...]
    typed_state: str
    relation_query_identity: object
    replay_recipe: object
    information_loss_declaration: str
    target_use: str


@dataclass(frozen=True)
class _Receipt:
    contract_id: str
    stage_id: str
    status: _Status
    upstream_refs: tuple[dict[str, str], ...]
    output_refs: tuple[dict[str, str], ...]
    input_envelope_hash: str
    output_envelope_hash: str
    semantic_owner: str
    scope: object
    consumer_permission: tuple[str, ...]
    typed_state: str
    replay_recipe: object
    information_loss_declaration: str
    target_use: str
    details: object
    receipt_id: str
    content_hash: str


def _plain(value):
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "__dataclass_fields__"):
        return {k: _plain(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_plain(v) for v in value]
    return value


def _digest(value):
    body = json.dumps(
        _plain(value),
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _validate_refs(refs):
    for ref in refs:
        assert set(ref) == {"kind", "object_id", "content_hash"}
        assert len(ref["content_hash"]) == 64
    return tuple(refs)


@pytest.fixture
def protocol(monkeypatch):
    module = types.ModuleType("rawlsing_next.wsc_gt0_protocol")
    module.GT0StageStatus = _Status
    module.GT0ConservationEnvelope = _Envelope
    module.GT0StageReceipt = _Receipt
    module.deterministic_content_hash = _digest
    module.validate_exact_upstream_refs = _validate_refs
    monkeypatch.setitem(sys.modules, "rawlsing_next.wsc_gt0_protocol", module)
    return module


def _ref(tag="f0"):
    return {
        "kind": "CURRENT_SOURCE_STRUCTURE_CANDIDATE",
        "object_id": "cssu.r1.afrobarometer.r1.005b474d6eb4253cb166",
        "content_hash": _h("exact-" + tag),
    }


def _envelope(**updates):
    data = dict(
        object_id="cssu.r1.afrobarometer.r1.005b474d6eb4253cb166",
        object_type="CURRENT_SOURCE_STRUCTURE_CANDIDATE",
        semantic_owner="J01-A_CURRENT_SOURCE_STRUCTURE",
        scope={
            "source": "AFROBAROMETER",
            "structure_type": "MATRIX_GRID",
            "members": (
                "pfesol", "pfrsay", "pfrass", "pfrvot", "pfreql", "pfpsaf",
            ),
        },
        consumer_permission=("REFERENCE", "QUERY_IF_SEPARATELY_AUTHORIZED"),
        typed_state="PASS",
        relation_query_identity={
            "kind": "SOURCE_STRUCTURE_REFERENCE",
            "label": "Current-versus-past freedoms and equality",
        },
        replay_recipe={
            "immutable_ref": "ba23b0fc1d22bb35abb8a6e8f9ab6100df8f7564",
            "selection": "EXACT",
        },
        information_loss_declaration=INFORMATION_LOSS,
        target_use="GT0_FIELD_FORGE_INGRESS_REFERENCE",
    )
    data.update(updates)
    return _Envelope(**data)


def _preff_receipt(refs, *, status=_Status.PASS, envelope=None):
    envelope = envelope or _envelope()
    eh = _digest(envelope)
    material = dict(
        contract_id="TEST_PREFF@1",
        stage_id="GT0_PREFF",
        status=status,
        upstream_refs=tuple(refs),
        output_refs=tuple(refs),
        input_envelope_hash=eh,
        output_envelope_hash=eh,
        semantic_owner=envelope.semantic_owner,
        scope=envelope.scope,
        consumer_permission=envelope.consumer_permission,
        typed_state=envelope.typed_state,
        replay_recipe=envelope.replay_recipe,
        information_loss_declaration=envelope.information_loss_declaration,
        target_use=envelope.target_use,
        details={"current_j_candidate_not_executable_j": True},
    )
    digest = _digest(material)
    return _Receipt(
        **material,
        receipt_id="urn:test:preff:" + digest,
        content_hash=digest,
    )


def test_reference_preserving_ingress_returns_same_envelope_and_exact_refs(protocol):
    ref = _ref()
    envelope = _envelope()
    preff = _preff_receipt((ref,), envelope=envelope)

    out_envelope, receipt = run_gt0_field_forge_ingress(envelope, preff, (ref,))

    assert out_envelope is envelope
    assert receipt.stage_id == STAGE_ID
    assert receipt.status is _Status.PASS
    assert receipt.semantic_owner == envelope.semantic_owner
    assert receipt.scope == envelope.scope
    assert receipt.consumer_permission == envelope.consumer_permission
    assert receipt.typed_state == envelope.typed_state
    assert receipt.replay_recipe == envelope.replay_recipe
    assert receipt.information_loss_declaration == INFORMATION_LOSS
    assert receipt.upstream_refs == (ref,)
    assert receipt.output_refs == (ref,)
    assert receipt.input_envelope_hash == receipt.output_envelope_hash == _digest(envelope)
    assert receipt.details["new_field_forge_relation_minted"] is False
    assert receipt.details["strong_noun_admission_minted"] is False
    assert receipt.details["actor_semantics_minted"] is False


@pytest.mark.parametrize("status", [_Status.OBSERVED_ZERO, _Status.VALID_EMPTY, _Status.NONCOMPARABLE])
def test_typed_nonpositive_stage_status_is_preserved(protocol, status):
    ref = _ref(status.value)
    envelope = _envelope(typed_state=status.value)
    preff = _preff_receipt((ref,), status=status, envelope=envelope)

    _, receipt = run_gt0_field_forge_ingress(envelope, preff, (ref,))

    assert receipt.status is status
    assert receipt.typed_state == status.value
    assert receipt.details["typed_state_preserved"] is True


def test_replay_is_deterministic(protocol):
    ref = _ref()
    envelope = _envelope()
    preff = _preff_receipt((ref,), envelope=envelope)

    first = run_gt0_field_forge_ingress(envelope, preff, (ref,))[1]
    second = run_gt0_field_forge_ingress(envelope, preff, (ref,))[1]

    assert first == second
    assert first.content_hash == second.content_hash
    assert first.receipt_id == second.receipt_id


def test_rejects_non_reference_preserving_information_loss(protocol):
    ref = _ref()
    envelope = _envelope(information_loss_declaration="LOSSY_SUMMARY")
    preff = _preff_receipt((ref,), envelope=envelope)

    with pytest.raises(GT0FieldForgeIngressError, match="information-loss"):
        run_gt0_field_forge_ingress(envelope, preff, (ref,))


@pytest.mark.parametrize(
    "claim",
    [
        {"semantic_family": "FIELD"},
        {"semantic_family": "FIELD_SPECIFIC_CAPITAL"},
        {"semantic_family": "HEGEMONY"},
        {"semantic_family": "HOMOLOGY"},
        {"semantic_family": "PRESSURE_PATHWAY"},
        {"semantic_family": "STRUCTURAL_MECHANISM"},
    ],
)
def test_rejects_strong_noun_promotion(protocol, claim):
    ref = _ref("strong")
    envelope = _envelope(relation_query_identity=claim)
    preff = _preff_receipt((ref,), envelope=envelope)

    with pytest.raises(GT0FieldForgeIngressError, match="strong FIELD FORGE nouns"):
        run_gt0_field_forge_ingress(envelope, preff, (ref,))


def test_rejects_upstream_ref_mismatch(protocol):
    ref = _ref("one")
    other = _ref("two")
    envelope = _envelope()
    preff = _preff_receipt((ref,), envelope=envelope)

    with pytest.raises(GT0FieldForgeIngressError, match="do not match PRE-FF receipt"):
        run_gt0_field_forge_ingress(envelope, preff, (other,))


def test_rejects_mutable_or_inexact_ref(protocol):
    envelope = _envelope()
    bad = {
        "kind": "CURRENT_SOURCE_STRUCTURE_CANDIDATE",
        "object_id": "latest",
        "content_hash": "not-a-sha",
    }
    preff = _preff_receipt((_ref(),), envelope=envelope)

    with pytest.raises(GT0FieldForgeIngressError):
        run_gt0_field_forge_ingress(envelope, preff, (bad,))
