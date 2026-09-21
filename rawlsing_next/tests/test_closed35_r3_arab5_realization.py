from types import SimpleNamespace
import unicodedata

import pytest

from rawlsing_next.closed35_arab5_realization import (
    APPLICABLE_EDGE_CLASSES,
    Arab5RealizationError,
    BOUNDED_UNKNOWN,
    CANONICAL_SHA256,
    CandidateSemanticBinding,
    IDENTITY_AUTHORITY,
    ORDINARY_STORED_VALUE,
    Q101_DICTIONARY_KEYS,
    Q101_EXTRA_DICTIONARY_CODES,
    R35_HOOK_BINDING,
    RANKED_CHALLENGE_SLOTS,
    REPLAY_IDENTITY,
    SOURCE_SPECIFIC_REALIZATION_IDENTITY,
    SYSTEM_MISSING,
    UNICODE_STORAGE_WITNESS,
    admit_source_binding,
    preserve_literal_source_text,
    project_design_carrier,
    require_common_abc_semantic_law,
    require_current_design_use_authority,
    require_full_q101_dictionary,
    require_ranked_challenge_topology,
    resolve_item_routing,
    resolve_q101_dictionary_state,
    split_carrier_state,
)


def test_native_id_collision_cannot_replace_row_ordinal_replay_identity():
    assert IDENTITY_AUTHORITY["hard_replay_identity"] == REPLAY_IDENTITY
    assert IDENTITY_AUTHORITY["native_id_noninjective"] is True
    assert IDENTITY_AUTHORITY["country_plus_id_still_noninjective"] is True
    assert IDENTITY_AUTHORITY["accepted_country_plus_id_duplicate_pairs"] == 3
    assert IDENTITY_AUTHORITY["native_id_hard_replay_authority"] is False
    assert IDENTITY_AUTHORITY["country_plus_id_hard_replay_authority"] is False


def test_wt_psu_system_missing_preserves_rows_without_design_invention():
    wt = project_design_carrier("WT", physical_state=SYSTEM_MISSING)
    psu = project_design_carrier("PSU", physical_state=SYSTEM_MISSING)

    for projected in (wt, psu):
        assert projected.physical_state == SYSTEM_MISSING
        assert projected.semantic_role == BOUNDED_UNKNOWN
        assert projected.row_retention_required is True
        assert projected.default_analysis_use_authorized is False

    with pytest.raises(Arab5RealizationError, match="bounded UNKNOWN"):
        require_current_design_use_authority("WT")
    with pytest.raises(Arab5RealizationError, match="bounded UNKNOWN"):
        require_current_design_use_authority("PSU")


def test_q101_full_dictionary_survives_even_when_extra_codes_are_unobserved():
    assert require_full_q101_dictionary(Q101_DICTIONARY_KEYS) == tuple(
        sorted(Q101_DICTIONARY_KEYS)
    )

    for code in Q101_EXTRA_DICTIONARY_CODES:
        state = resolve_q101_dictionary_state(code)
        assert state.source_dictionary_member is True
        assert state.observed_in_accepted_snapshot is False
        assert state.documentary_membership is False
        assert state.semantic_status == BOUNDED_UNKNOWN
        assert state.documentary_label is None

    pruned = tuple(code for code in Q101_DICTIONARY_KEYS if code not in {-9, -8, 97})
    with pytest.raises(Arab5RealizationError, match="changed or pruned"):
        require_full_q101_dictionary(pruned)


def test_q101_dictionary_membership_does_not_prove_observation_or_semantics():
    code97 = resolve_q101_dictionary_state(97)
    assert code97.source_dictionary_member is True
    assert code97.observed_in_accepted_snapshot is False
    assert code97.semantic_status == BOUNDED_UNKNOWN

    code98 = resolve_q101_dictionary_state(98)
    assert code98.observed_in_accepted_snapshot is True
    assert code98.documentary_label == "DON'T_KNOW"

    unknown = resolve_q101_dictionary_state(123456)
    assert unknown.source_dictionary_member is False
    assert unknown.observed_in_accepted_snapshot is None
    assert unknown.semantic_status == BOUNDED_UNKNOWN


