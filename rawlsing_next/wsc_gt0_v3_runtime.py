"""Golden Thread 0 PRE-V3 -> V3 zero-effect runtime candidate.

This module implements only WSC002E.  It deliberately does not create a
predicate/comparator authority, PSEPF support, developmental rule, actor fact,
or positive transition authority.

The baseline GT0 path is a conservation proof: nonpositive PRE-V3 material is
preserved by exact reference, any actual positioned-subject possibility remains
learned-world evidence, and V3 state/ledger/RNG/scheduler stay unchanged.

The shared WSC002 protocol module is a sibling implementation and therefore is
not imported at module import time on this independent branch.  The stage binds
it lazily at execution time, or accepts an explicit protocol module test double.
Central integration can therefore supply ``rawlsing_next.wsc_gt0_protocol``
without this worker consuming the sibling branch.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from importlib import import_module
import inspect
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.source_backed_positioned_subject_possibility import (
    PositionedSubjectPossibilityResult,
)
from rawlsing_next.v3_psepf_zero_positive_guard import (
    GuardOutcome,
    evaluate_psepf_zero_positive_guard,
)

GT0_V3_RUNTIME_CONTRACT_ID = "WSC002E_GT0_PREV3_V3_ZERO_EFFECT_RUNTIME@1.0.0"
GT0_V3_STAGE_ID = "PREV3_V3"
GT0_V3_CONTROL_OWNER = "V3_GENERATED_PERSON_RUNTIME_CONTROL"
GT0_V3_PERMISSION_CEILING = "ZERO_EFFECT_ONLY__NO_ACTOR_MUTATION"
GT0_V3_TRANSITION_SURFACE = "GT0.PREV3_TO_V3"
GT0_V3_OPERATION_CLASS = "GT0_BASELINE_TRANSITION_PROPOSAL"

_ALLOWED_STAGE_STATUSES = frozenset(
    {
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
)
_FORBIDDEN_SELECTORS = frozenset({"latest", "default", "nearest", "fuzzy", "*"})


class GT0V3RuntimeIntegrityError(ValueError):
    """The GT0 V3 stage cannot establish exact identity/protocol closure."""


class GT0ProtocolIntegrationError(GT0V3RuntimeIntegrityError):
    """The shared WSC002 protocol surface is absent or constructor-incompatible."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GT0V3RuntimeIntegrityError(f"{name} must be a non-empty string")
    out = value.strip()
    if out.lower() in _FORBIDDEN_SELECTORS:
        raise GT0V3RuntimeIntegrityError(f"{name} may not use mutable/fuzzy selector {out!r}")
    return out


def _status_name(value: Any) -> str:
    if isinstance(value, Enum):
        value = value.value
    return _text(str(value), "stage_status")


def _stable_ref(value: Any, name: str) -> str:
    """Return an exact stable reference without inventing semantic ownership."""

    if isinstance(value, str):
        return _text(value, name)

    for attr in ("ref", "receipt_ref", "object_ref", "stage_ref"):
        if hasattr(value, attr):
            ref = getattr(value, attr)
            if ref is value:
                continue
            if hasattr(ref, "key"):
                return _text(str(ref.key), name)
            if isinstance(ref, str):
                return _text(ref, name)

    for attr in ("content_hash", "receipt_hash", "stage_hash", "decision_hash", "checkpoint_hash"):
        if hasattr(value, attr):
            digest = getattr(value, attr)
            if callable(digest):
                digest = digest()
            if isinstance(digest, str) and digest.strip():
                return f"{type(value).__name__}|sha256:{_text(digest, name)}"

    material = getattr(value, "material", None)
    if callable(material):
        digest = semantic_hash(material())
        return f"{type(value).__name__}|sha256:{digest}"

    raise GT0V3RuntimeIntegrityError(f"{name} lacks an exact stable ref/hash surface")


def _upstream_status(receipt: Any) -> str:
    for attr in ("status", "stage_status", "typed_state", "result_state"):
        if hasattr(receipt, attr):
            return _status_name(getattr(receipt, attr))
    raise GT0V3RuntimeIntegrityError("PRE-V3 receipt lacks typed stage status")


