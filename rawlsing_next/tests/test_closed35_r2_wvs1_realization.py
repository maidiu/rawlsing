from types import SimpleNamespace

import pytest

from rawlsing_next.closed35_wvs1_realization import (
    ACCEPTED_ALL_SYSTEM_COLUMN_COUNT,
    APPLICABLE_EDGE_CLASSES,
    BOUNDED_UNKNOWN,
    CANONICAL_SHA256,
    CandidateSemanticBinding,
    NativeIdentityEvidence,
    R35_HOOK_BINDING,
    R35_REQUIRED_PHYSICAL_DIMENSIONS,
    S007_ACCEPTED_RAW_MAX,
    S007_ACCEPTED_RAW_MIN,
    S007_DISPLAY_FORMAT_SENTINEL,
    SOURCE_SPECIFIC_REALIZATION_IDENTITY,
    WEIGHT_CARRIERS,
    WVS1RealizationError,
    admit_source_identity,
    authorize_weight_selection,
    preserve_all_system_column,
    preserve_native_identity_evidence,
    preserve_raw_display_separation,
    preserve_typed_missingness,
    replay_identity,
    require_common_abc_semantic_law,
    weight_surface,
)


def test_s007_raw_magnitude_survives_f2_display_metadata():
    projected = preserve_raw_display_separation(
        "S007",
        raw_storage_value=320120001,
        display_metadata={"original_variable_type": "F2.0", "storage_width": 8},
        display_rendering="32",
    )
    assert projected.raw_storage_value == 320120001
    assert projected.display_metadata["original_variable_type"] == S007_DISPLAY_FORMAT_SENTINEL
    assert projected.display_rendering == "32"
    assert projected.display_is_raw_value_authority is False
    assert S007_ACCEPTED_RAW_MIN == 320120001
    assert S007_ACCEPTED_RAW_MAX == 8400122325


def test_display_string_cannot_be_substituted_for_s007_raw_storage():
    with pytest.raises(WVS1RealizationError, match="raw storage must remain numeric"):
        preserve_raw_display_separation(
            "S007",
            raw_storage_value="32",
            display_metadata={"original_variable_type": "F2.0"},
            display_rendering="32",
        )


def test_s007_injectivity_does_not_mint_replay_authority():
    evidence = preserve_native_identity_evidence(
        "S007",
        physical_value=320120001,
        source_local_injectivity_observed=True,
    )
    assert evidence.source_local_injectivity_observed is True
    assert evidence.replay_authority is False
    assert evidence.semantic_role == BOUNDED_UNKNOWN

    with pytest.raises(WVS1RealizationError, match="cannot replace"):
        NativeIdentityEvidence(
            variable_name="S007",
            documentary_name="Unified respondent number",
            physical_value=320120001,
            source_local_injectivity_observed=True,
            replay_authority=True,
        )

    hard_key = replay_identity(0)
    assert hard_key.key == f"{CANONICAL_SHA256}:0"


def test_all_system_column_is_retained_and_does_not_gain_semantics():
    projected = preserve_all_system_column(
        "I_WOMPOL",
        row_count=13586,
        system_missing_count=13586,
        declared_user_missing_metadata={"kind": "discrete", "value": -99},
    )
    assert projected.retained is True
    assert projected.semantic_role == BOUNDED_UNKNOWN
    assert projected.routing_applicability_state == BOUNDED_UNKNOWN
    assert ACCEPTED_ALL_SYSTEM_COLUMN_COUNT == 8

    with pytest.raises(WVS1RealizationError, match="requires system_missing_count"):
        preserve_all_system_column(
            "I_WOMPOL",
            row_count=13586,
            system_missing_count=13585,
        )


