"""Generic governed source-free rule/material substrate for adopted V556 semantics.

Scope discipline (HQ204-V556-R1 / 01_SCOPE.md):
    This module AUTHOR material for ALREADY-ADOPTED semantic families. It
    invents no new social ontology and mints no strong noun. It only supplies
    the smallest generic registry/path needed for the existing
    ``m3_v556_higher_order_structural`` rule/result-contract/closed-schema
    contract to have positive source-free instances at all.

Nothing here decodes meaning. ``V556_SEMANTIC_FAMILIES`` remains the frozen
vocabulary; this module refuses any family outside it.

Explicitly NOT provided, by contract:
    * no scalar pressure magnitude
    * no universal pressure footprint / coupling scalar
    * no hegemony, capital, homology, formation
    * no actor desire, belief, personality or history
    * no person-state semantic role (the closed contract already forbids them)
    * no positive V556_ATTRACTOR_PREREQUISITE rule

The canary packs below are SOURCE-FREE MACHINERY PROOFS ONLY. They carry no
authority for any real-world structural claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.m2_v555_atomic_route import semantic_hash
from rawlsing_next.m3_v556_higher_order_structural import (
    M3_CONTRACT_ID,
    PERSON_STATE_SEMANTICS,
    RESULT_CONTRACT_BINDING_REF_KIND,
    RESULT_JURISDICTION,
    RESULT_SCHEMA_REF_KIND,
    V556_SEMANTIC_FAMILIES,
)

SUBSTRATE_CONTRACT_ID = "PYAT_HQ204_V556_POSITIVE_SUBSTRATE@1.0.0"

#: Typed valid-empty state when the registry holds no governed rule.
#: Missing rule authority must never manufacture a positive result.
VALID_EMPTY_NO_GOVERNED_RULE = "VALID_EMPTY_NO_GOVERNED_RULE"

#: Only frozen V556 families may be materialized.
SUPPORTED_FAMILIES = tuple(sorted(V556_SEMANTIC_FAMILIES))

#: Only frozen M3 typed outcome states may be named by a rule.
ALLOWED_TYPED_OUTCOME_STATES = (
    "SUPPORTED",
    "VALID_EMPTY",
    "DENIED",
    "NONCOMPARABLE",
    "CONFLICTING_AUTHORITY",
)

#: Only admitted objective-world semantic roles may be used by a schema.
ADMITTED_OBJECTIVE_ROLES = (
    "OBJECTIVE_STRUCTURAL_RELATION",
    "OBJECTIVE_INSTITUTION",
    "OBJECTIVE_STATUS",
    "OBJECTIVE_MEASUREMENT",
    "OBJECTIVE_REFERENCE",
    "OBJECTIVE_GROUPING",
    "OBJECTIVE_TEXT_LABEL",
    "OBJECTIVE_CONSTRAINT",
)

#: Vocabulary admitted by this tranche. Anything else is refused at authoring
#: time so a future edit cannot smuggle a strong Field Forge noun or a scalar.
PERMITTED_RELATION_KINDS = (
    "COEXISTING_STRUCTURAL_INCIDENCE",
    "SHARED_UPSTREAM_STRUCTURAL_CHANNEL",
    "PARALLEL_STRUCTURAL_OCCURRENCE",
)
PERMITTED_INCIDENCE_KINDS = (
    "STRUCTURAL_INCIDENCE_PRESENT",
    "STRUCTURAL_INCIDENCE_ABSENT",
)


class SubstrateAuthoringError(ValueError):
    """Refusal at authoring time. No partial material is ever emitted."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SubstrateAuthoringError(f"{name} must be a non-empty string")
    return value.strip()


def _sha(value: Any, name: str) -> str:
    text = _text(value, name)
    if len(text) != 64 or any(c not in "0123456789abcdef" for c in text):
        raise SubstrateAuthoringError(f"{name} must be a lowercase sha256 hex digest")
    return text


def _ref(kind: str, object_id: str) -> dict[str, str]:
    kind = _text(kind, "ref.kind")
    object_id = _text(object_id, "ref.object_id")
    return {
        "kind": kind,
        "object_id": object_id,
        "content_hash": semantic_hash([kind, object_id]),
    }