def _upstream_permission(receipt: Any) -> Any:
    for attr in ("consumer_permission", "permission", "permission_ceiling", "permissions"):
        if hasattr(receipt, attr):
            value = getattr(receipt, attr)
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, (str, int, bool, tuple, list, dict)) or value is None:
                return value
            return str(value)
    return None


def _upstream_information_loss(receipt: Any) -> Any:
    for attr in ("information_loss", "information_loss_declaration"):
        if hasattr(receipt, attr):
            value = getattr(receipt, attr)
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, (str, int, bool, tuple, list, dict)) or value is None:
                return value
            return str(value)
    return None


@dataclass(frozen=True)
class GT0V3RuntimeCheckpoint:
    """Minimal deterministic V3 fingerprint sufficient for a zero-effect proof."""

    actor_id: str
    actor_state_hash: str
    causal_ledger_hash: str
    causal_cursor: int
    rng_state_hash: str
    scheduler_state_hash: str
    checkpoint_version: str = "GT0_V3_ZERO_EFFECT_CHECKPOINT@1"

    def __post_init__(self) -> None:
        object.__setattr__(self, "actor_id", _text(self.actor_id, "actor_id"))
        for field in (
            "actor_state_hash",
            "causal_ledger_hash",
            "rng_state_hash",
            "scheduler_state_hash",
            "checkpoint_version",
        ):
            object.__setattr__(self, field, _text(getattr(self, field), field))
        if not isinstance(self.causal_cursor, int) or isinstance(self.causal_cursor, bool) or self.causal_cursor < 0:
            raise GT0V3RuntimeIntegrityError("causal_cursor must be a nonnegative integer")

    def material(self) -> Mapping[str, Any]:
        return {
            "checkpoint_version": self.checkpoint_version,
            "actor_id": self.actor_id,
            "actor_state_hash": self.actor_state_hash,
            "causal_ledger_hash": self.causal_ledger_hash,
            "causal_cursor": self.causal_cursor,
            "rng_state_hash": self.rng_state_hash,
            "scheduler_state_hash": self.scheduler_state_hash,
        }

    @property
    def checkpoint_hash(self) -> str:
        return semantic_hash(self.material())

    @property
    def ref(self) -> str:
        return f"urn:rawlsing:gt0:v3-checkpoint:sha256:{self.checkpoint_hash}"

    def guard_fingerprint(self) -> Mapping[str, Any]:
        return {
            "actor_state_hash": self.actor_state_hash,
            "causal_ledger_hash": self.causal_ledger_hash,
            "causal_cursor": self.causal_cursor,
            "rng_state_hash": self.rng_state_hash,
            "scheduler_state_hash": self.scheduler_state_hash,
        }


