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

from dataclasses import dataclass
from decimal import Decimal
from itertools import combinations
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


class DeterminicityCycleError(ValueError):
    """Country, source, budget, replay or scientific-claim boundary refused."""


@dataclass(frozen=True)
class CyclePolicy:
    target_axis: int
    predictor_axes: tuple[int, ...]
    fixed_context: tuple[tuple[int, Any], ...]
    min_branch_n: int
    max_depth: int
    max_total_nodes: int
    max_pending_nodes: int
    max_new_nodes_per_call: int
    max_receipt_bytes: int
    max_pair_order: int = 2
    bootstrap_replicates: int = 0
    bootstrap_case_cap: int = 4096
    min_signal_bits: str = "0.0"  # canonical decimal; method tolerance, not physics

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
                self.min_branch_n, self.max_total_nodes, self.max_pending_nodes,
                self.max_new_nodes_per_call, self.max_receipt_bytes,
                self.bootstrap_case_cap)):
            raise DeterminicityCycleError("INVALID_CYCLE_LIMIT")
        if (type(self.max_depth) is not int or self.max_depth < 0
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
    require_positive_authority(
        snap, authority_kind="COORDINATE_SEMANTICS",
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


def _revive_deferred(m: dict[str, Any], domains: Sequence[Sequence[Any]],
                     max_pending: int) -> None:
    """Store one range cursor rather than silently dropping source branches."""
    while m["deferred"] and len(m["frontier"]) < max_pending:
        item = m["deferred"][0]
        axis = item["axis"]
        nxt = item["next_index"]
        domain = domains[axis]
        if nxt >= len(domain):
            m["deferred"].pop(0)
            continue
        ctx = _ctx(item["context"])
        ctx[axis] = domain[nxt]
        m["frontier"].append({
            "context": _serialize_context(ctx),
            "depth": item["depth"], "parent": item["parent"],
        })
        item["next_index"] += 1


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
        "country": country.country, "country_mode": mode,
        "country_native_value": canonicalize(country_value),
        "policy": {
            **{key: value for key, value in vars(policy).items()
               if key not in ("fixed_context", "min_signal_bits")},
            "fixed_context": _serialize_context(context),
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
    if m_source["state"] != "SUPPORTED_SAMPLE_DESCRIPTIVE":
        state["stopping_reason"] = "UPSTREAM_TYPED_HELD_NOT_A_NEGATIVE_ANSWER"
        return _seal(state, policy.max_receipt_bytes)
    domains = m_source["target_domains"]
    for axis, value in context.items():
        if _key(value) not in {_key(v) for v in domains[axis]}:
            raise DeterminicityCycleError("CONDITION_OUTSIDE_EXACT_DOMAIN")
    positive = [(tuple(row["cell"]), row["raw_count"])
                for row in m_source["complete_cells"] if row["raw_count"] > 0]
    used = domain_cells
    processed_axes = 0
    completed_this_call = 0
    stop = "NO_PENDING_WORK"
    # This controls exploration. Every batch is an actual DHIKR single-node
    # inquiry; existing entropy/interaction/minority code remains the owner.
    while True:
        if completed_this_call >= policy.max_new_nodes_per_call:
            stop = "CALL_NODE_BUDGET"; break
        if state["completed_nodes"] >= policy.max_total_nodes:
            stop = "TOTAL_NODE_BUDGET_WITH_UNSEARCHED_FRONTIER"; break
        _revive_deferred(state, domains, policy.max_pending_nodes)
        if state["active"] is None:
            if not state["frontier"]:
                stop = "EXPLORATION_FRONTIER_COMPLETE"; break
            node = state["frontier"].pop(0)
            state["active"] = {
                **node, "next_predictor_offset": 0,
                "candidate_screens": [], "batch_groups": [],
                "raw_target_counts": None, "raw_n": None,
            }
        active = state["active"]
        selected = _ctx(active["context"])
        available = [a for a in policy.predictor_axes if a not in selected]
        cursor = active["next_predictor_offset"]
        if cursor < len(available) and processed_axes < resources.max_candidates:
            batch = tuple(available[cursor:cursor + min(
                MAX_DHIKR_BATCH, resources.max_candidates - processed_axes,
            )])
            # Conservative workload prediction: DHIKR scores all singles,
            # all pairs and a bounded candidate-group frontier. Bootstrap
            # resampling adds n*repetitions*group evaluations.
            k = len(batch)
            pairs = comb(k, 2) if policy.max_pair_order == 2 else 0
            cases = len(positive)
            estimated = cases * (8 + 8*k + 8*pairs)
            estimated += (policy.bootstrap_replicates * min(
                policy.bootstrap_case_cap, m_source["raw_fully_resolved_joint_n"]
            ) * (k + pairs))
            if (used + estimated > resources.max_cell_visits
                    or not _resource_ok(deadline=deadline, budget=resources,
                                        resource_sample=resource_sample)):
                stop = "HOST_COST_OR_DEADLINE_BEFORE_NEXT_DHIKR_BATCH"; break
            req = DHIKRComparisonRequest(
                target_axis=policy.target_axis, predictor_axes=batch,
                fixed_context=tuple(sorted(selected.items())),
                min_branch_n=policy.min_branch_n, max_depth=0, max_nodes=1,
                max_interaction_order=policy.max_pair_order,
                bootstrap_replicates=policy.bootstrap_replicates,
                bootstrap_case_cap=policy.bootstrap_case_cap,
            )
            result = analyze_s04_dhikr(workspace, req).material()
            used += estimated
            processed_axes += k
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
            if active["next_predictor_offset"] < len(available):
                continue
        if active["next_predictor_offset"] < len(available):
            stop = "PREDICTOR_BATCH_BUDGET_UNSEARCHED"; break

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
            "cross_batch_interactions": "NOT_SEARCHED",
            "missingness_for_unspecified_axes": "NOT_ISSUED",
            "bootstrap_uncertainty": "EXPLORATORY_IID_ONLY__NO_DESIGN_VARIANCE",
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
            _revive_deferred(next_state, domains, policy.max_pending_nodes)
        if len(canonical_json(next_state).encode("utf-8")) > policy.max_receipt_bytes:
            stop = "RECEIPT_STORAGE_BUDGET_CURRENT_NODE_UNCOMMITTED"; break
        state = next_state
        completed_this_call += 1
    state["total_estimated_cell_visits"] += used
    state["last_call_estimated_cell_visits"] = used
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
    node_id: int,
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
            or type(node_id) is not int):
        raise DeterminicityCycleError("INDEPENDENT_RECEIPT_AND_WORKSPACE_REQUIRED")
    m = receipt.material()
    if (m["source"]["knowledge_ref"] != workspace._knowledge.ref.as_dict()
            or not 0 <= node_id < len(m["nodes"])):
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
