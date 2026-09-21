from dataclasses import replace
from types import SimpleNamespace

import pytest

from rawlsing_next.closed35_asian4_realization import (
    APPLICABLE_EDGE_CLASSES,
    Asian4RealizationError,
    BOUNDED_UNKNOWN,
    CANONICAL_SHA256,
    CandidateSemanticBinding,
    EXPECTED_RANKED_FAMILIES,
    GEOGRAPHY_BINDING,
    Q172_ROUTING,
    R35_HOOK_BINDING,
    R35_REQUIRED_PHYSICAL_DIMENSIONS,
    SOURCE_SPECIFIC_REALIZATION_IDENTITY,
    WEIGHT_CARRIERS,
    admit_source_identity,
    make_replay_binding,
    project_ordinary_minus_one,
    reconcile_merged_and_instrument_geography,
    reject_cross_wave_semantic_import,
    reject_global_minus_one_semantics,
    reject_native_id_as_replay_authority,
    require_common_abc_semantic_law,
    require_distinct_weight_carriers,
    require_q172_documentary_scope,
    resolve_q172_row_applicability,
    select_default_weight,
    validate_ranked_slot_topology,
)


def test_source_sha_drift_fails_closed():
    admit_source_identity(
        source_sha256=CANONICAL_SHA256,
        reader_mode="SAV_NATIVE_GOVERNED",
    )
    with pytest.raises(Asian4RealizationError, match="source root mismatch"):
        admit_source_identity(
            source_sha256="0" * 64,
            reader_mode="SAV_NATIVE_GOVERNED",
        )


def test_source_sha_plus_row_ordinal_is_hard_replay_identity():
    a = make_replay_binding(10, native_country=4, native_idnumber=1001)
    b = make_replay_binding(11, native_country=4, native_idnumber=1001)
    assert a.replay_key != b.replay_key
    assert a.native_country == b.native_country
    assert a.native_idnumber == b.native_idnumber

    with pytest.raises(Asian4RealizationError, match="source attributes only"):
        reject_native_id_as_replay_authority(key_fields=("country", "idnumber"))


def test_minus_one_remains_ordinary_storage_not_system_missing():
    projection = project_ordinary_minus_one("q1")
    assert projection.raw_value == -1
    assert projection.physical_state == "OBSERVED_STORAGE_VALUE"
    assert projection.semantic_state.startswith("BOUNDED_UNKNOWN__VARIABLE_LOCAL")

    with pytest.raises(Asian4RealizationError, match="cannot be coerced"):
        project_ordinary_minus_one("q1", physical_state="SYSTEM_MISSING")


def test_minus_one_semantics_cannot_be_globalized():
    reject_global_minus_one_semantics(asserted_semantic_state=BOUNDED_UNKNOWN)
    with pytest.raises(Asian4RealizationError, match="variable-local"):
        reject_global_minus_one_semantics(asserted_semantic_state="NOT_APPLICABLE")


def test_merged_and_instrument_geographies_remain_distinct():
    assert GEOGRAPHY_BINDING["merged_source_carrier"] == "country"
    assert GEOGRAPHY_BINDING["instrument_country_carrier"] == "SE1"
    assert GEOGRAPHY_BINDING["merged_to_instrument_reconciliation"] == BOUNDED_UNKNOWN
    assert GEOGRAPHY_BINDING["cross_wave_harmonization_authorized"] is False
    assert (
        GEOGRAPHY_BINDING["drift_witness"]["merged_codes_3_to_8"]
        != GEOGRAPHY_BINDING["drift_witness"]["instrument_codes_3_to_8"]
    )

    with pytest.raises(Asian4RealizationError, match="may not be harmonized"):
        reconcile_merged_and_instrument_geography()