@dataclass(frozen=True)
class GT0V3ZeroEffectDisposition:
    """Control/audit receipt.  It is not actor causal history."""

    actor_id: str
    upstream_receipt_ref: str
    upstream_status: str
    upstream_producer_refs: tuple[str, ...]
    decision_status: str
    reason_code: str
    psepf_result_ref: str | None
    psepf_result_hash: str | None
    guard_outcome: str | None
    guard_reason: str | None
    pre_checkpoint_ref: str
    post_checkpoint_ref: str
    actor_state_effect: str
    causal_ledger_appends: int
    causal_cursor_delta: int
    rng_mutations: int
    scheduler_mutations: int
    replay_determinants: tuple[str, ...]
    information_loss: str
    upstream_permission: Any = None
    upstream_information_loss: Any = None
    contract_id: str = GT0_V3_RUNTIME_CONTRACT_ID

    def __post_init__(self) -> None:
        if self.decision_status not in _ALLOWED_STAGE_STATUSES:
            raise GT0V3RuntimeIntegrityError(f"unsupported GT0 stage status {self.decision_status!r}")
        if self.actor_state_effect != "ZERO":
            raise GT0V3RuntimeIntegrityError("WSC002E may only emit zero actor-state effect")
        if any(
            value != 0
            for value in (
                self.causal_ledger_appends,
                self.causal_cursor_delta,
                self.rng_mutations,
                self.scheduler_mutations,
            )
        ):
            raise GT0V3RuntimeIntegrityError("WSC002E may not mutate V3 causal/RNG/scheduler state")
        if self.pre_checkpoint_ref != self.post_checkpoint_ref:
            raise GT0V3RuntimeIntegrityError("zero-effect disposition must preserve checkpoint identity")

    def material(self) -> Mapping[str, Any]:
        return {
            "contract_id": self.contract_id,
            "actor_id": self.actor_id,
            "upstream_receipt_ref": self.upstream_receipt_ref,
            "upstream_status": self.upstream_status,
            "upstream_producer_refs": list(self.upstream_producer_refs),
            "decision_status": self.decision_status,
            "reason_code": self.reason_code,
            "psepf_result_ref": self.psepf_result_ref,
            "psepf_result_hash": self.psepf_result_hash,
            "guard_outcome": self.guard_outcome,
            "guard_reason": self.guard_reason,
            "pre_checkpoint_ref": self.pre_checkpoint_ref,
            "post_checkpoint_ref": self.post_checkpoint_ref,
            "actor_state_effect": self.actor_state_effect,
            "causal_ledger_appends": self.causal_ledger_appends,
            "causal_cursor_delta": self.causal_cursor_delta,
            "rng_mutations": self.rng_mutations,
            "scheduler_mutations": self.scheduler_mutations,
            "replay_determinants": list(self.replay_determinants),
            "information_loss": self.information_loss,
            "upstream_permission": self.upstream_permission,
            "upstream_information_loss": self.upstream_information_loss,
        }

    @property
    def decision_hash(self) -> str:
        return semantic_hash(self.material())

    @property
    def ref(self) -> str:
        return f"urn:rawlsing:gt0:prev3-v3-disposition:sha256:{self.decision_hash}"


@dataclass(frozen=True)
class GT0Prev3V3Execution:
    """Integration carrier containing the shared protocol receipt and zero-effect proof."""

    envelope: Any
    stage_receipt: Any
    disposition: GT0V3ZeroEffectDisposition
    pre_checkpoint: GT0V3RuntimeCheckpoint
    post_checkpoint: GT0V3RuntimeCheckpoint

    @property
    def zero_effect(self) -> bool:
        return (
            self.pre_checkpoint == self.post_checkpoint
            and self.pre_checkpoint.checkpoint_hash == self.post_checkpoint.checkpoint_hash
            and self.disposition.actor_state_effect == "ZERO"
            and self.disposition.causal_ledger_appends == 0
            and self.disposition.causal_cursor_delta == 0
            and self.disposition.rng_mutations == 0
            and self.disposition.scheduler_mutations == 0
        )


def _psepf_ref(result: PositionedSubjectPossibilityResult) -> str:
    return _stable_ref(result.ref, "psepf_result_ref")


