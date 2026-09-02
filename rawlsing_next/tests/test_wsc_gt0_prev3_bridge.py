from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
from types import SimpleNamespace
from typing import Any, Mapping

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.wsc_gt0_prev3_bridge import (
    GT0Prev3BridgeError,
    INFORMATION_LOSS,
    STAGE_ID,
    ZERO_V556_MARKER,
    run_gt0_prev3,
)


def _sha(seed: str) -> str:
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def _ref(kind: str, seed: str) -> ExactRef:
    digest = _sha(seed)
    return ExactRef(kind, f"urn:test:{kind}:{digest}", digest)


class _Status(str, Enum):
    PASS = "PASS"
    OBSERVED_ZERO = "OBSERVED_ZERO"
    VALID_EMPTY = "VALID_EMPTY"
    UNDEFINED_FOR_OBJECT = "UNDEFINED_FOR_OBJECT"
    BLOCKED_EXPLICIT_AUTHORITY = "BLOCKED_EXPLICIT_AUTHORITY"
    BLOCKED_COMPARATOR_ANCESTRY = "BLOCKED_COMPARATOR_ANCESTRY"
    BLOCKED_POSITIVE_TRANSITION_AUTHORITY = "BLOCKED_POSITIVE_TRANSITION_AUTHORITY"
    BLOCKED_NAMED_AUTHORITY_REQUIRED = "BLOCKED_NAMED_AUTHORITY_REQUIRED"
    NONCOMPARABLE = "NONCOMPARABLE"
    UNRESOLVED = "UNRESOLVED"
    DENIED = "DENIED"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"


@dataclass(frozen=True)
class _Receipt:
    stage_id: str
    status: _Status
    upstream_receipt_refs: tuple[ExactRef, ...]
    producer_refs: tuple[ExactRef, ...]
    semantic_owner: str
    permission_ceiling: tuple[str, ...]
    typed_state: str
    target_use: str
    information_loss: str
    replay_ref: ExactRef
    details: Mapping[str, Any]
    content_hash: str

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            "GT0StageReceipt",
            f"urn:test:gt0-stage:{self.stage_id}:sha256:{self.content_hash}",
            self.content_hash,
        )


@dataclass(frozen=True)
class _Upstream:
    receipt_ref: ExactRef
    producer_refs: tuple[ExactRef, ...]
    semantic_owner: str
    permission_ceiling: tuple[str, ...]
    typed_state: str


@dataclass(frozen=True)
class _Envelope:
    upstream_receipt_refs: tuple[ExactRef, ...]
    producer_refs: tuple[ExactRef, ...]
    permission_ceiling: tuple[str, ...]


_PROTOCOL = SimpleNamespace(GT0StageStatus=_Status, GT0StageReceipt=_Receipt)


def _inputs():
    producer = _ref("FieldForgeIngressReference", "producer")
    upstream_ref = _ref("GT0StageReceipt", "upstream")
    upstream = _Upstream(
        receipt_ref=upstream_ref,
        producer_refs=(producer,),
        semantic_owner="FIELD_FORGE_UPSTREAM_PRODUCER",
        permission_ceiling=("REVIEW",),
        typed_state="REFERENCE_PRESERVED",
    )
    envelope = _Envelope(
        upstream_receipt_refs=(upstream_ref,),
        producer_refs=(producer,),
        permission_ceiling=("REVIEW",),
    )
    return envelope, upstream, producer


def test_f0_baseline_is_undefined_and_mints_no_structure():
    envelope, upstream, producer = _inputs()

    result = run_gt0_prev3(
        conservation_envelope=envelope,
        upstream_receipt=upstream,
        producer_ref=producer,
        protocol_module=_PROTOCOL,
    )

    assert result.disposition == "UNDEFINED_FOR_OBJECT"
    assert result.preserved_producer_ref == producer
    assert result.structural_admission_ref is None
    assert result.v555_route_ref is None
    assert result.v556_object_refs == ()

    receipt = result.stage_receipt
    assert receipt.stage_id == STAGE_ID
    assert receipt.status is _Status.UNDEFINED_FOR_OBJECT
    assert receipt.producer_refs == (producer,)
    assert receipt.semantic_owner == upstream.semantic_owner
    assert receipt.permission_ceiling == ("REVIEW",)
    assert receipt.information_loss == INFORMATION_LOSS
    assert receipt.details["substantive_structure_minted"] is False
    assert receipt.details["actor_state_minted"] is False
    assert receipt.details["v555_route_ref"] is None
    assert receipt.details["v556_object_refs"] == []
    assert receipt.details["v556_disposition"] == ZERO_V556_MARKER


def test_named_substantive_request_blocks_without_i04_p06_admission():
    envelope, upstream, producer = _inputs()

    result = run_gt0_prev3(
        conservation_envelope=envelope,
        upstream_receipt=upstream,
        producer_ref=producer,
        requested_structural_meaning="STRUCTURAL_PRESSURE",
        protocol_module=_PROTOCOL,
    )

    assert result.disposition == "BLOCKED_EXPLICIT_AUTHORITY"
    assert result.stage_receipt.status is _Status.BLOCKED_EXPLICIT_AUTHORITY
    assert (
        result.stage_receipt.details["reason_code"]
        == "NAMED_SUBSTANTIVE_STRUCTURAL_MEANING_REQUIRES_EXACT_I04_P06_ADMISSION"
    )
    assert result.v555_route_ref is None
    assert result.v556_object_refs == ()


def test_replay_identity_is_deterministic():
    envelope, upstream, producer = _inputs()

    left = run_gt0_prev3(
        conservation_envelope=envelope,
        upstream_receipt=upstream,
        producer_ref=producer,
        protocol_module=_PROTOCOL,
    )
    right = run_gt0_prev3(
        conservation_envelope=envelope,
        upstream_receipt=upstream,
        producer_ref=producer,
        protocol_module=_PROTOCOL,
    )

    assert left.replay_ref == right.replay_ref
    assert left.stage_receipt.content_hash == right.stage_receipt.content_hash


def test_upstream_receipt_cannot_claim_different_producer():
    envelope, upstream, _producer = _inputs()
    wrong = _ref("FieldForgeIngressReference", "wrong-producer")

    with pytest.raises(GT0Prev3BridgeError, match="not declared by upstream receipt"):
        run_gt0_prev3(
            conservation_envelope=envelope,
            upstream_receipt=upstream,
            producer_ref=wrong,
            protocol_module=_PROTOCOL,
        )


def test_envelope_must_bind_exact_upstream_receipt():
    envelope, upstream, producer = _inputs()
    bad_envelope = _Envelope(
        upstream_receipt_refs=(_ref("GT0StageReceipt", "different-upstream"),),
        producer_refs=(producer,),
        permission_ceiling=("REVIEW",),
    )

    with pytest.raises(GT0Prev3BridgeError, match="does not bind upstream receipt"):
        run_gt0_prev3(
            conservation_envelope=bad_envelope,
            upstream_receipt=upstream,
            producer_ref=producer,
            protocol_module=_PROTOCOL,
        )


def test_mutable_or_fuzzy_target_use_is_rejected():
    envelope, upstream, producer = _inputs()

    with pytest.raises(GT0Prev3BridgeError, match="mutable/fuzzy"):
        run_gt0_prev3(
            conservation_envelope=envelope,
            upstream_receipt=upstream,
            producer_ref=producer,
            target_use="latest",
            protocol_module=_PROTOCOL,
        )
