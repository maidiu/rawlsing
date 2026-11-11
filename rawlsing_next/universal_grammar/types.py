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

NOT_STARTED = "NOT_STARTED"
PENDING = "PENDING"
COMPLETED = "COMPLETED"
ERROR = "ERROR"

SUPPORTED_RESULT = "SUPPORTED"
OBSERVED_ZERO = "OBSERVED_ZERO"
VALID_NULL = "VALID_NULL"
DIFFUSE = "DIFFUSE"
VALID_EMPTY = "VALID_EMPTY"
ZERO_SUPPORT = "ZERO_SUPPORT"
UNSUPPORTED_RESULT = "UNSUPPORTED"

ELIGIBILITY_STATES = (
    ELIGIBLE, PROHIBITED, INAPPLICABLE_PROVED, HELD, UNKNOWN,
)
EXECUTION_STATES = (
    NOT_STARTED, PENDING, COMPLETED, UNSUPPORTED_RUNTIME, ERROR,
)
RESULT_STATES = (
    SUPPORTED_RESULT, OBSERVED_ZERO, VALID_NULL, DIFFUSE,
    VALID_EMPTY, ZERO_SUPPORT, UNSUPPORTED_RESULT, UNKNOWN,
)
# Backward-compatible name: disposition is the eligibility axis only.
DISPOSITIONS = ELIGIBILITY_STATES
CONSIDERED_DISPOSITIONS = ELIGIBILITY_STATES


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


@dataclass(frozen=True)
class AbsentValue:
    """Explicit typed absence, distinct from an explicit null value."""

    def as_dict(self) -> dict[str, str]:
        return {"$typed_value": "ABSENT"}

    def material(self) -> dict[str, str]:
        return self.as_dict()


ABSENT = AbsentValue()


def _validate_typed_value(value: Any) -> None:
    if value is None or isinstance(value, (bool, int, str, AbsentValue)):
        return
    raise ValueError("domain values must be typed bool/int/string/null/absent, not float or opaque")


def value_material(value: Any) -> Any:
    return _material(value)


