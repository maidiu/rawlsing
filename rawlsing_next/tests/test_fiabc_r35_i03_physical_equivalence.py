from __future__ import annotations

from decimal import Decimal

import pytest

from rawlsing_next.fiabc_whole_source_physical_equivalence import (
    COMPATIBILITY_PHYSICAL_ONLY,
    PASS_STATUS,
    PhysicalEquivalenceError,
    build_candidate_realization,
    build_canonical_expectation,
    canonical_digest,
    verify_candidate_physical_equivalence,
)


SOURCE_SHA = "a" * 64
SEMANTIC_DIGEST = "b" * 64


def source_identity():
    return {
        "family": "Synthetic",
        "wave_or_release": "R35 hostile",
        "canonical_filename": "synthetic.sav",
        "sha256": SOURCE_SHA,
        "format": "sav",
    }


def native_reader():
    return {
        "decoder_implementation": "pyreadstat",
        "decoder_version": "1.2.8",
        "decoder_mode": "SAV_NATIVE_GOVERNED",
        "config": {"apply_value_formats": False, "user_missing": True, "encoding": None},
        "compatibility_mode": "NO_SOURCE_SPECIFIC_COMPATIBILITY_OVERRIDE",
        "compatibility_semantic_scope": "NO_COMPATIBILITY_OVERRIDE__NO_SEMANTIC_CLAIM",
        "semantic_authority": False,
    }


def metadata_binding(material=None, *, receipt="c" * 64):
    if material is None:
        material = {
            "raw_header_layout": {"nominal_case_size": 174},
            "normalized_geometry": {"dictionary_width": 332, "row_count": 1200},
            "display_metadata": {"S007": "F2.0"},
            "reader_config_identity": "pyreadstat@1.2.8/native",
        }
    return {
        "contract": "FIABC_R35_I01_GENERIC_PHYSICAL_METADATA@EXTERNAL",
        "receipt_identity": receipt,
        "source_sha256": SOURCE_SHA,
        "physical_metadata_digest": canonical_digest(material),
        "verification_state": "VERIFIED",
        "semantic_authority": False,
    }


def base_evidence():
    return {
        "variable_inventory_order": [(1, "id"), (2, "all_missing"), (3, "weight")],
        "raw_storage_values": {
            "id": [9876543210, 9876543211],
            "all_missing": [None, None],
            "weight": [Decimal("1.0"), Decimal("2.0")],
        },
        "row_replay_identity": [
            {"source_sha256": SOURCE_SHA, "row_ordinal": 1},
            {"source_sha256": SOURCE_SHA, "row_ordinal": 2},
        ],
    }


def expectation(*, edges=("EC01",), evidence=None, metadata=None):
    material = base_evidence()
    if "EC03" in edges:
        material["compatibility_decode_evidence"] = {
            "encoding": "latin1",
            "raw_bytes_retained": True,
            "semantic_authority": False,
        }
    if "EC04" in edges:
        material["raw_display_separation"] = {
            "variable": "S007",
            "raw_values": [9876543210, 9876543211],
            "display_format": "F2.0",
        }
    if evidence:
        material.update(evidence)
    return build_canonical_expectation(
        scope_id="WHOLE_SOURCE_SYNTHETIC_R35",
        source_identity=source_identity(),
        reader_configuration=native_reader(),
        applicable_edge_classes=edges,
        evidence_material=material,
        physical_metadata_binding=metadata or metadata_binding(),
    )


def realization(
    expected,
    *,
    candidate="A",
    reader=None,
    edges=None,
    evidence=None,
    metadata=None,
    realization_kind="DIRECT_RAW",
    parentage=None,
    semantic_digest=SEMANTIC_DIGEST,
):
    if edges is None:
        edges = expected["scope"]["applicable_edge_classes"]
    material = base_evidence()
    if "EC03" in edges:
        material["compatibility_decode_evidence"] = {
            "encoding": "latin1",
            "raw_bytes_retained": True,
            "semantic_authority": False,
        }
    if "EC04" in edges:
        material["raw_display_separation"] = {
            "variable": "S007",
            "raw_values": [9876543210, 9876543211],
            "display_format": "F2.0",
        }
    if evidence:
        material.update(evidence)
    return build_candidate_realization(
        candidate=candidate,
        expectation=expected,
        source_identity=source_identity(),
        reader_configuration=reader or native_reader(),
        applicable_edge_classes=edges,
        evidence_material=material,
        physical_metadata_binding=metadata or metadata_binding(),
        realization_kind=realization_kind,
        derivative_parentage_binding=parentage,
        semantic_observation_digest=semantic_digest,
    )


