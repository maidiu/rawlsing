from dataclasses import replace
from types import SimpleNamespace

import pytest

from rawlsing_next.closed35_asian1_realization import (
    ACCEPTED_SOURCE_ROWS,
    ACCEPTED_SOURCE_VARIABLES,
    APPLICABLE_EDGE_CLASSES,
    Asian1RealizationError,
    BOUNDED_UNKNOWN,
    CANONICAL_SHA256,
    CandidateSemanticBinding,
    EXPECTED_Q097_RANKED_SLOTS,
    EXPECTED_WEIGHT_CARRIERS,
    GEOGRAPHY_BINDING,
    Q001_USER_MISSING_98,
    Q018_1_SYSTEM_MISSING,
    R35_HOOK_BINDING,
    R35_REQUIRED_PHYSICAL_DIMENSIONS,
    READER_MODE,
    SOURCE_SPECIFIC_REALIZATION_IDENTITY,
    admit_source_identity,
    make_replay_binding,
    preserve_decoded_text,
    reject_native_id_as_replay_authority,
    require_common_abc_semantic_law,
    require_typed_missing_noncollapse,
    resolve_routing_projection,
    select_default_weight,
    validate_q097_ranked_topology,
    validate_weight_carriers,
)


def test_exact_source_and_big5_reader_are_frozen():
    admit_source_identity(
        source_sha256=CANONICAL_SHA256,
        reader_mode=READER_MODE,
    )

    with pytest.raises(Asian1RealizationError, match="source root mismatch"):
        admit_source_identity(
            source_sha256="0" * 64,
            reader_mode=READER_MODE,
        )

    with pytest.raises(Asian1RealizationError, match="BIG-5 reader mode drift"):
        admit_source_identity(
            source_sha256=CANONICAL_SHA256,
            reader_mode="SAV_NATIVE_GOVERNED",
        )


def test_big5_readability_does_not_mint_documentary_semantics_or_normalization():
    source_text = "source-decoded-text"
    assert preserve_decoded_text(source_text) == source_text

    with pytest.raises(Asian1RealizationError, match="not documentary semantic authority"):
        preserve_decoded_text(
            source_text,
            asserted_documentary_semantic_authority=True,
        )

    with pytest.raises(Asian1RealizationError, match="may not be normalized"):
        preserve_decoded_text(source_text, normalization_requested=True)


def test_source_sha_plus_row_ordinal_not_native_id_is_replay_identity():
    a = make_replay_binding(10, native_country=1, native_idnumber=1)
    b = make_replay_binding(11, native_country=1, native_idnumber=1)
    assert a.replay_key != b.replay_key

    with pytest.raises(Asian1RealizationError, match="source-local attributes"):
        reject_native_id_as_replay_authority(key_fields=("idnumber",))

    with pytest.raises(Asian1RealizationError, match="source-local attributes"):
        reject_native_id_as_replay_authority(key_fields=("country", "idnumber"))


def test_typed_missing_states_preserve_storage_and_declaration_without_semantic_promotion():
    assert Q001_USER_MISSING_98.physical_state == "FORMAT_USER_MISSING_VALUE"
    assert Q001_USER_MISSING_98.stored_value == 98.0
    assert Q001_USER_MISSING_98.declaration == "USER_MISSING_VALUES_98_99"
    assert Q001_USER_MISSING_98.semantic_state == BOUNDED_UNKNOWN

    assert Q018_1_SYSTEM_MISSING.physical_state == "SYSTEM_MISSING"
    assert Q018_1_SYSTEM_MISSING.stored_value is None
    assert Q018_1_SYSTEM_MISSING.semantic_state == BOUNDED_UNKNOWN

    with pytest.raises(Asian1RealizationError, match="cannot be collapsed"):
        require_typed_missing_noncollapse(
            Q001_USER_MISSING_98,
            Q018_1_SYSTEM_MISSING,
            asserted_same_physical_state=True,
        )


def test_routing_cannot_be_inferred_from_missingness_or_decoded_labels():
    a = resolve_routing_projection(
        "q018_1",
        observed_physical_state="SYSTEM_MISSING",
        decoded_label_text="readable label",
    )
    b = resolve_routing_projection(
        "q018_1",
        observed_physical_state="OBSERVED_STORAGE_VALUE",
        decoded_label_text="different readable label",
    )
    assert a == b
    assert "ROUTING_AUTHORITY_NOT_RECOVERED" in a.exact_applicability_state


def test_all_nine_weight_carriers_survive_without_default_or_role_invention():
    assert tuple(x.variable_name for x in EXPECTED_WEIGHT_CARRIERS) == (
        "w_jp",
        "w_hk",
        "w_kr",
        "w_cn",
        "w_mo",
        "w_ph",
        "w_tw",
        "w_th",
        "w_all",
    )
    assert validate_weight_carriers(EXPECTED_WEIGHT_CARRIERS) == EXPECTED_WEIGHT_CARRIERS
    assert all(x.role_or_estimand == BOUNDED_UNKNOWN for x in EXPECTED_WEIGHT_CARRIERS)
    assert all(x.default_use_authorized is False for x in EXPECTED_WEIGHT_CARRIERS)

    with pytest.raises(Asian1RealizationError, match="nine-weight topology drift"):
        validate_weight_carriers(EXPECTED_WEIGHT_CARRIERS[:-1])

    with pytest.raises(Asian1RealizationError, match="no default"):
        select_default_weight()


def test_q097_ranked_slots_are_ordered_and_not_flattened():
    assert validate_q097_ranked_topology(EXPECTED_Q097_RANKED_SLOTS) == EXPECTED_Q097_RANKED_SLOTS

    reordered = (
        EXPECTED_Q097_RANKED_SLOTS[1],
        EXPECTED_Q097_RANKED_SLOTS[0],
        EXPECTED_Q097_RANKED_SLOTS[2],
    )
    with pytest.raises(Asian1RealizationError, match="may not be flattened"):
        validate_q097_ranked_topology(reordered)

    malformed = (
        EXPECTED_Q097_RANKED_SLOTS[0],
        replace(EXPECTED_Q097_RANKED_SLOTS[1], variable_name="q097_1"),
        EXPECTED_Q097_RANKED_SLOTS[2],
    )
    with pytest.raises(Asian1RealizationError, match="may not be flattened"):
        validate_q097_ranked_topology(malformed)


def test_geography_and_identity_remain_source_scoped():
    assert GEOGRAPHY_BINDING["country_carrier"] == "country"
    assert GEOGRAPHY_BINDING["level3_carrier"] == "level3"
    assert GEOGRAPHY_BINDING["cross_wave_recoding_authorized"] is False
    assert GEOGRAPHY_BINDING["instrument_reconciliation_state"] == BOUNDED_UNKNOWN
    assert ACCEPTED_SOURCE_ROWS == 12217
    assert ACCEPTED_SOURCE_VARIABLES == 217


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
    with pytest.raises(Asian1RealizationError, match="semantic realization divergence"):
        require_common_abc_semantic_law(divergent)


def test_s35_edge_scope_and_r35_hooks_are_frozen():
    assert APPLICABLE_EDGE_CLASSES == (
        "EC01",
        "EC02",
        "EC05",
        "EC07",
        "EC09",
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
        "reader_configuration",
        "physical_missing_states",
        "row_replay_identity",
        "ordered_repeated_slot_topology",
        "weight_design_variables",
        "source_local_coordinate_carriers",
    }
    assert R35_HOOK_BINDING["i03_source_scope"]["semantic_authority"] is False
