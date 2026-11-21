"""REMONT RMT-Q019: no duplicated estimators or manufactured respondent joins.

Sourcefree only: ACTUAL I03→S04/DHIKR source fixtures; accepted C1/N10E
possibility evaluator is a separate owner; F6 has independently sourced and
authorized finite-frame fixture. First fault, test execution and repairs
belong to REMONT, not this forward-construction author.
"""
import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_s04_observed_research import receive_s04_i03_research
from rawlsing_next.pre553_s04_general_joint_algebra import S04GeneralJointWorkspace
from rawlsing_next.pre553_s04_position_repertoire_inquiry import (
    PositionRepertoireInquiryError, PositionRepertoireRequest,
    inquire_position_repertoire, replay_position_repertoire_inquiry,
)
from rawlsing_next.tests.test_pre553_s04_country_refinement import _real_joint
from rawlsing_next.tests.test_pre553_s04_determinicity_cycle import _advance
from rawlsing_next.tests.test_pre553_s04_partially_identified_repertoire import (
    _observed, _bridge, _ask,
)
from rawlsing_next.tests.test_pre553_s04_uncertain_repertoire import (
    _setup as _uncertain_setup, _invoke as _uncertain_invoke,
)
from rawlsing_next.pre553_s04_partially_identified_repertoire import (
    PartiallyIdentifiedRepertoire, PartialIdentificationError,
)
from rawlsing_next.pre553_empirical_objects import canonical_json, semantic_hash



def _ready(tag="haqqq019"):
    real = _real_joint(tag)
    cycle = _advance(real)
    knowledge = receive_s04_i03_research(query=real["query"], execution=real["execution"])
    workspace = S04GeneralJointWorkspace(
        knowledge=knowledge, expected_knowledge_ref=knowledge.ref,
    )
    return real, cycle, workspace


def _request(**kwargs):
    args = dict(
        target_axis=0, conditions=(), joint_position_axes=(1, 2),
        reverse_axes=(1,), reverse_given_target_value="1",
    )
    args.update(kwargs)
    return PositionRepertoireRequest(**args)


def _inquire(cycle, workspace, *, request=None, **kwargs):
    return inquire_position_repertoire(
        workspace=workspace, cycle=cycle,
        independently_pinned_cycle_ref=cycle.ref,
        request=request or _request(), **kwargs,
    )


def test_inherited_real_i03_s04_forward_joint_and_reverse_conditional_reuse():
    _, cycle, workspace = _ready()
    out = _inquire(cycle, workspace).material()
    assert out["state"] == "INQUIRY_ASSEMBLED_SEPARATE_AUTHORITY_LANES"
    assert out["source"]["country"] == "US"
    assert out["forward"]["raw_selected_full_case_n"] == 8
    assert sum(x["raw_count"] for x in out["forward"]["complete_output_cells"]) == 8
    assert out["joint"]["raw_selected_full_case_n"] == 8
    assert sum(x["raw_count"] for x in out["joint"]["complete_output_cells"]) == 8
    assert out["reverse"]["raw_selected_full_case_n"] == 4
    assert {tuple(x["output_states"]): x["raw_count"]
            for x in out["reverse"]["complete_output_cells"]} == {
        ("0",): 0, ("1",): 4,
    }
    assert out["joint"]["source_fact_ref"] == out["forward"]["source_fact_ref"]
    assert out["joint"]["source_risk_set_ref"] == out["reverse"]["source_risk_set_ref"]
    assert out["source_positive_minorities_not_pruned_by_this_inquiry"]
    assert out["unsearched_higher_order_patterns_not_declared_absent"]
    assert out["n10e"] is None
    assert out["f6"] is None


def test_no_new_i03_and_separately_pinned_cold_replay():
    _, cycle, workspace = _ready("haqqq019-replay")
    args = dict(
        workspace=workspace, cycle=cycle,
        independently_pinned_cycle_ref=cycle.ref,
        request=_request(),
    )
    produced = inquire_position_repertoire(**args)
    replayed = replay_position_repertoire_inquiry(
        expected=produced, independently_pinned_expected_ref=produced.ref,
        **args,
    )
    assert produced.ref == replayed.ref
    assert "NO_NEW_I03_OR_SOURCE_QUERY" in produced.material()["not_issued"]
    with pytest.raises(PositionRepertoireInquiryError, match="INQUIRY_INDEPENDENT_PIN"):
        replay_position_repertoire_inquiry(
            expected=produced,
            independently_pinned_expected_ref=cycle.ref, **args,
        )