def test_typed_missing_states_do_not_collapse_or_create_routing():
    user_missing = preserve_typed_missingness(
        "V106",
        physical_state="FORMAT_USER_MISSING_RANGE",
        raw_storage_value=-4,
        missing_declaration={"kind": "range", "lo": -5, "hi": -1},
        documentary_label="Not asked",
    )
    system_missing = preserve_typed_missingness(
        "I_WOMPOL",
        physical_state="SYSTEM_MISSING",
        raw_storage_value=None,
        missing_declaration={"kind": "discrete", "value": -99},
    )

    assert user_missing.physical_state != system_missing.physical_state
    assert user_missing.raw_storage_value == -4
    assert system_missing.raw_storage_value is None
    assert user_missing.semantic_response_state == BOUNDED_UNKNOWN
    assert user_missing.routing_applicability_state == BOUNDED_UNKNOWN
    assert system_missing.semantic_response_state == BOUNDED_UNKNOWN
    assert system_missing.routing_applicability_state == BOUNDED_UNKNOWN

    with pytest.raises(WVS1RealizationError, match="must not be rewritten"):
        preserve_typed_missingness(
            "I_WOMPOL",
            physical_state="SYSTEM_MISSING",
            raw_storage_value=-99,
        )


def test_all_thirteen_weight_carriers_survive_without_default_or_estimand():
    surface = weight_surface()
    assert tuple(item.variable_name for item in surface) == WEIGHT_CARRIERS
    assert len(surface) == 13
    assert all(item.role_state == BOUNDED_UNKNOWN for item in surface)
    assert all(item.design_state == BOUNDED_UNKNOWN for item in surface)
    assert all(item.estimand_state == BOUNDED_UNKNOWN for item in surface)
    assert all(item.selected_by_default is False for item in surface)

    with pytest.raises(WVS1RealizationError, match="no default"):
        authorize_weight_selection(None, authority=None)

    with pytest.raises(WVS1RealizationError, match="explicit source-native"):
        authorize_weight_selection("V236", authority=None)


def test_source_sha_drift_fails_closed():
    assert admit_source_identity(CANONICAL_SHA256) == CANONICAL_SHA256
    with pytest.raises(WVS1RealizationError, match="source root mismatch"):
        admit_source_identity("0" * 64)


def test_v3_remains_source_local_evidence_not_global_identity():
    evidence = preserve_native_identity_evidence(
        "V3",
        physical_value=1,
        source_local_injectivity_observed=False,
    )
    assert evidence.replay_authority is False
    assert evidence.semantic_role == BOUNDED_UNKNOWN


def test_abc_candidates_share_one_source_specific_owner():
    bindings = tuple(CandidateSemanticBinding(candidate) for candidate in ("A", "B", "C"))
    identity = require_common_abc_semantic_law(bindings)
    assert identity == SOURCE_SPECIFIC_REALIZATION_IDENTITY

    divergent = (
        bindings[0],
        bindings[1],
        SimpleNamespace(
            candidate_id="C",
            source_sha256=CANONICAL_SHA256,
            source_specific_realization_identity="f" * 64,
        ),
    )
    with pytest.raises(WVS1RealizationError, match="semantic realization divergence"):
        require_common_abc_semantic_law(divergent)


def test_wvs1_edge_scope_and_r35_hooks_are_frozen_without_semantic_authority():
    assert APPLICABLE_EDGE_CLASSES == ("EC01", "EC04", "EC05", "EC06", "EC12", "EC14")
    assert set(R35_REQUIRED_PHYSICAL_DIMENSIONS) == {
        "physical_metadata",
        "variable_inventory_order",
        "raw_storage_values",
        "row_replay_identity",
        "raw_display_separation",
        "typed_missingness",
        "all_missing_column_retention",
        "weight_design_variables",
    }
    assert R35_HOOK_BINDING["i01_physical_metadata"]["required"] is True
    assert R35_HOOK_BINDING["i01_physical_metadata"]["semantic_authority"] is False
    assert R35_HOOK_BINDING["i02_derivative_parentage"]["required_for_non_direct_raw"] is True
    i03 = R35_HOOK_BINDING["i03_whole_source_physical_equivalence"]
    assert tuple(i03["applicable_edge_classes"]) == APPLICABLE_EDGE_CLASSES
    assert tuple(i03["required_physical_dimensions"]) == R35_REQUIRED_PHYSICAL_DIMENSIONS
    assert i03["semantic_authority"] is False
