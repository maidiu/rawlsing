"""Generic SOURCEFREE FF01 descriptive first reader of a genuine I03 joint fact.

This is not a new query engine, estimator, semantic issuer, FF02 structural
admission, or population/actor model.  It calls the existing I03 owner once,
then checks and conserves its full co-asked joint output at the FF01 boundary.
The frozen GT12/Q86B->Q86A count producer and D bridge remain untouched.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from json import loads
from math import prod
from typing import Any, Iterable, Mapping

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query


FAMILY = "FF01GenericObservedJoint@1.0.0"
MAX_DECLARED_CELLS = 16384  # explicit bounded sourcefree reader, not the future service ceiling
GRADE = "EXACT_RAW_DESCRIPTIVE_SAMPLE_ONLY__NO_POPULATION_INFERENCE"
BLOCKED_GRADE = "TYPED_PRODUCER_NONPOSITIVE__NO_OBSERVED_JOINT"
ANTI_INFERENCES = (
    "SAMPLE_ZERO_IS_NOT_STRUCTURAL_IMPOSSIBILITY",
    "CONDITIONING_IS_NOT_CAUSATION",
    "CO_TRAVEL_IS_NOT_BETWEEN_PERSON_RELATION",
    "SURVEY_POSITION_IS_NOT_INDEPENDENTLY_WARRANTED_MATERIAL_POWER",
    "NO_SCIENTIFICALLY_ISSUED_PREDICTOR_RANK",
    "NO_FF02_N9_V3_SOROK_AUTHORITY",
)


class FF01GenericIngressError(ValueError):
    """The input cannot lawfully become a generic FF01 observed relation."""


class FF01CapacityHold(FF01GenericIngressError):
    """The bounded exact full-domain reader declines excessive cardinality."""


@dataclass(frozen=True)
class FF01ObservedJoint:
    """A hash-addressed FF01 descriptive receipt, no separate fact repository.

    Its canonical JSON projection is the immutable value.  Each access returns
    detached material, so modifying a caller's export cannot mutate identity.
    """

    projection_json: str
    content_hash: str
    object_id: str

    def __post_init__(self) -> None:
        value = loads(self.projection_json)
        if canonical_json(value) != self.projection_json:
            raise FF01GenericIngressError("noncanonical FF01 projection")
        digest = semantic_hash(value)
        if value.get("family") != FAMILY or digest != self.content_hash:
            raise FF01GenericIngressError("FF01 identity/projection disagreement")
        if self.object_id != f"urn:rawlsing:ff01:observed-joint:sha256:{digest}":
            raise FF01GenericIngressError("FF01 object_id substituted")

    @property
    def ref(self) -> ExactRef:
        return ExactRef(FAMILY, self.object_id, self.content_hash)

    def semantic_projection(self) -> dict[str, Any]:
        return loads(self.projection_json)


def _exact(value: Any, label: str) -> ExactRef:
    try:
        return exact_ref(value, label)
    except (TypeError, ValueError, AttributeError, KeyError) as exc:
        raise FF01GenericIngressError(f"{label} must be an exact ref") from exc


def _refs(values: Iterable[Any], label: str) -> tuple[ExactRef, ...]:
    return tuple(_exact(value, label) for value in values)


def _permission_set(values: Iterable[str], label: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise FF01GenericIngressError(f"{label}: iterable of distinct permission names required")
    result = tuple(values)
    if not result or any(not isinstance(x, str) or not x.strip() for x in result):
        raise FF01GenericIngressError(f"{label}: empty or invalid permission")
    if len(result) != len(set(result)):
        raise FF01GenericIngressError(f"{label}: duplicate permission")
    return tuple(sorted(result))


def _domain(query: EmpiricalQuerySpec) -> tuple[tuple[ExactRef, ...], tuple[tuple[Any, ...], ...], str]:
    spec = query.target_arity_and_topology
    refs = _refs(query.target_refs, "target")
    if not isinstance(spec, Mapping) or len(refs) < 2 or spec.get("arity") != len(refs):
        raise FF01GenericIngressError("only exact multi-target queries with matching arity are admitted")
    if spec.get("joint_order_semantics") not in ("SEMANTIC_ORDERED", "CANONICAL_SET_ORDER"):
        raise FF01GenericIngressError("unsupported query target order")
    if spec.get("joint_order_semantics") == "CANONICAL_SET_ORDER" and refs != tuple(sorted(refs, key=lambda r: r.key)):
        raise FF01GenericIngressError("canonical target order is not canonical")
    components = spec.get("components")
    if not isinstance(components, (list, tuple)) or len(components) != len(refs):
        raise FF01GenericIngressError("target components absent or incorrectly ordered")
    domains: list[tuple[Any, ...]] = []
    normalized: list[dict[str, Any]] = []
    for i, (component, ref) in enumerate(zip(components, refs)):
        if not isinstance(component, Mapping) or _exact(component.get("target_ref"), "component.target_ref") != ref:
            raise FF01GenericIngressError(f"target component {i} changes its role")
        if component.get("topology") != "SCALAR_SINGULAR":
            raise FF01GenericIngressError("this exact reader cannot collapse repeated/multiselect topology")
        raw = component.get("domain")
        if not isinstance(raw, (list, tuple)):
            raise FF01GenericIngressError("source-native target domain missing")
        domain = tuple(canonicalize(v) for v in raw)
        if len({canonical_json(v) for v in domain}) != len(domain):
            raise FF01GenericIngressError("duplicate target state")
        replay_ref = _exact(component.get("target_domain_replay_ref"), "target_domain_replay_ref")
        domains.append(domain)
        normalized.append({
            "target_ref": ref.as_dict(),
            "topology": "SCALAR_SINGULAR",
            "domain": list(domain),
            "target_domain_replay_ref": replay_ref.as_dict(),
        })
    n = prod(len(d) for d in domains)
    if n > MAX_DECLARED_CELLS:
        raise FF01CapacityHold(f"declared {n} cells exceed sourcefree FF01 limit {MAX_DECLARED_CELLS}")
    cartesian = tuple(canonicalize(list(v)) for v in product(*domains))
    explicit = spec.get("joint_domain")
    if explicit is not None:
        if not isinstance(explicit, (list, tuple)):
            raise FF01GenericIngressError("explicit joint domain is malformed")
        explicit_keys = [canonical_json(canonicalize(v)) for v in explicit]
        if len(explicit_keys) != len(set(explicit_keys)) or set(explicit_keys) != {canonical_json(v) for v in cartesian}:
            raise FF01GenericIngressError("selected joint_domain omits or duplicates full cells")
        full = tuple(canonicalize(v) for v in explicit)
    else:
        full = cartesian
    identity = semantic_hash({
        "components": normalized,
        "joint_order_semantics": spec["joint_order_semantics"],
        "full_domain": list(full),
    })
    return refs, tuple(domains), identity


def receive_ff01_observed_joint(
    *,
    execution: QueryExecutionResult,
    query: EmpiricalQuerySpec,
    conditioner_index: int,
    producer_permission_ceiling: Iterable[str],
    relation_permission_ceiling: Iterable[str] | None = None,
) -> FF01ObservedJoint:
    """Consume one genuine I03 result, no re-query or inferred respondents.

    Only RAW SINGLE_UNIVERSE, scalar components, complete-domain exact joint
    cells are supported.  Nonpositive I03 facts retain their typed state with
    **no** projected positive joint.  Permission ceilings are caller-declared
    and are NOT proof of source-use issuance; the output is sample-descriptive.
    """
    if type(execution) is not QueryExecutionResult or type(query) is not EmpiricalQuerySpec:
        raise FF01GenericIngressError("exact I03 result/query types required")
    if semantic_hash(query.semantic_projection()) != query.content_hash:
        raise FF01GenericIngressError("query semantic identity mismatch")
    if query.typed_state != "QUERY_AUTHORIZED_RESOLVABLE" or execution.query_ref != query.ref:
        raise FF01GenericIngressError("not the exact selected authorized query")
    if execution.source_scope_mode != "SINGLE_UNIVERSE" or len(execution.release_refs) != 1:
        raise FF01GenericIngressError("cannot pool independent survey respondents at FF01")
    if len(execution.facts) != 1 or type(execution.facts[0]) is not EmpiricalFact:
        raise FF01GenericIngressError("one real producer-owned fact per single universe required")

    fact = execution.facts[0]
    if semantic_hash(fact.semantic_projection()) != fact.content_hash:
        raise FF01GenericIngressError("fact semantic identity mismatch")
    if _exact(fact.empirical_query_spec_ref, "fact.query") != query.ref:
        raise FF01GenericIngressError("substituted fact or query")
    if _exact(fact.condition_predicate_ref, "fact.predicate") != _exact(query.condition_predicate_ref, "query.predicate"):
        raise FF01GenericIngressError("changed condition predicate")
    if _exact(fact.risk_set_ref, "fact.risk") != _exact(query.risk_set_ref, "query.risk"):
        raise FF01GenericIngressError("changed risk population")
    if _exact(fact.measure_basis_ref, "fact.measure") != _exact(query.measure_basis_ref, "query.measure"):
        raise FF01GenericIngressError("changed measure basis")
    if _refs(fact.empirical_universe_refs, "fact.universe") != _refs(query.empirical_universe_refs, "query.universe"):
        raise FF01GenericIngressError("changed source universe")
    grain = query.requested_output_grain
    if not isinstance(grain, Mapping) or grain.get("source_scope_mode") != "SINGLE_UNIVERSE" or grain.get("measure_kind") != "RAW":
        raise FF01GenericIngressError("only source-scoped RAW original response counts admitted")
    if getattr(fact, "source_scope_mode", "SINGLE_UNIVERSE") != "SINGLE_UNIVERSE":
        raise FF01GenericIngressError("fact's source scope changed")
    if getattr(fact, "measure_kind", "RAW") != "RAW":
        raise FF01GenericIngressError("fact is not RAW")
    if fact.weighted_numerator_support_if_authorized is not None or fact.weighted_denominator_support_if_authorized is not None:
        raise FF01GenericIngressError("weighted inference cannot silently become RAW FF01")
    if _exact(fact.response_state_semantics_ref, "response_state") != _exact(grain.get("response_state_semantics_ref"), "query.response_state"):
        raise FF01GenericIngressError("response meaning changed")
    if fact.uncertainty_method_or_typed_state != grain.get("uncertainty_method_or_typed_state"):
        raise FF01GenericIngressError("uncertainty claim differs from query")
    if _exact(fact.replay_ref, "fact.replay") != _exact(fact.producer_replay_locator_or_reference_root, "fact.replay root"):
        raise FF01GenericIngressError("producer replay root substituted")

    dependencies = set(_refs(fact.dependency_refs, "fact.dependency"))
    provenance = set(_refs(fact.source_empirical_provenance_refs, "fact.provenance"))
    replay = _exact(fact.replay_ref, "fact.replay")
    if not provenance or not provenance.issubset(dependencies):
        raise FF01GenericIngressError("producer source evidence was dropped")
    if not {query.ref, replay, execution.release_refs[0]}.issubset(dependencies):
        raise FF01GenericIngressError("query/replay/release not bound to producer fact")
    if execution.release_refs[0] not in provenance:
        raise FF01GenericIngressError("claimed release missing from producer provenance")
    authorities = set(fact.authority_snapshot_refs)
    issued_query_authorities = {authority_ref(a) for a in query.query_authority_refs}
    if not authorities or not set(query.authority_snapshot_refs).issubset(authorities) or not issued_query_authorities.issubset(authorities):
        raise FF01GenericIngressError("query issuer/authority closure missing")

    refs, domains, domain_identity = _domain(query)
    if not isinstance(conditioner_index, int) or isinstance(conditioner_index, bool) or not (0 <= conditioner_index < len(refs)):
        raise FF01GenericIngressError("conditioner must be one actual target index")
    producer_permissions = _permission_set(producer_permission_ceiling, "producer permissions")
    relation_permissions = _permission_set(
        producer_permissions if relation_permission_ceiling is None else relation_permission_ceiling,
        "relation permissions",
    )
    if not set(relation_permissions).issubset(set(producer_permissions)):
        raise FF01GenericIngressError("consumer permissions widen producer permissions")

    projection = {
        "family": FAMILY,
        "claim_grade": GRADE if fact.typed_state == "SUPPORTED" else BLOCKED_GRADE,
        "producer_state": fact.typed_state,
        "source_permission_grade": "CALLER_DECLARED__NOT_INDEPENDENTLY_ISSUED",
        "producer_permission_ceiling": list(producer_permissions),
        "relation_permission_ceiling": list(relation_permissions),
        "producer_query_ref": query.ref.as_dict(),
        "producer_fact_ref": fact.ref.as_dict(),
        "producer_replay_ref": replay.as_dict(),
        "release_ref": execution.release_refs[0].as_dict(),
        "universe_ref": _exact(query.empirical_universe_refs[0], "query.universe").as_dict(),
        "risk_set_ref": _exact(query.risk_set_ref, "query.risk").as_dict(),
        "measure_basis_ref": _exact(query.measure_basis_ref, "query.measure").as_dict(),
        "condition_predicate_ref": _exact(query.condition_predicate_ref, "query.predicate").as_dict(),
        "authority_snapshot_refs": [a.as_dict() for a in sorted(authorities, key=lambda a: a.key)],
        "source_provenance_refs": [a.as_dict() for a in sorted(provenance, key=lambda a: a.key)],
        "target_refs": [r.as_dict() for r in refs],
        "target_domain_identity": domain_identity,
        "conditioner_index": conditioner_index,
        "conditioner_ref": refs[conditioner_index].as_dict(),
        "joint_order_semantics": query.target_arity_and_topology["joint_order_semantics"],
        "joint_arity": len(refs),
        "raw_eligible_condition_denominator": fact.raw_denominator_support,
        "raw_fully_resolved_joint_n": fact.raw_numerator_support,
        "uncertainty_state": fact.uncertainty_method_or_typed_state,
        "zero_means": "OBSERVED_ZERO_WITHIN_SUPPORTED_ASKED_RISK__NOT_IMPOSSIBLE",
        "complete_cells": [],
        "conditioned_complete_case_support": [],
        "not_proven": [
            "PER_CELL_RESPONDENT_MEMBERSHIP_NOT_PRESENT_IN_AGGREGATE_FACT",
            "RECURSIVE_DISCOVERY_NOT_ISSUED_BY_THIS_CONSUMER",
            "POPULATION_WEIGHT_VARIANCE_NOT_ESTABLISHED",
            "FF02_OR_MATERIAL_POWER_NOT_ISSUED",
            "PREDICTOR_IMPORTANCE_ESTIMATOR_NOT_ISSUED",
            "N10E_V3_ACTOR_NOT_CONSUMED_HERE",
        ],
        "anti_inferences": list(ANTI_INFERENCES),
    }
    if fact.typed_state == "SUPPORTED":
        topology = fact.target_topology
        if not isinstance(topology, Mapping) or topology.get("arity") != len(refs) or topology.get("joint_order_semantics") != query.target_arity_and_topology["joint_order_semantics"]:
            raise FF01GenericIngressError("fact has wrong joint topology/order")
        if topology.get("target_domain_identity") != domain_identity or getattr(fact, "target_domain_identity", domain_identity) != domain_identity:
            raise FF01GenericIngressError("fact joint domain identity differs from selected query")
        rows = topology.get("complete_cell_semantic_projection")
        if not isinstance(rows, (list, tuple)):
            raise FF01GenericIngressError("positive fact has no complete target cells")
        expected = {canonical_json(list(combo)) for combo in product(*domains)}
        seen: dict[str, tuple[Any, int]] = {}
        for row in rows:
            if not isinstance(row, Mapping) or not isinstance(row.get("cell"), (list, tuple)):
                raise FF01GenericIngressError("malformed joint row")
            cell = canonicalize(row["cell"])
            if len(cell) != len(refs):
                raise FF01GenericIngressError("joint row contains wrong number of target states")
            key = canonical_json(cell)
            if key not in expected or key in seen:
                raise FF01GenericIngressError("missing, unauthorized or duplicate joint cell")
            n = row.get("raw_numerator_support")
            if type(n) is not int or n < 0:
                raise FF01GenericIngressError("invalid joint count")
            expected_state = "OBSERVED_POSITIVE" if n else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
            if row.get("cell_state") != expected_state or row.get("weighted_numerator_support_if_authorized") is not None:
                raise FF01GenericIngressError("cell status or RAW weight material mismatch")
            seen[key] = (cell, n)
        if set(seen) != expected:
            raise FF01GenericIngressError("incomplete native joint cell support")
        total = sum(n for _, n in seen.values())
        if total != fact.raw_numerator_support or total > fact.raw_denominator_support:
            raise FF01GenericIngressError("joint count disagrees with producer fully resolved/eligible denominator")
        if getattr(fact, "raw_resolved_target_support", total) != total:
            raise FF01GenericIngressError("resolved target support lost in FF01")
        risk_members = getattr(fact, "risk_set_member_refs", None)
        denom_members = getattr(fact, "denominator_member_refs", None)
        if risk_members is not None and denom_members is not None:
            rm, dm = set(_refs(risk_members, "risk respondent")), set(_refs(denom_members, "denominator respondent"))
            if len(dm) != fact.raw_denominator_support or not dm.issubset(rm):
                raise FF01GenericIngressError("condition-selected denominator members disagree with fact")
        # Only rearrange I03's actual complete cells; do not infer per-cell people.
        projection["complete_cells"] = [
            {"cell": cell, "raw_support": n, "cell_state": "OBSERVED_POSITIVE" if n else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"}
            for cell, n in (seen[k] for k in sorted(seen))
        ]
        for condition_value in domains[conditioner_index]:
            selected = [
                {"remaining_state": [v for j, v in enumerate(cell) if j != conditioner_index], "raw_support": n}
                for cell, n in seen.values() if cell[conditioner_index] == condition_value
            ]
            projection["conditioned_complete_case_support"].append({
                "condition_value": condition_value,
                "fully_resolved_condition_n": sum(v["raw_support"] for v in selected),
                "remaining_joint_cells": sorted(selected, key=lambda item: canonical_json(item["remaining_state"])),
            })
    else:
        # Typed nonpositive results are retained without fabricating a domain
        # cell that the source/issuer did not actually support.
        if fact.raw_numerator_support != 0:
            raise FF01GenericIngressError("nonpositive producer has unexplained positive target support")

    canonical = canonical_json(projection)
    digest = semantic_hash(projection)
    return FF01ObservedJoint(
        projection_json=canonical,
        content_hash=digest,
        object_id=f"urn:rawlsing:ff01:observed-joint:sha256:{digest}",
    )


def execute_ff01_observed_joint(
    *,
    repository: Any,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    authority_registry: Any,
    release_refs: Iterable[ExactRef],
    conditioner_index: int,
    producer_permission_ceiling: Iterable[str],
    relation_permission_ceiling: Iterable[str] | None = None,
) -> FF01ObservedJoint:
    """One actual existing I03 execution, then the generic FF01 consumer."""
    refs = tuple(release_refs)
    actual = execute_empirical_query(
        repository=repository,
        query=query,
        predicate=predicate,
        authority_registry=authority_registry,
        release_refs=refs,
    )
    return receive_ff01_observed_joint(
        execution=actual, query=query, conditioner_index=conditioner_index,
        producer_permission_ceiling=producer_permission_ceiling,
        relation_permission_ceiling=relation_permission_ceiling,
    )


def replay_ff01_observed_joint(
    expected: ExactRef, **kwargs: Any,
) -> FF01ObservedJoint:
    current = receive_ff01_observed_joint(**kwargs)
    if current.ref != _exact(expected, "expected"):
        raise FF01GenericIngressError("source/conditions changed since selected FF01 result")
    return current


__all__ = [
    "FAMILY", "MAX_DECLARED_CELLS", "GRADE", "FF01GenericIngressError",
    "FF01CapacityHold", "FF01ObservedJoint", "receive_ff01_observed_joint",
    "execute_ff01_observed_joint", "replay_ff01_observed_joint",
]
