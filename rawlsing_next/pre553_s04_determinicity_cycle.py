"""PYAT S04/DHIKR continuing, country-safe, resource-bounded determinicity cycle.

The science is INHERITED: S04 exact same-case joint + DHIKR conditional
entropy, interaction, minority and optional IID sensitivity. This module
schedules and resumes those calculations. It does not replace I03, C11,
I05 or source-specific survey estimands. No statistical score is causal,
population-calibrated or an authority to suppress unsearched minorities.

A single issued country-bound I03 joint is the maximum knowledge available
here. Requests for a higher-resolution joint are returned as explicit next
SOURCE-ISSUANCE requirements, not fabricated source results.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from itertools import combinations, islice
from json import loads
from math import comb, isfinite, prod
from time import monotonic
from typing import Any, Callable, Mapping, Sequence

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry, require_positive_authority,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, EmpiricalPredicate, EmpiricalQuerySpec, EmpiricalUniverse,
    ExactRef, authority_ref, canonical_json, canonicalize, exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_s04_country_refinement import (
    CountryRequest, RefinementBudget, ResourceSample, _country_scope,
)
from rawlsing_next.pre553_s04_adaptive_support import (
    AdaptiveSupportPolicy, classify_observed_branch, order_child_probes,
    thresholds as country_support_thresholds,
)
from rawlsing_next.pre553_s04_observed_research import (
    MAX_CELLS as S04_MAX_CELLS, receive_s04_i03_research,
)
from rawlsing_next.pre553_s04_general_joint_algebra import (
    S04GeneralJointWorkspace, S04Projection,
)
from rawlsing_next.pre553_s04_dhikr_comparative import (
    DHIKRComparisonRequest, analyze_s04_dhikr,
    read_dhikr_sample_estimate, _association,
)

CYCLE_CONTRACT = "PYAT_S04_DHIKR_COUNTRY_BUDGETED_CONTINUING_CYCLE@1"
CONSUMER_CONTRACT = "PYAT_S04_DETERMINICITY_CONTEXT_EXISTING_FF_PREV3@1"
METHOD_GRADE = "SOURCE_EXACT_RAW_SAME_CASE_EXPLORATION_NONCAUSAL_NONPOPULATION"
MAX_DHIKR_BATCH = 8  # existing DHIKR method contract; batch, not total predictor ceiling


def _dhikr_batch_work_estimate(
    *, context_positive_rows: int, axis_count: int,
    bootstrap_replicates: int, raw_context_n: int,
    bootstrap_case_cap: int,
) -> int:
    """Accounting estimate for the INHERITED DHIKR operation, not CPU seconds.

    DHIKR performs same-case singles, pair diagnostics, and group scoring.
    Use source-observed nonzero cells in the exact current context, not the
    entire survey or an arbitrary eightfold multiplier. This is a planning
    estimate; measured wall time and a process supervisor remain distinct.
    """
    if not 1 <= axis_count <= MAX_DHIKR_BATCH:
        raise DeterminicityCycleError("INVALID_DHIKR_BATCH_WIDTH")
    pairs = comb(axis_count, 2)
    row_passes = 2 + 3 * axis_count + 4 * pairs
    bootstrap_work = (
        bootstrap_replicates * min(raw_context_n, bootstrap_case_cap)
        * (axis_count + pairs)
    )
    return max(1, context_positive_rows) * row_passes + bootstrap_work


def _plan_affordable_batch(
    *, remaining_axes: Sequence[int], max_width: int,
    context_positive_rows: int, context_raw_n: int,
    domains: Sequence[Sequence[Any]], target_axis: int,
    policy: "CyclePolicy", remaining_work: int,
    remaining_output_cells: int,
    measured_seconds_per_work_unit: Decimal | None = None,
    wall_seconds_remaining: float | None = None,
) -> tuple[tuple[int, ...], int, int]:
    """Downshift from a full 8-axis DHIKR inquiry to 1 affordable axis.

    Every candidate remains eligible for a later call. Small-batch
    interactions are partial evidence, not an exhaustive no-interaction
    finding. This prevents one pessimistic large-batch estimate from
    blocking useful source-valid screening.
    """
    max_width = min(MAX_DHIKR_BATCH, max_width, len(remaining_axes))
    for width in range(max_width, 0, -1):
        axes = tuple(remaining_axes[:width])
        pairs = comb(width, 2)
        work = _dhikr_batch_work_estimate(
            context_positive_rows=context_positive_rows,
            axis_count=width,
            bootstrap_replicates=policy.bootstrap_replicates,
            raw_context_n=context_raw_n,
            bootstrap_case_cap=policy.bootstrap_case_cap,
        )
        output = len(domains[target_axis]) + sum(
            len(domains[a]) for a in axes
        ) + pairs
        if work <= remaining_work and output <= remaining_output_cells:
            # After a real small pilot, admit only time-affordable work.
            # Calibration is local to this invocation; a resumed call on
            # another host must never inherit its wall-time forecast.
            if (measured_seconds_per_work_unit is not None
                    and wall_seconds_remaining is not None
                    and Decimal(work) * measured_seconds_per_work_unit
                    > Decimal(str(max(0.0, wall_seconds_remaining)))):
                continue
            return axes, work, output
    return (), 0, 0





class DeterminicityCycleError(ValueError):
    """Country, source, budget, replay or scientific-claim boundary refused."""


@dataclass(frozen=True)
class CyclePolicy:
    target_axis: int
    predictor_axes: tuple[int, ...]
    fixed_context: tuple[tuple[int, Any], ...]
    max_depth: int
    max_total_nodes: int
    max_pending_nodes: int
    max_new_nodes_per_call: int
    max_receipt_bytes: int
    max_pair_order: int = 2
    bootstrap_replicates: int = 0
    bootstrap_case_cap: int = 4096
    min_signal_bits: str = "0.0"  # canonical decimal; method tolerance, not physics
    support_policy: AdaptiveSupportPolicy = field(default_factory=AdaptiveSupportPolicy)

    def __post_init__(self) -> None:
        if (type(self.target_axis) is not int
                or type(self.predictor_axes) is not tuple
                or not self.predictor_axes
                or any(type(x) is not int or x < 0 for x in self.predictor_axes)
                or self.target_axis in self.predictor_axes
                or len(set(self.predictor_axes)) != len(self.predictor_axes)):
            raise DeterminicityCycleError("INVALID_TARGET_OR_PREDICTOR_AXIS")
        if (type(self.fixed_context) is not tuple
                or any(type(p) is not tuple or len(p) != 2
                       or type(p[0]) is not int for p in self.fixed_context)
                or len({p[0] for p in self.fixed_context}) != len(self.fixed_context)):
            raise DeterminicityCycleError("INVALID_FIXED_CONTEXT")
        if any(type(v) is not int or v < 1 for v in (
                self.max_total_nodes, self.max_pending_nodes,
                self.max_new_nodes_per_call, self.max_receipt_bytes,
                self.bootstrap_case_cap)):
            raise DeterminicityCycleError("INVALID_CYCLE_LIMIT")
        if (type(self.support_policy) is not AdaptiveSupportPolicy
                or type(self.max_depth) is not int or self.max_depth < 0
                or type(self.max_pair_order) is not int
                or self.max_pair_order not in (1, 2)
                or type(self.bootstrap_replicates) is not int
                or not 0 <= self.bootstrap_replicates <= 200):
            raise DeterminicityCycleError("INVALID_METHOD_SCOPE")
        try:
            value = Decimal(self.min_signal_bits)
        except (TypeError, ArithmeticError) as exc:
            raise DeterminicityCycleError("INVALID_SIGNAL_THRESHOLD") from exc
        if not value.is_finite() or value < 0:
            raise DeterminicityCycleError("INVALID_SIGNAL_THRESHOLD")
        for _, v in self.fixed_context:
            canonicalize(v)


@dataclass(frozen=True)
class ObservationChannel:
    """Only an independently issued source coordinate can distinguish M_X."""
    value_axis: int
    status_axis: int
    observed_status: Any
    unobserved_placeholder: Any
    semantics_authority_ref: AuthorityRef


@dataclass(frozen=True)
class DeterminicityCycleReceipt:
    payload_json: str
    content_hash: str

    def __post_init__(self) -> None:
        try:
            m = loads(self.payload_json)
            if (type(m) is not dict or m.get("contract") != CYCLE_CONTRACT
                    or canonical_json(m) != self.payload_json
                    or semantic_hash(m) != self.content_hash):
                raise DeterminicityCycleError("DETERMINICITY_RECEIPT_NOT_CANONICAL")
        except (ValueError, TypeError) as exc:
            raise DeterminicityCycleError("DETERMINICITY_RECEIPT_INVALID") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            CYCLE_CONTRACT, "urn:rawlsing:pyat:determinicity:" + self.content_hash,
            self.content_hash,
        )

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


def _key(value: Any) -> str:
    return canonical_json(value)


def _ctx(pairs: Sequence[Sequence[Any]]) -> dict[int, Any]:
    return {int(x[0]): x[1] for x in pairs}


def _serialize_context(context: Mapping[int, Any]) -> list[list[Any]]:
    return [[int(axis), canonicalize(value)] for axis, value in sorted(context.items())]


def _decimal(value: Any) -> Decimal:
    if type(value) is Decimal:
        if not value.is_finite():
            raise DeterminicityCycleError("NONFINITE_SCORE_REFUSED")
        return value
    v = read_dhikr_sample_estimate(value)
    return Decimal(0) if v is None else v


def _validate_budget(budget: RefinementBudget, resource_sample: Any) -> None:
    if type(budget) is not RefinementBudget:
        raise DeterminicityCycleError("INHERITED_RESOURCE_ENVELOPE_REQUIRED")
    if any(type(v) is not int or v < 1 for v in (
            budget.max_input_cells, budget.max_cell_visits,
            budget.max_output_cells, budget.max_candidates)):
        raise DeterminicityCycleError("INVALID_INTEGER_RESOURCE_BUDGET")
    if (type(budget.wall_seconds) not in (int, float)
            or not isfinite(budget.wall_seconds) or budget.wall_seconds <= 0):
        raise DeterminicityCycleError("INVALID_WALL_BUDGET")
    if any(v is not None and (type(v) is not int or v <= 0)
           for v in (budget.max_rss_bytes, budget.max_scratch_bytes)):
        raise DeterminicityCycleError("INVALID_PHYSICAL_RESOURCE_BUDGET")
    if ((budget.max_rss_bytes is not None or budget.max_scratch_bytes is not None)
            and not callable(resource_sample)):
        raise DeterminicityCycleError("MEASURED_RESOURCE_MONITOR_REQUIRED")


def _resource_ok(
    *, deadline: float, budget: RefinementBudget,
    resource_sample: Callable[[], ResourceSample] | None,
) -> bool:
    if monotonic() >= deadline:
        return False
    if resource_sample is None:
        return True
    sample = resource_sample()
    if (type(sample) is not ResourceSample
            or type(sample.rss_bytes) is not int or sample.rss_bytes < 0
            or type(sample.scratch_bytes) is not int or sample.scratch_bytes < 0):
        raise DeterminicityCycleError("INVALID_HOST_RESOURCE_SAMPLE")
    return ((budget.max_rss_bytes is None or sample.rss_bytes < budget.max_rss_bytes)
            and (budget.max_scratch_bytes is None
                 or sample.scratch_bytes < budget.max_scratch_bytes))


def _observation_contract(
    *, channel: ObservationChannel, registry: AuthorityRegistry,
    universe: EmpiricalUniverse, query: EmpiricalQuerySpec,
) -> None:
    if type(channel) is not ObservationChannel:
        raise DeterminicityCycleError("SOURCE_ISSUED_OBSERVATION_SPEC_REQUIRED")
    a, b = channel.value_axis, channel.status_axis
    if (type(a) is not int or type(b) is not int or a == b
            or min(a, b) < 0 or max(a, b) >= len(query.target_refs)):
        raise DeterminicityCycleError("INVALID_OBSERVATION_AXIS")
    snap = registry.resolve_exact(authority_ref(channel.semantics_authority_ref)).snapshot
    if snap.authority_kind not in ("COORDINATE_SEMANTICS", "SOURCE_SEMANTICS_TOPOLOGY"):
        raise DeterminicityCycleError("OBSERVATION_AUTHORITY_WRONG_SOURCE_FAMILY")
    require_positive_authority(
        snap, authority_kind=snap.authority_kind,
        source_universe_ref=universe.ref,
    )
    scope = snap.scope_envelope
    expected = {
        "observation_value_axis_ref": exact_ref(query.target_refs[a]).as_dict(),
        "observation_status_axis_ref": exact_ref(query.target_refs[b]).as_dict(),
        "observed_status_value": canonicalize(channel.observed_status),
        "unobserved_placeholder": canonicalize(channel.unobserved_placeholder),
        "observation_risk_set_ref": exact_ref(query.risk_set_ref).as_dict(),
    }
    if (not isinstance(scope, Mapping)
            or not all(key in scope for key in expected)
            or scope.get("observation_semantics_kind")
            != "SOURCE_ISSUED_OBSERVATION_STATUS_AND_VALUE"
            or any(_key(scope.get(k)) != _key(v) for k, v in expected.items())):
        raise DeterminicityCycleError("OBSERVATION_STATUS_SEMANTICS_NOT_ISSUED")


def _observation_value_information(
    *, cells: list[tuple[tuple[Any, ...], int]], target: int,
    channel: ObservationChannel,
) -> dict[str, Any]:
    """DHIKR's own same-risk MI estimator; missingness is NEVER imputed."""
    status = _association(cells, target, (channel.status_axis,))
    observed = []
    nonobs_n = 0
    for row, n in cells:
        if _key(row[channel.status_axis]) == _key(channel.observed_status):
            if _key(row[channel.value_axis]) == _key(channel.unobserved_placeholder):
                raise DeterminicityCycleError("OBSERVED_VALUE_IS_MISSING_PLACEHOLDER")
            observed.append((row, n))
        else:
            if _key(row[channel.value_axis]) != _key(channel.unobserved_placeholder):
                raise DeterminicityCycleError("NONOBSERVED_RESPONSE_VALUE_FABRICATED")
            nonobs_n += n
    n = sum(v for _, v in cells)
    nobs = sum(v for _, v in observed)
    if nobs + nonobs_n != n:
        raise DeterminicityCycleError("OBSERVATION_PARTITION_CHANGED_RISK")
    value = _association(observed, target, (channel.value_axis,))
    bits = value["information_bits"]
    adjusted = (Decimal(str(bits)) * Decimal(nobs) / Decimal(n)
                if n and bits is not None else Decimal(0))
    return {
        "value_axis": channel.value_axis,
        "status_axis": channel.status_axis,
        "observed_n": nobs,
        "nonobserved_n": nonobs_n,
        "denominator_n": n,
        "status_information_bits": status["information_bits"],
        "observed_value_information_bits": bits,
        "coverage_adjusted_value_bits": adjusted,
        "status_and_value_information_not_causal": True,
        "unobserved_value_imputation": False,
        "grade": "ISSUED_STATUS_SEPARATED_RAW_SAME_CASE__NO_DESIGN_VARIANCE",
    }