def verified_parentage(reader_digest, *, ancestor=SOURCE_SHA):
    return {
        "contract": "FIABC_R35_I02_DERIVATIVE_PARENTAGE@EXTERNAL",
        "receipt_identity": "d" * 64,
        "parent_receipt_identity": "e" * 64,
        "canonical_source_sha256": ancestor,
        "derivative_identity": "f" * 64,
        "producer_identity": "synthetic-builder@blob:1234",
        "operation": "MATERIALIZE_WHOLE_SOURCE_PHYSICAL_CARRIER",
        "reader_configuration_digest": reader_digest,
        "scope_state": "CURRENT_AND_SCOPE_COMPLETE",
        "verification_state": "VERIFIED",
        "semantic_authority": False,
    }


def test_positive_direct_raw_receipt_is_physical_only():
    expected = expectation()
    observed = realization(expected, candidate="B")
    receipt = verify_candidate_physical_equivalence(expected, observed)
    assert receipt["status"] == PASS_STATUS
    assert receipt["semantic_parity_claimed"] is False
    assert receipt["source_certification_claimed"] is False
    assert receipt["weight_population_authority_claimed"] is False


def test_source_without_mr_or_weight_edges_does_not_require_meaningless_fields():
    expected = expectation(edges=("EC01",))
    observed = realization(expected, candidate="C")
    receipt = verify_candidate_physical_equivalence(expected, observed)
    assert receipt["applicable_edge_classes"] == ["EC01"]
    assert "native_mr_sets" not in receipt["matched_required_dimensions"]
    assert "weight_design_variables" not in receipt["matched_required_dimensions"]


def test_wrong_reader_version_fails_even_when_source_and_semantic_digest_match():
    expected = expectation()
    wrong = native_reader()
    wrong["decoder_version"] = "9.9.9"
    observed = realization(expected, reader=wrong)
    with pytest.raises(PhysicalEquivalenceError, match="reader"):
        verify_candidate_physical_equivalence(expected, observed)


def test_compatibility_mode_cannot_be_promoted_to_semantic_authority():
    reader = native_reader()
    reader.update({
        "decoder_mode": "SAV_LATIN1_COMPAT_PHYSICAL_ONLY__SOURCE_DECLARES_UTF8",
        "compatibility_mode": "COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY",
        "compatibility_semantic_scope": "SOURCE_TEXT_SEMANTIC_AUTHORITY",
    })
    with pytest.raises(PhysicalEquivalenceError, match="physical-only"):
        build_canonical_expectation(
            scope_id="EVS_COMPAT_HOSTILE",
            source_identity=source_identity(),
            reader_configuration=reader,
            applicable_edge_classes=("EC01", "EC02", "EC03"),
            evidence_material={
                **base_evidence(),
                "compatibility_decode_evidence": {"encoding": "latin1", "raw_bytes_retained": True},
            },
            physical_metadata_binding=metadata_binding(),
        )


def test_all_missing_column_drop_is_physical_nonequivalence():
    extra = {
        "typed_missingness": {"all_missing": ["SYSTEM_MISSING", "SYSTEM_MISSING"]},
        "all_missing_column_retention": {
            "ordinal": 2,
            "name": "all_missing",
            "row_states": ["SYSTEM_MISSING", "SYSTEM_MISSING"],
        },
    }
    expected = expectation(edges=("EC01", "EC05", "EC06"), evidence=extra)
    changed = dict(extra)
    changed["all_missing_column_retention"] = {"columns": []}
    observed = realization(expected, evidence=changed)
    with pytest.raises(PhysicalEquivalenceError, match="all_missing_column_retention"):
        verify_candidate_physical_equivalence(expected, observed)


def test_display_metadata_may_not_replace_raw_storage_magnitude():
    extra = {
        "raw_display_separation": {
            "variable": "S007",
            "raw_values": [9876543210, 9876543211],
            "display_format": "F2.0",
        }
    }
    expected = expectation(edges=("EC01", "EC04"), evidence=extra)
    changed = {
        "raw_display_separation": {
            "variable": "S007",
            "raw_values": [98, 98],
            "display_format": "F2.0",
        }
    }
    observed = realization(expected, evidence=changed)
    with pytest.raises(PhysicalEquivalenceError, match="raw_display_separation"):
        verify_candidate_physical_equivalence(expected, observed)