def _evaluate_psepf_state(
    result: PositionedSubjectPossibilityResult,
    checkpoint: GT0V3RuntimeCheckpoint,
) -> tuple[str, str, str | None, str | None, str]:
    """Map existing PSEPF typed state without creating comparator authority."""

    state = result.result_state
    if state == "VALID_EMPTY":
        return (
            "VALID_EMPTY",
            "PSEPF_VALID_EMPTY_PRESERVED__NO_ACTOR_EFFECT",
            None,
            None,
            "NO_DEFAULT_VALUE_SUBSTITUTION",
        )
    if state == "NONCOMPARABLE":
        return (
            "NONCOMPARABLE",
            "PSEPF_NONCOMPARABLE_PRESERVED__NO_PROXY_RESCUE",
            None,
            None,
            "NO_DEFAULT_VALUE_SUBSTITUTION",
        )
    if state in {"UNRESOLVED", "EXACT_UNRESOLVED_PROXY_AVAILABLE"}:
        loss = (
            "NO_ADDITIONAL_SEAM_COMPRESSION__UPSTREAM_PROXY_SPECIFICITY_LOSS_PRESERVED"
            if result.proxy is not None
            else "NO_DEFAULT_VALUE_SUBSTITUTION"
        )
        return (
            "UNRESOLVED",
            f"PSEPF_{state}_PRESERVED__NOT_ACTOR_EVIDENCE",
            None,
            None,
            loss,
        )
    if state == "FAIL_CLOSED":
        return (
            "INTEGRITY_FAILURE",
            "PSEPF_FAIL_CLOSED_PRESERVED__NO_ACTOR_EFFECT",
            None,
            None,
            "NO_DEFAULT_VALUE_SUBSTITUTION",
        )
    if state != "EXACT_SUPPORTED":
        return (
            "INTEGRITY_FAILURE",
            f"UNRECOGNIZED_PSEPF_STATE__{state}",
            None,
            None,
            "NO_DEFAULT_VALUE_SUBSTITUTION",
        )

    # Exact empirical possibility is still learned-world evidence.  Invoke the
    # accepted zero-positive guard only as an additional zero-effect witness;
    # this does not resolve OBL031 predicate/comparator ancestry.
    guard = evaluate_psepf_zero_positive_guard(
        {
            "actor_id": checkpoint.actor_id,
            "source_class": "PSEPF",
            "source_ref": _psepf_ref(result),
            "source_hash": result.result_hash,
            "source_lineage": [],
            "transition_surface_id": GT0_V3_TRANSITION_SURFACE,
            "operation_class": GT0_V3_OPERATION_CLASS,
            "state_fingerprint": checkpoint.guard_fingerprint(),
        }
    )
    if guard.outcome is not GuardOutcome.DENY_ZERO_EFFECT or not guard.zero_effect:
        # Current WSC002E has no positive comparator or transition authority;
        # any nonzero/delegating behavior here would violate the commissioned
        # implementation ceiling rather than authorize a positive path.
        return (
            "INTEGRITY_FAILURE",
            "UNEXPECTED_NONZERO_OR_DELEGATING_GUARD_RESULT",
            guard.outcome.value,
            guard.reason.value,
            "NO_ADDITIONAL_SEAM_COMPRESSION",
        )
    return (
        "BLOCKED_COMPARATOR_ANCESTRY",
        "EXACT_PSEPF_PRESENT__OBL031_COMPARATOR_ANCESTRY_NOT_PRODUCTION_VERIFIED",
        guard.outcome.value,
        guard.reason.value,
        "NO_ADDITIONAL_SEAM_COMPRESSION",
    )


def _load_protocol(protocol_module: Any | None) -> Any:
    if protocol_module is not None:
        return protocol_module
    try:
        return import_module("rawlsing_next.wsc_gt0_protocol")
    except ModuleNotFoundError as exc:
        raise GT0ProtocolIntegrationError(
            "wsc_gt0_protocol is a sibling WSC002 candidate and is not present on this independent branch; "
            "pass a protocol_module test double here or bind the real module during central integration"
        ) from exc


def _enum_status(protocol: Any, status_name: str) -> Any:
    enum_cls = getattr(protocol, "GT0StageStatus", None)
    if enum_cls is None:
        raise GT0ProtocolIntegrationError("protocol module lacks GT0StageStatus")
    try:
        return enum_cls[status_name]
    except Exception:
        try:
            return enum_cls(status_name)
        except Exception as exc:
            raise GT0ProtocolIntegrationError(
                f"shared protocol does not expose required status {status_name}"
            ) from exc


def _call_supported(callable_obj: Any, candidates: Mapping[str, Any]) -> Any:
    sig = inspect.signature(callable_obj)
    params = sig.parameters
    accepts_kwargs = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values())
    if accepts_kwargs:
        return callable_obj(**dict(candidates))
    kwargs = {name: candidates[name] for name in params if name in candidates}
    missing = [
        name
        for name, param in params.items()
        if name not in kwargs
        and param.default is inspect.Parameter.empty
        and param.kind not in {inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD}
    ]
    if missing:
        raise GT0ProtocolIntegrationError(
            "GT0StageReceipt constructor has unresolved required fields: " + ", ".join(missing)
        )
    return callable_obj(**kwargs)


