"""Asked-eligible default: real I03 executor with source-typed nonanswers.

All expected counts are based on sourcefree authority-validated risk sets,
not observed-value selection. Explicit MISSING is not a fabricated event.
"""
from types import SimpleNamespace

import pytest

from rawlsing_next._pre553_query_common import (
    EmpiricalQueryExecutionError, _parse_target_plan, _profile,
)
from rawlsing_next.pre553_asked_eligible_raw_distribution import (
    POLICY, PROFILE_FIELD, STATE_SET,
    AskedEligibleDistributionError, include_asked_eligible_states,
    summarize_asked_eligible_raw_fact,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source, _query_authority, _branch_predicate, _query, _run,
    _registry,
)


def _case(*, absent_event=False, unknown_route=False):
    rows = [
        {"id": "R1", "responses": {"Y": 0}},
        {"id": "R2", "responses": {"Y": 1}},
        {"id": "R3", "responses": {"Y": "98"}},
        {"id": "R4", "responses": {"Y": "99"}},
        {"id": "R5", "responses": {"Y": "source-recorded-no-answer"}},
        {"id": "R6", "responses": {"Y": "97"}},
        # Even a supplied response cannot put a NOT_ASKED respondent in N.
        {"id": "R7", "responses": {"Y": 0}},
    ]
    if absent_event:
        rows.append({"id": "R8", "responses": {}})
    source = _build_source(
        "asked-eligible-raw" + ("-unknown-route" if unknown_route else "")
        + ("-no-event" if absent_event else ""),
        rows,
        risk_sets={"R": {"Y": {
            "R1", "R2", "R3", "R4", "R5", "R6"
        } | ({"R8"} if absent_event else set())}},
        nonmember_routing_state="ROUTING_UNKNOWN" if unknown_route else "NOT_ASKED",
        event_states={
            ("R3", "Y"): "DK",
            ("R4", "Y"): "REFUSAL",
            ("R5", "Y"): "MISSING",
            ("R6", "Y"): "SOURCE_SPECIFIC_SPECIAL",
        },
    )
    qauth = _query_authority("asked-eligible-query")
    predicate = _branch_predicate(source, qauth)
    query = _query(source, qauth, predicate, ("Y",),
                   tag="asked-eligible", asked_eligible_raw=True)
    return source, qauth, predicate, query


def test_native_i03_counts_all_asked_including_nonanswers_not_never_asked():
    source, qa, pred, query = _case()
    assert query.requested_output_grain[PROFILE_FIELD] == POLICY
    assert query.target_arity_and_topology["components"][0]["included_states"] == list(STATE_SET)
    fact = _run(source, qa, pred, query).facts[0]
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 6
    assert fact.raw_numerator_support == 6
    result = summarize_asked_eligible_raw_fact(query=query, fact=fact)
    assert result["state"] == "SOURCE_COHERENT_RAW_ASKED_ELIGIBLE_DISTRIBUTION"
    assert result["asked_eligible_n"] == 6
    assert result["substantive_response_n"] == 2
    cells = result["source_typed_response_counts"]
    assert sum(x["raw_n"] for x in cells) == 6
    by_state = {}
    for item in cells:
        by_state[item["response_state"]] = by_state.get(item["response_state"], 0) + item["raw_n"]
    assert by_state == {
        "SUBSTANTIVE_RESPONSE": 2, "MISSING": 1, "DK": 1,
        "REFUSAL": 1, "SOURCE_SPECIFIC_SPECIAL": 1,
    }
    yes = next(row for row in cells if row["exact_target_cell"] == "1")
    assert yes["asked_share_exact"] == {"numerator": 1, "denominator": 6}
    assert yes["substantive_share_exact"] == {"numerator": 1, "denominator": 2}


