"""Actual I03 -> source-validated S04 -> NO OBSERVED JOINT -> partial ID.

All data are synthetic sourcefree finite frames. These tests assert only
mathematical inference conditional on a deliberately constructed explicit
common-frame authority. They issue NO original-wave or actor permission.
"""
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot, ExactRef, canonical_json, semantic_hash,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_s04_observed_research import (
    receive_s04_i03_research,
)
from rawlsing_next.pre553_s04_partially_identified_repertoire import (
    BRIDGE_OPERATION, CONTRACT, PartialIdentificationError,
    PartiallyIdentifiedRepertoire, identify_unobserved_overlap,
    ask_partial_repertoire_configuration,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source, _query_authority, _branch_predicate, _query, _run,
    _h, _ref,
)


def _observed(tag, positive_n, n=10):
    rows = [
        {"id": "R" + str(i + 1),
         "responses": {"Y": 1 if i < positive_n else 0}}
        for i in range(n)
    ]
    source = _build_source(tag, rows)
    qa = _query_authority("bridge-" + tag)
    predicate = _branch_predicate(source, qa)
    query = _query(source, qa, predicate, ("Y",), tag="bridge-" + tag)
    execution = _run(source, qa, predicate, query)
    result = receive_s04_i03_research(query=query, execution=execution)
    assert result.material()["state"] == "SUPPORTED_SAMPLE_DESCRIPTIVE"
    return result


def _bridge(left, right, *, modified=None, state="ALLOW"):
    a, b = left.material(), right.material()
    scope = {
        "source_universe_refs": [a["universe_ref"], b["universe_ref"]],
        "release_refs": [a["release_ref"], b["release_ref"]],
        "s04_knowledge_refs": [left.ref.as_dict(), right.ref.as_dict()],
        "risk_set_refs": [a["risk_set_ref"], b["risk_set_ref"]],
        "target_refs": [a["target_refs"][0], b["target_refs"][0]],
        "response_semantics_refs": [
            a["response_semantics_ref"], b["response_semantics_ref"],
        ],
        "measure_basis_refs": [a["measure_basis_ref"], b["measure_basis_ref"]],
        "predicate_refs": [a["predicate_ref"], b["predicate_ref"]],
        "common_frame_ref": _ref("COMMON_FRAME", "synthetic-1972").as_dict(),
        "finite_population_n": 10,
        "frame_period": "SYNTHETIC_1972_FRAME",
        "frame_coverage": "BOTH_COMPLETE_FINITE_FRAME_CENSUS",
        "joint_observation": "NO_RESPONDENT_LINKAGE",
    }
    if modified:
        scope.update(modified)
    auth = AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", "partial-bridge-" + state
        ),
        authority_id="TEST-ONLY-EXPLICIT-COMMON-FINITE-FRAME",
        authority_version="1.0.0",
        authority_content_hash=_h("scope-" + canonical_json(scope) + state),
        authority_kind="SOURCE_UNIVERSE_RELATION",
        decision_state=state,
        governed_operations=(BRIDGE_OPERATION,),
        governed_object_families=("EmpiricalFact@1.0.0",),
        scope_envelope=scope,
        effective_time_or_interval="SYNTHETIC_1972_FRAME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h("test-only-exact-frame"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", "finite-frame"),
    )
    return AuthorityRegistry((auth,)), auth.authority_ref


def _ask(a, b, registry=None, auth=None):
    return identify_unobserved_overlap(
        left=a, right=b, left_event_cell="1", right_event_cell="1",
        authority_registry=registry, common_frame_authority_ref=auth,
    )


def _f(n, d=1):
    return {"numerator": n, "denominator": d}