def test_raw_header_dictionary_stream_mismatch_must_survive_metadata_digest():
    expected = expectation(edges=("EC01", "EC04"))
    normalized_away = metadata_binding({
        "raw_header_layout": {"nominal_case_size": 332},
        "normalized_geometry": {"dictionary_width": 332, "row_count": 1200},
        "display_metadata": {"S007": "F2.0"},
        "reader_config_identity": "pyreadstat@1.2.8/native",
    }, receipt="1" * 64)
    observed = realization(expected, metadata=normalized_away)
    with pytest.raises(PhysicalEquivalenceError, match="metadata digest"):
        verify_candidate_physical_equivalence(expected, observed)


def test_mr_topology_flattening_fails_with_identical_raw_vectors():
    extra = {
        "native_mr_sets": {
            "Q112": ["Q112_1", "Q112_2"],
            "SE15": ["Q112_2", "SE15_2"],
        }
    }
    expected = expectation(edges=("EC01", "EC08"), evidence=extra)
    observed = realization(
        expected,
        evidence={"native_mr_sets": {"MERGED": ["Q112_1", "Q112_2", "SE15_2"]}},
    )
    with pytest.raises(PhysicalEquivalenceError, match="native_mr_sets"):
        verify_candidate_physical_equivalence(expected, observed)


def test_weight_candidates_are_physical_facts_not_default_selection():
    extra = {
        "weight_design_variables": {
            "candidates": ["WT", "WT_OLD", "WT_NEW"],
            "selected_default": None,
            "raw_values_retained": True,
        }
    }
    expected = expectation(edges=("EC01", "EC12"), evidence=extra)
    observed = realization(
        expected,
        evidence={
            "weight_design_variables": {
                "candidates": ["WT"],
                "selected_default": "WT",
                "raw_values_retained": True,
            }
        },
    )
    with pytest.raises(PhysicalEquivalenceError, match="weight_design_variables"):
        verify_candidate_physical_equivalence(expected, observed)


def test_candidate_subset_cache_cannot_drop_canonical_extra_dimension():
    expected = expectation(
        edges=("EC01",),
        evidence={"variable_dictionaries": {"id": {}, "weight": {"0": "zero"}}},
    )
    observed = realization(expected)
    with pytest.raises(PhysicalEquivalenceError, match="dropped required physical evidence"):
        verify_candidate_physical_equivalence(expected, observed)


def test_equal_semantic_projection_does_not_rescue_unequal_physical_metadata():
    expected = expectation(edges=("EC01", "EC04"))
    drifted = metadata_binding(
        {
            "raw_header_layout": {"nominal_case_size": 174},
            "normalized_geometry": {"dictionary_width": 332, "row_count": 1200},
            "display_metadata": {},
            "reader_config_identity": "pyreadstat@1.2.8/native",
        },
        receipt="2" * 64,
    )
    observed = realization(
        expected,
        metadata=drifted,
        semantic_digest=SEMANTIC_DIGEST,
    )
    assert observed["semantic_observation_digest"] == SEMANTIC_DIGEST
    with pytest.raises(PhysicalEquivalenceError, match="metadata digest"):
        verify_candidate_physical_equivalence(expected, observed)


def test_derivative_with_asserted_source_sha_but_no_parentage_receipt_is_rejected():
    expected = expectation()
    with pytest.raises(PhysicalEquivalenceError, match="parentage"):
        realization(
            expected,
            realization_kind="PRESERVED_DERIVATIVE",
            parentage=None,
        )


def test_derivative_parentage_wrong_ancestor_is_rejected():
    expected = expectation()
    with pytest.raises(PhysicalEquivalenceError, match="wrong canonical source"):
        realization(
            expected,
            realization_kind="STRUCTURAL_PREIMAGE",
            parentage=verified_parentage(expected["reader_configuration_digest"], ancestor="9" * 64),
        )


def test_verified_derivative_parentage_can_close_to_same_canonical_expectation():
    expected = expectation(edges=("EC01", "EC04"))
    observed = realization(
        expected,
        candidate="A",
        realization_kind="PRESERVED_CARRIER",
        parentage=verified_parentage(expected["reader_configuration_digest"]),
    )
    receipt = verify_candidate_physical_equivalence(expected, observed)
    assert receipt["status"] == PASS_STATUS
    assert receipt["derivative_parentage_receipt_identity"] == "d" * 64
    assert receipt["semantic_observation_used_as_physical_truth"] is False


def test_compound_edge_class_requires_actual_atomic_composition():
    with pytest.raises(PhysicalEquivalenceError, match="compound"):
        expectation(edges=("EC01", "EC14"))