def test_low_budget_never_turns_unvisited_joint_into_source_zero():
    _, cycle, workspace = _ready("haqqq019-capped")
    out = _inquire(cycle, workspace, request=_request(
        max_projection_cells=2,
    )).material()
    assert out["forward"]["raw_selected_full_case_n"] == 8
    assert out["joint"]["state"] == "HELD_OUTPUT_EXPANSION_BUDGET_NOT_SOURCE_ZERO"
    assert out["joint"]["complete_output_cells"] == []
    assert out["joint"]["source_fact_not_reinterpreted"]
    assert out["reverse"]["raw_selected_full_case_n"] == 4


def test_country_base_can_not_be_removed_or_another_source_attached():
    _, cycle, workspace = _ready("haqqq019-source")
    _, _, alien_workspace = _ready("haqqq019-other")
    with pytest.raises(PositionRepertoireInquiryError, match="SOURCE_COUNTRY_OR_TARGET"):
        _inquire(cycle, alien_workspace)


def test_wrong_cycle_pin_and_bad_axis_geometry_refused():
    _, cycle, workspace = _ready("haqqq019-refusal")
    with pytest.raises(PositionRepertoireInquiryError, match="CYCLE_INDEPENDENT_PIN"):
        inquire_position_repertoire(
            workspace=workspace, cycle=cycle,
            independently_pinned_cycle_ref=ExactRef(
                "FRAUD", "urn:foreign:fake", "0" * 64,
            ),
            request=_request(),
        )
    with pytest.raises(PositionRepertoireInquiryError, match="TARGET_CONDITION_OR_OUTPUT_LEAK"):
        _inquire(cycle, workspace, request=_request(joint_position_axes=(0,)))
    with pytest.raises(PositionRepertoireInquiryError, match="REVERSE_TARGET_VALUE_REQUIRED"):
        _inquire(cycle, workspace, request=_request(reverse_given_target_value=None))


def test_f6_common_frame_constraints_remain_separate_and_not_sampled():
    _, cycle, workspace = _ready("haqqq019-f6")
    a, b = _observed("haqqq019-marginal-a", 7), _observed("haqqq019-marginal-b", 6)
    reg, auth = _bridge(a, b)
    relation = _ask(a, b, reg, auth)
    out = _inquire(cycle, workspace, request=_request(f6_events=(True, True)),
                   f6_relation=relation,
                   independently_pinned_f6_ref=relation.ref,
                   f6_replay_inputs={
                       "left": a, "right": b,
                       "left_event_cell": "1", "right_event_cell": "1",
                       "authority_registry": reg,
                       "common_frame_authority_ref": auth,
                   }).material()
    assert out["forward"]["raw_selected_full_case_n"] == 8
    assert out["f6"]["constraint"]["interval"] == {
        "lower": {"numerator": 3, "denominator": 10},
        "upper": {"numerator": 3, "denominator": 5},
    }
    assert out["f6"]["not_merged_into_s04_respondent_joint"]
    assert out["f6"]["constraint"]["selected_coupling"] is None
    assert out["joint"]["source_fact_ref"] == out["forward"]["source_fact_ref"]


def test_unqualified_f6_common_frame_is_not_born_as_probability():
    _, cycle, workspace = _ready("haqqq019-f6-held")
    a, b = _observed("haqqq019-held-a", 7), _observed("haqqq019-held-b", 6)
    held = _ask(a, b)
    out = _inquire(cycle, workspace, request=_request(f6_events=(True, False)),
                   f6_relation=held,
                   independently_pinned_f6_ref=held.ref).material()
    assert out["f6"]["constraint"]["state"] == "HELD_COMMON_POPULATION_UNPROVEN"
    assert out["f6"]["constraint"]["interval"] is None
    assert out["forward"]["raw_selected_full_case_n"] == 8


def test_cannot_attach_a_self_described_n10e_field_without_owner_object():
    _, cycle, workspace = _ready("haqqq019-n10e")
    with pytest.raises(PositionRepertoireInquiryError, match="N10E_OWNER_RECEIPT"):
        _inquire(cycle, workspace, n10e_possibility={
            "result_state": "EXACT_SUPPORTED"
        }, independently_pinned_n10e_ref=cycle.ref)


def test_storage_budget_is_a_typed_hold_not_truncated_source_evidence():
    _, cycle, workspace = _ready("haqqq019-retention")
    with pytest.raises(PositionRepertoireInquiryError, match="RESULT_STORAGE_BUDGET_HOLD"):
        _inquire(cycle, workspace, request=_request(max_result_bytes=350))


