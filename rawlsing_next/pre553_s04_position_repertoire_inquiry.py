"""HAQQMULCH Q019: thin, evidence-qualified position↔repertoire inquiry.

No new estimator, joint, walkback, branching engine, N10E provider, sampler or
S04 cache. It coordinates EXISTING:
  - S04GeneralJointWorkspace conditioned/forward/reverse SAME respondent joint;
  - S04/DHIKR's already-created country-qualified determinicity cycle;
  - N10E/C1 positioned-subject possibility (optional, separately issued);
  - F6 disjoint partial-identification constraint (optional, separate lane).
Only the first two are necessarily related to the same source. F6 NEVER
becomes an observed respondent joint or an alternative sampling distribution.

This is a restricted PYAT sample-descriptive diagnostic, not a public
microdata release, a population estimator or permission for SOROK to
particularize a person. The C4/C5/C6 and N10E consumers own that interface.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from math import prod
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonical_json, canonicalize, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_s04_general_joint_algebra import (
    S04GeneralJointWorkspace, S04Projection,
)
from rawlsing_next.pre553_s04_determinicity_cycle import (
    DeterminicityCycleReceipt,
)
from rawlsing_next.pre553_s04_partially_identified_repertoire import (
    PartiallyIdentifiedRepertoire, ask_partial_repertoire_configuration,
)
from rawlsing_next.pre553_s04_uncertain_repertoire import (
    UncertainRepertoire, ask_uncertain_repertoire_configuration,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    PositionedSubjectPossibilityResult,
)

CONTRACT = "PYAT_HAQQMULCH_S04_POSITION_REPERTOIRE_INQUIRY@1"
GRADE = "RAW_ONE_SOURCE_RESPONDENT_JOINT__SEPARATE_C1_AND_F6_EVIDENCE_LANES"
NOT_ISSUED = (
    "NO_NEW_I03_OR_SOURCE_QUERY",
    "NO_POPULATION_OR_DESIGN_BASED_PROBABILITIES",
    "NO_F6_CROSS_SOURCE_RESPONDENT_COTRAVEL",
    "NO_GENERATED_RESPONDENT_OR_PERSON",
    "NO_C4_C5_C6_OR_N10E_ACTOR_PERMISSION",
    "NO_CAUSAL_DETERMINICITY",
)


class PositionRepertoireInquiryError(ValueError):
    """Mismatch of source/country, provenance, authority or physical budget."""


@dataclass(frozen=True)
class PositionRepertoireRequest:
    target_axis: int
    conditions: tuple[tuple[int, Any], ...] = ()
    joint_position_axes: tuple[int, ...] = ()
    reverse_axes: tuple[int, ...] = ()
    reverse_given_target_value: Any | None = None
    max_projection_cells: int = 2048
    max_result_bytes: int = 250_000
    f6_events: tuple[bool, bool] | None = None

    def __post_init__(self):
        if type(self.target_axis) is not int or self.target_axis < 0:
            raise PositionRepertoireInquiryError("INVALID_TARGET_AXIS")
        if (type(self.conditions) is not tuple
                or any(type(pair) is not tuple or len(pair) != 2 or
                       type(pair[0]) is not int or pair[0] < 0
                       for pair in self.conditions)
                or len({pair[0] for pair in self.conditions}) != len(self.conditions)):
            raise PositionRepertoireInquiryError("INVALID_CONTEXT")
        for sequence in (self.joint_position_axes, self.reverse_axes):
            if (type(sequence) is not tuple
                    or len(set(sequence)) != len(sequence)
                    or any(type(x) is not int or x < 0 for x in sequence)):
                raise PositionRepertoireInquiryError("INVALID_POSITION_AXES")
        if any(type(v) is not int or v < 1 for v in
               (self.max_projection_cells, self.max_result_bytes)):
            raise PositionRepertoireInquiryError("INVALID_PHYSICAL_OR_PRIVACY_BUDGET")
        if self.f6_events is not None and (
                type(self.f6_events) is not tuple
                or len(self.f6_events) != 2
                or any(type(v) is not bool for v in self.f6_events)):
            raise PositionRepertoireInquiryError("F6_EVENT_ROLES_MUST_BE_BOOLEAN_PAIR")
        for _, value in self.conditions:
            canonicalize(value)
        if self.reverse_given_target_value is not None:
            canonicalize(self.reverse_given_target_value)


@dataclass(frozen=True)
class PositionRepertoireInquiry:
    payload_json: str
    digest: str

    def __post_init__(self):
        try:
            m = loads(self.payload_json)
            if (type(m) is not dict or m.get("contract") != CONTRACT
                    or m.get("grade") != GRADE
                    or m.get("not_issued") != list(NOT_ISSUED)
                    or canonical_json(m) != self.payload_json
                    or semantic_hash(m) != self.digest):
                raise PositionRepertoireInquiryError("UNVERIFIED_INQUIRY_SEAL")
        except (TypeError, ValueError) as e:
            raise PositionRepertoireInquiryError("INVALID_INQUIRY_RECEIPT") from e

    @property
    def ref(self) -> ExactRef:
        return ExactRef(CONTRACT, "urn:rawlsing:pyat:position-repertoire:sha256:" + self.digest, self.digest)

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


def _seal(m: dict[str, Any], budget: int) -> PositionRepertoireInquiry:
    packed = canonical_json(m)
    if len(packed.encode("utf-8")) > budget:
        raise PositionRepertoireInquiryError("RESULT_STORAGE_BUDGET_HOLD_NO_FACT_DROPPED")
    return PositionRepertoireInquiry(packed, semantic_hash(m))


def _require_exact_pin(value: Any, pin: ExactRef | None, name: str) -> None:
    if type(pin) is not ExactRef or pin != value.ref:
        raise PositionRepertoireInquiryError(name + "_INDEPENDENT_PIN_REQUIRED")


def _context(pairs: tuple[tuple[int, Any], ...]) -> dict[int, Any]:
    return {axis: canonicalize(value) for axis, value in pairs}


def _same(a: Any, b: Any) -> bool:
    return canonical_json(a) == canonical_json(b)


def _prepared_projection(
    workspace: S04GeneralJointWorkspace, output_axes: tuple[int, ...],
    conditions: Mapping[int, Any], *, cap: int,
):
    # S04 generates the complete domain output: preflight before requesting.
    if (any(type(i) is not int or i < 0 or i >= len(workspace._domains)
            for i in output_axes)
            or len(set(output_axes)) != len(output_axes)):
        raise PositionRepertoireInquiryError("SOURCE_JOINT_OUTPUT_AXES_INVALID")
    cells = prod(len(workspace._domains[i]) for i in output_axes)
    if cells > cap:
        return {
            "state": "HELD_OUTPUT_EXPANSION_BUDGET_NOT_SOURCE_ZERO",
            "proposed_output_cells": cells,
            "source_fact_not_reinterpreted": True,
            "source_projection_ref": None,
            "raw_selected_full_case_n": None,
            "complete_output_cells": [],
        }
    result = workspace.query(S04Projection(output_axes, conditions))
    m = result.material()
    return {
        "state": m["state"],
        "proposed_output_cells": cells,
        "source_projection_ref": result.ref.as_dict(),
        "raw_selected_full_case_n": m["raw_selected_full_case_n"],
        "complete_output_cells": m["complete_output_cells"],
        "source_risk_set_ref": m["source_risk_set_ref"],
        "source_fact_ref": m["source_fact_ref"],
        "original_source_authenticity": m["original_source_authenticity"],
    }


def inquire_position_repertoire(
    *, workspace: S04GeneralJointWorkspace,
    cycle: DeterminicityCycleReceipt,
    independently_pinned_cycle_ref: ExactRef,
    request: PositionRepertoireRequest,
    n10e_possibility: PositionedSubjectPossibilityResult | None = None,
    independently_pinned_n10e_ref: ExactRef | None = None,
    f6_relation: PartiallyIdentifiedRepertoire | None = None,
    independently_pinned_f6_ref: ExactRef | None = None,
    f6_replay_inputs: Mapping[str, Any] | None = None,
    f6_uncertain_relation: UncertainRepertoire | None = None,
    independently_pinned_f6_uncertain_ref: ExactRef | None = None,
    f6_uncertain_replay_inputs: Mapping[str, Any] | None = None,
) -> PositionRepertoireInquiry:
    """Call existing real S04 algebra, attach separately issued owner results.

    Every S04 projection remains same-country and same full-case respondent
    risk. An optional N10E possibility must match *this* source and target.
    F6 is deliberately displayed as separate nonjoint logical evidence.
    """
    if (type(workspace) is not S04GeneralJointWorkspace
            or type(cycle) is not DeterminicityCycleReceipt
            or type(request) is not PositionRepertoireRequest):
        raise PositionRepertoireInquiryError("ACTUAL_SOURCE_OBJECTS_REQUIRED")
    _require_exact_pin(cycle, independently_pinned_cycle_ref, "CYCLE")
    m = cycle.material()
    source = workspace._knowledge.material()
    if (not _same(m["source"]["knowledge_ref"], workspace._knowledge.ref.as_dict())
            or not _same(m["source"]["fact_ref"], source["fact_ref"])
            or not _same(m["source"]["risk_set_ref"], source["risk_set_ref"])
            or not _same(m["source"]["universe_ref"], source["universe_ref"])
            or not _same(m["source"]["query_ref"], source["query_ref"])
            or not _same(m["source"]["release_ref"], source["release_ref"])
            or not _same(m["source"]["response_semantics_ref"],
                         source["response_semantics_ref"])
            or request.target_axis != m["source"]["target_axis"]):
        raise PositionRepertoireInquiryError("DETERMINICITY_SOURCE_COUNTRY_OR_TARGET_DRIFT")
    conditions = _context(request.conditions)
    for axis, value in m["base_context"]:
        if axis not in conditions or not _same(conditions[axis], value):
            raise PositionRepertoireInquiryError("ISSUED_COUNTRY_BASE_CONTEXT_NOT_PRESERVED")
    if (request.target_axis in conditions
            or request.target_axis in request.joint_position_axes
            or request.target_axis in request.reverse_axes
            or any(axis in conditions for axis in request.joint_position_axes)
            or any(axis in conditions for axis in request.reverse_axes)):
        raise PositionRepertoireInquiryError("TARGET_CONDITION_OR_OUTPUT_LEAK")
    # S04's positive jurisdiction and CURRENT checks are inherited, not
    # replicated. A held source yields typed held projectors, never zero.
    forward = _prepared_projection(
        workspace, (request.target_axis,), conditions,
        cap=request.max_projection_cells,
    )
    if forward["state"] == "HELD_OUTPUT_EXPANSION_BUDGET_NOT_SOURCE_ZERO":
        return _seal({
            "contract": CONTRACT, "grade": GRADE,
            "state": "HELD_BASE_TARGET_OUTPUT_BUDGET",
            "source_cycle_ref": cycle.ref.as_dict(),
            "source_workspace_ref": workspace._knowledge.ref.as_dict(),
            "forward": forward, "joint": None, "reverse": None,
            "n10e": None, "f6": None,
            "not_issued": list(NOT_ISSUED),
        }, request.max_result_bytes)

    joint = None
    if request.joint_position_axes:
        joint = _prepared_projection(
            workspace, (request.target_axis,) + request.joint_position_axes,
            conditions, cap=request.max_projection_cells,
        )
    reverse = None
    if request.reverse_axes:
        if request.reverse_given_target_value is None:
            raise PositionRepertoireInquiryError("REVERSE_TARGET_VALUE_REQUIRED")
        reverse_conditions = {**conditions, request.target_axis: canonicalize(
            request.reverse_given_target_value)}
        reverse = _prepared_projection(
            workspace, request.reverse_axes, reverse_conditions,
            cap=request.max_projection_cells,
        )
    elif request.reverse_given_target_value is not None:
        raise PositionRepertoireInquiryError("REVERSE_AXES_REQUIRED")

    n10e = None
    if n10e_possibility is not None:
        if type(n10e_possibility) is not PositionedSubjectPossibilityResult:
            raise PositionRepertoireInquiryError("N10E_OWNER_RECEIPT_REQUIRED")
        _require_exact_pin(n10e_possibility, independently_pinned_n10e_ref, "N10E")
        if (n10e_possibility.source_universe_ref != exact_ref(source["universe_ref"])
                or n10e_possibility.release_ref != exact_ref(source["release_ref"])
                or n10e_possibility.target_ref != exact_ref(
                    source["target_refs"][request.target_axis])):
            raise PositionRepertoireInquiryError("N10E_FOREIGN_SOURCE_OR_TARGET")
        n10e = {
            "source_owner": "EXISTING_C1_N10E_POSITIONED_SUBJECT_PROVIDER",
            "owner_result_ref": n10e_possibility.ref.as_dict(),
            "result_state": n10e_possibility.result_state,
            "exact_disposition": n10e_possibility.exact_disposition,
            "proxy_is_explicit_nonexact": n10e_possibility.proxy is not None,
            "does_not_derive_new_authority_or_actor": True,
        }
    elif independently_pinned_n10e_ref is not None:
        raise PositionRepertoireInquiryError("UNMATCHED_N10E_EXPECTED_PIN")

    # F6 is a separately sourced probability-compatibility lane, never an
    # I03 respondent join. Exact finite-frame and survey-interval authorities
    # have distinct estimands and must never be silently substituted.
    f6 = None
    if f6_relation is not None and f6_uncertain_relation is not None:
        raise PositionRepertoireInquiryError("F6_DISTINCT_ESTIMANDS_MUST_NOT_BE_MERGED")
    if f6_relation is not None:
        if type(f6_relation) is not PartiallyIdentifiedRepertoire:
            raise PositionRepertoireInquiryError("ACTUAL_F6_RELATION_REQUIRED")
        _require_exact_pin(f6_relation, independently_pinned_f6_ref, "F6")
        if request.f6_events is None:
            raise PositionRepertoireInquiryError("F6_EVENT_ROLES_REQUIRED")
        if (f6_uncertain_replay_inputs is not None
                or independently_pinned_f6_uncertain_ref is not None):
            raise PositionRepertoireInquiryError("F6_CROSS_LANE_ARGUMENTS_FORBIDDEN")
        replay_kwargs = {}
        if f6_replay_inputs is not None:
            if (type(f6_replay_inputs) is not dict
                    or set(f6_replay_inputs) != {
                        "left", "right", "left_event_cell", "right_event_cell",
                        "authority_registry", "common_frame_authority_ref",
                    }):
                raise PositionRepertoireInquiryError("F6_EXACT_REPLAY_INPUT_SHAPE_REQUIRED")
            replay_kwargs = dict(f6_replay_inputs)
        calculated = ask_partial_repertoire_configuration(
            relation=f6_relation, event_a=request.f6_events[0],
            event_b=request.f6_events[1], **replay_kwargs,
        )
        f6 = {
            "source_owner": "EXISTING_S04_F6_SEPARATE_COMMON_FRAME",
            "relation_ref": f6_relation.ref.as_dict(),
            "constraint": calculated,
            "not_merged_into_s04_respondent_joint": True,
            "not_a_sampling_probability_or_actor": True,
        }
    elif f6_uncertain_relation is not None:
        if type(f6_uncertain_relation) is not UncertainRepertoire:
            raise PositionRepertoireInquiryError("ACTUAL_F6_UNCERTAIN_RELATION_REQUIRED")
        _require_exact_pin(f6_uncertain_relation, independently_pinned_f6_uncertain_ref, "F6_UNCERTAIN")
        if request.f6_events is None:
            raise PositionRepertoireInquiryError("F6_EVENT_ROLES_REQUIRED")
        if f6_replay_inputs is not None or independently_pinned_f6_ref is not None:
            raise PositionRepertoireInquiryError("F6_CROSS_LANE_ARGUMENTS_FORBIDDEN")
        if (type(f6_uncertain_replay_inputs) is not dict
                or set(f6_uncertain_replay_inputs) != {
                    "left", "right", "left_event_cell", "right_event_cell",
                    "registry", "left_interval_authority",
                    "right_interval_authority", "common_population_authority",
                }):
            raise PositionRepertoireInquiryError("F6_UNCERTAIN_EXACT_REPLAY_INPUTS_REQUIRED")
        calculated = ask_uncertain_repertoire_configuration(
            relation=f6_uncertain_relation, event_a=request.f6_events[0],
            event_b=request.f6_events[1], **f6_uncertain_replay_inputs,
        )
        f6 = {
            "source_owner": "EXISTING_S04_F6_ISSUED_POPULATION_INTERVALS",
            "relation_ref": f6_uncertain_relation.ref.as_dict(),
            "constraint": calculated,
            "not_merged_into_s04_respondent_joint": True,
            "not_a_sampling_probability_or_actor": True,
        }
    elif (request.f6_events is not None
            or independently_pinned_f6_ref is not None
            or f6_replay_inputs is not None
            or independently_pinned_f6_uncertain_ref is not None
            or f6_uncertain_replay_inputs is not None):
        raise PositionRepertoireInquiryError("F6_RELATION_AND_EVENTS_REQUIRED")

    source_joint_grade = (
        "SOURCE_EXACT_RAW_SINGLE_RISK_NO_POPULATION_INFERENCE"
        if forward["state"] == "OBSERVED_FULL_CASE_SUPPORT"
        else "UPSTREAM_HELD_OR_NO_OBSERVED_CASE_NOT_A_POPULATION_IMPOSSIBILITY"
    )
    packet = {
        "contract": CONTRACT, "grade": GRADE,
        "state": "INQUIRY_ASSEMBLED_SEPARATE_AUTHORITY_LANES",
        "source_cycle_ref": cycle.ref.as_dict(),
        "source_workspace_ref": workspace._knowledge.ref.as_dict(),
        "source": {
            "country": m["source"]["country"],
            "source_family": m["source"]["source_family"],
            "wave": m["source"]["wave"],
            "source_query_ref": source["query_ref"],
            "source_fact_ref": source["fact_ref"],
            "source_risk_set_ref": source["risk_set_ref"],
            "unvisited_determinicity_frontier": m["remaining_budgeted_work"],
            "country_qualification": m["country_scope_mode"],
        },
        "request": {
            "target_axis": request.target_axis,
            "conditions": [[axis, value] for axis, value in sorted(conditions.items())],
            "joint_position_axes": list(request.joint_position_axes),
            "reverse_axes": list(request.reverse_axes),
            "reverse_given_target_value": canonicalize(
                request.reverse_given_target_value),
        },
        "forward": forward, "joint": joint, "reverse": reverse,
        "sample_evidence_grade": source_joint_grade,
        "n10e": n10e, "f6": f6,
        "output_cap_applies_per_projection": request.max_projection_cells,
        "source_positive_minorities_not_pruned_by_this_inquiry": True,
        "unsearched_higher_order_patterns_not_declared_absent": True,
        "not_issued": list(NOT_ISSUED),
    }
    return _seal(packet, request.max_result_bytes)


def replay_position_repertoire_inquiry(
    *, expected: PositionRepertoireInquiry,
    independently_pinned_expected_ref: ExactRef,
    **kwargs,
) -> PositionRepertoireInquiry:
    if type(expected) is not PositionRepertoireInquiry:
        raise PositionRepertoireInquiryError("EXACT_PREVIOUS_INQUIRY_REQUIRED")
    _require_exact_pin(expected, independently_pinned_expected_ref, "INQUIRY")
    actual = inquire_position_repertoire(**kwargs)
    if actual.ref != expected.ref:
        raise PositionRepertoireInquiryError("SOURCE_ISSUED_INQUIRY_COLD_REPLAY_CHANGED")
    return actual


__all__ = [
    "CONTRACT", "PositionRepertoireInquiryError", "PositionRepertoireRequest",
    "PositionRepertoireInquiry", "inquire_position_repertoire",
    "replay_position_repertoire_inquiry",
]