def _initial(
    *, identity: str, source: dict[str, Any], country_mode: str,
    context: dict[int, Any],
) -> dict[str, Any]:
    return {
        "contract": CYCLE_CONTRACT, "method_grade": METHOD_GRADE,
        "identity": identity, "source": source,
        "country_scope_mode": country_mode,
        "base_context": _serialize_context(context),
        "adaptive_support": None,
        "country_question_common_case_n": None,
        "base_same_case_n": None, "base_target_distribution": [],
        "base_support_grade": "NOT_YET_ISSUED",
        "nodes": [], "frontier": [{"context": _serialize_context(context),
                                  "depth": 0, "parent": None}],
        "deferred": [], "active": None,
        "total_estimated_cell_visits": 0,
        "completed_nodes": 0, "stopping_reason": "NOT_STARTED",
        "missingness_inference": "NOT_ASSUMED_FROM_COMPLETE_CASE_ABSENCE",
        "survey_design_uncertainty": "NOT_ISSUED",
        "population_predictor_determinism": "NOT_ISSUED",
        "original_source_currentness": "NOT_ESTABLISHED_BY_SOURCEFREE_ADAPTER",
        "independent_original_source_rights": False,
        "exact_I05_frontier_modified": False,
        "new_I03_queries": 0,
        "requires_external_worker_for_hard_blocking_deadline": True,
    }