def _build_stage_receipt(
    *,
    protocol: Any,
    envelope_ref: str,
    upstream_receipt_ref: str,
    producer_refs: tuple[str, ...],
    disposition: GT0V3ZeroEffectDisposition,
    checkpoint: GT0V3RuntimeCheckpoint,
) -> Any:
    receipt_cls = getattr(protocol, "GT0StageReceipt", None)
    if receipt_cls is None:
        raise GT0ProtocolIntegrationError("protocol module lacks GT0StageReceipt")

    status = _enum_status(protocol, disposition.decision_status)
    output_refs = (disposition.ref, checkpoint.ref)
    replay_refs = disposition.replay_determinants
    receipt_material = {
        "stage_id": GT0_V3_STAGE_ID,
        "status": disposition.decision_status,
        "envelope_ref": envelope_ref,
        "upstream_refs": (upstream_receipt_ref,),
        "producer_refs": producer_refs,
        "output_refs": output_refs,
        "semantic_owner": GT0_V3_CONTROL_OWNER,
        "consumer_permission": GT0_V3_PERMISSION_CEILING,
        "information_loss": disposition.information_loss,
        "replay_refs": replay_refs,
        "disposition_ref": disposition.ref,
        "checkpoint_ref": checkpoint.ref,
    }
    receipt_hash = semantic_hash(receipt_material)
    receipt_id = f"urn:rawlsing:gt0:stage:prev3-v3:sha256:{receipt_hash}"

    candidates = {
        # canonical candidate names
        "receipt_id": receipt_id,
        "content_hash": receipt_hash,
        "receipt_hash": receipt_hash,
        "stage_id": GT0_V3_STAGE_ID,
        "stage_name": GT0_V3_STAGE_ID,
        "status": status,
        "stage_status": status,
        "typed_state": status,
        "envelope_ref": envelope_ref,
        "upstream_refs": (upstream_receipt_ref,),
        "upstream_reference_refs": (upstream_receipt_ref,),
        "producer_refs": producer_refs,
        "producer_reference_refs": producer_refs,
        "output_refs": output_refs,
        "output_reference_refs": output_refs,
        "semantic_owner": GT0_V3_CONTROL_OWNER,
        "producer_owner": GT0_V3_CONTROL_OWNER,
        "consumer_permission": GT0_V3_PERMISSION_CEILING,
        "permission": GT0_V3_PERMISSION_CEILING,
        "permission_ceiling": GT0_V3_PERMISSION_CEILING,
        "information_loss": disposition.information_loss,
        "information_loss_declaration": disposition.information_loss,
        "replay_refs": replay_refs,
        "replay_determinants": replay_refs,
        "details": receipt_material,
        "payload": receipt_material,
        "metadata": receipt_material,
    }

    from_material = getattr(receipt_cls, "from_material", None)
    if callable(from_material):
        try:
            return from_material(receipt_material)
        except TypeError:
            pass
    build = getattr(receipt_cls, "build", None)
    if callable(build):
        try:
            return _call_supported(build, candidates)
        except TypeError:
            pass
    return _call_supported(receipt_cls, candidates)


