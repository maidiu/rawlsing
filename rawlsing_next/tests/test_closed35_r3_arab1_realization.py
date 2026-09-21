from types import SimpleNamespace

import pytest

from rawlsing_next.closed35_arab1_realization import (
    APPLICABLE_EDGE_CLASSES,
    BOUNDED_UNKNOWN_SET,
    CANONICAL_FILENAME,
    CANONICAL_SHA256,
    DESIGN_BOUNDED_UNKNOWN,
    DISPLAY_TEXT_TRANSFORM_BOUNDED_UNKNOWN,
    MOROCCO_COUNTRY_CODE,
    R35_HOOK_BINDING,
    R35_REQUIRED_PHYSICAL_DIMENSIONS,
    ROUTING_BOUNDED_UNKNOWN,
    SOURCE_SPECIFIC_REALIZATION_IDENTITY,
    Arab1RealizationError,
    CandidateSemanticBinding,
    NativeRespondentAttribute,
    PhysicalDesignLikeCarrier,
    ReplayIdentity,
    authorize_display_text_transform,
    preserve_design_like_carrier,
    preserve_literal_source_text,
    require_common_abc_semantic_law,
    require_distinct_rows,
    require_wave1_authority_scope,
    resolve_routing,
)


def test_duplicate_ser_is_preserved_and_never_becomes_hard_replay_identity():
    a = NativeRespondentAttribute(ReplayIdentity(CANONICAL_SHA256, 3021), ser=972, country=4)
    b = NativeRespondentAttribute(ReplayIdentity(CANONICAL_SHA256, 3450), ser=972, country=4)
    keys = require_distinct_rows((a, b))
    assert keys == ((CANONICAL_SHA256, 3021), (CANONICAL_SHA256, 3450))
    assert a.ser == b.ser


def test_literal_c1_text_is_preserved_without_typographic_normalization():
    source = "can\u0092t choose"
    assert preserve_literal_source_text(source) == source


def test_display_text_normalization_without_authority_fails_closed():
    source = "can\u0092t choose"
    with pytest.raises(Arab1RealizationError, match=DISPLAY_TEXT_TRANSFORM_BOUNDED_UNKNOWN):
        authorize_display_text_transform(source, "can’t choose")


def test_separately_authorized_display_transform_does_not_rewrite_source_text():
    source = "can\u0092t choose"
    rendered = authorize_display_text_transform(
        source,
        "Can’t Choose/Don’t know",
        authority_id="ARAB_W1_SOURCE_NATIVE_QUESTIONNAIRE_DISPLAY_AUTHORITY",
    )
    assert rendered == "Can’t Choose/Don’t know"
    assert source == "can\u0092t choose"


def test_morocco_routing_distinction_is_document_led():
    non_ma = resolve_routing("q715withoutmorocco", country_code=1)
    ma = resolve_routing("q715withoutmorocco", country_code=MOROCCO_COUNTRY_CODE)
    ma_only = resolve_routing("V715onlymorocco", country_code=MOROCCO_COUNTRY_CODE)

    assert non_ma.status == "DOCUMENTED_APPLICABLE_NON_MOROCCO"
    assert ma.status == "DOCUMENTED_NOT_APPLICABLE_TO_MOROCCO"
    assert ma_only.documented_scope == "MOROCCO_ONLY"
    assert "ALIAS_BINDING_BOUNDED_UNKNOWN" in ma_only.status


def test_missingness_cannot_create_or_change_routing():
    a = resolve_routing(
        "q715withoutmorocco",
        country_code=1,
        observed_missing_state="SYSTEM_MISSING",
    )
    b = resolve_routing(
        "q715withoutmorocco",
        country_code=1,
        observed_missing_state="OBSERVED_STORAGE_VALUE",
    )
    assert a == b
    assert a.missingness_used_as_authority is False


def test_undocumented_routing_remains_bounded_unknown():
    resolution = resolve_routing("Q999_UNDOCUMENTED", observed_missing_state="SYSTEM_MISSING")
    assert resolution.status == ROUTING_BOUNDED_UNKNOWN
    assert resolution.missingness_used_as_authority is False


def test_design_like_carrier_name_or_value_cannot_mint_design_authority():
    carrier = preserve_design_like_carrier(
        "PSU",
        physical_value=17,
        physical_metadata={"label": "primary sampling unit"},
    )
    assert carrier.semantic_state == DESIGN_BOUNDED_UNKNOWN
    assert carrier.survey_design_role_authorized is False
    assert carrier.analytical_weight_authorized is False

    with pytest.raises(Arab1RealizationError, match="no Arab1 weight/design authority"):
        PhysicalDesignLikeCarrier(
            "WT",
            physical_value=1.0,
            analytical_weight_authorized=True,
        )


def test_cross_wave_semantic_leakage_is_rejected():
    require_wave1_authority_scope(
        source_filename=CANONICAL_FILENAME,
        source_sha256=CANONICAL_SHA256,
        authority_wave="W1",
    )
    with pytest.raises(Arab1RealizationError, match="cross-wave semantic leakage"):
        require_wave1_authority_scope(
            source_filename=CANONICAL_FILENAME,
            source_sha256=CANONICAL_SHA256,
            authority_wave="Wave 2",
        )


def test_candidate_specific_semantic_divergence_is_rejected():
    bindings = (
        CandidateSemanticBinding("A"),
        CandidateSemanticBinding("B"),
        CandidateSemanticBinding("C"),
    )
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
    with pytest.raises(Arab1RealizationError, match="semantic realization divergence"):
        require_common_abc_semantic_law(divergent)


def test_s35_edge_scope_r35_hooks_and_bounded_unknown_set_are_frozen():
    assert APPLICABLE_EDGE_CLASSES == ("EC01", "EC07", "EC10", "EC14")
    assert R35_HOOK_BINDING["i01_physical_metadata"]["required"] is True
    assert R35_HOOK_BINDING["i02_derivative_parentage"]["required_for_non_direct_raw"] is True
    assert tuple(R35_HOOK_BINDING["i03_source_scope"]["applicable_edge_classes"]) == APPLICABLE_EDGE_CLASSES
    assert set(R35_REQUIRED_PHYSICAL_DIMENSIONS) >= {
        "physical_metadata",
        "row_replay_identity",
        "native_id_replay_evidence",
        "form_module_skip_routing_carriers",
    }
    assert "CROSS_WAVE_SEMANTIC_EQUIVALENCE" in BOUNDED_UNKNOWN_SET
    assert R35_HOOK_BINDING["i03_source_scope"]["semantic_authority"] is False