def _revive_deferred(m: dict[str, Any], max_pending: int) -> None:
    """Resume exactly the eligible *observed* children, never fake zero cells.

    The parent node already retains all categories' source-positive evidence
    and a count of exact source-zero declared categories. This cursor
    persists the subset eligible for bounded further investigation; it
    does not convert other observed categories into absent possibilities.
    """
    while m["deferred"] and len(m["frontier"]) < max_pending:
        item = m["deferred"][0]
        nxt = item["next_index"]
        if nxt >= len(item["scheduled"]):
            m["deferred"].pop(0)
            continue
        child = item["scheduled"][nxt]
        ctx = _ctx(item["context"])
        ctx[item["axis"]] = child["source_value"]
        m["frontier"].append({
            "context": _serialize_context(ctx),
            "depth": item["depth"], "parent": item["parent"],
            "source_support_at_admission": child["support"],
        })
        item["next_index"] += 1


def _target_counts_in_context(
    positive: Sequence[tuple[tuple[Any, ...], int]], *,
    target_axis: int, context: Mapping[int, Any],
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row, n in positive:
        if all(_key(row[axis]) == _key(value) for axis, value in context.items()):
            k = _key(row[target_axis])
            counts[k] = counts.get(k, 0) + n
    return counts


def _child_outcome_inventory(
    *, positive: Sequence[tuple[tuple[Any, ...], int]],
    target_axis: int, split_axis: int, context: Mapping[int, Any],
    source_domain: Sequence[Any],
    country_n: int, policy: AdaptiveSupportPolicy,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], int]:
    """One source-joint pass; no modal-category truncation.

    Counts and contrasts are **source-exact** inside the same respondent
    population. Positive but below-threshold options remain inspectable
    in the parent inventory with their precise source-native identity.
    """
    parent_counts = _target_counts_in_context(
        positive, target_axis=target_axis, context=context)
    by_value: dict[str, dict[str, int]] = {}
    original: dict[str, Any] = {}
    for row, n in positive:
        if not all(_key(row[a]) == _key(v) for a, v in context.items()):
            continue
        key = _key(row[split_axis])
        original[key] = row[split_axis]
        child = by_value.setdefault(key, {})
        y = _key(row[target_axis])
        child[y] = child.get(y, 0) + n
    parent_n = sum(parent_counts.values())
    candidates: list[tuple[Any, dict[str, Any]]] = []
    for value in source_domain:
        key = _key(value)
        if key not in by_value:
            continue
        data = classify_observed_branch(
            country_question_n=country_n,
            parent_n=parent_n,
            observed_n=sum(by_value[key].values()),
            parent_target_counts=parent_counts,
            child_target_counts=by_value[key],
            policy=policy,
        )
        candidates.append((value, data))
    schedule, conserved = order_child_probes(candidates, policy)
    inventory = [
        {"source_value": value, "source_target_counts": by_value[_key(value)],
         "support": item}
        for value, item in candidates
    ]
    exact_source_zeros = len(source_domain) - len(candidates)
    if exact_source_zeros < 0 or sum(
        item["support"]["observed_raw_n"] for item in inventory
    ) != parent_n:
        raise DeterminicityCycleError("SPLIT_CHILD_POPULATION_NOT_CONSERVED")
    return schedule, conserved, inventory, exact_source_zeros


