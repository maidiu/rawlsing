"""R95 R06 source-separated world selected-view binding (TEST_ONLY).

Binds independently typed source-indexed fields to the actual unchanged N10E
positioned-subject consumer through the accepted composition owner. It creates
no new evidence, geometry, pooling or temporal authority.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash


P41_COMMIT = "f27d1101048638bba395143a48efb7ef00bfcda4"
P41_PACKET = ("WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-"
              "N10E-N10W-SERVING-R1")
_P41_PINNED = None


def _tree_sha256(root: Path) -> str:
    entries = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        rel = path.relative_to(root).as_posix()
        entries.append((rel, hashlib.sha256(path.read_bytes()).hexdigest()))
    return semantic_hash(entries)


def _pinned_p41_runtime() -> Path:
    global _P41_PINNED
    if _P41_PINNED is not None:
        return _P41_PINNED
    repo = Path(__file__).resolve().parents[1]
    base = Path(tempfile.mkdtemp(prefix="r06r4-pinned-p41-"))
    archive = base / "pinned-p41.tar"
    proc = subprocess.run(
        ["git", "-C", str(repo), "archive", P41_COMMIT, P41_PACKET,
         "-o", str(archive)],
        capture_output=True, text=True, timeout=300,
    )
    if proc.returncode != 0:
        shutil.rmtree(base, ignore_errors=True)
        raise WorldBindingError("P41_RUNTIME_PIN_UNAVAILABLE")
    with tarfile.open(archive) as handle:
        handle.extractall(base)
    runtime = base / P41_PACKET / "runtime"
    if not runtime.is_dir():
        shutil.rmtree(base, ignore_errors=True)
        raise WorldBindingError("P41_RUNTIME_PIN_INCOMPLETE")
    _P41_PINNED = runtime.resolve()
    return _P41_PINNED


def _validate_pinned_runtime(candidate: str) -> Path:
    if not isinstance(candidate, str) or not candidate:
        raise WorldBindingError("P41_RUNTIME_PIN_REQUIRED")
    candidate_path = Path(candidate).resolve()
    if not candidate_path.is_dir():
        raise WorldBindingError("UNTRUSTED_P41_RUNTIME")
    pinned = _pinned_p41_runtime()
    if _tree_sha256(candidate_path) != _tree_sha256(pinned):
        raise WorldBindingError("UNTRUSTED_P41_RUNTIME")
    return pinned


def _purge_p41_modules() -> None:
    for name in tuple(sys.modules):
        if (name in {"bootstrap", "p41_service", "fixture", "readthrough"}
                or name == "product" or name.startswith("product.")):
            del sys.modules[name]


@dataclass(frozen=True)
class R06TrustedExecutionContext:
    learned_consumer: Any
    original_ref: ExactRef
    step: Mapping[str, Any]
    empirical: Mapping[str, Any]
    structural_revision: bool
    p41_runtime: str
    coordinator: Any
    execution_request: Any
    original_view: Any

    def verify_original(self) -> Any:
        bound = self.coordinator.execute(self.execution_request)
        if bound.original_ref != self.original_ref:
            raise WorldBindingError("R05_COORDINATOR_ORIGINAL_MISMATCH")
        if self.original_view.original_ref != self.original_ref:
            raise WorldBindingError("R05_COORDINATOR_ORIGINAL_MISMATCH")
        if self.step.get("content_hash") != self.learned_consumer.consumer_result.result_hash:
            raise WorldBindingError("R05_ACTUAL_STEP_CONSUMER_MISMATCH")
        if not bound.view.compositions:
            raise WorldBindingError("R05_COORDINATOR_ORIGINAL_EMPTY")
        if (bound.view.compositions[0].consumer_result_or_null is None
                or bound.view.compositions[0].consumer_result_or_null.result_hash
                != self.learned_consumer.consumer_result.result_hash):
            raise WorldBindingError("R05_COORDINATOR_CONSUMER_MISMATCH")
        return bound


_TRUSTED_CONTEXTS: dict[str, R06TrustedExecutionContext] = {}


def configure_trusted_execution_context(
    *,
    p41_runtime: str,
    learned_consumer: Any,
    step: Mapping[str, Any],
    empirical: Mapping[str, Any],
    structural_revision: bool,
    coordinator: Any,
    execution_request: Any,
    original_ref: ExactRef,
    original_view: Any,
) -> str:
    pinned = _validate_pinned_runtime(p41_runtime)
    context = R06TrustedExecutionContext(
        learned_consumer=learned_consumer, original_ref=original_ref,
        step=dict(step), empirical=empirical,
        structural_revision=structural_revision, p41_runtime=str(pinned),
        coordinator=coordinator, execution_request=execution_request,
        original_view=original_view,
    )
    context.verify_original()
    handle = "r06ctx-" + hashlib.sha256(os.urandom(32)).hexdigest()
    _TRUSTED_CONTEXTS[handle] = context
    return handle


class WorldBindingError(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class WorldFieldBinding:
    binding_id: str
    empirical_coordinate_ref: ExactRef
    exact_value: Any
    subject_fact_ref: ExactRef
    source_universe_ref: ExactRef
    release_ref: ExactRef
    unit: str
    role: str = "STRUCTURAL"
    clock_ref: str | None = None
    relation_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        if not self.binding_id or not self.unit or not self.role:
            raise WorldBindingError("WORLD_FIELD_IDENTITY_INCOMPLETE")
        if self.role not in {"STRUCTURAL", "CONTEXT"}:
            raise WorldBindingError("WORLD_FIELD_ROLE_UNKNOWN")
        if not all(isinstance(ref, ExactRef) for ref in (
            self.empirical_coordinate_ref, self.subject_fact_ref,
            self.source_universe_ref, self.release_ref,
        )):
            raise WorldBindingError("WORLD_FIELD_EXACT_REF_REQUIRED")

    def material(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "empirical_coordinate_ref": self.empirical_coordinate_ref.as_dict(),
            "exact_value": self.exact_value,
            "subject_fact_ref": self.subject_fact_ref.as_dict(),
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "unit": self.unit, "role": self.role,
            "clock_ref": self.clock_ref,
            "relation_ref": None if self.relation_ref is None else self.relation_ref.as_dict(),
        }


@dataclass(frozen=True)
class WorldSelectionRequest:
    fields: tuple[WorldFieldBinding, ...]
    repository: Any
    empirical_query: Any
    predicate: Any
    authority_registry: Any
    release_refs: tuple[ExactRef, ...]
    consumer_query: Any
    model_rule: Any
    condition_binding_witness: Any
    currentness: str = "CURRENT"
    relation_transport_ref: ExactRef | None = None
    relation_transport_authorized: bool = False
    ff_structural_authority_ref: ExactRef | None = None
    ff_structural_admission: Any | None = None
    temporal_pair_ref: ExactRef | None = None
    observed_temporal_pair_refs: tuple[ExactRef, ...] = ()
    as_of_ref: str | None = None


@dataclass(frozen=True)
class WorldSelectedView:
    state: str
    reason_code: str
    field_refs: tuple[ExactRef, ...]
    source_universe_ref: ExactRef
    release_ref: ExactRef
    consumer_result: Any | None
    consumer_values_read: Mapping[str, Any] | None
    view_hash: str
    z_unresolved: bool = True

    def material(self) -> dict[str, Any]:
        return {
            "state": self.state, "reason_code": self.reason_code,
            "field_refs": [ref.as_dict() for ref in self.field_refs],
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "consumer_result_hash": (
                None if self.consumer_result is None
                else self.consumer_result.result_hash
            ),
            "consumer_values_read": self.consumer_values_read,
            "view_hash": self.view_hash, "z_unresolved": self.z_unresolved,
        }


def _refusal(code: str, request: WorldSelectionRequest, field_refs: tuple[ExactRef, ...]) -> WorldSelectedView:
    material = {
        "state": "REFUSED", "reason_code": code,
        "fields": [ref.as_dict() for ref in field_refs],
        "source": request.consumer_query.source_universe_ref.as_dict(),
        "release": request.consumer_query.release_ref.as_dict(),
    }
    return WorldSelectedView(
        state="REFUSED", reason_code=code, field_refs=field_refs,
        source_universe_ref=request.consumer_query.source_universe_ref,
        release_ref=request.consumer_query.release_ref,
        consumer_result=None, consumer_values_read=None,
        view_hash=semantic_hash(material),
    )


def select_world_view(request: WorldSelectionRequest) -> WorldSelectedView:
    """Validate source-separated world fields and invoke the unchanged N10E consumer."""
    if request.currentness != "CURRENT":
        return _refusal("WORLD_CURRENTNESS_NOT_CURRENT", request, ())
    fields = tuple(request.fields)
    if len(fields) < 2:
        return _refusal("WORLD_REQUIRES_AT_LEAST_TWO_FIELDS", request, ())
    if len({field.binding_id for field in fields}) != len(fields):
        return _refusal("WORLD_DUPLICATE_FIELD_BINDING", request, ())
    field_refs = tuple(sorted((field.empirical_coordinate_ref for field in fields), key=lambda ref: ref.key))
    if any(field.source_universe_ref != request.consumer_query.source_universe_ref
           or field.release_ref != request.consumer_query.release_ref for field in fields):
        return _refusal("WORLD_FIELD_SOURCE_RELEASE_MISMATCH", request, field_refs)
    if any(field.release_ref not in request.release_refs for field in fields):
        return _refusal("WORLD_FIELD_RELEASE_NOT_ADMITTED", request, field_refs)
    units = {field.unit for field in fields}
    if len(units) > 1:
        return _refusal("CROSS_UNIT_LINKED_QUERY_UNAVAILABLE", request, field_refs)
    if any(field.role == "CONTEXT" for field in fields):
        return _refusal("CONTEXT_STRUCTURAL_AUTHORITY_HELD", request, field_refs)
    clocks = {field.clock_ref for field in fields if field.clock_ref is not None}
    if len(clocks) > 1:
        if (request.temporal_pair_ref is None or not request.observed_temporal_pair_refs
                or request.temporal_pair_ref not in request.observed_temporal_pair_refs):
            return _refusal("UNOBSERVED_TEMPORAL_PAIR", request, field_refs)
    query_bindings = tuple(request.consumer_query.conditioner_bindings)
    expected = {
        (field.empirical_coordinate_ref.key, field.subject_fact_ref.key)
        for field in fields
    }
    observed = {
        (binding.empirical_coordinate_ref.key, binding.subject_fact_ref.key)
        for binding in query_bindings
    }
    if expected != observed:
        return _refusal("WORLD_FIELD_CONSUMER_MISMATCH", request, field_refs)
    try:
        composition = compose_positioned_subject_possibility(
            repository=request.repository,
            empirical_query=request.empirical_query,
            predicate=request.predicate,
            authority_registry=request.authority_registry,
            release_refs=request.release_refs,
            consumer_query=request.consumer_query,
            model_rule=request.model_rule,
            condition_binding_witness=request.condition_binding_witness,
        )
    except Exception as exc:
        return _refusal("WORLD_NATIVE_CONSUMER_REFUSED:" + type(exc).__name__, request, field_refs)
    consumer = composition.consumer_result_or_null
    if consumer is None:
        return _refusal("WORLD_CONSUMER_RESULT_UNAVAILABLE:" + composition.analytical_state, request, field_refs)
    values = {
        "consumer_result_hash": consumer.result_hash,
        "consumer_values_read": consumer.material(),
        "analytical_state": composition.analytical_state,
        "conditioner_ids": request.consumer_query.conditioner_ids,
        "as_of_ref": request.as_of_ref,
    }
    material = {
        "state": composition.analytical_state,
        "fields": [field.material() for field in sorted(fields, key=lambda item: item.binding_id)],
        "consumer_query_ref": request.consumer_query.ref.as_dict(),
        "consumer_result_hash": consumer.result_hash,
        "consumer_values": consumer.material(),
        "source": request.consumer_query.source_universe_ref.as_dict(),
        "release": request.consumer_query.release_ref.as_dict(),
        "as_of_ref": request.as_of_ref,
    }
    return WorldSelectedView(
        state=composition.analytical_state, reason_code="WORLD_SELECTED_VIEW",
        field_refs=field_refs,
        source_universe_ref=request.consumer_query.source_universe_ref,
        release_ref=request.consumer_query.release_ref,
        consumer_result=consumer, consumer_values_read=values,
        view_hash=semantic_hash(material),
    )


__all__ = [
    "WorldBindingError", "WorldFieldBinding", "WorldSelectionRequest",
    "WorldSelectedView", "select_world_view",
]


# ---------------------------------------------------------------------------
# Actual joined N9/N10W/E04 adapter (J42/P41 runtime, TEST_ONLY).

@dataclass(frozen=True)
class JoinedWorldField:
    field_id: str
    expected_value: Any
    unit: str = "SYNTHETIC_INDIVIDUAL_RESPONDENT"
    role: str = "STRUCTURAL"
    clock_ref: str | None = None
    relation_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        if not self.field_id or not self.unit or not self.role:
            raise WorldBindingError("JOINED_FIELD_IDENTITY_INCOMPLETE")
        if self.role not in {"STRUCTURAL", "CONTEXT"}:
            raise WorldBindingError("JOINED_FIELD_ROLE_UNKNOWN")


@dataclass(frozen=True)
class JoinedWorldSelectionRequest:
    joined_receipts: Mapping[str, Any]
    view_key: str
    fields: tuple[JoinedWorldField, ...]
    source_rows_hash: str
    currentness: str = "CURRENT"
    as_of_ref: str | None = None
    relation_transport_ref: ExactRef | None = None
    relation_transport_authorized: bool = False
    ff_structural_authority_ref: ExactRef | None = None
    ff_structural_admission: Any | None = None
    temporal_pair_ref: ExactRef | None = None
    observed_temporal_pair_refs: tuple[ExactRef, ...] = ()


@dataclass(frozen=True)
class JoinedWorldSelectedView:
    state: str
    reason_code: str
    view_key: str
    field_ids: tuple[str, ...]
    consumer_values_read: Mapping[str, Any] | None
    view_hash: str
    z_unresolved: bool = True

    def material(self) -> Mapping[str, Any]:
        return {
            "state": self.state, "reason_code": self.reason_code,
            "view_key": self.view_key, "field_ids": list(self.field_ids),
            "consumer_values_read": self.consumer_values_read,
            "view_hash": self.view_hash, "z_unresolved": self.z_unresolved,
        }


def _joined_refusal(code: str, request: JoinedWorldSelectionRequest,
                    field_ids: tuple[str, ...] = ()) -> JoinedWorldSelectedView:
    return JoinedWorldSelectedView(
        state="REFUSED", reason_code=code, view_key=request.view_key,
        field_ids=field_ids, consumer_values_read=None,
        view_hash=semantic_hash({"state": "REFUSED", "reason": code,
                                 "view_key": request.view_key,
                                 "field_ids": list(field_ids)}),
    )


def select_joined_world_view(request: JoinedWorldSelectionRequest) -> JoinedWorldSelectedView:
    """Select from the actual unchanged J42/P41 N9/N10W/E04 product.

    The caller supplies receipts produced by the pinned J42 build; this adapter
    validates identities and returns a world-view assertion. It does not
    reimplement or replace the native consumer.
    """
    if request.currentness != "CURRENT":
        return _joined_refusal("WORLD_CURRENTNESS_NOT_CURRENT", request)
    receipts = request.joined_receipts
    if not isinstance(receipts, Mapping):
        return _joined_refusal("JOINED_RECEIPTS_REQUIRED", request)
    p41 = (receipts.get("p41_joined_receipts") or {}).get(request.view_key)
    joined = (receipts.get("joined_consumer_receipts") or {}).get(request.view_key)
    if not isinstance(p41, Mapping) or not isinstance(joined, Mapping):
        return _joined_refusal("JOINED_VIEW_NOT_FOUND", request)
    if (p41.get("schema") != "PYAT_R41_P41_GENERIC_POSSIBILITY_RECEIPT@1"
            or p41.get("service") != "P41_GENERIC_POSSIBILITY_SERVICE@1"):
        return _joined_refusal("JOINED_CONSUMER_CONTRACT_MISMATCH", request)
    providers = p41.get("providers") or {}
    if (not str(providers.get("n9_world", "")).startswith("W41_")
            or not str(providers.get("n10e_empirical", "")).startswith("E41_")
            or not str(providers.get("n10w_progressive", "")).startswith("P41_")):
        return _joined_refusal("JOINED_PROVIDER_IDENTITY_MISMATCH", request)
    material = joined.get("material") or {}
    if (material.get("service_contract")
            != "J42_JOINED_E41_W41_P41_PREV3_CONSUMER@1"):
        return _joined_refusal("JOINED_E04_CONSUMER_CONTRACT_MISMATCH", request)
    bindings = p41.get("j42_bindings") or {}
    if (not request.source_rows_hash
            or bindings.get("e41_rows_hash") != request.source_rows_hash
            or material.get("e41_rows_hash") != request.source_rows_hash):
        return _joined_refusal("JOINED_SOURCE_ROWS_MISMATCH", request)
    clock = bindings.get("w41_clock") or {}
    if request.as_of_ref is not None and request.as_of_ref not in {
        clock.get("valid_at"), clock.get("published_asof"), clock.get("test_now")
    }:
        return _joined_refusal("JOINED_AS_OF_MISMATCH", request)
    fields = tuple(request.fields)
    field_ids = tuple(field.field_id for field in fields)
    if len(fields) < 2:
        return _joined_refusal("WORLD_REQUIRES_AT_LEAST_TWO_FIELDS", request, field_ids)
    if len(set(field_ids)) != len(fields):
        return _joined_refusal("WORLD_DUPLICATE_FIELD_BINDING", request, field_ids)
    rules = (p41.get("n9_world") or {}).get("rules") or {}
    for field in fields:
        if field.field_id not in rules:
            return _joined_refusal("JOINED_WORLD_FIELD_ABSENT", request, field_ids)
        if rules[field.field_id].get("value") != field.expected_value:
            return _joined_refusal("JOINED_WORLD_FIELD_VALUE_MISMATCH", request, field_ids)
        if field.field_id not in set(material.get("dependencies") or ()):
            return _joined_refusal("JOINED_FIELD_NOT_CONSUMED", request, field_ids)
    units = {field.unit for field in fields}
    if len(units) > 1:
        return _joined_refusal("CROSS_UNIT_LINKED_QUERY_UNAVAILABLE", request, field_ids)
    if any(field.role == "CONTEXT" for field in fields):
        return _joined_refusal("CONTEXT_STRUCTURAL_AUTHORITY_HELD", request, field_ids)
    clocks = {field.clock_ref for field in fields if field.clock_ref is not None}
    if len(clocks) > 1:
        if (request.temporal_pair_ref is None or not request.observed_temporal_pair_refs
                or request.temporal_pair_ref not in request.observed_temporal_pair_refs):
            return _joined_refusal("UNOBSERVED_TEMPORAL_PAIR", request, field_ids)
    n10e = p41.get("n10e_steps") or ()
    n10w = p41.get("n10w") or {}
    structural = p41.get("structural") or {}
    if (len(n10e) < 1
            or not all(step.get("state") == "EXACT_SUPPORTED" for step in n10e)
            or not n10w.get("positioned_consumptions")
            or not structural.get("routes")):
        return _joined_refusal("JOINED_CONSUMER_NOT_PRODUCTIVE", request, field_ids)
    values = {
        "schema": "R95_R06_JOINED_WORLD_VIEW@1",
        "view_key": request.view_key,
        "field_values": {field.field_id: field.expected_value for field in fields},
        "n9_clock": clock,
        "n9_currentness": (p41.get("n9_world") or {}).get("currentness"),
        "n9_routes": structural.get("routes"),
        "n10e_steps": n10e,
        "n10w": n10w,
        "joined_receipt_hash": joined.get("receipt_hash"),
        "p41_receipt_hash": p41.get("content_hash"),
        "consumer": p41.get("consumer"),
        "families": {"n9": providers.get("n9_world"),
                     "n10e": providers.get("n10e_empirical"),
                     "n10w": providers.get("n10w_progressive")},
        "z_unresolved": True,
    }
    return JoinedWorldSelectedView(
        state="SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER",
        reason_code="WORLD_SELECTED_VIEW",
        view_key=request.view_key, field_ids=field_ids,
        consumer_values_read=values,
        view_hash=semantic_hash(values),
    )


# ---------------------------------------------------------------------------
# R05 accepted-product -> actual P41 N9/N10W/E04 consumer (R06R3).

from typing import Callable


@dataclass(frozen=True)
class R05WorldField:
    field_id: str
    expected_value: Any
    unit: str
    role: str = "STRUCTURAL"
    clock_ref: str | None = None
    relation_ref: ExactRef | None = None
    temporal_expected_value: Any = None
    field_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        if not self.field_id or not self.unit or not self.role:
            raise WorldBindingError("R05_FIELD_IDENTITY_INCOMPLETE")
        if self.role not in {"STRUCTURAL", "CONTEXT"}:
            raise WorldBindingError("R05_FIELD_ROLE_UNKNOWN")


@dataclass(frozen=True)
class R05ActualExecution:
    """Host-retained actual P41 execution inputs, not a caller receipt."""

    p41_runtime: str
    empirical: Mapping[str, Any]
    step: Mapping[str, Any]
    learned_consumer: Any
    structural_revision: bool = True
    coordinator_original_ref: ExactRef | None = None
    trusted_context: R06TrustedExecutionContext | None = None
    execution_handle: str | None = None


@dataclass(frozen=True)
class R05WorldConsumerRequest:
    learned_consumer: Any
    fields: tuple[R05WorldField, ...]
    consumer: Callable[[str], Mapping[str, Any]] | None
    source_universe_ref: ExactRef
    release_ref: ExactRef
    source_rows_hash: str
    temporal_pair_ref: ExactRef | None = None
    observed_temporal_pair_refs: tuple[ExactRef, ...] = ()
    currentness: str = "CURRENT"
    as_of_ref: str | None = None
    relation_transport_ref: ExactRef | None = None
    relation_transport_authorized: bool = False
    ff_structural_authority_ref: ExactRef | None = None
    ff_structural_admission: Any | None = None
    actual_execution: R05ActualExecution | None = None
    claimed_receipts: Mapping[str, Mapping[str, Any]] | None = None
    execution_handle: str | None = None


@dataclass(frozen=True)
class R05WorldSelectedView:
    state: str
    reason_code: str
    field_ids: tuple[str, ...]
    consumer_values_read: Mapping[str, Any] | None
    view_hash: str
    temporal_changed: bool = False
    z_unresolved: bool = True

    def material(self) -> Mapping[str, Any]:
        return {
            "state": self.state, "reason_code": self.reason_code,
            "field_ids": list(self.field_ids),
            "consumer_values_read": self.consumer_values_read,
            "view_hash": self.view_hash,
            "temporal_changed": self.temporal_changed,
            "z_unresolved": self.z_unresolved,
        }


def _r05_refusal(code: str, request: R05WorldConsumerRequest,
                 field_ids: tuple[str, ...] = ()) -> R05WorldSelectedView:
    return R05WorldSelectedView(
        state="REFUSED", reason_code=code, field_ids=field_ids,
        consumer_values_read=None,
        view_hash=semantic_hash({"state": "REFUSED", "reason": code,
                                 "fields": list(field_ids)}),
    )


def _actual_temporal_payload(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    """Actual consumer value projection; excludes clock/hash/provenance labels."""
    steps = []
    for step in receipt.get("n10e_steps") or ():
        steps.append({
            "target": step.get("target"),
            "conditioners": step.get("conditioners"),
            "state": step.get("state"),
            "denominator": step.get("denominator"),
            "cells": step.get("cells"),
        })
    n10w = receipt.get("n10w") or {}
    return {
        "routes": (receipt.get("structural") or {}).get("routes"),
        "n10e": steps,
        "n10w_consumptions": n10w.get("positioned_consumptions"),
        "n10w_state": n10w.get("progressive_chain_state"),
    }


def _validate_r05_receipt(receipt: Any, request: R05WorldConsumerRequest,
                          fields: tuple[R05WorldField, ...], learned: Any,
                          *, temporal: bool) -> tuple[Mapping[str, Any] | None, str | None]:
    if not isinstance(receipt, Mapping):
        return None, "R05_CONSUMER_RECEIPT_REQUIRED"
    expected_hash = receipt.get("content_hash")
    material = {key: value for key, value in receipt.items() if key != "content_hash"}
    if not expected_hash or semantic_hash(material) != expected_hash:
        return None, "R05_CONSUMER_RECEIPT_HASH_MISMATCH"
    if (receipt.get("schema") != "PYAT_R41_P41_GENERIC_POSSIBILITY_RECEIPT@1"
            or receipt.get("service") != "P41_GENERIC_POSSIBILITY_SERVICE@1"):
        return None, "R05_P41_CONSUMER_CONTRACT_MISMATCH"
    providers = receipt.get("providers") or {}
    if providers.get("n10w_progressive") not in {
        "E03_PROGRESSIVE_CHAIN@1", "P41_GENERIC_POSSIBILITY_SERVICE@1"
    }:
        return None, "R05_P41_N10W_PROVIDER_MISMATCH"
    n9 = receipt.get("n9_world") or {}
    binding = n9.get("r05_binding") or {}
    if not binding:
        return None, "R05_LEARNED_BINDING_ABSENT"
    if (binding.get("source_universe_ref") != request.source_universe_ref.as_dict()
            or binding.get("release_ref") != request.release_ref.as_dict()):
        return None, "R05_SOURCE_RELEASE_MISMATCH"
    if binding.get("source_rows_hash") != request.source_rows_hash:
        return None, "R05_SOURCE_ROWS_MISMATCH"
    if binding.get("learned_receipt_ref") != learned.learned_receipt_ref.as_dict():
        return None, "R05_LEARNED_RECEIPT_MISMATCH"
    if binding.get("m1_disposition_ref") != learned.m1_disposition_ref.as_dict():
        return None, "R05_M1_DISPOSITION_MISMATCH"
    if binding.get("m2_release_ref") != learned.m2_release_ref.as_dict():
        return None, "R05_M2_RELEASE_MISMATCH"
    consumer_hash = learned.consumer_result.result_hash
    if binding.get("consumer_result_hash") != consumer_hash:
        return None, "R05_CONSUMER_RESULT_MISMATCH"
    if (learned.evidence_ref is None
            or binding.get("evidence_ref") != learned.evidence_ref.as_dict()):
        return None, "R05_EVIDENCE_REF_MISMATCH"
    steps = receipt.get("n10e_steps") or ()
    if not steps or any(step.get("content_hash") != consumer_hash for step in steps):
        return None, "R05_N10E_STEP_BINDING_MISMATCH"
    if learned.producer_query_ref is None or learned.producer_predicate_ref is None:
        return None, "R05_LEARNED_PRODUCER_REFERENCE_ABSENT"
    geometry = getattr(learned.consumer_result, "exact_geometry", None) or {}
    for step in steps:
        if step.get("producer_query_ref") != learned.producer_query_ref.as_dict():
            return None, "R05_N10E_QUERY_BINDING_MISMATCH"
        if step.get("producer_query_ref") != geometry.get("producer_query_ref"):
            return None, "R05_N10E_QUERY_BINDING_MISMATCH"
        if step.get("producer_fact_ref") != geometry.get("source_fact_ref"):
            return None, "R05_N10E_FACT_BINDING_MISMATCH"
        if step.get("evidence_ref") != learned.evidence_ref.as_dict():
            return None, "R05_N10E_EVIDENCE_BINDING_MISMATCH"
    if not (receipt.get("n10w") or {}).get("positioned_consumptions"):
        return None, "R05_N10W_CONSUMPTION_ABSENT"
    if not (receipt.get("structural") or {}).get("routes"):
        return None, "R05_E04_STRUCTURAL_ROUTES_ABSENT"
    rules = n9.get("rules") or {}
    for field in fields:
        if field.field_id not in rules:
            return None, "R05_WORLD_FIELD_ABSENT"
        expected = field.temporal_expected_value if (
            temporal and field.temporal_expected_value is not None
        ) else field.expected_value
        if rules[field.field_id].get("value") != expected:
            return None, "R05_WORLD_FIELD_VALUE_MISMATCH"
    selection = n9.get("selection") or {}
    if request.as_of_ref is not None and request.as_of_ref not in {
        selection.get("valid_at"), selection.get("published_asof")
    }:
        return None, "R05_AS_OF_MISMATCH"
    return receipt, None


def _validate_ff_admission(request: R05WorldConsumerRequest,
                           fields: tuple[R05WorldField, ...]) -> str | None:
    if any(field.role == "CONTEXT" for field in fields):
        return "CONTEXT_STRUCTURAL_AUTHORITY_HELD"
    return None


def _execute_p41_world(
    request: R05WorldConsumerRequest,
    context: R06TrustedExecutionContext,
) -> dict[str, Mapping[str, Any]]:
    actual = request.actual_execution
    if actual is not None:
        actual_pinned = _validate_pinned_runtime(actual.p41_runtime)
        if str(actual_pinned) != context.p41_runtime:
            raise WorldBindingError("UNTRUSTED_P41_RUNTIME")
        if actual.coordinator_original_ref != context.original_ref:
            raise WorldBindingError("R05_COORDINATOR_ORIGINAL_MISMATCH")
        if actual.learned_consumer is not context.learned_consumer:
            requested = actual.learned_consumer
            learned = context.learned_consumer
            if (learned.learned_receipt_ref != requested.learned_receipt_ref
                    or learned.m1_disposition_ref != requested.m1_disposition_ref
                    or learned.m2_release_ref != requested.m2_release_ref
                    or learned.consumer_result.result_hash
                    != requested.consumer_result.result_hash
                    or getattr(learned, "evidence_ref", None)
                    != getattr(requested, "evidence_ref", None)):
                raise WorldBindingError("R05_LEARNED_ORIGINAL_MISMATCH")
        if dict(actual.step) != dict(context.step):
            raise WorldBindingError("R05_ACTUAL_STEP_ORIGINAL_MISMATCH")
    requested = request.learned_consumer
    learned = context.learned_consumer
    if (learned.learned_receipt_ref != requested.learned_receipt_ref
            or learned.m1_disposition_ref != requested.m1_disposition_ref
            or learned.m2_release_ref != requested.m2_release_ref
            or learned.consumer_result.result_hash
            != requested.consumer_result.result_hash
            or getattr(learned, "evidence_ref", None)
            != getattr(requested, "evidence_ref", None)):
        raise WorldBindingError("R05_LEARNED_ORIGINAL_MISMATCH")
    pinned = Path(context.p41_runtime)
    _purge_p41_modules()
    if str(pinned) not in sys.path:
        sys.path.insert(0, str(pinned))
    import bootstrap
    bootstrap.install()
    import p41_service
    from p41_service import P41Service
    from product.world import SelectedWorldCatalog
    for module in (bootstrap, p41_service):
        module_file = Path(getattr(module, "__file__", "")).resolve()
        if pinned not in module_file.parents:
            raise WorldBindingError("UNTRUSTED_P41_MODULE_SUBSTITUTION")
    step = dict(context.step)
    if step.get("content_hash") != learned.consumer_result.result_hash:
        raise WorldBindingError("R05_ACTUAL_STEP_CONSUMER_MISMATCH")
    empirical = context.empirical
    source = empirical.get("source") or {}
    universe = source.get("universe")
    if universe is None or universe.ref != request.source_universe_ref:
        raise WorldBindingError("R05_ACTUAL_EMPIRICAL_SOURCE_MISMATCH")
    if source.get("release_ref") != request.release_ref:
        raise WorldBindingError("R05_ACTUAL_EMPIRICAL_RELEASE_MISMATCH")
    if empirical.get("rows_hash") != request.source_rows_hash:
        raise WorldBindingError("R05_ACTUAL_EMPIRICAL_ROWS_MISMATCH")
    catalog = SelectedWorldCatalog(
        empirical, structural_revision=context.structural_revision
    )
    snapshots = {
        "T0": catalog.select(mode="HISTORICAL", valid_at="2026-06-01",
                             published_asof="2026-04-15"),
    }
    if request.temporal_pair_ref is not None:
        snapshots["T1"] = catalog.select(
            mode="AS_OF", valid_at="2027-09-01", published_asof="2027-09-01"
        )

    step_conditions = tuple(
        tuple(item) for item in step.get("conditioners", (("X", 1),))
    )

    class R05Provider:
        def __init__(self):
            self.world = {"query_permits": {"Y": {}}}
            self.trace = []

        def _validate(self, target, ordered):
            if target != "Y" or tuple(tuple(c) for c in ordered) != step_conditions:
                raise ValueError("R06R3_R05_CONDITION_AUTHORITY")

        def progressive(self, target, ordered):
            self._validate(target, ordered)
            self.trace.append(dict(
                call="R05_LEARNED_CONSUMER_READ",
                consumer_result_hash=step["content_hash"],
            ))
            return [dict(step)]

    class R05StructuralService:
        def __init__(self, catalog):
            self.catalog = catalog
            self.value_reads = []

        def structural(self, snapshot, key, consumer):
            value = self.catalog.read(snapshot, key)
            self.value_reads.append(dict(
                consumer=consumer, key=key, state=value["state"],
                value=value.get("value"), snapshot_ref=snapshot.snapshot_hash,
            ))
            return value

        def possibilities(self, snapshot, *, target="Y",
                          conditions=step_conditions, consumer="GENERIC"):
            self.value_reads.append(dict(
                consumer=consumer, key="empirical", state="EXACT_SUPPORTED",
                value=step["cells"], snapshot_ref=snapshot.snapshot_hash,
            ))
            return dict(
                state="PRODUCTIVE_TEST_ONLY", steps=[dict(step)],
                dependencies=["empirical"], source_root="TEST_ONLY_E04_SOURCE_ROOT",
            )

        def _record(self, material):
            from copy import deepcopy
            material = deepcopy(material)
            material.update(
                service_contract="R06R3_R05_WORLD_SERVICE@1",
                grade="TEST_ONLY", operative_N9=False, operative_N10W=False,
                new_issuer=False, actor_executions=0, model_calls=0,
            )
            digest = semantic_hash(material)
            return dict(receipt_hash=digest, material=material)

    class R05P41Service(P41Service):
        def __init__(self, provider, structural):
            self.prepared = object()
            self.readthrough = structural
            self.provider = provider
            self.receipts = {}

        def _world_block(self, snapshot):
            block = super()._world_block(snapshot)
            block["r05_binding"] = {
                "source_universe_ref": request.source_universe_ref.as_dict(),
                "release_ref": request.release_ref.as_dict(),
                "source_rows_hash": request.source_rows_hash,
                "learned_receipt_ref": learned.learned_receipt_ref.as_dict(),
                "m1_disposition_ref": learned.m1_disposition_ref.as_dict(),
                "m2_release_ref": learned.m2_release_ref.as_dict(),
                "coordinator_original_ref": context.original_ref.as_dict(),
                "consumer_result_hash": learned.consumer_result.result_hash,
                "evidence_ref": (
                    None if learned.evidence_ref is None
                    else learned.evidence_ref.as_dict()
                ),
            }
            return block

    receipts = {}
    for label, snapshot in snapshots.items():
        provider = R05Provider()
        structural = R05StructuralService(catalog)
        service = R05P41Service(provider, structural)
        receipts[label] = service.progressive(
            target="Y", conditions=step_conditions, snapshot=snapshot
        )
    return receipts


def select_r05_world_view(request: R05WorldConsumerRequest) -> R05WorldSelectedView:
    """Invoke the actual P41/N9/N10W/E04 owner from admitted R05 inputs.

    The caller cannot supply the execution receipt. The host-retained
    `actual_execution` inputs are consumed by the actual pinned P41 service here.
    A caller callback or canned receipt is refused.
    """
    learned = request.learned_consumer
    if request.consumer is not None:
        return _r05_refusal("CALLER_CALLBACK_NOT_ACCEPTED", request)
    if getattr(learned, "state", None) != "LEARNED_CONSUMER_EXACT_SUPPORTED":
        return _r05_refusal("R05_LEARNED_CONSUMER_NOT_EXACT_SUPPORTED", request)
    if request.actual_execution is not None:
        try:
            _validate_pinned_runtime(request.actual_execution.p41_runtime)
        except WorldBindingError as exc:
            return _r05_refusal(exc.code, request)
    if not request.execution_handle:
        return _r05_refusal("TRUSTED_EXECUTION_HANDLE_REQUIRED", request)
    context = _TRUSTED_CONTEXTS.get(request.execution_handle)
    if context is None:
        return _r05_refusal("TRUSTED_EXECUTION_HANDLE_INVALID", request)
    if request.currentness != "CURRENT":
        return _r05_refusal("R05_CURRENTNESS_NOT_CURRENT", request)
    fields = tuple(request.fields)
    field_ids = tuple(field.field_id for field in fields)
    if len(fields) < 2:
        return _r05_refusal("R05_WORLD_REQUIRES_AT_LEAST_TWO_FIELDS", request, field_ids)
    if len(set(field_ids)) != len(fields):
        return _r05_refusal("R05_DUPLICATE_FIELD_BINDING", request, field_ids)
    units = {field.unit for field in fields}
    if len(units) > 1:
        return _r05_refusal("CROSS_UNIT_LINKED_QUERY_UNAVAILABLE", request, field_ids)
    ff_problem = _validate_ff_admission(request, fields)
    if ff_problem is not None:
        return _r05_refusal(ff_problem, request, field_ids)
    clocks = {field.clock_ref for field in fields if field.clock_ref is not None}
    if len(clocks) > 1:
        if (request.temporal_pair_ref is None or not request.observed_temporal_pair_refs
                or request.temporal_pair_ref not in request.observed_temporal_pair_refs):
            return _r05_refusal("UNOBSERVED_TEMPORAL_PAIR", request, field_ids)
    if request.temporal_pair_ref is not None:
        if request.temporal_pair_ref not in request.observed_temporal_pair_refs:
            return _r05_refusal("UNOBSERVED_TEMPORAL_PAIR", request, field_ids)
    try:
        receipts = _execute_p41_world(request, context)
    except WorldBindingError as exc:
        return _r05_refusal(exc.code, request, field_ids)
    except Exception as exc:
        return _r05_refusal("R05_ACTUAL_CONSUMER_REFUSED:" + type(exc).__name__, request, field_ids)
    if request.claimed_receipts is not None:
        for label, claimed in request.claimed_receipts.items():
            actual = receipts.get(label)
            if not isinstance(claimed, Mapping) or not isinstance(actual, Mapping):
                return _r05_refusal("R05_CLAIMED_RECEIPT_MISSING", request, field_ids)
            if claimed.get("content_hash") != actual.get("content_hash"):
                return _r05_refusal("R05_CLAIMED_RECEIPT_MISMATCH", request, field_ids)
    receipt_t0, problem = _validate_r05_receipt(
        receipts.get("T0"), request, fields, learned, temporal=False
    )
    if problem is not None:
        return _r05_refusal(problem, request, field_ids)
    temporal_changed = False
    receipt_t1 = None
    if request.temporal_pair_ref is not None:
        receipt_t1, problem = _validate_r05_receipt(
            receipts.get("T1"), request, fields, learned, temporal=True
        )
        if problem is not None:
            return _r05_refusal("R05_TEMPORAL_" + problem, request, field_ids)
        clock0 = (receipt_t0.get("n9_world") or {}).get("selection") or {}
        clock1 = (receipt_t1.get("n9_world") or {}).get("selection") or {}
        if (clock0.get("valid_at") == clock1.get("valid_at")
                or clock0.get("published_asof") == clock1.get("published_asof")):
            return _r05_refusal("R05_TEMPORAL_CLOCKS_NOT_DISTINCT", request, field_ids)
        if _actual_temporal_payload(receipt_t0) == _actual_temporal_payload(receipt_t1):
            return _r05_refusal("R05_TEMPORAL_PAIR_NOT_CONSUMED", request, field_ids)
        temporal_changed = True
    values = {
        "schema": "R95_R06R3_R05_WORLD_VIEW@1",
        "field_values": {field.field_id: field.expected_value for field in fields},
        "learned_receipt_ref": learned.learned_receipt_ref.as_dict(),
        "m1_disposition_ref": learned.m1_disposition_ref.as_dict(),
        "m2_release_ref": learned.m2_release_ref.as_dict(),
        "consumer_result_hash": learned.consumer_result.result_hash,
        "coordinator_original_ref": (
            receipt_t0.get("n9_world") or {}
        ).get("r05_binding", {}).get("coordinator_original_ref"),
        "source_universe_ref": request.source_universe_ref.as_dict(),
        "release_ref": request.release_ref.as_dict(),
        "source_rows_hash": request.source_rows_hash,
        "t0_receipt_hash": receipt_t0.get("content_hash"),
        "t0_routes": (receipt_t0.get("structural") or {}).get("routes"),
        "t0_clock": (receipt_t0.get("n9_world") or {}).get("selection"),
        "t0_n10e_steps": receipt_t0.get("n10e_steps"),
        "t0_n10w": receipt_t0.get("n10w"),
        "t1_receipt_hash": None if receipt_t1 is None else receipt_t1.get("content_hash"),
        "t1_routes": None if receipt_t1 is None else (receipt_t1.get("structural") or {}).get("routes"),
        "t1_clock": None if receipt_t1 is None else (receipt_t1.get("n9_world") or {}).get("selection"),
        "t1_n10e_steps": None if receipt_t1 is None else receipt_t1.get("n10e_steps"),
        "t1_n10w": None if receipt_t1 is None else receipt_t1.get("n10w"),
        "temporal_changed": temporal_changed,
        "z_unresolved": True,
    }
    return R05WorldSelectedView(
        state="R05_WORLD_SELECTED_VIEW", reason_code="ACTUAL_R05_TO_P41_VIEW",
        field_ids=field_ids, consumer_values_read=values,
        view_hash=semantic_hash(values), temporal_changed=temporal_changed,
    )
