from types import SimpleNamespace

import pytest

from rawlsing_next.closed35_lat2011_realization import (
    ACCEPTED_PACKET_ROW_COUNT,
    APPLICABLE_EDGE_CLASSES,
    CANONICAL_SHA256,
    COUNTRY_SAMPLE_COUNTS,
    CandidateSemanticBinding,
    FORBIDDEN_CROSS_WAVE_SPECIAL_LAWS,
    LAT2011RealizationError,
    NATIVE_IDENTITY_ATTRIBUTE_LAW,
    NO_AGGREGATE_ESTIMAND,
    R35_HOOK_BINDING,
    R35_REQUIRED_PHYSICAL_DIMENSIONS,
    SOURCE_SPECIFIC_REALIZATION_IDENTITY,
    admit_physical_incidence,
    bind_weight_carrier,
    preserve_physical_cell,
    reject_cross_wave_special_law,
    replay_identity,
    require_common_abc_semantic_law,
    source_local_variable_identity,
    source_specific_realization_payload,
    validate_country_structure,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState


def _synthetic_incidence(source_sha=CANONICAL_SHA256, **overrides):
    reader = {
        "reader": "pyreadstat",
        "reader_version": "1.3.6",
        "user_missing": True,
        "apply_value_formats": False,
        "encoding": None,
        "authority_status": None,
    }
    reader.update(overrides)
    return SimpleNamespace(
        source_sha256=source_sha,
        source_format="SAV",
        reader_configuration=reader,
    )


def test_exact_source_root_and_native_reader_config_are_required():
    admission = admit_physical_incidence(_synthetic_incidence())
    assert admission.source_sha256 == CANONICAL_SHA256
    assert admission.whole_source_physical_equivalence_qualified is False

    with pytest.raises(LAT2011RealizationError, match="source root mismatch"):
        admit_physical_incidence(_synthetic_incidence(source_sha="0" * 64))

    with pytest.raises(LAT2011RealizationError, match="reader/config drift"):
        admit_physical_incidence(_synthetic_incidence(encoding="latin1"))


def test_replay_identity_is_only_source_sha_plus_preserved_row_ordinal():
    first = replay_identity(17)
    same = replay_identity(17)
    other = replay_identity(18)

    assert first == same
    assert first != other
    assert first.source_sha256 == CANONICAL_SHA256
    assert first.row_ordinal == 17
    assert set(first.__dict__) == {"source_sha256", "row_ordinal"}
    assert NATIVE_IDENTITY_ATTRIBUTE_LAW.replay_identity_authorized is False
    assert NATIVE_IDENTITY_ATTRIBUTE_LAW.durable_cross_release_identity_authorized is False


def test_source_local_variable_identity_never_becomes_family_wide_identity():
    identity = source_local_variable_identity("P2ST", 37)
    assert identity.source_sha256 == CANONICAL_SHA256
    assert identity.variable_name == "P2ST"
    assert identity.variable_ordinal == 37


def test_exact_18_country_structure_is_frozen_from_accepted_packet():
    result = validate_country_structure(COUNTRY_SAMPLE_COUNTS)
    assert len(result) == 18
    assert sum(result.values()) == ACCEPTED_PACKET_ROW_COUNT

    drifted = dict(COUNTRY_SAMPLE_COUNTS)
    drifted["76"] -= 1
    with pytest.raises(LAT2011RealizationError, match="country-coordinate/sample structure drift"):
        validate_country_structure(drifted)


def test_physical_user_missing_and_system_missing_remain_distinct():
    declaration = {"kind": "range", "lo": -9, "hi": -1}
    user_missing = PhysicalCell(
        row_ordinal=479,
        variable_ordinal=36,
        variable_name="P1ST",
        raw_value=-2,
        missing_state=PhysicalMissingState.FORMAT_USER_MISSING_RANGE,
        source_missing_declaration=declaration,
    )
    system_missing = PhysicalCell(
        row_ordinal=480,
        variable_ordinal=36,
        variable_name="P1ST",
        raw_value=None,
        missing_state=PhysicalMissingState.SYSTEM_MISSING,
        source_missing_declaration=None,
    )

    user_witness = preserve_physical_cell(user_missing)
    system_witness = preserve_physical_cell(system_missing)

    assert user_witness.raw_value == -2
    assert user_witness.missing_state == "FORMAT_USER_MISSING_RANGE"
    assert user_witness.source_missing_declaration == declaration
    assert system_witness.raw_value is None
    assert system_witness.missing_state == "SYSTEM_MISSING"
    assert system_witness.source_missing_declaration is None
    assert user_witness != system_witness


def test_wt_is_preserved_without_synthesizing_an_aggregate_estimand_or_default():
    wt = PhysicalCell(
        row_ordinal=1,
        variable_ordinal=414,
        variable_name="WT",
        raw_value=1.25,
        missing_state=PhysicalMissingState.OBSERVED_STORAGE_VALUE,
        source_missing_declaration=None,
    )
    witness = bind_weight_carrier(wt)
    assert witness.raw_value == 1.25
    assert witness.documentary_role == "Weighting"
    assert witness.aggregate_estimand_authority == NO_AGGREGATE_ESTIMAND

    with pytest.raises(LAT2011RealizationError, match="aggregate WT estimand is not authorized"):
        bind_weight_carrier(wt, requested_aggregate_estimand="UNIVERSAL_18_COUNTRY_POPULATION")

    with pytest.raises(LAT2011RealizationError, match="default WT use is not authorized"):
        bind_weight_carrier(wt, select_as_default=True)


def test_abc_share_exactly_one_source_specific_semantic_owner():
    bindings = tuple(CandidateSemanticBinding(candidate) for candidate in ("A", "B", "C"))
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
    with pytest.raises(LAT2011RealizationError, match="semantic realization divergence"):
        require_common_abc_semantic_law(divergent)


def test_1995_and_2024_special_laws_are_explicitly_nonimportable():
    assert FORBIDDEN_CROSS_WAVE_SPECIAL_LAWS
    for law_id in FORBIDDEN_CROSS_WAVE_SPECIAL_LAWS:
        with pytest.raises(LAT2011RealizationError, match="foreign Latinobarometro wave law"):
            reject_cross_wave_special_law(law_id)

    payload = source_specific_realization_payload()
    assert payload["cross_wave_inheritance"] == "NONE_AUTHORIZED"
    assert set(payload["forbidden_cross_wave_imports"]) == set(FORBIDDEN_CROSS_WAVE_SPECIAL_LAWS)


def test_s35_edge_scope_and_r35_hooks_are_minimal_and_frozen():
    assert APPLICABLE_EDGE_CLASSES == ("EC01", "EC05", "EC12", "EC13")
    assert R35_HOOK_BINDING["i01_physical_metadata"]["required"] is True
    assert R35_HOOK_BINDING["i02_derivative_parentage"]["required_for_non_direct_raw"] is True
    assert tuple(R35_HOOK_BINDING["i03_source_scope"]["applicable_edge_classes"]) == APPLICABLE_EDGE_CLASSES
    assert set(R35_REQUIRED_PHYSICAL_DIMENSIONS) >= {
        "physical_missing_declarations",
        "physical_missing_states",
        "row_replay_identity",
        "source_coordinate_carriers",
        "weight_design_carriers",
    }
    assert R35_HOOK_BINDING["i03_source_scope"]["semantic_authority"] is False


def test_realization_payload_does_not_claim_physical_equivalence_qualification():
    payload = source_specific_realization_payload()
    assert payload["claim_boundary"] == (
        "SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__NOT_PHYSICAL_EQUIVALENCE_QUALIFIED"
    )
    assert payload["accepted_packet_structure"]["native_identity_is_replay_authority"] is False
    assert payload["weight"]["country_specific_methodology_does_not_authorize_universal_pooling"] is True
