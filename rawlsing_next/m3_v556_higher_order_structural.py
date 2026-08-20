#!/usr/bin/env python3
"""Fail-closed clean-sideline runtime for frozen M3 / V556 higher-order structure."""
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

M3_CONTRACT_ID = "M3_V555_V556_HIGHER_ORDER_STRUCTURAL_EXACT_SEAM_CONTRACT@1.0.0"
SCR556_CONTRACT_ID = "SCR556_V556_INTERACTION_TOPOLOGY_EXACT_CONTRACT@scr556.v1"
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
    "source_composition_authority", "governed_result", "intended_use",
})
_FROZEN_STATES = frozenset({
    "SUPPORTED", "VALID_EMPTY", "DENIED", "NONCOMPARABLE", "UNKNOWN_AUTHORITY",
    "CONFLICTING_AUTHORITY", "INVALID_PARTICIPANT_SET", "UNRESOLVABLE_PARTICIPANT",
})
_FORBIDDEN_SEMANTIC_KEYS = ("actor", "persona", "phenomenolog", "render", "voice", "belief", "psyche")


class M3DecisionState(str, Enum):
    SUPPORTED = "SUPPORTED"
    VALID_EMPTY = "VALID_EMPTY"
    DENIED = "DENIED"
    NONCOMPARABLE = "NONCOMPARABLE"
    UNKNOWN_AUTHORITY = "UNKNOWN_AUTHORITY"
    CONFLICTING_AUTHORITY = "CONFLICTING_AUTHORITY"
    INVALID_PARTICIPANT_SET = "INVALID_PARTICIPANT_SET"
    UNRESOLVABLE_PARTICIPANT = "UNRESOLVABLE_PARTICIPANT"


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


def _rule_key(value: Any) -> tuple[tuple[str, ...], dict[str, Any]]:
    if not isinstance(value, Mapping) or set(value) != _RULE_FIELDS:
        raise _Authority("rule_authority fields do not match frozen SCR556 contract")
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
    except ValueError as exc:
        raise _Authority(str(exc)) from exc
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


def _binding_material(binding: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "v555_route_identity_ref": dict(binding["v555_route_identity_ref"]),
        "role": binding["role"],
        "ordinal_or_null": binding["ordinal_or_null"],
        "multiplicity_index": binding["multiplicity_index"],
    }


def _participants(
    upstream: Sequence[M2Evaluation], raw_bindings: Any, rule: Mapping[str, Any],
) -> tuple[tuple[dict[str, Any], ...], tuple[Mapping[str, Any], ...], tuple[dict[str, str], ...]]:
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


def _contains_forbidden_semantics(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if isinstance(key, str) and any(token in key.lower() for token in _FORBIDDEN_SEMANTIC_KEYS):
                return True
            if _contains_forbidden_semantics(child):
                return True
        return False
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return any(_contains_forbidden_semantics(x) for x in value)
    return False


def _result(state: M3DecisionState | None, reason: str, behavior: str, bindings=(), obj=None, handoffs=(), replay=None) -> M3Evaluation:
    return M3Evaluation(M3_CONTRACT_ID, state, reason, behavior, tuple(bindings), obj, tuple(handoffs), replay)


def evaluate_m3_v556_higher_order_structural(
    upstream: Sequence[M2Evaluation],
    request: Any,
    *,
    active_rule_keys: Sequence[Sequence[str]] = (),
    active_source_composition_keys: Sequence[Sequence[str]] = (),
) -> M3Evaluation:
    """Evaluate only governed V556 higher-order structure over exact V555 routes.

    `active_rule_keys` and `active_source_composition_keys` are exact immutable
    authority-snapshot keys supplied by the caller; this module owns no semantic
    registry and never treats branch/latest labels as authority.
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
        return _result(M3DecisionState.UNKNOWN_AUTHORITY, "M3 request fields are not exact; actor/persona/raw upstream/filler fields forbidden", "V556_EVALUATION_FAILED")
    try:
        active_rules = _active_key_set(active_rule_keys, 6, "active_rule_keys")
        active_composition = _active_key_set(active_source_composition_keys, 4, "active_source_composition_keys")
        rule_key, rule = _rule_key(request["rule_authority"])
        if rule_key not in active_rules:
            raise _Authority("rule authority is not in exact active V556 authority snapshot")
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
        if _contains_forbidden_semantics(payload):
            raise _Denied("actor/persona/phenomenology/render semantics are outside V556 jurisdiction")
        canonical_bindings = tuple(_binding_material(x) for x in bindings)
        identity_material = {
            "m3_contract_id": M3_CONTRACT_ID,
            "scr556_contract_id": SCR556_CONTRACT_ID,
            "semantic_family": rule["semantic_family"],
            "rule_authority": rule,
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
        if not isinstance(payload, Mapping) or not payload:
            raise _Denied("SUPPORTED V556 meaning requires non-empty higher-order semantic payload; filler forbidden")
        obj = {
            "object_id": f"urn:rawlsing:v556:higher-order:sha256:{replay}",
            "semantic_family": rule["semantic_family"],
            "typed_outcome_state": state.value,
            "rule_authority": rule,
            "participant_bindings": canonical_bindings,
            "source_composition_authority": composition,
            "semantic_payload": payload,
            "producer_allowed_uses": tuple(sorted(allowed_uses)),
            "replay_key_hash": replay,
            "actor_independent": True,
        }
        return _result(state, "exact active V556 authority and exact V555 participant seam verified", "V556_EVALUATED", canonical_bindings, obj=obj, replay=replay)
    except _Unresolvable as exc:
        return _result(M3DecisionState.UNRESOLVABLE_PARTICIPANT, str(exc), "V556_EVALUATION_FAILED")
    except _Participant as exc:
        return _result(M3DecisionState.INVALID_PARTICIPANT_SET, str(exc), "V556_EVALUATION_FAILED")
    except _Denied as exc:
        return _result(M3DecisionState.DENIED, str(exc), "V556_EVALUATED")
    except (_Authority, ValueError, TypeError, KeyError) as exc:
        return _result(M3DecisionState.UNKNOWN_AUTHORITY, str(exc) or "exact V556 authority unresolved", "V556_EVALUATION_FAILED")
