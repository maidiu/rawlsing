"""R50 G50 candidate types: SourceDecisionBundle / ScientificGrammarPolicy / frontier.

Every object is a *candidate1 compatibility proposal*, not adopted source seman-
tics. Nothing here issues source rights, method adoption, original U/E_pre counts
or native execution permission.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import json
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash

BUNDLE_SCHEMA = "SourceDecisionBundle@candidate1"
POLICY_SCHEMA = "ScientificGrammarPolicy@candidate1"
FRONTIER_SCHEMA = "ScientificFrontier@candidate1"
PLAN_SCHEMA = "NativeConstructionPlan@candidate1"

OPERATION_CLASSES = (
    "DIST", "CONDITIONAL", "JOINT", "CO_TRAVEL", "FORK",
    "INTERACTION", "REVERSAL", "STATE_ROBUSTNESS",
)
SEPARATE_CLASSES = ("CROSS_SOURCE", "TEMPORAL", "POSSIBILITY", "STRUCTURAL")
DISPOSITIONS = (
    "ELIGIBLE", "PROHIBITED", "INAPPLICABLE_PROVED", "UNRESOLVED_SCIENCE",
    "UNSUPPORTED_RUNTIME", "DEFERRED", "PARTIAL_PENDING",
)


def _material(value: Any) -> Any:
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
class ItemOccurrence:
    item_id: str
    label: str
    unit: str
    topology: str
    forms: tuple[str, ...]
    domain: tuple[int, ...]
    target_role: bool
    conditioner_role: bool
    route_state: str
    semantic_state: str
    scope: str
    administered: bool = True

    def material(self) -> dict:
        return _material(self.__dict__ if hasattr(self, "__dict__") else {
            name: getattr(self, name) for name in self.__dataclass_fields__
        })


@dataclass(frozen=True)
class MeasurePlan:
    measure_id: str
    kind: str  # SAMPLE | POPULATION
    weight_ref: str | None
    design_ref: str | None
    estimand: str
    variance_policy: str

    def material(self) -> dict:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}


@dataclass(frozen=True)
class SourceDecisionBundle:
    bundle_id: str
    source_id: str
    wave: str
    edition: str
    source_sha256: str
    scope: str
    items: tuple[ItemOccurrence, ...]
    measure_plans: tuple[MeasurePlan, ...]
    risk_set_ref: str
    route_states: tuple[str, ...]
    unit_transforms: tuple[str, ...]
    state_map: Mapping[str, str]
    authority_refs: tuple[str, ...]
    current_selection: str | None
    inventory_complete: bool
    inventory_gaps: tuple[str, ...] = ()
    held: tuple[str, ...] = ()
    unresolved: tuple[str, ...] = ()
    schema: str = BUNDLE_SCHEMA

    def item(self, item_id: str) -> ItemOccurrence:
        for item in self.items:
            if item.item_id == item_id:
                return item
        raise KeyError(item_id)

    def material(self) -> dict:
        return _material({
            "schema": self.schema, "bundle_id": self.bundle_id,
            "source_id": self.source_id, "wave": self.wave, "edition": self.edition,
            "source_sha256": self.source_sha256, "scope": self.scope,
            "items": [i.material() for i in sorted(self.items, key=lambda x: x.item_id)],
            "measure_plans": [m.material() for m in sorted(self.measure_plans, key=lambda x: x.measure_id)],
            "risk_set_ref": self.risk_set_ref, "route_states": self.route_states,
            "unit_transforms": self.unit_transforms, "state_map": dict(self.state_map),
            "authority_refs": self.authority_refs, "current_selection": self.current_selection,
            "inventory_complete": self.inventory_complete,
            "inventory_gaps": self.inventory_gaps, "held": self.held,
            "unresolved": self.unresolved,
        })

    @property
    def content_hash(self) -> str:
        return content_hash(self.material())

    def require_version(self) -> None:
        if self.schema != BUNDLE_SCHEMA:
            raise ValueError(f"INCOMPATIBLE_BUNDLE_SCHEMA:{self.schema}")


@dataclass(frozen=True)
class ScientificGrammarPolicy:
    policy_id: str
    grade: str  # PROPOSED_TEST_ONLY for this build
    allowed_classes: tuple[str, ...]
    separate_classes: tuple[str, ...]
    target_roles: tuple[str, ...]
    conditioner_roles: tuple[str, ...]
    denied_roles: tuple[str, ...]
    bounds: Mapping[str, int]  # J, K, D
    population_requires_weight: bool
    exclusions: tuple[str, ...]
    validation_policy: str
    exploration_policy: str
    stop_policy: str
    owner_refs: tuple[str, ...]
    authority_refs: tuple[str, ...]
    schema: str = POLICY_SCHEMA

    def material(self) -> dict:
        return _material({name: getattr(self, name) for name in self.__dataclass_fields__})

    @property
    def content_hash(self) -> str:
        return content_hash(self.material())

    def require_version(self) -> None:
        if self.schema != POLICY_SCHEMA:
            raise ValueError(f"INCOMPATIBLE_POLICY_SCHEMA:{self.schema}")
        if self.grade not in {"PROPOSED_TEST_ONLY", "COMPETENT_ISSUED"}:
            raise ValueError(f"UNKNOWN_POLICY_GRADE:{self.grade}")


@dataclass(frozen=True)
class ScientificOperation:
    op_id: str
    claim_class: str
    targets: tuple[str, ...]
    conditions: tuple[tuple[str, int], ...]
    condition_mode: str  # AND | XOR_EXACTLY_ONE
    unit: str
    measure: str
    topology: str
    state_variant: str
    scope: str
    branch_depth: int
    source_bundle: str
    policy_id: str
    disposition: str
    reasons: tuple[str, ...] = ()
    native_support: str = "NONE"
    current_permission: str = "NOT_ASSERTED"
    validation_status: str = "EXPLORATORY_NOT_VALIDATED"
    release_status: str = "NOT_RELEASED"
    aliases: tuple[str, ...] = ()

    def identity_material(self) -> dict:
        conditions = [list(pair) for pair in self.conditions]
        if self.condition_mode == "AND":
            # A conjunction is sorted only because AND commutativity is proved by
            # the policy; target order is always retained.
            conditions = sorted(conditions, key=lambda p: (p[0], p[1]))
        return _material({
            "bundle": self.source_bundle, "policy": self.policy_id,
            "class": self.claim_class, "targets": list(self.targets),
            "conditions": conditions, "condition_mode": self.condition_mode,
            "unit": self.unit, "measure": self.measure, "topology": self.topology,
            "state_variant": self.state_variant, "scope": self.scope,
            "branch_depth": self.branch_depth,
        })

    @property
    def canonical_hash(self) -> str:
        return semantic_hash(self.identity_material())

    def canonical_id(self) -> str:
        return "urn:g50:op:" + self.canonical_hash

    def material(self) -> dict:
        return _material({
            "op_id": self.op_id, "candidate_hash": self.canonical_hash,
            "claim_class": self.claim_class, "targets": list(self.targets),
            "conditions": [list(p) for p in self.conditions],
            "condition_mode": self.condition_mode, "unit": self.unit,
            "measure": self.measure, "topology": self.topology,
            "state_variant": self.state_variant, "scope": self.scope,
            "branch_depth": self.branch_depth, "source_bundle": self.source_bundle,
            "policy_id": self.policy_id, "disposition": self.disposition,
            "reasons": list(self.reasons), "native_support": self.native_support,
            "current_permission": self.current_permission,
            "validation_status": self.validation_status,
            "release_status": self.release_status, "aliases": list(self.aliases),
        })


@dataclass(frozen=True)
class ScientificFrontier:
    schema: str
    bundle_id: str
    bundle_hash: str
    policy_id: str
    policy_hash: str
    policy_grade: str
    source_identity: Mapping[str, str]
    u_item_root: str | None
    u_unit_root: str | None
    u_app_root: str | None
    e_pre_count: int | None
    e_pre_root: str | None
    e_pre_cause: str | None
    operations: tuple[ScientificOperation, ...]
    class_counts: Mapping[str, int]
    disposition_counts: Mapping[str, int]
    deferred: tuple[Mapping[str, Any], ...]
    unknown: tuple[Mapping[str, Any], ...]
    excluded: tuple[Mapping[str, Any], ...]
    budget_state: str
    pending_operation_ids: tuple[str, ...]
    maximum_bounds: Mapping[str, int]
    original_science_grade: str = "SOURCEFREE_PROPOSAL_NOT_ORIGINAL"

    def material(self) -> dict:
        return _material({
            "schema": self.schema, "bundle_id": self.bundle_id,
            "bundle_hash": self.bundle_hash, "policy_id": self.policy_id,
            "policy_hash": self.policy_hash, "policy_grade": self.policy_grade,
            "source_identity": dict(self.source_identity),
            "u_item_root": self.u_item_root, "u_unit_root": self.u_unit_root,
            "u_app_root": self.u_app_root, "e_pre_count": self.e_pre_count,
            "e_pre_root": self.e_pre_root, "e_pre_cause": self.e_pre_cause,
            "operations": [op.material() for op in self.operations],
            "class_counts": dict(self.class_counts),
            "disposition_counts": dict(self.disposition_counts),
            "deferred": list(self.deferred), "unknown": list(self.unknown),
            "excluded": list(self.excluded), "budget_state": self.budget_state,
            "pending_operation_ids": list(self.pending_operation_ids),
            "maximum_bounds": dict(self.maximum_bounds),
            "original_science_grade": self.original_science_grade,
        })

    @property
    def content_hash(self) -> str:
        return content_hash(self.material())

    def eligible(self) -> tuple[ScientificOperation, ...]:
        return tuple(op for op in self.operations if op.disposition == "ELIGIBLE")

    def by_id(self, op_id: str) -> ScientificOperation:
        for op in self.operations:
            if op.op_id == op_id:
                return op
        raise KeyError(op_id)


def make_operation(
    *,
    bundle: SourceDecisionBundle,
    policy: ScientificGrammarPolicy,
    claim_class: str,
    targets: Sequence[str],
    conditions: Sequence[tuple[str, int]] = (),
    condition_mode: str = "AND",
    unit: str = "adult",
    measure: str = "SAMPLE",
    topology: str = "SCALAR_SINGULAR",
    state_variant: str = "COMPLETE_RESPONSE",
    scope: str | None = None,
    branch_depth: int = 0,
    disposition: str = "ELIGIBLE",
    reasons: Sequence[str] = (),
    native_support: str = "NONE",
    aliases: Sequence[str] = (),
) -> ScientificOperation:
    op = ScientificOperation(
        op_id="",
        claim_class=claim_class,
        targets=tuple(targets),
        conditions=tuple(conditions),
        condition_mode=condition_mode,
        unit=unit,
        measure=measure,
        topology=topology,
        state_variant=state_variant,
        scope=scope or bundle.scope,
        branch_depth=branch_depth,
        source_bundle=bundle.bundle_id,
        policy_id=policy.policy_id,
        disposition=disposition,
        reasons=tuple(reasons),
        native_support=native_support,
        aliases=tuple(aliases),
    )
    return replace(op, op_id=op.canonical_id())


__all__ = [
    "BUNDLE_SCHEMA", "POLICY_SCHEMA", "FRONTIER_SCHEMA", "PLAN_SCHEMA",
    "OPERATION_CLASSES", "SEPARATE_CLASSES", "DISPOSITIONS",
    "ItemOccurrence", "MeasurePlan", "SourceDecisionBundle",
    "ScientificGrammarPolicy", "ScientificOperation", "ScientificFrontier",
    "make_operation", "content_hash", "canonicalize",
]
