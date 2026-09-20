from dataclasses import replace
from types import SimpleNamespace

import pytest

from rawlsing_next.closed35_asian5_realization import (
    APPLICABLE_EDGE_CLASSES,
    Asian5RealizationError,
    BOUNDED_UNKNOWN,
    CANONICAL_SHA256,
    CandidateSemanticBinding,
    EXPECTED_MR_SETS,
    EXPECTED_Q112_SE15_OVERLAP,
    GEOGRAPHY_BINDING,
    R35_HOOK_BINDING,
    R35_REQUIRED_PHYSICAL_DIMENSIONS,
    SOURCE_SPECIFIC_REALIZATION_IDENTITY,
    WEIGHT_CARRIER,
    admit_source_identity,
    make_replay_binding,
    reject_native_id_as_replay_authority,
    require_common_abc_semantic_law,
    require_no_mr_semantic_alias,
    require_questionnaire_q112_nonidentity,
    resolve_routing_projection,
    select_default_weight,
    validate_native_mr_topology,
)


def test_row_ordinal_not_country_plus_id_is_replay_identity():
    a = make_replay_binding(10, native_country=2, native_idnumber=704273201)
    b = make_replay_binding(11, native_country=2, native_idnumber=704273201)
    assert a.replay_key != b.replay_key
    assert a.native_country == b.native_country
    assert a.native_idnumber == b.native_idnumber

    with pytest.raises(Asian5RealizationError, match="noninjective"):
        reject_native_id_as_replay_authority(key_fields=("COUNTRY", "IDnumber"))


def test_source_sha_drift_fails_closed():
    admit_source_identity(
        source_sha256=CANONICAL_SHA256,
        reader_mode="SAV_NATIVE_GOVERNED",
    )
    with pytest.raises(Asian5RealizationError, match="source root mismatch"):
        admit_source_identity(
            source_sha256="0" * 64,
            reader_mode="SAV_NATIVE_GOVERNED",
        )


def test_exact_three_native_mr_sets_survive_with_exact_overlap():
    validated = validate_native_mr_topology(EXPECTED_MR_SETS)
    assert tuple(x.set_name for x in validated) == ("IR3a", "Q112", "SE15")

    q112 = next(x for x in validated if x.set_name == "Q112")
    se15 = next(x for x in validated if x.set_name == "SE15")
    overlap = tuple(member for member in q112.members if member in set(se15.members))
    assert overlap == EXPECTED_Q112_SE15_OVERLAP
    assert q112.set_name != se15.set_name


def test_mr_flattening_or_member_drift_is_rejected():
    q112 = next(x for x in EXPECTED_MR_SETS if x.set_name == "Q112")
    malformed = (
        EXPECTED_MR_SETS[0],
        replace(q112, members=q112.members[:-1]),
        EXPECTED_MR_SETS[2],
    )
    with pytest.raises(Asian5RealizationError, match="topology drift"):
        validate_native_mr_topology(malformed)

    with pytest.raises(Asian5RealizationError, match="flattening"):
        validate_native_mr_topology(EXPECTED_MR_SETS[:2])


def test_q112_se15_overlap_does_not_mint_alias():
    with pytest.raises(Asian5RealizationError, match="does not authorize"):
        require_no_mr_semantic_alias("Q112", "SE15", asserted_alias=True)


def test_native_q112_name_is_not_questionnaire_q112_semantics():
    with pytest.raises(Asian5RealizationError, match="cannot be identified"):
        require_questionnaire_q112_nonidentity(asserted_same_semantics=True)


def test_india_and_asean_routing_topology_survives_without_missingness_inference():
    india_a = resolve_routing_projection(
        "INDIA_Q106CDE",
        observed_missing_or_sentinel_state=-1,
        native_country_value=18,
    )
    india_b = resolve_routing_projection(
        "INDIA_Q106CDE",
        observed_missing_or_sentinel_state="OBSERVED_VALUE",
        native_country_value=1,
    )
    assert india_a == india_b
    assert india_a.exact_applicability_state == BOUNDED_UNKNOWN

    asean = resolve_routing_projection(
        "ASEAN_Q186",
        observed_missing_or_sentinel_state=-1,
        native_country_value=9,
    )
    assert "EXACT_SOURCE_RISK_SET" in asean.exact_applicability_state


def test_weight_presence_does_not_select_estimand_or_default():
    assert WEIGHT_CARRIER.variable_name == "w"
    assert WEIGHT_CARRIER.role_or_estimand == BOUNDED_UNKNOWN
    assert WEIGHT_CARRIER.default_use_authorized is False
    with pytest.raises(Asian5RealizationError, match="no default"):
        select_default_weight()


def test_geography_remains_source_local_and_unreconciled():
    assert GEOGRAPHY_BINDING["physical_coordinate_authority"] == "RAW_SOURCE_LOCAL_CARRIER"
    assert GEOGRAPHY_BINDING["merged_to_instrument_mapping"] == BOUNDED_UNKNOWN
    assert GEOGRAPHY_BINDING["cross_wave_recoding_authorized"] is False


def test_abc_candidates_share_one_semantic_owner():
    bindings = tuple(CandidateSemanticBinding(c) for c in ("A", "B", "C"))
    assert require_common_abc_semantic_law(bindings) == SOURCE_SPECIFIC_REALIZATION_IDENTITY

    divergent = (
        bindings[0],
        bindings[1],
        SimpleNamespace(
            candidate_id="C",
            source_sha256=CANONICAL_SHA256,
            source_specific_realization_identity="f" * 64,
        ),
    )
    with pytest.raises(Asian5RealizationError, match="semantic realization divergence"):
        require_common_abc_semantic_law(divergent)


def test_s35_edge_scope_and_r35_hooks_are_frozen():
    assert APPLICABLE_EDGE_CLASSES == (
        "EC01",
        "EC07",
        "EC08",
        "EC10",
        "EC12",
        "EC13",
        "EC14",
    )
    assert R35_HOOK_BINDING["i01_physical_metadata"]["required"] is True
    assert R35_HOOK_BINDING["i02_derivative_parentage"]["required_for_non_direct_raw"] is True
    assert tuple(
        R35_HOOK_BINDING["i03_source_scope"]["applicable_edge_classes"]
    ) == APPLICABLE_EDGE_CLASSES
    assert set(R35_REQUIRED_PHYSICAL_DIMENSIONS) >= {
        "row_replay_identity",
        "native_id_replay_evidence",
        "native_mr_sets",
        "form_module_skip_routing_carriers",
        "weight_design_variables",
        "source_local_coordinate_carriers",
    }
    assert R35_HOOK_BINDING["i03_source_scope"]["semantic_authority"] is False