def test_q019_f6_finite_frame_replay_cannot_be_skipped_or_self_rehashed():
    _, cycle, workspace = _ready("q019-cold-finite-replay")
    a, b = _observed("q019-a", 7), _observed("q019-b", 6)
    reg, auth = _bridge(a, b)
    relation = _ask(a, b, reg, auth)
    with pytest.raises(PartialIdentificationError, match="F6_EXACT_SOURCE_AND_AUTHORITY_REPLAY_REQUIRED"):
        _inquire(cycle, workspace, request=_request(f6_events=(True, True)),
                 f6_relation=relation, independently_pinned_f6_ref=relation.ref)
    m = relation.material()
    m["bounds"]["A_AND_B"]["lower"] = {"numerator": 0, "denominator": 1}
    forged = PartiallyIdentifiedRepertoire(canonical_json(m), semantic_hash(m))
    with pytest.raises(PartialIdentificationError, match="F6_SOURCE_AND_ISSUER_REPLAY_MISMATCH"):
        _inquire(cycle, workspace, request=_request(f6_events=(True, True)),
                 f6_relation=forged, independently_pinned_f6_ref=forged.ref,
                 f6_replay_inputs={
                     "left": a, "right": b,
                     "left_event_cell": "1", "right_event_cell": "1",
                     "authority_registry": reg,
                     "common_frame_authority_ref": auth,
                 })


def test_q020_existing_inquiry_reads_issued_interval_f6_without_a_fake_joint():
    _, cycle, workspace = _ready("q020-inquiry-interval")
    fixture = _uncertain_setup(a_n=10, b_n=13)
    relation = _uncertain_invoke(fixture)
    a, b, reg, la, ra, bridge = fixture
    answer = _inquire(
        cycle, workspace,
        request=_request(f6_events=(True, True)),
        f6_uncertain_relation=relation,
        independently_pinned_f6_uncertain_ref=relation.ref,
        f6_uncertain_replay_inputs={
            "left": a, "right": b,
            "left_event_cell": "1", "right_event_cell": "1",
            "registry": reg,
            "left_interval_authority": la,
            "right_interval_authority": ra,
            "common_population_authority": bridge,
        },
    ).material()
    assert answer["state"] == "INQUIRY_ASSEMBLED_SEPARATE_AUTHORITY_LANES"
    assert answer["f6"]["source_owner"] == "EXISTING_S04_F6_ISSUED_POPULATION_INTERVALS"
    assert answer["f6"]["constraint"]["interval"] == {
        "lower": {"numerator": 1, "denominator": 10},
        "upper": {"numerator": 7, "denominator": 10},
    }
    assert answer["f6"]["constraint"]["selected_coupling"] is None
    assert answer["f6"]["constraint"]["person_or_respondent_created"] is False
    assert answer["f6"]["not_merged_into_s04_respondent_joint"]
    assert answer["joint"]["source_fact_ref"] == answer["forward"]["source_fact_ref"]


def test_q020_f6_distinct_estimands_no_cross_lane_and_revoked_issuer_no_probability():
    _, cycle, workspace = _ready("q020-cross-lane")
    a, b = _observed("q020-a", 7), _observed("q020-b", 6)
    reg, auth = _bridge(a, b)
    finite = _ask(a, b, reg, auth)
    fixture = _uncertain_setup()
    issued = _uncertain_invoke(fixture)
    with pytest.raises(PositionRepertoireInquiryError, match="F6_DISTINCT_ESTIMANDS"):
        _inquire(
            cycle, workspace, request=_request(f6_events=(True, True)),
            f6_relation=finite, independently_pinned_f6_ref=finite.ref,
            f6_uncertain_relation=issued,
            independently_pinned_f6_uncertain_ref=issued.ref,
        )
    ua, ub, ureg, la, ra, bridge = fixture
    with pytest.raises(PositionRepertoireInquiryError, match="F6_UNCERTAIN_EXACT_REPLAY_INPUTS_REQUIRED"):
        _inquire(
            cycle, workspace, request=_request(f6_events=(True, True)),
            f6_uncertain_relation=issued, independently_pinned_f6_uncertain_ref=issued.ref,
        )
    from rawlsing_next.pre553_s04_uncertain_repertoire import UncertainRepertoireError
    with pytest.raises(UncertainRepertoireError, match="UNCERTAIN_REPERTOIRE_SOURCE_REPLAY_FAILED"):
        _inquire(
            cycle, workspace, request=_request(f6_events=(True, True)),
            f6_uncertain_relation=issued, independently_pinned_f6_uncertain_ref=issued.ref,
            f6_uncertain_replay_inputs={
                "left": ua, "right": ub,
                "left_event_cell": "1", "right_event_cell": "1",
                "registry": ureg,
                "left_interval_authority": la,
                "right_interval_authority": ra,
                "common_population_authority": None,
            },
        )