def test_ranked_slot_topology_is_exact_and_ordered():
    validated = validate_ranked_slot_topology(EXPECTED_RANKED_FAMILIES)
    assert validated[0].slots == ("q20", "q21", "q22")
    assert validated[1].slots == ("q99", "q99a", "q99b")
    assert validated[1].role_authority == (
        "FIRST_RESPONSE",
        "SECOND_RESPONSE_OPTIONAL",
        "THIRD_RESPONSE_OPTIONAL",
    )


def test_ranked_slot_flattening_or_reordering_is_rejected():
    q99 = EXPECTED_RANKED_FAMILIES[1]
    malformed = (
        EXPECTED_RANKED_FAMILIES[0],
        replace(q99, slots=("q99", "q99b", "q99a")),
    )
    with pytest.raises(Asian4RealizationError, match="topology drift"):
        validate_ranked_slot_topology(malformed)

    with pytest.raises(Asian4RealizationError, match="flattening"):
        validate_ranked_slot_topology(EXPECTED_RANKED_FAMILIES[:1])


def test_q172_documented_scope_is_asean_only_without_row_risk_set_invention():
    assert require_q172_documentary_scope("ASEAN_COUNTRIES_ONLY") == "ASEAN_COUNTRIES_ONLY"
    assert Q172_ROUTING.exact_source_risk_set_state.startswith("BOUNDED_UNKNOWN")

    with pytest.raises(Asian4RealizationError, match="beyond the documented"):
        require_q172_documentary_scope("ALL_COUNTRIES")


def test_q172_routing_is_not_inferred_from_missingness_or_country_storage():
    a = resolve_q172_row_applicability(
        native_country_value=9,
        observed_missing_or_sentinel_state=-1,
    )
    b = resolve_q172_row_applicability(
        native_country_value=1,
        observed_missing_or_sentinel_state="OBSERVED_VALUE",
    )
    assert a == b
    assert a.startswith("BOUNDED_UNKNOWN__EXACT_SOURCE_RISK_SET")


def test_w_and_w_cross_remain_distinct_without_default_weight():
    assert tuple(x.variable_name for x in WEIGHT_CARRIERS) == ("w", "w_cross")
    assert all(x.role_or_estimand == BOUNDED_UNKNOWN for x in WEIGHT_CARRIERS)
    assert all(x.default_use_authorized is False for x in WEIGHT_CARRIERS)

    with pytest.raises(Asian4RealizationError, match="distinct source carriers"):
        require_distinct_weight_carriers(asserted_alias=True)

    with pytest.raises(Asian4RealizationError, match="no default"):
        select_default_weight()


def test_cross_wave_semantic_leakage_is_rejected():
    reject_cross_wave_semantic_import("Wave 4")
    with pytest.raises(Asian4RealizationError, match="another Asian Barometer wave"):
        reject_cross_wave_semantic_import("Wave 5")


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
    with pytest.raises(Asian4RealizationError, match="semantic realization divergence"):
        require_common_abc_semantic_law(divergent)


def test_s35_edge_scope_is_exact_without_invented_ec14():
    assert APPLICABLE_EDGE_CLASSES == (
        "EC01",
        "EC05",
        "EC09",
        "EC10",
        "EC12",
        "EC13",
    )
    assert "EC14" not in APPLICABLE_EDGE_CLASSES


def test_r35_hooks_are_physical_only():
    assert R35_HOOK_BINDING["i01_physical_metadata"]["required"] is True
    assert R35_HOOK_BINDING["i02_derivative_parentage"]["required_for_non_direct_raw"] is True
    assert tuple(
        R35_HOOK_BINDING["i03_source_scope"]["applicable_edge_classes"]
    ) == APPLICABLE_EDGE_CLASSES
    assert set(R35_REQUIRED_PHYSICAL_DIMENSIONS) >= {
        "raw_storage_values",
        "physical_missingness",
        "ordered_repeated_slot_topology",
        "form_module_skip_routing_carriers",
        "weight_design_variables",
        "source_local_coordinate_carriers",
    }
    assert R35_HOOK_BINDING["i03_source_scope"]["semantic_authority"] is False