def advance_country_determinicity(
    *, universe: EmpiricalUniverse, query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate, execution: QueryExecutionResult,
    registry: AuthorityRegistry, country: CountryRequest,
    policy: CyclePolicy, resources: RefinementBudget,
    observation_channels: Sequence[ObservationChannel] = (),
    prior: DeterminicityCycleReceipt | None = None,
    independently_pinned_prior_ref: ExactRef | None = None,
    resource_sample: Callable[[], ResourceSample] | None = None,
    current_guard: Callable[[], Any] | None = None,
    issuer_evidence: Mapping[str, Any] | None = None,
) -> DeterminicityCycleReceipt:
    """Advance bounded work; resume by independently pinned receipt.

    Work is bounded in *estimated source-joint cell examinations*, real
    wall-clock prechecks, caller-provided current resource probes, retained
    output bytes and node count. A single blocking I03/S04/DHIKR call cannot
    be hard-killed here; supervised execution remains an explicit requirement.
    """
    _validate_budget(resources, resource_sample)
    if type(policy) is not CyclePolicy or type(registry) is not AuthorityRegistry:
        raise DeterminicityCycleError("EXACT_POLICY_AND_AUTHORITY_REQUIRED")
    if (type(query) is not EmpiricalQuerySpec or type(predicate) is not EmpiricalPredicate
            or type(execution) is not QueryExecutionResult
            or type(universe) is not EmpiricalUniverse):
        raise DeterminicityCycleError("ACTUAL_I03_SOURCE_OBJECTS_REQUIRED")
    mode, country_axis, country_value = _country_scope(
        universe=universe, query=query, predicate=predicate,
        registry=registry, request=country,
    )
    if query.ref != execution.query_ref:
        raise DeterminicityCycleError("I03_QUERY_AND_EXECUTION_DRIFT")
    arity = len(query.target_refs)
    if (not 0 <= policy.target_axis < arity
            or any(i >= arity for i in policy.predictor_axes)):
        raise DeterminicityCycleError("UNDECLARED_TARGET_OR_PREDICTOR")
    context = dict(policy.fixed_context)
    if (len(context) != len(policy.fixed_context)
            or any(i < 0 or i >= arity for i in context)
            or policy.target_axis in context
            or any(i in context for i in policy.predictor_axes)):
        raise DeterminicityCycleError("TARGET_OR_PREDICTOR_CONTEXT_LEAK")
    if country_axis is not None:
        if country_axis in context or country_axis == policy.target_axis or country_axis in policy.predictor_axes:
            raise DeterminicityCycleError("COUNTRY_AXIS_MUST_BE_FIXED_NOT_PREDICTOR")
        context[country_axis] = country_value
    channels: dict[int, ObservationChannel] = {}
    for channel in observation_channels:
        _observation_contract(channel=channel, registry=registry,
                              universe=universe, query=query)
        if (channel.value_axis not in policy.predictor_axes
                or channel.status_axis == policy.target_axis
                or channel.status_axis in policy.predictor_axes
                or channel.status_axis in context
                or channel.value_axis in channels):
            raise DeterminicityCycleError("OBSERVATION_CHANNEL_SCOPE_CONFLICT")
        channels[channel.value_axis] = channel

    components = query.target_arity_and_topology.get("components", ())
    if (len(components) != arity
            or any(not isinstance(c, Mapping) or
                   not isinstance(c.get("domain"), (list, tuple))
                   for c in components)):
        raise DeterminicityCycleError("MISSING_ISSUED_JOINT_DOMAINS")
    domain_cells = prod(len(c["domain"]) for c in components)
    if domain_cells > min(resources.max_input_cells, S04_MAX_CELLS):
        raise DeterminicityCycleError("JOINT_EXCEEDS_EXISTING_S04_AND_HOST_BUDGET")
    identity = semantic_hash({
        "source_query": query.ref.as_dict(),
        "source_predicate": predicate.ref.as_dict(),
        "source_universe": universe.ref.as_dict(),
        "source_release_refs": [r.as_dict() for r in execution.release_refs],
        "source_issuer_evidence": canonicalize(issuer_evidence) if issuer_evidence is not None
                                  else "EXACT_I03_QUERY_ISSUER_NOT_SEPARATELY_CERTIFIED",
        "country": country.country, "country_mode": mode,
        "country_native_value": canonicalize(country_value),
        "policy": {
            **{key: value for key, value in vars(policy).items()
               if key not in ("fixed_context", "min_signal_bits", "support_policy",
                              "max_total_nodes", "max_pending_nodes",
                              "max_new_nodes_per_call", "max_receipt_bytes")},
            "fixed_context": _serialize_context(context),
            "support_policy": vars(policy.support_policy),
            "min_signal_bits": Decimal(policy.min_signal_bits),
        },
        "observation_channels": [
            {"value_axis": c.value_axis, "status_axis": c.status_axis,
             "observed_status": canonicalize(c.observed_status),
             "unobserved_placeholder": canonicalize(c.unobserved_placeholder),
             "source_authority": c.semantics_authority_ref.as_dict()}
            for c in sorted(channels.values(), key=lambda x: x.value_axis)
        ],
    })
    start = monotonic()
    deadline = start + resources.wall_seconds
    if not _resource_ok(deadline=deadline, budget=resources,
                        resource_sample=resource_sample):
        raise DeterminicityCycleError("RESOURCE_LIMIT_BEFORE_SOURCE_RECEPTION")
    knowledge = receive_s04_i03_research(query=query, execution=execution)
    workspace = S04GeneralJointWorkspace(
        knowledge=knowledge, expected_knowledge_ref=knowledge.ref,
        current_guard=current_guard,
    )
    m_source = knowledge.material()
    source = {
        "knowledge_ref": knowledge.ref.as_dict(), "query_ref": query.ref.as_dict(),
        "fact_ref": m_source["fact_ref"], "release_ref": m_source["release_ref"],
        "universe_ref": m_source["universe_ref"],
        "risk_set_ref": m_source["risk_set_ref"],
        "response_semantics_ref": m_source["response_semantics_ref"],
        "target_refs": m_source["target_refs"],
        "target_axis": policy.target_axis,
        "country": country.country, "source_family": country.source_family,
        "wave": country.wave, "native_country_value": canonicalize(country_value),
        "issuer_evidence": canonicalize(issuer_evidence) if issuer_evidence is not None
                           else "EXACT_I03_QUERY_ISSUER_NOT_SEPARATELY_CERTIFIED",
    }
    if prior is None:
        if independently_pinned_prior_ref is not None:
            raise DeterminicityCycleError("UNEXPECTED_PRIOR_PIN")
        state = _initial(identity=identity, source=source,
                         country_mode=mode, context=context)
    else:
        if (type(prior) is not DeterminicityCycleReceipt
                or type(independently_pinned_prior_ref) is not ExactRef
                or independently_pinned_prior_ref != prior.ref):
            raise DeterminicityCycleError("INDEPENDENT_PREVIOUS_RECEIPT_PIN_REQUIRED")
        state = prior.material()
        if (state.get("identity") != identity or state.get("source") != source
                or state.get("country_scope_mode") != mode
                or state.get("completed_nodes") != len(state.get("nodes", []))):
            raise DeterminicityCycleError("RESUMED_SOURCE_POLICY_OR_IDENTITY_DRIFT")
    domains = m_source["target_domains"]
    for axis, value in context.items():
        if _key(value) not in {_key(v) for v in domains[axis]}:
            raise DeterminicityCycleError("CONDITION_OUTSIDE_EXACT_DOMAIN")
    if m_source["state"] != "SUPPORTED_SAMPLE_DESCRIPTIVE":
        state["stopping_reason"] = "UPSTREAM_TYPED_HELD_NOT_A_NEGATIVE_ANSWER"
        state["status"] = "HELD_SOURCE_NOT_AN_OBSERVED_ZERO"
        return _seal(state, policy.max_receipt_bytes)
    # Return a useful coarser answer even when no predictor-screening
    # operation can be admitted by this host budget. This S04 projection
    # is exact for the source-country risk set; it is NOT a population
    # estimate and is intentionally not re-derived from marginal tables.
    if len(domains[policy.target_axis]) > resources.max_output_cells:
        state["stopping_reason"] = "BASELINE_OUTPUT_DOMAIN_EXCEEDS_HOST_BUDGET"
        state["status"] = "HELD_SOURCE_OUTPUT_CAPACITY"
        return _seal(state, policy.max_receipt_bytes)
    country_only = (
        {country_axis: country_value} if country_axis is not None else {}
    )
    country_projection = workspace.query(S04Projection((), country_only)).material()
    country_n = country_projection["raw_selected_full_case_n"]
    if type(country_n) is not int or country_n < 0:
        raise DeterminicityCycleError("COUNTRY_QUESTION_COMMON_CASE_N_NOT_ISSUED")
    adaptive = country_support_thresholds(country_n, policy.support_policy)
    explore_min_n = adaptive["explore_min_n"]
    base = workspace.query(S04Projection(
        (policy.target_axis,), context,
    )).material()
    base_n = base["raw_selected_full_case_n"]
    base_grade = (
        "SOURCE_EXACT_RAW_SAME_CASE_COARSE_NOT_POPULATION"
        if base_n is not None and base_n >= explore_min_n else
        "SOURCE_OBSERVED_BELOW_EXPLORATION_THRESHOLD_NOT_POPULATION"
        if base_n else "ZERO_OR_HELD_CONTEXT_NO_POPULATION_CLAIM"
    )
    # Retain source-observed positive categories even when there is
    # insufficient support for a reliable inference. The downstream
    # population/actor consumer must separately check support_grade.
    base_counts = (
        [{"state": item["output_states"][0], "n": item["raw_count"]}
         for item in base["complete_output_cells"]]
        if base_n and base_n > 0 else []
    )
    if prior is not None and (
        state.get("base_context") != _serialize_context(context)
        or state.get("adaptive_support") != adaptive
        or state.get("country_question_common_case_n") != country_n
        or state.get("base_same_case_n") != base_n
        or state.get("base_target_distribution") != base_counts
        or state.get("base_support_grade") != base_grade
    ):
        raise DeterminicityCycleError("COARSER_SOURCE_BASELINE_CHANGED_ON_RESUME")
    state["base_context"] = _serialize_context(context)
    state["adaptive_support"] = adaptive
    state["country_question_common_case_n"] = country_n
    state["base_same_case_n"] = base_n
    state["base_target_distribution"] = base_counts
    state["base_support_grade"] = base_grade
    positive = [(tuple(row["cell"]), row["raw_count"])
                for row in m_source["complete_cells"] if row["raw_count"] > 0]
    used = domain_cells
    processed_axes = 0
    output_cells_used = 0
    timed_batch_work = 0
    timed_batch_seconds = Decimal(0)
    completed_this_call = 0
    stop = "NO_PENDING_WORK"
    # This controls exploration. Every batch is an actual DHIKR single-node
    # inquiry; existing entropy/interaction/minority code remains the owner.
    while True:
        if completed_this_call >= policy.max_new_nodes_per_call:
            stop = "CALL_NODE_BUDGET"; break
        if state["completed_nodes"] >= policy.max_total_nodes:
            stop = "TOTAL_NODE_BUDGET_WITH_UNSEARCHED_FRONTIER"; break
        _revive_deferred(state, policy.max_pending_nodes)
        if state["active"] is None:
            if not state["frontier"]:
                stop = "EXPLORATION_FRONTIER_COMPLETE"; break
            node = state["frontier"].pop(0)
            state["active"] = {
                **node, "next_predictor_offset": 0,
                "candidate_screens": [], "batch_groups": [],
                "raw_target_counts": None, "raw_n": None,
                "batch_bootstrap_sensitivity": [],
                "pairs_covered_in_batch": [],
                "next_cross_batch_pair_index": 0,
                "cross_batch_pair_evidence": [],
            }
        active = state["active"]
        selected = _ctx(active["context"])
        available = [a for a in policy.predictor_axes if a not in selected]
        cursor = active["next_predictor_offset"]
        if cursor < len(available) and processed_axes < resources.max_candidates:
            # Work is evaluated in THIS source-selected configuration.
            # Never reject a useful singleton because a proposed 8-axis
            # screening batch is too expensive. DHIKR's fixed eight-axis
            # arity is a per-call method limit, not a scientific stop.
            context_positive = [
                (row, n) for row, n in positive if all(
                    _key(row[a]) == _key(v) for a, v in selected.items()
                )
            ]
            context_raw_n = sum(n for _, n in context_positive)
            if not _resource_ok(deadline=deadline, budget=resources,
                                resource_sample=resource_sample):
                stop = "HOST_DEADLINE_RSS_OR_SCRATCH_LIMIT"; break
            batch, estimated, projected_output = _plan_affordable_batch(
                remaining_axes=available[cursor:],
                # Start with a small timed probe instead of betting the
                # entire interactive wall budget on an uncalibrated 8-axis
                # estimate. Subsequent batches grow when measured time fits.
                max_width=min(
                    2 if timed_batch_work == 0 else MAX_DHIKR_BATCH,
                    resources.max_candidates - processed_axes,
                ),
                context_positive_rows=len(context_positive),
                context_raw_n=context_raw_n,
                domains=domains, target_axis=policy.target_axis,
                policy=policy,
                remaining_work=resources.max_cell_visits - used,
                remaining_output_cells=resources.max_output_cells - output_cells_used,
                measured_seconds_per_work_unit=(
                    timed_batch_seconds / Decimal(timed_batch_work)
                    if timed_batch_work else None
                ),
                wall_seconds_remaining=deadline - monotonic(),
            )
            if not batch:
                stop = "NO_SINGLETON_FITS_REMAINING_ACCOUNTING_ENVELOPE"; break
            k = len(batch)
            req = DHIKRComparisonRequest(
                target_axis=policy.target_axis, predictor_axes=batch,
                fixed_context=tuple(sorted(selected.items())),
                min_branch_n=explore_min_n, max_depth=0, max_nodes=1,
                max_interaction_order=policy.max_pair_order,
                bootstrap_replicates=policy.bootstrap_replicates,
                bootstrap_case_cap=policy.bootstrap_case_cap,
            )
            before_batch = loads(canonical_json(state))
            batch_started = monotonic()
            result = analyze_s04_dhikr(workspace, req).material()
            actual_seconds = Decimal(str(round(monotonic() - batch_started, 6)))
            used += estimated
            timed_batch_work += estimated
            timed_batch_seconds += actual_seconds
            output_cells_used += projected_output
            processed_axes += k
            if policy.max_pair_order == 2 and k >= 2:
                active["pairs_covered_in_batch"].extend(
                    [list(pair) for pair in combinations(batch, 2)]
                )
            active["batch_bootstrap_sensitivity"].append({
                "source_dhikr_source_query_ref": result["source_query_ref"],
                "budget_forecast_cell_visits": estimated,
                "measured_batch_wall_seconds": actual_seconds,
                "batch_width_selected_by_affordability": k,
                "candidate_axes": list(batch),
                "bootstrap_state": result["bootstrap_rank_instability"],
                "method": (
                    "IID_RAW_MIXED_STATUS_SCORE_NOT_VALID_FOR_VALUE_PRIORITY"
                    if any(a in channels for a in batch)
                    else "IID_SENSITIVITY_ONLY_NOT_COMPLEX_SURVEY_DESIGN"
                ),
            })
            if result["state"] != "SOURCE_COHERENT_SAMPLE_COMPARISON":
                active["raw_n"] = 0
                active["raw_target_counts"] = []
                active["next_predictor_offset"] = len(available)
            elif result["nodes"]:
                node = result["nodes"][0]
                if active["raw_n"] is not None and active["raw_n"] != node["raw_same_case_n"]:
                    raise DeterminicityCycleError("CROSS_BATCH_COMMON_RISK_CHANGED")
                active["raw_n"] = node["raw_same_case_n"]
                active["raw_target_counts"] = node["raw_target_counts"]
                for score in node["sample_association_scores"]:
                    item = {
                        "axis": score["axis"],
                        "source_predictor_ref": m_source["target_refs"][score["axis"]],
                        "raw_n": score["raw_n"],
                        "information_bits": score["information_bits"],
                        "normalized_reduction": score["normalized_reduction"],
                        "missingness_grade": "NOT_ISSUED_COMPLETE_CASE_ONLY",
                    }
                    if score["axis"] in channels:
                        chosen = [(row, n) for row, n in positive if all(
                            _key(row[a]) == _key(v) for a, v in selected.items())]
                        extra = _observation_value_information(
                            cells=chosen, target=policy.target_axis,
                            channel=channels[score["axis"]],
                        )
                        item["source_issued_observation_decomposition"] = extra
                        item["priority_information_bits"] = extra["coverage_adjusted_value_bits"]
                        item["missingness_grade"] = extra["grade"]
                    else:
                        item["priority_information_bits"] = _decimal(score["information_bits"])
                    active["candidate_screens"].append(item)
                axes = tuple(node["priority_group"])
                if axes and not any(a in channels for a in axes):
                    active["batch_groups"].append({
                        "axes": list(axes),
                        "per_axis_priority_bits": node["priority_normalized_by_group_size_bits"],
                        "minority_contradictions": node["minority_contradictions"],
                        "search_scope": "SAME_BATCH_UP_TO_PAIR_ORDER",
                    })
                # A status-adjusted predictor can still be chosen; its
                # missingness information never enters value priority.
                for item in active["candidate_screens"][-k:]:
                    if item["axis"] in channels:
                        active["batch_groups"].append({
                            "axes": [item["axis"]],
                            "per_axis_priority_bits": item["priority_information_bits"],
                            "minority_contradictions": [],
                            "search_scope": "SOURCE_ISSUED_OBSERVED_VALUE_ONLY",
                        })
                active["next_predictor_offset"] += k
            else:
                active["raw_n"] = 0
                active["raw_target_counts"] = []
                active["next_predictor_offset"] = len(available)
            # Progress checkpoint can be returned mid-node. The remaining
            # unscanned predictors are explicitly NOT_SEARCHED.
            if len(canonical_json(state).encode("utf-8")) > policy.max_receipt_bytes:
                state = before_batch
                stop = "RECEIPT_BUDGET_BEFORE_UNCOMMITTED_DHIKR_BATCH"
                break
            if active["next_predictor_offset"] < len(available):
                continue
        if active["next_predictor_offset"] < len(available):
            stop = "PREDICTOR_BATCH_BUDGET_UNSEARCHED"; break
        # All marginal candidates have now been examined. Recover useful
        # pairwise interactions between candidates that fell into *different*
        # budget-sized batches. Otherwise shrinking a batch for economy could
        # silently miss an XOR (zero information for both single variables).
        # Read the same joint; no new I03, R03, storage or predictor authority.
        if policy.max_pair_order == 2 and len(available) >= 2:
            total_pairs = comb(len(available), 2)
            covered = {
                (int(pair[0]), int(pair[1]))
                for pair in active["pairs_covered_in_batch"]
            }
            # Skip source-unissued observation-status interactions rather
            # than ranking mixed missingness as predictive value.
            while active["next_cross_batch_pair_index"] < total_pairs:
                pair_index = active["next_cross_batch_pair_index"]
                pair = next(islice(combinations(available, 2), pair_index, None))
                if pair in covered or any(a in channels for a in pair):
                    active["next_cross_batch_pair_index"] += 1
                    continue
                if processed_axes >= resources.max_candidates:
                    stop = "CROSS_BATCH_INTERACTION_CALL_BUDGET"
                    break
                context_positive = [
                    (row, n) for row, n in positive if all(
                        _key(row[a]) == _key(v) for a, v in selected.items()
                    )
                ]
                # One inherited two-axis association scan and its emitted
                # diagnostic; unlike DHIKR's full group comparator, no
                # duplicate full-joint projection or bootstrap is incurred.
                pair_work = max(1, len(context_positive))
                if (used + pair_work > resources.max_cell_visits
                        or output_cells_used + 1 > resources.max_output_cells
                        or not _resource_ok(
                            deadline=deadline, budget=resources,
                            resource_sample=resource_sample,
                        )):
                    stop = "CROSS_BATCH_INTERACTION_RESOURCE_BUDGET"
                    break
                before_pair = loads(canonical_json(state))
                pair_started = monotonic()
                estimate = _association(
                    context_positive, policy.target_axis, pair,
                )
                pair_elapsed = Decimal(
                    str(round(monotonic() - pair_started, 6))
                )
                used += pair_work
                output_cells_used += 1
                processed_axes += 1
                bits = _decimal(estimate["information_bits"])
                active["cross_batch_pair_evidence"].append({
                    "axes": list(pair),
                    "raw_n": estimate["raw_n"],
                    "information_bits": estimate["information_bits"],
                    "budget_forecast_cell_visits": pair_work,
                    "measured_wall_seconds": pair_elapsed,
                    "source_evidence": "EXISTING_S04_SAME_CASE_DHIKR_ASSOCIATION",
                })
                if bits > 0:
                    active["batch_groups"].append({
                        "axes": list(pair),
                        "per_axis_priority_bits": bits / Decimal(2),
                        "minority_contradictions": [],
                        "search_scope": "CROSS_BATCH_SAME_CASE_PAIR",
                    })
                active["next_cross_batch_pair_index"] += 1
                if len(canonical_json(state).encode("utf-8")) > policy.max_receipt_bytes:
                    state = before_pair
                    stop = "CROSS_BATCH_PAIR_RECEIPT_STORAGE_BUDGET"
                    break
            if active["next_cross_batch_pair_index"] < total_pairs:
                break
        # Once every candidate in this query joint has been conditioned
        # away, the result is still a REAL source-supported leaf distribution.
        # It must not be mislabeled as LOW_SUPPORT merely because no
        # predictor batch remained to call DHIKR.
        if active["raw_n"] is None:
            exact_leaf = workspace.query(S04Projection(
                (policy.target_axis,), selected,
            )).material()
            active["raw_n"] = exact_leaf["raw_selected_full_case_n"]
            active["raw_target_counts"] = [
                {"state": c["output_states"][0], "n": c["raw_count"]}
                for c in exact_leaf["complete_output_cells"]
            ]

        node_id = state["completed_nodes"]
        groups = sorted(
            active["batch_groups"],
            key=lambda v: (-_decimal(v["per_axis_priority_bits"]),
                           len(v["axes"]), v["axes"]),
        )
        best = groups[0] if groups else None
        gain = _decimal(best["per_axis_priority_bits"]) if best else Decimal(0)
        split = best["axes"][0] if best and gain > Decimal(policy.min_signal_bits) else None
        raw_n = active["raw_n"]
        no_support = raw_n is None or raw_n < policy.min_branch_n
        if no_support:
            split = None
        if active["depth"] >= policy.max_depth:
            split = None
        complete = {
            "node": node_id, "parent": active["parent"],
            "depth": active["depth"], "context": active["context"],
            "raw_same_case_n": raw_n,
            "target_distribution": active["raw_target_counts"] if not no_support else [],
            "target_disclosure": ("RAW_SAME_CASE_SAMPLE_NOT_POPULATION"
                                  if not no_support else "LOW_ZERO_OR_HELD_NO_TARGET_DISCLOSURE"),
            "predictor_screens": active["candidate_screens"],
            "exploratory_priority_groups": groups,
            "selected_split_axis": split,
            "selected_split_score_bits": gain,
            "minority_contradictions": (
                best["minority_contradictions"] if best else []
            ),
            "cross_batch_interactions": (
                active["cross_batch_pair_evidence"]
                if policy.max_pair_order == 2 else
                "NOT_REQUESTED_SINGLETON_ONLY"
            ),
            "missingness_for_unspecified_axes": "NOT_ISSUED",
            "bootstrap_uncertainty": active["batch_bootstrap_sensitivity"],
            "survey_design_variance": "NOT_ISSUED",
            "terminal_reason": (
                "LOW_OR_ZERO_SOURCE_SUPPORT" if no_support
                else "CONFIGURED_DEPTH_BOUND" if active["depth"] >= policy.max_depth
                else "NO_OBSERVED_POSITIVE_INFORMATION_OR_UNSEARCHED_INTERACTIONS"
                if split is None else None
            ),
        }
        next_state = dict(state)
        next_state["nodes"] = state["nodes"] + [complete]
        next_state["active"] = None
        next_state["completed_nodes"] = node_id + 1
        next_state["frontier"] = list(state["frontier"])
        next_state["deferred"] = [dict(d) for d in state["deferred"]]
        if split is not None:
            next_state["deferred"].append({
                "context": active["context"], "axis": split,
                "next_index": 0, "depth": active["depth"] + 1,
                "parent": node_id,
            })
            _revive_deferred(next_state, policy.max_pending_nodes)
        if len(canonical_json(next_state).encode("utf-8")) > policy.max_receipt_bytes:
            stop = "RECEIPT_STORAGE_BUDGET_CURRENT_NODE_UNCOMMITTED"; break
        state = next_state
        completed_this_call += 1
    state["total_estimated_cell_visits"] += used
    state["last_call_estimated_cell_visits"] = used
    state["last_call_budgeted_output_cells"] = output_cells_used
    state["last_call_measured_dhikr_batch_seconds"] = timed_batch_seconds
    state["last_call_measured_batch_work_units"] = timed_batch_work
    state["last_call_wall_forecast_is_host_local_not_science"] = True
    state["last_call_elapsed_seconds"] = Decimal(
        str(round(monotonic() - start, 6))
    )
    state["stopping_reason"] = stop
    state["remaining_budgeted_work"] = bool(
        state["active"] or state["frontier"] or state["deferred"])
    state["status"] = ("PARTIAL_RESUMABLE"
                       if state["remaining_budgeted_work"]
                       else "COMPLETE_WITHIN_SOURCE_JOINT_NOT_EXHAUSTIVE_HUMAN")
    # Check same source-current guard after all calculations.
    workspace.query(S04Projection((), {}))
    return _seal(state, policy.max_receipt_bytes)