def typed_value_key(value: Any) -> str:
    return json.dumps(_material(value), sort_keys=True, separators=(",", ":"))


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
            _validate_typed_value(value)
        if len({typed_value_key(v) for v in self.domain}) != len(self.domain):
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
class HeldRecord:
    occurrence_id: str
    reason: str
    authority_ref: str | None = None
    structured: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "occurrence_id", _text(self.occurrence_id, "occurrence_id"))
        object.__setattr__(self, "reason", _text(self.reason, "reason"))
        if self.authority_ref is not None:
            object.__setattr__(self, "authority_ref", _text(self.authority_ref, "authority_ref"))
        if not isinstance(self.structured, bool):
            raise TypeError("structured must be bool")

    def material(self) -> dict[str, Any]:
        return {
            "occurrence_id": self.occurrence_id, "reason": self.reason,
            "authority_ref": self.authority_ref, "structured": self.structured,
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
    held: tuple[Any, ...] = ()
    unresolved: tuple[str, ...] = ()
    dataset_id: str | None = None
    instrument_ref: str | None = None
    observation_clock_ref: str | None = None
    reference_clock_ref: str | None = None
    as_of_ref: str | None = None
    publication_clock_ref: str | None = None
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
        held_records: list[HeldRecord] = []
        for value in self.held:
            if isinstance(value, HeldRecord):
                held_records.append(value)
            elif isinstance(value, str):
                held_records.append(HeldRecord(
                    occurrence_id=_text(value, "held entry"),
                    reason="UNSTRUCTURED_FREE_TEXT_HELD_CLAIM",
                    authority_ref=None, structured=False,
                ))
            else:
                raise TypeError("held entries must be HeldRecord or legacy string")
        object.__setattr__(self, "held", tuple(held_records))
        object.__setattr__(self, "unresolved", _texts(self.unresolved, "unresolved"))
        if self.current_selection is not None:
            object.__setattr__(self, "current_selection", _text(self.current_selection, "current_selection"))
        for name in ("dataset_id", "instrument_ref", "observation_clock_ref",
                     "reference_clock_ref", "as_of_ref", "publication_clock_ref"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _text(value, name))
        if not isinstance(self.inventory_complete, bool):
            raise TypeError("inventory_complete must be bool")
        if not self.inventory_complete and not self.inventory_gaps:
            raise ValueError("incomplete inventory must state its exact gaps")

    def by_key(self) -> dict[OccurrenceKey, Occurrence]:
        return {occurrence.key: occurrence for occurrence in self.occurrences}

    @property
    def held_records(self) -> tuple[HeldRecord, ...]:
        return tuple(record for record in self.held if isinstance(record, HeldRecord))

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
            "inventory_gaps": list(self.inventory_gaps),
            "held": [record.material() for record in self.held],
            "unresolved": list(self.unresolved),
            "dataset_id": self.dataset_id, "instrument_ref": self.instrument_ref,
            "observation_clock_ref": self.observation_clock_ref,
            "reference_clock_ref": self.reference_clock_ref,
            "as_of_ref": self.as_of_ref,
            "publication_clock_ref": self.publication_clock_ref,
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
    recursion_relation_ref: str | None = None
    baseline_policy_ref: str | None = None
    risk_set_policy: str = "UNKNOWN"
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
        if self.risk_set_policy not in {"UNKNOWN", "UNCONSTRAINED"}:
            raise ValueError(f"UNKNOWN_RISK_SET_POLICY:{self.risk_set_policy}")
        for name in ("recursion_relation_ref", "baseline_policy_ref"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _text(value, name))
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
            "recursion_relation_ref": self.recursion_relation_ref,
            "baseline_policy_ref": self.baseline_policy_ref,
            "risk_set_policy": self.risk_set_policy,
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
    recursion_depth: int
    baseline_ref: str | None
    recursion_relation_ref: str | None
    baseline_policy_ref: str | None
    source_inventory: str
    source_id: str
    dataset_id: str | None
    wave: str
    edition: str
    source_sha256: str
    instrument_ref: str | None
    policy_id: str
    policy_hash: str
    policy_grade: str
    estimand: str
    weight_ref: str | None
    design_ref: str | None
    variance_policy: str
    observation_clock_ref: str | None
    reference_clock_ref: str | None
    as_of_ref: str | None
    publication_clock_ref: str | None
    current_selection_ref: str | None
    disposition: str
    reasons: tuple[str, ...] = ()
    native_support: str = "UNMAPPED"
    administration_states: tuple[str, ...] = ()
    execution_state: str = NOT_STARTED
    result_state: str = UNKNOWN
    aliases: tuple[str, ...] = ()
    schema: str = OPERATION_SCHEMA

    def __post_init__(self) -> None:
        if self.schema != OPERATION_SCHEMA:
            raise ValueError(f"INCOMPATIBLE_OPERATION_SCHEMA:{self.schema}")
        if not isinstance(self.targets, tuple) or not self.targets:
            raise ValueError("operation must have at least one target occurrence")
        if not isinstance(self.conditions, tuple):
            raise ValueError("conditions must be a tuple")
        if self.disposition not in ELIGIBILITY_STATES:
            raise ValueError(f"UNKNOWN_ELIGIBILITY_STATE:{self.disposition}")
        if self.execution_state not in EXECUTION_STATES:
            raise ValueError(f"UNKNOWN_EXECUTION_STATE:{self.execution_state}")
        if self.result_state not in RESULT_STATES:
            raise ValueError(f"UNKNOWN_RESULT_STATE:{self.result_state}")
        if self.branch_depth < 0 or self.recursion_depth < 0:
            raise ValueError("branch/recursion depth must be nonnegative")

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
            "recursion_depth": self.recursion_depth,
            "baseline_ref": self.baseline_ref,
            "recursion_relation_ref": self.recursion_relation_ref,
            "baseline_policy_ref": self.baseline_policy_ref,
            "source_inventory": self.source_inventory, "source_id": self.source_id,
            "dataset_id": self.dataset_id, "wave": self.wave,
            "edition": self.edition, "source_sha256": self.source_sha256,
            "instrument_ref": self.instrument_ref,
            "policy_id": self.policy_id, "policy_hash": self.policy_hash,
            "policy_grade": self.policy_grade,
            "estimand": self.estimand, "weight_ref": self.weight_ref,
            "design_ref": self.design_ref, "variance_policy": self.variance_policy,
            "observation_clock_ref": self.observation_clock_ref,
            "reference_clock_ref": self.reference_clock_ref,
            "as_of_ref": self.as_of_ref,
            "publication_clock_ref": self.publication_clock_ref,
            "current_selection_ref": self.current_selection_ref,
            "administration_states": list(self.administration_states),
        }

    @property
    def canonical_hash(self) -> str:
        return semantic_hash(self.identity_material())

    def material(self) -> dict[str, Any]:
        return {
            **self.identity_material(), "op_id": self.op_id,
            "candidate_hash": self.canonical_hash, "disposition": self.disposition,
            "execution_state": self.execution_state, "result_state": self.result_state,
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
    recursion_depth: int = 0,
    baseline_ref: str | None = None,
    disposition: str = ELIGIBLE,
    reasons: Sequence[str] = (),
    native_support: str = "UNMAPPED",
    administration_states: Sequence[str] = (),
    execution_state: str = NOT_STARTED,
    result_state: str = UNKNOWN,
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
        recursion_depth=recursion_depth,
        baseline_ref=baseline_ref,
        recursion_relation_ref=policy.recursion_relation_ref,
        baseline_policy_ref=policy.baseline_policy_ref,
        source_inventory=inventory.inventory_id,
        source_id=inventory.source_id,
        dataset_id=inventory.dataset_id,
        wave=inventory.wave,
        edition=inventory.edition,
        source_sha256=inventory.source_sha256,
        instrument_ref=inventory.instrument_ref,
        policy_id=policy.policy_id,
        policy_hash=policy.content_hash,
        policy_grade=policy.grade,
        estimand=measure.estimand,
        weight_ref=measure.weight_ref,
        design_ref=measure.design_ref,
        variance_policy=measure.variance_policy,
        observation_clock_ref=inventory.observation_clock_ref,
        reference_clock_ref=inventory.reference_clock_ref,
        as_of_ref=inventory.as_of_ref,
        publication_clock_ref=inventory.publication_clock_ref,
        current_selection_ref=inventory.current_selection,
        disposition=disposition,
        reasons=tuple(reasons),
        native_support=native_support,
        administration_states=tuple(administration_states),
        execution_state=execution_state,
        result_state=result_state,
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
    held_reason: str | None = None
    held_authority_ref: str | None = None

    def material(self) -> dict[str, Any]:
        return {
            "occurrence_id": self.occurrence_id, "target_role": self.target_role,
            "conditioner_role": self.conditioner_role,
            "administrative_role": self.administrative_role,
            "administration": self.administration, "disposition": self.disposition,
            "reasons": list(self.reasons), "held_reason": self.held_reason,
            "held_authority_ref": self.held_authority_ref,
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
    execution_counts: Mapping[str, int]
    result_counts: Mapping[str, int]
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
             "eligibility": op.disposition,
             "execution": op.execution_state, "result": op.result_state,
             "reasons": list(op.reasons)}
            for op in self.operations
        )

    @property
    def eligibility_counts(self) -> Mapping[str, int]:
        return dict(self.disposition_counts)

    @property
    def considered_count(self) -> int:
        return len(self.operations)

    def axis_conservation(self) -> dict[str, Any]:
        considered = sum(self.disposition_counts.values())
        eligible_ops = self.eligible()
        execution_total = sum(self.execution_counts.values())
        result_total = sum(self.result_counts.values())
        return {
            "considered_count": len(self.operations),
            "eligibility_total": considered,
            "eligible_count": len(eligible_ops),
            "execution_total": execution_total,
            "eligible_execution_total": sum(
                1 for op in eligible_ops
            ),
            "result_total": result_total,
            "considered_equals_eligibility": considered == len(self.operations),
            "execution_equals_considered": execution_total == len(self.operations),
            "result_equals_considered": result_total == len(self.operations),
            "eligibility_partition_ok": set(self.disposition_counts) <= set(ELIGIBILITY_STATES),
            "execution_partition_ok": set(self.execution_counts) <= set(EXECUTION_STATES),
            "result_partition_ok": set(self.result_counts) <= set(RESULT_STATES),
        }

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
            "execution_counts": dict(self.execution_counts),
            "result_counts": dict(self.result_counts),
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
    "UNSUPPORTED_RUNTIME", "DEFERRED", "NOT_STARTED", "PENDING", "COMPLETED",
    "ERROR", "SUPPORTED_RESULT", "OBSERVED_ZERO", "VALID_NULL", "DIFFUSE",
    "VALID_EMPTY", "ZERO_SUPPORT", "UNSUPPORTED_RESULT",
    "ELIGIBILITY_STATES", "EXECUTION_STATES", "RESULT_STATES",
    "DISPOSITIONS", "CONSIDERED_DISPOSITIONS",
    "AbsentValue", "ABSENT", "value_material", "typed_value_key", "HeldRecord",
    "OccurrenceKey", "Occurrence", "MeasurePlan", "SourceInventory",
    "DirectionGrant", "GrammarPolicy", "ScientificOperation",
    "InventoryLedgerEntry", "ScientificFrontier", "FrontierPartition",
    "make_operation", "content_hash",
]
