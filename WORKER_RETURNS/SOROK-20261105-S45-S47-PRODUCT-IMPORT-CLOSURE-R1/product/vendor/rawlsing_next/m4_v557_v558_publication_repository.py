#!/usr/bin/env python3
"""Clean-sideline runtime for frozen M4 V557 publication / V558 repository law.

This module contains no reads from stage-close artifacts. All semantic authority is
supplied through exact immutable inputs produced by the accepted M1/M2/M3 runtimes.
V557 and V558 remain logically distinct even when used in one process.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from rawlsing_next.m1_temporal_v554_admission_dedup import (
    M1_CONTRACT_ID,
    M1DecisionState,
    M1Evaluation,
    SCR554_CONTRACT_ID,
    semantic_hash,
)
from rawlsing_next.m2_v555_atomic_route import (
    M2_CONTRACT_ID,
    M2DecisionState,
    M2Evaluation,
    SCR555_CONTRACT_ID,
    SEMANTIC_FAMILY as V555_SEMANTIC_FAMILY,
)
from rawlsing_next.m3_v556_higher_order_structural import (
    M3_CONTRACT_ID,
    M3DecisionState,
    M3Evaluation,
    SCR556_CONTRACT_ID,
    V556_SEMANTIC_FAMILIES,
)

M4_CONTRACT_ID = "M4_SCR5578_MIXED_PRODUCER_FINAL_SEAM@1.0.0"
SCR5578_CONTRACT_ID = "SCR5578_PUBLICATION_REPOSITORY_RESOLUTION_EXACT_CONTRACT@1.0.0"
V557_PUBLICATION_SCHEMA = "SCR5578_V557_IMMUTABLE_PUBLICATION_BUNDLE@1.0.0"
V558_REPOSITORY_SCHEMA = "SCR5578_STRUCTURAL_PRIOR_REPOSITORY@1.0.0"
V558_LOCATOR_SCHEMA = "SCR5578_PRODUCER_PRESERVING_OBJECT_LOCATOR@1.0.0"
V558_RESOLUTION_RECEIPT_SCHEMA = "SCR5578_V558_CONTEXT_RESOLUTION_RECEIPT@1.0.0"
V558_SELECTION_RECORD_SCHEMA = "SCR5578_V558_SELECTION_RECORD@1.0.0"
RSC_SCHEMA = "SCR5578_RESOLVED_STRUCTURAL_CONTEXT@1.0.0"
RESOLVER_POLICY_ID = "V558_CONTEXT_RESOLVER_POLICY"
RESOLVER_POLICY_VERSION = "1.0.0"
RESOLVER_POLICY_HASH = "4e34517b78547ef555c4025abff4f682b6eb201a3dfda2cce2c4ec3bec9b6f2f"

PERMISSION_ATOMS = frozenset({"REVIEW", "CONTEXT", "ACTIVE_CAUSAL"})
ALLOWED_ROOT_FAMILIES = frozenset({"V553", "V554", "V555", "V556"})
MANDATORY_LOGICAL_INDEXES = frozenset({
    "OBJECT_IDENTITY", "TEMPORAL", "GEOGRAPHIC", "FINITE_STRATUM",
    "GENERATED_POSITION_REQUIREMENT", "NEGATIVE_LIMIT", "PROVENANCE",
})
AUDIT_ONLY_CLASSES = frozenset({"DiscoveryResultReceipt", "ReplayReceipt"})
FORBIDDEN_CLASSES = frozenset({
    "PositionedSubjectEmpiricalPossibilityField", "PSEPF",
    "V3EmpiricalPossibilityInput", "ActorComparatorReceipt",
    "RenderedExpression_or_Persona",
})
_SHA = re.compile(r"^[0-9a-f]{64}$")
_V555_ROUTE_ID = re.compile(r"^urn:rawlsing:v555:route:sha256:([0-9a-f]{64})$")
_V556_OBJECT_ID = re.compile(r"^urn:rawlsing:v556:higher-order:sha256:([0-9a-f]{64})$")


class M4IntegrityError(ValueError):
    pass


class PermissionWideningError(M4IntegrityError):
    pass


class ClosureIntegrityError(M4IntegrityError):
    pass


class ReferenceClassError(M4IntegrityError):
    pass


class V557DecisionState(str, Enum):
    ALLOW_ACTIVE_CAUSAL_CONTEXT = "ALLOW_ACTIVE_CAUSAL_CONTEXT"
    ALLOW_CONTEXT_ONLY = "ALLOW_CONTEXT_ONLY"
    ALLOW_REVIEW_ONLY = "ALLOW_REVIEW_ONLY"
    DENY_CAUSAL_USE = "DENY_CAUSAL_USE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class V557ExceptionState(str, Enum):
    NO_EXCEPTION_STATE = "NO_EXCEPTION_STATE"
    NEGATIVE_AUTHORITY = "NEGATIVE_AUTHORITY"
    MISSING_AUTHORITY = "MISSING_AUTHORITY"
    NONCOMPARABLE = "NONCOMPARABLE"
    VALID_EMPTY = "VALID_EMPTY"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"


_STATE_CEILING = {
    V557DecisionState.ALLOW_ACTIVE_CAUSAL_CONTEXT: frozenset(PERMISSION_ATOMS),
    V557DecisionState.ALLOW_CONTEXT_ONLY: frozenset({"REVIEW", "CONTEXT"}),
    V557DecisionState.ALLOW_REVIEW_ONLY: frozenset({"REVIEW"}),
    V557DecisionState.DENY_CAUSAL_USE: frozenset(),
    V557DecisionState.NOT_APPLICABLE: frozenset(),
}


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise M4IntegrityError(f"{name} must be a non-empty string")
    out = value.strip()
    if out.lower() in {"latest", "default", "*"}:
        raise M4IntegrityError(f"{name} may not use latest/default/fuzzy selection")
    return out


def _hash(value: Any, name: str) -> str:
    out = _text(value, name)
    if not _SHA.fullmatch(out):
        raise M4IntegrityError(f"{name} must be lowercase sha256")
    return out


def _freeze(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise M4IntegrityError("floats are forbidden in immutable M4 semantic material")
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        if any(not isinstance(k, str) for k in value):
            raise M4IntegrityError("immutable mapping keys must be strings")
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return tuple(_freeze(v) for v in value)
    raise M4IntegrityError(f"unsupported immutable material type {type(value).__name__}")


def _uses(values: Any, name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise M4IntegrityError(f"{name} must be a sequence")
    out = tuple(sorted({_text(v, name) for v in values}))
    if not set(out) <= PERMISSION_ATOMS:
        raise M4IntegrityError(f"{name} contains non-frozen permission atoms")
    return out


def _ref_key(ref: "ExactRef") -> tuple[str, str, str]:
    return ref.kind, ref.object_id, ref.content_hash


def _is_forbidden_class(name: str) -> bool:
    if name in FORBIDDEN_CLASSES:
        return True
    upper = name.upper()
    return (
        upper.startswith("V2_") or upper.startswith("V3_") or
        "ACTOR" in upper or "PERSONA" in upper or "PHENOMENOLOG" in upper or
        "RENDER" in upper or "VOICE" in upper or "PSYCHE" in upper
    )


def _safe_storage_locator(value: str, *, content_hash: str) -> str:
    out = _text(value, "storage_locator")
    lower = out.lower()
    forbidden = ("http://", "https://", "data/ddm_build", "raw_stage", "raw-stage", "/latest", ":latest")
    if any(token in lower for token in forbidden):
        raise M4IntegrityError("storage locator uses forbidden raw/latest/network repair surface")
    if not (out.startswith("bundle://") or out == f"cas://sha256/{content_hash}"):
        raise M4IntegrityError("storage locator must be bundle-local or exact content-addressed CAS")
    return out


@dataclass(frozen=True)
class ExactRef:
    kind: str
    object_id: str
    content_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", _text(self.kind, "ref.kind"))
        object.__setattr__(self, "object_id", _text(self.object_id, "ref.object_id"))
        object.__setattr__(self, "content_hash", _hash(self.content_hash, "ref.content_hash"))

    def as_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "object_id": self.object_id, "content_hash": self.content_hash}


@dataclass(frozen=True)
class AuthorityRef:
    authority_id: str
    authority_version: str
    authority_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "authority_id", _text(self.authority_id, "authority_id"))
        object.__setattr__(self, "authority_version", _text(self.authority_version, "authority_version"))
        object.__setattr__(self, "authority_hash", _hash(self.authority_hash, "authority_hash"))

    def as_dict(self) -> dict[str, str]:
        return {"id": self.authority_id, "version": self.authority_version, "content_hash": self.authority_hash}


def exact_ref(value: Any, name: str = "exact_ref") -> ExactRef:
    if isinstance(value, ExactRef):
        return value
    if not isinstance(value, Mapping) or set(value) != {"kind", "object_id", "content_hash"}:
        raise M4IntegrityError(f"{name} must contain exactly kind/object_id/content_hash")
    return ExactRef(value["kind"], value["object_id"], value["content_hash"])


@dataclass(frozen=True)
class StructuralObject:
    producer_family: str
    semantic_class: str
    object_id: str
    content_hash: str
    schema_id: str
    schema_version: str
    typed_state: str
    producer_allowed_uses: tuple[str, ...]
    payload: Mapping[str, Any] | None
    source_stage: str
    required_dependency_refs: tuple[ExactRef, ...] = ()
    negative_dependency_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "producer_family", _text(self.producer_family, "producer_family"))
        object.__setattr__(self, "semantic_class", _text(self.semantic_class, "semantic_class"))
        object.__setattr__(self, "object_id", _text(self.object_id, "object_id"))
        object.__setattr__(self, "content_hash", _hash(self.content_hash, "content_hash"))
        object.__setattr__(self, "schema_id", _text(self.schema_id, "schema_id"))
        object.__setattr__(self, "schema_version", _text(self.schema_version, "schema_version"))
        object.__setattr__(self, "typed_state", _text(self.typed_state, "typed_state"))
        object.__setattr__(self, "source_stage", _text(self.source_stage, "source_stage"))
        object.__setattr__(self, "producer_allowed_uses", _uses(self.producer_allowed_uses, "producer_allowed_uses"))
        req = tuple(sorted((exact_ref(x, "required_dependency_ref") for x in self.required_dependency_refs), key=_ref_key))
        neg = tuple(sorted((exact_ref(x, "negative_dependency_ref") for x in self.negative_dependency_refs), key=_ref_key))
        object.__setattr__(self, "required_dependency_refs", req)
        object.__setattr__(self, "negative_dependency_refs", neg)
        if self.payload is not None:
            frozen = _freeze(self.payload)
            if semantic_hash(frozen) != self.content_hash:
                raise M4IntegrityError("producer content hash does not match immutable payload")
            object.__setattr__(self, "payload", frozen)

    @property
    def ref(self) -> ExactRef:
        return ExactRef(self.semantic_class, self.object_id, self.content_hash)


def make_structural_object(
    *, producer_family: str, semantic_class: str, object_id: str,
    schema_id: str, schema_version: str, typed_state: str,
    producer_allowed_uses: Sequence[str], payload: Mapping[str, Any], source_stage: str,
    required_dependency_refs: Sequence[ExactRef | Mapping[str, str]] = (),
    negative_dependency_refs: Sequence[ExactRef | Mapping[str, str]] = (),
) -> StructuralObject:
    frozen = _freeze(payload)
    return StructuralObject(
        producer_family, semantic_class, object_id, semantic_hash(frozen), schema_id,
        schema_version, typed_state, tuple(producer_allowed_uses), frozen, source_stage,
        tuple(exact_ref(x) for x in required_dependency_refs),
        tuple(exact_ref(x) for x in negative_dependency_refs),
    )


def make_external_stub(
    *, producer_family: str, semantic_class: str, object_id: str, content_hash: str,
    schema_id: str, schema_version: str, typed_state: str,
    producer_allowed_uses: Sequence[str], source_stage: str,
) -> StructuralObject:
    return StructuralObject(
        producer_family, semantic_class, object_id, content_hash, schema_id,
        schema_version, typed_state, tuple(producer_allowed_uses), None, source_stage,
    )


def structural_objects_from_m1(
    evaluation: M1Evaluation, *, producer_allowed_uses: Sequence[str],
) -> tuple[StructuralObject, ...]:
    if not isinstance(evaluation, M1Evaluation) or evaluation.contract_id != M1_CONTRACT_ID:
        raise M4IntegrityError("M1 adapter requires exact accepted M1Evaluation")
    handoff = evaluation.direct_v557_handoff
    if handoff is None:
        return ()
    if not isinstance(handoff, Mapping) or handoff.get("route") != "V554_TO_V557_DIRECT":
        raise M4IntegrityError("M1 direct handoff route is not exact V554->V557")
    refs = handoff.get("object_refs")
    if isinstance(refs, (str, bytes)) or not isinstance(refs, Sequence):
        raise M4IntegrityError("M1 direct handoff object_refs malformed")
    payloads: dict[str, tuple[str, Mapping[str, Any], str]] = {}
    if evaluation.f1 is not None:
        payloads[evaluation.f1["f1_id"]] = ("F1", evaluation.f1, evaluation.f1.get("state", evaluation.decision_state.value))
    for f2 in evaluation.f2:
        payloads[f2["f2_id"]] = ("F2", f2, f2.get("disposition", evaluation.decision_state.value))
    if evaluation.b1 is not None:
        payloads[evaluation.b1["b1_id"]] = ("B1", evaluation.b1, evaluation.b1.get("decision_state", evaluation.decision_state.value))
    out: list[StructuralObject] = []
    for raw in refs:
        if not isinstance(raw, Mapping) or set(raw) != {"family", "object_id", "content_hash"}:
            raise M4IntegrityError("M1 direct publication ref fields are not exact")
        oid = _text(raw["object_id"], "M1.object_id")
        family = _text(raw["family"], "M1.family")
        h = _hash(raw["content_hash"], "M1.content_hash")
        if oid not in payloads or payloads[oid][0] != family:
            raise M4IntegrityError("M1 handoff ref does not resolve to exact producer object")
        _, payload, state = payloads[oid]
        if semantic_hash(payload) != h:
            raise M4IntegrityError("M1 handoff object hash mismatch")
        out.append(make_structural_object(
            producer_family="V554", semantic_class=family, object_id=oid,
            schema_id=SCR554_CONTRACT_ID, schema_version="1.0.0", typed_state=state,
            producer_allowed_uses=producer_allowed_uses, payload=payload,
            source_stage="M1_DIRECT_V554_TO_V557",
        ))
    return tuple(out)


def structural_object_from_m2(evaluation: M2Evaluation, *, require_direct_handoff: bool = True) -> StructuralObject:
    if not isinstance(evaluation, M2Evaluation) or evaluation.contract_id != M2_CONTRACT_ID:
        raise M4IntegrityError("M2 adapter requires exact accepted M2Evaluation")
    if evaluation.decision_state is not M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED or not isinstance(evaluation.route, Mapping):
        raise M4IntegrityError("only exact positive V555 route may be publication root")
    route = evaluation.route
    ident = evaluation.canonical_route_identity
    if not isinstance(ident, tuple) or len(ident) != 7 or tuple(route.get("canonical_route_identity", ())) != ident:
        raise M4IntegrityError("V555 seven-field canonical identity not preserved")
    ih = semantic_hash(list(ident))
    rid = route.get("route_id")
    match = _V555_ROUTE_ID.fullmatch(rid) if isinstance(rid, str) else None
    if not match or match.group(1) != ih or evaluation.canonical_route_identity_hash != ih or route.get("canonical_route_identity_hash") != ih:
        raise M4IntegrityError("V555 route id/hash no longer addresses exact seven-field identity")
    if route.get("semantic_family") != V555_SEMANTIC_FAMILY:
        raise M4IntegrityError("V555 semantic family mismatch")
    if evaluation.exact_v554_f1_ref is None:
        raise M4IntegrityError("positive V555 route lacks exact accepted V554 F1 reference")
    f1_ref = exact_ref(evaluation.exact_v554_f1_ref, "V555.F1")
    if ident[0] != f1_ref.object_id:
        raise M4IntegrityError("V555 route tuple field 1 no longer equals exact V554 F1 identity")
    forbidden_ids: list[str] = []
    if evaluation.exact_v554_b1_ref is not None:
        forbidden_ids.append(exact_ref(evaluation.exact_v554_b1_ref, "V555.B1").object_id)
    forbidden_ids.extend(exact_ref(x, "V555.F2").object_id for x in evaluation.inherited_v554_f2_refs)
    if any(fid in repr(ident) for fid in forbidden_ids):
        raise M4IntegrityError("B1/F2 may not be promoted into seven-field V555 semantic identity")
    ordered = route.get("ordered_structure")
    if isinstance(ordered, (str, bytes)) or not isinstance(ordered, Sequence) or len(ordered) != 3:
        raise M4IntegrityError("V555 ordered SOURCE->MEDIATION_LOCUS->RECEIVER structure missing")
    if not all(isinstance(x, Mapping) for x in ordered):
        raise M4IntegrityError("V555 ordered structure entries malformed")
    if tuple(x.get("role") for x in ordered) != ("SOURCE", "MEDIATION_LOCUS", "RECEIVER"):
        raise M4IntegrityError("V555 source/mediation/receiver role order corrupted")
    if ordered[1].get("channel_structural_role_id") != ident[3] or exact_ref(ordered[1].get("binding"), "V555.channel") != exact_ref(ident[4], "V555.identity.channel"):
        raise M4IntegrityError("V555 channel role/binding differs from canonical route tuple")
    if ordered[2].get("receiving_constraint_kind") != ident[5] or exact_ref(ordered[2].get("binding"), "V555.receiver") != exact_ref(ident[6], "V555.identity.receiver"):
        raise M4IntegrityError("V555 receiver constraint/binding differs from canonical route tuple")
    deps: list[ExactRef] = [f1_ref]
    if evaluation.exact_v554_b1_ref is not None:
        deps.append(exact_ref(evaluation.exact_v554_b1_ref, "V555.B1"))
    deps.extend(exact_ref(x, "V555.F2") for x in evaluation.inherited_v554_f2_refs)
    if require_direct_handoff:
        handoff = evaluation.direct_v557_handoff
        if not isinstance(handoff, Mapping) or handoff.get("route") != "V555_TO_V557_DIRECT":
            raise M4IntegrityError("V555 direct publication requires exact M2 direct V557 handoff")
        rr = exact_ref(handoff.get("route_ref"), "V555.direct_handoff.route_ref")
        expected = ExactRef(V555_SEMANTIC_FAMILY, rid, semantic_hash(route))
        if rr != expected:
            raise M4IntegrityError("V555 direct handoff re-identifies or corrupts route")
    return make_structural_object(
        producer_family="V555", semantic_class=V555_SEMANTIC_FAMILY, object_id=rid,
        schema_id=SCR555_CONTRACT_ID, schema_version="stage-close-r03-1",
        typed_state=evaluation.decision_state.value,
        producer_allowed_uses=route.get("producer_allowed_uses", ()),
        payload=route, source_stage="M2_DIRECT_V555_TO_V557",
        required_dependency_refs=deps,
    )


def _v556_cardinality_marker(rule: Mapping[str, Any]) -> str:
    minimum = rule.get("minimum_cardinality")
    maximum = rule.get("maximum_cardinality_or_unbounded_marker")
    if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 2:
        raise M4IntegrityError("V556 rule minimum cardinality invalid")
    if maximum == "UNBOUNDED":
        return f"{minimum}..n"
    if not isinstance(maximum, int) or isinstance(maximum, bool) or maximum < minimum:
        raise M4IntegrityError("V556 rule maximum cardinality invalid")
    return str(minimum) if minimum == maximum else f"{minimum}..{maximum}"


def structural_object_from_m3(evaluation: M3Evaluation) -> StructuralObject:
    if not isinstance(evaluation, M3Evaluation) or evaluation.contract_id != M3_CONTRACT_ID:
        raise M4IntegrityError("M3 adapter requires exact accepted M3Evaluation")
    if evaluation.decision_state is not M3DecisionState.SUPPORTED or not isinstance(evaluation.v556_object, Mapping):
        raise M4IntegrityError("only exact SUPPORTED V556 object may be positive publication root")
    obj = evaluation.v556_object
    oid = obj.get("object_id")
    match = _V556_OBJECT_ID.fullmatch(oid) if isinstance(oid, str) else None
    replay = obj.get("replay_key_hash")
    if not match or match.group(1) != replay or evaluation.replay_key_hash != replay:
        raise M4IntegrityError("V556 object identity/replay binding mismatch")
    family = _text(obj.get("semantic_family"), "V556.semantic_family")
    if family not in V556_SEMANTIC_FAMILIES:
        raise M4IntegrityError("V556 semantic family outside frozen M3 contract")
    rule = obj.get("rule_authority")
    if not isinstance(rule, Mapping) or rule.get("semantic_family") != family:
        raise M4IntegrityError("V556 object lacks exact owning rule authority")
    _v556_cardinality_marker(rule)
    raw_bindings = obj.get("participant_bindings")
    if isinstance(raw_bindings, (str, bytes)) or not isinstance(raw_bindings, Sequence) or len(raw_bindings) < 2:
        raise M4IntegrityError("V556 object lacks exact 2..n participant bindings")
    minimum = rule["minimum_cardinality"]
    maximum = rule["maximum_cardinality_or_unbounded_marker"]
    if len(raw_bindings) < minimum or (maximum != "UNBOUNDED" and len(raw_bindings) > maximum):
        raise M4IntegrityError("V556 participant occurrence count violates exact owning rule")
    order_policy = rule.get("participant_order_policy")
    if order_policy not in {"ORDERED", "UNORDERED"}:
        raise M4IntegrityError("V556 participant order policy invalid")
    allowed_roles = rule.get("participant_roles")
    if isinstance(allowed_roles, (str, bytes)) or not isinstance(allowed_roles, Sequence) or not allowed_roles:
        raise M4IntegrityError("V556 participant role authority invalid")
    reuse = rule.get("same_route_reuse_policy")
    if reuse not in {"FORBIDDEN", "PERMITTED"}:
        raise M4IntegrityError("V556 same-route reuse policy invalid")
    deps: list[ExactRef] = []
    distinct: set[tuple[str, str, str]] = set()
    occurrences: dict[tuple[str, str, str], list[int]] = {}
    ordinals: list[int | None] = []
    roles: list[str] = []
    for binding in raw_bindings:
        if not isinstance(binding, Mapping) or set(binding) != {"v555_route_identity_ref", "role", "ordinal_or_null", "multiplicity_index"}:
            raise M4IntegrityError("V556 participant role/order/cardinality/multiplicity binding corrupted")
        ref = exact_ref(binding["v555_route_identity_ref"], "V556.participant.route_ref")
        role = _text(binding["role"], "V556.participant.role")
        if role not in set(allowed_roles):
            raise M4IntegrityError("V556 participant role outside exact owning rule")
        ordinal = binding["ordinal_or_null"]
        multi = binding["multiplicity_index"]
        if ordinal is not None and (not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal < 1):
            raise M4IntegrityError("V556 participant ordinal invalid")
        if not isinstance(multi, int) or isinstance(multi, bool) or multi < 0:
            raise M4IntegrityError("V556 participant multiplicity invalid")
        deps.append(ref)
        key = _ref_key(ref)
        distinct.add(key)
        occurrences.setdefault(key, []).append(multi)
        ordinals.append(ordinal)
        roles.append(role)
    if len(distinct) < 2:
        raise M4IntegrityError("positive V556 object requires at least two distinct V555 routes")
    if any(len(v) > 1 for v in occurrences.values()) and reuse != "PERMITTED":
        raise M4IntegrityError("V556 same-route reuse exceeds exact owning rule")
    for values in occurrences.values():
        if sorted(values) != list(range(len(values))):
            raise M4IntegrityError("V556 multiplicity indexes no longer describe exact occurrences")
    if order_policy == "ORDERED":
        if any(x is None for x in ordinals) or sorted(ordinals) != list(range(1, len(raw_bindings) + 1)):
            raise M4IntegrityError("ordered V556 rule requires contiguous semantic ordinals")
        if len(allowed_roles) > 1 and tuple(roles) != tuple(allowed_roles):
            raise M4IntegrityError("V556 ordered role pattern differs from exact owning rule")
    elif any(x is not None for x in ordinals):
        raise M4IntegrityError("unordered V556 rule requires null participant ordinals")
    return make_structural_object(
        producer_family="V556", semantic_class=family, object_id=oid,
        schema_id=SCR556_CONTRACT_ID, schema_version="scr556.v1",
        typed_state=evaluation.decision_state.value,
        producer_allowed_uses=obj.get("producer_allowed_uses", ()), payload=obj,
        source_stage="M3_V556_TO_V557", required_dependency_refs=deps,
    )


@dataclass(frozen=True)
class V557GovernanceRecord:
    record_id: str
    object_ref: ExactRef
    decision_state: V557DecisionState
    exception_state: V557ExceptionState
    producer_allowed_uses: tuple[str, ...]
    v557_allowed_uses: tuple[str, ...]
    authority_ref: AuthorityRef
    record_hash: str

    @property
    def ref(self) -> ExactRef:
        return ExactRef("V557_GOVERNANCE_RECORD", self.record_id, self.record_hash)


def _governance_material(record: V557GovernanceRecord) -> dict[str, Any]:
    return {
        "m4_contract_id": M4_CONTRACT_ID,
        "object_ref": record.object_ref.as_dict(),
        "producer_allowed_uses": list(record.producer_allowed_uses),
        "v557_allowed_uses": list(record.v557_allowed_uses),
        "decision_state": record.decision_state.value,
        "exception_state": record.exception_state.value,
        "authority_ref": record.authority_ref.as_dict(),
    }


def govern_v557(
    obj: StructuralObject, *, decision_state: V557DecisionState | str,
    v557_allowed_uses: Sequence[str], authority_ref: AuthorityRef,
    exception_state: V557ExceptionState | str = V557ExceptionState.NO_EXCEPTION_STATE,
) -> V557GovernanceRecord:
    if not isinstance(obj, StructuralObject):
        raise M4IntegrityError("V557 governance requires exact StructuralObject")
    try:
        state = V557DecisionState(decision_state)
        exc = V557ExceptionState(exception_state)
    except ValueError as e:
        raise M4IntegrityError("unknown frozen V557 governance/exception state") from e
    allowed = _uses(v557_allowed_uses, "v557_allowed_uses")
    producer = obj.producer_allowed_uses
    if not set(allowed) <= set(producer):
        raise PermissionWideningError("V557 allowed uses widen producer permission")
    if not set(allowed) <= _STATE_CEILING[state]:
        raise PermissionWideningError("V557 allowed uses exceed governance-state ceiling")
    provisional = V557GovernanceRecord(
        "PENDING", obj.ref, state, exc, producer, allowed, authority_ref, "0" * 64,
    )
    h = semantic_hash(_governance_material(provisional))
    return V557GovernanceRecord(f"V557GOV:{h}", obj.ref, state, exc, producer, allowed, authority_ref, h)


@dataclass(frozen=True)
class V557PublicationEntry:
    obj: StructuralObject
    governance: V557GovernanceRecord

    def __post_init__(self) -> None:
        if self.governance.object_ref != self.obj.ref:
            raise M4IntegrityError("V557 governance record does not bind exact producer object")
        if tuple(self.governance.producer_allowed_uses) != tuple(self.obj.producer_allowed_uses):
            raise PermissionWideningError("V557 record producer ceiling differs from producer object")
        if not set(self.governance.v557_allowed_uses) <= set(self.obj.producer_allowed_uses):
            raise PermissionWideningError("V557 record widens producer permission")
        if not set(self.governance.v557_allowed_uses) <= _STATE_CEILING[self.governance.decision_state]:
            raise PermissionWideningError("V557 record exceeds governance-state ceiling")
        if semantic_hash(_governance_material(self.governance)) != self.governance.record_hash or self.governance.record_id != f"V557GOV:{self.governance.record_hash}":
            raise M4IntegrityError("V557 governance record identity/hash is stale or corrupt")


@dataclass(frozen=True)
class V557PublicationBundle:
    publication_id: str
    publication_hash: str
    schema: str
    entries: tuple[V557PublicationEntry, ...]

    @property
    def ref(self) -> ExactRef:
        return ExactRef("V557_PUBLICATION_BUNDLE", self.publication_id, self.publication_hash)


def _publication_material(entries: Sequence[V557PublicationEntry]) -> dict[str, Any]:
    return {
        "schema": V557_PUBLICATION_SCHEMA,
        "m4_contract_id": M4_CONTRACT_ID,
        "entries": [
            {"object_ref": e.obj.ref.as_dict(), "producer_family": e.obj.producer_family,
             "typed_state": e.obj.typed_state, "governance_ref": e.governance.ref.as_dict()}
            for e in entries
        ],
    }


def build_v557_publication_bundle(entries: Sequence[V557PublicationEntry]) -> V557PublicationBundle:
    if isinstance(entries, (str, bytes)) or not isinstance(entries, Sequence):
        raise M4IntegrityError("publication entries must be sequence")
    normalized = tuple(sorted(entries, key=lambda e: (e.obj.producer_family, e.obj.object_id, e.obj.content_hash)))
    seen: dict[tuple[str, str], str] = {}
    for entry in normalized:
        if not isinstance(entry, V557PublicationEntry):
            raise M4IntegrityError("publication bundle contains non-entry")
        if entry.obj.producer_family not in ALLOWED_ROOT_FAMILIES:
            raise ReferenceClassError("publication root family must be exact V553/V554/V555/V556")
        if _is_forbidden_class(entry.obj.semantic_class) or entry.obj.semantic_class in AUDIT_ONLY_CLASSES:
            raise ReferenceClassError("forbidden/audit-only class may not be V557 semantic root")
        key = (entry.obj.producer_family, entry.obj.object_id)
        old = seen.setdefault(key, entry.obj.content_hash)
        if old != entry.obj.content_hash:
            raise M4IntegrityError("same producer identity appears with different content hash")
    h = semantic_hash(_publication_material(normalized))
    return V557PublicationBundle(f"V557PUB:{h}", h, V557_PUBLICATION_SCHEMA, normalized)


@dataclass(frozen=True)
class ProducerLocator:
    locator_id: str
    logical_collection_kind: str
    authoritative_producer_family: str
    authoritative_object_id: str
    authoritative_object_hash: str
    authoritative_build_id: str
    authoritative_build_hash: str
    producer_schema_id: str
    producer_schema_version: str
    producer_contract_id: str
    producer_contract_version: str
    producer_contract_hash: str
    producer_rule_bindings: tuple[AuthorityRef, ...]
    v557_governance_ref: ExactRef
    content_blob_hash: str
    storage_locator: str
    provenance_locator: str
    locator_hash: str

    @property
    def ref(self) -> ExactRef:
        return ExactRef("V558_LOCATOR", self.locator_id, self.locator_hash)


def _locator_material(locator: ProducerLocator) -> dict[str, Any]:
    return {
        "schema": V558_LOCATOR_SCHEMA,
        "logical_collection_kind": locator.logical_collection_kind,
        "authoritative_producer_family": locator.authoritative_producer_family,
        "authoritative_object_id": locator.authoritative_object_id,
        "authoritative_object_hash": locator.authoritative_object_hash,
        "authoritative_build_id": locator.authoritative_build_id,
        "authoritative_build_hash": locator.authoritative_build_hash,
        "producer_schema_id": locator.producer_schema_id,
        "producer_schema_version": locator.producer_schema_version,
        "producer_contract_id": locator.producer_contract_id,
        "producer_contract_version": locator.producer_contract_version,
        "producer_contract_hash": locator.producer_contract_hash,
        "producer_rule_bindings": [x.as_dict() for x in locator.producer_rule_bindings],
        "v557_governance_ref": locator.v557_governance_ref.as_dict(),
        "content_blob_hash": locator.content_blob_hash,
        "storage_locator": locator.storage_locator,
        "provenance_locator": locator.provenance_locator,
    }


def make_producer_locator(
    obj: StructuralObject, governance: V557GovernanceRecord, *, logical_collection_kind: str,
    authoritative_build_id: str, authoritative_build_hash: str,
    producer_contract_id: str, producer_contract_version: str, producer_contract_hash: str,
    producer_rule_bindings: Sequence[AuthorityRef] = (), storage_locator: str | None = None,
    provenance_locator: str | None = None,
) -> ProducerLocator:
    if governance.object_ref != obj.ref:
        raise M4IntegrityError("locator governance does not bind exact object")
    bindings = tuple(producer_rule_bindings)
    if any(not isinstance(x, AuthorityRef) for x in bindings):
        raise M4IntegrityError("producer_rule_bindings must be exact AuthorityRef values")
    storage = _safe_storage_locator(storage_locator or f"bundle://objects/{obj.content_hash}", content_hash=obj.content_hash)
    provenance = _text(provenance_locator or f"audit://{obj.producer_family}/{obj.object_id}", "provenance_locator")
    draft = ProducerLocator(
        "PENDING", _text(logical_collection_kind, "logical_collection_kind"), obj.producer_family,
        obj.object_id, obj.content_hash, _text(authoritative_build_id, "authoritative_build_id"),
        _hash(authoritative_build_hash, "authoritative_build_hash"), obj.schema_id, obj.schema_version,
        _text(producer_contract_id, "producer_contract_id"),
        _text(producer_contract_version, "producer_contract_version"),
        _hash(producer_contract_hash, "producer_contract_hash"), bindings, governance.ref,
        obj.content_hash, storage, provenance, "0" * 64,
    )
    h = semantic_hash(_locator_material(draft))
    return ProducerLocator(
        f"V558LOC:{h}", draft.logical_collection_kind, draft.authoritative_producer_family,
        draft.authoritative_object_id, draft.authoritative_object_hash, draft.authoritative_build_id,
        draft.authoritative_build_hash, draft.producer_schema_id, draft.producer_schema_version,
        draft.producer_contract_id, draft.producer_contract_version, draft.producer_contract_hash,
        draft.producer_rule_bindings, draft.v557_governance_ref, draft.content_blob_hash,
        draft.storage_locator, draft.provenance_locator, h,
    )


@dataclass(frozen=True)
class ReferenceEdge:
    source_locator_ref: ExactRef
    target_locator_ref: ExactRef
    reference_contract: AuthorityRef
    edge_role: str
    requiredness: str
    participant_role: str
    declared_cardinality: str
    multiplicity_key: str
    order_significant: bool
    semantic_ordinal: int | None
    edge_hash: str


def _edge_material(edge: ReferenceEdge) -> dict[str, Any]:
    return {
        "source_locator_ref": edge.source_locator_ref.as_dict(),
        "target_locator_ref": edge.target_locator_ref.as_dict(),
        "reference_contract_id_version_hash": edge.reference_contract.as_dict(),
        "edge_role": edge.edge_role, "requiredness": edge.requiredness,
        "participant_role": edge.participant_role,
        "declared_cardinality": edge.declared_cardinality,
        "multiplicity_key": edge.multiplicity_key,
        "order_significant": edge.order_significant,
        "semantic_ordinal": edge.semantic_ordinal,
    }


def make_reference_edge(
    source: ProducerLocator, target: ProducerLocator, *, reference_contract: AuthorityRef,
    edge_role: str, requiredness: str = "REQUIRED", participant_role: str = "NONE",
    declared_cardinality: str = "1", multiplicity_key: str = "0",
    order_significant: bool = False, semantic_ordinal: int | None = None,
) -> ReferenceEdge:
    req = _text(requiredness, "requiredness")
    if req not in {"REQUIRED", "OPTIONAL"}:
        raise M4IntegrityError("requiredness must be REQUIRED or OPTIONAL")
    if not isinstance(order_significant, bool):
        raise M4IntegrityError("order_significant must be boolean")
    if semantic_ordinal is not None and (not isinstance(semantic_ordinal, int) or isinstance(semantic_ordinal, bool) or semantic_ordinal < 1):
        raise M4IntegrityError("semantic_ordinal must be positive integer or null")
    draft = ReferenceEdge(
        source.ref, target.ref, reference_contract, _text(edge_role, "edge_role"), req,
        _text(participant_role, "participant_role"), _text(declared_cardinality, "declared_cardinality"),
        _text(multiplicity_key, "multiplicity_key"), order_significant, semantic_ordinal, "0" * 64,
    )
    return ReferenceEdge(
        draft.source_locator_ref, draft.target_locator_ref, draft.reference_contract,
        draft.edge_role, draft.requiredness, draft.participant_role, draft.declared_cardinality,
        draft.multiplicity_key, draft.order_significant, draft.semantic_ordinal,
        semantic_hash(_edge_material(draft)),
    )


@dataclass(frozen=True)
class ExternalResolutionBinding:
    object_ref: ExactRef
    storage_locator: str
    resolver_authority: AuthorityRef
    binding_id: str
    binding_hash: str


def make_external_resolution_binding(
    obj: StructuralObject, *, resolver_authority: AuthorityRef,
) -> ExternalResolutionBinding:
    if obj.payload is not None:
        raise M4IntegrityError("external resolution binding is only for metadata-only immutable stub")
    storage = f"cas://sha256/{obj.content_hash}"
    material = {"object_ref": obj.ref.as_dict(), "storage_locator": storage, "resolver_authority": resolver_authority.as_dict()}
    h = semantic_hash(material)
    return ExternalResolutionBinding(obj.ref, storage, resolver_authority, f"V558EXT:{h}", h)


@dataclass(frozen=True)
class RepositoryEntry:
    obj: StructuralObject
    governance: V557GovernanceRecord
    locator: ProducerLocator

    def __post_init__(self) -> None:
        V557PublicationEntry(self.obj, self.governance)
        loc = self.locator
        if (
            loc.authoritative_producer_family != self.obj.producer_family or
            loc.authoritative_object_id != self.obj.object_id or
            loc.authoritative_object_hash != self.obj.content_hash or
            loc.content_blob_hash != self.obj.content_hash or
            loc.v557_governance_ref != self.governance.ref or
            loc.producer_schema_id != self.obj.schema_id or
            loc.producer_schema_version != self.obj.schema_version
        ):
            raise M4IntegrityError("producer locator does not reversibly preserve exact producer tuple")
        if semantic_hash(_locator_material(loc)) != loc.locator_hash or loc.locator_id != f"V558LOC:{loc.locator_hash}":
            raise M4IntegrityError("producer locator identity/hash is stale or corrupt")


@dataclass(frozen=True)
class IndexRecord:
    index_name: str
    key: str
    locator_ref: ExactRef

    def __post_init__(self) -> None:
        object.__setattr__(self, "index_name", _text(self.index_name, "index_name"))
        object.__setattr__(self, "key", _hash(self.key, "index_key"))


@dataclass(frozen=True)
class LogicalIndexManifest:
    manifest_id: str
    manifest_hash: str
    declared_indexes: tuple[str, ...]
    records: tuple[IndexRecord, ...]

    @property
    def ref(self) -> ExactRef:
        return ExactRef("V558_INDEX_MANIFEST", self.manifest_id, self.manifest_hash)


def exact_resolution_key(locator: ProducerLocator) -> str:
    return semantic_hash({
        "logical_collection_kind": locator.logical_collection_kind,
        "producer_family": locator.authoritative_producer_family,
        "object_id": locator.authoritative_object_id,
        "content_hash": locator.authoritative_object_hash,
    })


def _index_material(declared: Sequence[str], records: Sequence[IndexRecord]) -> dict[str, Any]:
    return {
        "declared_indexes": sorted(declared),
        "records": [
            {"index_name": r.index_name, "key": r.key, "locator_ref": r.locator_ref.as_dict()}
            for r in sorted(records, key=lambda r: (r.index_name, r.key, _ref_key(r.locator_ref)))
        ],
    }


def make_index_manifest(
    entries: Sequence[RepositoryEntry], *, supplemental_records: Sequence[IndexRecord] = (),
) -> LogicalIndexManifest:
    records = [IndexRecord("OBJECT_IDENTITY", exact_resolution_key(e.locator), e.locator.ref) for e in entries]
    records.extend(supplemental_records)
    declared = tuple(sorted(MANDATORY_LOGICAL_INDEXES | {r.index_name for r in records}))
    h = semantic_hash(_index_material(declared, records))
    return LogicalIndexManifest(f"V558IDX:{h}", h, declared, tuple(records))


@dataclass(frozen=True)
class V558RepositoryBundle:
    repository_id: str
    repository_hash: str
    schema: str
    publication_bundle_ref: ExactRef
    entries: tuple[RepositoryEntry, ...]
    reference_edges: tuple[ReferenceEdge, ...]
    external_bindings: tuple[ExternalResolutionBinding, ...]
    index_manifest: LogicalIndexManifest

    @property
    def ref(self) -> ExactRef:
        return ExactRef("V558_REPOSITORY_BUNDLE", self.repository_id, self.repository_hash)


def _repository_material_from_ref(
    publication_ref: ExactRef, entries: Sequence[RepositoryEntry], edges: Sequence[ReferenceEdge],
    external: Sequence[ExternalResolutionBinding], index_manifest: LogicalIndexManifest,
) -> dict[str, Any]:
    return {
        "schema": V558_REPOSITORY_SCHEMA,
        "m4_contract_id": M4_CONTRACT_ID,
        "publication_bundle_ref": publication_ref.as_dict(),
        "entries": [
            {"object_ref": e.obj.ref.as_dict(), "producer_family": e.obj.producer_family,
             "typed_state": e.obj.typed_state, "governance_ref": e.governance.ref.as_dict(),
             "locator_ref": e.locator.ref.as_dict()}
            for e in entries
        ],
        "reference_edges": [e.edge_hash for e in edges],
        "external_bindings": [b.binding_id for b in external],
        "index_manifest_ref": index_manifest.ref.as_dict(),
    }


def _validate_v556_participant_edges(
    entry: RepositoryEntry, entries_by_object: Mapping[tuple[str, str, str], RepositoryEntry],
    edges_by_source: Mapping[tuple[str, str, str], Sequence[ReferenceEdge]],
) -> None:
    obj = entry.obj
    if obj.producer_family != "V556" or obj.typed_state != M3DecisionState.SUPPORTED.value:
        return
    payload = obj.payload
    if not isinstance(payload, Mapping):
        raise ClosureIntegrityError("positive V556 object must be packaged for participant-shape validation")
    bindings = payload.get("participant_bindings")
    rule = payload.get("rule_authority")
    if not isinstance(rule, Mapping):
        raise ClosureIntegrityError("positive V556 object lacks owning rule authority in packaged payload")
    expected_cardinality = _v556_cardinality_marker(rule)
    if isinstance(bindings, (str, bytes)) or not isinstance(bindings, Sequence) or len(bindings) < 2:
        raise ClosureIntegrityError("positive V556 object has incomplete participant set")
    source_edges = [e for e in edges_by_source.get(_ref_key(entry.locator.ref), ()) if e.edge_role == "PARTICIPANT"]
    if len(source_edges) != len(bindings):
        raise ClosureIntegrityError("partial n-ary V556 participant closure is forbidden")
    used: set[str] = set()
    distinct: set[tuple[str, str, str]] = set()
    for raw in bindings:
        if not isinstance(raw, Mapping) or set(raw) != {"v555_route_identity_ref", "role", "ordinal_or_null", "multiplicity_index"}:
            raise ClosureIntegrityError("V556 participant binding fields corrupted")
        rr = exact_ref(raw["v555_route_identity_ref"], "V556.participant")
        distinct.add(_ref_key(rr))
        target = entries_by_object.get(_ref_key(rr))
        if target is None or target.obj.producer_family != "V555":
            raise ClosureIntegrityError("V556 participant does not resolve to exact V555 producer object")
        role = _text(raw["role"], "participant.role")
        ordinal = raw["ordinal_or_null"]
        multi = raw["multiplicity_index"]
        matches = [
            e for e in source_edges
            if e.edge_hash not in used and e.target_locator_ref == target.locator.ref and
            e.participant_role == role and e.semantic_ordinal == ordinal and
            e.multiplicity_key == str(multi) and e.order_significant == (ordinal is not None) and
            e.declared_cardinality == expected_cardinality and e.requiredness == "REQUIRED"
        ]
        if len(matches) != 1:
            raise ClosureIntegrityError("V556 role/order/cardinality/multiplicity edge does not exactly survive packaging")
        used.add(matches[0].edge_hash)
    if len(distinct) < 2:
        raise ClosureIntegrityError("positive V556 object collapsed below distinct-route floor")


def build_v558_repository_bundle(
    publication: V557PublicationBundle, entries: Sequence[RepositoryEntry], *,
    reference_edges: Sequence[ReferenceEdge] = (),
    external_bindings: Sequence[ExternalResolutionBinding] = (),
    index_manifest: LogicalIndexManifest | None = None,
) -> V558RepositoryBundle:
    if not isinstance(publication, V557PublicationBundle):
        raise M4IntegrityError("V558 repository requires exact distinct V557 publication bundle")
    expected_pub_hash = semantic_hash(_publication_material(publication.entries))
    if publication.schema != V557_PUBLICATION_SCHEMA or publication.publication_hash != expected_pub_hash or publication.publication_id != f"V557PUB:{expected_pub_hash}":
        raise M4IntegrityError("V557 publication bundle identity/hash is stale or corrupt")
    normalized = tuple(sorted(entries, key=lambda e: (e.obj.producer_family, e.obj.object_id, e.obj.content_hash)))
    edges = tuple(sorted(reference_edges, key=lambda e: e.edge_hash))
    external = tuple(sorted(external_bindings, key=lambda b: b.binding_id))
    by_object: dict[tuple[str, str, str], RepositoryEntry] = {}
    by_locator: dict[tuple[str, str, str], RepositoryEntry] = {}
    by_identity: dict[str, str] = {}
    for entry in normalized:
        if not isinstance(entry, RepositoryEntry):
            raise M4IntegrityError("repository entries must be exact RepositoryEntry values")
        if _is_forbidden_class(entry.obj.semantic_class):
            raise ReferenceClassError("actor/V3/V2/persona/render object rejected from StructuralPriorRepository")
        oid_old = by_identity.setdefault(entry.obj.object_id, entry.obj.content_hash)
        if oid_old != entry.obj.content_hash:
            raise M4IntegrityError("same semantic object id with different hash is integrity failure")
        if _ref_key(entry.obj.ref) in by_object or _ref_key(entry.locator.ref) in by_locator:
            raise M4IntegrityError("duplicate object or locator in immutable repository")
        by_object[_ref_key(entry.obj.ref)] = entry
        by_locator[_ref_key(entry.locator.ref)] = entry
    roots = {(e.obj.ref, e.governance.ref) for e in publication.entries}
    present = {(e.obj.ref, e.governance.ref) for e in normalized}
    if not roots <= present:
        raise ClosureIntegrityError("atomic publication root missing from repository bundle")
    edge_by_source: dict[tuple[str, str, str], list[ReferenceEdge]] = {}
    for edge in edges:
        if _ref_key(edge.source_locator_ref) not in by_locator or _ref_key(edge.target_locator_ref) not in by_locator:
            raise ClosureIntegrityError("reference edge locator is missing or stale")
        if semantic_hash(_edge_material(edge)) != edge.edge_hash:
            raise ClosureIntegrityError("reference edge hash mismatch")
        edge_by_source.setdefault(_ref_key(edge.source_locator_ref), []).append(edge)
    binding_map: dict[tuple[str, str, str], ExternalResolutionBinding] = {}
    for binding in external:
        if binding.storage_locator != f"cas://sha256/{binding.object_ref.content_hash}":
            raise ClosureIntegrityError("external binding is not exact content-addressed resolution")
        material = {"object_ref": binding.object_ref.as_dict(), "storage_locator": binding.storage_locator, "resolver_authority": binding.resolver_authority.as_dict()}
        if semantic_hash(material) != binding.binding_hash or binding.binding_id != f"V558EXT:{binding.binding_hash}":
            raise ClosureIntegrityError("external binding hash/identity mismatch")
        if _ref_key(binding.object_ref) in binding_map:
            raise ClosureIntegrityError("ambiguous multiple external bindings for exact object")
        binding_map[_ref_key(binding.object_ref)] = binding
    for entry in normalized:
        if entry.obj.payload is None and _ref_key(entry.obj.ref) not in binding_map:
            raise ClosureIntegrityError("metadata-only dependency lacks exact immutable hash-bound resolution binding")
        _validate_v556_participant_edges(entry, by_object, edge_by_source)
        declared = tuple(entry.obj.required_dependency_refs) + tuple(entry.obj.negative_dependency_refs)
        for dep in declared:
            target = by_object.get(_ref_key(dep))
            if target is None:
                raise ClosureIntegrityError("required positive/negative dependency absent from standalone repository")
            matches = [
                e for e in edge_by_source.get(_ref_key(entry.locator.ref), ())
                if e.target_locator_ref == target.locator.ref and e.requiredness == "REQUIRED"
            ]
            if not matches:
                raise ClosureIntegrityError("required positive/negative dependency lacks exact role-preserving edge")
    manifest = index_manifest or make_index_manifest(normalized)
    if not MANDATORY_LOGICAL_INDEXES <= set(manifest.declared_indexes):
        raise ClosureIntegrityError("repository logical index manifest is incomplete")
    expected_identity = {(exact_resolution_key(e.locator), _ref_key(e.locator.ref)) for e in normalized}
    actual_identity = {(r.key, _ref_key(r.locator_ref)) for r in manifest.records if r.index_name == "OBJECT_IDENTITY"}
    if actual_identity != expected_identity:
        raise ClosureIntegrityError("OBJECT_IDENTITY index is incomplete, stale, or ambiguous")
    index_material = _index_material(manifest.declared_indexes, manifest.records)
    if semantic_hash(index_material) != manifest.manifest_hash or manifest.manifest_id != f"V558IDX:{manifest.manifest_hash}":
        raise ClosureIntegrityError("logical index manifest hash mismatch")
    material = _repository_material_from_ref(publication.ref, normalized, edges, external, manifest)
    h = semantic_hash(material)
    return V558RepositoryBundle(f"V558REPO:{h}", h, V558_REPOSITORY_SCHEMA, publication.ref, normalized, edges, external, manifest)


@dataclass(frozen=True)
class ContextQueryItem:
    resolution_key: str
    requested_uses: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "resolution_key", _hash(self.resolution_key, "resolution_key"))
        uses = _uses(self.requested_uses, "requested_uses")
        if not uses:
            raise M4IntegrityError("resolution query item must request at least one exact permission atom")
        object.__setattr__(self, "requested_uses", uses)


@dataclass(frozen=True)
class ContextQuery:
    query_id: str
    query_hash: str
    items: tuple[ContextQueryItem, ...]
    generated_binding_refs: tuple[ExactRef, ...]


def _query_material(items: Sequence[ContextQueryItem], bindings: Sequence[ExactRef]) -> dict[str, Any]:
    return {
        "items": [{"resolution_key": i.resolution_key, "requested_uses": list(i.requested_uses)} for i in items],
        "generated_binding_refs": [x.as_dict() for x in bindings],
    }


def make_context_query(
    items: Sequence[ContextQueryItem], *, generated_binding_refs: Sequence[ExactRef | Mapping[str, str]] = (),
) -> ContextQuery:
    normalized = tuple(items)
    if len({i.resolution_key for i in normalized}) != len(normalized):
        raise M4IntegrityError("duplicate exact resolution key in ContextQuery")
    bindings = tuple(sorted((exact_ref(x) for x in generated_binding_refs), key=_ref_key))
    h = semantic_hash(_query_material(normalized, bindings))
    return ContextQuery(f"V558QUERY:{h}", h, normalized, bindings)


@dataclass(frozen=True)
class ResolverPolicy:
    policy_id: str = RESOLVER_POLICY_ID
    policy_version: str = RESOLVER_POLICY_VERSION
    policy_hash: str = RESOLVER_POLICY_HASH

    def __post_init__(self) -> None:
        if (self.policy_id, self.policy_version, self.policy_hash) != (RESOLVER_POLICY_ID, RESOLVER_POLICY_VERSION, RESOLVER_POLICY_HASH):
            raise M4IntegrityError("resolver policy must be exact frozen M4 policy; latest/default substitution forbidden")

    def as_dict(self) -> dict[str, str]:
        return {"id": self.policy_id, "version": self.policy_version, "content_hash": self.policy_hash}


@dataclass(frozen=True)
class SelectionRecord:
    selection_record_id: str
    selection_record_hash: str
    resolution_key: str
    locator_ref: ExactRef | None
    producer_object_ref: ExactRef | None
    producer_allowed_uses: tuple[str, ...]
    v557_allowed_uses: tuple[str, ...]
    resolver_allowed_uses: tuple[str, ...]
    typed_state: str | None
    decision: str
    reason: str
    closure_digest: str | None

    @property
    def ref(self) -> ExactRef:
        return ExactRef("V558_SELECTION_RECORD", self.selection_record_id, self.selection_record_hash)


@dataclass(frozen=True)
class ResolvedEntry:
    resolution_key: str
    selection_record_ref: ExactRef
    canonical_producer_family: str
    producer_object_ref: ExactRef
    producer_locator_ref: ExactRef
    resolver_allowed_uses: tuple[str, ...]
    decision_state: str


@dataclass(frozen=True)
class ResolutionReceipt:
    receipt_id: str
    receipt_hash: str
    schema: str
    result_state: str
    selection_record_refs: tuple[ExactRef, ...]
    resolved_entry_refs: tuple[ExactRef, ...]
    unresolved_keys: tuple[str, ...]
    replay_input_digest: str

    @property
    def ref(self) -> ExactRef:
        return ExactRef("V558_RESOLUTION_RECEIPT", self.receipt_id, self.receipt_hash)


@dataclass(frozen=True)
class ResolutionResult:
    selection_records: tuple[SelectionRecord, ...]
    resolved_entries: tuple[ResolvedEntry, ...]
    receipt: ResolutionReceipt
    resolved_structural_context: None = None


def _selection(
    *, repository: V558RepositoryBundle, query: ContextQuery, policy: ResolverPolicy,
    item: ContextQueryItem, entry: RepositoryEntry | None, decision: str, reason: str,
    resolver_allowed_uses: Sequence[str] = (), closure_digest: str | None = None,
) -> SelectionRecord:
    material = {
        "schema": V558_SELECTION_RECORD_SCHEMA,
        "repository_ref": repository.ref.as_dict(),
        "index_manifest_ref": repository.index_manifest.ref.as_dict(),
        "query_id": query.query_id, "query_hash": query.query_hash,
        "resolver_policy": policy.as_dict(), "resolution_key": item.resolution_key,
        "locator_ref": entry.locator.ref.as_dict() if entry else None,
        "producer_object_ref": entry.obj.ref.as_dict() if entry else None,
        "producer_allowed_uses": list(entry.obj.producer_allowed_uses) if entry else [],
        "v557_allowed_uses": list(entry.governance.v557_allowed_uses) if entry else [],
        "resolver_allowed_uses": list(resolver_allowed_uses),
        "typed_state": entry.obj.typed_state if entry else None,
        "decision": decision, "reason": reason, "closure_digest": closure_digest,
    }
    h = semantic_hash(material)
    return SelectionRecord(
        f"V558SEL:{h}", h, item.resolution_key, entry.locator.ref if entry else None,
        entry.obj.ref if entry else None, entry.obj.producer_allowed_uses if entry else (),
        entry.governance.v557_allowed_uses if entry else (), tuple(resolver_allowed_uses),
        entry.obj.typed_state if entry else None, decision, reason, closure_digest,
    )


def _entry_body(entry: RepositoryEntry, external_store: Mapping[str, Mapping[str, Any]]) -> Mapping[str, Any]:
    if entry.obj.payload is not None:
        if semantic_hash(entry.obj.payload) != entry.obj.content_hash:
            raise ClosureIntegrityError("packaged object hash changed after repository construction")
        return entry.obj.payload
    raw = external_store.get(entry.obj.object_id)
    if not isinstance(raw, Mapping):
        raise ClosureIntegrityError("exact external immutable object is unavailable")
    frozen = _freeze(raw)
    if semantic_hash(frozen) != entry.obj.content_hash:
        raise ClosureIntegrityError("external immutable object hash mismatch")
    return frozen


def _transitive_entries(root: RepositoryEntry, repository: V558RepositoryBundle) -> tuple[RepositoryEntry, ...]:
    by_locator = {_ref_key(e.locator.ref): e for e in repository.entries}
    adjacency: dict[tuple[str, str, str], list[ExactRef]] = {}
    for edge in repository.reference_edges:
        if edge.requiredness == "REQUIRED":
            adjacency.setdefault(_ref_key(edge.source_locator_ref), []).append(edge.target_locator_ref)
    out: list[RepositoryEntry] = []
    seen: set[tuple[str, str, str]] = set()
    stack = [root]
    while stack:
        entry = stack.pop()
        key = _ref_key(entry.locator.ref)
        if key in seen:
            continue
        seen.add(key)
        out.append(entry)
        for target_ref in adjacency.get(key, ()):
            target = by_locator.get(_ref_key(target_ref))
            if target is None:
                raise ClosureIntegrityError("required closure target disappeared from immutable repository")
            stack.append(target)
    return tuple(sorted(out, key=lambda e: (e.obj.producer_family, e.obj.object_id, e.obj.content_hash)))


def _validate_repository_checksum(repository: V558RepositoryBundle) -> None:
    if repository.schema != V558_REPOSITORY_SCHEMA:
        raise ClosureIntegrityError("repository schema mismatch")
    index_material = _index_material(repository.index_manifest.declared_indexes, repository.index_manifest.records)
    expected_index_hash = semantic_hash(index_material)
    if repository.index_manifest.manifest_hash != expected_index_hash or repository.index_manifest.manifest_id != f"V558IDX:{expected_index_hash}":
        raise ClosureIntegrityError("repository index manifest checksum mismatch")
    material = _repository_material_from_ref(
        repository.publication_bundle_ref, repository.entries, repository.reference_edges,
        repository.external_bindings, repository.index_manifest,
    )
    expected = semantic_hash(material)
    if repository.repository_hash != expected or repository.repository_id != f"V558REPO:{expected}":
        raise ClosureIntegrityError("repository bundle checksum mismatch")


def resolve_v558(
    repository: V558RepositoryBundle, query: ContextQuery, *,
    policy: ResolverPolicy = ResolverPolicy(),
    external_store: Mapping[str, Mapping[str, Any]] | None = None,
) -> ResolutionResult:
    """Resolve exact immutable candidates without fabricating a ResolvedStructuralContext."""
    if not isinstance(repository, V558RepositoryBundle) or not isinstance(query, ContextQuery):
        raise M4IntegrityError("resolver requires exact repository and ContextQuery")
    _validate_repository_checksum(repository)
    expected_query_hash = semantic_hash(_query_material(query.items, query.generated_binding_refs))
    if query.query_hash != expected_query_hash or query.query_id != f"V558QUERY:{expected_query_hash}":
        raise M4IntegrityError("ContextQuery identity/hash is stale or corrupt")
    external_store = external_store or {}
    index: dict[str, ExactRef] = {}
    for record in repository.index_manifest.records:
        if record.index_name != "OBJECT_IDENTITY":
            continue
        if record.key in index:
            raise ClosureIntegrityError("ambiguous OBJECT_IDENTITY index key")
        index[record.key] = record.locator_ref
    by_locator = {_ref_key(e.locator.ref): e for e in repository.entries}
    selections: list[SelectionRecord] = []
    resolved: list[ResolvedEntry] = []
    unresolved: list[str] = []
    integrity_failed = False
    denied = False
    for item in query.items:
        locator_ref = index.get(item.resolution_key)
        if locator_ref is None:
            unresolved.append(item.resolution_key)
            selections.append(_selection(
                repository=repository, query=query, policy=policy, item=item, entry=None,
                decision="UNRESOLVED_EXACT_KEY", reason="exact immutable index key not present; no fuzzy/latest repair",
            ))
            continue
        entry = by_locator.get(_ref_key(locator_ref))
        if entry is None:
            integrity_failed = True
            selections.append(_selection(
                repository=repository, query=query, policy=policy, item=item, entry=None,
                decision="INTEGRITY_FAILURE", reason="index locator does not resolve exactly",
            ))
            continue
        if entry.obj.semantic_class in AUDIT_ONLY_CLASSES:
            denied = True
            selections.append(_selection(
                repository=repository, query=query, policy=policy, item=item, entry=entry,
                decision="AUDIT_ONLY_NOT_CONTEXT", reason="audit-only receipt cannot become semantic structural context",
            ))
            continue
        try:
            closure_entries = _transitive_entries(entry, repository)
            for dep in closure_entries:
                _entry_body(dep, external_store)
            requested = set(item.requested_uses)
            permission_fail = next((
                dep for dep in closure_entries
                if not requested <= set(dep.obj.producer_allowed_uses) or
                not requested <= set(dep.governance.v557_allowed_uses)
            ), None)
            closure_digest = semantic_hash([
                {"object_ref": dep.obj.ref.as_dict(), "locator_ref": dep.locator.ref.as_dict(),
                 "governance_ref": dep.governance.ref.as_dict(),
                 "producer_allowed_uses": list(dep.obj.producer_allowed_uses),
                 "v557_allowed_uses": list(dep.governance.v557_allowed_uses)}
                for dep in closure_entries
            ])
            if permission_fail is not None:
                denied = True
                selections.append(_selection(
                    repository=repository, query=query, policy=policy, item=item, entry=entry,
                    decision="PERMISSION_DENIED", reason="root or required dependency does not authorize requested use item-wise",
                    closure_digest=closure_digest,
                ))
                continue
            allowed = tuple(item.requested_uses)
            record = _selection(
                repository=repository, query=query, policy=policy, item=item, entry=entry,
                decision="SELECTED", reason="exact identity/hash/closure and item-wise permission subsets verified",
                resolver_allowed_uses=allowed, closure_digest=closure_digest,
            )
            selections.append(record)
            resolved.append(ResolvedEntry(
                item.resolution_key, record.ref, entry.obj.producer_family, entry.obj.ref,
                entry.locator.ref, allowed, entry.obj.typed_state,
            ))
        except ClosureIntegrityError as exc:
            integrity_failed = True
            selections.append(_selection(
                repository=repository, query=query, policy=policy, item=item, entry=entry,
                decision="INTEGRITY_FAILURE", reason=str(exc),
            ))
    if integrity_failed:
        state = "RESOLUTION_INTEGRITY_FAILED"
    elif unresolved and resolved:
        state = "RESOLUTION_PARTIAL_TYPED_DEFERRED"
    elif unresolved:
        state = "RESOLUTION_MISSING_REQUIRED_AUTHORITY"
    elif denied and resolved:
        state = "RESOLUTION_PARTIAL_TYPED_DEFERRED"
    elif denied:
        state = "RESOLUTION_DENIED_OR_NOT_APPLICABLE"
    elif not query.items:
        state = "RESOLUTION_COMPLETE_VALID_EMPTY"
    else:
        state = "RESOLUTION_COMPLETE"
    replay = semantic_hash({
        "repository_ref": repository.ref.as_dict(), "index_manifest_ref": repository.index_manifest.ref.as_dict(),
        "query_id": query.query_id, "query_hash": query.query_hash, "policy": policy.as_dict(),
        "generated_binding_refs": [x.as_dict() for x in query.generated_binding_refs],
    })
    receipt_material = {
        "schema": V558_RESOLUTION_RECEIPT_SCHEMA, "result_state": state,
        "repository_ref": repository.ref.as_dict(), "query_id": query.query_id,
        "query_hash": query.query_hash, "policy": policy.as_dict(),
        "selection_record_refs": [s.ref.as_dict() for s in selections],
        "resolved_entry_refs": [r.producer_object_ref.as_dict() for r in resolved],
        "unresolved_keys": list(unresolved), "replay_input_digest": replay,
    }
    rh = semantic_hash(receipt_material)
    receipt = ResolutionReceipt(
        f"V558REC:{rh}", rh, V558_RESOLUTION_RECEIPT_SCHEMA, state,
        tuple(s.ref for s in selections), tuple(r.producer_object_ref for r in resolved),
        tuple(unresolved), replay,
    )
    return ResolutionResult(tuple(selections), tuple(resolved), receipt, None)
