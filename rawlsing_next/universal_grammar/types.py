"""R61 generic source-owned symbolic grammar types (TEST_ONLY proposal).

The inventory is typed by source-owned occurrence identity and semantic roles.
No item label, reserved question name, fixed scientific arity or observed value
selects membership in the prospective frontier.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash

OCCURRENCE_SCHEMA = "UniversalOccurrence@r61.1"
INVENTORY_SCHEMA = "UniversalSourceInventory@r61.1"
POLICY_SCHEMA = "UniversalGrammarPolicy@r61.1"
OPERATION_SCHEMA = "UniversalOperation@r61.1"
FRONTIER_SCHEMA = "UniversalFrontier@r61.1"
PARTITION_SCHEMA = "UniversalFrontierPartition@r61.1"

ADMINISTERED = "ADMINISTERED"
NOT_ADMINISTERED = "NOT_ADMINISTERED"
ADMINISTRATION_UNKNOWN = "UNKNOWN"
ADMINISTRATION_STATES = (ADMINISTERED, NOT_ADMINISTERED, ADMINISTRATION_UNKNOWN)

SCALAR_TOPOLOGY = "SCALAR_SINGULAR"

ELIGIBLE = "ELIGIBLE"
PROHIBITED = "PROHIBITED"
INAPPLICABLE_PROVED = "INAPPLICABLE_PROVED"
HELD = "HELD"
UNKNOWN = "UNKNOWN"
UNSUPPORTED_RUNTIME = "UNSUPPORTED_RUNTIME"
DEFERRED = "DEFERRED"

DISPOSITIONS = (
    ELIGIBLE, PROHIBITED, INAPPLICABLE_PROVED, HELD, UNKNOWN,
    UNSUPPORTED_RUNTIME, DEFERRED,
)
CONSIDERED_DISPOSITIONS = (
    ELIGIBLE, PROHIBITED, INAPPLICABLE_PROVED, HELD, UNKNOWN,
)


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _texts(values: Iterable[Any], name: str, *, allow_empty: bool = True) -> tuple[str, ...]:
    result = tuple(_text(value, name) for value in values)
    if not allow_empty and not result:
        raise ValueError(f"{name} may not be empty")
    if len(set(result)) != len(result):
        raise ValueError(f"{name} contains duplicates")
    return result


def _role_texts(values: Iterable[Any], name: str, *, allow_empty: bool = True) -> tuple[str, ...]:
    result = tuple(_text(value, name) for value in values)
    if not allow_empty and not result:
        raise ValueError(f"{name} may not be empty")
    return result


def _material(value: Any) -> Any:
    if hasattr(value, "material"):
        return _material(value.material())
    if hasattr(value, "as_dict"):
        return _material(value.as_dict())
    if isinstance(value, Mapping):
        return {str(k): _material(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_material(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_material(v) for v in value), key=lambda x: json.dumps(x, sort_keys=True))
    return value


def content_hash(value: Any) -> str:
    return semantic_hash(_material(value))


@dataclass(frozen=True, order=True)
class OccurrenceKey:
    """Exact source-native occurrence identity, never only a column name."""

    item_id: str
    option_id: str | None = None
    form_id: str | None = None
    repeat_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "item_id", _text(self.item_id, "item_id"))
        for name in ("option_id", "form_id", "repeat_id"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _text(value, name))

    def material(self) -> dict[str, str | None]:
        return {
            "item_id": self.item_id,
            "option_id": self.option_id,
            "form_id": self.form_id,
            "repeat_id": self.repeat_id,
        }

    def as_tuple(self) -> tuple[str, str | None, str | None, str | None]:
        return (self.item_id, self.option_id, self.form_id, self.repeat_id)

    @property
    def key(self) -> str:
        return json.dumps(self.material(), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class Occurrence:
    key: OccurrenceKey
    label: str
    unit: str
    topology: str = SCALAR_TOPOLOGY
    forms: tuple[str, ...] = ("DEFAULT_FORM",)
    domain: tuple[Any, ...] = (0, 1)
    target_role: str | None = None
    conditioner_role: str | None = None
    administrative_role: str | None = None
    administration: str = ADMINISTERED
    route_state: str = "KNOWN"
    semantic_state: str = "UNRESOLVED"
    scope: str = ""
    risk_set_refs: tuple[str, ...] = ()
    schema: str = OCCURRENCE_SCHEMA

    def __post_init__(self) -> None:
        if self.schema != OCCURRENCE_SCHEMA:
            raise ValueError(f"INCOMPATIBLE_OCCURRENCE_SCHEMA:{self.schema}")
        object.__setattr__(self, "label", _text(self.label, "label"))
        object.__setattr__(self, "unit", _text(self.unit, "unit"))
        object.__setattr__(self, "topology", _text(self.topology, "topology"))
        object.__setattr__(self, "forms", _texts(self.forms, "forms", allow_empty=False))
        if not isinstance(self.domain, tuple):
            object.__setattr__(self, "domain", tuple(self.domain))
        if not self.domain:
            raise ValueError("domain may not be empty")
        for value in self.domain:
            if isinstance(value, (float, bool)) or value is None:
                raise ValueError("domain values must be exact non-float scalars")
            canonicalize(value)
        if len({json.dumps(canonicalize(v), sort_keys=True) for v in self.domain}) != len(self.domain):
            raise ValueError("domain contains duplicate typed values")
        for name in ("target_role", "conditioner_role", "administrative_role"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _text(value, name))
        object.__setattr__(self, "administration", _text(self.administration, "administration"))
        if self.administration not in ADMINISTRATION_STATES:
            raise ValueError(f"UNKNOWN_ADMINISTRATION_STATE:{self.administration}")
        object.__setattr__(self, "route_state", _text(self.route_state, "route_state"))
        object.__setattr__(self, "semantic_state", _text(self.semantic_state, "semantic_state"))
        object.__setattr__(self, "scope", _text(self.scope, "scope"))
        object.__setattr__(self, "risk_set_refs", _texts(self.risk_set_refs, "risk_set_refs"))

    @property
    def occurrence_id(self) -> str:
        return self.key.key

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema, "key": self.key.material(), "label": self.label,
            "unit": self.unit, "topology": self.topology, "forms": list(self.forms),
            "domain": [_material(value) for value in self.domain],
            "target_role": self.target_role, "conditioner_role": self.conditioner_role,
            "administrative_role": self.administrative_role,
            "administration": self.administration, "route_state": self.route_state,
            "semantic_state": self.semantic_state, "scope": self.scope,
            "risk_set_refs": list(self.risk_set_refs),
        }


@dataclass(frozen=True)
class MeasurePlan:
    measure_id: str
    kind: str
    weight_ref: str | None
    design_ref: str | None
    estimand: str
    variance_policy: str

    def __post_init__(self) -> None:
        for name in ("measure_id", "kind", "estimand", "variance_policy"):
            object.__setattr__(self, name, _text(getattr(self, name), name))
        if self.kind not in {"SAMPLE", "POPULATION"}:
            raise ValueError(f"UNKNOWN_MEASURE_KIND:{self.kind}")
        for name in ("weight_ref", "design_ref"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _text(value, name))

    def material(self) -> dict[str, Any]:
        return {
            "measure_id": self.measure_id, "kind": self.kind,
            "weight_ref": self.weight_ref, "design_ref": self.design_ref,
            "estimand": self.estimand, "variance_policy": self.variance_policy,
        }


@dataclass(frozen=True)
class SourceInventory:
    inventory_id: str
    source_id: str
    wave: str
    edition: str
    source_sha256: str
    scope: str
    occurrences: tuple[Occurrence, ...]
    measure_plans: tuple[MeasurePlan, ...]
    risk_set_refs: tuple[str, ...]
    unit_transforms: tuple[str, ...]
    state_map: Mapping[str, str]
    authority_refs: tuple[str, ...]
    current_selection: str | None
    inventory_complete: bool
    inventory_gaps: tuple[str, ...] = ()
    held: tuple[str, ...] = ()
    unresolved: tuple[str, ...] = ()
    schema: str = INVENTORY_SCHEMA

    def __post_init__(self) -> None:
        if self.schema != INVENTORY_SCHEMA:
            raise ValueError(f"INCOMPATIBLE_INVENTORY_SCHEMA:{self.schema}")
        for name in ("inventory_id", "source_id", "wave", "edition", "source_sha256", "scope"):
            object.__setattr__(self, name, _text(getattr(self, name), name))
        if len(self.source_sha256) != 64:
            raise ValueError("source_sha256 must be 64 hexadecimal characters")
        if not self.occurrences:
            raise ValueError("inventory must contain at least one occurrence")
        seen: set[tuple[str, str | None, str | None, str | None]] = set()
        for occurrence in self.occurrences:
            if not isinstance(occurrence, Occurrence):
                raise TypeError("occurrences must be typed Occurrence objects")
            identity = occurrence.key.as_tuple()
            if identity in seen:
                raise ValueError(f"DUPLICATE_OCCURRENCE:{occurrence.key.key}")
            seen.add(identity)
        if len({m.measure_id for m in self.measure_plans}) != len(self.measure_plans):
            raise ValueError("duplicate measure_id")
        if not isinstance(self.state_map, Mapping):
            raise TypeError("state_map must be a mapping")
        object.__setattr__(self, "state_map", {str(k): str(v) for k, v in self.state_map.items()})
        object.__setattr__(self, "risk_set_refs", _texts(self.risk_set_refs, "risk_set_refs"))
        object.__setattr__(self, "unit_transforms", _texts(self.unit_transforms, "unit_transforms"))
        object.__setattr__(self, "authority_refs", _texts(self.authority_refs, "authority_refs"))
        object.__setattr__(self, "inventory_gaps", _texts(self.inventory_gaps, "inventory_gaps"))
        object.__setattr__(self, "held", _texts(self.held, "held"))
        object.__setattr__(self, "unresolved", _texts(self.unresolved, "unresolved"))
        if self.current_selection is not None:
            object.__setattr__(self, "current_selection", _text(self.current_selection, "current_selection"))
        if not isinstance(self.inventory_complete, bool):
            raise TypeError("inventory_complete must be bool")
        if not self.inventory_complete and not self.inventory_gaps:
            raise ValueError("incomplete inventory must state its exact gaps")

    def by_key(self) -> dict[OccurrenceKey, Occurrence]:
        return {occurrence.key: occurrence for occurrence in self.occurrences}

    def require_version(self) -> None:
        if self.schema != INVENTORY_SCHEMA:
            raise ValueError(f"INCOMPATIBLE_INVENTORY_SCHEMA:{self.schema}")

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema, "inventory_id": self.inventory_id,
            "source_id": self.source_id, "wave": self.wave, "edition": self.edition,
            "source_sha256": self.source_sha256, "scope": self.scope,
            "occurrences": [o.material() for o in sorted(self.occurrences, key=lambda x: x.key.key)],
            "measure_plans": [m.material() for m in sorted(self.measure_plans, key=lambda x: x.measure_id)],
            "risk_set_refs": list(self.risk_set_refs),
            "unit_transforms": list(self.unit_transforms), "state_map": dict(self.state_map),
            "authority_refs": list(self.authority_refs), "current_selection": self.current_selection,
            "inventory_complete": self.inventory_complete,
            "inventory_gaps": list(self.inventory_gaps), "held": list(self.held),
            "unresolved": list(self.unresolved),
        }

    @property
    def content_hash(self) -> str:
        return content_hash(self.material())


@dataclass(frozen=True)
class DirectionGrant:
    target_roles: tuple[str, ...]
    conditioner_roles: tuple[str, ...]
    claim_class: str
    direction_ref: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_roles", _role_texts(self.target_roles, "target_roles", allow_empty=False))
        object.__setattr__(self, "conditioner_roles", _role_texts(self.conditioner_roles, "conditioner_roles"))
        object.__setattr__(self, "claim_class", _text(self.claim_class, "claim_class"))
        object.__setattr__(self, "direction_ref", _text(self.direction_ref, "direction_ref"))

    def covers(self, target_roles: tuple[str, ...], conditioner_roles: tuple[str, ...], claim_class: str) -> bool:
        return (
            self.claim_class == claim_class
            and self.target_roles == target_roles
            and self.conditioner_roles == conditioner_roles
        )

    def material(self) -> dict[str, Any]:
        return {
            "target_roles": list(self.target_roles),
            "conditioner_roles": list(self.conditioner_roles),
            "claim_class": self.claim_class, "direction_ref": self.direction_ref,
        }


@dataclass(frozen=True)
class GrammarPolicy:
    policy_id: str
    grade: str
    allowed_classes: tuple[str, ...]
    separate_classes: tuple[str, ...]
    target_roles: tuple[str, ...]
    conditioner_roles: tuple[str, ...]
    administrative_roles: tuple[str, ...]
    direction_grants: tuple[DirectionGrant, ...]
    bounds: Mapping[str, int]
    population_requires_weight: bool
    validation_policy: str
    exploration_policy: str
    stop_policy: str
    owner_refs: tuple[str, ...]
    authority_refs: tuple[str, ...]
    schema: str = POLICY_SCHEMA

    def __post_init__(self) -> None:
        if self.schema != POLICY_SCHEMA:
            raise ValueError(f"INCOMPATIBLE_POLICY_SCHEMA:{self.schema}")
        for name in ("policy_id", "grade", "validation_policy", "exploration_policy", "stop_policy"):
            object.__setattr__(self, name, _text(getattr(self, name), name))
        if self.grade not in {"PROPOSED_TEST_ONLY", "COMPETENT_ISSUED"}:
            raise ValueError(f"UNKNOWN_POLICY_GRADE:{self.grade}")
        for name in ("allowed_classes", "separate_classes", "target_roles",
                     "conditioner_roles", "administrative_roles", "owner_refs", "authority_refs"):
            object.__setattr__(self, name, _texts(getattr(self, name), name))
        overlap = set(self.allowed_classes) & set(self.separate_classes)
        if overlap:
            raise ValueError(f"CLASS_CANNOT_BE_ALLOWED_AND_SEPARATE:{sorted(overlap)}")
        if not isinstance(self.bounds, Mapping):
            raise TypeError("bounds must be a mapping")
        normalized: dict[str, int] = {}
        for name in ("J", "K", "D"):
            value = self.bounds.get(name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"BOUND_{name}_MUST_BE_NONNEGATIVE_INTEGER")
            normalized[name] = value
        if normalized["J"] < 1:
            raise ValueError("BOUND_J_MUST_BE_POSITIVE")
        object.__setattr__(self, "bounds", normalized)
        if not isinstance(self.population_requires_weight, bool):
            raise TypeError("population_requires_weight must be bool")
        if not isinstance(self.direction_grants, tuple) or not all(
            isinstance(g, DirectionGrant) for g in self.direction_grants
        ):
            raise TypeError("direction_grants must be DirectionGrant tuple")

    def direction_for(
        self, target_roles: tuple[str, ...], conditioner_roles: tuple[str, ...], claim_class: str
    ) -> DirectionGrant | None:
        for grant in self.direction_grants:
            if grant.covers(target_roles, conditioner_roles, claim_class):
                return grant
        return None

    def require_version(self) -> None:
        if self.schema != POLICY_SCHEMA:
            raise ValueError(f"INCOMPATIBLE_POLICY_SCHEMA:{self.schema}")
        if self.grade not in {"PROPOSED_TEST_ONLY", "COMPETENT_ISSUED"}:
            raise ValueError(f"UNKNOWN_POLICY_GRADE:{self.grade}")

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema, "policy_id": self.policy_id, "grade": self.grade,
            "allowed_classes": list(self.allowed_classes),
            "separate_classes": list(self.separate_classes),
            "target_roles": list(self.target_roles),
            "conditioner_roles": list(self.conditioner_roles),
            "administrative_roles": list(self.administrative_roles),
            "direction_grants": [g.material() for g in self.direction_grants],
            "bounds": dict(self.bounds),
            "population_requires_weight": self.population_requires_weight,
            "validation_policy": self.validation_policy,
            "exploration_policy": self.exploration_policy,
            "stop_policy": self.stop_policy,
            "owner_refs": list(self.owner_refs), "authority_refs": list(self.authority_refs),
        }

    @property
    def content_hash(self) -> str:
        return content_hash(self.material())


@dataclass(frozen=True)
class ScientificOperation:
    op_id: str
    claim_class: str
    targets: tuple[OccurrenceKey, ...]
    target_roles: tuple[str, ...]
    conditions: tuple[tuple[OccurrenceKey, Any], ...]
    conditioner_roles: tuple[str, ...]
    condition_mode: str
    unit: str
    topology: str
    state_variant: str
    measure_id: str
    measure_kind: str
    risk_set_ref: str | None
    risk_set_refs: tuple[str, ...]
    direction_ref: str | None
    form_scope: tuple[str, ...]
    scope: str
    branch_depth: int
    source_inventory: str
    policy_id: str
    policy_hash: str
    disposition: str
    reasons: tuple[str, ...] = ()
    native_support: str = "UNMAPPED"
    administration_states: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    schema: str = OPERATION_SCHEMA

    def __post_init__(self) -> None:
        if self.schema != OPERATION_SCHEMA:
            raise ValueError(f"INCOMPATIBLE_OPERATION_SCHEMA:{self.schema}")
        if not isinstance(self.targets, tuple) or not self.targets:
            raise ValueError("operation must have at least one target occurrence")
        if not isinstance(self.conditions, tuple):
            raise ValueError("conditions must be a tuple")
        if self.disposition not in DISPOSITIONS:
            raise ValueError(f"UNKNOWN_DISPOSITION:{self.disposition}")
        if self.branch_depth < 0:
            raise ValueError("branch_depth must be nonnegative")

    def identity_material(self) -> dict[str, Any]:
        return {
            "schema": self.schema, "claim_class": self.claim_class,
            "targets": [key.material() for key in self.targets],
            "target_roles": list(self.target_roles),
            "conditions": [[key.material(), _material(value)] for key, value in self.conditions],
            "conditioner_roles": list(self.conditioner_roles),
            "condition_mode": self.condition_mode, "unit": self.unit,
            "topology": self.topology, "state_variant": self.state_variant,
            "measure_id": self.measure_id, "measure_kind": self.measure_kind,
            "risk_set_ref": self.risk_set_ref, "risk_set_refs": list(self.risk_set_refs),
            "direction_ref": self.direction_ref, "form_scope": list(self.form_scope),
            "scope": self.scope, "branch_depth": self.branch_depth,
            "source_inventory": self.source_inventory, "policy_id": self.policy_id,
            "policy_hash": self.policy_hash,
            "administration_states": list(self.administration_states),
        }

    @property
    def canonical_hash(self) -> str:
        return semantic_hash(self.identity_material())

    def material(self) -> dict[str, Any]:
        return {
            **self.identity_material(), "op_id": self.op_id,
            "candidate_hash": self.canonical_hash, "disposition": self.disposition,
            "reasons": list(self.reasons), "native_support": self.native_support,
            "aliases": list(self.aliases),
        }


def make_operation(
    *,
    inventory: SourceInventory,
    policy: GrammarPolicy,
    claim_class: str,
    targets: Sequence[OccurrenceKey],
    target_roles: Sequence[str],
    conditions: Sequence[tuple[OccurrenceKey, Any]] = (),
    conditioner_roles: Sequence[str] = (),
    condition_mode: str = "AND",
    unit: str,
    topology: str = SCALAR_TOPOLOGY,
    state_variant: str = "COMPLETE_RESPONSE",
    measure: MeasurePlan,
    risk_set_ref: str | None,
    risk_set_refs: Sequence[str],
    direction_ref: str | None,
    form_scope: Sequence[str],
    scope: str,
    branch_depth: int = 0,
    disposition: str = ELIGIBLE,
    reasons: Sequence[str] = (),
    native_support: str = "UNMAPPED",
    administration_states: Sequence[str] = (),
    aliases: Sequence[str] = (),
) -> ScientificOperation:
    provisional = ScientificOperation(
        op_id="",
        claim_class=claim_class,
        targets=tuple(targets),
        target_roles=tuple(target_roles),
        conditions=tuple(conditions),
        conditioner_roles=tuple(conditioner_roles),
        condition_mode=condition_mode,
        unit=unit,
        topology=topology,
        state_variant=state_variant,
        measure_id=measure.measure_id,
        measure_kind=measure.kind,
        risk_set_ref=risk_set_ref,
        risk_set_refs=tuple(risk_set_refs),
        direction_ref=direction_ref,
        form_scope=tuple(form_scope),
        scope=scope,
        branch_depth=branch_depth,
        source_inventory=inventory.inventory_id,
        policy_id=policy.policy_id,
        policy_hash=policy.content_hash,
        disposition=disposition,
        reasons=tuple(reasons),
        native_support=native_support,
        administration_states=tuple(administration_states),
        aliases=tuple(aliases),
    )
    return ScientificOperation(
        **{
            **{name: getattr(provisional, name) for name in provisional.__dataclass_fields__},
            "op_id": "urn:r61:op:" + provisional.canonical_hash,
        }
    )


@dataclass(frozen=True)
class InventoryLedgerEntry:
    occurrence_id: str
    target_role: str | None
    conditioner_role: str | None
    administrative_role: str | None
    administration: str
    disposition: str
    reasons: tuple[str, ...]

    def material(self) -> dict[str, Any]:
        return {
            "occurrence_id": self.occurrence_id, "target_role": self.target_role,
            "conditioner_role": self.conditioner_role,
            "administrative_role": self.administrative_role,
            "administration": self.administration, "disposition": self.disposition,
            "reasons": list(self.reasons),
        }


@dataclass(frozen=True)
class ScientificFrontier:
    schema: str
    inventory_id: str
    inventory_hash: str
    policy_id: str
    policy_hash: str
    policy_grade: str
    source_identity: Mapping[str, Any]
    operations: tuple[ScientificOperation, ...]
    inventory_ledger: tuple[InventoryLedgerEntry, ...]
    class_counts: Mapping[str, int]
    disposition_counts: Mapping[str, int]
    deferred: tuple[Mapping[str, Any], ...]
    unknown: tuple[Mapping[str, Any], ...]
    excluded: tuple[Mapping[str, Any], ...]
    budget_state: str
    pending_operation_ids: tuple[str, ...]
    partition_size: int
    partition_root: str
    partition_count: int
    maximum_bounds: Mapping[str, int]
    u_item_root: str | None
    u_unit_root: str | None
    u_app_root: str | None
    e_pre_count: int | None
    e_pre_root: str | None
    e_pre_cause: str | None
    original_science_grade: str = "SOURCEFREE_PROPOSAL_NOT_ORIGINAL"

    def eligible(self) -> tuple[ScientificOperation, ...]:
        return tuple(op for op in self.operations if op.disposition == ELIGIBLE)

    def by_id(self, op_id: str) -> ScientificOperation:
        for op in self.operations:
            if op.op_id == op_id:
                return op
        raise KeyError(op_id)

    def disposition_ledger(self) -> tuple[Mapping[str, Any], ...]:
        return tuple(
            {"op_id": op.op_id, "class": op.claim_class,
             "disposition": op.disposition, "reasons": list(op.reasons)}
            for op in self.operations
        )

    @property
    def considered_count(self) -> int:
        return len(self.operations)

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema, "inventory_id": self.inventory_id,
            "inventory_hash": self.inventory_hash, "policy_id": self.policy_id,
            "policy_hash": self.policy_hash, "policy_grade": self.policy_grade,
            "source_identity": dict(self.source_identity),
            "operations": [op.material() for op in self.operations],
            "inventory_ledger": [entry.material() for entry in self.inventory_ledger],
            "class_counts": dict(self.class_counts),
            "disposition_counts": dict(self.disposition_counts),
            "deferred": list(self.deferred), "unknown": list(self.unknown),
            "excluded": list(self.excluded), "budget_state": self.budget_state,
            "pending_operation_ids": list(self.pending_operation_ids),
            "partition_size": self.partition_size,
            "partition_root": self.partition_root,
            "partition_count": self.partition_count,
            "maximum_bounds": dict(self.maximum_bounds),
            "u_item_root": self.u_item_root, "u_unit_root": self.u_unit_root,
            "u_app_root": self.u_app_root, "e_pre_count": self.e_pre_count,
            "e_pre_root": self.e_pre_root, "e_pre_cause": self.e_pre_cause,
            "original_science_grade": self.original_science_grade,
        }

    @property
    def content_hash(self) -> str:
        return content_hash(self.material())


@dataclass(frozen=True)
class FrontierPartition:
    schema: str
    index: int
    partition_size: int
    operation_ids: tuple[str, ...]
    operation_count: int
    root: str

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema, "index": self.index,
            "partition_size": self.partition_size,
            "operation_ids": list(self.operation_ids),
            "operation_count": self.operation_count, "root": self.root,
        }


__all__ = [
    "OCCURRENCE_SCHEMA", "INVENTORY_SCHEMA", "POLICY_SCHEMA", "OPERATION_SCHEMA",
    "FRONTIER_SCHEMA", "PARTITION_SCHEMA", "ADMINISTERED", "NOT_ADMINISTERED",
    "ADMINISTRATION_UNKNOWN", "ADMINISTRATION_STATES", "SCALAR_TOPOLOGY",
    "ELIGIBLE", "PROHIBITED", "INAPPLICABLE_PROVED", "HELD", "UNKNOWN",
    "UNSUPPORTED_RUNTIME", "DEFERRED", "DISPOSITIONS", "CONSIDERED_DISPOSITIONS",
    "OccurrenceKey", "Occurrence", "MeasurePlan", "SourceInventory",
    "DirectionGrant", "GrammarPolicy", "ScientificOperation",
    "InventoryLedgerEntry", "ScientificFrontier", "FrontierPartition",
    "make_operation", "content_hash",
]
