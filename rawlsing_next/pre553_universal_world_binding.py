"""R95 R06 source-separated world selected-view binding (TEST_ONLY).

Binds independently typed source-indexed fields to the actual unchanged N10E
positioned-subject consumer through the accepted composition owner. It creates
no new evidence, geometry, pooling or temporal authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash


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
        if not request.relation_transport_authorized or request.relation_transport_ref is None:
            return _refusal("UNLINKED_UNIT_POOLING_UNAUTHORIZED", request, field_refs)
        if any(field.relation_ref != request.relation_transport_ref for field in fields):
            return _refusal("UNAUTHORIZED_TRANSPORT_RELATION", request, field_refs)
    if any(field.role == "CONTEXT" for field in fields) and request.ff_structural_authority_ref is None:
        return _refusal("CONTEXT_AS_STRUCTURAL_UNAUTHORIZED", request, field_refs)
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
        if not request.relation_transport_authorized or request.relation_transport_ref is None:
            return _joined_refusal("UNLINKED_UNIT_POOLING_UNAUTHORIZED", request, field_ids)
        if any(field.relation_ref != request.relation_transport_ref for field in fields):
            return _joined_refusal("UNAUTHORIZED_TRANSPORT_RELATION", request, field_ids)
    if any(field.role == "CONTEXT" for field in fields) and request.ff_structural_authority_ref is None:
        return _joined_refusal("CONTEXT_AS_STRUCTURAL_UNAUTHORIZED", request, field_ids)
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