# --------------------------------------------------------------- schema nodes
def _node_string(role: str, allowed: Sequence[str] | str = "UNBOUNDED") -> dict[str, Any]:
    role = _text(role, "semantic_role")
    if role not in ADMITTED_OBJECTIVE_ROLES:
        raise SubstrateAuthoringError(f"role {role!r} is not an admitted objective-world role")
    if allowed != "UNBOUNDED":
        allowed = tuple(_text(x, "allowed_values") for x in allowed)
        if not allowed or len(set(allowed)) != len(allowed):
            raise SubstrateAuthoringError("string enum must be non-empty and duplicate-free")
    return {"type": "string", "semantic_role": role,
            "allowed_values_or_unbounded_marker": allowed}


def _node_exact_ref(role: str, kinds: Sequence[str] | str = "UNBOUNDED") -> dict[str, Any]:
    role = _text(role, "semantic_role")
    if role not in ADMITTED_OBJECTIVE_ROLES:
        raise SubstrateAuthoringError(f"role {role!r} is not an admitted objective-world role")
    if kinds != "UNBOUNDED":
        kinds = tuple(_text(x, "allowed_kinds") for x in kinds)
        if not kinds or len(set(kinds)) != len(kinds):
            raise SubstrateAuthoringError("exact-ref kind list must be non-empty and duplicate-free")
    return {"type": "exact_ref", "semantic_role": role,
            "allowed_kinds_or_unbounded_marker": kinds}


def _node_array(items: Mapping[str, Any], *, min_items: int,
                max_items: int | str = "UNBOUNDED",
                role: str = "OBJECTIVE_GROUPING") -> dict[str, Any]:
    role = _text(role, "semantic_role")
    if role not in ADMITTED_OBJECTIVE_ROLES:
        raise SubstrateAuthoringError(f"role {role!r} is not an admitted objective-world role")
    if not isinstance(min_items, int) or isinstance(min_items, bool) or min_items < 0:
        raise SubstrateAuthoringError("min_items must be a nonnegative integer")
    if max_items != "UNBOUNDED" and (
        not isinstance(max_items, int) or isinstance(max_items, bool) or max_items < min_items
    ):
        raise SubstrateAuthoringError("max_items must be >= min_items or UNBOUNDED")
    return {"type": "array", "semantic_role": role, "items": dict(items),
            "min_items": min_items, "max_items_or_unbounded_marker": max_items}


def _node_object(fields: Mapping[str, Any], required: Sequence[str],
                 role: str = "OBJECTIVE_GROUPING") -> dict[str, Any]:
    role = _text(role, "semantic_role")
    if role not in ADMITTED_OBJECTIVE_ROLES:
        raise SubstrateAuthoringError(f"role {role!r} is not an admitted objective-world role")
    required = tuple(_text(x, "required") for x in required)
    if len(set(required)) != len(required) or not set(required) <= set(fields):
        raise SubstrateAuthoringError("required must be a duplicate-free subset of fields")
    # Closed schema: additional_fields is always False.
    return {"type": "object", "semantic_role": role, "fields": dict(fields),
            "required": required, "additional_fields": False}


#: Frozen PRE-V3 objective-world schema classes (mirrors the closed M3 contract).
ADMITTED_OBJECTIVE_SCHEMA_CLASSES = (
    "OBJECTIVE_STRUCTURAL_RESULT",
    "OBJECTIVE_ACTOR_POSITION",
    "OBJECTIVE_ACTOR_OPPORTUNITY",
    "OBJECTIVE_WORLD_STATUS",
    "OBJECTIVE_MEASUREMENT",
)