def run_gt0_prev3_v3(
    envelope: Any,
    prev3_receipt: Any,
    *,
    actor_id: str,
    runtime_checkpoint: GT0V3RuntimeCheckpoint,
    prev3_producer_refs: Sequence[Any],
    psepf_result: PositionedSubjectPossibilityResult | None = None,
    protocol_module: Any | None = None,
) -> GT0Prev3V3Execution:
    """Run the minimum GT0 PRE-V3 -> V3 stage.

    Current positive behavior is intentionally unavailable.  The function may
    preserve a real upstream PSEPF result, but it never constructs one.  Even an
    exact-supported PSEPF remains blocked at OBL031 because this worker has no
    competent production comparator/predicate-ancestry verifier.  The current
    zero-positive guard is additionally evaluated as a nonmutation witness.
    """

    actor_id = _text(actor_id, "actor_id")
    if runtime_checkpoint.actor_id != actor_id:
        raise GT0V3RuntimeIntegrityError("actor_id does not match runtime checkpoint")

    envelope_ref = _stable_ref(envelope, "conservation_envelope_ref")
    upstream_receipt_ref = _stable_ref(prev3_receipt, "prev3_receipt_ref")
    upstream_status = _upstream_status(prev3_receipt)
    producer_refs = tuple(_stable_ref(ref, "prev3_producer_ref") for ref in prev3_producer_refs)
    if not producer_refs:
        raise GT0V3RuntimeIntegrityError("at least one exact PRE-V3 producer ref is required")
    if len(set(producer_refs)) != len(producer_refs):
        raise GT0V3RuntimeIntegrityError("duplicate PRE-V3 producer refs are not allowed")

    psepf_ref: str | None = None
    psepf_hash: str | None = None
    guard_outcome: str | None = None
    guard_reason: str | None = None

    if psepf_result is None:
        decision_status = "BLOCKED_COMPARATOR_ANCESTRY"
        reason = (
            "NO_POSITIONED_SUBJECT_POSSIBILITY_FABRICATED__"
            f"UPSTREAM_{upstream_status}_PRESERVED__OBL031_OPEN"
        )
        information_loss = "NO_DEFAULT_VALUE_SUBSTITUTION__NO_PSEPF_FABRICATION"
    elif not isinstance(psepf_result, PositionedSubjectPossibilityResult):
        decision_status = "INTEGRITY_FAILURE"
        reason = "PSEPF_INPUT_IS_NOT_CURRENT_POSITIONED_SUBJECT_POSSIBILITY_RESULT"
        information_loss = "NO_DEFAULT_VALUE_SUBSTITUTION"
    else:
        psepf_ref = _psepf_ref(psepf_result)
        psepf_hash = psepf_result.result_hash
        (
            decision_status,
            reason,
            guard_outcome,
            guard_reason,
            information_loss,
        ) = _evaluate_psepf_state(psepf_result, runtime_checkpoint)

    # WSC002E is zero-effect by construction.  No actor causal event/checkpoint
    # mutation is attempted, and the same immutable checkpoint is returned.
    post_checkpoint = runtime_checkpoint
    replay_determinants = (
        envelope_ref,
        upstream_receipt_ref,
        *producer_refs,
        runtime_checkpoint.ref,
        *(() if psepf_ref is None else (psepf_ref,)),
    )
    disposition = GT0V3ZeroEffectDisposition(
        actor_id=actor_id,
        upstream_receipt_ref=upstream_receipt_ref,
        upstream_status=upstream_status,
        upstream_producer_refs=producer_refs,
        decision_status=decision_status,
        reason_code=reason,
        psepf_result_ref=psepf_ref,
        psepf_result_hash=psepf_hash,
        guard_outcome=guard_outcome,
        guard_reason=guard_reason,
        pre_checkpoint_ref=runtime_checkpoint.ref,
        post_checkpoint_ref=post_checkpoint.ref,
        actor_state_effect="ZERO",
        causal_ledger_appends=0,
        causal_cursor_delta=0,
        rng_mutations=0,
        scheduler_mutations=0,
        replay_determinants=replay_determinants,
        information_loss=information_loss,
        upstream_permission=_upstream_permission(prev3_receipt),
        upstream_information_loss=_upstream_information_loss(prev3_receipt),
    )

    protocol = _load_protocol(protocol_module)
    stage_receipt = _build_stage_receipt(
        protocol=protocol,
        envelope_ref=envelope_ref,
        upstream_receipt_ref=upstream_receipt_ref,
        producer_refs=producer_refs,
        disposition=disposition,
        checkpoint=post_checkpoint,
    )
    execution = GT0Prev3V3Execution(
        envelope=envelope,
        stage_receipt=stage_receipt,
        disposition=disposition,
        pre_checkpoint=runtime_checkpoint,
        post_checkpoint=post_checkpoint,
    )
    if not execution.zero_effect:
        raise GT0V3RuntimeIntegrityError("zero-effect proof failed")
    return execution
