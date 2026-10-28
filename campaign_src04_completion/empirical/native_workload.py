"""Executable native observed-response workload construction for SRC04 Lane C.

The builder consumes an exact accepted C11 release, an explicit
``ObservedResponseContract`` and a declared finite workload policy.  It builds
ordinary ``EmpiricalQuerySpec``/``EmpiricalPredicate`` objects and executes them
through the existing ``execute_empirical_query`` owner.  It is not a new query
engine and it does not inspect original source files.

A pending/unissued contract produces a plan/refusal only.  Execution requires an
authorized contract whose exact authority resolves through the supplied
``AuthorityRegistry``.  No target count, triple cardinality, routing state or
fixture identity is hardcoded into the operation enumerator.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_c11_integrity import RespondentIdentity
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    make_empirical_predicate,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_observed_response import (
    CO_OBSERVED_RESPONSE_RISK_SET,
    OBSERVED_RESPONSE_RISK_SET,
    ObservedResponseContract,
    ObservedResponseTopologyBinding,
    topology_binding_for,
)

NATIVE_WORKLOAD_SCHEMA = "PYAT_SRC04_NATIVE_OBSERVED_RESPONSE_WORKLOAD@2.0.0"
NATIVE_RECEIPT_SCHEMA = "PYAT_SRC04_NATIVE_OBSERVED_RESPONSE_RECEIPT@2.0.0"
FAMILIES = frozenset({
    "UNARY_OBSERVED_DISTRIBUTION",
    "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION",
    "SAME_RESPONDENT_JOINT_DISTRIBUTION",
    "HIGHER_ORDER_CO_OBSERVED_JOINT",
})


class NativeWorkloadRefusal(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


@dataclass(frozen=True)
class WorkloadPolicy:
    policy_id: str
    families: tuple[str, ...]
    max_arity: int
    conditional_value_scope: str = "ALL_OBSERVED_DISTINCT_STATES_VALUES_IN_QUALIFIED_RELEASE"
    execution_requires_authorized_contract: bool = True

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise NativeWorkloadRefusal("POLICY_ID_REQUIRED")
        unknown = set(self.families) - FAMILIES
        if unknown:
            raise NativeWorkloadRefusal("UNKNOWN_OPERATION_FAMILY", repr(sorted(unknown)))
        if self.max_arity < 1 or self.max_arity > 4:
            raise NativeWorkloadRefusal("POLICY_ARITY_OUT_OF_RANGE", str(self.max_arity))
        if self.conditional_value_scope != "ALL_OBSERVED_DISTINCT_STATES_VALUES_IN_QUALIFIED_RELEASE":
            raise NativeWorkloadRefusal("UNSUPPORTED_CONDITIONAL_VALUE_SCOPE", self.conditional_value_scope)

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "WorkloadPolicy":
        return cls(
            policy_id=str(raw.get("policy_id", "")),
            families=tuple(str(x) for x in raw.get("operation_families", ())),
            max_arity=int(raw.get("max_arity", 0)),
            conditional_value_scope=str(raw.get(
                "conditional_value_scope",
                "ALL_OBSERVED_DISTINCT_STATES_VALUES_IN_QUALIFIED_RELEASE",
            )),
            execution_requires_authorized_contract=bool(
                raw.get("execution_requires_authorized_contract", True)),
        )


@dataclass(frozen=True)
class TargetView:
    target_ref: ExactRef
    binding: ObservedResponseTopologyBinding
    domain: tuple[Any, ...]
    conditions: tuple[Mapping[str, Any], ...]
    observed_event_count: int


@dataclass
class NativeOperation:
    operation_id: str
    family: str
    target_refs: tuple[ExactRef, ...]
    condition_ref: ExactRef | None
    condition_state: str | None
    condition_kind: str | None
    condition_value_ref: ExactRef | None
    condition_counts: Mapping[str, int] | None = None
    query: EmpiricalQuerySpec | None = None
    predicate: EmpiricalPredicate | None = None
    status: str = "CONSTRUCTED"
    detail: str = ""
    fact_ref: ExactRef | None = None
    fact_state: str | None = None
    raw_denominator: int | None = None
    raw_numerator: int | None = None
    cells: list[dict[str, Any]] = field(default_factory=list)
    observed_ledger: dict[str, Any] | None = None
    error: str | None = None

    def receipt(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "family": self.family,
            "target_refs": [ref.as_dict() for ref in self.target_refs],
            "condition_ref": self.condition_ref.as_dict() if self.condition_ref else None,
            "condition_kind": self.condition_kind,
            "condition_state": self.condition_state,
            "condition_value_ref": self.condition_value_ref.as_dict() if self.condition_value_ref else None,
            "condition_counts": dict(self.condition_counts) if self.condition_counts is not None else None,
            "query_ref": self.query.ref.as_dict() if self.query is not None else None,
            "status": self.status,
            "detail": self.detail,
            "fact_ref": self.fact_ref.as_dict() if self.fact_ref else None,
            "fact_state": self.fact_state,
            "raw_denominator": self.raw_denominator,
            "raw_numerator": self.raw_numerator,
            "cells": self.cells,
            "observed_ledger": self.observed_ledger,
            "error": self.error,
        }


@dataclass
class NativeWorkload:
    contract_ref: ExactRef
    release_ref: ExactRef | None
    policy: WorkloadPolicy
    targets: tuple[TargetView, ...]
    operations: tuple[NativeOperation, ...]
    accounting: Mapping[str, Any]

    def receipt(self) -> dict[str, Any]:
        return {
            "schema": NATIVE_WORKLOAD_SCHEMA,
            "contract_ref": self.contract_ref.as_dict(),
            "release_ref": self.release_ref.as_dict() if self.release_ref else None,
            "policy": {
                "policy_id": self.policy.policy_id,
                "families": list(self.policy.families),
                "max_arity": self.policy.max_arity,
                "conditional_value_scope": self.policy.conditional_value_scope,
            },
            "targets": [
                {
                    "target_ref": target.target_ref.as_dict(),
                    "observed_event_count": target.observed_event_count,
                    "domain_size": len(target.domain),
                    "condition_count": len(target.conditions),
                }
                for target in self.targets
            ],
            "operations": [operation.receipt() for operation in self.operations],
            "accounting": dict(self.accounting),
        }


def _event_matches(event, target_ref: ExactRef) -> bool:
    native = exact_ref(event.native_question_ref, "native_question_ref")
    canonical = event.canonical_question_ref_if_authorized
    if canonical is not None and exact_ref(canonical, "canonical_question_ref") == target_ref:
        return True
    component = event.component_or_subitem_ref
    if native == target_ref:
        return True
    return component is not None and exact_ref(component, "component_or_subitem_ref") == target_ref


def _event_cell(event) -> Any:
    if event.typed_state == "SUBSTANTIVE_RESPONSE":
        value = event.canonical_response_value_if_authorized
        if value is None:
            value = event.raw_response_value
        return canonicalize(value)
    return canonicalize({"typed_response_state": event.typed_state})


def _state_ref(target_ref: ExactRef, state: str) -> ExactRef:
    digest = semantic_hash({"target_ref": target_ref.as_dict(), "state": state})
    return ExactRef("OBSERVED_RESPONSE_CONDITION_STATE",
                    f"urn:rawlsing:pre553:observed-response:condition-state:{digest}", digest)


def _value_ref(target_ref: ExactRef, value: Any) -> ExactRef:
    digest = semantic_hash({"target_ref": target_ref.as_dict(), "value": canonicalize(value)})
    return ExactRef("OBSERVED_RESPONSE_CONDITION_VALUE",
                    f"urn:rawlsing:pre553:observed-response:condition-value:{digest}", digest)


def _replay_ref(kind: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:observed-response:{kind.lower()}:{digest}", digest)


def _target_views(release: C11LogicalRelease, contract: ObservedResponseContract) -> tuple[TargetView, ...]:
    events = [o for o in release.public_objects if o.schema_id == "RespondentEvent"]
    bindings_by_ref = {binding.target_ref.key: binding for binding in contract.topology_bindings}
    by_target: dict[str, list[Any]] = defaultdict(list)
    for event in events:
        native = exact_ref(event.native_question_ref, "native_question_ref")
        candidate_keys = [native.key]
        canonical = event.canonical_question_ref_if_authorized
        if canonical is not None:
            candidate_keys.append(exact_ref(canonical, "canonical_question_ref").key)
        component = event.component_or_subitem_ref
        if component is not None:
            candidate_keys.append(exact_ref(component, "component_or_subitem_ref").key)
        matched = {key for key in candidate_keys if key in bindings_by_ref}
        if len(matched) > 1:
            raise NativeWorkloadRefusal(
                "EVENT_MATCHES_MULTIPLE_CONTRACT_TARGETS", repr(sorted(matched)))
        for key in matched:
            by_target[key].append(event)
    views: list[TargetView] = []
    for binding in contract.topology_bindings:
        matches = by_target.get(binding.target_ref.key, [])
        observed = [event for event in matches if event.typed_state in contract.observed_states]
        domain: list[Any] = []
        seen_domain: set[str] = set()
        conditions: dict[str, Mapping[str, Any]] = {}
        for event in observed:
            cell = _event_cell(event)
            cell_key = canonical_json(cell)
            if cell_key not in seen_domain:
                seen_domain.add(cell_key)
                domain.append(cell)
            if event.typed_state == "SUBSTANTIVE_RESPONSE":
                value = cell
                condition = {
                    "kind": "VALUE",
                    "operator": "EQ",
                    "exact_value": value,
                    "value_ref": _value_ref(binding.target_ref, value),
                    "state": event.typed_state,
                }
            else:
                condition = {
                    "kind": "STATE",
                    "operator": "STATE_EQ",
                    "typed_state": event.typed_state,
                    "value_ref": _state_ref(binding.target_ref, event.typed_state),
                    "state": event.typed_state,
                }
            conditions[canonical_json({k: v for k, v in condition.items() if k != "value_ref"})] = condition
        domain = tuple(sorted(domain, key=canonical_json))
        views.append(TargetView(
            target_ref=binding.target_ref,
            binding=binding,
            domain=domain,
            conditions=tuple(sorted(conditions.values(), key=lambda item: canonical_json(
                {k: v for k, v in item.items() if k != "value_ref"}))),
            observed_event_count=len(observed),
        ))
    return tuple(views)


def _branch_predicate_ast(contract: ObservedResponseContract, release: C11LogicalRelease) -> dict[str, Any]:
    respondents = sorted(
        (record for record in release.internal_records if isinstance(record, RespondentIdentity)),
        key=lambda record: record.ref.key,
    )
    if not respondents:
        raise NativeWorkloadRefusal("RELEASE_HAS_NO_RESPONDENTS")
    if contract.operation_authority_ref is None:
        raise NativeWorkloadRefusal("CONTRACT_OPERATION_AUTHORITY_REQUIRED")
    return {
        "op": "LEAF",
        "leaf_type": "DERIVED_BRANCH_COHORT",
        "branch_definition_id": "OBSERVED-RESPONSE-RELEASE-SCOPE",
        "resolved_predicate_hash_or_exact_membership_ref": _replay_ref(
            "BRANCH_MEMBERSHIP", {"contract_ref": contract.ref.as_dict(), "scope": "ALL_RELEASE_RESPONDENTS"}).as_dict(),
        "parent_ancestry_ref": _replay_ref(
            "BRANCH_PARENT", {"contract_ref": contract.ref.as_dict()}).as_dict(),
        "branch_algorithm_authority_ref": contract.operation_authority_ref.as_dict(),
        "branch_membership_replay_ref": _replay_ref(
            "BRANCH_REPLAY", {"contract_ref": contract.ref.as_dict(), "respondents": [r.ref.as_dict() for r in respondents]}).as_dict(),
        "branch_source_scope_ref": contract.universe_ref.as_dict() if contract.universe_ref else None,
        "exact_member_respondent_refs": [record.ref.as_dict() for record in respondents],
    }


def _condition_members(
    release: C11LogicalRelease,
    view: TargetView,
    condition: Mapping[str, Any],
    contract: ObservedResponseContract,
    target_ref: ExactRef,
) -> tuple[tuple[ExactRef, ...], Mapping[str, int]]:
    target_events: dict[str, list[Any]] = {}
    condition_events: dict[str, list[Any]] = {}
    for event in release.public_objects:
        if event.schema_id != "RespondentEvent":
            continue
        respondent = exact_ref(event.scoped_respondent_ref, "scoped_respondent_ref")
        if _event_matches(event, target_ref):
            target_events.setdefault(respondent.key, []).append(event)
        if _event_matches(event, view.target_ref):
            condition_events.setdefault(respondent.key, []).append(event)
    respondent_by_key = {
        record.ref.key: record for record in release.internal_records
        if isinstance(record, RespondentIdentity)
    }
    unobserved = 0
    false = 0
    matching_keys: set[str] = set()
    for respondent_key, events in target_events.items():
        if not any(event.typed_state in contract.observed_states for event in events):
            continue
        conditions = [
            event for event in condition_events.get(respondent_key, [])
            if event.typed_state in contract.observed_states
        ]
        if not conditions:
            unobserved += 1
            continue
        matches = False
        for event in conditions:
            if condition["kind"] == "STATE":
                matches = event.typed_state == condition.get("typed_state")
            else:
                matches = _event_cell(event) == canonicalize(condition.get("exact_value"))
            if matches:
                break
        if matches:
            matching_keys.add(respondent_key)
        else:
            false += 1
    member_refs = tuple(sorted(
        (respondent_by_key[key].ref for key in matching_keys if key in respondent_by_key),
        key=lambda ref: ref.key,
    ))
    return member_refs, {
        "condition_unobserved": unobserved,
        "condition_false": false,
        "condition_true": len(member_refs),
    }

def _condition_predicate_ast(
    contract: ObservedResponseContract,
    view: TargetView,
    condition: Mapping[str, Any],
    member_refs: tuple[ExactRef, ...],
    target_ref: ExactRef,
) -> dict[str, Any]:
    if contract.operation_authority_ref is None or contract.universe_ref is None:
        raise NativeWorkloadRefusal("CONTRACT_OPERATION_AUTHORITY_AND_UNIVERSE_REQUIRED")
    material = {
        "contract_ref": contract.ref.as_dict(),
        "target_ref": target_ref.as_dict(),
        "condition_ref": view.target_ref.as_dict(),
        "condition_kind": condition["kind"],
        "condition_state": condition.get("state"),
        "condition_value_ref": condition["value_ref"].as_dict(),
    }
    return {
        "op": "LEAF",
        "leaf_type": "DERIVED_BRANCH_COHORT",
        "branch_definition_id": "OBSERVED-CONDITION-COHORT",
        "resolved_predicate_hash_or_exact_membership_ref": _replay_ref(
            "BRANCH_MEMBERSHIP", material).as_dict(),
        "parent_ancestry_ref": _replay_ref("BRANCH_PARENT", material).as_dict(),
        "branch_algorithm_authority_ref": contract.operation_authority_ref.as_dict(),
        "branch_membership_replay_ref": _replay_ref("BRANCH_REPLAY", material).as_dict(),
        "branch_source_scope_ref": contract.universe_ref.as_dict(),
        "exact_member_respondent_refs": [ref.as_dict() for ref in member_refs],
    }

def _make_predicate(
    contract: ObservedResponseContract,
    release: C11LogicalRelease,
    predicate_ast: Mapping[str, Any],
    *,
    tag: str,
) -> EmpiricalPredicate:
    if contract.operation_authority_ref is None:
        raise NativeWorkloadRefusal("CONTRACT_OPERATION_AUTHORITY_REQUIRED")
    grammar = contract.operation_authority_ref
    return make_empirical_predicate(
        predicate_ast=predicate_ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(grammar,),
        dependency_refs=(contract.ref,),
        producer_replay_locator_or_reference_root=_replay_ref(
            "REPLAY_ROOT", {"contract_ref": contract.ref.as_dict(), "tag": tag}),
        grammar_authority_ref=grammar,
        coordinate_question_value_refs=(),
        risk_set_refs=(contract.risk_set_ref,),
        scope_refs=(contract.universe_ref,) if contract.universe_ref else (),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(
            _replay_ref("OPERATOR_SEMANTICS", {"grammar": "BOOLEAN-AND-OR-NOT-EXACT"}),
        ),
    )


_CONTRACT_PROJECTION_CACHE: dict[str, dict[str, Any]] = {}


def _contract_projection(contract: ObservedResponseContract) -> dict[str, Any]:
    key = contract.ref.key
    cached = _CONTRACT_PROJECTION_CACHE.get(key)
    if cached is None:
        cached = contract.semantic_projection()
        _CONTRACT_PROJECTION_CACHE[key] = cached
    return cached


def _component(view: TargetView, contract: ObservedResponseContract) -> dict[str, Any]:
    if view.binding.topology_authority_ref is None:
        raise NativeWorkloadRefusal("TARGET_TOPOLOGY_AUTHORITY_REQUIRED")
    return {
        "target_ref": view.target_ref.as_dict(),
        "topology": view.binding.i03_topology,
        "domain": list(view.domain),
        "target_domain_replay_ref": _replay_ref(
            "TARGET_DOMAIN", {"target_ref": view.target_ref.as_dict(), "domain": list(view.domain)}).as_dict(),
        "topology_authority_refs": [view.binding.topology_authority_ref.as_dict()],
        "response_semantic_authority_refs": [
            ref.as_dict() for ref in view.binding.response_semantic_authority_refs
        ],
        "included_states": list(contract.observed_states),
    }


def _make_query(
    *,
    contract: ObservedResponseContract,
    views: Sequence[TargetView],
    predicate: EmpiricalPredicate,
    risk_set_type: str,
    tag: str,
    condition_counts: Mapping[str, int] | None = None,
) -> EmpiricalQuerySpec:
    if contract.operation_authority_ref is None:
        raise NativeWorkloadRefusal("CONTRACT_OPERATION_AUTHORITY_REQUIRED")
    if contract.universe_ref is None:
        raise NativeWorkloadRefusal("CONTRACT_UNIVERSE_REQUIRED")
    target_use = {}
    closure_authorities = [contract.operation_authority_ref]
    query_dependencies = [predicate.ref, contract.ref]
    if contract.target_use_authority_ref is not None:
        if contract.target_use_ref is None or contract.target_use_operation is None:
            raise NativeWorkloadRefusal("CONTRACT_TARGET_USE_INCOMPLETE")
        target_use = {
            "target_use_ref": contract.target_use_ref.as_dict(),
            "target_use_authority_ref": contract.target_use_authority_ref.as_dict(),
            "target_use_operation": contract.target_use_operation,
        }
        closure_authorities.append(contract.target_use_authority_ref)
        query_dependencies.append(contract.target_use_ref)
    query = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=tuple(dict.fromkeys(closure_authorities)),
        dependency_refs=tuple(query_dependencies),
        producer_replay_locator_or_reference_root=_replay_ref(
            "REPLAY_ROOT", {"contract_ref": contract.ref.as_dict(), "tag": tag}),
        target_refs=tuple(view.target_ref for view in views),
        target_arity_and_topology={
            "arity": len(views),
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": [_component(view, contract) for view in views],
        },
        condition_predicate_ref=predicate.ref,
        risk_set_ref=contract.risk_set_ref,
        empirical_universe_refs=(contract.universe_ref,),
        scope_refs=(contract.universe_ref,),
        measure_basis_ref=_replay_ref("MEASURE_BASIS", {"measure": "RAW"}),
        requested_output_grain={
            "source_scope_mode": "SINGLE_UNIVERSE",
            "measure_kind": "RAW",
            "risk_set_type": risk_set_type,
            "response_state_semantics_ref": _replay_ref(
                "OBSERVED_RESPONSE_STATE_SEMANTICS",
                {"observed_states": list(contract.observed_states),
                 "missing_states": list(contract.missing_states)},
            ).as_dict(),
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
            "query_operation": contract.operation,
            "observed_response_contract_ref": contract.ref.as_dict(),
            "observed_response_contract": _contract_projection(contract),
            "observed_response_condition_counts": dict(condition_counts) if condition_counts is not None else None,
            **target_use,
        },
        query_authority_refs=(contract.operation_authority_ref,),
    )
    return query


def _operation_id(family: str, target_refs: Iterable[ExactRef], condition: Mapping[str, Any] | None) -> str:
    material = {
        "family": family,
        "target_refs": [ref.as_dict() for ref in target_refs],
        "condition": (
            {k: v for k, v in condition.items() if k not in {"exact_value"}}
            if condition is not None else None
        ),
    }
    return semantic_hash(material)


def build_native_workload(
    *,
    repository: C11Repository,
    release_ref: ExactRef,
    contract: ObservedResponseContract,
    policy: WorkloadPolicy,
) -> NativeWorkload:
    """Build the exact finite operation set for one release and contract.

    No query is executed here.  A pending/unissued contract is represented as
    blocked operations rather than silently executed.
    """
    if not isinstance(repository, C11Repository):
        raise NativeWorkloadRefusal("C11_REPOSITORY_REQUIRED")
    release = repository.resolve_release_exact(exact_ref(release_ref, "release_ref"))
    if contract.release_ref is not None and contract.release_ref != release.release_ref:
        raise NativeWorkloadRefusal("CONTRACT_RELEASE_MISMATCH")
    if contract.source_artifact_ref != release.source_artifact_ref:
        raise NativeWorkloadRefusal("CONTRACT_SOURCE_ARTIFACT_MISMATCH")
    if contract.source_release_manifest_hash is not None and \
            contract.source_release_manifest_hash != release.source_release_manifest_hash:
        raise NativeWorkloadRefusal("CONTRACT_SOURCE_MANIFEST_MISMATCH")
    views = _target_views(release, contract)
    by_ref = {view.target_ref.key: view for view in views}
    selected = tuple(view for view in views if view.observed_event_count > 0)
    operations: list[NativeOperation] = []
    authorized = contract.contract_state == "AUTHORIZED" and contract.operation_authority_ref is not None
    shared_scope_predicate = None
    if authorized and (("UNARY_OBSERVED_DISTRIBUTION" in policy.families) or
                       ("SAME_RESPONDENT_JOINT_DISTRIBUTION" in policy.families)):
        shared_scope_predicate = _make_predicate(
            contract, release, _branch_predicate_ast(contract, release), tag="release-scope")

    if "UNARY_OBSERVED_DISTRIBUTION" in policy.families:
        for view in selected:
            operation_id = _operation_id("UNARY_OBSERVED_DISTRIBUTION", (view.target_ref,), None)
            operation = NativeOperation(
                operation_id=operation_id,
                family="UNARY_OBSERVED_DISTRIBUTION",
                target_refs=(view.target_ref,),
                condition_ref=None,
                condition_state=None,
                condition_kind=None,
                condition_value_ref=None,
                status="CONSTRUCTED" if authorized else "BLOCKED_CONTRACT_NOT_AUTHORIZED",
            )
            if authorized:
                predicate = shared_scope_predicate
                operation.predicate = predicate
                operation.query = _make_query(
                    contract=contract, views=(view,), predicate=predicate,
                    risk_set_type=OBSERVED_RESPONSE_RISK_SET, tag=f"unary:{operation_id}")
            operations.append(operation)

    if "SAME_RESPONDENT_JOINT_DISTRIBUTION" in policy.families and policy.max_arity >= 2:
        for i, left in enumerate(selected):
            for right in selected[i + 1:]:
                operation_id = _operation_id(
                    "SAME_RESPONDENT_JOINT_DISTRIBUTION", (left.target_ref, right.target_ref), None)
                operation = NativeOperation(
                    operation_id=operation_id,
                    family="SAME_RESPONDENT_JOINT_DISTRIBUTION",
                    target_refs=(left.target_ref, right.target_ref),
                    condition_ref=None,
                    condition_state=None,
                    condition_kind=None,
                    condition_value_ref=None,
                    status="CONSTRUCTED" if authorized else "BLOCKED_CONTRACT_NOT_AUTHORIZED",
                )
                if authorized:
                    predicate = shared_scope_predicate
                    operation.predicate = predicate
                    operation.query = _make_query(
                        contract=contract, views=(left, right), predicate=predicate,
                        risk_set_type=CO_OBSERVED_RESPONSE_RISK_SET, tag=f"joint:{operation_id}")
                operations.append(operation)

    if "HIGHER_ORDER_CO_OBSERVED_JOINT" in policy.families and policy.max_arity >= 3:
        from itertools import combinations
        for arity in range(3, min(policy.max_arity, len(selected)) + 1):
            for group in combinations(selected, arity):
                operation_id = _operation_id(
                    "HIGHER_ORDER_CO_OBSERVED_JOINT", tuple(v.target_ref for v in group), None)
                operations.append(NativeOperation(
                    operation_id=operation_id,
                    family="HIGHER_ORDER_CO_OBSERVED_JOINT",
                    target_refs=tuple(v.target_ref for v in group),
                    condition_ref=None,
                    condition_state=None,
                    condition_kind=None,
                    condition_value_ref=None,
                    status="BLOCKED_HIGHER_ORDER_FAMILY_NOT_AUTHORIZED" if not authorized else "CONSTRUCTED",
                ))

    if "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION" in policy.families:
        for target in selected:
            for condition_target in selected:
                if condition_target.target_ref == target.target_ref:
                    continue
                for condition in condition_target.conditions:
                    member_refs, condition_counts = _condition_members(
                        release, condition_target, condition, contract, target.target_ref)
                    operation_id = _operation_id(
                        "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION",
                        (target.target_ref,),
                        condition,
                    )
                    operation = NativeOperation(
                        operation_id=operation_id,
                        family="BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION",
                        target_refs=(target.target_ref,),
                        condition_ref=condition_target.target_ref,
                        condition_state=condition.get("state"),
                        condition_kind=condition.get("kind"),
                        condition_value_ref=condition.get("value_ref"),
                        condition_counts=condition_counts,
                        status="CONSTRUCTED" if authorized else "BLOCKED_CONTRACT_NOT_AUTHORIZED",
                    )
                    if authorized:
                        ast = _condition_predicate_ast(
                            contract, condition_target, condition, member_refs, target.target_ref)
                        predicate = _make_predicate(contract, release, ast, tag=f"conditional:{operation_id}")
                        operation.predicate = predicate
                        operation.query = _make_query(
                            contract=contract, views=(target,), predicate=predicate,
                            risk_set_type=OBSERVED_RESPONSE_RISK_SET,
                            tag=f"conditional:{operation_id}",
                            condition_counts=condition_counts)
                    operations.append(operation)

    counts = Counter(operation.status for operation in operations)
    family_counts = Counter(operation.family for operation in operations)
    held = len(contract.target_refs) - len(selected)
    accounting = {
        "selected_observed_targets": len(selected),
        "contract_target_refs": len(contract.target_refs),
        "held_or_unobserved_targets": held,
        "operations_total": len(operations),
        "operations_by_family": dict(sorted(family_counts.items())),
        "operations_by_status": dict(sorted(counts.items())),
        "requested_higher_order_not_authorized": (
            _comb(len(selected), 3) if policy.max_arity < 3 else 0
        ),
        "routing_conditions_used": 0,
        "routing_state": "ROUTING_UNKNOWN",
        "conditional_values": "EXACT_OBSERVED_DISTINCT_STATES_VALUES_ONLY",
        "held_residuals_are_not_zero": held > 0,
        "fixture_scope": release.release_id.startswith("R157_FIXTURE_RELEASE"),
    }
    return NativeWorkload(
        contract_ref=contract.ref,
        release_ref=release.release_ref,
        policy=policy,
        targets=views,
        operations=tuple(operations),
        accounting=accounting,
    )


def _comb(n: int, k: int) -> int:
    if n < k:
        return 0
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result


def execute_native_workload(
    *,
    repository: C11Repository,
    release_ref: ExactRef,
    contract: ObservedResponseContract,
    authority_registry: AuthorityRegistry,
    policy: WorkloadPolicy,
    start_after_operation_id: str | None = None,
) -> NativeWorkload:
    """Execute constructed operations through the existing I03 owner.

    The caller supplies the exact authority registry.  Pending/unissued contracts
    refuse execution before any query is issued.
    """
    if contract.contract_state != "AUTHORIZED" or contract.operation_authority_ref is None:
        raise NativeWorkloadRefusal("CONTRACT_NOT_AUTHORIZED_FOR_EXECUTION")
    workload = build_native_workload(
        repository=repository, release_ref=release_ref, contract=contract, policy=policy)
    started = start_after_operation_id is None
    for operation in workload.operations:
        if not started:
            if operation.operation_id == start_after_operation_id:
                started = True
                continue
            continue
        if operation.query is None or operation.predicate is None:
            operation.status = "BLOCKED_QUERY_NOT_CONSTRUCTED"
            continue
        try:
            result = execute_empirical_query(
                repository=repository,
                query=operation.query,
                predicate=operation.predicate,
                authority_registry=authority_registry,
                release_refs=(release_ref,),
            )
            fact = result.facts[0]
            operation.fact_ref = fact.ref
            operation.fact_state = fact.typed_state
            operation.raw_denominator = fact.raw_denominator_support
            operation.raw_numerator = fact.raw_numerator_support
            operation.cells = [
                {
                    "cell": row["cell"],
                    "raw_numerator_support": row["raw_numerator_support"],
                    "cell_state": row["cell_state"],
                }
                for row in fact.target_topology.get("complete_cell_semantic_projection", ())
            ]
            operation.observed_ledger = dict(
                fact.target_topology.get("observed_response", {}).get("ledger", {})
            ) or None
            operation.status = "EXECUTED"
            operation.detail = fact.execution_detail
        except Exception as exc:  # keep exact per-operation refusal, never fabricate success
            operation.status = "REFUSED"
            operation.error = f"{type(exc).__name__}: {exc}"
    counts = Counter(operation.status for operation in workload.operations)
    # frozen dataclass not used here; accounting is a mutable mapping on the workload
    workload.accounting = {
        **dict(workload.accounting),
        "operations_by_status": dict(sorted(counts.items())),
        "executed_operations": counts["EXECUTED"],
        "refused_operations": counts["REFUSED"],
        "blocked_operations": sum(v for k, v in counts.items() if k.startswith("BLOCKED")),
        "receipt_scope": "EXACT_OPERATION_FACTS_ONLY_NO_RESPONDENT_ROWS",
        "resume_after_operation_id": start_after_operation_id,
    }
    return workload


def plan_from_scope(
    *,
    scope: Mapping[str, Any],
    contract: ObservedResponseContract,
    policy: WorkloadPolicy,
) -> dict[str, Any]:
    """Construct a release-independent finite plan from the exact scope ledger."""
    available = tuple(str(x) for x in scope.get("available_field_ids", ()))
    held = tuple(str(x) for x in scope.get("held_field_ids", ()))
    if len(available) != len(contract.target_refs):
        raise NativeWorkloadRefusal(
            "SCOPE_CONTRACT_TARGET_COUNT_MISMATCH",
            f"scope={len(available)} contract={len(contract.target_refs)}",
        )
    scope_target_refs = tuple(sorted(
        (exact_ref(item, "scope.native_target_refs") for item in scope.get("native_target_refs", ())),
        key=lambda ref: ref.key,
    ))
    if scope_target_refs != contract.target_refs:
        raise NativeWorkloadRefusal("SCOPE_CONTRACT_TARGET_IDENTITY_MISMATCH")
    n = len(available)
    unary = n if "UNARY_OBSERVED_DISTRIBUTION" in policy.families else 0
    joint = _comb(n, 2) if "SAME_RESPONDENT_JOINT_DISTRIBUTION" in policy.families and policy.max_arity >= 2 else 0
    triple = _comb(n, 3) if policy.max_arity < 3 else 0
    conditional_target_pairs = n * (n - 1)
    conditional = {
        "planned_operations": 0,
        "target_ordered_pairs": conditional_target_pairs,
        "status": "DEFERRED_REQUIRES_QUALIFIED_RELEASE_DISTINCT_OBSERVED_VALUES",
        "reason": "conditional operation instances require exact distinct observed condition values/states from the qualified release; no release-free value crossproduct is fabricated",
    }
    return {
        "schema": "PYAT_SRC04_NATIVE_OBSERVED_RESPONSE_PLAN@2.0.0",
        "policy": {
            "policy_id": policy.policy_id,
            "families": list(policy.families),
            "max_arity": policy.max_arity,
        },
        "scope": {
            "available_response_fields": n,
            "held_response_fields": len(held),
            "available_analytical_coordinates": 0,
            "identity_only_coordinates": 1,
            "held_coordinate_roles": 2,
        },
        "operations": {
            "unary_operations": unary,
            "joint_pair_operations": joint,
            "conditional_operations": conditional,
            "higher_order_requested_not_authorized": triple,
            "constructible_without_release": unary + joint,
            "conditional_target_pairs_awaiting_release_values": conditional_target_pairs,
            "constructible_with_qualified_release": "UNARY_AND_JOINT_NOW_PLUS_EXACT_CONDITIONAL_VALUES_FROM_RELEASE",
        },
        "execution": {
            "issued": 0,
            "executed": 0,
            "status": "PLAN_ONLY_ORIGINAL_CONTRACT_PENDING",
        },
        "residuals": scope.get("field_ledger", []),
        "coordinate_roles": scope.get("coordinate_ledger", []),
    }


__all__ = [
    "NATIVE_WORKLOAD_SCHEMA",
    "NATIVE_RECEIPT_SCHEMA",
    "FAMILIES",
    "NativeWorkloadRefusal",
    "WorkloadPolicy",
    "TargetView",
    "NativeOperation",
    "NativeWorkload",
    "build_native_workload",
    "execute_native_workload",
    "plan_from_scope",
]