def test_70_60_sharp_range_is_30_60_not_independence_and_two_distinct_couplings():
    a, b = _observed("partial-a", 7), _observed("partial-b", 6)
    registry, auth = _bridge(a, b)
    receipt = _ask(a, b, registry, auth)
    m = receipt.material()
    assert m["state"] == "SHARP_PARTIAL_IDENTIFICATION_CONDITIONAL_ON_COMMON_FINITE_FRAME"
    assert m["bounds"]["A_AND_B"] == {"lower": _f(3, 10), "upper": _f(3, 5)}
    assert m["bounds"]["A_GIVEN_B"] == {"lower": _f(1, 2), "upper": _f(1)}
    assert m["bounds"]["B_GIVEN_A"] == {"lower": _f(3, 7), "upper": _f(6, 7)}
    assert m["bounds"]["positive_overlap_logically_necessary"] is True
    low, high = (m["countercouplings"][key] for key in (
        "LOWER_EXTREME", "UPPER_EXTREME"
    ))
    assert low == {
        "A_AND_B": _f(3, 10),
        "A_ONLY": _f(2, 5),
        "B_ONLY": _f(3, 10),
        "NEITHER": _f(0),
    }
    assert high == {
        "A_AND_B": _f(3, 5),
        "A_ONLY": _f(1, 10),
        "B_ONLY": _f(0),
        "NEITHER": _f(3, 10),
    }
    assert m["joint_observation_state"] == "NOT_OBSERVED_NO_LINKED_RESPONDENTS"
    assert m["first_consumer_policy"].startswith("NO_FF01_SUPPORTED_JOINT")
    assert "NO_INDEPENDENCE_OR_MAX_ENTROPY_COUPLING_SELECTED" in m["unissued"]
    assert receipt.content_hash == semantic_hash(m)
    assert PartiallyIdentifiedRepertoire(
        receipt.payload_json, receipt.content_hash
    ).material() == m


def test_without_positive_common_frame_bridge_preserve_local_facts_but_no_joint():
    a, b = _observed("without-a", 7), _observed("without-b", 6)
    m = _ask(a, b).material()
    assert m["state"] == "HELD_POPULATION_BRIDGE_UNPROVEN"
    assert m["bounds"] is None
    assert m["countercouplings"] is None
    assert m["marginal_left"]["source_local_raw_fraction"] == _f(7, 10)
    assert m["marginal_right"]["source_local_raw_fraction"] == _f(3, 5)
    assert m["common_frame"] is None


@pytest.mark.parametrize("mutation", [
    {"frame_coverage": "SURVEY_SAMPLES_ESTIMATE_THE_SAME_POPULATION"},
    {"joint_observation": "MATCHED_BY_COUNTRY_LABEL_ONLY"},
    {"finite_population_n": 9},
    {"frame_period": "UNKNOWN"},
    {"s04_knowledge_refs": [
        _ref("S04_REPLACE", "fake").as_dict(),
        _ref("S04_REPLACE", "other").as_dict(),
    ]},
    {"risk_set_refs": [
        _ref("RISK", "foreign-left").as_dict(),
        _ref("RISK", "foreign-right").as_dict(),
    ]},
])
def test_false_common_frame_or_stale_source_cannot_create_numerical_overlap(mutation):
    a, b = _observed("bad-bridge-a", 7), _observed("bad-bridge-b", 6)
    reg, auth = _bridge(a, b, modified=mutation)
    m = _ask(a, b, reg, auth).material()
    assert m["state"] == "HELD_POPULATION_BRIDGE_UNPROVEN"
    assert m["bounds"] is None
    assert m["countercouplings"] is None


def test_negative_source_authority_does_not_convert_a_survey_sample_to_census():
    a, b = _observed("negative-auth-a", 7), _observed("negative-auth-b", 6)
    reg, auth = _bridge(a, b, state="DENY")
    m = _ask(a, b, reg, auth).material()
    assert m["state"] == "HELD_POPULATION_BRIDGE_UNPROVEN"
    assert m["bounds"] is None


def test_different_source_size_even_with_matching_bridge_claim_is_held():
    a, b = _observed("size-a", 7, 10), _observed("size-b", 6, 11)
    reg, auth = _bridge(a, b)
    m = _ask(a, b, reg, auth).material()
    assert m["state"] == "HELD_POPULATION_BRIDGE_UNPROVEN"
    assert m["bounds"] is None


def test_mutated_source_independent_observation_retracts_stale_bridge():
    a, b = _observed("fresh-a", 7), _observed("fresh-b", 6)
    reg, auth = _bridge(a, b)
    replacement = _observed("changed-b", 5)
    m = _ask(a, replacement, reg, auth).material()
    assert m["state"] == "HELD_POPULATION_BRIDGE_UNPROVEN"
    assert m["marginal_right"]["source_local_raw_fraction"] == _f(1, 2)
    assert m["bounds"] is None


def test_weak_association_cannot_be_conjured_from_20_20_marginals():
    a, b = _observed("zero-a", 2), _observed("zero-b", 2)
    reg, auth = _bridge(a, b)
    m = _ask(a, b, reg, auth).material()
    assert m["bounds"]["A_AND_B"] == {"lower": _f(0), "upper": _f(1, 5)}
    assert m["bounds"]["zero_overlap_logically_possible"] is True
    assert m["bounds"]["positive_overlap_logically_necessary"] is False