def _seal(material: dict[str, Any], max_bytes: int) -> DeterminicityCycleReceipt:
    packed = canonical_json(material)
    if len(packed.encode("utf-8")) > max_bytes:
        raise DeterminicityCycleError(
            "CHECKPOINT_CANNOT_FIT_RETENTION_BUDGET__NO_SOURCE_FACT_CHANGED")
    return DeterminicityCycleReceipt(packed, semantic_hash(material))


def consume_determinicity_context_for_prev3(
    *, receipt: DeterminicityCycleReceipt,
    independently_pinned_receipt_ref: ExactRef,
    workspace: S04GeneralJointWorkspace,
    node_id: int | None = None,
) -> dict[str, Any]:
    """Real S04 projection consumer, suitable to pass conditions to C4/C5.

    No actor, trait, probability generalization, FF02 grant, or implicit
    C4 external receipt is produced. Caller must separately retain and pin
    its original FF/C4 source bridge and the same source I03 joint.
    """
    if (type(receipt) is not DeterminicityCycleReceipt
            or type(independently_pinned_receipt_ref) is not ExactRef
            or independently_pinned_receipt_ref != receipt.ref
            or type(workspace) is not S04GeneralJointWorkspace
            or (node_id is not None and type(node_id) is not int)):
        raise DeterminicityCycleError("INDEPENDENT_RECEIPT_AND_WORKSPACE_REQUIRED")
    m = receipt.material()
    if m["source"]["knowledge_ref"] != workspace._knowledge.ref.as_dict():
        raise DeterminicityCycleError("FOREIGN_SOURCE_OR_UNISSUED_NODE")
    if node_id is None:
        node = {
            "context": m["base_context"],
            "raw_same_case_n": m["base_same_case_n"],
            "target_disclosure": (
                "RAW_SAME_CASE_SAMPLE_NOT_POPULATION"
                if m["base_support_grade"].startswith("SOURCE_EXACT")
                else "COARSE_SOURCE_HELD"
            ),
        }
    else:
        if not 0 <= node_id < len(m["nodes"]):
            raise DeterminicityCycleError("FOREIGN_SOURCE_OR_UNISSUED_NODE")
        node = m["nodes"][node_id]
    if node["target_disclosure"] != "RAW_SAME_CASE_SAMPLE_NOT_POPULATION":
        raise DeterminicityCycleError("HELD_CONTEXT_CANNOT_BECOME_PERSONAL_EVIDENCE")
    context = _ctx(node["context"])
    answer = workspace.query(S04Projection(
        (m["source"]["target_axis"],), context,
    ))
    result = answer.material()
    if result["raw_selected_full_case_n"] != node["raw_same_case_n"]:
        raise DeterminicityCycleError("CONTEXT_CHANGED_SOURCE_DENOMINATOR")
    if result["knowledge_ref"] != m["source"]["knowledge_ref"]:
        raise DeterminicityCycleError("CONTEXT_SOURCE_NOT_SAME_JOINT")
    return {
        "contract": CONSUMER_CONTRACT,
        "determinicity_receipt_ref": receipt.ref.as_dict(),
        "existing_s04_projection_ref": answer.ref.as_dict(),
        "source_fact_ref": m["source"]["fact_ref"],
        "source_query_ref": m["source"]["query_ref"],
        "source_risk_set_ref": m["source"]["risk_set_ref"],
        "source_universe_ref": m["source"]["universe_ref"],
        "country": m["source"]["country"],
        "source_family": m["source"]["source_family"],
        "wave": m["source"]["wave"],
        "conditions_for_existing_c4_c5": context,
        "target_distribution": result["complete_output_cells"],
        "raw_same_case_n": result["raw_selected_full_case_n"],
        "unvisited_frontier_retained": m["remaining_budgeted_work"],
        "grade": METHOD_GRADE,
        "must_use_existing_independently_pinned_c4_c5_before_v3": True,
        "does_not_issue_actor_or_person": True,
        "does_not_issue_population_probability_or_causality": True,
    }



