#!/usr/bin/env python3
"""HQ206 V556 ontology-smuggling / authoring repair.

The adopted M3 seam (``m3_v556_higher_order_structural.py``) is NOT modified. This
module repairs only the HQ206/HQ205-review substrate, and it introduces **no new
structural ontology**.

The load-bearing authority is TD_R03 (``TD_R03_V556/RESULT.md``), the V556
architecture of record. Three of its clauses drive this repair:

**§5 non-inference law.** "No F1 may be created solely because routes coexist, have
opposite signs/directions, share source/target/mediator/stratum, overlap in
geography/time, derive from the same V554 affordance, have similar labels, or appear
together in runtime context. These may be candidate premises a future rule examines;
they are never the rule itself."

**§6 interaction authority verdict.** "No complete governed V556 interaction-rule
authority was found in the audited architecture. Therefore F1 is required as a family
but the first implementation tranche may be **valid-empty**. Empty because no rule
authorizes a relation is distinct from missing/corrupt input, schema failure, duplicate
ID, hash failure or other construction failure."

**§5/§8 quantitative ceiling.** Numeric combination sits behind a "nullable
numeric-formula ref, **unset by default**"; F2 "may never assert ... numeric attractor
strength/threshold without formula authority".

Consequences, all of them reductions rather than additions:

1.  ``V556_INTERACTION_RELATION`` is returned **lawfully VALID_EMPTY**. The previous
    tranche minted exactly the three relation kinds TD-R03 §5 forbids as constituting
    an F1. Those names are retained only as *non-inferable premises*, never as an
    authorable relation-kind enum. No positive interaction rule is fabricated to
    preserve a canary goal.
2.  Authoring refuses strong-noun enums (the Field Forge R2 / OBL blocked nouns, named
    from adopted negative ceilings, not invented here) and refuses numeric scalar
    leaves outright.
3.  The topology canary declares a **truthful dyadic maximum** instead of a false
    ``UNBOUNDED``, is labelled one illustrative authorized shape rather than generic
    topology, makes no F2 claim, and binds its payload refs to governed participant
    route identities.
4.  Validation reaches the paths the review found ungated: the binding author, the rule
    author and the registry build. Unlawful material can no longer become
    ``GOVERNED_RULES_PRESENT``.
5.  Material is deep-frozen, ``multiplicity_policy`` is a frozen named vocabulary, and
    the tranche-local narrowings (one rule per family; admitted-role subset; no actor
    indexing) are recorded as named data rather than living only in an exception
    string.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.m2_v555_atomic_route import SEMANTIC_FAMILY as V555_FAMILY, semantic_hash
from rawlsing_next.m3_v556_higher_order_structural import (
    M3_CONTRACT_ID,
    PERSON_STATE_SEMANTICS,
    RESULT_CONTRACT_BINDING_REF_KIND,
    RESULT_JURISDICTION,
    RESULT_SCHEMA_REF_KIND,
    V556_SEMANTIC_FAMILIES,
)

SUBSTRATE_CONTRACT_ID = "PYAT_HQ204_V556_POSITIVE_SUBSTRATE@1.0.0"
REPAIR_ID = "PYAT_HQ206_V556_ONTOLOGY_AUTHORING_REPAIR_R1"

#: Typed valid-empty state when the registry holds no governed rule. Missing rule
#: authority must never manufacture a positive result. TD_R03 §12 requires this to be
#: distinguished from integrity/build failure.
VALID_EMPTY_NO_GOVERNED_RULE = "VALID_EMPTY_NO_GOVERNED_RULE"

#: Only frozen V556 families may be materialized.
SUPPORTED_FAMILIES = tuple(sorted(V556_SEMANTIC_FAMILIES))

ALLOWED_TYPED_OUTCOME_STATES = (
    "SUPPORTED",
    "VALID_EMPTY",
    "DENIED",
    "NONCOMPARABLE",
    "CONFLICTING_AUTHORITY",
)

# --------------------------------------------------------------------- tranche law
#: TRANCHE-LOCAL narrowing, recorded as named data rather than living only in an
#: exception string (review F6/F7). The adopted M3 contract admits more; this tranche
#: does not. This is a bounded authoring choice, NOT an architectural ceiling.
TRANCHE_LOCAL_ADMITTED_ROLE_NARROWING = MappingProxyType({
    "admitted_objective_roles": (
        "OBJECTIVE_STRUCTURAL_RELATION",
        "OBJECTIVE_INSTITUTION",
        "OBJECTIVE_STATUS",
        "OBJECTIVE_MEASUREMENT",
        "OBJECTIVE_REFERENCE",
        "OBJECTIVE_GROUPING",
        "OBJECTIVE_TEXT_LABEL",
        "OBJECTIVE_CONSTRAINT",
    ),
    "m3_also_admits_but_this_tranche_excludes": (
        "OBJECTIVE_ACTOR_INDEX",
        "OBJECTIVE_POSITION",
        "OBJECTIVE_OPPORTUNITY",
    ),
    "why": "admitted-M3 roles narrowed for bounded authoring only; no architectural ceiling is claimed",
    "objectively_not_person_state": "M3 line 9: objective actor identifiers are not person-state",
})

ADMITTED_OBJECTIVE_ROLES = TRANCHE_LOCAL_ADMITTED_ROLE_NARROWING["admitted_objective_roles"]

#: TRANCHE-LOCAL. Review F7 proved by probe P14 that M3 evaluates two distinct
#: same-family rules SUPPORTED, so this restriction is registry-local data, NOT law.
TRANCHE_LOCAL_ONE_RULE_PER_FAMILY = True
TRANCHE_LOCAL_ONE_RULE_PER_FAMILY_NOTE = (
    "at most one governed rule per semantic family IN THIS TRANCHE only; "
    "the adopted M3 seam evaluates multiple distinct same-family rules, "
    "so this is a bounded authoring restriction and not a timeless ceiling"
)

#: TRANCHE-LOCAL (review F6/P3). OBJECTIVE_ACTOR_INDEXED is REMOVED rather than left
#: as a dead accepted mode: ADMITTED_OBJECTIVE_ROLES excludes OBJECTIVE_ACTOR_INDEX, so
#: no binding this tranche can author would ever satisfy the M3 requirement.
TRANCHE_LOCAL_ACTOR_INDEXING_MODES = ("NO_ACTOR_INDEX",)
ACTOR_INDEXED_MODE_WITHDRAWN_REASON = (
    "OBJECTIVE_ACTOR_INDEXED is withdrawn from this tranche because OBJECTIVE_ACTOR_INDEX "
    "is outside the tranche-admitted role set, so any such binding would be a guaranteed "
    "INTEGRITY_FAILURE; a dead accepted mode is removed instead of retained"
)

#: Frozen multiplicity vocabulary (review R7/F10). Previously any string was accepted.
MULTIPLICITY_POLICIES = (
    "EXACT_OCCURRENCE_INDEX",
    "ROUTE_INDEXED_OCCURRENCE_SET",
)

# --------------------------------------------------------------------- TD_R03 law
#: TD_R03 §5 non-inference: these are PREMISES a future governed rule may examine.
#: They may NEVER constitute an F1 relation. The previous tranche used exactly these
#: three as its constituting relation kinds, which inverted the non-inference law.
TD_R03_NON_INFERABLE_F1_PREMISE_KINDS = (
    "COEXISTING_STRUCTURAL_INCIDENCE",
    "SHARED_UPSTREAM_STRUCTURAL_CHANNEL",
    "PARALLEL_STRUCTURAL_OCCURRENCE",
)

#: TD_R03 §5/§6: NO governed interaction rule authorizes any relation kind today, so
#: the authorable set is EMPTY. That emptiness IS the finding, and it is why
#: V556_INTERACTION_RELATION is returned lawfully valid-empty.
AUTHORIZED_INTERACTION_RELATION_KINDS = ()

#: TRANCHE-LOCAL (Repair 2). The VALID_EMPTY claim for the interaction and attractor
#: families must be a MACHINERY CEILING, not a fact about the shipped instance.
#: Review P7 showed the generic path could author, register and positively evaluate
#: both families, so "lawfully valid-empty" was true only of the shipped registry.
#: These two families are therefore refused AT AUTHORING and AT REGISTRY BUILD until a
#: later governed rule authority explicitly opens them. This is a bounded current
#: ceiling for this tranche, NOT a timeless ontology claim.
TRANCHE_LOCAL_AUTHORABLE_FAMILIES = ("V556_TOPOLOGY",)

TRANCHE_LOCAL_VALID_EMPTY_REQUIRED_FAMILIES = (
    "V556_ATTRACTOR_PREREQUISITE",
    "V556_INTERACTION_RELATION",
)

TRANCHE_LOCAL_VALID_EMPTY_CEILING_NOTE = (
    "V556_INTERACTION_RELATION and V556_ATTRACTOR_PREREQUISITE MUST refuse generic positive "
    "rule authoring in this tranche. V556_INTERACTION_RELATION because AUTHORIZED_INTERACTION_"
    "RELATION_KINDS is empty and TD_R03 §5 forbids an F1 constituted solely by coexistence, "
    "shared channel or parallel occurrence; V556_ATTRACTOR_PREREQUISITE because no governed "
    "attractor prerequisite rule authority exists and HQ forbids fabricating one. Opening "
    "either family requires a new governed rule authority; it is not a code flag."
)

#: TRANCHE-LOCAL (Repair 4). A POSITIVE participant-role allowlist, not a blacklist.
#: Derived ONLY from already-authorized current material: the two roles the topology
#: canary actually uses. Review P5 found ten actor/person-semantic labels accepted
#: because the refusal was substring-token based. An allowlist refuses the whole
#: complement, so no further vocabulary may be added to a list to widen it.
TRANCHE_LOCAL_FAMILY_PARTICIPANT_ROLE_MAP: Mapping[str, tuple[str, ...]] = MappingProxyType({
    "V556_TOPOLOGY": ("STRUCTURAL_ENDPOINT_A", "STRUCTURAL_ENDPOINT_B"),
})

TRANCHE_LOCAL_PARTICIPANT_ROLE_ALLOWLIST_NOTE = (
    "participant_roles MUST be drawn from the per-family governed role map. The map is "
    "derived only from already-authorized current material and is deliberately NOT widened: "
    "no role name is invented to make the API look generic. A role outside the map is "
    "refused regardless of whether it looks structural, so actor/person-semantic labels "
    "and any other unlisted label are refused by construction rather than by blacklist."
)

#: TD_R03 §5 names terminal-demand candidate relation kinds and then explicitly
#: refuses to canonize them: "TD-R03 does not canonize those terms merely by naming
#: them." Recorded so the vocabulary is traceable to adopted architecture rather than
#: invented, and never authorable until a governed rule registry supplies it.
TD_R03_CANDIDATE_RELATION_KINDS_NOT_CANONIZED = (
    "FLOW_CONTINUATION",
    "REROUTING",
    "CROSS_ROUTE_BUFFERING",
    "CROSS_ROUTE_AMPLIFICATION",
    "CROSS_ROUTE_BLOCKAGE",
    "COMPETITION_OR_COUNTER_PRESSURE",
    "CONTRADICTION",
    "REINFORCEMENT_OR_DESTABILIZATION_POSSIBILITY",
    "FEEDBACK",
    "CONDITIONAL_COUPLING",
)

#: Strong nouns blocked by adopted Field Forge R2 / OBL040 / OBL041 negative ceilings.
#: Named from adopted law, not invented here. Refused in any string enum value.
BLOCKED_STRONG_NOUNS = (
    "DOMINATION",
    "HEGEMONY",
    "SUBHEGEMONY",
    "CAPITAL",
    "FIELD_SPECIFIC_CAPITAL",
    "FIELD",
    "CONVERSION",
    "HOMOLOGY",
    "PRESSURE_FOOTPRINT",
    "PRESSURE_PATHWAY",
    "PRESSURE_COUPLING",
    "PRESSURE_COUPLING_PROFILE",
    "STRUCTURAL_MECHANISM",
)

#: Actor-semantic / person-state participant-role label tokens. Refused structurally
#: before registrability (review F2/P2).
_FORBIDDEN_PARTICIPANT_ROLE_TOKENS = (
    "ACTOR", "PERSON", "PSYCH", "BELIEF", "DESIRE", "MOTIV", "AFFECT",
    "TRAIT", "PREFERENCE", "IDEOLOGY", "WISH", "STRIVING", "SUBCONSCIOUS",
    "BIOGRAPH", "PERSONA", "PSYCHE", "APPETITE",
)

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

#: TRANCHE-LOCAL admitted objective-world result classes, each LINKED to the family that
#: authorizes it (Repair 7). The two actor-named classes that the previous tranche
#: admitted are REMOVED: OBJECTIVE_ACTOR_POSITION and OBJECTIVE_ACTOR_OPPORTUNITY name
#: actor concepts whose roles (OBJECTIVE_ACTOR_INDEX / POSITION / OPPORTUNITY) this
#: tranche excludes, so admitting the class while excluding the role was incoherent.
TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP: Mapping[str, str] = MappingProxyType({
    "OBJECTIVE_STRUCTURAL_RESULT": "V556_TOPOLOGY",
    "OBJECTIVE_WORLD_STATUS": "V556_TOPOLOGY",
    "OBJECTIVE_MEASUREMENT": "V556_TOPOLOGY",
})

ADMITTED_OBJECTIVE_SCHEMA_CLASSES = tuple(sorted(TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP))


def _refuse_if_class_family_mismatch(*, semantic_class: Any, family: Any, where: str) -> str:
    """The ONE class/family coherence decision, shared by authoring and registry build.

    HQ214 Repair D-1. The decision reads the semantic class from the VALIDATED result
    contract and the family from the RULE BODY, never from a caller-side convenience, and
    refuses a pair whose authorizing family is not the rule's own family even when every
    hash is internally consistent.

    Returns the authorizing family so callers can use it without a second lookup.
    """
    authorizing = TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP.get(semantic_class)
    if authorizing is None:
        raise SubstrateAuthoringError(
            f"{where} names semantic_class {semantic_class!r}, which no governed family "
            "authorizes; an unmapped class is never authorable")
    if authorizing != family:
        raise SubstrateAuthoringError(
            f"{where} is incoherent: semantic_class {semantic_class!r} is authorized by "
            f"{authorizing!r} but the rule declares {family!r}; class and family must agree")
    return authorizing

TRANCHE_LOCAL_SCHEMA_CLASS_WITHDRAWAL_NOTE = (
    "OBJECTIVE_ACTOR_POSITION and OBJECTIVE_ACTOR_OPPORTUNITY are withdrawn from the "
    "admitted class set: this tranche excludes OBJECTIVE_ACTOR_INDEX, OBJECTIVE_POSITION "
    "and OBJECTIVE_OPPORTUNITY, so admitting an actor-named result class was incoherent "
    "with the role ceiling. Every admitted class now names the family that authorizes it."
)

#: TD_R03 §5/§8 place quantitative combination behind a nullable numeric-formula ref
#: that is unset by default. Numeric LEAVES are therefore refused outright.
_REFUSED_NUMERIC_LEAF_TYPES = ("number", "integer")

PERMITTED_INCIDENCE_KINDS = (
    "STRUCTURAL_INCIDENCE_PRESENT",
    "STRUCTURAL_INCIDENCE_ABSENT",
)

_SUPPORTED_NODE_TYPES = frozenset(
    {"object", "array", "string", "exact_ref", "boolean"})


class SubstrateAuthoringError(ValueError):
    """Authoring-time refusal. Unlawful material never becomes registrable."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SubstrateAuthoringError(f"{name} must be a non-empty string")
    return value.strip()