def test_point_identified_logically_does_not_become_observed_joint():
    a, b = _observed("all-a", 10), _observed("six-b", 6)
    reg, auth = _bridge(a, b)
    m = _ask(a, b, reg, auth).material()
    assert m["bounds"]["A_AND_B"] == {"lower": _f(3, 5), "upper": _f(3, 5)}
    assert m["bounds"]["point_identified_logically_not_observed"] is True
    assert m["joint_observation_state"] == "NOT_OBSERVED_NO_LINKED_RESPONDENTS"


def test_same_source_must_use_actual_i03_joint_not_marginal_cross_join():
    a = _observed("same", 7)
    with pytest.raises(PartialIdentificationError, match="SAME_SOURCE_MUST_USE_ACTUAL"):
        _ask(a, a)


def test_non_domain_response_must_not_be_interpreted_as_a_positive_proposition():
    a, b = _observed("bad-cell-a", 7), _observed("bad-cell-b", 6)
    with pytest.raises(PartialIdentificationError, match="POSITIVE_CELL_NOT_IN_SOURCE_DOMAIN"):
        identify_unobserved_overlap(
            left=a, right=b, left_event_cell="unknown_code", right_event_cell="1"
        )


def test_rehashed_counterfeit_receipt_does_not_pass_cold_readback():
    a, b = _observed("seal-a", 7), _observed("seal-b", 6)
    reg, auth = _bridge(a, b)
    receipt = _ask(a, b, reg, auth)
    m = receipt.material()
    m["bounds"]["A_AND_B"]["lower"] = _f(0)
    with pytest.raises(PartialIdentificationError, match="SEAL_OR_CONTRACT"):
        PartiallyIdentifiedRepertoire(canonical_json(m), receipt.content_hash)



@pytest.mark.parametrize("a_event,b_event,low,high", [
    (True, True, (3, 10), (3, 5)),
    (True, False, (1, 10), (2, 5)),
    (False, True, (0, 1), (3, 10)),
    (False, False, (0, 1), (3, 10)),
])
def test_downstream_compatibility_reader_never_selects_or_generates_coupling(
        a_event, b_event, low, high):
    a, b = _observed("reader-a", 7), _observed("reader-b", 6)
    reg, auth = _bridge(a, b)
    relation = _ask(a, b, reg, auth)
    result = ask_partial_repertoire_configuration(
        relation=relation, event_a=a_event, event_b=b_event
    )
    assert result["state"] == "CONSTRAINT_CALCULATED_FOR_EXACT_FINITE_FRAME"
    assert result["interval"] == {
        "lower": _f(*low), "upper": _f(*high),
    }
    assert result["selected_coupling"] is None
    assert result["not_an_observed_joint_or_person"] is True


def test_downstream_consumer_holds_instead_of_fabricating_couple_configuration():
    a, b = _observed("held-reader-a", 7), _observed("held-reader-b", 6)
    relation = _ask(a, b)
    result = ask_partial_repertoire_configuration(
        relation=relation, event_a=True, event_b=True
    )
    assert result["state"] == "HELD_COMMON_POPULATION_UNPROVEN"
    assert result["configuration_status"] == "UNASSESSABLE_NOT_IMPOSSIBLE"
    assert result["interval"] is None


def test_exact_finite_frame_impossibility_is_not_universal_person_impossibility():
    a, b = _observed("all-left", 10), _observed("other-right", 6)
    reg, auth = _bridge(a, b)
    result = ask_partial_repertoire_configuration(
        relation=_ask(a, b, reg, auth), event_a=False, event_b=True
    )
    assert result["interval"] == {
        "lower": _f(0), "upper": _f(0)
    }
    assert result["configuration_status"] == (
        "NO_OCCURRENCE_COMPATIBLE_WITH_THIS_EXACT_FRAME"
    )
    assert result["source_grade"] == "NO_ORIGINAL_SOURCE_OR_ACTOR_PERMISSION_INFERRED"


def test_compatibility_reader_refuses_nonbinary_selector_or_forged_relation():
    a, b = _observed("bool-a", 7), _observed("bool-b", 6)
    with pytest.raises(PartialIdentificationError, match="EXACT_BINARY"):
        ask_partial_repertoire_configuration(
            relation=_ask(a, b), event_a="yes", event_b=True
        )