def advance_r03_v2_country_determinicity(
    *, issuance: Any, operation_id: str, query_role: str,
    universe: EmpiricalUniverse, execution: QueryExecutionResult,
    country: CountryRequest, policy: CyclePolicy, resources: RefinementBudget,
    observation_channels: Sequence[ObservationChannel] = (),
    prior: DeterminicityCycleReceipt | None = None,
    independently_pinned_prior_ref: ExactRef | None = None,
    resource_sample: Callable[[], ResourceSample] | None = None,
    current_guard: Callable[[], Any] | None = None,
) -> DeterminicityCycleReceipt:
    """Actual R03 V2 sourcefree issuer→I03→S04/DHIKR continuing ingress.

    This is TEST_ONLY_SOURCEFREE by R03 contract; original35 rights,
    population science and future I03 QUERY issuance are NOT asserted.
    """
    from rawlsing_next.pre553_s04_country_refinement import (
        resolve_r03_v2_issued_sourcefree_role,
    )
    query, predicate, registry, envelope = resolve_r03_v2_issued_sourcefree_role(
        issuance=issuance, operation_id=operation_id,
        query_role=query_role, execution=execution,
    )
    issued = {
        "r03_compilation_hash": issuance.content_hash,
        "r03_workload_envelope_sha256": envelope,
        "r03_operation_id": operation_id,
        "r03_query_role": query_role,
        "permission": "TEST_ONLY_SOURCEFREE_NO_ORIGINAL_SOURCE_GRANT",
    }
    return advance_country_determinicity(
        universe=universe, query=query, predicate=predicate,
        execution=execution, registry=registry, country=country,
        policy=policy, resources=resources,
        observation_channels=observation_channels, prior=prior,
        independently_pinned_prior_ref=independently_pinned_prior_ref,
        resource_sample=resource_sample, current_guard=current_guard,
        issuer_evidence=issued,
    )
