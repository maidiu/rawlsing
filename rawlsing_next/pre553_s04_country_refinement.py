"""Source-issued country guard + budgeted S04 determinicity screening.

This is an ADDITIVE S04 adapter over exact I03 output, not another query
engine, source decoder, statistical issuer or I05 frontier authority.

One-country universes (including GSS) work through the same exact source
identity law as country-specific portions of multi-country survey releases.
For a mixed-country universe, the upstream source owner must actually issue a
positive, scoped country-coordinate semantics authority. Without it we HOLD.

Each candidate table is computed by the existing S04 common-risk reader.
Resource budgets bound *which already-materialized candidate tables are
requested*, not upstream cold I03/open/index work. A supervising process is
still needed to enforce a hard deadline/RSS on an individual blocking call.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log2, prod
from time import monotonic
from typing import Any, Callable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry, require_positive_authority,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, EmpiricalPredicate, EmpiricalQuerySpec, EmpiricalUniverse,
    ExactRef, authority_ref, canonical_json, exact_ref, semantic_hash,
)
from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_s04_observed_research import (
    ask_s04_common_risk_predictor_evidence, receive_s04_i03_research,
)

CONTRACT = "PYAT_S04_SOURCE_ISSUED_COUNTRY_REFINEMENT@1"
HOLD = "HELD__COUNTRY_SOURCE_OR_RESOURCE"


class CountryRefinementError(ValueError):
    """An exact input/scope mismatch, not an empirical negative finding."""


@dataclass(frozen=True)
class CountryRequest:
    country: str
    source_family: str
    wave: str
    country_axis: int | None = None
    country_coordinate_ref: ExactRef | None = None
    country_coordinate_authority_ref: AuthorityRef | None = None
    source_country_value: Any | None = None  # source-native code, issuer-mapped


@dataclass(frozen=True)
class RefinementBudget:
    """Choose these numbers from a real host/workload, not inherited magic."""
    max_input_cells: int
    max_cell_visits: int
    max_output_cells: int
    max_candidates: int
    wall_seconds: float
    max_rss_bytes: int | None = None
    max_scratch_bytes: int | None = None


@dataclass(frozen=True)
class ResourceSample:
    rss_bytes: int
    scratch_bytes: int


def _same(a: Any, b: Any) -> bool:
    return canonical_json(a) == canonical_json(b)


def _has_entailing_country_leaf(
    node: Mapping[str, Any], *, coordinate: ExactRef, country: str,
    authority: AuthorityRef,
) -> bool:
    """A top-level conjunction of exact country equality entails the country.

    Country inside OR/NOT, a different authority/coordinate, or an IN with
    multiple possible values cannot establish a one-country predicate.
    """
    op = node.get("op")
    if op == "AND":
        children = node.get("children")
        return (isinstance(children, (tuple, list)) and
                any(isinstance(child, Mapping) and
                    _has_entailing_country_leaf(
                        child, coordinate=coordinate, country=country,
                        authority=authority,
                    ) for child in children))
    if op != "LEAF" or node.get("leaf_type") != "EMPIRICAL_POSITION_COORDINATE":
        return False
    if node.get("operator") != "EQ" or "exact_values" in node:
        return False
    try:
        return (
            exact_ref(node.get("coordinate_semantic_ref")) == coordinate
            and authority_ref(node.get("coordinate_authority_ref")) == authority
            and _same(node.get("exact_value"), country)
        )
    except (ValueError, TypeError, KeyError):
        return False


def _country_scope(
    *, universe: EmpiricalUniverse, query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate, registry: AuthorityRegistry,
    request: CountryRequest,
) -> tuple[str, int | None, Any]:
    if not request.country or not request.source_family or not request.wave:
        raise CountryRefinementError("COUNTRY_SOURCE_WAVE_REQUIRED")
    wave = universe.canonical_wave_if_governed or universe.raw_wave
    if universe.source_family != request.source_family or not _same(wave, request.wave):
        raise CountryRefinementError("SOURCE_WAVE_NOT_EXACT")
    if (len(query.empirical_universe_refs) != 1 or
            exact_ref(query.empirical_universe_refs[0]) != universe.ref or
            universe.ref not in tuple(exact_ref(r) for r in query.scope_refs) or
            exact_ref(query.condition_predicate_ref) != predicate.ref or
            universe.ref not in tuple(exact_ref(r) for r in predicate.scope_refs) or
            exact_ref(query.risk_set_ref) not in tuple(exact_ref(r) for r in predicate.risk_set_refs)):
        raise CountryRefinementError("QUERY_PREDICATE_SOURCE_SCOPE_MISMATCH")
    for obj in (universe, query, predicate):
        if semantic_hash(obj.semantic_projection()) != obj.content_hash:
            raise CountryRefinementError("SOURCE_OBJECT_HASH_MISMATCH")
        validate_object_authority_closure(obj, registry)

    if _same(universe.country_geography, request.country):
        if (request.country_axis is not None or request.country_coordinate_ref is not None or
                request.country_coordinate_authority_ref is not None or
                request.source_country_value is not None):
            raise CountryRefinementError("SOURCE_ALREADY_COUNTRY_SCOPED")
        return "SOURCE_UNIVERSE_COUNTRY", None, request.country

    # Neither family name nor a displayed country label can confer geography.
    # A multi-country source needs exact positive source semantic authority,
    # with an explicit governed country coordinate and universe declaration.
    if request.country_coordinate_ref is None or request.country_coordinate_authority_ref is None:
        raise CountryRefinementError("MULTICOUNTRY_COUNTRY_COORDINATE_ISSUER_REQUIRED")
    coord = exact_ref(request.country_coordinate_ref)
    auth = authority_ref(request.country_coordinate_authority_ref)
    snapshot = registry.resolve_exact(auth).snapshot
    require_positive_authority(
        snapshot, authority_kind="COORDINATE_SEMANTICS",
        object_family="EmpiricalCoordinateFact@1.0.0",
        source_universe_ref=universe.ref,
    )
    scope = snapshot.scope_envelope
    if not isinstance(scope, Mapping) or (
        not _same(scope.get("country_coordinate_semantic_ref"), coord.as_dict())
        or not _same(scope.get("source_universe_country_geography"),
                     universe.country_geography)
        or scope.get("country_scope_kind") != "MULTICOUNTRY_SOURCE_COORDINATE"
    ):
        raise CountryRefinementError("SOURCE_COUNTRY_COORDINATE_MEANING_NOT_ISSUED")

    country_values = scope.get("country_values_by_canonical_code")
    if (not isinstance(country_values, Mapping) or request.country not in country_values):
        raise CountryRefinementError("COUNTRY_CODE_TO_SOURCE_VALUE_NOT_ISSUED")
    source_value = country_values[request.country]
    if (source_value is None or isinstance(source_value, (Mapping, list, tuple)) or
            not isinstance(source_value, (str, int)) or isinstance(source_value, bool)):
        raise CountryRefinementError("INVALID_ISSUED_COUNTRY_SOURCE_VALUE")
    if request.source_country_value is not None and not _same(request.source_country_value, source_value):
        raise CountryRefinementError("SOURCE_COUNTRY_VALUE_MISMATCH")
    if request.country_axis is None:
        if not _has_entailing_country_leaf(
            predicate.predicate_ast, coordinate=coord, country=source_value,
            authority=auth,
        ):
            raise CountryRefinementError("QUERY_PREDICATE_DOES_NOT_ENTAIL_COUNTRY")
        return "ISSUED_EXACT_COUNTRY_PREDICATE", None, source_value

    axis = request.country_axis
    if type(axis) is not int or not 0 <= axis < len(query.target_refs):
        raise CountryRefinementError("COUNTRY_AXIS_INVALID")
    if exact_ref(query.target_refs[axis]) != coord:
        raise CountryRefinementError("COUNTRY_AXIS_NOT_SOURCE_COORDINATE")
    components = query.target_arity_and_topology.get("components")
    if not isinstance(components, (tuple, list)) or len(components) <= axis:
        raise CountryRefinementError("COUNTRY_AXIS_NO_SOURCE_DOMAIN")
    component = components[axis]
    if (not isinstance(component, Mapping) or
            not any(_same(v, source_value) for v in component.get("domain", ()))):
        raise CountryRefinementError("COUNTRY_NOT_IN_EXACT_SOURCE_DOMAIN")
    return "ISSUED_COUNTRY_AXIS", axis, source_value


def _mutual_information(table: Mapping[tuple[str, str], int]) -> float:
    row: dict[str, int] = {}
    col: dict[str, int] = {}
    total = 0
    for (x, y), n in table.items():
        if type(n) is not int or n < 0:
            raise CountryRefinementError("BAD_SOURCE_COUNT")
        row[x] = row.get(x, 0) + n
        col[y] = col.get(y, 0) + n
        total += n
    if total == 0:
        return 0.0
    return max(0.0, sum((n / total) * log2(n * total / (row[x] * col[y]))
                        for (x, y), n in table.items() if n))


def run_issued_country_refinement(
    *, universe: EmpiricalUniverse, predicate: EmpiricalPredicate,
    query: EmpiricalQuerySpec, execution: QueryExecutionResult,
    registry: AuthorityRegistry, request: CountryRequest,
    target_index: int, candidate_indices: Sequence[int],
    context: Mapping[int, Any], budget: RefinementBudget,
    resource_sample: Callable[[], ResourceSample] | None = None,
) -> dict[str, Any]:
    """Consume an issued I03 and return economical diagnostic candidate tables.

    Never promotes ranking to source fact or exact I05 control. The original
    I03/S04 source operation has *already happened*; caller must budget it
    separately. Each unvisited candidate is explicit unknown, never zero.
    """
    if not isinstance(universe, EmpiricalUniverse) or not isinstance(predicate, EmpiricalPredicate):
        raise CountryRefinementError("ACTUAL_SOURCE_OBJECTS_REQUIRED")
    if not isinstance(query, EmpiricalQuerySpec) or not isinstance(execution, QueryExecutionResult):
        raise CountryRefinementError("ACTUAL_I03_OBJECTS_REQUIRED")
    if not isinstance(registry, AuthorityRegistry):
        raise CountryRefinementError("EXACT_AUTHORITY_REGISTRY_REQUIRED")
    if (any(type(v) is not int or v <= 0 for v in (
            budget.max_input_cells, budget.max_cell_visits,
            budget.max_output_cells, budget.max_candidates))
            or not isinstance(budget.wall_seconds, (int, float)) or
            not 0 < budget.wall_seconds < float("inf")):
        raise CountryRefinementError("INVALID_RESOURCE_ENVELOPE")
    if (budget.max_rss_bytes is not None or budget.max_scratch_bytes is not None) and resource_sample is None:
        raise CountryRefinementError("RESOURCE_MONITOR_REQUIRED")
    mode, country_axis, source_country_value = _country_scope(
        universe=universe, query=query, predicate=predicate,
        registry=registry, request=request,
    )
    if (not isinstance(candidate_indices, (tuple, list)) or not candidate_indices
            or any(type(x) is not int for x in candidate_indices)
            or len(set(candidate_indices)) != len(candidate_indices)
            or type(target_index) is not int
            or not isinstance(context, Mapping)
            or any(type(k) is not int for k in context)):
        raise CountryRefinementError("INVALID_CANDIDATES_OR_CONTEXT")
    if target_index in context or target_index in candidate_indices:
        raise CountryRefinementError("TARGET_IS_NOT_ITS_OWN_PREDICTOR")
    if country_axis is not None and (country_axis == target_index or
            country_axis in candidate_indices or country_axis in context):
        raise CountryRefinementError("COUNTRY_CANNOT_COMPETE_AS_PREDICTOR")
    if any(x in context for x in candidate_indices):
        raise CountryRefinementError("ALREADY_CONDITIONED_PREDICTOR")
    if execution.query_ref != query.ref:
        raise CountryRefinementError("I03_QUERY_IDENTITY_MISMATCH")

    # Fail *before* S04 expands a wide complete domain into an expensive
    # Cartesian table. This returns a typed hold, not an inferred source zero.
    components = query.target_arity_and_topology.get("components")
    if not isinstance(components, (list, tuple)) or any(
            not isinstance(c, Mapping) or
            not isinstance(c.get("domain"), (list, tuple)) for c in components):
        raise CountryRefinementError("INVALID_SOURCE_TARGET_COMPONENTS")
    predicted_cells = prod(len(c["domain"]) for c in components)
    if predicted_cells > budget.max_input_cells:
        return {
            "contract": CONTRACT, "state": HOLD,
            "stop_reason": "ISSUED_JOINT_DOMAIN_EXCEEDS_BUDGET_BEFORE_S04",
            "country": request.country, "country_proof_mode": mode,
            "source_query_ref": query.ref.as_dict(),
            "unvisited_candidate_indices": list(candidate_indices),
            "projected_complete_domain_cells": predicted_cells,
            "source_fact_not_reinterpreted": True,
        }

    if resource_sample is not None:
        u = resource_sample()
        if not isinstance(u, ResourceSample) or u.rss_bytes < 0 or u.scratch_bytes < 0:
            raise CountryRefinementError("INVALID_RESOURCE_SAMPLE")
        if ((budget.max_rss_bytes is not None and u.rss_bytes >= budget.max_rss_bytes) or
                (budget.max_scratch_bytes is not None and u.scratch_bytes >= budget.max_scratch_bytes)):
            return {
                "contract": CONTRACT, "state": HOLD,
                "stop_reason": "RESOURCE_LIMIT_BEFORE_S04_MATERIALIZATION",
                "country": request.country, "country_proof_mode": mode,
                "source_query_ref": query.ref.as_dict(),
                "unvisited_candidate_indices": list(candidate_indices),
                "source_fact_not_reinterpreted": True,
            }

    knowledge = receive_s04_i03_research(query=query, execution=execution)
    m = knowledge.material()
    if m["state"] != "SUPPORTED_SAMPLE_DESCRIPTIVE":
        return {"contract": CONTRACT, "state": HOLD, "stop_reason": "SOURCE_I03_HELD",
                "country": request.country, "mode": mode, "unvisited": list(candidate_indices),
                "knowledge_ref": knowledge.ref.as_dict()}
    domains = m["target_domains"]
    rows = m["complete_cells"]
    if len(rows) > budget.max_input_cells:
        return {"contract": CONTRACT, "state": HOLD, "stop_reason": "JOINT_OVER_INPUT_BUDGET",
                "country": request.country, "mode": mode, "unvisited": list(candidate_indices),
                "knowledge_ref": knowledge.ref.as_dict()}
    if (any(x < 0 or x >= m["target_arity"] for x in candidate_indices) or
            target_index < 0 or target_index >= m["target_arity"]):
        raise CountryRefinementError("UNDECLARED_SOURCE_AXIS")
    conditions = dict(context)
    if country_axis is not None:
        conditions[country_axis] = source_country_value

    start = monotonic()
    visits, output_cells = 0, 0
    done: list[dict[str, Any]] = []
    stop = "EVALUATED_DECLARED_CANDIDATES"

    def within_resource() -> bool:
        if monotonic() - start >= budget.wall_seconds:
            return False
        if resource_sample is None:
            return True
        current = resource_sample()
        if not isinstance(current, ResourceSample) or current.rss_bytes < 0 or current.scratch_bytes < 0:
            raise CountryRefinementError("INVALID_RESOURCE_SAMPLE")
        return ((budget.max_rss_bytes is None or current.rss_bytes < budget.max_rss_bytes)
                and (budget.max_scratch_bytes is None or current.scratch_bytes < budget.max_scratch_bytes))

    for candidate in candidate_indices:
        if len(done) >= budget.max_candidates:
            stop = "CANDIDATE_COUNT_BUDGET"
            break
        # S04 scans this source joint once per candidate value. Admit enough
        # worst-case row visits *before* beginning a sealed candidate.
        projected = len(domains[candidate]) * len(domains[target_index])
        worst_visits = len(rows) * (1 + len(domains[candidate]))
        if (visits + worst_visits > budget.max_cell_visits or
                output_cells + projected > budget.max_output_cells):
            stop = "CELL_SCAN_OR_OUTPUT_BUDGET"
            break
        if not within_resource():
            stop = "WALL_RSS_OR_SCRATCH_BUDGET"
            break
        answer = ask_s04_common_risk_predictor_evidence(
            knowledge=knowledge, target_index=target_index,
            candidate_indices=(candidate,), context=conditions,
        ).material()
        tables = answer.get("tables", ())
        if not tables:
            stop = "SOURCE_TABLE_OR_SCIENCE_HELD"
            break
        table: dict[tuple[str, str], int] = {}
        branch_states = []
        for part in tables[0]["states"]:
            xkey = canonical_json(part["predictor_value"])
            branch_states.append({"value": part["predictor_value"],
                                  "raw_n": part["raw_conditioned_full_case_n"]})
            for cell in part["target_cells"]:
                table[(xkey, canonical_json(cell["target_state"]))] = cell["raw_count"]
        base_n = answer["common_full_case_n"]
        if sum(table.values()) != base_n:
            raise CountryRefinementError("COUNTRY_COMMON_RISK_NOT_CONSERVED")
        done.append({
            "index": candidate,
            "candidate_ref": m["target_refs"][candidate],
            "common_full_case_n": base_n,
            "unadjusted_mutual_information_bits": _mutual_information(table),
            "branches": branch_states,
            "source_s04_evidence_ref": answer["baseline_answer_ref"],
            "claim_grade": "SOURCE_EXACT_RAW_SAMPLE_DIAGNOSTIC_NOT_POPULATION_OR_CAUSAL",
        })
        visits += worst_visits
        output_cells += projected
    unvisited = list(candidate_indices[len(done):])
    return {
        "contract": CONTRACT,
        "state": "COMPLETE_NONCONTROLLING_SCREEN" if not unvisited else "PARTIAL_UNVISITED_UNKNOWN",
        "stop_reason": stop, "country": request.country,
        "source_family": request.source_family, "wave": request.wave,
        "country_proof_mode": mode, "country_axis": country_axis,
        "source_issued_country_value": source_country_value,
        "knowledge_ref": knowledge.ref.as_dict(),
        "source_query_ref": query.ref.as_dict(),
        "source_universe_ref": universe.ref.as_dict(),
        "source_risk_set_ref": exact_ref(query.risk_set_ref).as_dict(),
        "candidate_evidence": done, "unvisited_candidate_indices": unvisited,
        "used_upper_bound_cell_visits": visits, "used_output_cells": output_cells,
        "ranking_is_exploratory_not_method_issued": True,
        "comparable_full_case_only": True,
        "missingness_decomposition_issued": False,
        "design_variance_issued": False,
        "adaptive_i05_frontier_control": False,
        "process_supervisor_required_for_hard_per_unit_deadlines": True,
        "original_survey_rights_from_this_adapter": False,
    }


def run_r03_v2_issued_country_refinement(
    *, issuance: Any, operation_id: str, query_role: str,
    universe: EmpiricalUniverse, execution: QueryExecutionResult,
    request: CountryRequest, target_index: int,
    candidate_indices: Sequence[int], context: Mapping[int, Any],
    budget: RefinementBudget,
    resource_sample: Callable[[], ResourceSample] | None = None,
) -> dict[str, Any]:
    """Bind an original-R03-lowered *TEST_ONLY* QUERY role to the S04 adapter.

    The caller CANNOT inject a new query/predicate into this receiving path.
    R03 owns compilation and issuance; this adapter resolves exact preimages
    only from the authentic v2 runtime catalog. It does not upgrade R03's
    TEST_ONLY_SOURCEFREE ceiling to original-survey science.
    """
    from rawlsing_next.pre553_governed_query_issuer_v2 import (
        GOVERNED_QUERY_ISSUER_SCHEMA, GovernedQueryIssuanceV2,
    )

    if (type(issuance) is not GovernedQueryIssuanceV2
            or issuance.schema != GOVERNED_QUERY_ISSUER_SCHEMA
            or issuance.issued.record.scope != "TEST_ONLY_SOURCEFREE"):
        raise CountryRefinementError("R03_V2_EXACT_SOURCEFREE_ISSUANCE_REQUIRED")
    if (not isinstance(operation_id, str) or not operation_id
            or not isinstance(query_role, str) or not query_role):
        raise CountryRefinementError("R03_OPERATION_AND_ROLE_REQUIRED")
    issued = issuance.issued
    workload = issued.workload
    if (issued.envelope_sha256 != semantic_hash(workload.envelope())
            or issued.record.envelope_sha256 != issued.envelope_sha256):
        raise CountryRefinementError("R03_ISSUED_WORKLOAD_ENVELOPE_DRIFT")
    matches = [b for b in issuance.operation_jobs
               if b.operation_id == operation_id and b.query_role == query_role]
    if len(matches) != 1:
        raise CountryRefinementError("R03_ORIGINAL_QUERY_ROLE_NOT_ISSUED")
    binding = matches[0]
    if not any(
        r.query_ref == binding.query_ref and r.predicate_ref == binding.predicate_ref
        for r in workload.requests
    ):
        raise CountryRefinementError("R03_ISSUED_QUERY_ROLE_NOT_IN_WORKLOAD")
    catalog = workload.catalog
    query = catalog.resolve_query_exact(binding.query_ref)
    predicate = catalog.resolve_predicate_exact(binding.predicate_ref)
    if (query.ref != binding.query_ref or predicate.ref != binding.predicate_ref
            or exact_ref(query.condition_predicate_ref) != predicate.ref
            or not isinstance(execution, QueryExecutionResult)
            or execution.query_ref != query.ref):
        raise CountryRefinementError("R03_SOURCE_QUERY_PREDICATE_EXECUTION_DRIFT")
    result = run_issued_country_refinement(
        universe=universe, predicate=predicate, query=query, execution=execution,
        registry=catalog.authority_registry, request=request,
        target_index=target_index, candidate_indices=candidate_indices,
        context=context, budget=budget, resource_sample=resource_sample,
    )
    return {
        **result, "r03_issued_compilation_hash": issuance.content_hash,
        "r03_issued_operation_id": operation_id,
        "r03_issued_query_role": query_role,
        "r03_issued_workload_envelope_sha256": issued.envelope_sha256,
        "source_original_science_permission": "NOT_GRANTED_TEST_ONLY_SOURCEFREE",
    }
