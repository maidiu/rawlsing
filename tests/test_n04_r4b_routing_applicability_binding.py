from rawlsing_next.n04_r4b_routing_applicability_binding import build


def test_n04_r4b_exact_159_routing_accounting():
    records, summary = build()
    assert len(records) == 159
    assert len({row["question_implementation_id"] for row in records}) == 159
    assert all(
        row["routing_state"] == "UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY"
        for row in records
    )
    assert all(row["routing_applicability_ref"] is None for row in records)
    assert all(row["typed_residual"] == "routing_applicability_ref" for row in records)
    assert summary["routing_applicability_refs_bound"] == 0
    assert summary["preserved_state_counts"] == {
        "APPLICABLE_OR_CURRENT_ROUTING_REF_BOUND": 0,
        "GOVERNED_KNOWN_ABSENCE_OR_NONAPPLICABILITY": 0,
        "OUTSIDE_ROUTING_BEARING_JURISDICTION": 0,
        "UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY": 159,
    }
    assert (
        summary["terminal"]
        == "PASS__N04_R4B_159_ROUTING_STATES_ACCOUNTED__"
        "ZERO_APPLICABLE_CURRENT_REFS__159_UNRESOLVED_PRESERVED"
    )