def _sha(value: Any, name: str) -> str:
    value = _text(value, name)
    if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise SubstrateAuthoringError(f"{name} must be a lowercase 64-char sha256")
    return value


def _ref(kind: str, object_id: str) -> dict[str, str]:
    kind = _text(kind, "ref.kind")
    object_id = _text(object_id, "ref.object_id")
    return {"kind": kind, "object_id": object_id,
            "content_hash": semantic_hash([kind, object_id])}


def _freeze(value: Any) -> Any:
    """Deep-freeze material so a post-authoring mutation is impossible (R7/F9)."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value


def _plain(value: Any) -> Any:
    """Inverse of _freeze, for hashing and for handing M3 plain JSON-able data."""
    if isinstance(value, Mapping):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return value


# ------------------------------------------------------- R2 vocabulary gating
def _refuse_if_forbidden_vocabulary(text: str, where: str) -> None:
    upper = text.upper()
    for noun in BLOCKED_STRONG_NOUNS:
        if noun in upper:
            raise SubstrateAuthoringError(
                f"{where} names blocked strong noun {noun!r}; blocked by adopted Field Forge R2 "
                "and OBL040/OBL041 negative ceilings and never authorable here")
    for premise in TD_R03_NON_INFERABLE_F1_PREMISE_KINDS:
        if premise in upper:
            raise SubstrateAuthoringError(
                f"{where} names {premise!r}, which TD_R03 §5 forbids as constituting an F1 relation; "
                "it may be a premise a future governed rule examines, never the rule itself")


def _refuse_if_actor_semantic_role(role: str, where: str) -> None:
    upper = role.upper()
    for token in _FORBIDDEN_PARTICIPANT_ROLE_TOKENS:
        if token in upper:
            raise SubstrateAuthoringError(
                f"{where} uses actor-semantic participant label {role!r}; this substrate admits only "
                "actor-independent structural role labels")


# --------------------------------------------------------------- schema nodes
def _node_string(role: str, allowed: Sequence[str] | None = None) -> dict[str, Any]:
    """Closed governed value list REQUIRED. The UNBOUNDED sentinel is refused (R6/Repair 1).

    Review P1/P4: a leaf declared ``UNBOUNDED`` bypassed this gate entirely, and the
    M3 seam then accepts ANY string for it (m3:655-660) and copies it verbatim into the
    positive object (m3:931). An unbounded semantic value leaf is therefore not
    authorable. A closed list also makes M3 enforce the enum at evaluation time.
    """
    role = _text(role, "semantic_role")
    if role not in ADMITTED_OBJECTIVE_ROLES:
        raise SubstrateAuthoringError(f"role {role!r} is not an admitted objective-world role")
    if allowed is None:
        raise SubstrateAuthoringError(
            f"string leaf under role {role!r} requires an explicit closed governed value "
            "list; omitting it is refused because the UNBOUNDED sentinel is refused for "
            "semantic value leaves")
    if isinstance(allowed, str) or not isinstance(allowed, Sequence):
        raise SubstrateAuthoringError(
            f"string leaf under role {role!r} requires an explicit closed governed value "
            "list; the UNBOUNDED sentinel is refused for semantic value leaves")
    allowed = tuple(_text(x, "allowed_values") for x in allowed)
    if not allowed or len(set(allowed)) != len(allowed):
        raise SubstrateAuthoringError("string enum must be non-empty and duplicate-free")
    for value in allowed:
        _refuse_if_forbidden_vocabulary(value, f"string enum under role {role!r}")
    return {"type": "string", "semantic_role": role,
            "allowed_values_or_unbounded_marker": allowed}


def _node_exact_ref(role: str, kinds: Sequence[str] | None = None) -> dict[str, Any]:
    """Closed governed kind list REQUIRED. The UNBOUNDED sentinel is refused (R6/Repair 1).

    Review P2: an unbounded exact-ref kind leaf let an arbitrary kind such as HEGEMONY
    reach a SUPPORTED object, because M3 only checks the kind when the list is closed
    (m3:667-669).
    """
    role = _text(role, "semantic_role")
    if role not in ADMITTED_OBJECTIVE_ROLES:
        raise SubstrateAuthoringError(f"role {role!r} is not an admitted objective-world role")
    if kinds is None:
        raise SubstrateAuthoringError(
            f"exact_ref leaf under role {role!r} requires an explicit closed governed kind "
            "list; omitting it is refused because the UNBOUNDED sentinel is refused for "
            "semantic kind leaves")
    if isinstance(kinds, str) or not isinstance(kinds, Sequence):
        raise SubstrateAuthoringError(
            f"exact_ref leaf under role {role!r} requires an explicit closed governed kind "
            "list; the UNBOUNDED sentinel is refused for semantic kind leaves")
    kinds = tuple(_text(x, "allowed_kinds") for x in kinds)
    if not kinds or len(set(kinds)) != len(kinds):
        raise SubstrateAuthoringError("exact-ref kind list must be non-empty and duplicate-free")
    for kind in kinds:
        _refuse_if_forbidden_vocabulary(kind, f"exact-ref kind under role {role!r}")
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
    return {"type": "object", "semantic_role": role, "fields": dict(fields),
            "required": required, "additional_fields": False}


def _validate_authored_schema_node(node: Any, path: str = "$") -> None:
    """Fail closed at AUTHORING time across every authoring entry point."""
    if not isinstance(node, Mapping):
        raise SubstrateAuthoringError(f"{path} schema node must be a mapping")
    node_type = node.get("type")
    if node_type in _REFUSED_NUMERIC_LEAF_TYPES:
        raise SubstrateAuthoringError(
            f"{path} uses a {node_type!r} scalar leaf; TD_R03 §5/§8 place quantitative "
            "magnitude behind a nullable numeric-formula ref unset by default, so a numeric "
            "leaf (including a pressure magnitude) is refused")
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
        # MACHINERY GATE (Repair 1). This branch is reached for HAND-AUTHORED schema
        # mappings too, not only for nodes built by _node_string, so a caller cannot
        # evade the gate by writing the mapping directly.
        if allowed == "UNBOUNDED":
            raise SubstrateAuthoringError(
                f"{path} declares an UNBOUNDED semantic string value leaf; the M3 seam "
                "accepts ANY string for such a leaf and copies it into the positive object, "
                "so an explicit closed governed value list is required")
        if isinstance(allowed, (str, bytes)) or not isinstance(allowed, Sequence) or not allowed:
            raise SubstrateAuthoringError(f"{path} string enum must be a non-empty closed sequence")
        values = tuple(_text(x, f"{path}.allowed_values") for x in allowed)
        if len(values) != len(set(values)):
            raise SubstrateAuthoringError(f"{path} string enum contains duplicates")
        for value in values:
            _refuse_if_forbidden_vocabulary(value, f"{path} string enum")
        return
    if node_type == "exact_ref":
        if set(node) != {"type", "semantic_role", "allowed_kinds_or_unbounded_marker"}:
            raise SubstrateAuthoringError(f"{path} exact_ref schema fields are not exact")
        kinds = node["allowed_kinds_or_unbounded_marker"]
        # MACHINERY GATE (Repair 1). Same rationale as the string branch above.
        if kinds == "UNBOUNDED":
            raise SubstrateAuthoringError(
                f"{path} declares an UNBOUNDED exact-ref kind leaf; the M3 seam accepts ANY "
                "kind for such a leaf, so an explicit closed governed kind list is required")
        if isinstance(kinds, (str, bytes)) or not isinstance(kinds, Sequence) or not kinds:
            raise SubstrateAuthoringError(f"{path} allowed exact-ref kinds must be a non-empty closed sequence")
        parsed = tuple(_text(x, f"{path}.allowed_kinds") for x in kinds)
        if len(parsed) != len(set(parsed)):
            raise SubstrateAuthoringError(f"{path} exact-ref kind list contains duplicates")
        for kind in parsed:
            _refuse_if_forbidden_vocabulary(kind, f"{path} allowed exact-ref kind")
        return
    if set(node) != {"type", "semantic_role"}:
        raise SubstrateAuthoringError(f"{path} scalar schema fields are not exact")


def author_closed_result_schema(*, schema_id: str, semantic_class: str,
                                root: Mapping[str, Any], schema_version: str = "1.0.0") -> dict[str, Any]:
    """Build an exact closed result schema plus its exact ref."""
    if semantic_class not in ADMITTED_OBJECTIVE_SCHEMA_CLASSES:
        raise SubstrateAuthoringError(
            f"semantic_class {semantic_class!r} is outside the PRE-V3 objective-world classes")
    _validate_authored_schema_node(root, "$.root")
    material = {
        "schema_id": _text(schema_id, "schema_id"),
        "schema_version": _text(schema_version, "schema_version"),
        "semantic_class": _text(semantic_class, "semantic_class"),
        "root": _plain(root),
    }
    return {
        "schema": material,
        "schema_ref": {
            "kind": RESULT_SCHEMA_REF_KIND,
            "object_id": f"{material['schema_id']}@{material['schema_version']}",
            "content_hash": semantic_hash(material),
        },
    }


# ------------------------------------------------------- result-contract bind
@dataclass(frozen=True)
class ResultContractBinding:
    binding: Mapping[str, Any]
    binding_ref: Mapping[str, str]


def _binding_material(schema_material: Mapping[str, Any], *, binding_id: str, rule_id: str,
                      rule_version: str, authorization_state: str,
                      actor_indexing_mode: str, owner_tag: str) -> dict[str, Any]:
    return {
        "contract_id": M3_CONTRACT_ID,
        "binding_id": binding_id,
        "binding_version": "1.0.0",
        "authorization_state": authorization_state,
        "bound_rule_id": rule_id,
        "bound_rule_version": rule_version,
        "result_schema_ref": None,  # filled by caller with the recomputed schema ref
        "result_semantic_owner_ref": _ref("M3_RESULT_SEMANTIC_OWNER", f"owner:{owner_tag}:{rule_id}"),
        "result_semantic_owner_current_selection_ref": _ref(
            "M3_RESULT_OWNER_CURRENT_SELECTION", f"owner-current:{owner_tag}:{rule_id}"),
        "semantic_jurisdiction": RESULT_JURISDICTION,
        "actor_indexing_mode": actor_indexing_mode,
        "person_state_semantics": PERSON_STATE_SEMANTICS,
        "result_schema": dict(schema_material),
    }


def _expected_schema_ref(schema_material: Mapping[str, Any]) -> dict[str, str]:
    return {
        "kind": RESULT_SCHEMA_REF_KIND,
        "object_id": f"{schema_material['schema_id']}@{schema_material['schema_version']}",
        "content_hash": semantic_hash(dict(schema_material)),
    }


#: Mirrors M3 ``_RESULT_CONTRACT_FIELDS`` exactly. The seam requires an exact field
#: set with no ``contract_id``, so this validator enforces the same shape.
_EXPECTED_BINDING_FIELDS = frozenset({
    "binding_id", "binding_version", "binding_content_hash", "authorization_state",
    "bound_rule_id", "bound_rule_version", "result_schema_ref",
    "result_semantic_owner_ref", "result_semantic_owner_current_selection_ref",
    "semantic_jurisdiction", "actor_indexing_mode", "person_state_semantics",
    "result_schema",
})


def validate_result_contract_binding(binding: Mapping[str, Any]) -> None:
    """Re-validate an embedded binding, including its schema and hash (R1).

    Used by ``author_result_contract_binding``, ``author_governed_rule`` and the
    registry build, so a binding that did not come through the validated constructor
    cannot become registrable. The hash is recomputed exactly as the M3 seam
    recomputes it, so a stale or forged binding is refused here rather than only at
    evaluation time.
    """
    material = _plain(binding)
    if set(material) != _EXPECTED_BINDING_FIELDS:
        raise SubstrateAuthoringError(
            "embedded result contract fields are not the exact M3 binding field set")
    if material["authorization_state"] not in {"AUTHORIZED_CURRENT", "DENIED", "STALE", "OUT_OF_SCOPE"}:
        raise SubstrateAuthoringError("embedded result contract has a non-frozen authorization_state")
    if material["actor_indexing_mode"] not in TRANCHE_LOCAL_ACTOR_INDEXING_MODES:
        raise SubstrateAuthoringError(
            f"embedded result contract actor_indexing_mode "
            f"{material['actor_indexing_mode']!r} is withdrawn from this tranche")
    if material["semantic_jurisdiction"] != RESULT_JURISDICTION:
        raise SubstrateAuthoringError("embedded result contract leaves the PRE-V3 objective world")
    if material["person_state_semantics"] != PERSON_STATE_SEMANTICS:
        raise SubstrateAuthoringError("embedded result contract must carry person-state FORBIDDEN")
    schema = material["result_schema"]
    if not isinstance(schema, Mapping) or set(schema) != {
            "schema_id", "schema_version", "semantic_class", "root"}:
        raise SubstrateAuthoringError("embedded result_schema fields are not exact")
    if schema["semantic_class"] not in ADMITTED_OBJECTIVE_SCHEMA_CLASSES:
        raise SubstrateAuthoringError("embedded result_schema semantic_class is not an admitted class")
    _validate_authored_schema_node(schema["root"], "$.result_schema.root")
    recomputed = _expected_schema_ref(schema)
    if dict(material["result_schema_ref"]) != recomputed:
        raise SubstrateAuthoringError(
            "embedded result_schema_ref does not match the recomputed hash of its schema")
    declared_hash = _sha(material["binding_content_hash"], "binding_content_hash")
    m3_material = {"contract_id": M3_CONTRACT_ID}
    m3_material.update({k: v for k, v in material.items() if k != "binding_content_hash"})
    if declared_hash != semantic_hash(m3_material):
        raise SubstrateAuthoringError("embedded result contract content hash is stale or forged")


def author_result_contract_binding(*, binding_id: str, rule_id: str, rule_version: str,
                                   schema: Mapping[str, Any], schema_ref: Mapping[str, str],
                                   authorization_state: str = "AUTHORIZED_CURRENT",
                                   actor_indexing_mode: str = "NO_ACTOR_INDEX",
                                   owner_tag: str = "hq206") -> ResultContractBinding:
    """Build the exact M3ResultContractBinding@2.0.0 material and its ref.

    R1: the supplied schema is validated here and ``schema_ref`` is recomputed and
    required to equal it, so an open or person-state schema, or a schema_ref whose
    hash is unrelated to the schema, cannot be bound.
    """
    binding_id = _text(binding_id, "binding_id")
    rule_id = _text(rule_id, "rule_id")
    rule_version = _text(rule_version, "rule_version")
    if authorization_state not in {"AUTHORIZED_CURRENT", "DENIED", "STALE", "OUT_OF_SCOPE"}:
        raise SubstrateAuthoringError("authorization_state is not a frozen M3 result authorization state")
    if actor_indexing_mode not in TRANCHE_LOCAL_ACTOR_INDEXING_MODES:
        raise SubstrateAuthoringError(
            f"actor_indexing_mode {actor_indexing_mode!r} is withdrawn from this tranche; "
            + ACTOR_INDEXED_MODE_WITHDRAWN_REASON)

    schema_material = _plain(schema)
    if not isinstance(schema_material, Mapping):
        raise SubstrateAuthoringError("schema must be a mapping")
    for field in ("schema_id", "schema_version", "semantic_class", "root"):
        if field not in schema_material:
            raise SubstrateAuthoringError(f"schema is missing {field!r}")
    if schema_material["semantic_class"] not in ADMITTED_OBJECTIVE_SCHEMA_CLASSES:
        raise SubstrateAuthoringError("schema semantic_class is not an admitted objective-world class")
    _validate_authored_schema_node(schema_material["root"], "$.schema.root")

    recomputed = _expected_schema_ref(schema_material)
    if dict(schema_ref) != recomputed:
        raise SubstrateAuthoringError(
            "schema_ref does not resolve to the supplied schema; the ref is recomputed and "
            "must equal it exactly")

    material = _binding_material(
        schema_material, binding_id=binding_id, rule_id=rule_id, rule_version=rule_version,
        authorization_state=authorization_state, actor_indexing_mode=actor_indexing_mode,
        owner_tag=owner_tag)
    material["result_schema_ref"] = dict(recomputed)
    binding_hash = semantic_hash(material)
    binding = {k: v for k, v in material.items() if k != "contract_id"}
    binding["binding_content_hash"] = binding_hash
    binding_ref = {
        "kind": RESULT_CONTRACT_BINDING_REF_KIND,
        "object_id": f"{binding_id}@{binding['binding_version']}",
        "content_hash": binding_hash,
    }
    validate_result_contract_binding(binding)
    return ResultContractBinding(binding=_freeze(binding), binding_ref=MappingProxyType(binding_ref))


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
    """Build one exact governed V556 rule with an exact content-hash binding."""
    family = _text(semantic_family, "semantic_family")
    if family not in V556_SEMANTIC_FAMILIES:
        raise SubstrateAuthoringError(
            f"semantic_family {family!r} is not an adopted V556 family; this substrate "
            "materializes adopted semantics only and will not introduce a family")
    # Repair 2: the valid-empty families are refused AT AUTHORING, so the ceiling is a
    # machinery fact rather than a property of the shipped instance.
    if family not in TRANCHE_LOCAL_AUTHORABLE_FAMILIES:
        reason = ("it is a required-valid-empty family in this tranche"
                  if family in TRANCHE_LOCAL_VALID_EMPTY_REQUIRED_FAMILIES
                  else "it is outside the tranche-local authorable family set")
        raise SubstrateAuthoringError(
            f"semantic_family {family!r} is not authorable in this tranche because {reason}. "
            + TRANCHE_LOCAL_VALID_EMPTY_CEILING_NOTE)

    # Repair 4: POSITIVE allowlist per family, not a substring blacklist.
    allowed_roles = TRANCHE_LOCAL_FAMILY_PARTICIPANT_ROLE_MAP.get(family, ())
    roles = tuple(_text(x, "participant_roles") for x in participant_roles)
    if not roles or len(set(roles)) != len(roles):
        raise SubstrateAuthoringError("participant_roles must be non-empty and duplicate-free")
    for role in roles:
        if role not in allowed_roles:
            raise SubstrateAuthoringError(
                f"participant role {role!r} is not in the governed role allowlist for family "
                f"{family!r} {list(allowed_roles)}. " + TRANCHE_LOCAL_PARTICIPANT_ROLE_ALLOWLIST_NOTE)
        # Defence in depth only; the allowlist above is the authority ceiling.
        _refuse_if_actor_semantic_role(role, "participant_roles")
        _refuse_if_forbidden_vocabulary(role, "participant_roles")
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
    multiplicity = _text(multiplicity_policy, "multiplicity_policy")
    if multiplicity not in MULTIPLICITY_POLICIES:
        raise SubstrateAuthoringError(
            f"multiplicity_policy {multiplicity!r} is not in the frozen named vocabulary "
            f"{list(MULTIPLICITY_POLICIES)}")

    # R1: the embedded contract is re-validated, never trusted because it exists.
    if not isinstance(result_contract, ResultContractBinding):
        raise SubstrateAuthoringError("result_contract must be a ResultContractBinding")
    validate_result_contract_binding(result_contract.binding)
    binding_ref = _plain(result_contract.binding_ref)
    if binding_ref.get("kind") != RESULT_CONTRACT_BINDING_REF_KIND:
        raise SubstrateAuthoringError("result_contract_ref kind is not the frozen M3 binding kind")
    if binding_ref.get("content_hash") != result_contract.binding["binding_content_hash"]:
        raise SubstrateAuthoringError("result_contract_ref content_hash does not commit to its binding")
    # Repair 7: object_id consistency at AUTHORING, not only at the M3 seam. The ref must
    # resolve to exactly the binding it claims, so a ref relabelled onto another binding
    # cannot be authored even if its content_hash were somehow consistent.
    binding = result_contract.binding
    if binding_ref.get("object_id") != f"{binding['binding_id']}@{binding['binding_version']}":
        raise SubstrateAuthoringError(
            "result_contract_ref object_id does not resolve to its binding id@version")
    # Repair 7 / D-1: the class/family coherence decision is delegated to the shared
    # helper, with the class read from the VALIDATED binding's result_schema.
    _refuse_if_class_family_mismatch(
        semantic_class=binding["result_schema"]["semantic_class"],
        family=family, where=f"{family!r} rule {rule_id!r}")
    bound_rule_id = result_contract.binding["bound_rule_id"]
    bound_rule_version = result_contract.binding["bound_rule_version"]
    if bound_rule_id != _text(rule_id, "rule_id") or bound_rule_version != _text(rule_version, "rule_version"):
        raise SubstrateAuthoringError("result contract is bound to a different rule id/version")

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
        "multiplicity_policy": multiplicity,
        "same_route_reuse_policy": same_route_reuse_policy,
        "source_composition_policy": "NONE_BY_DEFAULT",
        "allowed_typed_outcome_states": list(states),
        "producer_allowed_uses": list(uses),
        "result_contract_binding_ref": dict(binding_ref),
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
        "multiplicity_policy": multiplicity,
        "same_route_reuse_policy": same_route_reuse_policy,
        "source_composition_policy": "NONE_BY_DEFAULT",
        "allowed_typed_outcome_states": list(states),
        "producer_allowed_uses": list(uses),
        "result_contract_binding_ref": dict(binding_ref),
    }
    key = tuple(rule[k] for k in (
        "authority_id", "authority_version", "authority_content_hash",
        "rule_id", "rule_version", "rule_content_hash"))
    return GovernedRule(
        rule=_freeze(rule), rule_key=key,
        # Repair 7: deep-freeze the stored binding here too, so immutability does not
        # wait for registry build. A hand-built ResultContractBinding that was never
        # frozen by the validated constructor is frozen at this boundary.
        result_contract=_freeze(result_contract.binding),
        result_contract_ref=MappingProxyType(dict(binding_ref)),
        semantic_family=family,
    )


# ---------------------------------------------------------------- registry
@dataclass(frozen=True)
class V556RuleMaterialRegistry:
    """Holds governed V556 rule/result-contract material.

    An empty registry is a LAWFUL VALID_EMPTY state. It never manufactures a positive
    result: with no active rule key the closed evaluator refuses.
    """

    rules: tuple[GovernedRule, ...] = ()

    @staticmethod
    def build(rules: Iterable[GovernedRule]) -> "V556RuleMaterialRegistry":
        seen: set[tuple[str, ...]] = set()
        families: set[str] = set()
        out: list[GovernedRule] = []
        for r in rules:
            if not isinstance(r, GovernedRule):
                raise SubstrateAuthoringError("registry accepts only GovernedRule material")
            # R5: the registry is an unguarded publication surface; enforce the frozen
            # family set HERE, not only in the rule author and the M3 seam.
            if r.semantic_family not in SUPPORTED_FAMILIES:
                raise SubstrateAuthoringError(
                    f"registry build refuses non-frozen semantic_family {r.semantic_family!r}")
            # Repair 2: enforced at REGISTRY BUILD as well as at authoring, so a
            # hand-constructed GovernedRule cannot bypass the valid-empty ceiling.
            if r.semantic_family not in TRANCHE_LOCAL_AUTHORABLE_FAMILIES:
                raise SubstrateAuthoringError(
                    f"registry build refuses authorable-in-tranche family "
                    f"{r.semantic_family!r}; it is a required-valid-empty family. "
                    + TRANCHE_LOCAL_VALID_EMPTY_CEILING_NOTE)
            # Repair 4: re-check the role allowlist at build, so a hand-constructed rule
            # cannot carry an unlisted participant role into GOVERNED_RULES_PRESENT.
            allowed_roles = TRANCHE_LOCAL_FAMILY_PARTICIPANT_ROLE_MAP.get(r.semantic_family, ())
            for role in _plain(r.rule).get("participant_roles", ()):
                if role not in allowed_roles:
                    raise SubstrateAuthoringError(
                        f"registry build refuses participant role {role!r} outside the governed "
                        f"allowlist for {r.semantic_family!r}. "
                        + TRANCHE_LOCAL_PARTICIPANT_ROLE_ALLOWLIST_NOTE)
            # R1: re-validate embedded material before it can become GOVERNED_RULES_PRESENT.
            validate_result_contract_binding(r.result_contract)
            rule_plain = _plain(r.rule)
            if rule_plain.get("semantic_family") != r.semantic_family:
                raise SubstrateAuthoringError("registry material family disagrees with its rule body")
            # D-1: independent class/family coherence at the registry surface. The class is
            # read from the VALIDATED contract (not from a caller-side field) and the family
            # from the rule body (not from the dataclass attribute, which is cross-checked
            # one line above but is still caller-supplied). A hand-built, consistently
            # rehashed rule cannot carry a class its family does not authorize.
            _refuse_if_class_family_mismatch(
                semantic_class=_plain(r.result_contract)["result_schema"]["semantic_class"],
                family=rule_plain["semantic_family"],
                where=f"registry material rule {rule_plain.get('rule_id')!r}")
            if dict(r.result_contract_ref) != dict(rule_plain["result_contract_binding_ref"]):
                raise SubstrateAuthoringError("registry material contract ref disagrees with its rule body")
            rule_body = {"contract_id": M3_CONTRACT_ID}
            rule_body.update({k: v for k, v in rule_plain.items()
                              if k not in ("rule_content_hash", "authority_id",
                                           "authority_version", "authority_content_hash")})
            if rule_plain["rule_content_hash"] != semantic_hash(rule_body):
                raise SubstrateAuthoringError("registry material rule_content_hash is stale or forged")
            if r.rule_key in seen:
                raise SubstrateAuthoringError("duplicate governed rule key in registry")
            if r.semantic_family in families and TRANCHE_LOCAL_ONE_RULE_PER_FAMILY:
                raise SubstrateAuthoringError(
                    "at most one governed rule per semantic family in this tranche; "
                    + TRANCHE_LOCAL_ONE_RULE_PER_FAMILY_NOTE)
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
            "repair_id": REPAIR_ID,
            "state": self.state,
            "registered_rule_count": self.registered_rule_count,
            "populated_families": list(self.populated_families),
            "unfilled_families": list(self.unfilled_families),
            "active_rule_keys": self.active_rule_keys(),
            "active_result_contract_refs": self.active_result_contract_refs(),
            "tranche_local_one_rule_per_family": TRANCHE_LOCAL_ONE_RULE_PER_FAMILY,
            "tranche_local_one_rule_per_family_note": TRANCHE_LOCAL_ONE_RULE_PER_FAMILY_NOTE,
            "tranche_local_admitted_role_narrowing": _plain(TRANCHE_LOCAL_ADMITTED_ROLE_NARROWING),
            "actor_indexing_modes": list(TRANCHE_LOCAL_ACTOR_INDEXING_MODES),
            "authorized_interaction_relation_kinds": list(AUTHORIZED_INTERACTION_RELATION_KINDS),
            "td_r03_non_inferable_f1_premise_kinds": list(TD_R03_NON_INFERABLE_F1_PREMISE_KINDS),
            "tranche_local_authorable_families": list(TRANCHE_LOCAL_AUTHORABLE_FAMILIES),
            "tranche_local_valid_empty_required_families":
                list(TRANCHE_LOCAL_VALID_EMPTY_REQUIRED_FAMILIES),
            "tranche_local_valid_empty_ceiling_note": TRANCHE_LOCAL_VALID_EMPTY_CEILING_NOTE,
            "tranche_local_family_participant_role_map":
                {k: list(v) for k, v in TRANCHE_LOCAL_FAMILY_PARTICIPANT_ROLE_MAP.items()},
            "tranche_local_participant_role_allowlist_note":
                TRANCHE_LOCAL_PARTICIPANT_ROLE_ALLOWLIST_NOTE,
            "tranche_local_admitted_schema_class_family_map":
                dict(TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP),
            "tranche_local_schema_class_withdrawal_note":
                TRANCHE_LOCAL_SCHEMA_CLASS_WITHDRAWAL_NOTE,
            # Repair 6: these two labels are DOCUMENTARY and are surfaced HERE only. They
            # are deliberately NOT embedded in the emitted rule/schema/contract material,
            # and the court asserts that absence so the claim stays exactly true.
            "topology_canary_shape_label": TOPOLOGY_CANARY_SHAPE_LABEL,
            "topology_canary_f2_claim": TOPOLOGY_CANARY_F2_CLAIM,
            "illustrative_labels_are_snapshot_only": True,
        }


# -------------------------------------------------- R4 payload-to-participant binding
#: HQ214 Repair D-4. MACHINE-READABLE classification of the payload-participant helper.
#: The HQ211 court proved this status by searching the helper's DOCSTRING for words, which
#: is decorative: prose can be reworded without changing behaviour. This record makes the
#: claim a data value the court asserts field by field, and the seam-absence half is proved
#: behaviourally by inspecting the seam source for the helper name.
#:
#: The classification is TRUTHFUL, not aspirational: this helper is genuinely not wired into
#: the adopted M3 seam or into any evaluation path. HQ211/HQ214 forbid adding a seam merely
#: to make it "real", so it stays a court/helper utility and is declared as one.
PAYLOAD_PARTICIPANT_HELPER_NAME = "validate_payload_against_participants"

PAYLOAD_PARTICIPANT_HELPER_CLASSIFICATION: Mapping[str, Any] = MappingProxyType({
    "helper": PAYLOAD_PARTICIPANT_HELPER_NAME,
    "classification": "COURT_HELPER_VALIDATION_UTILITY",
    "is_seam_enforcement": False,
    "is_production_evaluation_path": False,
    "invoked_by_m3_seam": False,
    "invoked_by_evaluation_path": False,
    "new_seam_added_to_make_it_real": False,
    "classification_is_declared_not_aspirational": True,
    "why": "wiring this helper into evaluation would require a new seam, which HQ211 and "
           "HQ214 forbid; it is therefore declared a court/helper utility and no claim of "
           "production enforcement is made anywhere",
})


def validate_payload_against_participants(rule: GovernedRule,
                                          payload: Mapping[str, Any],
                                          participant_bindings: Sequence[Mapping[str, Any]],
                                          payload_route_fields: Sequence[str]) -> None:
    """Court/helper validation utility. NOT seam enforcement.

    The machine-readable truth about this helper is
    ``PAYLOAD_PARTICIPANT_HELPER_CLASSIFICATION``; this docstring is explanation, not
    the authority for that classification. See that record for why the helper is not on
    the evaluation path and why no seam was added to change that.
    """
    rule_plain = _plain(rule.rule)
    # A governed route identity carries BOTH identifiers M3 itself commits to
    # (object_id = route_id, content_hash = semantic_hash(route)). Accept either,
    # so a payload names the same exact route the participant governs.
    governed: set[str] = set()
    for binding in participant_bindings:
        for field in ("v555_route_identity_ref", "source_universe_ref"):
            value = binding.get(field)
            if isinstance(value, Mapping):
                for key in ("object_id", "content_hash"):
                    if value.get(key):
                        governed.add(str(value[key]))
    minimum = rule_plain["minimum_cardinality"]
    if len(participant_bindings) < minimum:
        raise SubstrateAuthoringError(
            f"participant count {len(participant_bindings)} is below the rule minimum {minimum}")
    maximum = rule_plain["maximum_cardinality_or_unbounded_marker"]
    if maximum != "UNBOUNDED" and len(participant_bindings) > maximum:
        raise SubstrateAuthoringError(
            f"participant count {len(participant_bindings)} exceeds the rule maximum {maximum}")

    payload_plain = _plain(payload)
    for field in payload_route_fields:
        if field not in payload_plain:
            raise SubstrateAuthoringError(f"payload is missing required route field {field!r}")
        value = payload_plain[field]
        if not isinstance(value, Mapping):
            raise SubstrateAuthoringError(f"payload route field {field!r} must be an exact ref")
        candidates = {str(value[k]) for k in ("object_id", "content_hash") if value.get(k)}
        if not candidates or not (candidates & governed):
            raise SubstrateAuthoringError(
                f"payload route field {field!r} is not bound to any governed participant "
                "v555 route identity")


# -------------------------------------------------- source-free canary packs
#: TRANCHE-LOCAL declared shape, recorded in the material so the canary cannot be
#: mistaken for a generic V556_TOPOLOGY instance (review F4).
TOPOLOGY_CANARY_SHAPE_LABEL = "HQ206_ONE_ILLUSTRATIVE_AUTHORIZED_DYADIC_INCIDENCE_SHAPE"
TOPOLOGY_CANARY_MAX_CARDINALITY = 2

#: The topology canary does NOT materialize TD_R03 §8's F2 attractor-prerequisite
#: topology grain. Recorded explicitly so the material cannot claim otherwise.
TOPOLOGY_CANARY_F2_CLAIM = (
    "NOT_AN_F2_ATTRACTOR_PREREQUISITE_TOPOLOGY__NO_F2_GRAIN_CLAIMED"
)


def _topology_schema() -> dict[str, Any]:
    """Truthful dyadic endpoint/incidence shape with route-kind-bound refs."""
    return author_closed_result_schema(
        schema_id="HQ206_CANARY_V556_TOPOLOGY_DYADIC_INCIDENCE_RESULT",
        semantic_class="OBJECTIVE_STRUCTURAL_RESULT",
        root=_node_object(
            {
                "endpoint_a_ref": _node_exact_ref("OBJECTIVE_REFERENCE", (V555_FAMILY,)),
                "endpoint_b_ref": _node_exact_ref("OBJECTIVE_REFERENCE", (V555_FAMILY,)),
                "incidence_kind": _node_string("OBJECTIVE_STRUCTURAL_RELATION",
                                               PERMITTED_INCIDENCE_KINDS),
            },
            ("endpoint_a_ref", "endpoint_b_ref", "incidence_kind"),
        ),
    )


def topology_canary_rule(*, rule_id: str = "V556-HQ206-TOPOLOGY-DYADIC-CANARY",
                         authority_id: str = "V556_HQ206_CANARY_AUTHORITY",
                         authority_version: str = "1.0.0",
                         authority_content_hash: str | None = None) -> GovernedRule:
    """One illustrative authorized source-free V556_TOPOLOGY shape.

    R4: the declared maximum is the truthful dyadic 2, never a false UNBOUNDED. The
    previous mandatory ``shared_structural_channel_ref`` is removed, so the shape is
    no longer structurally a shared-channel dyad. It makes no F2 claim.
    """
    built = _topology_schema()
    contract = author_result_contract_binding(
        binding_id=f"M3-RESULT-BINDING-{rule_id}", rule_id=rule_id, rule_version="1.0.0",
        schema=built["schema"], schema_ref=built["schema_ref"], owner_tag="hq206-topology")
    return author_governed_rule(
        authority_id=authority_id,
        authority_version=authority_version,
        authority_content_hash=authority_content_hash
        or semantic_hash(["V556_HQ206_CANARY_AUTHORITY", authority_version]),
        rule_id=rule_id,
        rule_version="1.0.0",
        semantic_family="V556_TOPOLOGY",
        participant_roles=("STRUCTURAL_ENDPOINT_A", "STRUCTURAL_ENDPOINT_B"),
        participant_order_policy="ORDERED",
        minimum_cardinality=2,
        maximum_cardinality_or_unbounded_marker=TOPOLOGY_CANARY_MAX_CARDINALITY,
        same_route_reuse_policy="FORBIDDEN",
        result_contract=contract,
    )


def interaction_relation_canary_rule(**_kwargs: Any) -> GovernedRule:
    """REFUSED: no governed V556 interaction-rule authority exists.

    TD_R03 §5 forbids an F1 from being created solely from coexistence, shared
    channel/mediator, or parallel occurrence, and §6 records that no complete governed
    interaction-rule authority was found. The previous tranche minted exactly those
    three forbidden premises as its constituting relation kinds. Rather than fabricate a
    replacement positive relation kind to preserve a canary, this refuses and the family
    is returned lawfully VALID_EMPTY.
    """
    raise SubstrateAuthoringError(
        "V556_INTERACTION_RELATION cannot be populated in this tranche: TD_R03 §5 forbids an F1 "
        "constituted solely by coexistence/shared-channel/parallel-occurrence, and §6 records that "
        "no complete governed V556 interaction-rule authority exists. AUTHORIZED_INTERACTION_RELATION_KINDS "
        "is empty, so the family is lawfully VALID_EMPTY pending a governed interaction-rule registry.")


def source_free_canary_registry() -> V556RuleMaterialRegistry:
    """The tranche's source-free registry.

    V556_INTERACTION_RELATION and V556_ATTRACTOR_PREREQUISITE are both lawfully
    unfilled. No positive interaction rule is fabricated and no attractor prerequisite
    is populated.
    """
    return V556RuleMaterialRegistry.build([topology_canary_rule()])


__all__ = [
    "SUBSTRATE_CONTRACT_ID",
    "REPAIR_ID",
    "VALID_EMPTY_NO_GOVERNED_RULE",
    "SUPPORTED_FAMILIES",
    "ALLOWED_TYPED_OUTCOME_STATES",
    "ADMITTED_OBJECTIVE_ROLES",
    "ADMITTED_OBJECTIVE_SCHEMA_CLASSES",
    "TRANCHE_LOCAL_ADMITTED_ROLE_NARROWING",
    "TRANCHE_LOCAL_ONE_RULE_PER_FAMILY",
    "TRANCHE_LOCAL_ONE_RULE_PER_FAMILY_NOTE",
    "TRANCHE_LOCAL_ACTOR_INDEXING_MODES",
    "ACTOR_INDEXED_MODE_WITHDRAWN_REASON",
    "MULTIPLICITY_POLICIES",
    "TD_R03_NON_INFERABLE_F1_PREMISE_KINDS",
    "TRANCHE_LOCAL_AUTHORABLE_FAMILIES",
    "TRANCHE_LOCAL_VALID_EMPTY_REQUIRED_FAMILIES",
    "TRANCHE_LOCAL_VALID_EMPTY_CEILING_NOTE",
    "TRANCHE_LOCAL_FAMILY_PARTICIPANT_ROLE_MAP",
    "TRANCHE_LOCAL_PARTICIPANT_ROLE_ALLOWLIST_NOTE",
    "TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP",
    "TRANCHE_LOCAL_SCHEMA_CLASS_WITHDRAWAL_NOTE",
    "AUTHORIZED_INTERACTION_RELATION_KINDS",
    "TD_R03_CANDIDATE_RELATION_KINDS_NOT_CANONIZED",
    "BLOCKED_STRONG_NOUNS",
    "PERMITTED_INCIDENCE_KINDS",
    "TOPOLOGY_CANARY_SHAPE_LABEL",
    "TOPOLOGY_CANARY_MAX_CARDINALITY",
    "TOPOLOGY_CANARY_F2_CLAIM",
    "SubstrateAuthoringError",
    "ResultContractBinding",
    "GovernedRule",
    "V556RuleMaterialRegistry",
    "author_closed_result_schema",
    "validate_result_contract_binding",
    "author_result_contract_binding",
    "author_governed_rule",
    "PAYLOAD_PARTICIPANT_HELPER_NAME",
    "PAYLOAD_PARTICIPANT_HELPER_CLASSIFICATION",
    "validate_payload_against_participants",
    "topology_canary_rule",
    "interaction_relation_canary_rule",
    "source_free_canary_registry",
]