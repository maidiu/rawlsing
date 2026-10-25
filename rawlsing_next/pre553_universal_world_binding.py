"""R95 R06 source-separated world selected-view binding (TEST_ONLY).

Binds independently typed source-indexed fields to the actual unchanged N10E
positioned-subject consumer through the accepted composition owner. It creates
no new evidence, geometry, pooling or temporal authority.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, semantic_hash


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

    class R05Provider:
        def __init__(self):
            self.world = {"query_permits": {"Y": {}}}
            self.trace = []

        def _validate(self, target, ordered):
            if target != "Y" or tuple(tuple(c) for c in ordered) != (("X", 1),):
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
                          conditions=(("X", 1),), consumer="GENERIC"):
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
            target="Y", conditions=(("X", 1),), snapshot=snapshot
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


# ---------------------------------------------------------------------------
# R100 retained Afrobarometer R5 Q86 CONTEXT consumer.

Q86_SOURCE_COMMIT = "f148f9ba34deb0ae2ad3983fe94bbcef8f004b03"
Q86_TRANSPORT_PATH = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/"
    "R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/"
    "R4_E2A_RUNTIME_TRANSPORT_SEAL_R1/"
    "R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2"
)
Q86_OWNER_PATH = "rawlsing_next/pre553_repo_native_current_payload.py"
Q86_SOURCE_SHA256 = "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"
Q86_QUERY_SHA256 = "e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0"
Q86_FACT_SHA256 = "540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46"
Q86_RISK_SHA256 = "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b"
Q86_DENOMINATOR = 19_210
Q86_ROLE_ORDER = ("Q86B", "Q86A")
Q86_PURPOSE_CONTEXT = "SOCIAL_ATMOSPHERE_CONTEXT"
Q86_PURPOSE_CONTROL = "ENGINEERING_CONTROL"


@dataclass(frozen=True)
class Q86ContextEvidence:
    source: str
    source_sha256: str
    query_ref: ExactRef
    fact_ref: ExactRef
    conditioner_ref: ExactRef
    target_ref: ExactRef
    risk_ref: ExactRef
    relation_ref: ExactRef
    admission_ref: ExactRef
    f1_ref: ExactRef
    resolution_ref: ExactRef
    role_order: tuple[str, str]
    conditioner_domain: tuple[Any, ...]
    target_domain: tuple[Any, ...]
    cells: tuple[Mapping[str, Any], ...]
    denominator: int
    permission: str
    operative_current: bool
    temporal_grade: str
    v554_rule_material: Mapping[str, Any]
    payload: Mapping[str, Any]
    content_hash: str

    def material(self) -> Mapping[str, Any]:
        return {
            "source": self.source,
            "source_sha256": self.source_sha256,
            "query_ref": self.query_ref.as_dict(),
            "fact_ref": self.fact_ref.as_dict(),
            "conditioner_ref": self.conditioner_ref.as_dict(),
            "target_ref": self.target_ref.as_dict(),
            "risk_ref": self.risk_ref.as_dict(),
            "relation_ref": self.relation_ref.as_dict(),
            "admission_ref": self.admission_ref.as_dict(),
            "f1_ref": self.f1_ref.as_dict(),
            "resolution_ref": self.resolution_ref.as_dict(),
            "role_order": list(self.role_order),
            "conditioner_domain": list(self.conditioner_domain),
            "target_domain": list(self.target_domain),
            "cells": [canonicalize(cell) for cell in self.cells],
            "denominator": self.denominator,
            "permission": self.permission,
            "operative_current": self.operative_current,
            "temporal_grade": self.temporal_grade,
            "v554_rule_material": canonicalize(self.v554_rule_material),
            "payload": canonicalize(self.payload),
        }


@dataclass(frozen=True)
class Q86ContextRequest:
    evidence: Q86ContextEvidence
    purpose: str = Q86_PURPOSE_CONTEXT
    as_of_ref: str | None = None
    engineering_counterfactual_cells: tuple[Mapping[str, Any], ...] | None = None


@dataclass(frozen=True)
class Q86ContextView:
    state: str
    reason_code: str
    evidence_ref: ExactRef | None
    context_cells: tuple[Mapping[str, Any], ...]
    denominator: int
    permission: str
    p41_receipts: tuple[Mapping[str, Any], ...]
    p41_receipt_hashes: tuple[str, ...]
    structural_assertion: None
    actor_state: str
    nonoriginal: bool
    view_hash: str
    z_unresolved: bool = True

    def material(self) -> Mapping[str, Any]:
        return {
            "state": self.state,
            "reason_code": self.reason_code,
            "evidence_ref": None if self.evidence_ref is None else self.evidence_ref.as_dict(),
            "context_cells": [canonicalize(cell) for cell in self.context_cells],
            "denominator": self.denominator,
            "permission": self.permission,
            "p41_receipts": [canonicalize(receipt) for receipt in self.p41_receipts],
            "p41_receipt_hashes": list(self.p41_receipt_hashes),
            "structural_assertion": None,
            "actor_state": self.actor_state,
            "nonoriginal": self.nonoriginal,
            "view_hash": self.view_hash,
            "z_unresolved": self.z_unresolved,
        }


def _q86_exact(value: Any) -> ExactRef:
    if isinstance(value, ExactRef):
        return value
    if hasattr(value, "as_dict"):
        return ExactRef(**dict(value.as_dict()))
    if isinstance(value, Mapping):
        return ExactRef(**dict(value))
    raise WorldBindingError("Q86_EXACT_REF_REQUIRED")


def _q86_refusal(code: str) -> Q86ContextView:
    return Q86ContextView(
        state="REFUSED", reason_code=code, evidence_ref=None,
        context_cells=(), denominator=0, permission="CONTEXT_ONLY",
        p41_receipts=(), p41_receipt_hashes=(), structural_assertion=None,
        actor_state="NOT_TOUCHED", nonoriginal=False,
        view_hash=semantic_hash({"state": "REFUSED", "reason": code}),
    )


def _materialize_q86_owner():
    repo = Path(__file__).resolve().parents[1]
    base = Path(tempfile.mkdtemp(prefix="r100-q86-", dir=repo))
    archive = base / "q86-transport.tar"
    proc = subprocess.run(
        ["git", "-C", str(repo), "archive", Q86_SOURCE_COMMIT,
         Q86_TRANSPORT_PATH, Q86_OWNER_PATH, "-o", str(archive)],
        capture_output=True, text=True, timeout=300,
    )
    if proc.returncode != 0:
        shutil.rmtree(base, ignore_errors=True)
        raise WorldBindingError("Q86_TRANSPORT_PIN_UNAVAILABLE")
    with tarfile.open(archive) as handle:
        handle.extractall(base)
    module_path = base / Q86_OWNER_PATH
    spec = importlib.util.spec_from_file_location("r100_q86_payload", module_path)
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.load_current_gt2_query_fact_from_committed_transport(), base
    except Exception:
        shutil.rmtree(base, ignore_errors=True)
        raise


_Q86_QUERY_FACT_CACHE = None


def _load_q86_query_fact():
    global _Q86_QUERY_FACT_CACHE
    if _Q86_QUERY_FACT_CACHE is not None:
        return _Q86_QUERY_FACT_CACHE
    try:
        from rawlsing_next.pre553_repo_native_current_payload import (
            load_current_gt2_query_fact_from_committed_transport,
        )
        query_fact = load_current_gt2_query_fact_from_committed_transport()
    except FileNotFoundError:
        query_fact, base = _materialize_q86_owner()
        shutil.rmtree(base, ignore_errors=True)
    _Q86_QUERY_FACT_CACHE = query_fact
    return query_fact


def _q86_cells(relation: Any) -> tuple[Mapping[str, Any], ...]:
    cells = []
    seen = set()
    for row in relation.conditional_count_profile:
        conditioner = canonicalize(row["condition_state"])
        for target in row["target_counts"]:
            state = canonicalize(target["target_state"])
            key = (semantic_hash(conditioner), semantic_hash(state))
            if key in seen:
                raise WorldBindingError("Q86_DUPLICATE_JOINT_CELL")
            seen.add(key)
            cells.append({
                "conditioner": "Q86B",
                "conditioner_state": conditioner,
                "target": "Q86A",
                "target_state": state,
                "cell_state": target["cell_state"],
                "joint_support_count": int(target["joint_support_count"]),
            })
    if len(cells) != 36:
        raise WorldBindingError("Q86_JOINT_CELL_COUNT_MISMATCH")
    if sum(cell["joint_support_count"] for cell in cells) != Q86_DENOMINATOR:
        raise WorldBindingError("Q86_DENOMINATOR_MISMATCH")
    return tuple(cells)


_Q86_EVIDENCE_CACHE = None


def load_q86_context_evidence() -> Q86ContextEvidence:
    global _Q86_EVIDENCE_CACHE
    if _Q86_EVIDENCE_CACHE is not None:
        return _Q86_EVIDENCE_CACHE
    from rawlsing_next import field_forge_conditional_support as ff
    from rawlsing_next import gt12_c_to_d_relation_bridge as ff_admission
    from rawlsing_next import gt12_d_to_m4_typed_bridge as ff_world
    from rawlsing_next.gt12_e2b_publication_governance_binding import (
        load_current_gt12_e2b_publication_governance_binding,
    )
    query, fact = _load_q86_query_fact()
    if query.ref.content_hash != Q86_QUERY_SHA256 or fact.ref.content_hash != Q86_FACT_SHA256:
        raise WorldBindingError("Q86_FROZEN_QUERY_FACT_MISMATCH")
    if fact.typed_state != "SUPPORTED":
        raise WorldBindingError("Q86_FACT_NOT_SUPPORTED")
    relation = ff.produce_exact_conditional_support_profile(
        joint_fact=fact, joint_query=query,
        conditioner_ref=query.target_refs[0], target_ref=query.target_refs[1],
        producer_permission_ceiling=("STRUCTURAL_MEDIATION_INPUT",),
        relation_permission_ceiling=("STRUCTURAL_MEDIATION_INPUT",),
    )
    if relation.typed_state != "SUPPORTED" or relation.producer_state_blocking:
        raise WorldBindingError("Q86_RELATION_NOT_SUPPORTED")
    if _q86_exact(relation.risk_set_ref).content_hash != Q86_RISK_SHA256:
        raise WorldBindingError("Q86_RISK_MISMATCH")
    admission = ff_admission.admit_gt12_c_relation(relation).admission
    if admission.decision != "ADMITTED":
        raise WorldBindingError("Q86_ADMISSION_NOT_ADMITTED")
    if admission.target_use != "STRUCTURAL_MEDIATION_INPUT":
        raise WorldBindingError("Q86_ADMISSION_TARGET_USE_MISMATCH")
    if "STRUCTURAL_MEDIATION_INPUT" not in tuple(admission.target_use_permissions):
        raise WorldBindingError("Q86_ADMISSION_PERMISSION_MISMATCH")
    binding = load_current_gt12_e2b_publication_governance_binding()
    _, v554 = ff_world.evaluate_typed_d_to_e_at_v554(
        admission, governed_use_id=binding.governed_use_id,
        v554_rule_ref=binding.v554_rule_ref,
        publication_authority=binding.publication_authority,
    )
    if str(v554.decision_state).split(".")[-1] != "ELIGIBLE":
        raise WorldBindingError("Q86_V554_NOT_ELIGIBLE")
    if not isinstance(v554.f1, Mapping) or v554.f1.get("state") != "ELIGIBLE":
        raise WorldBindingError("Q86_F1_NOT_ELIGIBLE")
    terminal = ff_world.publish_and_resolve_relation_v554_at_current_m4(
        admission, v554, v557_allowed_uses=("CONTEXT",),
        requested_resolution_uses=("CONTEXT",),
        v557_authority_ref=binding.v557_authority_ref,
        v557_decision_state="ALLOW_CONTEXT_ONLY",
    )
    entries = terminal.resolution.resolved_entries
    if len(entries) != 1:
        raise WorldBindingError("Q86_EXACT_CONTEXT_ENTRY_REQUIRED")
    entry = entries[0]
    if tuple(entry.resolver_allowed_uses) != ("CONTEXT",):
        raise WorldBindingError("Q86_CONTEXT_PERMISSION_MISMATCH")
    if entry.decision_state != "ELIGIBLE":
        raise WorldBindingError("Q86_CONTEXT_NOT_ELIGIBLE")
    producer = next(
        (item.obj for item in terminal.repository.entries
         if item.obj.ref == entry.producer_object_ref), None
    )
    if producer is None or tuple(producer.producer_allowed_uses) != ("CONTEXT",):
        raise WorldBindingError("Q86_CONTEXT_PRODUCER_PERMISSION_MISMATCH")
    payload = canonicalize(producer.payload)
    if payload.get("family") != "F1" or payload.get("state") != "ELIGIBLE":
        raise WorldBindingError("Q86_F1_PAYLOAD_MISMATCH")
    relation_refs = payload.get("originating_field_forge_relation_exact_refs") or ()
    if [canonicalize(ref) for ref in relation_refs] != [relation.ref.as_dict()]:
        raise WorldBindingError("Q86_FF_LINEAGE_MISMATCH")
    cells = _q86_cells(relation)
    evidence_material = {
        "source": "Afrobarometer Round 5",
        "source_sha256": Q86_SOURCE_SHA256,
        "query_ref": query.ref.as_dict(),
        "fact_ref": fact.ref.as_dict(),
        "conditioner_ref": _q86_exact(relation.conditioner_ref).as_dict(),
        "target_ref": _q86_exact(relation.target_ref).as_dict(),
        "risk_ref": _q86_exact(relation.risk_set_ref).as_dict(),
        "relation_ref": relation.ref.as_dict(),
        "admission_ref": admission.ref.as_dict(),
        "f1_ref": _q86_exact(entry.producer_object_ref).as_dict(),
        "resolution_ref": terminal.resolution.receipt.ref.as_dict(),
        "role_order": list(Q86_ROLE_ORDER),
        "conditioner_domain": [canonicalize(value) for value in relation.conditioner_domain],
        "target_domain": [canonicalize(value) for value in relation.target_domain],
        "cells": [canonicalize(cell) for cell in cells],
        "denominator": Q86_DENOMINATOR,
        "permission": "CONTEXT_ONLY",
        "operative_current": False,
        "temporal_grade": "RETAINED_HISTORICAL_CONTEXT_NOT_OPERATIVE_CURRENT",
        "v554_rule_material": canonicalize(binding.v554_rule_ref),
        "payload": payload,
    }
    evidence = Q86ContextEvidence(
        source="Afrobarometer Round 5", source_sha256=Q86_SOURCE_SHA256,
        query_ref=query.ref, fact_ref=fact.ref,
        conditioner_ref=_q86_exact(relation.conditioner_ref),
        target_ref=_q86_exact(relation.target_ref),
        risk_ref=_q86_exact(relation.risk_set_ref),
        relation_ref=relation.ref, admission_ref=admission.ref,
        f1_ref=_q86_exact(entry.producer_object_ref),
        resolution_ref=terminal.resolution.receipt.ref,
        role_order=Q86_ROLE_ORDER,
        conditioner_domain=tuple(canonicalize(value) for value in relation.conditioner_domain),
        target_domain=tuple(canonicalize(value) for value in relation.target_domain),
        cells=cells, denominator=Q86_DENOMINATOR, permission="CONTEXT_ONLY",
        operative_current=False,
        temporal_grade="RETAINED_HISTORICAL_CONTEXT_NOT_OPERATIVE_CURRENT",
        v554_rule_material=canonicalize(binding.v554_rule_ref),
        payload=payload, content_hash=semantic_hash(evidence_material),
    )
    _Q86_EVIDENCE_CACHE = evidence
    return evidence


def _q86_p41_receipts(evidence: Q86ContextEvidence, cells: tuple[Mapping[str, Any], ...]):
    pinned = _pinned_p41_runtime()
    _purge_p41_modules()
    if str(pinned) not in sys.path:
        sys.path.insert(0, str(pinned))
    import bootstrap
    bootstrap.install()
    import p41_service
    from p41_service import P41Service
    for module in (bootstrap, p41_service):
        module_file = Path(getattr(module, "__file__", "")).resolve()
        if pinned not in module_file.parents:
            raise WorldBindingError("UNTRUSTED_P41_MODULE_SUBSTITUTION")
    grouped = {}
    for cell in cells:
        key = semantic_hash(cell["conditioner_state"])
        grouped.setdefault(key, []).append(cell)
    snapshot = SimpleNamespace(
        material={
            "mode": "HISTORICAL_RETAINED_CONTEXT",
            "valid_at": "RETAINED_ORIGINAL_TRANSPORT",
            "published_asof": "R100_CONTEXT_BINDING",
            "fields": {},
        },
        snapshot_hash="r100-q86-context",
    )

    class Q86Provider:
        def __init__(self, condition_state, row_cells):
            self.world = {"query_permits": {"Q86A": {"target_ref": evidence.target_ref.as_dict()}}}
            self.trace = []
            self.condition_state = condition_state
            self.row_cells = row_cells

        def _validate(self, target, ordered):
            if target != "Q86A" or len(ordered) != 1 or ordered[0][0] != "Q86B":
                raise ValueError("R100_Q86_ROLE_ORDER")

        def progressive(self, target, ordered):
            self._validate(target, ordered)
            step_cells = [
                {"cell": semantic_hash(cell["target_state"]),
                 "cell_state": cell["cell_state"],
                 "raw_numerator_support": cell["joint_support_count"]}
                for cell in self.row_cells
            ]
            step = {
                "state": "EXACT_SUPPORTED",
                "route": "RETAINED_Q86_CONTEXT",
                "target": "Q86A",
                "conditioners": [["Q86B", self.condition_state]],
                "denominator": sum(cell["joint_support_count"] for cell in self.row_cells),
                "cells": step_cells,
                "uncertainty": "UNCERTAINTY_UNQUANTIFIED",
                "evidence_ref": evidence.relation_ref.as_dict(),
                "producer_query_ref": evidence.query_ref.as_dict(),
                "producer_fact_ref": evidence.fact_ref.as_dict(),
                "model_rule_hash": evidence.v554_rule_material.get("hash"),
                "risk_set_ref": evidence.risk_ref.as_dict(),
                "release_ref": None,
                "content_hash": semantic_hash(step_cells),
            }
            self.trace.append({"call": "R100_Q86_CONTEXT_CONSUMED"})
            return [step]

    class Q86P41Service(P41Service):
        def __init__(self, provider):
            self.prepared = object()
            self.readthrough = None
            self.provider = provider
            self.receipts = {}

        def _world_block(self, snapshot):
            return {
                "selection": {
                    "mode": "HISTORICAL_RETAINED_CONTEXT",
                    "valid_at": "RETAINED_ORIGINAL_TRANSPORT",
                    "published_asof": "R100_CONTEXT_BINDING",
                },
                "rules": {},
                "source": {
                    "source": evidence.source,
                    "source_sha256": evidence.source_sha256,
                    "query_ref": evidence.query_ref.as_dict(),
                    "fact_ref": evidence.fact_ref.as_dict(),
                    "conditioner_ref": evidence.conditioner_ref.as_dict(),
                    "target_ref": evidence.target_ref.as_dict(),
                    "risk_set_ref": evidence.risk_ref.as_dict(),
                    "relation_ref": evidence.relation_ref.as_dict(),
                    "permission": evidence.permission,
                },
                "permission_root": "RETAINED_Q86_CONTEXT_ONLY",
                "currentness": evidence.temporal_grade,
            }

        def progressive(self, *args, **kwargs):
            core = super().progressive(*args, **kwargs)
            core["providers"] = {
                "n9_world": "R100_Q86_RETAINED_CONTEXT@1",
                "n10e_empirical": "R100_Q86_CONDITIONAL_SUPPORT@1",
                "n10w_progressive": "P41_GENERIC_POSSIBILITY_SERVICE@1",
                "learned_release": "NOT_APPLICABLE_RETAINED_Q86_CONTEXT",
            }
            core["consumer"] = {
                "name": "Q86_CONTEXT_READER",
                "permission_state": "CONTEXT_ONLY",
                "values_read": "actual retained Q86 conditional count profile",
            }
            core["q86_context_ref"] = evidence.relation_ref.as_dict()
            core.pop("content_hash", None)
            core["content_hash"] = semantic_hash(core)
            return core

    receipts = []
    for condition in evidence.conditioner_domain:
        key = semantic_hash(condition)
        row_cells = grouped.get(key)
        if not row_cells:
            raise WorldBindingError("Q86_CONDITIONER_ROW_MISSING")
        service = Q86P41Service(Q86Provider(condition, row_cells))
        receipt = service.progressive(
            target="Q86A", conditions=(("Q86B", condition),),
            snapshot=snapshot, world_part=False,
        )
        receipts.append(receipt)
    return tuple(receipts)


def receive_q86_context_view(request: Q86ContextRequest) -> Q86ContextView:
    if request.purpose not in {Q86_PURPOSE_CONTEXT, Q86_PURPOSE_CONTROL}:
        return _q86_refusal("Q86_PURPOSE_NOT_PERMITTED")
    if request.as_of_ref is not None:
        return _q86_refusal("Q86_AS_OF_NOT_APPLICABLE_TO_RETAINED_CONTEXT")
    if request.engineering_counterfactual_cells is not None and request.purpose != Q86_PURPOSE_CONTROL:
        return _q86_refusal("Q86_COUNTERFACTUAL_REQUIRES_ENGINEERING_CONTROL")
    try:
        actual = load_q86_context_evidence()
    except WorldBindingError as exc:
        return _q86_refusal(exc.code)
    except Exception as exc:
        return _q86_refusal("Q86_ACTUAL_OWNER_REFUSED:" + type(exc).__name__)
    if (not isinstance(request.evidence, Q86ContextEvidence)
            or request.evidence.content_hash != actual.content_hash
            or semantic_hash(request.evidence.material()) != semantic_hash(actual.material())):
        return _q86_refusal("Q86_EVIDENCE_SEVERED")
    if actual.permission != "CONTEXT_ONLY" or actual.operative_current:
        return _q86_refusal("Q86_PERMISSION_OR_CURRENTNESS_MISMATCH")
    if request.purpose == Q86_PURPOSE_CONTROL:
        cells = tuple(canonicalize(cell) for cell in (
            request.engineering_counterfactual_cells or actual.cells
        ))
        nonoriginal = True
    else:
        cells = actual.cells
        nonoriginal = False
    if len(cells) != 36 or sum(cell["joint_support_count"] for cell in cells) != Q86_DENOMINATOR:
        return _q86_refusal("Q86_CONTEXT_CELL_GEOMETRY_MISMATCH")
    try:
        receipts = _q86_p41_receipts(actual, cells)
    except WorldBindingError as exc:
        return _q86_refusal(exc.code)
    except Exception as exc:
        return _q86_refusal("Q86_P41_CONSUMER_REFUSED:" + type(exc).__name__)
    if len(receipts) != 6:
        return _q86_refusal("Q86_P41_CONTEXT_RECEIPT_COUNT_MISMATCH")
    for receipt in receipts:
        if (receipt.get("schema") != "PYAT_R41_P41_GENERIC_POSSIBILITY_RECEIPT@1"
                or receipt.get("service") != "P41_GENERIC_POSSIBILITY_SERVICE@1"
                or receipt.get("structural") is not None
                or not receipt.get("n10e_steps")
                or not (receipt.get("n10w") or {}).get("positioned_consumptions")):
            return _q86_refusal("Q86_P41_CONTEXT_CONSUMER_MISMATCH")
    material = {
        "state": "NONORIGINAL_CONTEXT_CONTROL" if nonoriginal else "Q86_CONTEXT_SELECTED_VIEW",
        "source": actual.source,
        "source_sha256": actual.source_sha256,
        "query_ref": actual.query_ref.as_dict(),
        "fact_ref": actual.fact_ref.as_dict(),
        "conditioner_ref": actual.conditioner_ref.as_dict(),
        "target_ref": actual.target_ref.as_dict(),
        "risk_ref": actual.risk_ref.as_dict(),
        "relation_ref": actual.relation_ref.as_dict(),
        "admission_ref": actual.admission_ref.as_dict(),
        "f1_ref": actual.f1_ref.as_dict(),
        "resolution_ref": actual.resolution_ref.as_dict(),
        "permission": actual.permission,
        "temporal_grade": actual.temporal_grade,
        "context_cells": [canonicalize(cell) for cell in cells],
        "denominator": sum(cell["joint_support_count"] for cell in cells),
        "p41_receipt_hashes": [receipt["content_hash"] for receipt in receipts],
        "p41_receipts": [canonicalize(receipt) for receipt in receipts],
        "structural_assertion": None,
        "actor_state": "NOT_TOUCHED",
        "nonoriginal": nonoriginal,
    }
    return Q86ContextView(
        state=material["state"],
        reason_code="ACTUAL_RETAINED_Q86_CONTEXT" if not nonoriginal else "ENGINEERING_COUNTERFACTUAL",
        evidence_ref=actual.relation_ref,
        context_cells=cells, denominator=material["denominator"],
        permission=actual.permission, p41_receipts=receipts,
        p41_receipt_hashes=tuple(material["p41_receipt_hashes"]),
        structural_assertion=None, actor_state="NOT_TOUCHED",
        nonoriginal=nonoriginal, view_hash=semantic_hash(material),
    )
