"""Exact governed empirical query execution over sealed PRE553 C11 releases.

I03 is deliberately narrow.  It consumes the accepted I01 public semantic
objects and the accepted I02 sealed C11 repository.  It does not perform
search/discovery, source composition inference, structural admission, V553
work, generated-position mapping, or actor/V3/V2 behavior.

The executor is fail-closed: every source, predicate, risk set, target,
topology, measure, authority and replay input is exact and identity-bearing.
No latest/default/fuzzy/nearest lookup or marginal-product reconstruction is
implemented.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_c11_integrity import (
    C11InternalRecord,
    RespondentIdentity,
    ReplayManifest,
)
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, C11Repository
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    CanonicalSemanticObject,
    DIAGNOSTIC_ONLY_KINDS,
    EmpiricalCoordinateFact,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    RespondentEvent,
    RoutingEligibilityFact,
    SourceUniverseRelation,
    WeightMeasureFact,
    authority_ref,
    canonical_json,
    canonical_set,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_observed_response import (
    CO_OBSERVED_RESPONSE_RISK_SET,
    OBSERVED_RESPONSE_RISK_SET,
    OBSERVED_RESPONSE_RISK_SET_TYPES,
)

QUERY_EXECUTION_CONTRACT_ID = "PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0"

SOURCE_SCOPE_MODES = frozenset({
    "SINGLE_UNIVERSE",
    "SOURCE_INDEXED_MULTI_UNIVERSE",
    "AUTHORIZED_COMPOSITE",
})
MEASURE_KINDS = frozenset({"RAW", "GOVERNED_WEIGHTED"})
RISK_SET_TYPES = frozenset({
    "WHOLE_QUESTION_RISK_SET",
    "COMMON_ELIGIBLE_RISK_SET",
    "ROUTED_APPLICABLE_RISK_SET",
    "ANCHOR_SELECTED_RISK_SET",
    "CANDIDATE_QUESTION_RISK_SET",
    "BRANCH_COHORT_RISK_SET",
    "CUSTOM_GOVERNED_RISK_SET",
    OBSERVED_RESPONSE_RISK_SET,
    CO_OBSERVED_RESPONSE_RISK_SET,
})
TARGET_TOPOLOGIES = frozenset({
    "SCALAR_SINGULAR",
    "UNORDERED_MULTISELECT",
    "UNORDERED_MULTISELECT_SET",
    "MULTISELECT",
    "ORDERED_SEQUENCE",
    "REPEATED_EVENT",
    "REPEATED_MEASUREMENT",
    "RANKED_RESPONSE",
    "ROUTED_RESPONSE",
    "COMPONENTIZED_RESPONSE",
})
JOINT_ORDER_SEMANTICS = frozenset({"SEMANTIC_ORDERED", "CANONICAL_SET_ORDER"})
ELIGIBLE_ROUTING_STATES = frozenset({"ELIGIBLE_APPLICABLE"})
EXPLICIT_NONMEMBER_ROUTING_STATES = frozenset({"NOT_ASKED", "INAPPLICABLE", "NOT_ELIGIBLE"})
UNRESOLVED_ROUTING_STATES = frozenset({"ROUTING_UNKNOWN", "RULE_UNAVAILABLE"})


class EmpiricalQueryExecutionError(Pre553IntegrityError):
    """The exact query cannot be lawfully executed as supplied."""


class EmpiricalQueryResolutionError(EmpiricalQueryExecutionError):
    """One exact source/predicate/risk/target input cannot be resolved."""


class UnsupportedResponseTopology(EmpiricalQueryExecutionError):
    """The query asks I03 to collapse topology it cannot represent exactly."""


@dataclass(frozen=True)
class QueryExecutionResult:
    """Nonsemantic execution envelope; canonical truth lives in ``facts``."""

    query_ref: ExactRef
    facts: tuple[EmpiricalFact, ...]
    source_scope_mode: str
    release_refs: tuple[ExactRef, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.query_ref, ExactRef):
            raise EmpiricalQueryExecutionError("query_ref must be exact")
        if self.source_scope_mode not in SOURCE_SCOPE_MODES:
            raise EmpiricalQueryExecutionError("unknown source_scope_mode")
        if tuple(sorted(self.release_refs, key=lambda r: r.key)) != self.release_refs:
            raise EmpiricalQueryExecutionError("release_refs must be canonical exact-ref sorted")
        if tuple(sorted(self.facts, key=lambda f: f.ref.key)) != self.facts:
            raise EmpiricalQueryExecutionError("facts must be canonical exact-ref sorted")


@dataclass(frozen=True)
class _ExecutionProfile:
    source_scope_mode: str
    measure_kind: str
    risk_set_type: str
    response_state_semantics_ref: ExactRef
    weight_basis_id: str | None
    uncertainty_method_or_typed_state: Any
    observed_response_contract_ref: ExactRef | None = None
    observed_response_contract: Mapping[str, Any] | None = None
    observed_response_condition_counts: Mapping[str, int] | None = None


@dataclass(frozen=True)
class _TargetComponent:
    target_ref: ExactRef
    topology: str
    domain: tuple[Any, ...]
    target_domain_replay_ref: ExactRef
    topology_authority_refs: tuple[AuthorityRef, ...]
    response_semantic_authority_refs: tuple[AuthorityRef, ...]
    included_states: frozenset[str]


@dataclass(frozen=True)
class _TargetPlan:
    components: tuple[_TargetComponent, ...]
    joint_order_semantics: str
    full_domain: tuple[Any, ...]
    domain_identity: str

    @property
    def arity(self) -> int:
        return len(self.components)


@dataclass
class _ReleaseIndex:
    release: C11LogicalRelease
    universe: EmpiricalUniverse
    respondents: dict[str, RespondentIdentity]
    events_by_respondent: dict[str, list[RespondentEvent]]
    events_by_target: dict[tuple[str, str], list[RespondentEvent]]
    coordinates_by_respondent: dict[str, list[EmpiricalCoordinateFact]]
    routing_by_respondent: dict[str, list[RoutingEligibilityFact]]
    weights_by_respondent: dict[str, list[WeightMeasureFact]]
    source_relations: tuple[SourceUniverseRelation, ...]
    runtime_authorities: Any | None = None
    runtime_repository: C11Repository | None = None
    runtime_predicate_grammar_authority_ref: Any | None = None


@dataclass(frozen=True)
class _Evaluation:
    fact_state: str
    detail: str
    risk_members: tuple[ExactRef, ...]
    denominator_members: tuple[ExactRef, ...]
    raw_denominator: int
    raw_resolved_target_support: int
    raw_cells: Mapping[str, int]
    cell_material: Mapping[str, Any]
    weighted_denominator: Fraction | None
    weighted_cells: Mapping[str, Fraction] | None
    used_objects: tuple[CanonicalSemanticObject | C11InternalRecord, ...]
    used_authority_refs: tuple[AuthorityRef, ...]
    observed_response_ledger: Mapping[str, Any] | None = None


def _require_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise EmpiricalQueryExecutionError(f"{name} must be an exact mapping")
    return value


def _require_sequence(value: Any, name: str, *, allow_empty: bool = False) -> Sequence[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise EmpiricalQueryExecutionError(f"{name} must be a sequence")
    if not allow_empty and not value:
        raise EmpiricalQueryExecutionError(f"{name} may not be empty")
    return value


def _exact(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Pre553IntegrityError as exc:
        raise EmpiricalQueryResolutionError(str(exc)) from exc


def _authority(value: Any, name: str) -> AuthorityRef:
    try:
        return authority_ref(value, name)
    except Pre553IntegrityError as exc:
        raise EmpiricalQueryResolutionError(str(exc)) from exc


def _ref_field(obj: CanonicalSemanticObject, name: str, *, allow_none: bool = False) -> ExactRef | None:
    value = getattr(obj, name)
    if value is None and allow_none:
        return None
    return _exact(value, f"{obj.schema_id}.{name}")


def _authority_field(
    obj: CanonicalSemanticObject, name: str, *, allow_none: bool = False
) -> AuthorityRef | None:
    value = getattr(obj, name)
    if value is None and allow_none:
        return None
    return _authority(value, f"{obj.schema_id}.{name}")


def _canonical_refs(values: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    return tuple(sorted(set(values), key=lambda r: r.key))


def _canonical_authorities(values: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    return tuple(sorted(set(values), key=lambda r: r.key))


def _object_universe_ref(obj: CanonicalSemanticObject) -> ExactRef:
    return _ref_field(obj, "empirical_universe_ref")  # type: ignore[return-value]


def _object_respondent_ref(obj: CanonicalSemanticObject) -> ExactRef:
    return _ref_field(obj, "scoped_respondent_ref")  # type: ignore[return-value]


def _semantic_value(obj: RespondentEvent | EmpiricalCoordinateFact) -> Any:
    if isinstance(obj, RespondentEvent):
        canonical = obj.canonical_response_value_if_authorized
        return canonical if canonical is not None else obj.raw_response_value
    canonical = obj.canonical_coordinate_value_if_authorized
    return canonical if canonical is not None else obj.raw_coordinate_value


def _fraction_from_exact(value: Any, name: str) -> Fraction:
    if isinstance(value, bool):
        raise EmpiricalQueryExecutionError(f"{name} cannot be boolean")
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise EmpiricalQueryExecutionError(f"{name} is empty")
        try:
            return Fraction(text)
        except (ValueError, ZeroDivisionError) as exc:
            raise EmpiricalQueryExecutionError(f"{name} is not exact rational/decimal text") from exc
    if isinstance(value, Mapping):
        if set(value) == {"$exact_fraction"}:
            pair = _require_sequence(value["$exact_fraction"], name)
            if len(pair) != 2 or not all(isinstance(x, int) and not isinstance(x, bool) for x in pair):
                raise EmpiricalQueryExecutionError(f"{name} invalid exact fraction")
            return Fraction(pair[0], pair[1])
        if set(value) == {"$exact_decimal"} and isinstance(value["$exact_decimal"], str):
            try:
                return Fraction(value["$exact_decimal"])
            except ValueError as exc:
                raise EmpiricalQueryExecutionError(f"{name} invalid exact decimal") from exc
    raise EmpiricalQueryExecutionError(f"{name} is not an accepted exact numeric representation")


def _profile(query: EmpiricalQuerySpec) -> _ExecutionProfile:
    grain = _require_mapping(query.requested_output_grain, "requested_output_grain")
    mode = grain.get("source_scope_mode")
    measure = grain.get("measure_kind")
    risk = grain.get("risk_set_type")
    if mode not in SOURCE_SCOPE_MODES:
        raise EmpiricalQueryExecutionError("requested_output_grain.source_scope_mode is invalid")
    if measure not in MEASURE_KINDS:
        raise EmpiricalQueryExecutionError("requested_output_grain.measure_kind is invalid")
    if risk not in RISK_SET_TYPES:
        raise EmpiricalQueryExecutionError("requested_output_grain.risk_set_type is invalid")
    diagnostic = grain.get("diagnostic_kind")
    if diagnostic in DIAGNOSTIC_ONLY_KINDS:
        raise Pre553SemanticCollapseError("diagnostic score cannot define I03 EmpiricalFact execution")
    state_ref = _exact(grain.get("response_state_semantics_ref"), "response_state_semantics_ref")
    weight_basis = grain.get("weight_basis_id")
    if measure == "GOVERNED_WEIGHTED":
        if not isinstance(weight_basis, str) or not weight_basis.strip():
            raise EmpiricalQueryExecutionError("weighted query requires exact weight_basis_id")
        weight_basis = weight_basis.strip()
    elif weight_basis is not None:
        raise EmpiricalQueryExecutionError("RAW query may not carry a weight_basis_id")
    observed_ref_raw = grain.get("observed_response_contract_ref")
    observed_material_raw = grain.get("observed_response_contract")
    observed_ref: ExactRef | None = None
    observed_material: Mapping[str, Any] | None = None
    observed_condition_counts: Mapping[str, int] | None = None
    if risk in OBSERVED_RESPONSE_RISK_SET_TYPES:
        if measure != "RAW":
            raise EmpiricalQueryExecutionError(
                "observed-response operations are not weighted population estimands")
        if observed_ref_raw is None or observed_material_raw is None:
            raise EmpiricalQueryExecutionError(
                "observed-response risk set requires exact contract ref and material")
        observed_ref = _exact(
            observed_ref_raw, "requested_output_grain.observed_response_contract_ref")
        observed_material = _require_mapping(
            observed_material_raw, "requested_output_grain.observed_response_contract")
        if observed_material.get("contract_ref") is not None:
            raise EmpiricalQueryExecutionError(
                "observed_response_contract material must not embed its own contract_ref")
        raw_counts = grain.get("observed_response_condition_counts")
        if raw_counts is not None:
            counts = _require_mapping(raw_counts, "observed_response_condition_counts")
            normalized_counts: dict[str, int] = {}
            for key in ("condition_unobserved", "condition_false", "condition_true"):
                value = counts.get(key, 0)
                if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                    raise EmpiricalQueryExecutionError(
                        "observed_response_condition_counts values must be nonnegative integers")
                normalized_counts[key] = value
            observed_condition_counts = MappingProxyType(normalized_counts)
    else:
        if observed_ref_raw is not None or observed_material_raw is not None:
            raise EmpiricalQueryExecutionError(
                "observed-response contract binding requires an observed-response risk set")
    uncertainty = grain.get("uncertainty_method_or_typed_state", "UNCERTAINTY_UNQUANTIFIED")
    return _ExecutionProfile(
        mode,
        measure,
        risk,
        state_ref,
        weight_basis,
        canonicalize(uncertainty),
        observed_ref,
        observed_material,
        observed_condition_counts,
    )


def _parse_target_plan(query: EmpiricalQuerySpec, registry: AuthorityRegistry) -> _TargetPlan:
    spec = _require_mapping(query.target_arity_and_topology, "target_arity_and_topology")
    target_refs = tuple(_exact(v, "target_refs") for v in query.target_refs)
    arity = spec.get("arity")
    if not isinstance(arity, int) or isinstance(arity, bool) or arity < 1 or arity != len(target_refs):
        raise EmpiricalQueryExecutionError("target arity must exactly equal target_refs length")
    order_semantics = spec.get("joint_order_semantics")
    if order_semantics not in JOINT_ORDER_SEMANTICS:
        raise EmpiricalQueryExecutionError("joint_order_semantics is invalid")
    components_raw = _require_sequence(spec.get("components"), "target components")
    if len(components_raw) != arity:
        raise EmpiricalQueryExecutionError("target components length must equal declared arity")

    components: list[_TargetComponent] = []
    for idx, (raw, target_ref) in enumerate(zip(components_raw, target_refs)):
        item = _require_mapping(raw, f"target component {idx}")
        item_ref = _exact(item.get("target_ref"), f"target component {idx}.target_ref")
        if item_ref != target_ref:
            raise EmpiricalQueryResolutionError("target component exact ref disagrees with EmpiricalQuerySpec")
        topology = item.get("topology")
        if topology not in TARGET_TOPOLOGIES:
            raise UnsupportedResponseTopology(f"unsupported target topology {topology!r}")
        domain = tuple(canonicalize(v) for v in _require_sequence(
            item.get("domain", ()), f"target component {idx}.domain", allow_empty=True))
        replay_ref = _exact(item.get("target_domain_replay_ref"), "target_domain_replay_ref")
        topo_raw = item.get("topology_authority_refs")
        if topo_raw is None:
            topo_raw = [item.get("topology_authority_ref")]
        response_raw = item.get("response_semantic_authority_refs")
        if response_raw is None:
            response_raw = [item.get("response_semantic_authority_ref")]
        topo_auths = _canonical_authorities(
            _authority(v, "topology_authority_refs")
            for v in _require_sequence(topo_raw, "topology_authority_refs")
        )
        response_auths = _canonical_authorities(
            _authority(v, "response_semantic_authority_refs")
            for v in _require_sequence(response_raw, "response_semantic_authority_refs")
        )
        for ref in (*topo_auths, *response_auths):
            resolution = registry.resolve_exact(ref)
            if resolution.snapshot.typed_state != "ALLOW":
                raise Pre553AuthorityError("target topology/semantic authority is not positive")
        included_states_raw = _require_sequence(item.get("included_states"), "included_states")
        included_states = frozenset(str(x) for x in included_states_raw)
        if not included_states:
            raise EmpiricalQueryExecutionError("included_states cannot be empty")
        components.append(_TargetComponent(
            target_ref=item_ref,
            topology=topology,
            domain=domain,
            target_domain_replay_ref=replay_ref,
            topology_authority_refs=topo_auths,
            response_semantic_authority_refs=response_auths,
            included_states=included_states,
        ))

    if order_semantics == "CANONICAL_SET_ORDER":
        canonical_targets = tuple(sorted(target_refs, key=lambda r: r.key))
        if target_refs != canonical_targets:
            raise EmpiricalQueryExecutionError(
                "CANONICAL_SET_ORDER target_refs must already be exact-ref sorted")

    if any(not component.domain for component in components):
        full_domain: tuple[Any, ...] = ()
    elif arity == 1:
        full_domain = tuple(components[0].domain)
    else:
        explicit_joint = spec.get("joint_domain")
        if explicit_joint is not None:
            full_domain = tuple(canonicalize(v) for v in _require_sequence(
                explicit_joint, "joint_domain", allow_empty=True))
        else:
            full_domain = tuple(canonicalize(list(values)) for values in product(
                *(component.domain for component in components)))
    # Exact duplicate domain cells are a contract defect; silently collapsing them
    # would alter declared topology.
    domain_keys = [canonical_json(v) for v in full_domain]
    if len(domain_keys) != len(set(domain_keys)):
        raise EmpiricalQueryExecutionError("target domain contains duplicate exact cells")
    return _TargetPlan(
        components=tuple(components),
        joint_order_semantics=order_semantics,
        full_domain=full_domain,
        domain_identity=semantic_hash({
            "components": [
                {
                    "target_ref": c.target_ref.as_dict(),
                    "topology": c.topology,
                    "domain": list(c.domain),
                    "target_domain_replay_ref": c.target_domain_replay_ref.as_dict(),
                }
                for c in components
            ],
            "joint_order_semantics": order_semantics,
            "full_domain": list(full_domain),
        }),
    )


__all__ = [name for name in globals() if not name.startswith("__")]
