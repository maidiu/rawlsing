"""DHIKR first comparative/contextual reader over the EXISTING I03->S04 joint.

This is a same-case, single-source, RAW-sample, on-demand S04 consumer.
It does not execute C11/I03, pool risks, issue mappings, estimate survey-design
variance, infer causality, or publish a population predictor hierarchy.

The reported conditional-entropy reduction IS an actual descriptive measure
of observed sample dependence, not a claim of psychological determinism.
The bounded recursive frontier explores source-observed contexts while
retaining minorities and contradictions. Bootstrap is an exploratory
IID-resampling sensitivity exercise, explicitly not design uncertainty.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal
from itertools import combinations
import json
from math import isfinite, log2
from random import Random
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonical_json, canonicalize, semantic_hash,
)
from rawlsing_next.pre553_s04_general_joint_algebra import (
    S04GeneralJointWorkspace, S04Projection,
)
from rawlsing_next.pre553_s04_observed_research import (
    receive_s04_i03_research,
)

CONTRACT = "S04_DHIKR_CONDITIONAL_SAMPLE_EXPLORATION@1"
GRADE = "RAW_SOURCE_COHERENT_SAMPLE_ASSOCIATION__PROVISIONAL_METHOD__NO_POPULATION_GRANT"


class DHIKRExplorationError(ValueError):
    """Reject stale source, malformed request, or fabricated comparison."""


@dataclass(frozen=True)
class DHIKRComparisonRequest:
    target_axis: int
    predictor_axes: tuple[int, ...]
    fixed_context: tuple[tuple[int, Any], ...] = ()
    min_branch_n: int = 2
    max_depth: int = 2
    max_nodes: int = 24
    max_interaction_order: int = 3
    bootstrap_replicates: int = 0
    bootstrap_case_cap: int = 4096


@dataclass(frozen=True)
class DHIKRComparisonReceipt:
    payload_json: str
    content_hash: str

    def __post_init__(self):
        try:
            material = json.loads(self.payload_json)
            if (type(material) is not dict or material.get("contract") != CONTRACT
                    or canonical_json(material) != self.payload_json
                    or semantic_hash(material) != self.content_hash):
                raise DHIKRExplorationError("comparative receipt lacks exact identity")
        except (ValueError, TypeError) as exc:
            raise DHIKRExplorationError("invalid comparative receipt") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            CONTRACT,
            "urn:rawlsing:s04:dhikr-sample:sha256:" + self.content_hash,
            self.content_hash,
        )

    def material(self) -> dict[str, Any]:
        return json.loads(self.payload_json)


def _key(value: Any) -> str:
    return canonical_json(canonicalize(value))


def _estimates_to_semantic_material(value: Any) -> Any:
    """Serialize SAMPLE numeric estimates without weakening PRE553 identity.

    Entropy and bootstrap calculations use floating-point arithmetic inside
    this provisional scientific method. Binary floats may NEVER enter
    canonical source/receipt identity. The output decimal is an exact
    serialization of a rounded computational estimate, NOT an exact
    scientific, population, design-variance or causal claim.

    Whole-number estimates retain JSON integer interoperability (0 and 1).
    Nonintegral estimates use PRE553's native $exact_decimal representation.
    Nonfinite results fail closed instead of leaking NaN/Infinity.
    """
    if type(value) is float:
        if not isfinite(value):
            raise DHIKRExplorationError("nonfinite in-sample estimator refused")
        decimal_value = Decimal(str(value))
        if decimal_value == decimal_value.to_integral_value():
            return int(decimal_value)
        return decimal_value
    if isinstance(value, Mapping):
        return {key: _estimates_to_semantic_material(item)
                for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_estimates_to_semantic_material(item) for item in value]
    return value


def read_dhikr_sample_estimate(value: Any) -> Decimal | None:
    """Read a DHIKR estimate explicitly, without weakening source identities.

    Issued computational estimates are either JSON integral numbers or
    PRE553 canonical $exact_decimal material. This is deliberately NOT a
    general-purpose numeric parser: binary floats, booleans, uncanonical
    decimal strings and unrelated source-state objects fail closed.
    """
    if value is None:
        return None
    if type(value) is int:
        return Decimal(value)
    if (type(value) is dict and set(value) == {"$exact_decimal"}
            and type(value["$exact_decimal"]) is str):
        try:
            number = Decimal(value["$exact_decimal"])
        except ArithmeticError as exc:
            raise DHIKRExplorationError("invalid canonical estimate") from exc
        if (not number.is_finite()
                or canonicalize(number) != value):
            raise DHIKRExplorationError("noncanonical or nonfinite estimate")
        return number
    raise DHIKRExplorationError("DHIKR estimate requires issued decimal or integer")


def _seal_dhikr_result(result: dict[str, Any]) -> DHIKRComparisonReceipt:
    """One identity boundary shared by held and supported DHIKR returns."""
    # Source identity and caller conditions were already canonical at their
    # owning S04 ingress. Never launder a future noncanonical source float
    # through the provisional estimator's float-to-decimal output codec.
    for name, source in result.items():
        if name.startswith("source_") or name in (
            "fixed_context", "mapping_edition_dependencies",
            "original_source_authenticity", "source_current_check",
        ):
            canonicalize(source)
    result["sample_estimate_encoding"] = (
        "FINITE_BINARY_COMPUTATION_ROUNDED_TO_DECIMAL_SEMANTIC_MATERIAL__"
        "NOT_EXACT_SCIENTIFIC_ESTIMATION"
    )
    stable = _estimates_to_semantic_material(result)
    # Native canonical_json converts Decimal into $exact_decimal material.
    # Hash THE SAME packed value; no lossy JSON default=float workaround.
    return DHIKRComparisonReceipt(canonical_json(stable), semantic_hash(stable))


def _entropy(counts: Mapping[str, int]) -> float:
    n = sum(counts.values())
    if not n:
        return 0.0
    return -sum((v / n) * log2(v / n) for v in counts.values() if v)


def _association(
    cells: list[tuple[tuple[Any, ...], int]], target: int, axes: tuple[int, ...],
) -> dict[str, Any]:
    """Same-case sample H(Y), H(Y|X), I(Y;X), no smoothing or imputation."""
    target_counts: Counter[str] = Counter()
    group_target: dict[str, Counter[str]] = defaultdict(Counter)
    for row, n in cells:
        if n <= 0:
            continue
        y = _key(row[target])
        x = _key([row[i] for i in axes])
        target_counts[y] += n
        group_target[x][y] += n
    total = sum(target_counts.values())
    if not total:
        return {"raw_n": 0, "target_entropy_bits": None,
                "conditional_entropy_bits": None,
                "information_bits": None, "normalized_reduction": None}
    h = _entropy(target_counts)
    cond = sum(
        sum(counts.values()) / total * _entropy(counts)
        for counts in group_target.values()
    )
    info = max(0.0, h - cond)
    return {
        "raw_n": total,
        "target_entropy_bits": round(h, 12),
        "conditional_entropy_bits": round(cond, 12),
        "information_bits": round(info, 12),
        "normalized_reduction": round(info / h, 12) if h > 0 else None,
    }


def _source_minority(
    cells: list[tuple[tuple[Any, ...], int]],
    target: int, axis: int, *, cap: int = 64,
) -> list[dict[str, Any]]:
    """Exact contradictory configurations relative to their own group modal Y."""
    target_by_value: dict[str, Counter[str]] = defaultdict(Counter)
    original: dict[str, Any] = {}
    target_original: dict[str, Any] = {}
    for row, n in cells:
        if n <= 0:
            continue
        x, y = _key(row[axis]), _key(row[target])
        original[x] = canonicalize(row[axis])
        target_original[y] = canonicalize(row[target])
        target_by_value[x][y] += n
    minority: list[dict[str, Any]] = []
    for x in sorted(target_by_value):
        counts = target_by_value[x]
        maximum = max(counts.values())
        modal = {y for y, n in counts.items() if n == maximum}
        if len(modal) != 1:
            # A tie is a real contradictory context, not an absence of
            # contradiction. It does not license a fake single majority.
            minority.append({
                "predictor_axis": axis,
                "predictor_state": original[x],
                "raw_group_n": sum(counts.values()),
                "tied_modal_target_states": [
                    target_original[y] for y in sorted(modal)
                ],
                "qualification": "TIED_MODAL_TARGETS__NO_UNIQUE_NONMODAL_LABEL",
            })
            continue
        for y in sorted(counts):
            if y not in modal and counts[y]:
                minority.append({
                    "predictor_axis": axis,
                    "predictor_state": original[x],
                    "target_state": target_original[y],
                    "raw_contradictory_n": counts[y],
                    "raw_group_n": sum(counts.values()),
                    "modal_target_state": target_original[next(iter(modal))],
                    "qualification": "NONMODAL_WITHIN_OBSERVED_CONTEXT__NOT_PERSONAL_TRAIT",
                })
    minority.sort(key=lambda v: (
        -v.get("raw_contradictory_n", 0),
        _key(v["predictor_state"]), _key(v.get("target_state"))
    ))
    return minority[:cap]


def _candidate_groups(
    cells: list[tuple[tuple[Any, ...], int]], target: int,
    predictors: tuple[int, ...], max_order: int,
) -> list[tuple[float, float, tuple[int, ...]]]:
    """Exactly the bounded per-axis-normalized priority used in recursion.

    Zero-signal groups are not a discovery result. The groups are exploratory
    same-case sample associations, never a science-issued predictor ranking.
    """
    ordered: list[tuple[float, float, tuple[int, ...]]] = []
    for width in range(1, min(max_order, len(predictors)) + 1):
        for group in combinations(predictors, width):
            signal = _association(cells, target, group)["information_bits"]
            if signal is not None and signal > 1e-12:
                ordered.append((signal / width, signal, group))
    ordered.sort(key=lambda row: (-row[0], -row[1], row[2]))
    return ordered


def _bootstrap_stability(
    cells: list[tuple[tuple[Any, ...], int]],
    target: int, predictors: tuple[int, ...], *,
    repeats: int, case_cap: int, seed: int,
    max_interaction_order: int = 1,
) -> dict[str, Any]:
    """Bounded IID sample sensitivity for BOTH singles and recruited groups.

    Historical single-predictor output is preserved, but the new group
    fractions measure the same per-axis-normalized priority as the recursive
    search. This does NOT correct data-dependent selection or survey design.
    """
    n = sum(c for _, c in cells)
    if repeats == 0:
        return {"state": "NOT_REQUESTED__DESIGN_UNCERTAINTY_NOT_ESTABLISHED"}
    if n == 0:
        return {"state": "ZERO_OBSERVED_CONTEXT_SUPPORT__NO_IID_RESAMPLING",
                "raw_n": 0, "repetitions_completed": 0}
    if n > case_cap:
        return {"state": "HELD_RESOURCE_CAP", "raw_n": n,
                "max_case_n": case_cap, "repetitions_completed": 0}
    if (type(max_interaction_order) is not int
            or not 1 <= max_interaction_order <= 3):
        raise DHIKRExplorationError("bootstrap interaction order must be finite 1..3")
    groups = tuple(
        group
        for width in range(1, min(max_interaction_order, len(predictors)) + 1)
        for group in combinations(predictors, width)
    )
    # Every resample must score ALL candidate groups; avoid accidentally
    # multiplying the original bounded single-predictor budget by 92.
    # Single-predictor case bootstrap was already bounded by 4096 cases,
    # 200 replicates and 8 request axes. Do not withdraw that historical
    # capability merely because an optional interaction method was added.
    # Singleton group scores reuse the already-computed one-axis metrics.
    work = n * repeats * len(groups)
    if max_interaction_order > 1 and work > 2_000_000:
        return {"state": "HELD_GROUP_BOOTSTRAP_WORK_CAP",
                "raw_n": n, "estimated_case_group_evaluations": work,
                "max_case_group_evaluations": 2_000_000,
                "repetitions_completed": 0}
    observed = _candidate_groups(cells, target, predictors, max_interaction_order)
    observed_top = observed[0][2] if observed else None
    observed_by_group = {
        group: _association(cells, target, group)["information_bits"]
        for group in groups
    }
    rng = Random(seed)
    values = [row for row, _ in cells]
    weights = [count for _, count in cells]
    draws_by_predictor: dict[int, list[float]] = {a: [] for a in predictors}
    winner: Counter[int] = Counter()
    group_draws: dict[tuple[int, ...], list[float]] = {
        group: [] for group in groups
    }
    group_winners: Counter[tuple[int, ...]] = Counter()
    group_ties_or_no_signal = 0
    degenerate = 0
    for _ in range(repeats):
        indices = rng.choices(range(len(values)), weights=weights, k=n)
        counts = Counter(indices)
        sampled = [(values[i], count) for i, count in counts.items()]
        single_metrics = {
            axis: _association(sampled, target, (axis,))
            for axis in predictors
        }
        computed = {
            axis: single_metrics[axis]["normalized_reduction"]
            for axis in predictors
        }
        if any(value is None for value in computed.values()):
            degenerate += 1
            continue
        for axis, value in computed.items():
            draws_by_predictor[axis].append(value)
        best = max(computed.values())
        tied = [axis for axis, value in computed.items()
                if abs(value - best) <= 1e-10]
        if len(tied) == 1:
            winner[tied[0]] += 1
        # Interaction units use EXACTLY recursion's priority rule, not the
        # single-axis ranking previously mislabeled as recruitment stability.
        group_priority = {}
        for group in groups:
            bits = (
                single_metrics[group[0]]["information_bits"]
                if len(group) == 1
                else _association(sampled, target, group)["information_bits"]
            )
            score = (bits or 0.0) / len(group)
            group_draws[group].append(score)
            group_priority[group] = score
        top = max(group_priority.values(), default=0.0)
        group_ties = [
            group for group, score in group_priority.items()
            if abs(score - top) <= 1e-10
        ]
        if top <= 1e-12 or len(group_ties) != 1:
            group_ties_or_no_signal += 1
        else:
            group_winners[group_ties[0]] += 1

    def percentile(sorted_scores: list[float], fraction: float) -> float | None:
        if not sorted_scores:
            return None
        i = int((len(sorted_scores) - 1) * fraction)
        return round(sorted_scores[i], 10)

    retained = repeats - degenerate
    return {
        "state": "EXPLORATORY_IID_EMPIRICAL_BOOTSTRAP_NOT_DESIGN_UNCERTAINTY"
                 if retained else "HELD_DEGENERATE_BOOTSTRAP_TARGET",
        "repetitions_requested": repeats,
        "repetitions_with_target_variation": retained,
        "degenerate_target_repetitions": degenerate,
        "seed": seed,
        "max_interaction_order": max_interaction_order,
        "observed_priority_group": list(observed_top) if observed_top else None,
        "group_priority_rule": "IN_SAMPLE_INFORMATION_BITS_PER_GROUP_AXIS",
        "group_tie_or_zero_signal_repetitions": group_ties_or_no_signal,
        "groups": [
            {
                "axes": list(group),
                "observed_information_bits": observed_by_group[group],
                "observed_priority_bits_per_axis": (
                    round(observed_by_group[group] / len(group), 12)
                    if observed_by_group[group] is not None else None
                ),
                "empirical_priority_5_to_95_percentiles": [
                    percentile(sorted(group_draws[group]), 0.05),
                    percentile(sorted(group_draws[group]), 0.95),
                ],
                "unique_top_group_fraction": (
                    round(group_winners[group] / retained, 10)
                    if retained else None
                ),
            }
            for group in groups
        ],
        "predictors": [
            {
                "axis": axis,
                "empirical_5_to_95_percentiles": [
                    percentile(sorted(draws_by_predictor[axis]), 0.05),
                    percentile(sorted(draws_by_predictor[axis]), 0.95),
                ],
                "unique_top_rank_fraction": (
                    round(winner[axis] / retained, 10) if retained else None
                ),
            }
            for axis in predictors
        ],
        "limitation": "IID_CASE_RESAMPLING_ASSUMPTION_UNISSUED__"
                      "POST_SELECTION_BIAS_AND_COMPLEX_SURVEY_DESIGN_NOT_ESTIMATED",
    }


def _validate_request(request: DHIKRComparisonRequest, arity: int, domains):
    if type(request) is not DHIKRComparisonRequest:
        raise DHIKRExplorationError("exact typed DHIKR request required")
    t, axes = request.target_axis, request.predictor_axes
    if (type(t) is not int or not 0 <= t < arity
            or type(axes) is not tuple or not axes
            or len(axes) > 8
            or any(type(a) is not int or not 0 <= a < arity or a == t for a in axes)
            or len(axes) != len(set(axes))):
        raise DHIKRExplorationError("distinct bounded predictors cannot include target")
    if (type(request.fixed_context) is not tuple
            or any(type(p) is not tuple or len(p) != 2 or
                   type(p[0]) is not int or p[0] < 0 or p[0] >= arity
                   or p[0] == t for p in request.fixed_context)
            or len(set(a for a, _ in request.fixed_context)) != len(request.fixed_context)):
        raise DHIKRExplorationError("invalid fixed context or target leakage")
    for a, value in request.fixed_context:
        if _key(value) not in {_key(v) for v in domains[a]}:
            raise DHIKRExplorationError("fixed context outside exact S04 source domain")
    if (type(request.min_branch_n) is not int or request.min_branch_n < 2
            or type(request.max_depth) is not int or not 0 <= request.max_depth <= 5
            or type(request.max_nodes) is not int or not 1 <= request.max_nodes <= 64
            or type(request.max_interaction_order) is not int
            or not 1 <= request.max_interaction_order <= 3
            or type(request.bootstrap_replicates) is not int
            or not 0 <= request.bootstrap_replicates <= 200
            or type(request.bootstrap_case_cap) is not int
            or not 1 <= request.bootstrap_case_cap <= 4096):
        raise DHIKRExplorationError("resource bounds not finite/qualified")


def analyze_s04_dhikr(
    workspace: S04GeneralJointWorkspace, request: DHIKRComparisonRequest,
) -> DHIKRComparisonReceipt:
    """Consume ONLY the existing S04 workspace, with its CURRENT checks."""
    if type(workspace) is not S04GeneralJointWorkspace:
        raise DHIKRExplorationError("existing S04 joint workspace required")
    arity = len(workspace._domains)
    _validate_request(request, arity, workspace._domains)
    # Source-side query verifies exact currentness and reuses the retained
    # same-case positive full joint. No respondent reread or separate count.
    full = workspace.query(S04Projection(tuple(range(arity)), {})).material()
    state = full["state"]
    if state not in ("OBSERVED_FULL_CASE_SUPPORT", "UPSTREAM_SCIENCE_OR_SOURCE_HELD"):
        raise DHIKRExplorationError("unexpected source grade for full joint")
    cells = [
        (tuple(row["output_states"]), row["raw_count"])
        for row in full["complete_output_cells"] if row["raw_count"] > 0
    ]
    if sum(count for _, count in cells) != (
        full["raw_original_full_joint_resolved_n"] if state == "OBSERVED_FULL_CASE_SUPPORT"
        else 0
    ):
        raise DHIKRExplorationError("source sample count changed at DHIKR first consumer")
    seed = int(semantic_hash({
        "knowledge_ref": full["knowledge_ref"],
        "request": {
            "target_axis": request.target_axis,
            "predictor_axes": request.predictor_axes,
            "fixed_context": request.fixed_context,
            "bootstrap_replicates": request.bootstrap_replicates,
        }
    }), 16)
    result: dict[str, Any] = {
        "contract": CONTRACT, "grade": GRADE,
        "state": ("SOURCE_COHERENT_SAMPLE_COMPARISON"
                  if state == "OBSERVED_FULL_CASE_SUPPORT"
                  else "PRODUCER_TYPED_HELD"),
        "source_knowledge_ref": full["knowledge_ref"],
        "source_query_ref": full["source_query_ref"],
        "source_fact_ref": full["source_fact_ref"],
        "source_release_ref": full["source_release_ref"],
        "source_risk_set_ref": full["source_risk_set_ref"],
        "source_response_semantics_ref": full["source_response_semantics_ref"],
        "original_source_authenticity": full["original_source_authenticity"],
        "source_current_check": full["source_current_check"],
        "mapping_edition_dependencies": full["mapping_edition_dependencies"],
        "raw_original_full_joint_n": full["raw_original_full_joint_resolved_n"],
        "target_axis": request.target_axis,
        "predictor_axes": list(request.predictor_axes),
        "fixed_context": [{"axis": a, "value": canonicalize(v)}
                          for a, v in request.fixed_context],
        "max_depth": request.max_depth,
        "max_nodes": request.max_nodes,
        "max_interaction_order": request.max_interaction_order,
        "min_branch_n": request.min_branch_n,
        "nodes": [], "pending_or_budget_excluded": [],
        "source_interpretation": "UNISSUED_ORIGINAL_SOURCE_RIGHTS_AND_MAPPING_EDITION",
        "scientific_ceiling": [
            "IN_SAMPLE_CONDITIONAL_ENTROPY_REDUCTION_NOT_CAUSAL_DETERMINISM",
            "NO_COMPLEX_SURVEY_VARIANCE_OR_POPULATION_RANK_AUTHORITY",
            "EXPLORATORY_ADAPTIVE_CONTEXT_SELECTION_NOT_FAMILYWISE_VALIDATED",
            "BOOTSTRAP_GROUP_RANK_IS_SELECTED_SAMPLE_SENSITIVITY_NOT_POPULATION_INFERENCE",
            "NO_SOURCE_ISSUED_CONTEXT_DISCLOSURE_OR_MINORITY_THEORY",
            "NO_PER_CELL_PERSONAL_MEMBERSHIP_IN_AGGREGATE_S04",
            "NO_INDEPENDENT_ORIGINAL_SOURCE_CURRENTNESS",
            "NO_FF02_OR_PSYCHIC_ACTOR_FACT_EMITTED",
        ],
        "no_new_I03_or_source_reads": True,
        "no_cross_release_risk_pooling": True,
    }
    if result["state"] != "SOURCE_COHERENT_SAMPLE_COMPARISON":
        result["bootstrap_rank_instability"] = {
            "state": "UPSTREAM_HELD__NO_SAMPLE_INFERENCE"}
        workspace.query(S04Projection((), {}))
        return _seal_dhikr_result(result)

    context = tuple((axis, _key(value)) for axis, value in request.fixed_context)
    def selected(context_keys):
        return [(row, count) for row, count in cells if all(
            _key(row[axis]) == value for axis, value in context_keys
        )]

    root_rows = selected(context)
    if not root_rows:
        # A zero in a selected, observed full-case context is neither an
        # impossible configuration nor a statistical comparison.
        result["state"] = "ZERO_OBSERVED_CONTEXT__NO_DHIKR_COMPARISON"
        result["bootstrap_rank_instability"] = {
            "state": "ZERO_OBSERVED_CONTEXT_SUPPORT__NO_IID_RESAMPLING"
        }
        workspace.query(S04Projection((), {}))
        return _seal_dhikr_result(result)
    root_n = sum(count for _, count in root_rows)
    if root_n < request.min_branch_n:
        # A node held below the request's minimum support must not carry an
        # independently non-HELD bootstrap rank in a sibling receipt field.
        result["bootstrap_rank_instability"] = {
            "state": "HELD_BELOW_MIN_BRANCH_N__NO_IID_RANKING",
            "raw_n": root_n,
            "required_min_branch_n": request.min_branch_n,
        }
    elif any(a not in dict(context) for a in request.predictor_axes):
        result["bootstrap_rank_instability"] = _bootstrap_stability(
            root_rows, request.target_axis,
            tuple(a for a in request.predictor_axes if a not in dict(context)),
            repeats=request.bootstrap_replicates,
            case_cap=request.bootstrap_case_cap,
            seed=seed,
            max_interaction_order=request.max_interaction_order,
        )
    else:
        result["bootstrap_rank_instability"] = {
            "state": "NO_UNCONDITIONED_PREDICTOR_LEFT"
        }

    queue = [(context, 0, None)]
    n_processed = 0
    while queue and n_processed < request.max_nodes:
        keys, depth, parent = queue.pop(0)
        data = selected(keys)
        n = sum(count for _, count in data)
        remaining = tuple(a for a in request.predictor_axes if a not in dict(keys))
        scores = []
        if n >= request.min_branch_n:
            for axis in remaining:
                metrics = _association(data, request.target_axis, (axis,))
                scores.append({"axis": axis, **metrics})
        scores.sort(key=lambda v: (
            -(v["information_bits"] or 0), v["axis"]
        ))
        interactions = []
        if n >= request.min_branch_n:
            for a, b in combinations(remaining, 2):
                ia = _association(data, request.target_axis, (a,))["information_bits"]
                ib = _association(data, request.target_axis, (b,))["information_bits"]
                iab = _association(data, request.target_axis, (a, b))["information_bits"]
                interaction = round(iab - ia - ib, 12) if ia is not None and ib is not None and iab is not None else None
                interactions.append({
                    "axes": [a, b], "joint_information_bits": iab,
                    "sample_interaction_information_bits": interaction,
                    "interpretation": (
                        "SAMPLE_SYNERGY__NONCAUSAL" if interaction is not None and interaction > 1e-12
                        else "SAMPLE_REDUNDANCY__NONCAUSAL" if interaction is not None and interaction < -1e-12
                        else "ZERO_OR_UNRESOLVED_SAMPLE_INTERACTION__NONCAUSAL"
                    ),
                })
        frontier_groups = _candidate_groups(
            data, request.target_axis, remaining, request.max_interaction_order
        ) if n >= request.min_branch_n else []
        best = frontier_groups[0] if frontier_groups else None
        split_axis = best[2][0] if best is not None else None
        node_id = len(result["nodes"])
        detail = {
            "node": node_id, "parent": parent, "depth": depth,
            "context": [{"axis": a, "value": canonicalize(
                next(value for value in workspace._domains[a] if _key(value) == key)
            )} for a, key in keys],
            "raw_same_case_n": n,
            "raw_target_counts": [
                {"state": canonicalize(value), "n": sum(
                    count for row, count in data
                    if _key(row[request.target_axis]) == _key(value)
                )}
                for value in workspace._domains[request.target_axis]
            ] if n >= request.min_branch_n else [],
            "target_count_disposition": (
                "OBSERVED_SAMPLE_COUNTS__NOT_POPULATION"
                if n >= request.min_branch_n
                else "HELD_BELOW_MIN_BRANCH_N__NO_CONTEXT_TARGET_DISCLOSURE"
            ),
            "sample_association_scores": scores,
            "pairwise_conditional_interactions": interactions,
            "priority_group": list(best[2]) if best else [],
            "priority_normalized_by_group_size_bits": round(best[0], 12)
            if best else None,
            "minority_contradictions": _source_minority(
                data, request.target_axis, split_axis
            ) if split_axis is not None else [],
            "split_axis": split_axis,
            "terminal_reason": None,
        }
        result["nodes"].append(detail)
        n_processed += 1
        if n < request.min_branch_n:
            detail["terminal_reason"] = "BELOW_MINIMUM_OBSERVED_CONTEXT_N"
            continue
        if depth >= request.max_depth:
            detail["terminal_reason"] = "MAX_DEPTH"
            continue
        if split_axis is None:
            detail["terminal_reason"] = "NO_POSITIVE_IN_SAMPLE_SIGNAL_UP_TO_BOUNDED_INTERACTION_ORDER"
            continue
        observed = {
            _key(row[split_axis]) for row, count in data if count > 0
        }
        if not observed:
            detail["terminal_reason"] = "NO_OBSERVED_SPLIT_STATE"
            continue
        for key in sorted(observed):
            next_context = keys + ((split_axis, key),)
            if len(result["nodes"]) + len(queue) >= request.max_nodes:
                result["pending_or_budget_excluded"].append({
                    "parent": node_id, "axis": split_axis,
                    "value": canonicalize(next(
                        v for v in workspace._domains[split_axis] if _key(v) == key
                    )),
                    "reason": "MAX_NODES_BUDGET_NOT_SEARCHED",
                })
            else:
                queue.append((next_context, depth + 1, node_id))
        if len(queue) == 0:
            detail["terminal_reason"] = "NO_CHILD_WITHIN_BUDGET"

    for keys, depth, parent in queue:
        result["pending_or_budget_excluded"].append({
            "parent": parent, "depth": depth,
            "context_exact_keys": [{"axis": a, "source_state_key": v} for a, v in keys],
            "reason": "MAX_NODES_BUDGET_NOT_SEARCHED",
        })
    result["exploration_state"] = (
        "PARTIAL_BUDGET_BOUNDED" if result["pending_or_budget_excluded"]
        else "BOUNDED_FRONTIER_VISITED__NOT_EXHAUSTIVE_THEORY_SEARCH"
    )
    # CURRENT may have changed during the traversal; recheck without any I03.
    workspace.query(S04Projection((), {}))
    return _seal_dhikr_result(result)


def compare_dhikr_from_i03(
    *, query, execution, request: DHIKRComparisonRequest,
    current_guard=None, interpretation_current=None,
) -> DHIKRComparisonReceipt:
    """Canonical one-machine intake; independent I03 query/result needed."""
    knowledge = receive_s04_i03_research(query=query, execution=execution)
    workspace = S04GeneralJointWorkspace(
        knowledge=knowledge, expected_knowledge_ref=knowledge.ref,
        current_guard=current_guard, interpretation_current=interpretation_current,
    )
    return analyze_s04_dhikr(workspace, request)


__all__ = [
    "CONTRACT", "GRADE", "DHIKRExplorationError", "DHIKRComparisonRequest",
    "DHIKRComparisonReceipt", "analyze_s04_dhikr", "compare_dhikr_from_i03",
    "read_dhikr_sample_estimate",
]
