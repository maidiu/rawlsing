from rawlsing_next.pre553_r5_oracle import control_results, hostile_microfixture, independent_query


def test_mandatory_oracle_controls_reject_destructive_and_accept_benign_relayout():
    result = control_results()
    assert result == {
        "aggregate_preserving_respondent_permutation": True,
        "compensating_event_drop_duplicate": True,
        "one_field_omission": True,
        "negative_state_flattening": True,
        "self_consistent_destructive_rehash": True,
        "benign_physical_relayout": True,
    }


def test_independent_query_is_identity_and_risk_sensitive():
    fixture = hostile_microfixture()
    result = independent_query(fixture, question="q1", state="SUBSTANTIVE", require_eligible=True)
    assert result["matching_event_ids"] == ("e1",)
    assert "r4" not in result["governed_respondents"]
