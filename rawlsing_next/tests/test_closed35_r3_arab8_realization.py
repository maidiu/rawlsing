from types import SimpleNamespace

import pytest

from rawlsing_next.closed35_arab8_realization import (
    APPLICABLE_EDGE_CLASSES,
    Arab8RealizationError,
    BLOCK_ID_AUTHORITY,
    BOUNDED_UNKNOWN,
    CANONICAL_SHA256,
    CandidateSemanticBinding,
    DESIGN_CARRIERS,
    IDENTITY_AUTHORITY,
    ORDINARY_STORED_VALUE,
    Q622C_TOPOLOGY,
    R35_HOOK_BINDING,
    REPLAY_IDENTITY,
    SOURCE_SPECIFIC_REALIZATION_IDENTITY,
    admit_source_binding,
    project_block_id,
    project_id,
    require_common_abc_semantic_law,
    require_current_design_or_weight_use_authority,
    require_q1_stratum_nonalias,
    require_q622c_member_topology,
    require_wave8_documentary_scope,
    resolve_documentary_routing,
)


def test_id_zero_is_ordinary_source_state_not_replay_identity():
    projected = project_id(0)
    assert projected.raw_value == 0
    assert projected.physical_state == ORDINARY_STORED_VALUE
    assert projected.documentary_role == "RESPONDENT_ID_NUMBER"
    assert projected.hard_replay_authority is False
    assert IDENTITY_AUTHORITY["hard_replay_identity"] == REPLAY_IDENTITY
    assert IDENTITY_AUTHORITY["ID_hard_replay_authority"] is False
    assert IDENTITY_AUTHORITY["COUNTRY_PLUS_ID_hard_replay_authority"] is False


def test_blank_block_id_remains_ordinary_string_not_system_missing():
    projected = project_block_id("")
    assert projected.raw_value == ""
    assert projected.physical_state == ORDINARY_STORED_VALUE
    assert projected.semantic_state == BOUNDED_UNKNOWN
    assert BLOCK_ID_AUTHORITY["ordinary_blank_is_system_missing"] is False
    assert BLOCK_ID_AUTHORITY["accepted_snapshot_system_missing_count"] == 0

    with pytest.raises(Arab8RealizationError, match="source string"):
        project_block_id(None)


def test_q1_stratum_vector_equality_never_creates_alias_authority():
    q1, stratum = require_q1_stratum_nonalias(vectors_equal=True)
    assert q1.variable_name == "Q1"
    assert q1.documentary_role == "GOVERNORATE_FIRST_ADMINISTRATIVE_DIVISION"
    assert stratum.variable_name == "STRATUM"
    assert stratum.semantic_state == BOUNDED_UNKNOWN
    assert q1 != stratum

    with pytest.raises(Arab8RealizationError, match="semantic alias"):
        require_q1_stratum_nonalias(
            vectors_equal=True,
            semantic_alias_requested=True,
        )


def test_q1a_pal_routing_is_documentary_not_missingness_derived():
    resolved = resolve_documentary_routing(
        "Q1A_PAL",
        country_code=15,
        observed_missing_state=ORDINARY_STORED_VALUE,
    )
    assert resolved.status == "DOCUMENTARY_ROUTING_RESOLVED"
    assert resolved.applicability == "APPLIES_FOR_COUNTRY_15"

    unresolved = resolve_documentary_routing(
        "Q1A_PAL",
        country_code=8,
        observed_missing_state="SYSTEM_MISSING",
    )
    assert unresolved.status == BOUNDED_UNKNOWN
    assert unresolved.applicability == BOUNDED_UNKNOWN


def test_q622c_irq_select_all_topology_survives_without_native_mr_invention():
    resolved = resolve_documentary_routing(
        "Q622C_IRQ_*",
        country_code=7,
        split_assignment="A",
        observed_missing_state="SYSTEM_MISSING",
    )
    assert resolved.status == "DOCUMENTARY_ROUTING_RESOLVED"
    assert resolved.topology == "SELECT_ALL_THAT_APPLY"
    assert Q622C_TOPOLOGY["native_spss_mr_metadata"] is False
    assert Q622C_TOPOLOGY["member_variables_remain_distinct"] is True

    assert require_q622c_member_topology(("Q622C_IRQ_1",)) == ("Q622C_IRQ_1",)
    with pytest.raises(Arab8RealizationError, match="scalar-flattened"):
        require_q622c_member_topology(("Q622C_IRQ",))


def test_design_carriers_are_preserved_without_default_use_or_estimand_invention():
    carriers = {carrier.carrier_name: carrier for carrier in DESIGN_CARRIERS}
    assert set(carriers) == {"WT", "PSU", "STRATUM"}
    assert carriers["WT"].analytic_role == BOUNDED_UNKNOWN
    assert carriers["WT"].default_use_authorized is False
    assert carriers["PSU"].documentary_role == "SOURCE_NATIVE_SAMPLING_VARIABLE"
    assert carriers["PSU"].analytic_role == BOUNDED_UNKNOWN
    assert carriers["STRATUM"].documentary_role == BOUNDED_UNKNOWN

    for name in ("WT", "PSU", "STRATUM"):
        with pytest.raises(Arab8RealizationError, match="bounded UNKNOWN"):
            require_current_design_or_weight_use_authority(name)


def test_cross_wave_semantics_are_rejected():
    assert require_wave8_documentary_scope("Wave 8") == "Wave 8"
    with pytest.raises(Arab8RealizationError, match="cross-wave"):
        require_wave8_documentary_scope("Wave 5")
    with pytest.raises(Arab8RealizationError, match="cross-wave"):
        require_wave8_documentary_scope("Wave 2")


def test_source_sha_drift_fails_closed_without_physical_equivalence_claim():
    admission = admit_source_binding(source_sha256=CANONICAL_SHA256)
    assert admission.replay_identity == REPLAY_IDENTITY
    assert admission.physical_equivalence_claimed is False

    with pytest.raises(Arab8RealizationError, match="source root mismatch"):
        admit_source_binding(source_sha256="0" * 64)


def test_abc_candidates_share_one_source_specific_semantic_owner():
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
    with pytest.raises(Arab8RealizationError, match="semantic realization divergence"):
        require_common_abc_semantic_law(divergent)


def test_arab8_edge_scope_and_r35_hooks_are_frozen():
    assert APPLICABLE_EDGE_CLASSES == (
        "EC01",
        "EC05",
        "EC07",
        "EC10",
        "EC12",
        "EC14",
    )
    assert R35_HOOK_BINDING["i01_physical_metadata"]["required"] is True
    assert R35_HOOK_BINDING["i02_derivative_parentage"]["required_for_non_direct_raw"] is True
    assert tuple(
        R35_HOOK_BINDING["i03_source_scope"]["applicable_edge_classes"]
    ) == APPLICABLE_EDGE_CLASSES
    assert R35_HOOK_BINDING["i03_source_scope"]["semantic_authority"] is False
