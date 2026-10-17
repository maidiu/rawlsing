#!/usr/bin/env python3
"""Fail-closed M3 / V556 higher-order structure with exact result-schema authority.

R2 preserves the V555 participant/source authority seam from R1 and adds the
C07-required result-contract firewall.  A positive V556 object now requires an
exact active rule whose content hash commits to an exact result-contract
binding, an exact active/current result-contract binding, and payload
conformance to that binding's closed objective-world schema.  Actor indexing is
explicitly typed and objective actor identifiers are not person-state.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Any, Mapping, Sequence

from rawlsing_next.m2_v555_atomic_route import (
    M2_CONTRACT_ID,
    M2DecisionState,
    M2Evaluation,
    SEMANTIC_FAMILY as V555_SEMANTIC_FAMILY,
    semantic_hash,
)

M3_CONTRACT_ID = "M3_V555_V556_HIGHER_ORDER_STRUCTURAL_EXACT_SEAM_CONTRACT@2.0.0"
SCR556_CONTRACT_ID = "SCR556_V556_INTERACTION_TOPOLOGY_EXACT_CONTRACT@scr556.v2"
RESULT_SCHEMA_REF_KIND = "M3ResultSchema@2.0.0"
RESULT_CONTRACT_BINDING_REF_KIND = "M3ResultContractBinding@2.0.0"
RESULT_JURISDICTION = "PRE_V3_OBJECTIVE_WORLD"
PERSON_STATE_SEMANTICS = "FORBIDDEN"
ACTOR_INDEXING_MODES = frozenset({"NO_ACTOR_INDEX", "OBJECTIVE_ACTOR_INDEXED"})
V556_SEMANTIC_FAMILIES = frozenset({
    "V556_INTERACTION_RELATION",
    "V556_TOPOLOGY",
    "V556_ATTRACTOR_PREREQUISITE",
})
ZERO_V556_OBJECTS = "ZERO_V556_OBJECTS"
_SHA = re.compile(r"^[0-9a-f]{64}$")
_ROUTE_ID = re.compile(r"^urn:rawlsing:v555:route:sha256:([0-9a-f]{64})$")
_RULE_FIELDS = frozenset({
    "authority_id", "authority_version", "authority_content_hash",
    "rule_id", "rule_version", "rule_content_hash", "semantic_family",
    "participant_roles", "participant_order_policy", "minimum_cardinality",
    "maximum_cardinality_or_unbounded_marker", "multiplicity_policy",
    "same_route_reuse_policy", "source_composition_policy",
    "allowed_typed_outcome_states", "producer_allowed_uses",
    "result_contract_binding_ref",
})
_BINDING_FIELDS = frozenset({
    "v555_route_identity_ref", "role", "ordinal_or_null", "multiplicity_index",
    "source_universe_ref",
})
_COMPOSITION_FIELDS = frozenset({
    "authority_id", "authority_version", "authority_content_hash", "operation_id",
    "covered_source_universe_refs", "covered_participant_bindings",
    "compatibility_scope", "decision",
})
_REQ_FIELDS = frozenset({
    "higher_order_semantics_required", "rule_authority", "participant_bindings",
    "source_composition_authority", "result_contract_binding", "governed_result",
    "intended_use",
})
_RESULT_CONTRACT_FIELDS = frozenset({
    "binding_id", "binding_version", "binding_content_hash", "authorization_state",
    "bound_rule_id", "bound_rule_version", "result_schema_ref",
    "result_semantic_owner_ref", "result_semantic_owner_current_selection_ref",
    "semantic_jurisdiction", "actor_indexing_mode", "person_state_semantics",
    "result_schema",
})
_SCHEMA_FIELDS = frozenset({"schema_id", "schema_version", "semantic_class", "root"})
_FROZEN_STATES = frozenset({
    "SUPPORTED", "VALID_EMPTY", "DENIED", "NONCOMPARABLE", "UNKNOWN_AUTHORITY",
    "CONFLICTING_AUTHORITY", "INVALID_PARTICIPANT_SET", "UNRESOLVABLE_PARTICIPANT",
})
_RESULT_AUTH_STATES = frozenset({"AUTHORIZED_CURRENT", "DENIED", "STALE", "OUT_OF_SCOPE"})
_OBJECTIVE_SCHEMA_CLASSES = frozenset({
    "OBJECTIVE_STRUCTURAL_RESULT",
    "OBJECTIVE_ACTOR_POSITION",
    "OBJECTIVE_ACTOR_OPPORTUNITY",
    "OBJECTIVE_WORLD_STATUS",
    "OBJECTIVE_MEASUREMENT",
})
_OBJECTIVE_ROLES = frozenset({
    "OBJECTIVE_STRUCTURAL_RELATION",
    "OBJECTIVE_ACTOR_INDEX",
    "OBJECTIVE_INSTITUTION",
    "OBJECTIVE_POSITION",
    "OBJECTIVE_OPPORTUNITY",
    "OBJECTIVE_CONSTRAINT",
    "OBJECTIVE_STATUS",
    "OBJECTIVE_MEASUREMENT",
    "OBJECTIVE_REFERENCE",
    "OBJECTIVE_GROUPING",
    "OBJECTIVE_TEXT_LABEL",
})
_PERSON_STATE_ROLES = frozenset({
    "PERSONALITY_OR_PSYCHOMETRIC_TYPE",
    "SUBJECTIVE_BELIEF_IDEOLOGY",
    "AFFECT",
    "APPRAISAL",
    "PREFERENCE",
    "MOTIVATION",
    "SUBJECTIVE_DISPOSITION",
    "PSYCHOLOGICAL_TRAIT",
    "ACTOR_UPTAKE",
    "ACTOR_INTERPRETATION",
    "ACTOR_RESPONSE",
    "DURABLE_PERSON_STATE",
    "DEVELOPMENTAL_BIOGRAPHICAL_STATE",
})


class M3DecisionState(str, Enum):
    SUPPORTED = "SUPPORTED"
    VALID_EMPTY = "VALID_EMPTY"
    DENIED = "DENIED"
    NONCOMPARABLE = "NONCOMPARABLE"
    UNKNOWN_AUTHORITY = "UNKNOWN_AUTHORITY"
    CONFLICTING_AUTHORITY = "CONFLICTING_AUTHORITY"
    INVALID_PARTICIPANT_SET = "INVALID_PARTICIPANT_SET"
    UNRESOLVABLE_PARTICIPANT = "UNRESOLVABLE_PARTICIPANT"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"
    RESULT_CONTRACT_NOT_CURRENT = "RESULT_CONTRACT_NOT_CURRENT"
    RESULT_SCHEMA_NONCONFORMING = "RESULT_SCHEMA_NONCONFORMING"


@dataclass(frozen=True)
class M3Evaluation:
    contract_id: str
    decision_state: M3DecisionState | None
    reason: str
    behavior: str
    canonical_participant_bindings: tuple[Mapping[str, Any], ...]
    v556_object: Mapping[str, Any] | None
    passthrough_v555_v557_handoffs: tuple[Mapping[str, Any], ...]
    replay_key_hash: str | None


class _Authority(ValueError):
    pass


class _Participant(ValueError):
    pass


class _Unresolvable(ValueError):
    pass


class _Denied(ValueError):
    pass


class _SchemaIntegrity(ValueError):
    pass


class _SchemaNonconformance(ValueError):
    pass


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    out = value.strip()
    if out.lower() in {"latest", "default", "*"}:
        raise ValueError(f"{name} may not use mutable/fuzzy version selection")
    return out


def _hash(value: Any, name: str) -> str:
    out = _text(value, name)
    if not _SHA.fullmatch(out):
        raise ValueError(f"{name} must be lowercase sha256")
    return out


def _ref(value: Any, name: str) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise _Unresolvable(f"{name} must be an exact reference mapping")
    fields = {"kind", "object_id", "content_hash"}
    if set(value) != fields:
        raise _Unresolvable(f"{name} must contain exactly {sorted(fields)!r}")
    try:
        return {
            "kind": _text(value["kind"], f"{name}.kind"),
            "object_id": _text(value["object_id"], f"{name}.object_id"),
            "content_hash": _hash(value["content_hash"], f"{name}.content_hash"),
        }
    except ValueError as exc:
        raise _Unresolvable(str(exc)) from exc


def _ref_key(ref: Mapping[str, str]) -> tuple[str, str, str]:
    return ref["kind"], ref["object_id"], ref["content_hash"]


def _canonical_ref_list(refs: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [dict(x) for x in sorted(refs, key=_ref_key)]


def _route_ref(m2: Any) -> dict[str, str] | None:
    if not isinstance(m2, M2Evaluation) or m2.contract_id != M2_CONTRACT_ID:
        raise _Unresolvable("M3 accepts exact M2Evaluation inputs only")
    if m2.decision_state is not M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED:
        return None
    route = m2.route
    ident = m2.canonical_route_identity
    if not isinstance(route, Mapping) or not isinstance(ident, tuple) or len(ident) != 7:
        raise _Unresolvable("positive V555 input lacks exact seven-field canonical route identity")
    if route.get("semantic_family") != V555_SEMANTIC_FAMILY:
        raise _Unresolvable("V555 semantic family mismatch")
    if tuple(route.get("canonical_route_identity", ())) != ident:
        raise _Unresolvable("V555 route tuple mismatch")
    ih = semantic_hash(list(ident))
    if m2.canonical_route_identity_hash != ih or route.get("canonical_route_identity_hash") != ih:
        raise _Unresolvable("V555 canonical route identity hash mismatch")
    rid = route.get("route_id")
    match = _ROUTE_ID.fullmatch(rid) if isinstance(rid, str) else None
    if not match or match.group(1) != ih:
        raise _Unresolvable("V555 route id does not address exact canonical tuple")
    if not isinstance(m2.exact_v554_f1_ref, Mapping) or ident[0] != m2.exact_v554_f1_ref.get("object_id"):
        raise _Unresolvable("V555 tuple no longer binds exact M2 F1 reference")
    forbidden_ids: list[str] = []
    if isinstance(m2.exact_v554_b1_ref, Mapping) and isinstance(m2.exact_v554_b1_ref.get("object_id"), str):
        forbidden_ids.append(m2.exact_v554_b1_ref["object_id"])
    for f2 in m2.inherited_v554_f2_refs:
        if isinstance(f2, Mapping) and isinstance(f2.get("object_id"), str):
            forbidden_ids.append(f2["object_id"])
    if any(fid in repr(ident) for fid in forbidden_ids):
        raise _Unresolvable("B1/F2 may not be promoted into V555 route identity")
    return {"kind": V555_SEMANTIC_FAMILY, "object_id": rid, "content_hash": semantic_hash(route)}


def _rule_body_material(value: Mapping[str, Any], normalized_binding_ref: Mapping[str, str]) -> dict[str, Any]:
    roles = value["participant_roles"]
    states = value["allowed_typed_outcome_states"]
    uses = value["producer_allowed_uses"]
    return {
        "contract_id": M3_CONTRACT_ID,
        "rule_id": value["rule_id"],
        "rule_version": value["rule_version"],
        "semantic_family": value["semantic_family"],
        "participant_roles": list(roles),
        "participant_order_policy": value["participant_order_policy"],
        "minimum_cardinality": value["minimum_cardinality"],
        "maximum_cardinality_or_unbounded_marker": value["maximum_cardinality_or_unbounded_marker"],
        "multiplicity_policy": value["multiplicity_policy"],
        "same_route_reuse_policy": value["same_route_reuse_policy"],
        "source_composition_policy": value["source_composition_policy"],
        "allowed_typed_outcome_states": sorted(set(states)),
        "producer_allowed_uses": sorted(set(uses)),
        "result_contract_binding_ref": dict(normalized_binding_ref),
    }


def _rule_key(value: Any) -> tuple[tuple[str, ...], dict[str, Any]]:
    if not isinstance(value, Mapping) or set(value) != _RULE_FIELDS:
        raise _Authority("rule_authority fields do not match versioned SCR556 R2 contract")
    try:
        aid = _text(value["authority_id"], "rule.authority_id")
        aver = _text(value["authority_version"], "rule.authority_version")
        ahash = _hash(value["authority_content_hash"], "rule.authority_content_hash")
        rid = _text(value["rule_id"], "rule.rule_id")
        rver = _text(value["rule_version"], "rule.rule_version")
        rhash = _hash(value["rule_content_hash"], "rule.rule_content_hash")
        family = _text(value["semantic_family"], "rule.semantic_family")
        order = _text(value["participant_order_policy"], "rule.participant_order_policy")
        multiplicity = _text(value["multiplicity_policy"], "rule.multiplicity_policy")
        reuse = _text(value["same_route_reuse_policy"], "rule.same_route_reuse_policy")
        composition = _text(value["source_composition_policy"], "rule.source_composition_policy")
        binding_ref = _ref(value["result_contract_binding_ref"], "rule.result_contract_binding_ref")
    except (_Unresolvable, ValueError) as exc:
        raise _Authority(str(exc)) from exc
    if binding_ref["kind"] != RESULT_CONTRACT_BINDING_REF_KIND:
        raise _Authority("rule result_contract_binding_ref kind is not versioned M3 result binding")
    if family not in V556_SEMANTIC_FAMILIES:
        raise _Authority("rule semantic family is not frozen V556 higher-order structure")
    roles = value["participant_roles"]
    if isinstance(roles, (str, bytes)) or not isinstance(roles, Sequence) or not roles:
        raise _Authority("participant_roles must be a non-empty sequence")
    try:
        roles_out = tuple(_text(x, "rule.participant_roles") for x in roles)
    except ValueError as exc:
        raise _Authority(str(exc)) from exc
    if len(set(roles_out)) != len(roles_out):
        raise _Authority("participant_roles must not contain duplicate role labels")
    if order not in {"ORDERED", "UNORDERED"}:
        raise _Authority("participant_order_policy must be ORDERED or UNORDERED")
    if reuse not in {"FORBIDDEN", "PERMITTED"}:
        raise _Authority("same_route_reuse_policy must be FORBIDDEN or PERMITTED")
    if composition != "NONE_BY_DEFAULT":
        raise _Authority("source_composition_policy must remain NONE_BY_DEFAULT")
    minimum = value["minimum_cardinality"]
    maximum = value["maximum_cardinality_or_unbounded_marker"]
    if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 2:
        raise _Authority("minimum_cardinality must be an integer >= 2")
    if maximum != "UNBOUNDED" and (not isinstance(maximum, int) or isinstance(maximum, bool) or maximum < minimum):
        raise _Authority("maximum_cardinality must be >= minimum or UNBOUNDED")
    states = value["allowed_typed_outcome_states"]
    uses = value["producer_allowed_uses"]
    if isinstance(states, (str, bytes)) or not isinstance(states, Sequence) or not states:
        raise _Authority("allowed_typed_outcome_states must be non-empty sequence")
    if isinstance(uses, (str, bytes)) or not isinstance(uses, Sequence):
        raise _Authority("producer_allowed_uses must be sequence")
    try:
        states_out = tuple(sorted({_text(x, "rule.allowed_typed_outcome_states") for x in states}))
        uses_out = tuple(sorted({_text(x, "rule.producer_allowed_uses") for x in uses}))
    except ValueError as exc:
        raise _Authority(str(exc)) from exc
    if not set(states_out) <= _FROZEN_STATES:
        raise _Authority("rule names a non-frozen V556 typed outcome state")
    normalized_for_hash = {
        **value,
        "rule_id": rid,
        "rule_version": rver,
        "semantic_family": family,
        "participant_roles": roles_out,
        "participant_order_policy": order,
        "minimum_cardinality": minimum,
        "maximum_cardinality_or_unbounded_marker": maximum,
        "multiplicity_policy": multiplicity,
        "same_route_reuse_policy": reuse,
        "source_composition_policy": composition,
        "allowed_typed_outcome_states": states_out,
        "producer_allowed_uses": uses_out,
    }
    expected_rule_hash = semantic_hash(_rule_body_material(normalized_for_hash, binding_ref))
    if rhash != expected_rule_hash:
        raise _Authority("rule_content_hash does not commit to the versioned R2 rule/result binding material")
    key = (aid, aver, ahash, rid, rver, rhash)
    return key, {
        "authority_id": aid, "authority_version": aver, "authority_content_hash": ahash,
        "rule_id": rid, "rule_version": rver, "rule_content_hash": rhash,
        "semantic_family": family, "participant_roles": roles_out,
        "participant_order_policy": order, "minimum_cardinality": minimum,
        "maximum_cardinality_or_unbounded_marker": maximum,
        "multiplicity_policy": multiplicity, "same_route_reuse_policy": reuse,
        "source_composition_policy": composition,
        "allowed_typed_outcome_states": states_out, "producer_allowed_uses": uses_out,
        "result_contract_binding_ref": binding_ref,
    }


def _active_key_set(values: Sequence[Sequence[str]], width: int, name: str) -> set[tuple[str, ...]]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _Authority(f"{name} must be a sequence of exact authority keys")
    out: set[tuple[str, ...]] = set()
    for raw in values:
        if isinstance(raw, (str, bytes)) or not isinstance(raw, Sequence) or len(raw) != width:
            raise _Authority(f"{name} contains malformed authority key")
        try:
            key = tuple(_text(x, name) for x in raw)
        except ValueError as exc:
            raise _Authority(str(exc)) from exc
        out.add(key)
    return out


def _active_ref_set(values: Sequence[Mapping[str, Any]], name: str) -> set[tuple[str, str, str]]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _Authority(f"{name} must be a sequence of exact refs")
    out: set[tuple[str, str, str]] = set()
    for i, raw in enumerate(values):
        try:
            ref = _ref(raw, f"{name}[{i}]")
        except _Unresolvable as exc:
            raise _Authority(str(exc)) from exc
        out.add(_ref_key(ref))
    return out


def _binding_material(binding: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "v555_route_identity_ref": dict(binding["v555_route_identity_ref"]),
        "role": binding["role"],
        "ordinal_or_null": binding["ordinal_or_null"],
        "multiplicity_index": binding["multiplicity_index"],
    }


def _participants(
    upstream: Sequence[M2Evaluation], raw_bindings: Any, rule: Mapping[str, Any],
) -> tuple[tuple[dict[str, Any], ...], tuple[M2Evaluation, ...], tuple[dict[str, str], ...]]:
    if isinstance(upstream, (str, bytes)) or not isinstance(upstream, Sequence):
        raise _Unresolvable("upstream must be a sequence of exact M2Evaluation values")
    index: dict[tuple[str, str, str], M2Evaluation] = {}
    for item in upstream:
        ref = _route_ref(item)
        if ref is not None:
            index[_ref_key(ref)] = item
    if isinstance(raw_bindings, (str, bytes)) or not isinstance(raw_bindings, Sequence):
        raise _Participant("participant_bindings must be a sequence")
    n = len(raw_bindings)
    minimum = rule["minimum_cardinality"]
    maximum = rule["maximum_cardinality_or_unbounded_marker"]
    if n < minimum or n < 2 or (maximum != "UNBOUNDED" and n > maximum):
        raise _Participant("participant occurrence cardinality violates exact V556 rule")
    parsed: list[dict[str, Any]] = []
    source_refs: list[dict[str, str]] = []
    route_occurrences: dict[tuple[str, str, str], list[int]] = {}
    for i, raw in enumerate(raw_bindings):
        if not isinstance(raw, Mapping) or set(raw) != _BINDING_FIELDS:
            raise _Participant("participant binding fields are not exact; B1/F2/raw V554/adjacency fields are forbidden")
        try:
            route_ref = _ref(raw["v555_route_identity_ref"], f"participant[{i}].v555_route_identity_ref")
            source_ref = _ref(raw["source_universe_ref"], f"participant[{i}].source_universe_ref")
            role = _text(raw["role"], f"participant[{i}].role")
        except _Unresolvable:
            raise
        except ValueError as exc:
            raise _Participant(str(exc)) from exc
        key = _ref_key(route_ref)
        if key not in index:
            raise _Unresolvable("participant route ref does not resolve to exact accepted V555 route; reconstruction/re-ID forbidden")
        if role not in set(rule["participant_roles"]):
            raise _Participant("participant role is outside exact V556 rule")
        ordinal = raw["ordinal_or_null"]
        if ordinal is not None and (not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal < 1):
            raise _Participant("participant ordinal must be positive integer or null")
        multiplicity = raw["multiplicity_index"]
        if not isinstance(multiplicity, int) or isinstance(multiplicity, bool) or multiplicity < 0:
            raise _Participant("multiplicity_index must be a nonnegative integer")
        parsed.append({
            "v555_route_identity_ref": route_ref, "role": role,
            "ordinal_or_null": ordinal, "multiplicity_index": multiplicity,
            "source_universe_ref": source_ref,
        })
        source_refs.append(source_ref)
        route_occurrences.setdefault(key, []).append(multiplicity)
    if len(route_occurrences) < 2:
        raise _Participant("positive higher-order meaning requires at least two distinct canonical V555 route identities")
    duplicated = any(len(v) > 1 for v in route_occurrences.values())
    if duplicated and rule["same_route_reuse_policy"] != "PERMITTED":
        raise _Participant("same-route reuse is forbidden by exact V556 rule")
    for indexes in route_occurrences.values():
        if sorted(indexes) != list(range(len(indexes))):
            raise _Participant("multiplicity_index sequence does not exactly describe route occurrences")
    order = rule["participant_order_policy"]
    if order == "ORDERED":
        ordinals = [x["ordinal_or_null"] for x in parsed]
        if any(x is None for x in ordinals) or sorted(ordinals) != list(range(1, n + 1)):
            raise _Participant("ordered rule requires exact contiguous participant ordinals")
        parsed.sort(key=lambda x: x["ordinal_or_null"])
        role_pattern = rule["participant_roles"]
        if len(role_pattern) > 1 and (len(role_pattern) != n or tuple(x["role"] for x in parsed) != tuple(role_pattern)):
            raise _Participant("ordered participant role pattern does not match exact V556 rule")
    else:
        if any(x["ordinal_or_null"] is not None for x in parsed):
            raise _Participant("unordered rule requires null participant ordinals")
        parsed.sort(key=lambda x: (
            _ref_key(x["v555_route_identity_ref"]), x["role"], x["multiplicity_index"]
        ))
    upstream_routes = tuple(index[_ref_key(x["v555_route_identity_ref"])] for x in parsed)
    return tuple(parsed), upstream_routes, tuple(source_refs)


def _composition_key(value: Any) -> tuple[tuple[str, ...], dict[str, Any]]:
    if not isinstance(value, Mapping) or set(value) != _COMPOSITION_FIELDS:
        raise _Authority("source composition authority fields are not exact")
    try:
        aid = _text(value["authority_id"], "composition.authority_id")
        aver = _text(value["authority_version"], "composition.authority_version")
        ahash = _hash(value["authority_content_hash"], "composition.authority_content_hash")
        operation = _text(value["operation_id"], "composition.operation_id")
        scope = _text(value["compatibility_scope"], "composition.compatibility_scope")
        decision = _text(value["decision"], "composition.decision")
    except ValueError as exc:
        raise _Authority(str(exc)) from exc
    if decision not in {"AUTHORIZED", "NONCOMPARABLE", "DENIED", "CONFLICTING_AUTHORITY"}:
        raise _Authority("composition decision is not frozen")
    srcs = value["covered_source_universe_refs"]
    bindings = value["covered_participant_bindings"]
    if isinstance(srcs, (str, bytes)) or not isinstance(srcs, Sequence):
        raise _Authority("covered_source_universe_refs must be sequence")
    if isinstance(bindings, (str, bytes)) or not isinstance(bindings, Sequence):
        raise _Authority("covered_participant_bindings must be sequence")
    try:
        src_out = tuple(_ref(x, "composition.covered_source_universe_refs") for x in srcs)
    except _Unresolvable as exc:
        raise _Authority(str(exc)) from exc
    bind_out: list[dict[str, Any]] = []
    for x in bindings:
        if not isinstance(x, Mapping) or set(x) != {"v555_route_identity_ref", "role", "ordinal_or_null", "multiplicity_index"}:
            raise _Authority("covered participant binding is not exact")
        try:
            rr = _ref(x["v555_route_identity_ref"], "composition.covered_participant.route_ref")
            role = _text(x["role"], "composition.covered_participant.role")
        except (_Unresolvable, ValueError) as exc:
            raise _Authority(str(exc)) from exc
        ordinal, multi = x["ordinal_or_null"], x["multiplicity_index"]
        if ordinal is not None and (not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal < 1):
            raise _Authority("composition covered participant ordinal invalid")
        if not isinstance(multi, int) or isinstance(multi, bool) or multi < 0:
            raise _Authority("composition covered participant multiplicity invalid")
        bind_out.append({"v555_route_identity_ref": rr, "role": role, "ordinal_or_null": ordinal, "multiplicity_index": multi})
    return (aid, aver, ahash, operation), {
        "authority_id": aid, "authority_version": aver, "authority_content_hash": ahash,
        "operation_id": operation, "covered_source_universe_refs": tuple(src_out),
        "covered_participant_bindings": tuple(bind_out), "compatibility_scope": scope,
        "decision": decision,
    }


def _schema_role(value: Any, path: str) -> str:
    try:
        role = _text(value, f"{path}.semantic_role")
    except ValueError as exc:
        raise _SchemaIntegrity(str(exc)) from exc
    if role in _PERSON_STATE_ROLES:
        raise _SchemaIntegrity(f"{path} declares forbidden person-state semantic role {role}")
    if role not in _OBJECTIVE_ROLES:
        raise _SchemaIntegrity(f"{path} semantic role is not an admitted objective-world role")
    return role


def _validate_schema_node(node: Any, path: str = "$") -> set[str]:
    if not isinstance(node, Mapping):
        raise _SchemaIntegrity(f"{path} schema node must be a mapping")
    try:
        node_type = _text(node.get("type"), f"{path}.type")
    except ValueError as exc:
        raise _SchemaIntegrity(str(exc)) from exc
    role = _schema_role(node.get("semantic_role"), path)
    roles = {role}
    if node_type == "object":
        expected = {"type", "semantic_role", "fields", "required", "additional_fields"}
        if set(node) != expected:
            raise _SchemaIntegrity(f"{path} object schema fields are not exact")
        fields = node["fields"]
        required = node["required"]
        if not isinstance(fields, Mapping):
            raise _SchemaIntegrity(f"{path}.fields must be a mapping")
        if isinstance(required, (str, bytes)) or not isinstance(required, Sequence):
            raise _SchemaIntegrity(f"{path}.required must be a sequence")
        try:
            required_names = tuple(_text(x, f"{path}.required") for x in required)
        except ValueError as exc:
            raise _SchemaIntegrity(str(exc)) from exc
        if len(required_names) != len(set(required_names)) or not set(required_names) <= set(fields):
            raise _SchemaIntegrity(f"{path}.required must be duplicate-free subset of fields")
        if node["additional_fields"] is not False:
            raise _SchemaIntegrity(f"{path} additional_fields must be false; open result schemas are forbidden")
        for name, child in fields.items():
            try:
                field_name = _text(name, f"{path}.field_name")
            except ValueError as exc:
                raise _SchemaIntegrity(str(exc)) from exc
            roles |= _validate_schema_node(child, f"{path}.{field_name}")
        return roles
    if node_type == "array":
        expected = {"type", "semantic_role", "items", "min_items", "max_items_or_unbounded_marker"}
        if set(node) != expected:
            raise _SchemaIntegrity(f"{path} array schema fields are not exact")
        minimum = node["min_items"]
        maximum = node["max_items_or_unbounded_marker"]
        if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 0:
            raise _SchemaIntegrity(f"{path}.min_items must be nonnegative integer")
        if maximum != "UNBOUNDED" and (not isinstance(maximum, int) or isinstance(maximum, bool) or maximum < minimum):
            raise _SchemaIntegrity(f"{path}.max_items_or_unbounded_marker invalid")
        roles |= _validate_schema_node(node["items"], f"{path}[]")
        return roles
    if node_type == "string":
        expected = {"type", "semantic_role", "allowed_values_or_unbounded_marker"}
        if set(node) != expected:
            raise _SchemaIntegrity(f"{path} string schema fields are not exact")
        allowed = node["allowed_values_or_unbounded_marker"]
        if allowed != "UNBOUNDED":
            if isinstance(allowed, (str, bytes)) or not isinstance(allowed, Sequence) or not allowed:
                raise _SchemaIntegrity(f"{path} string enum must be non-empty sequence or UNBOUNDED")
            try:
                values = tuple(_text(x, f"{path}.allowed_values") for x in allowed)
            except ValueError as exc:
                raise _SchemaIntegrity(str(exc)) from exc
            if len(values) != len(set(values)):
                raise _SchemaIntegrity(f"{path} string enum contains duplicates")
        return roles
    if node_type == "exact_ref":
        expected = {"type", "semantic_role", "allowed_kinds_or_unbounded_marker"}
        if set(node) != expected:
            raise _SchemaIntegrity(f"{path} exact_ref schema fields are not exact")
        kinds = node["allowed_kinds_or_unbounded_marker"]
        if kinds != "UNBOUNDED":
            if isinstance(kinds, (str, bytes)) or not isinstance(kinds, Sequence) or not kinds:
                raise _SchemaIntegrity(f"{path} allowed exact-ref kinds invalid")
            try:
                parsed = tuple(_text(x, f"{path}.allowed_kinds") for x in kinds)
            except ValueError as exc:
                raise _SchemaIntegrity(str(exc)) from exc
            if len(parsed) != len(set(parsed)):
                raise _SchemaIntegrity(f"{path} exact-ref kind list contains duplicates")
        return roles
    if node_type in {"integer", "number", "boolean"}:
        if set(node) != {"type", "semantic_role"}:
            raise _SchemaIntegrity(f"{path} scalar schema fields are not exact")
        return roles
    raise _SchemaIntegrity(f"{path} schema node type is not supported")


def _schema_ref(schema: Any) -> tuple[dict[str, str], Mapping[str, Any], set[str]]:
    if not isinstance(schema, Mapping) or set(schema) != _SCHEMA_FIELDS:
        raise _SchemaIntegrity("result_schema fields are not exact")
    try:
        schema_id = _text(schema["schema_id"], "result_schema.schema_id")
        schema_version = _text(schema["schema_version"], "result_schema.schema_version")
        semantic_class = _text(schema["semantic_class"], "result_schema.semantic_class")
    except ValueError as exc:
        raise _SchemaIntegrity(str(exc)) from exc
    if semantic_class not in _OBJECTIVE_SCHEMA_CLASSES:
        raise _SchemaIntegrity("result schema semantic_class is outside PRE-V3 objective-world classes")
    roles = _validate_schema_node(schema["root"])
    normalized = {
        "schema_id": schema_id,
        "schema_version": schema_version,
        "semantic_class": semantic_class,
        "root": schema["root"],
    }
    return {
        "kind": RESULT_SCHEMA_REF_KIND,
        "object_id": f"{schema_id}@{schema_version}",
        "content_hash": semantic_hash(normalized),
    }, normalized, roles


def _validate_payload_node(node: Mapping[str, Any], value: Any, path: str, roles_seen: set[str]) -> None:
    node_type = node["type"]
    role = node["semantic_role"]
    roles_seen.add(role)
    if node_type == "object":
        if not isinstance(value, Mapping):
            raise _SchemaNonconformance(f"{path} must be object")
        fields = node["fields"]
        required = set(node["required"])
        unknown = set(value) - set(fields)
        missing = required - set(value)
        if unknown:
            raise _SchemaNonconformance(f"{path} contains undeclared fields {sorted(unknown)!r}")
        if missing:
            raise _SchemaNonconformance(f"{path} missing required fields {sorted(missing)!r}")
        for key, child_value in value.items():
            _validate_payload_node(fields[key], child_value, f"{path}.{key}", roles_seen)
        return
    if node_type == "array":
        if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
            raise _SchemaNonconformance(f"{path} must be array")
        minimum = node["min_items"]
        maximum = node["max_items_or_unbounded_marker"]
        if len(value) < minimum or (maximum != "UNBOUNDED" and len(value) > maximum):
            raise _SchemaNonconformance(f"{path} array cardinality outside schema")
        for i, child in enumerate(value):
            _validate_payload_node(node["items"], child, f"{path}[{i}]", roles_seen)
        return
    if node_type == "string":
        if not isinstance(value, str):
            raise _SchemaNonconformance(f"{path} must be string")
        allowed = node["allowed_values_or_unbounded_marker"]
        if allowed != "UNBOUNDED" and value not in set(allowed):
            raise _SchemaNonconformance(f"{path} value is outside exact schema enum")
        return
    if node_type == "exact_ref":
        try:
            ref = _ref(value, path)
        except _Unresolvable as exc:
            raise _SchemaNonconformance(str(exc)) from exc
        kinds = node["allowed_kinds_or_unbounded_marker"]
        if kinds != "UNBOUNDED" and ref["kind"] not in set(kinds):
            raise _SchemaNonconformance(f"{path} exact-ref kind outside schema")
        return
    if node_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise _SchemaNonconformance(f"{path} must be integer")
        return
    if node_type == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise _SchemaNonconformance(f"{path} must be number")
        return
    if node_type == "boolean":
        if not isinstance(value, bool):
            raise _SchemaNonconformance(f"{path} must be boolean")
        return
    raise _SchemaNonconformance(f"{path} schema type unsupported")


def _result_contract(
    value: Any,
    rule: Mapping[str, Any],
    active_refs: set[tuple[str, str, str]],
) -> tuple[dict[str, Any], dict[str, str]]:
    if not isinstance(value, Mapping) or set(value) != _RESULT_CONTRACT_FIELDS:
        raise _SchemaIntegrity("result_contract_binding fields are not exact")
    try:
        bid = _text(value["binding_id"], "result_contract.binding_id")
        bver = _text(value["binding_version"], "result_contract.binding_version")
        bhash = _hash(value["binding_content_hash"], "result_contract.binding_content_hash")
        auth_state = _text(value["authorization_state"], "result_contract.authorization_state")
        bound_rule_id = _text(value["bound_rule_id"], "result_contract.bound_rule_id")
        bound_rule_version = _text(value["bound_rule_version"], "result_contract.bound_rule_version")
        jurisdiction = _text(value["semantic_jurisdiction"], "result_contract.semantic_jurisdiction")
        actor_mode = _text(value["actor_indexing_mode"], "result_contract.actor_indexing_mode")
        person_state = _text(value["person_state_semantics"], "result_contract.person_state_semantics")
        supplied_schema_ref = _ref(value["result_schema_ref"], "result_contract.result_schema_ref")
        owner_ref = _ref(value["result_semantic_owner_ref"], "result_contract.result_semantic_owner_ref")
        owner_current_ref = _ref(
            value["result_semantic_owner_current_selection_ref"],
            "result_contract.result_semantic_owner_current_selection_ref",
        )
    except (_Unresolvable, ValueError) as exc:
        raise _SchemaIntegrity(str(exc)) from exc
    if auth_state not in _RESULT_AUTH_STATES:
        raise _SchemaIntegrity("result contract authorization_state is not recognized")
    if bound_rule_id != rule["rule_id"] or bound_rule_version != rule["rule_version"]:
        raise _SchemaIntegrity("result contract is not bound to the exact rule id/version")
    if jurisdiction != RESULT_JURISDICTION:
        raise _SchemaIntegrity("result contract jurisdiction must be PRE_V3_OBJECTIVE_WORLD")
    if actor_mode not in ACTOR_INDEXING_MODES:
        raise _SchemaIntegrity("result contract actor_indexing_mode invalid")
    if person_state != PERSON_STATE_SEMANTICS:
        raise _SchemaIntegrity("result contract must explicitly forbid person-state semantics")
    computed_schema_ref, schema, schema_roles = _schema_ref(value["result_schema"])
    if supplied_schema_ref != computed_schema_ref:
        raise _SchemaIntegrity("result_schema_ref does not resolve to exact supplied schema content")
    schema_has_actor = "OBJECTIVE_ACTOR_INDEX" in schema_roles
    if actor_mode == "NO_ACTOR_INDEX" and schema_has_actor:
        raise _SchemaIntegrity("NO_ACTOR_INDEX result contract may not declare objective actor-index fields")
    if actor_mode == "OBJECTIVE_ACTOR_INDEXED" and not schema_has_actor:
        raise _SchemaIntegrity("OBJECTIVE_ACTOR_INDEXED result contract must declare objective actor-index field")
    material = {
        "contract_id": M3_CONTRACT_ID,
        "binding_id": bid,
        "binding_version": bver,
        "authorization_state": auth_state,
        "bound_rule_id": bound_rule_id,
        "bound_rule_version": bound_rule_version,
        "result_schema_ref": supplied_schema_ref,
        "result_semantic_owner_ref": owner_ref,
        "result_semantic_owner_current_selection_ref": owner_current_ref,
        "semantic_jurisdiction": jurisdiction,
        "actor_indexing_mode": actor_mode,
        "person_state_semantics": person_state,
        "result_schema": schema,
    }
    if bhash != semantic_hash(material):
        raise _SchemaIntegrity("result contract binding hash does not match exact semantic material")
    binding_ref = {
        "kind": RESULT_CONTRACT_BINDING_REF_KIND,
        "object_id": f"{bid}@{bver}",
        "content_hash": bhash,
    }
    if binding_ref != rule["result_contract_binding_ref"]:
        raise _SchemaIntegrity("active rule does not commit to this exact result contract binding")
    if _ref_key(binding_ref) not in active_refs:
        raise _SchemaIntegrity("exact result contract binding is unavailable from current authority snapshot")
    normalized = {
        **material,
        "binding_content_hash": bhash,
        "binding_ref": binding_ref,
    }
    return normalized, binding_ref


def _validate_result_payload(contract: Mapping[str, Any], payload: Any) -> None:
    roles_seen: set[str] = set()
    _validate_payload_node(contract["result_schema"]["root"], payload, "$.semantic_payload", roles_seen)
    actor_seen = "OBJECTIVE_ACTOR_INDEX" in roles_seen
    if contract["actor_indexing_mode"] == "NO_ACTOR_INDEX" and actor_seen:
        raise _SchemaNonconformance("NO_ACTOR_INDEX payload contains objective actor-index role")
    if contract["actor_indexing_mode"] == "OBJECTIVE_ACTOR_INDEXED" and not actor_seen:
        raise _SchemaNonconformance("OBJECTIVE_ACTOR_INDEXED payload lacks required objective actor-index role")


def _result(state: M3DecisionState | None, reason: str, behavior: str, bindings=(), obj=None, handoffs=(), replay=None) -> M3Evaluation:
    return M3Evaluation(M3_CONTRACT_ID, state, reason, behavior, tuple(bindings), obj, tuple(handoffs), replay)


def evaluate_m3_v556_higher_order_structural(
    upstream: Sequence[M2Evaluation],
    request: Any,
    *,
    active_rule_keys: Sequence[Sequence[str]] = (),
    active_source_composition_keys: Sequence[Sequence[str]] = (),
    active_result_contract_refs: Sequence[Mapping[str, Any]] = (),
) -> M3Evaluation:
    """Evaluate governed V556 structure over exact V555 routes under R2 firewall.

    The caller supplies exact current rule/composition/result-contract authority
    snapshots.  No result schema is inferred, defaulted, label-resolved, or
    minted from the payload.
    """
    if not isinstance(request, Mapping):
        return _result(M3DecisionState.UNKNOWN_AUTHORITY, "M3 request must be exact mapping", "V556_EVALUATION_FAILED")
    required = request.get("higher_order_semantics_required")
    if not isinstance(required, bool):
        return _result(M3DecisionState.UNKNOWN_AUTHORITY, "higher_order_semantics_required must be boolean", "V556_EVALUATION_FAILED")
    if required is False:
        if set(request) != {"higher_order_semantics_required"}:
            return _result(M3DecisionState.UNKNOWN_AUTHORITY, "no-V556 request may not carry filler higher-order fields", "V556_EVALUATION_FAILED")
        handoffs: list[Mapping[str, Any]] = []
        route_refs: list[Mapping[str, str]] = []
        try:
            if isinstance(upstream, (str, bytes)) or not isinstance(upstream, Sequence):
                raise _Unresolvable("upstream must be exact M2Evaluation sequence")
            for item in upstream:
                ref = _route_ref(item)
                if ref is not None:
                    route_refs.append(ref)
                if isinstance(item, M2Evaluation) and item.direct_v557_handoff is not None:
                    handoffs.append(item.direct_v557_handoff)
        except _Unresolvable as exc:
            return _result(M3DecisionState.UNRESOLVABLE_PARTICIPANT, str(exc), "V556_EVALUATION_FAILED")
        replay = semantic_hash({
            "m3_contract_id": M3_CONTRACT_ID, "behavior": ZERO_V556_OBJECTS,
            "upstream_v555_route_refs": _canonical_ref_list(route_refs),
            "passthrough_v555_v557_handoffs": handoffs,
        })
        return _result(None, "no exact governed V556 higher-order meaning required; no filler object", ZERO_V556_OBJECTS, handoffs=handoffs, replay=replay)
    if set(request) != _REQ_FIELDS:
        return _result(M3DecisionState.UNKNOWN_AUTHORITY, "M3 request fields are not exact; raw upstream/filler fields forbidden", "V556_EVALUATION_FAILED")
    try:
        active_rules = _active_key_set(active_rule_keys, 6, "active_rule_keys")
        active_composition = _active_key_set(active_source_composition_keys, 4, "active_source_composition_keys")
        active_results = _active_ref_set(active_result_contract_refs, "active_result_contract_refs")
        rule_key, rule = _rule_key(request["rule_authority"])
        if rule_key not in active_rules:
            raise _Authority("rule authority is not in exact active V556 authority snapshot")
        try:
            result_contract, result_binding_ref = _result_contract(
                request["result_contract_binding"], rule, active_results
            )
        except _SchemaIntegrity as exc:
            return _result(M3DecisionState.INTEGRITY_FAILURE, str(exc), "V556_EVALUATION_FAILED")
        auth_state = result_contract["authorization_state"]
        if auth_state == "DENIED":
            return _result(M3DecisionState.DENIED, "exact result-contract authority denies this rule/result use", "V556_EVALUATED")
        if auth_state in {"STALE", "OUT_OF_SCOPE"}:
            return _result(M3DecisionState.RESULT_CONTRACT_NOT_CURRENT, f"result-contract authority is {auth_state}", "V556_EVALUATED")
        bindings, bound_routes, source_refs = _participants(upstream, request["participant_bindings"], rule)
        distinct_sources = {_ref_key(x) for x in source_refs}
        composition: Mapping[str, Any] | None = None
        if len(distinct_sources) > 1:
            raw_composition = request["source_composition_authority"]
            if raw_composition is None:
                raise _Authority("cross-source composition is NONE_BY_DEFAULT; exact positive authority required")
            comp_key, comp = _composition_key(raw_composition)
            if comp_key not in active_composition:
                raise _Authority("source composition authority is not in exact active snapshot")
            expected_sources = {_ref_key(x) for x in source_refs}
            supplied_sources = {_ref_key(x) for x in comp["covered_source_universe_refs"]}
            expected_bindings = {semantic_hash(_binding_material(x)) for x in bindings}
            supplied_bindings = {semantic_hash(x) for x in comp["covered_participant_bindings"]}
            if expected_sources != supplied_sources or expected_bindings != supplied_bindings:
                raise _Authority("source composition authority does not exactly cover participants and source universes")
            if comp["decision"] == "NONCOMPARABLE":
                return _result(M3DecisionState.NONCOMPARABLE, "exact source composition authority says noncomparable", "V556_EVALUATED", bindings)
            if comp["decision"] == "DENIED":
                return _result(M3DecisionState.DENIED, "exact source composition authority denies composition", "V556_EVALUATED", bindings)
            if comp["decision"] == "CONFLICTING_AUTHORITY":
                return _result(M3DecisionState.CONFLICTING_AUTHORITY, "exact source composition authorities conflict without precedence", "V556_EVALUATED", bindings)
            composition = comp
        elif request["source_composition_authority"] is not None:
            comp_key, comp = _composition_key(request["source_composition_authority"])
            if comp_key not in active_composition:
                raise _Authority("supplied composition authority is not in exact active snapshot")
            composition = comp
        intended_use = _text(request["intended_use"], "intended_use")
        allowed_uses = set(rule["producer_allowed_uses"])
        for route_eval in bound_routes:
            route_uses = route_eval.route.get("producer_allowed_uses", ()) if isinstance(route_eval.route, Mapping) else ()
            if isinstance(route_uses, (str, bytes)) or not isinstance(route_uses, Sequence):
                raise _Unresolvable("V555 producer_allowed_uses is malformed")
            allowed_uses &= {_text(x, "V555 producer_allowed_uses") for x in route_uses}
        if intended_use not in allowed_uses:
            raise _Denied("V556 intended use would exceed exact producer/rule permission ceiling")
        governed = request["governed_result"]
        if not isinstance(governed, Mapping) or set(governed) != {"state", "semantic_payload"}:
            raise _Authority("governed_result must contain exact state and semantic_payload")
        state_name = _text(governed["state"], "governed_result.state")
        if state_name not in rule["allowed_typed_outcome_states"] or state_name not in _FROZEN_STATES:
            raise _Authority("governed result state is not allowed by exact active V556 rule")
        state = M3DecisionState(state_name)
        payload = governed["semantic_payload"]
        canonical_bindings = tuple(_binding_material(x) for x in bindings)
        if state is M3DecisionState.SUPPORTED:
            if not isinstance(payload, Mapping) or not payload:
                return _result(M3DecisionState.RESULT_SCHEMA_NONCONFORMING, "SUPPORTED V556 meaning requires non-empty schema-bound payload", "V556_EVALUATED", canonical_bindings)
            try:
                _validate_result_payload(result_contract, payload)
            except _SchemaNonconformance as exc:
                return _result(M3DecisionState.RESULT_SCHEMA_NONCONFORMING, str(exc), "V556_EVALUATED", canonical_bindings)
        identity_material = {
            "m3_contract_id": M3_CONTRACT_ID,
            "scr556_contract_id": SCR556_CONTRACT_ID,
            "semantic_family": rule["semantic_family"],
            "rule_authority": rule,
            "result_contract_binding_ref": result_binding_ref,
            "result_schema_ref": result_contract["result_schema_ref"],
            "result_semantic_owner_ref": result_contract["result_semantic_owner_ref"],
            "result_semantic_owner_current_selection_ref": result_contract[
                "result_semantic_owner_current_selection_ref"
            ],
            "semantic_jurisdiction": result_contract["semantic_jurisdiction"],
            "actor_indexing_mode": result_contract["actor_indexing_mode"],
            "person_state_semantics": result_contract["person_state_semantics"],
            "participant_bindings": list(canonical_bindings),
            "source_composition_authority": composition,
            "semantic_payload": payload,
            "typed_outcome_state": state.value,
            "intended_use": intended_use,
            "producer_allowed_uses": sorted(allowed_uses),
        }
        replay = semantic_hash(identity_material)
        if state is not M3DecisionState.SUPPORTED:
            return _result(state, "exact governed V556 rule produced nonpositive/empty typed outcome", "V556_EVALUATED", canonical_bindings, replay=replay)
        obj = {
            "object_id": f"urn:rawlsing:v556:higher-order:sha256:{replay}",
            "semantic_family": rule["semantic_family"],
            "typed_outcome_state": state.value,
            "rule_authority": rule,
            "result_contract_binding_ref": result_binding_ref,
            "result_schema_ref": result_contract["result_schema_ref"],
            "result_semantic_owner_ref": result_contract["result_semantic_owner_ref"],
            "result_semantic_owner_current_selection_ref": result_contract[
                "result_semantic_owner_current_selection_ref"
            ],
            "semantic_jurisdiction": result_contract["semantic_jurisdiction"],
            "actor_indexing_mode": result_contract["actor_indexing_mode"],
            "person_state_absent": True,
            "participant_bindings": canonical_bindings,
            "source_composition_authority": composition,
            "semantic_payload": payload,
            "producer_allowed_uses": tuple(sorted(allowed_uses)),
            "replay_key_hash": replay,
        }
        return _result(state, "exact active V556 rule/result-schema authority and exact V555 participant seam verified", "V556_EVALUATED", canonical_bindings, obj=obj, replay=replay)
    except _Unresolvable as exc:
        return _result(M3DecisionState.UNRESOLVABLE_PARTICIPANT, str(exc), "V556_EVALUATION_FAILED")
    except _Participant as exc:
        return _result(M3DecisionState.INVALID_PARTICIPANT_SET, str(exc), "V556_EVALUATION_FAILED")
    except _Denied as exc:
        return _result(M3DecisionState.DENIED, str(exc), "V556_EVALUATED")
    except (_Authority, ValueError, TypeError, KeyError) as exc:
        return _result(M3DecisionState.UNKNOWN_AUTHORITY, str(exc) or "exact V556 authority unresolved", "V556_EVALUATION_FAILED")


__all__ = [
    "M3_CONTRACT_ID",
    "SCR556_CONTRACT_ID",
    "RESULT_SCHEMA_REF_KIND",
    "RESULT_CONTRACT_BINDING_REF_KIND",
    "RESULT_JURISDICTION",
    "PERSON_STATE_SEMANTICS",
    "ACTOR_INDEXING_MODES",
    "V556_SEMANTIC_FAMILIES",
    "ZERO_V556_OBJECTS",
    "M3DecisionState",
    "M3Evaluation",
    "evaluate_m3_v556_higher_order_structural",
]
