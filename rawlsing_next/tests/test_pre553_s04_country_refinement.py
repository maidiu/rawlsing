"""Sourcefree integration falsifiers using REAL C11→I03→S04 objects.

These tests depend on PYAT's inherited test fixture/issuer, not fabricated
S04 dictionary claims. No real original-data grant, survey inference, review
or economic scale is asserted.
"""
import pytest

from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_s04_country_refinement import (
    CountryRefinementError, CountryRequest, RefinementBudget, ResourceSample,
    _has_entailing_country_leaf, _inherited_same_case_information,
    run_issued_country_refinement,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source, _branch_predicate, _query, _query_authority,
    _registry, _ref, _coordinate_leaf,
)


def _real_joint(tag="country-haqq", *, n=8):
    rows = [
        {"id": f"R{i}", "responses": {
            "Y": str(i % 2),
            "X1": str(i % 2),
            "X2": str((i // 2) % 2),
        }}
        for i in range(n)
    ]
    source = _build_source(tag, rows)
    qauth = _query_authority(f"{tag}-query")
    predicate = _branch_predicate(source, qauth, tag=f"{tag}-all")
    query = _query(source, qauth, predicate, ("Y", "X1", "X2"),
                   tag=f"{tag}-joint")
    registry = _registry(source, qauth)
    execution = execute_empirical_query(
        repository=source["repo"], query=query, predicate=predicate,
        authority_registry=registry, release_refs=(source["release_ref"],),
    )
    return dict(
        universe=source["universe"], query=query,
        predicate=predicate, execution=execution, registry=registry,
        source=source,
    )


def _budget(**overrides):
    args = dict(max_input_cells=100, max_cell_visits=1000,
                max_output_cells=100, max_candidates=3,
                wall_seconds=60)
    args.update(overrides)
    return RefinementBudget(**args)


def _request(**overrides):
    args = dict(country="US", source_family="SURVEY", wave="W1")
    args.update(overrides)
    return CountryRequest(**args)


def _run(real, *, request=None, budget=None, candidates=(1, 2),
         target=0, context=None, monitor=None):
    return run_issued_country_refinement(
        universe=real["universe"], query=real["query"],
        predicate=real["predicate"], execution=real["execution"],
        registry=real["registry"], request=request or _request(),
        target_index=target, candidate_indices=candidates,
        context={} if context is None else context,
        budget=budget or _budget(), resource_sample=monitor,
    )


def test_actual_i03_s04_country_fixed_same_risk_candidate_information():
    real = _real_joint()
    out = _run(real)
    assert out["state"] == "COMPLETE_NONCONTROLLING_SCREEN"
    assert out["country_proof_mode"] == "SOURCE_UNIVERSE_COUNTRY"
    assert out["unvisited_candidate_indices"] == []
    assert [x["common_full_case_n"] for x in out["candidate_evidence"]] == [8, 8]
    assert out["candidate_evidence"][0]["unadjusted_mutual_information_bits"] == pytest.approx(1)
    assert out["candidate_evidence"][1]["unadjusted_mutual_information_bits"] == pytest.approx(0)
    assert out["ranking_is_exploratory_not_method_issued"]
    assert not out["original_survey_rights_from_this_adapter"]


def test_gss_style_single_country_does_not_need_dummy_country_axis():
    # Source family is intentionally *not* hardcoded to GSS. A genuinely
    # country-fixed source uses the same path for any source-family identity.
    out = _run(_real_joint("country-constant"))
    assert out["country"] == "US"
    assert out["country_axis"] is None
    assert out["country_proof_mode"] == "SOURCE_UNIVERSE_COUNTRY"


def test_another_country_is_not_pooled_into_us_sample():
    with pytest.raises(CountryRefinementError, match="COORDINATE_ISSUER_REQUIRED"):
        _run(_real_joint("country-wrong"), request=_request(country="DE"))


def test_country_name_cannot_self_issue_metadata_country_semantics():
    with pytest.raises(CountryRefinementError, match="COORDINATE_ISSUER_REQUIRED"):
        _run(_real_joint("country-fake"), request=_request(
            country="DE", country_axis=1))


def test_country_wrong_wave_or_family_is_rejected():
    real = _real_joint("country-wave")
    with pytest.raises(CountryRefinementError, match="SOURCE_WAVE_NOT_EXACT"):
        _run(real, request=_request(wave="W7"))
    with pytest.raises(CountryRefinementError, match="SOURCE_WAVE_NOT_EXACT"):
        _run(real, request=_request(source_family="GSS"))


def test_country_cannot_be_added_as_unsourced_survey_predictor():
    real = _real_joint("country-axis")
    with pytest.raises(CountryRefinementError, match="SOURCE_ALREADY_COUNTRY_SCOPED"):
        _run(real, request=_request(
            country_axis=1, country_coordinate_ref=real["source"]["qrefs"]["X1"]))


def test_budget_stops_after_first_sealed_candidate_and_keeps_unknown():
    out = _run(_real_joint("country-partial"), budget=_budget(max_candidates=1))
    assert out["state"] == "PARTIAL_UNVISITED_UNKNOWN"
    assert [x["index"] for x in out["candidate_evidence"]] == [1]
    assert out["unvisited_candidate_indices"] == [2]
    assert out["stop_reason"] == "CANDIDATE_COUNT_BUDGET"


def test_budget_refuses_unaffordable_full_table_and_does_not_make_negative():
    out = _run(_real_joint("country-no-budget"),
               budget=_budget(max_input_cells=2))
    assert out["state"].startswith("HELD")
    assert out["stop_reason"] == "ISSUED_JOINT_DOMAIN_EXCEEDS_BUDGET_BEFORE_S04"
    assert out["unvisited_candidate_indices"] == [1, 2]
    assert out["source_fact_not_reinterpreted"]


def test_budget_refuses_counted_cell_expansion_without_partial_silent_zero():
    out = _run(_real_joint("country-visits"),
               budget=_budget(max_cell_visits=1))
    assert out["state"].startswith("HELD")
    assert out["stop_reason"] == "JOINT_MATERIALIZATION_CELL_VISITS_OVER_BUDGET"
    assert out["unvisited_candidate_indices"] == [1, 2]


def test_explicit_real_memory_probe_is_required_and_respected():
    real = _real_joint("country-monitor")
    with pytest.raises(CountryRefinementError, match="RESOURCE_MONITOR_REQUIRED"):
        _run(real, budget=_budget(max_rss_bytes=100))
    out = _run(real, budget=_budget(max_rss_bytes=100),
               monitor=lambda: ResourceSample(rss_bytes=101, scratch_bytes=0))
    assert out["state"].startswith("HELD")
    assert out["stop_reason"] == "RESOURCE_LIMIT_BEFORE_S04_MATERIALIZATION"


def test_or_and_not_cannot_fake_predicate_country_entailment():
    real = _real_joint("country-or")
    source = real["source"]
    leaf = _coordinate_leaf(source, "X1", "US") if "X1" in source["crefs"] else {
        "op": "LEAF", "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
        "coordinate_semantic_ref": _ref("COORDINATE_NATIVE", "COUNTRY"),
        "coordinate_authority_ref": source["coord_auth"].authority_ref,
        "operator": "EQ", "exact_value": "US",
    }
    coord = _ref("COORDINATE_NATIVE", "COUNTRY")
    auth = source["coord_auth"].authority_ref
    assert _has_entailing_country_leaf(
        leaf, coordinate=coord, country="US", authority=auth)
    other = {"op": "LEAF", "leaf_type": "DERIVED_BRANCH_COHORT"}
    assert _has_entailing_country_leaf(
        {"op": "AND", "children": (other, leaf)},
        coordinate=coord, country="US", authority=auth)
    assert not _has_entailing_country_leaf(
        {"op": "OR", "children": (other, leaf)},
        coordinate=coord, country="US", authority=auth)
    assert not _has_entailing_country_leaf(
        {"op": "NOT", "children": (leaf,)},
        coordinate=coord, country="US", authority=auth)
    assert not _has_entailing_country_leaf(
        {**leaf, "operator": "IN", "exact_values": ["US", "DE"]},
        coordinate=coord, country="US", authority=auth)


def test_same_risk_source_diagnostic_refuses_target_leakage():
    with pytest.raises(CountryRefinementError, match="TARGET_IS_NOT_ITS_OWN"):
        _run(_real_joint("country-leak"), candidates=(0, 1))


def test_country_raw_information_uses_the_same_existing_dhikr_statistic():
    # Two-category and sparse three-category same-case tables; the country
    # adapter is not permitted to maintain its own alternate MI mathematics.
    from rawlsing_next.pre553_s04_dhikr_comparative import _association

    for table in (
        {("A", "yes"): 5, ("A", "no"): 0,
         ("B", "yes"): 1, ("B", "no"): 6},
        {("A", "y1"): 9, ("A", "y2"): 3,
         ("B", "y1"): 2, ("C", "y3"): 1,
         ("C", "y2"): 0},
    ):
        current = _inherited_same_case_information(table)
        inherited = _association(
            [((x, y), n) for (x, y), n in table.items()],
            target=1, axes=(0,),
        )
        assert current == inherited["information_bits"]
        assert inherited["raw_n"] == sum(table.values())


def test_country_information_negative_counts_are_not_reinterpreted():
    with pytest.raises(CountryRefinementError, match="BAD_SOURCE_COUNT"):
        _inherited_same_case_information({("A", "yes"): 3, ("B", "no"): -1})
    with pytest.raises(CountryRefinementError, match="BAD_SOURCE_COUNT"):
        _inherited_same_case_information({("A", "yes"): True})
    assert _inherited_same_case_information({("A", "yes"): 0}) == 0.0
