from types import SimpleNamespace

import pytest

from rawlsing_next.closed35_arab2_realization import (
    APPLICABLE_EDGE_CLASSES,
    Arab2RealizationError,
    BOUNDED_UNKNOWN,
    CANONICAL_SHA256,
    CandidateSemanticBinding,
    IDENTITY_AUTHORITY,
    ORDINARY_STORED_VALUE,
    Q2062_ZERO_SOURCE_DICTIONARY_LABEL,
    R35_HOOK_BINDING,
    RANKED_CHALLENGE_SLOTS,
    REPLAY_IDENTITY,
    SOURCE_SPECIFIC_REALIZATION_IDENTITY,
    SYSTEM_MISSING,
    WT_AUTHORITY,
    admit_source_binding,
    project_q2062_state,
    require_common_abc_semantic_law,
    require_current_weight_use_authority,
    require_ranked_challenge_topology,
    resolve_documentary_routing,
    resolve_semantic_code,
)


def test_q2062_ordinary_zero_is_not_system_missing():
    system = project_q2062_state(physical_state=SYSTEM_MISSING)
    ordinary_zero = project_q2062_state(
        physical_state=ORDINARY_STORED_VALUE,
        raw_value=0,
    )

    assert system.physical_state == SYSTEM_MISSING
    assert system.raw_storage_value is None
    assert ordinary_zero.physical_state == ORDINARY_STORED_VALUE
    assert ordinary_zero.raw_storage_value == 0
    assert ordinary_zero.source_dictionary_label == Q2062_ZERO_SOURCE_DICTIONARY_LABEL
    assert ordinary_zero.semantic_refinement == BOUNDED_UNKNOWN
    assert ordinary_zero != system


def test_source_dictionary_missing_label_does_not_invent_zero_semantics():
    result = resolve_semantic_code(
        "Q2062",
        0,
        source_dictionary_label=Q2062_ZERO_SOURCE_DICTIONARY_LABEL,
    )
    assert result.status == BOUNDED_UNKNOWN
    assert result.documentary_label is None
    assert result.source_dictionary_label == "0. missing"


def test_exact_documentary_codes_can_resolve_without_generalizing_zero():
    q101_dk = resolve_semantic_code("Q101", 8)
    q101_zero = resolve_semantic_code("Q101", 0)
    q2062_refused = resolve_semantic_code("Q2062", 99999)

    assert q101_dk.status == "DOCUMENTARY_CODE_SEMANTICS_RESOLVED"
    assert q101_dk.documentary_label == "I don't know"
    assert q101_zero.status == BOUNDED_UNKNOWN
    assert q2062_refused.documentary_label == "Declined to answer"


def test_ranked_slots_cannot_be_flattened_reordered_or_deduplicated():
    assert require_ranked_challenge_topology(RANKED_CHALLENGE_SLOTS) == RANKED_CHALLENGE_SLOTS
    assert [slot.rank for slot in RANKED_CHALLENGE_SLOTS] == [1, 2]
    assert [slot.variable_name for slot in RANKED_CHALLENGE_SLOTS] == ["Q2061", "Q2062"]

    with pytest.raises(Arab2RealizationError, match="topology changed or flattened"):
        require_ranked_challenge_topology(tuple(reversed(RANKED_CHALLENGE_SLOTS)))

    with pytest.raises(Arab2RealizationError, match="topology changed or flattened"):
        require_ranked_challenge_topology((RANKED_CHALLENGE_SLOTS[0],))


def test_routing_cannot_be_inferred_from_missingness():
    unresolved = resolve_documentary_routing(
        "EG2041",
        country_name="Egypt",
        rules=(),
        observed_missing_state=SYSTEM_MISSING,
    )
    assert unresolved.status == BOUNDED_UNKNOWN
    assert unresolved.applicability == BOUNDED_UNKNOWN
    assert unresolved.route_id is None

    lebanon = resolve_documentary_routing(
        "Q2062",
        country_name="Lebanon",
        observed_missing_state=ORDINARY_STORED_VALUE,
    )
    assert lebanon.status == "DOCUMENTARY_ROUTING_RESOLVED"
    assert lebanon.applicability == "SECOND_RANK_NOT_RECORDED_BY_INSTRUMENT"


def test_wt_carrier_survives_without_default_estimand():
    assert WT_AUTHORITY.carrier_name == "WT"
    assert WT_AUTHORITY.carrier_preservation == "REQUIRED_SOURCE_CARRIER"
    assert WT_AUTHORITY.estimand == BOUNDED_UNKNOWN
    assert WT_AUTHORITY.normalization == BOUNDED_UNKNOWN
    assert WT_AUTHORITY.default_use_authorized is False

    with pytest.raises(Arab2RealizationError, match="estimand/default-use authority"):
        require_current_weight_use_authority("WT")


def test_qid_or_country_qid_cannot_replace_row_ordinal_replay_identity():
    assert IDENTITY_AUTHORITY["hard_replay_identity"] == REPLAY_IDENTITY
    assert IDENTITY_AUTHORITY["QID_documentary_role"] == "QUESTIONNAIRE_ID_NUMBER"
    assert IDENTITY_AUTHORITY["QID_hard_replay_authority"] is False
    assert IDENTITY_AUTHORITY["COUNTRY_PLUS_QID_hard_replay_authority"] is False


def test_source_sha_drift_fails_closed_without_claiming_physical_equivalence():
    admission = admit_source_binding(source_sha256=CANONICAL_SHA256)
    assert admission.replay_identity == REPLAY_IDENTITY
    assert admission.physical_equivalence_claimed is False

    with pytest.raises(Arab2RealizationError, match="source root mismatch"):
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
    with pytest.raises(Arab2RealizationError, match="semantic realization divergence"):
        require_common_abc_semantic_law(divergent)


def test_arab2_edge_scope_and_r35_hooks_are_frozen():
    assert APPLICABLE_EDGE_CLASSES == (
        "EC01",
        "EC05",
        "EC09",
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