def test_asked_but_no_emitted_response_event_remains_held_and_in_denominator():
    source, qa, pred, query = _case(absent_event=True)
    fact = _run(source, qa, pred, query).facts[0]
    assert fact.typed_state == "UNRESOLVED"
    assert fact.raw_denominator_support == 7
    assert fact.raw_numerator_support == 6
    result = summarize_asked_eligible_raw_fact(query=query, fact=fact)
    assert result["state"] == "UPSTREAM_HELD__NO_COMPLETE_DISTRIBUTION"
    assert result["known_condition_true_risk_n"] == 7
    assert result["source_typed_response_counts"] is None
    assert result["asked_eligible_n"] is None


def test_unknown_routing_does_not_mean_asked_and_does_not_mean_not_asked():
    source, qa, pred, query = _case(unknown_route=True)
    with pytest.raises(EmpiricalQueryExecutionError, match="routing/risk-set state is unresolved"):
        _run(source, qa, pred, query)


def test_source_code_98_is_not_magically_recoded_as_dk_without_issuer_evidence():
    rows = [{"id": "R1", "responses": {"Y": "98"}}]
    source = _build_source("asked-98-without-codebook", rows)
    qa = _query_authority("asked-98-without-codebook")
    pred = _branch_predicate(source, qa)
    query = _query(source, qa, pred, ("Y",),
                   tag="asked-98-not-invented", asked_eligible_raw=True)
    with pytest.raises(EmpiricalQueryExecutionError, match="absent from the query-declared full target domain"):
        _run(source, qa, pred, query)


def test_policy_marker_cannot_smuggle_substantive_only_response_domain():
    source, qa, pred, ordinary = _case()
    nonpolicy = _query(source, qa, pred, ("Y",), tag="old-only")
    grain = dict(nonpolicy.requested_output_grain)
    grain[PROFILE_FIELD] = POLICY
    forged = SimpleNamespace(
        requested_output_grain=grain,
        target_arity_and_topology=nonpolicy.target_arity_and_topology,
        target_refs=nonpolicy.target_refs,
    )
    with pytest.raises(EmpiricalQueryExecutionError, match="ASKED_ELIGIBLE_MUST_INCLUDE"):
        _parse_target_plan(forged, _registry(source, qa))
    with pytest.raises(EmpiricalQueryExecutionError, match="ASKED_ELIGIBLE_REQUIRES_RAW"):
        _profile(SimpleNamespace(requested_output_grain={
            **grain, "measure_kind": "GOVERNED_WEIGHTED",
        }))


def test_multi_target_native_i03_uses_same_asked_risk_for_a_typed_nonanswer():
    rows = [
        {"id": "R1", "responses": {"X": 0, "Y": 0}},
        {"id": "R2", "responses": {"X": 1, "Y": "98"}},
        {"id": "R3", "responses": {"X": 0, "Y": "99"}},
    ]
    source = _build_source("asked-joint", rows, event_states={
        ("R2", "Y"): "DK", ("R3", "Y"): "REFUSAL",
    })
    qa = _query_authority("asked-joint")
    pred = _branch_predicate(source, qa)
    query = _query(source, qa, pred, ("X", "Y"),
                   tag="asked-joint", asked_eligible_raw=True)
    fact = _run(source, qa, pred, query).facts[0]
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 3
    assert fact.raw_numerator_support == 3
    cells = fact.target_topology["complete_cell_semantic_projection"]
    assert sum(row["raw_numerator_support"] for row in cells) == 3
    assert any(
        row["cell"] == ["1", {"typed_response_state": "DK"}]
        and row["raw_numerator_support"] == 1
        for row in cells
    )


def test_helper_rejects_unqualified_non_scalar_and_substantive_collision():
    base = {"topology": "SCALAR_SINGULAR", "included_states": ["SUBSTANTIVE_RESPONSE"],
            "domain": ["0", "1"]}
    assert include_asked_eligible_states(base)["included_states"] == list(STATE_SET)
    with pytest.raises(AskedEligibleDistributionError, match="SCALAR_SINGULAR"):
        include_asked_eligible_states({**base, "topology": "ORDERED_SEQUENCE"})
    with pytest.raises(AskedEligibleDistributionError, match="COLLIDES"):
        include_asked_eligible_states({
            **base, "domain": ["0", {"typed_response_state": "DK"}],
        })
