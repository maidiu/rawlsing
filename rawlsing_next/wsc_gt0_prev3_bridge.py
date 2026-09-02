"""WSC002D Golden Thread 0 FIELD FORGE -> PRE-V3 bridge.

GT0 F0 is only source-structure/current-J candidacy.  It is not an empirical
fact eligible for I04/P06 structural promotion.  Baseline execution therefore
preserves the exact upstream producer/replay surface and returns
UNDEFINED_FOR_OBJECT (or an already-owned narrower nonpositive I04/P06 result).
No V555 route is required and ZERO_V556_OBJECTS is lawful.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import importlib
import inspect
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, exact_ref, semantic_hash
from rawlsing_next.pre553_structural_admission import AdmissionEvaluation, POSITIVE_DECISION

CONTRACT_ID = "WSC002D_GT0_FIELD_FORGE_PREV3_BRIDGE@1.0.0"
STAGE_ID = "GT0_FIELD_FORGE_TO_PREV3"
GT0_F0_SOURCE_STRUCTURE_ID = "cssu.r1.afrobarometer.r1.005b474d6eb4253cb166"
GT0_BASELINE_TARGET_USE = "GT0_BASELINE_PREV3_STRUCTURAL_REQUEST"
INFORMATION_LOSS = "NONE__REFERENCE_PRESERVING"
ZERO_V556_MARKER = "ZERO_V556_OBJECTS"

_I04_TO_GT0_STATUS = {
    "MISSING_STRUCTURAL_ADMISSION_AUTHORITY": "BLOCKED_EXPLICIT_AUTHORITY",
    "UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY": "BLOCKED_EXPLICIT_AUTHORITY",
    "ADMISSION_DENIED": "DENIED",
    "NEGATIVE_AUTHORITY_ONLY": "DENIED",
    "SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE": "UNDEFINED_FOR_OBJECT",
    "EMPIRICAL_FACT_NONCOMPARABLE": "NONCOMPARABLE",
    "TEMPORAL_SCOPE_MISMATCH": "NONCOMPARABLE",
    "STRUCTURAL_TARGET_UNRESOLVED": "UNRESOLVED",
    "INSUFFICIENT_EVIDENCE_UNDER_RULE": "UNRESOLVED",
    "ADMISSION_DEFERRED": "UNRESOLVED",
    "VALID_EMPTY": "VALID_EMPTY",
    "INTEGRITY_FAILURE": "INTEGRITY_FAILURE",
}


class GT0Prev3BridgeError(ValueError):
    """The GT0 PRE-V3 boundary cannot be preserved exactly."""


@dataclass(frozen=True)
class GT0Prev3Result:
    conservation_envelope: Any
    stage_receipt: Any
    preserved_producer_ref: ExactRef
    structural_admission_ref: ExactRef | None
    v555_route_ref: ExactRef | None
    v556_object_refs: tuple[ExactRef, ...]
    disposition: str
    replay_ref: ExactRef


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GT0Prev3BridgeError(f"{name} must be non-empty text")
    out = value.strip()
    if out.lower() in {"latest", "default", "fuzzy", "nearest", "*"}:
        raise GT0Prev3BridgeError(f"{name} may not use mutable/fuzzy selection")
    return out


def _field(value: Any, *names: str, default: Any = None) -> Any:
    if isinstance(value, Mapping):
        for name in names:
            if name in value:
                return value[name]
    for name in names:
        if hasattr(value, name):
            return getattr(value, name)
    return default


def _eref(value: Any, name: str) -> ExactRef:
    if isinstance(value, ExactRef):
        return value
    if isinstance(value, Mapping) and {"kind", "object_id", "content_hash"}.issubset(value):
        return exact_ref({k: value[k] for k in ("kind", "object_id", "content_hash")}, name)
    for attr in ("ref", "receipt_ref", "object_ref", "producer_ref"):
        nested = getattr(value, attr, None)
        if nested is not None and nested is not value:
            try:
                return _eref(nested, name)
            except Exception:
                pass
    digest = _field(value, "content_hash", "receipt_hash")
    stage = _field(value, "stage_id", "stage")
    if isinstance(digest, str) and len(digest) == 64 and isinstance(stage, str):
        if digest.lower() != digest or any(ch not in "0123456789abcdef" for ch in digest):
            raise GT0Prev3BridgeError(f"{name} content hash is not exact sha256")
        return ExactRef(
            "GT0StageReceipt",
            f"urn:rawlsing:gt0:stage:{_text(stage, name + '.stage')}:sha256:{digest}",
            digest,
        )
    raise GT0Prev3BridgeError(f"{name} must expose exact kind/object_id/content_hash")


def _refs_if_declared(value: Any, *names: str) -> tuple[ExactRef, ...] | None:
    raw = _field(value, *names, default=None)
    if raw is None:
        return None
    if isinstance(raw, (str, bytes, bytearray)) or not isinstance(raw, Sequence):
        raise GT0Prev3BridgeError(f"{names[0]} must be an exact-ref sequence")
    return tuple(_eref(item, names[0]) for item in raw)


def _permissions(value: Any) -> tuple[str, ...]:
    raw = _field(
        value,
        "consumer_permission",
        "consumer_permissions",
        "permission_ceiling",
        "allowed_uses",
        default=(),
    )
    if raw is None:
        return ()
    if isinstance(raw, str):
        raw = (raw,)
    if isinstance(raw, (bytes, bytearray)) or not isinstance(raw, Sequence):
        raise GT0Prev3BridgeError("permission ceiling must be a sequence")
    return tuple(sorted({_text(item, "permission") for item in raw}))


def _owner(value: Any) -> str:
    raw = _field(value, "semantic_owner", "semantic_producer", "producer_owner", "owner")
    return (
        "UPSTREAM_PRODUCER_PRESERVED_BY_REFERENCE"
        if raw is None
        else _text(raw, "semantic_owner")
    )


def _upstream_state(value: Any) -> str:
    raw = _field(value, "typed_state", "status", "stage_status")
    if isinstance(raw, Enum):
        raw = raw.value
    return raw if isinstance(raw, str) and raw else "UPSTREAM_TYPED_STATE_PRESERVED"


def _validate_reference_closure(
    *,
    conservation_envelope: Any,
    upstream_receipt: Any,
    upstream_ref: ExactRef,
    producer_ref: ExactRef,
) -> None:
    receipt_producers = _refs_if_declared(upstream_receipt, "producer_refs", "producer_references")
    if receipt_producers is not None and producer_ref not in set(receipt_producers):
        raise GT0Prev3BridgeError("producer_ref is not declared by upstream receipt")
    envelope_upstream = _refs_if_declared(
        conservation_envelope, "upstream_receipt_refs", "upstream_refs"
    )
    if envelope_upstream is not None and upstream_ref not in set(envelope_upstream):
        raise GT0Prev3BridgeError("conservation envelope does not bind upstream receipt")
    envelope_producers = _refs_if_declared(
        conservation_envelope, "producer_refs", "producer_references"
    )
    if envelope_producers is not None and producer_ref not in set(envelope_producers):
        raise GT0Prev3BridgeError("conservation envelope does not bind producer ref")


def _admission_disposition(
    evaluation: AdmissionEvaluation | None,
) -> tuple[str, ExactRef | None, tuple[ExactRef, ...], str]:
    if evaluation is None:
        return (
            "UNDEFINED_FOR_OBJECT",
            None,
            (),
            "F0_SOURCE_STRUCTURE_CANDIDACY_HAS_NO_SUBSTANTIVE_PREV3_STRUCTURAL_SEMANTICS",
        )
    if not isinstance(evaluation, AdmissionEvaluation):
        raise GT0Prev3BridgeError("expected exact I04/P06 AdmissionEvaluation")
    if evaluation.decision_state == POSITIVE_DECISION:
        raise GT0Prev3BridgeError(
            "positive I04/P06 admission is outside WSC002D baseline; "
            "do not partially execute V554-V558"
        )
    status = _I04_TO_GT0_STATUS.get(evaluation.decision_state)
    if status is None:
        raise GT0Prev3BridgeError(
            f"unsupported I04/P06 decision {evaluation.decision_state!r}"
        )
    return (
        status,
        _eref(evaluation.receipt, "structural_admission_receipt"),
        tuple(sorted((_eref(x, "blocking_ref") for x in evaluation.blocking_refs), key=lambda r: r.key)),
        _text(evaluation.reason_code, "reason_code"),
    )


def _protocol_status(protocol: Any, name: str) -> Any:
    enum_type = getattr(protocol, "GT0StageStatus", None)
    if enum_type is None:
        raise GT0Prev3BridgeError("shared protocol lacks GT0StageStatus")
    try:
        return enum_type[name]
    except Exception:
        try:
            return enum_type(name)
        except Exception as exc:
            raise GT0Prev3BridgeError(f"shared protocol lacks status {name}") from exc


def _make_protocol_receipt(
    *,
    protocol: Any,
    envelope: Any,
    status_name: str,
    upstream_ref: ExactRef,
    producer_ref: ExactRef,
    owner: str,
    permission: tuple[str, ...],
    target_use: str,
    upstream_state: str,
    replay_ref: ExactRef,
    detail: Mapping[str, Any],
) -> Any:
    status = _protocol_status(protocol, status_name)
    receipt_hash = semantic_hash({
        "contract_id": CONTRACT_ID,
        "stage_id": STAGE_ID,
        "status": status_name,
        "detail": canonicalize(detail),
        "replay_ref": replay_ref.as_dict(),
    })
    values = {
        "stage_id": STAGE_ID,
        "stage": STAGE_ID,
        "status": status,
        "stage_status": status,
        "upstream_receipt_refs": (upstream_ref,),
        "upstream_refs": (upstream_ref,),
        "producer_refs": (producer_ref,),
        "producer_ref": producer_ref,
        "semantic_owner": owner,
        "semantic_producer": owner,
        "consumer_permission": permission,
        "permission_ceiling": permission,
        "typed_state": status_name,
        "target_use": target_use,
        "information_loss": INFORMATION_LOSS,
        "information_loss_declaration": INFORMATION_LOSS,
        "replay_ref": replay_ref,
        "replay_root": replay_ref,
        "details": detail,
        "detail": detail,
        "payload": detail,
        "content_hash": receipt_hash,
        "receipt_hash": receipt_hash,
        "conservation_envelope": envelope,
        "envelope": envelope,
        "upstream_typed_state": upstream_state,
    }
    receipt_type = getattr(protocol, "GT0StageReceipt", None)
    if receipt_type is None:
        raise GT0Prev3BridgeError("shared protocol lacks GT0StageReceipt")
    signature = inspect.signature(receipt_type)
    kwargs = {name: values[name] for name in signature.parameters if name in values}
    missing = [
        name
        for name, parameter in signature.parameters.items()
        if parameter.default is inspect._empty
        and parameter.kind not in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD)
        and name not in kwargs
    ]
    if missing:
        raise GT0Prev3BridgeError(
            "GT0StageReceipt integration fields unresolved: " + ", ".join(sorted(missing))
        )
    return receipt_type(**kwargs)


def run_gt0_prev3(
    *,
    conservation_envelope: Any,
    upstream_receipt: Any,
    producer_ref: ExactRef | Mapping[str, Any],
    target_use: str = GT0_BASELINE_TARGET_USE,
    requested_structural_meaning: str | None = None,
    structural_admission_evaluation: AdmissionEvaluation | None = None,
    protocol_module: Any | None = None,
) -> GT0Prev3Result:
    """Execute the GT0 FIELD FORGE -> PRE-V3 boundary without semantic inflation."""

    if conservation_envelope is None:
        raise GT0Prev3BridgeError("conservation_envelope is required")
    upstream_ref = _eref(upstream_receipt, "upstream_receipt")
    preserved_ref = _eref(producer_ref, "producer_ref")
    target = _text(target_use, "target_use")
    _validate_reference_closure(
        conservation_envelope=conservation_envelope,
        upstream_receipt=upstream_receipt,
        upstream_ref=upstream_ref,
        producer_ref=preserved_ref,
    )

    permission = _permissions(upstream_receipt) or _permissions(conservation_envelope)
    semantic_owner = _owner(upstream_receipt)
    upstream_state = _upstream_state(upstream_receipt)
    status_name, admission_ref, blockers, reason = _admission_disposition(
        structural_admission_evaluation
    )

    if requested_structural_meaning is not None:
        _text(requested_structural_meaning, "requested_structural_meaning")
        if structural_admission_evaluation is None:
            status_name = "BLOCKED_EXPLICIT_AUTHORITY"
            reason = "NAMED_SUBSTANTIVE_STRUCTURAL_MEANING_REQUIRES_EXACT_I04_P06_ADMISSION"

    detail = {
        "contract_id": CONTRACT_ID,
        "stage_id": STAGE_ID,
        "bound_seed_identity": GT0_F0_SOURCE_STRUCTURE_ID,
        "seed_authority_ceiling": "SOURCE_STRUCTURE_CURRENT_J_CANDIDACY_ONLY",
        "upstream_receipt_ref": upstream_ref.as_dict(),
        "preserved_producer_ref": preserved_ref.as_dict(),
        "semantic_owner": semantic_owner,
        "permission_ceiling": list(permission),
        "upstream_typed_state": upstream_state,
        "target_use": target,
        "disposition": status_name,
        "reason_code": reason,
        "structural_admission_ref": admission_ref.as_dict() if admission_ref else None,
        "blocking_refs": [ref.as_dict() for ref in blockers],
        "substantive_structure_minted": False,
        "v555_route_ref": None,
        "v556_object_refs": [],
        "v556_disposition": ZERO_V556_MARKER,
        "producer_reowned": False,
        "permission_widened": False,
        "actor_state_minted": False,
        "information_loss": INFORMATION_LOSS,
    }
    replay_hash = semantic_hash(canonicalize(detail))
    replay_ref = ExactRef(
        "GT0Prev3ReplayRoot",
        f"urn:rawlsing:wsc002d:prev3-replay:sha256:{replay_hash}",
        replay_hash,
    )

    protocol = protocol_module
    if protocol is None:
        try:
            protocol = importlib.import_module("rawlsing_next.wsc_gt0_protocol")
        except ModuleNotFoundError as exc:
            raise GT0Prev3BridgeError(
                "WSC002A shared protocol is required at integration time"
            ) from exc

    receipt = _make_protocol_receipt(
        protocol=protocol,
        envelope=conservation_envelope,
        status_name=status_name,
        upstream_ref=upstream_ref,
        producer_ref=preserved_ref,
        owner=semantic_owner,
        permission=permission,
        target_use=target,
        upstream_state=upstream_state,
        replay_ref=replay_ref,
        detail=detail,
    )

    returned_status = _field(receipt, "status", "stage_status", "typed_state")
    if isinstance(returned_status, Enum):
        returned_status = returned_status.value
    if isinstance(returned_status, str) and returned_status != status_name:
        raise GT0Prev3BridgeError("protocol receipt changed exact PRE-V3 disposition")
    returned_permission = _permissions(receipt)
    if returned_permission and not set(returned_permission).issubset(set(permission)):
        raise GT0Prev3BridgeError("protocol receipt widened upstream permission")

    return GT0Prev3Result(
        conservation_envelope=conservation_envelope,
        stage_receipt=receipt,
        preserved_producer_ref=preserved_ref,
        structural_admission_ref=admission_ref,
        v555_route_ref=None,
        v556_object_refs=(),
        disposition=status_name,
        replay_ref=replay_ref,
    )


__all__ = [
    "CONTRACT_ID",
    "STAGE_ID",
    "GT0_F0_SOURCE_STRUCTURE_ID",
    "GT0_BASELINE_TARGET_USE",
    "INFORMATION_LOSS",
    "ZERO_V556_MARKER",
    "GT0Prev3BridgeError",
    "GT0Prev3Result",
    "run_gt0_prev3",
]