def test_unicode_text_is_preserved_exactly_without_lossy_normalization():
    witness = UNICODE_STORAGE_WITNESS.literal_text
    assert preserve_literal_source_text(witness) == witness
    assert preserve_literal_source_text(witness).encode("utf-8") == witness.encode("utf-8")

    decomposed = "e\u0301"
    normalized = unicodedata.normalize("NFC", decomposed)
    assert decomposed != normalized
    assert preserve_literal_source_text(decomposed) == decomposed
    assert preserve_literal_source_text(decomposed) != normalized


def test_ranked_q2061_slots_cannot_be_flattened_or_reordered():
    assert require_ranked_challenge_topology(RANKED_CHALLENGE_SLOTS) == RANKED_CHALLENGE_SLOTS
    assert [slot.variable_name for slot in RANKED_CHALLENGE_SLOTS] == ["Q2061A", "Q2061B"]
    assert [slot.rank for slot in RANKED_CHALLENGE_SLOTS] == [1, 2]

    with pytest.raises(Arab5RealizationError, match="topology changed or flattened"):
        require_ranked_challenge_topology(tuple(reversed(RANKED_CHALLENGE_SLOTS)))

    with pytest.raises(Arab5RealizationError, match="topology changed or flattened"):
        require_ranked_challenge_topology((RANKED_CHALLENGE_SLOTS[0],))


def test_split_carriers_survive_without_inventing_item_routing():
    splita = split_carrier_state("SPLITA")
    splitb = split_carrier_state("SPLITB")

    assert splita.allowed_documentary_assignments == (1, 2)
    assert splitb.allowed_documentary_assignments == (1, 2, 3)
    assert splita.item_routing_semantics == BOUNDED_UNKNOWN
    assert splitb.item_routing_semantics == BOUNDED_UNKNOWN


def test_routing_cannot_be_inferred_from_missingness():
    unresolved = resolve_item_routing(
        "Q999_SYNTHETIC",
        observed_missing_state=SYSTEM_MISSING,
    )
    assert unresolved.status == BOUNDED_UNKNOWN
    assert unresolved.applicability == BOUNDED_UNKNOWN
    assert unresolved.authority_id is None

    resolved = resolve_item_routing(
        "Q999_SYNTHETIC",
        authority_id="SYNTHETIC_DOCUMENTARY_JOIN",
        documented_applicability="APPLIES_TO_EXACT_GOVERNED_SCOPE",
        observed_missing_state=ORDINARY_STORED_VALUE,
    )
    assert resolved.status == "DOCUMENTARY_ROUTING_RESOLVED"
    assert resolved.applicability == "APPLIES_TO_EXACT_GOVERNED_SCOPE"


def test_source_sha_drift_fails_closed_without_claiming_physical_equivalence():
    admission = admit_source_binding(source_sha256=CANONICAL_SHA256)
    assert admission.replay_identity == REPLAY_IDENTITY
    assert admission.physical_equivalence_claimed is False

    with pytest.raises(Arab5RealizationError, match="source root mismatch"):
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
    with pytest.raises(Arab5RealizationError, match="semantic realization divergence"):
        require_common_abc_semantic_law(divergent)


def test_arab5_edge_scope_and_r35_hooks_are_frozen():
    assert APPLICABLE_EDGE_CLASSES == (
        "EC01",
        "EC05",
        "EC07",
        "EC09",
        "EC10",
        "EC11",
        "EC12",
    )
    assert R35_HOOK_BINDING["i01_physical_metadata"]["required"] is True
    assert R35_HOOK_BINDING["i02_derivative_parentage"]["required_for_non_direct_raw"] is True
    assert tuple(
        R35_HOOK_BINDING["i03_source_scope"]["applicable_edge_classes"]
    ) == APPLICABLE_EDGE_CLASSES
    assert R35_HOOK_BINDING["i03_source_scope"]["semantic_authority"] is False


def test_cross_wave_semantic_imports_are_explicitly_forbidden():
    payload = source_specific_realization_payload()
    assert payload["cross_wave"]["semantic_imports_allowed"] is False
    assert payload["cross_wave"]["wave2_semantics_inherited"] is False
    assert payload["cross_wave"]["wave8_semantics_inherited"] is False