#: Frozen person-state semantic roles, refused at authoring time.
_FORBIDDEN_PERSON_STATE_ROLES = frozenset({
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

_SUPPORTED_NODE_TYPES = frozenset(
    {"object", "array", "string", "exact_ref", "integer", "number", "boolean"})


def _validate_authored_schema_node(node: Any, path: str = "$") -> None:
    """Fail closed at AUTHORING time.

    The closed M3 evaluator validates schemas again at evaluation time. This
    repeats the structural checks here so an unlawful schema can never be
    authored in the first place -- in particular a person-state semantic role
    or an open (``additional_fields``) object.
    """
    if not isinstance(node, Mapping):
        raise SubstrateAuthoringError(f"{path} schema node must be a mapping")
    node_type = node.get("type")
    if node_type not in _SUPPORTED_NODE_TYPES:
        raise SubstrateAuthoringError(f"{path} schema node type is not supported")
    role = node.get("semantic_role")
    role = _text(role, f"{path}.semantic_role")
    if role in _FORBIDDEN_PERSON_STATE_ROLES:
        raise SubstrateAuthoringError(
            f"{path} declares forbidden person-state semantic role {role!r}")
    if role not in ADMITTED_OBJECTIVE_ROLES:
        raise SubstrateAuthoringError(
            f"{path} role {role!r} is not an admitted objective-world role")
    if node_type == "object":
        if set(node) != {"type", "semantic_role", "fields", "required", "additional_fields"}:
            raise SubstrateAuthoringError(f"{path} object schema fields are not exact")
        if node["additional_fields"] is not False:
            raise SubstrateAuthoringError(
                f"{path} additional_fields must be false; open result schemas are forbidden")
        if not isinstance(node["fields"], Mapping):
            raise SubstrateAuthoringError(f"{path}.fields must be a mapping")
        required = node["required"]
        if isinstance(required, (str, bytes)) or not isinstance(required, Sequence):
            raise SubstrateAuthoringError(f"{path}.required must be a sequence")
        required = tuple(_text(x, f"{path}.required") for x in required)
        if len(set(required)) != len(required) or not set(required) <= set(node["fields"]):
            raise SubstrateAuthoringError(
                f"{path}.required must be a duplicate-free subset of fields")
        for name, child in node["fields"].items():
            _validate_authored_schema_node(child, f"{path}.{_text(name, 'field_name')}")
        return
    if node_type == "array":
        if set(node) != {"type", "semantic_role", "items", "min_items",
                         "max_items_or_unbounded_marker"}:
            raise SubstrateAuthoringError(f"{path} array schema fields are not exact")
        minimum = node["min_items"]
        maximum = node["max_items_or_unbounded_marker"]
        if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 0:
            raise SubstrateAuthoringError(f"{path}.min_items must be a nonnegative integer")
        if maximum != "UNBOUNDED" and (
            not isinstance(maximum, int) or isinstance(maximum, bool) or maximum < minimum):
            raise SubstrateAuthoringError(f"{path}.max_items_or_unbounded_marker invalid")
        _validate_authored_schema_node(node["items"], f"{path}[]")
        return
    if node_type == "string":
        if set(node) != {"type", "semantic_role", "allowed_values_or_unbounded_marker"}:
            raise SubstrateAuthoringError(f"{path} string schema fields are not exact")
        allowed = node["allowed_values_or_unbounded_marker"]
        if allowed != "UNBOUNDED":
            if isinstance(allowed, (str, bytes)) or not isinstance(allowed, Sequence) or not allowed:
                raise SubstrateAuthoringError(f"{path} string enum must be non-empty or UNBOUNDED")
            values = tuple(_text(x, f"{path}.allowed_values") for x in allowed)
            if len(values) != len(set(values)):
                raise SubstrateAuthoringError(f"{path} string enum contains duplicates")
        return
    if node_type == "exact_ref":
        if set(node) != {"type", "semantic_role", "allowed_kinds_or_unbounded_marker"}:
            raise SubstrateAuthoringError(f"{path} exact_ref schema fields are not exact")
        kinds = node["allowed_kinds_or_unbounded_marker"]
        if kinds != "UNBOUNDED":
            if isinstance(kinds, (str, bytes)) or not isinstance(kinds, Sequence) or not kinds:
                raise SubstrateAuthoringError(f"{path} allowed exact-ref kinds invalid")
            parsed = tuple(_text(x, f"{path}.allowed_kinds") for x in kinds)
            if len(parsed) != len(set(parsed)):
                raise SubstrateAuthoringError(f"{path} exact-ref kind list contains duplicates")
        return
    if set(node) != {"type", "semantic_role"}:
        raise SubstrateAuthoringError(f"{path} scalar schema fields are not exact")


def author_closed_result_schema(*, schema_id: str, semantic_class: str,
                                root: Mapping[str, Any], schema_version: str = "1.0.0") -> dict[str, Any]:
    """Build an exact closed result schema plus its exact ref.

    Validated here as well as by the closed evaluator, so an unlawful schema is
    refused at authoring time rather than only at evaluation time.
    """
    if semantic_class not in ADMITTED_OBJECTIVE_SCHEMA_CLASSES:
        raise SubstrateAuthoringError(
            f"semantic_class {semantic_class!r} is outside the PRE-V3 objective-world classes")
    _validate_authored_schema_node(root, "$.root")
    return {
        "schema": {
            "schema_id": _text(schema_id, "schema_id"),
            "schema_version": _text(schema_version, "schema_version"),
            "semantic_class": _text(semantic_class, "semantic_class"),
            "root": dict(root),
        },
        "schema_ref": {
            "kind": RESULT_SCHEMA_REF_KIND,
            "object_id": f"{_text(schema_id, 'schema_id')}@{_text(schema_version, 'schema_version')}",
            "content_hash": semantic_hash({
                "schema_id": _text(schema_id, "schema_id"),
                "schema_version": _text(schema_version, "schema_version"),
                "semantic_class": _text(semantic_class, "semantic_class"),
                "root": dict(root),
            }),
        },
    }


# ------------------------------------------------------- result-contract bind
@dataclass(frozen=True)
class ResultContractBinding:
    binding: Mapping[str, Any]
    binding_ref: Mapping[str, str]


def author_result_contract_binding(*, binding_id: str, rule_id: str, rule_version: str,
                                   schema: Mapping[str, Any], schema_ref: Mapping[str, str],
                                   authorization_state: str = "AUTHORIZED_CURRENT",
                                   actor_indexing_mode: str = "NO_ACTOR_INDEX",
                                   owner_tag: str = "hq204") -> ResultContractBinding:
    """Build the exact M3ResultContractBinding@2.0.0 material and its ref."""
    binding_id = _text(binding_id, "binding_id")
    rule_id = _text(rule_id, "rule_id")
    rule_version = _text(rule_version, "rule_version")
    if authorization_state not in {"AUTHORIZED_CURRENT", "DENIED", "STALE", "OUT_OF_SCOPE"}:
        raise SubstrateAuthoringError("authorization_state is not a frozen M3 result authorization state")
    if actor_indexing_mode not in {"NO_ACTOR_INDEX", "OBJECTIVE_ACTOR_INDEXED"}:
        raise SubstrateAuthoringError("actor_indexing_mode is not a frozen M3 actor indexing mode")
    material = {
        "contract_id": M3_CONTRACT_ID,
        "binding_id": binding_id,
        "binding_version": "1.0.0",
        "authorization_state": authorization_state,
        "bound_rule_id": rule_id,
        "bound_rule_version": rule_version,
        "result_schema_ref": dict(schema_ref),
        "result_semantic_owner_ref": _ref("M3_RESULT_SEMANTIC_OWNER", f"owner:{owner_tag}:{rule_id}"),
        "result_semantic_owner_current_selection_ref": _ref(
            "M3_RESULT_OWNER_CURRENT_SELECTION", f"owner-current:{owner_tag}:{rule_id}"),
        "semantic_jurisdiction": RESULT_JURISDICTION,
        "actor_indexing_mode": actor_indexing_mode,
        "person_state_semantics": PERSON_STATE_SEMANTICS,
        "result_schema": dict(schema),
    }
    binding_hash = semantic_hash(material)
    binding = {k: v for k, v in material.items() if k != "contract_id"}
    binding["binding_content_hash"] = binding_hash
    binding_ref = {
        "kind": RESULT_CONTRACT_BINDING_REF_KIND,
        "object_id": f"{binding_id}@{binding['binding_version']}",
        "content_hash": binding_hash,
    }
    return ResultContractBinding(binding=binding, binding_ref=binding_ref)


# ------------------------------------------------------------------- rule
@dataclass(frozen=True)
class GovernedRule:
    rule: Mapping[str, Any]
    rule_key: tuple[str, ...]
    result_contract: Mapping[str, Any]
    result_contract_ref: Mapping[str, str]
    semantic_family: str

    def active_rule_key(self) -> list[str]:
        return list(self.rule_key)


def author_governed_rule(*, authority_id: str, authority_version: str,
                          authority_content_hash: str,
                          rule_id: str, rule_version: str,
                          semantic_family: str, participant_roles: Sequence[str],
                          participant_order_policy: str = "ORDERED",
                          minimum_cardinality: int = 2,
                          maximum_cardinality_or_unbounded_marker: int | str = "UNBOUNDED",
                          multiplicity_policy: str = "EXACT_OCCURRENCE_INDEX",
                          same_route_reuse_policy: str = "FORBIDDEN",
                          producer_allowed_uses: Sequence[str] = ("M3_USE",),
                          result_contract: ResultContractBinding) -> GovernedRule:
    """Build one exact governed V556 rule with an exact content-hash binding.

    ``semantic_family`` MUST already be frozen in ``V556_SEMANTIC_FAMILIES``. This
    function refuses to introduce a family; it can only materialize one.
    """
    family = _text(semantic_family, "semantic_family")
    if family not in V556_SEMANTIC_FAMILIES:
        raise SubstrateAuthoringError(
            f"semantic_family {family!r} is not an adopted V556 family; this substrate "
            "materializes adopted semantics only and will not introduce a family")
    roles = tuple(_text(x, "participant_roles") for x in participant_roles)
    if not roles or len(set(roles)) != len(roles):
        raise SubstrateAuthoringError("participant_roles must be non-empty and duplicate-free")
    if participant_order_policy not in {"ORDERED", "UNORDERED"}:
        raise SubstrateAuthoringError("participant_order_policy must be ORDERED or UNORDERED")
    if same_route_reuse_policy not in {"FORBIDDEN", "PERMITTED"}:
        raise SubstrateAuthoringError("same_route_reuse_policy must be FORBIDDEN or PERMITTED")
    if not isinstance(minimum_cardinality, int) or isinstance(minimum_cardinality, bool) \
            or minimum_cardinality < 2:
        raise SubstrateAuthoringError("minimum_cardinality must be an integer >= 2")
    maximum = maximum_cardinality_or_unbounded_marker
    if maximum != "UNBOUNDED" and (
        not isinstance(maximum, int) or isinstance(maximum, bool) or maximum < minimum_cardinality
    ):
        raise SubstrateAuthoringError("maximum_cardinality must be >= minimum or UNBOUNDED")

    states = tuple(sorted(set(ALLOWED_TYPED_OUTCOME_STATES)))
    uses = tuple(sorted({_text(x, "producer_allowed_uses") for x in producer_allowed_uses}))

    rule_id = _text(rule_id, "rule_id")
    rule_version = _text(rule_version, "rule_version")

    body_material = {
        "contract_id": M3_CONTRACT_ID,
        "rule_id": rule_id,
        "rule_version": rule_version,
        "semantic_family": family,
        "participant_roles": list(roles),
        "participant_order_policy": participant_order_policy,
        "minimum_cardinality": minimum_cardinality,
        "maximum_cardinality_or_unbounded_marker": maximum,
        "multiplicity_policy": _text(multiplicity_policy, "multiplicity_policy"),
        "same_route_reuse_policy": same_route_reuse_policy,
        "source_composition_policy": "NONE_BY_DEFAULT",
        "allowed_typed_outcome_states": list(states),
        "producer_allowed_uses": list(uses),
        "result_contract_binding_ref": dict(result_contract.binding_ref),
    }
    rule = {
        "authority_id": _text(authority_id, "authority_id"),
        "authority_version": _text(authority_version, "authority_version"),
        "authority_content_hash": _sha(authority_content_hash, "authority_content_hash"),
        "rule_id": rule_id,
        "rule_version": rule_version,
        "rule_content_hash": semantic_hash(body_material),
        "semantic_family": family,
        "participant_roles": list(roles),
        "participant_order_policy": participant_order_policy,
        "minimum_cardinality": minimum_cardinality,
        "maximum_cardinality_or_unbounded_marker": maximum,
        "multiplicity_policy": _text(multiplicity_policy, "multiplicity_policy"),
        "same_route_reuse_policy": same_route_reuse_policy,
        "source_composition_policy": "NONE_BY_DEFAULT",
        "allowed_typed_outcome_states": list(states),
        "producer_allowed_uses": list(uses),
        "result_contract_binding_ref": dict(result_contract.binding_ref),
    }
    key = tuple(rule[k] for k in (
        "authority_id", "authority_version", "authority_content_hash",
        "rule_id", "rule_version", "rule_content_hash"))
    return GovernedRule(
        rule=rule, rule_key=key,
        result_contract=result_contract.binding,
        result_contract_ref=result_contract.binding_ref,
        semantic_family=family,
    )


# ---------------------------------------------------------------- registry
@dataclass(frozen=True)
class V556RuleMaterialRegistry:
    """Holds governed V556 rule/result-contract material.

    An empty registry is a LAWFUL VALID_EMPTY state. It never manufactures a
    positive result: with no active rule key the closed evaluator refuses.
    """

    rules: tuple[GovernedRule, ...] = ()

    @staticmethod
    def build(rules: Iterable[GovernedRule]) -> "V556RuleMaterialRegistry":
        seen: set[tuple[str, ...]] = set()
        families: set[str] = set()
        out: list[GovernedRule] = []
        for r in rules:
            if r.rule_key in seen:
                raise SubstrateAuthoringError("duplicate governed rule key in registry")
            if r.semantic_family in families:
                raise SubstrateAuthoringError(
                    "at most one governed rule per semantic family in this tranche")
            seen.add(r.rule_key)
            families.add(r.semantic_family)
            out.append(r)
        return V556RuleMaterialRegistry(rules=tuple(out))

    def active_rule_keys(self) -> list[list[str]]:
        return [r.active_rule_key() for r in self.rules]

    def active_result_contract_refs(self) -> list[Mapping[str, str]]:
        return [dict(r.result_contract_ref) for r in self.rules]

    @property
    def state(self) -> str:
        return "GOVERNED_RULES_PRESENT" if self.rules else VALID_EMPTY_NO_GOVERNED_RULE

    @property
    def registered_rule_count(self) -> int:
        return len(self.rules)

    @property
    def populated_families(self) -> tuple[str, ...]:
        return tuple(sorted(r.semantic_family for r in self.rules))

    @property
    def unfilled_families(self) -> tuple[str, ...]:
        return tuple(sorted(set(SUPPORTED_FAMILIES) - set(self.populated_families)))

    def rule_for(self, semantic_family: str) -> GovernedRule | None:
        for r in self.rules:
            if r.semantic_family == semantic_family:
                return r
        return None

    def snapshot(self) -> dict[str, Any]:
        return {
            "substrate_contract_id": SUBSTRATE_CONTRACT_ID,
            "state": self.state,
            "registered_rule_count": self.registered_rule_count,
            "populated_families": list(self.populated_families),
            "unfilled_families": list(self.unfilled_families),
            "active_rule_keys": self.active_rule_keys(),
            "active_result_contract_refs": self.active_result_contract_refs(),
        }


# -------------------------------------------------- source-free canary packs
def _topology_schema() -> dict[str, Any]:
    """Endpoint / route-identity / incidence fields. No scalar magnitude."""
    return author_closed_result_schema(
        schema_id="HQ204_CANARY_V556_TOPOLOGY_RESULT",
        semantic_class="OBJECTIVE_STRUCTURAL_RESULT",
        root=_node_object(
            {
                "endpoint_a_ref": _node_exact_ref("OBJECTIVE_REFERENCE"),
                "endpoint_b_ref": _node_exact_ref("OBJECTIVE_REFERENCE"),
                "shared_structural_channel_ref": _node_exact_ref("OBJECTIVE_REFERENCE"),
                "incidence_kind": _node_string("OBJECTIVE_STRUCTURAL_RELATION", PERMITTED_INCIDENCE_KINDS),
            },
            ("endpoint_a_ref", "endpoint_b_ref", "shared_structural_channel_ref", "incidence_kind"),
        ),
    )


def _interaction_schema() -> dict[str, Any]:
    """A coexisting-relation array with min_items >= 2. No scalar magnitude."""
    item = _node_object(
        {
            "relation_kind": _node_string("OBJECTIVE_STRUCTURAL_RELATION", PERMITTED_RELATION_KINDS),
            "left_endpoint_ref": _node_exact_ref("OBJECTIVE_REFERENCE"),
            "right_endpoint_ref": _node_exact_ref("OBJECTIVE_REFERENCE"),
        },
        ("relation_kind", "left_endpoint_ref", "right_endpoint_ref"),
        role="OBJECTIVE_GROUPING",
    )
    return author_closed_result_schema(
        schema_id="HQ204_CANARY_V556_INTERACTION_RELATION_RESULT",
        semantic_class="OBJECTIVE_STRUCTURAL_RESULT",
        root=_node_object(
            {"coexisting_relations": _node_array(item, min_items=2, max_items="UNBOUNDED")},
            ("coexisting_relations",),
        ),
    )


def topology_canary_rule(*, rule_id: str = "V556-HQ204-TOPOLOGY-CANARY",
                         authority_id: str = "V556_HQ204_CANARY_AUTHORITY",
                         authority_version: str = "1.0.0",
                         authority_content_hash: str | None = None) -> GovernedRule:
    """One lawful positive source-free V556_TOPOLOGY rule."""
    built = _topology_schema()
    contract = author_result_contract_binding(
        binding_id=f"M3-RESULT-BINDING-{rule_id}", rule_id=rule_id, rule_version="1.0.0",
        schema=built["schema"], schema_ref=built["schema_ref"], owner_tag="hq204-topology")
    return author_governed_rule(
        authority_id=authority_id,
        authority_version=authority_version,
        authority_content_hash=authority_content_hash
        or semantic_hash(["V556_HQ204_CANARY_AUTHORITY", authority_version]),
        rule_id=rule_id,
        rule_version="1.0.0",
        semantic_family="V556_TOPOLOGY",
        participant_roles=("STRUCTURAL_ENDPOINT", "SHARED_INCIDENCE_CHANNEL"),
        participant_order_policy="ORDERED",
        minimum_cardinality=2,
        maximum_cardinality_or_unbounded_marker="UNBOUNDED",
        same_route_reuse_policy="FORBIDDEN",
        result_contract=contract,
    )


def interaction_relation_canary_rule(
        *, rule_id: str = "V556-HQ204-INTERACTION-RELATION-CANARY",
        authority_id: str = "V556_HQ204_CANARY_AUTHORITY",
        authority_version: str = "1.0.0",
        authority_content_hash: str | None = None) -> GovernedRule:
    """One lawful positive source-free V556_INTERACTION_RELATION rule.

    Its closed result schema carries a coexisting-relation array with
    ``min_items >= 2``, giving the retained nonadditive/interaction demand a
    positive governed instance without any scalar coupling value.
    """
    built = _interaction_schema()
    contract = author_result_contract_binding(
        binding_id=f"M3-RESULT-BINDING-{rule_id}", rule_id=rule_id, rule_version="1.0.0",
        schema=built["schema"], schema_ref=built["schema_ref"], owner_tag="hq204-interaction")
    return author_governed_rule(
        authority_id=authority_id,
        authority_version=authority_version,
        authority_content_hash=authority_content_hash
        or semantic_hash(["V556_HQ204_CANARY_AUTHORITY", authority_version]),
        rule_id=rule_id,
        rule_version="1.0.0",
        semantic_family="V556_INTERACTION_RELATION",
        participant_roles=("COEXISTING_RELATION_LEFT", "COEXISTING_RELATION_RIGHT"),
        participant_order_policy="ORDERED",
        minimum_cardinality=2,
        maximum_cardinality_or_unbounded_marker="UNBOUNDED",
        same_route_reuse_policy="FORBIDDEN",
        result_contract=contract,
    )


def source_free_canary_registry() -> V556RuleMaterialRegistry:
    """The tranche's positive source-free registry.

    V556_ATTRACTOR_PREREQUISITE is intentionally left unfilled. The commission
    forbids fabricating a positive attractor prerequisite merely to populate it,
    so it stays a supported-but-unfilled family.
    """
    return V556RuleMaterialRegistry.build(
        [topology_canary_rule(), interaction_relation_canary_rule()])


__all__ = [
    "SUBSTRATE_CONTRACT_ID",
    "VALID_EMPTY_NO_GOVERNED_RULE",
    "SUPPORTED_FAMILIES",
    "ALLOWED_TYPED_OUTCOME_STATES",
    "ADMITTED_OBJECTIVE_ROLES",
    "PERMITTED_RELATION_KINDS",
    "PERMITTED_INCIDENCE_KINDS",
    "SubstrateAuthoringError",
    "ResultContractBinding",
    "GovernedRule",
    "V556RuleMaterialRegistry",
    "author_closed_result_schema",
    "author_result_contract_binding",
    "author_governed_rule",
    "topology_canary_rule",
    "interaction_relation_canary_rule",
    "source_free_canary_registry",
]
