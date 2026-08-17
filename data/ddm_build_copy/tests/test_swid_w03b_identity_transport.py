from __future__ import annotations

import unicodedata

import pandas as pd
import pytest

from data.ddm_build_copy import compile_v551_relation_evidence_atoms as compiler
from data.ddm_build_copy import ddm_v551_atoms as atoms
from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity
from data.ddm_build_copy.ddm_v551_directionality_expectation import (
    build_v551_directionality_stamp_audit,
)


AUTH = {
    "h1": {
        "response_semantics_contract_hash": "h1",
        "authority_intensity_semantics": "DIRECTIONAL_MAGNITUDE",
        "projection_rule_id": "r1",
        "authority_status": "CERTIFIED",
        "review_status": "NO_REVIEW",
    }
}

LEGACY_CANDIDATE_ID_FIELDS = [
    "source",
    "source_family",
    "canonical_wave",
    "country_code",
    "analysis_scope",
    "source_table",
    "question_id",
    "var_code",
    "position_field",
    "position_value",
    "response_value_normalized",
    "source_row_hash",
    "response_semantics_contract_hash",
]
LEGACY_DISTRIBUTION_ID_FIELDS = [
    "source",
    "source_family",
    "canonical_wave",
    "country_code",
    "analysis_scope",
    "source_table",
    "question_id",
    "var_code",
    "position_field",
    "position_value",
    "response_semantics_contract_hash",
    "response_family",
    "response_topology",
    "relation_axis_id",
    "target_entity_id",
    "driver_id",
    "driver_facet_id",
]


@pytest.fixture(autouse=True)
def _frozen_scale_authority(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(atoms, "_load_registry", lambda: AUTH)


def row(source: str = "Arab Barometer", wave: str = "I", **overrides):
    identity = resolve_source_wave_identity(source, wave)
    value = dict(
        run_id="run-1",
        source=source,
        source_family=source,
        source_family_uid=identity.source_family_uid,
        wave=wave,
        canonical_wave=wave,
        wave_uid=identity.wave_uid,
        country_code="DZ",
        analysis_scope="country",
        source_table="answer_distribution",
        source_row_hash="source-row-1",
        question_id="q1",
        var_code="v1",
        position_field="",
        position_value="",
        response_value_raw="1",
        response_value_normalized="1",
        response_label="agree",
        normalized_response_label="agree",
        response_family="agreement_scale",
        response_topology="scalar",
        response_direction="positive",
        response_intensity=0.8,
        directional_applicability_status="APPLICABLE_BY_AUTHORITY",
        bridge_evidence_lane="direct_relation_response",
        is_substantive=True,
        is_missing=False,
        is_special=False,
        response_semantics_contract_hash="h1",
        semantic_role="RELATION_EVIDENCE",
        semantic_role_authority_status="CERTIFIED",
        response_semantics_authority_status="CERTIFIED",
        directionality_authority_status="CERTIFIED",
        structural_mapping_status="COMPLETE",
        response_option_map_matched=True,
        usable_for_evidence=True,
        allowed_as_v551_relation_evidence=True,
        n_unweighted=10,
        n_respondents=20,
        n_weighted=10,
        pct_unweighted=0.5,
        pct_weighted=0.5,
        weight_status="weighted",
        support_status="sufficient_support",
        confidence_tier="high",
        empirical_object_type="answer_distribution",
        empirical_object_id="e1",
        driver_id="d",
        driver_facet_id="f",
        relation_axis_id="a",
        target_entity_id="t",
        manual_review_flag=False,
        source_structure_review_required=False,
        question_use_contract_hash="rowhash",
    )
    value.update(overrides)
    return value


def _without_uid_columns(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.drop(columns=[c for c in ("source_family_uid", "wave_uid") if c in frame.columns])


@pytest.mark.parametrize(
    ("source", "aliases"),
    [
        ("Arab Barometer", ("I", "W1", "Wave 1", "1")),
        ("EVS", ("1981", "W1")),
        ("EVS", ("1999", "W3")),
        ("Afrobarometer", ("R1", "ROUND1", "Round 1")),
    ],
)
def test_wave_aliases_resolve_to_identical_v551_uid_producer_scope(source: str, aliases: tuple[str, ...]) -> None:
    scopes = [compiler._producer_scope_identity(pd.DataFrame([row(source, alias)])) for alias in aliases]
    uid_scopes = {
        (
            scope["source_family_uid"],
            scope["wave_uid"],
            scope["source"],
            scope["wave"],
            scope["country_code"],
            scope["scope_kind"],
        )
        for scope in scopes
    }
    assert len(uid_scopes) == 1


def test_latinobarometro_nfc_nfd_and_unaccented_aliases_resolve_to_identical_scope() -> None:
    nfc = "Latinobarómetro"
    nfd = unicodedata.normalize("NFD", nfc)
    scopes = [
        compiler._producer_scope_identity(pd.DataFrame([row(source, "1995")]))
        for source in (nfc, nfd, "Latinobarometro")
    ]
    assert {
        (scope["source_family_uid"], scope["wave_uid"], scope["source"], scope["wave"])
        for scope in scopes
    } == {
        (
            scopes[0]["source_family_uid"],
            scopes[0]["wave_uid"],
            scopes[0]["source"],
            scopes[0]["wave"],
        )
    }


def test_uid_columns_transport_through_v551_adjudication_atoms_coverage_and_stamp() -> None:
    bridge = pd.DataFrame([row()])
    expected = bridge.iloc[0][["source_family_uid", "wave_uid"]].to_dict()

    adjudication = atoms.build_v551_directional_candidate_adjudication(bridge)
    relation_atoms, _ = atoms.build_v551_relation_evidence_atoms(bridge)
    coverage = atoms.build_v551_directional_distribution_coverage(adjudication)
    stamp = build_v551_directionality_stamp_audit(bridge)

    for frame in (adjudication, relation_atoms, coverage, stamp):
        assert {"source_family_uid", "wave_uid"}.issubset(frame.columns)
        assert frame.iloc[0]["source_family_uid"] == expected["source_family_uid"]
        assert frame.iloc[0]["wave_uid"] == expected["wave_uid"]


def test_redundant_identity_contradiction_fails_closed() -> None:
    bad = row()
    bad["source_family_uid"] = resolve_source_wave_identity("EVS", "1981").source_family_uid

    with pytest.raises(ValueError, match="BLOCKED_V551_SOURCE_WAVE_IDENTITY"):
        atoms.build_v551_directional_candidate_adjudication(pd.DataFrame([bad]))

    with pytest.raises(RuntimeError, match="BLOCKED_V551_SOURCE_WAVE_IDENTITY"):
        compiler._producer_scope_identity(pd.DataFrame([bad]))


def test_asian_barometer_w6_is_recognizable_but_cannot_be_v551_production_evidence() -> None:
    w6 = row("Asian Barometer", "W6")

    with pytest.raises(ValueError, match="BLOCKED_V551_PRODUCTION_IDENTITY"):
        atoms.build_v551_directional_candidate_adjudication(pd.DataFrame([w6]))

    with pytest.raises(RuntimeError, match="BLOCKED_V551_PRODUCTION_IDENTITY"):
        compiler._producer_scope_identity(pd.DataFrame([w6]))


@pytest.mark.parametrize("wave", ("I", "W1", "Wave 1", "1"))
def test_signed_direction_and_intensity_are_alias_spelling_invariant(wave: str) -> None:
    adjudication = atoms.build_v551_directional_candidate_adjudication(
        pd.DataFrame([row("Arab Barometer", wave)])
    )
    observed = adjudication.iloc[0][
        [
            "raw_response_direction",
            "raw_response_intensity",
            "raw_response_intensity_status",
            "authority_intensity_semantics",
            "v551_signed_side",
            "v551_signed_intensity",
            "v551_projection_rule_id",
            "adjudication_outcome",
            "promotable",
        ]
    ].to_dict()
    assert observed == {
        "raw_response_direction": "positive",
        "raw_response_intensity": 0.8,
        "raw_response_intensity_status": "OBSERVED_NUMERIC",
        "authority_intensity_semantics": "DIRECTIONAL_MAGNITUDE",
        "v551_signed_side": "positive",
        "v551_signed_intensity": 0.8,
        "v551_projection_rule_id": "r1",
        "adjudication_outcome": "PROMOTABLE",
        "promotable": True,
    }


def test_legacy_v551_id_and_hash_payloads_ignore_additive_uid_metadata() -> None:
    assert atoms.CANDIDATE_ID_FIELDS == LEGACY_CANDIDATE_ID_FIELDS
    assert atoms.DISTRIBUTION_ID_FIELDS == LEGACY_DISTRIBUTION_ID_FIELDS
    assert "source_family_uid" not in atoms.ATOM_CONTRACT_HASH_FIELDS
    assert "wave_uid" not in atoms.ATOM_CONTRACT_HASH_FIELDS

    modern_bridge = pd.DataFrame([row()])
    legacy_bridge = modern_bridge.drop(columns=["source_family_uid", "wave_uid"])

    modern_adjud = atoms.build_v551_directional_candidate_adjudication(modern_bridge)
    legacy_adjud = atoms.build_v551_directional_candidate_adjudication(legacy_bridge)
    modern_atoms, _ = atoms.build_v551_relation_evidence_atoms(modern_bridge)
    legacy_atoms, _ = atoms.build_v551_relation_evidence_atoms(legacy_bridge)

    for column in ("candidate_id", "empirical_distribution_id"):
        assert modern_adjud.iloc[0][column] == legacy_adjud.iloc[0][column]
    for column in (
        "atom_id",
        "candidate_id",
        "empirical_distribution_id",
        "measurement_contract_hash",
        "atom_contract_hash",
    ):
        assert modern_atoms.iloc[0][column] == legacy_atoms.iloc[0][column]


def test_uid_transport_is_semantically_additive_for_identical_legacy_spelling() -> None:
    modern_bridge = pd.DataFrame([row()])
    legacy_bridge = modern_bridge.drop(columns=["source_family_uid", "wave_uid"])

    modern_adjud = atoms.build_v551_directional_candidate_adjudication(modern_bridge)
    legacy_adjud = atoms.build_v551_directional_candidate_adjudication(legacy_bridge)
    modern_atoms, modern_nonpromotable = atoms.build_v551_relation_evidence_atoms(modern_bridge)
    legacy_atoms, legacy_nonpromotable = atoms.build_v551_relation_evidence_atoms(legacy_bridge)
    modern_coverage = atoms.build_v551_directional_distribution_coverage(modern_adjud)
    legacy_coverage = atoms.build_v551_directional_distribution_coverage(legacy_adjud)
    modern_stamp = build_v551_directionality_stamp_audit(modern_bridge)
    legacy_stamp = build_v551_directionality_stamp_audit(legacy_bridge)

    pd.testing.assert_frame_equal(
        _without_uid_columns(modern_adjud),
        _without_uid_columns(legacy_adjud),
        check_dtype=False,
    )
    pd.testing.assert_frame_equal(
        _without_uid_columns(modern_atoms),
        _without_uid_columns(legacy_atoms),
        check_dtype=False,
    )
    pd.testing.assert_frame_equal(
        _without_uid_columns(modern_nonpromotable),
        _without_uid_columns(legacy_nonpromotable),
        check_dtype=False,
    )
    pd.testing.assert_frame_equal(
        _without_uid_columns(modern_coverage),
        _without_uid_columns(legacy_coverage),
        check_dtype=False,
    )
    pd.testing.assert_frame_equal(
        _without_uid_columns(modern_stamp),
        _without_uid_columns(legacy_stamp),
        check_dtype=False,
    )


def test_country_and_shard_boundaries_remain_independent_of_uid_scope() -> None:
    a = row(source_row_hash="a", country_code="DZ")
    b = row(source_row_hash="b", country_code="MA")
    with pytest.raises(RuntimeError, match="COUNTRY_SCOPE_NOT_SINGULAR"):
        compiler._producer_scope_identity(pd.DataFrame([a, b]))

    a["shard_id"] = "shard-1"
    b["shard_id"] = "shard-1"
    shard_scope = compiler._producer_scope_identity(pd.DataFrame([a, b]))
    assert shard_scope["scope_kind"] == "shard"
    assert shard_scope["country_code"] == ""
    assert shard_scope["shard_id"] == "shard-1"

    b["shard_id"] = "shard-2"
    with pytest.raises(RuntimeError, match="SHARD_SCOPE_NOT_SINGULAR"):
        compiler._producer_scope_identity(pd.DataFrame([a, b]))


def test_run_identity_remains_exact_and_independent(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        compiler,
        "_boundary_api",
        lambda: (
            "test-boundary",
            lambda *args, **kwargs: None,
            lambda *args, **kwargs: None,
            lambda **kwargs: None,
        ),
    )
    with pytest.raises(RuntimeError, match="BLOCKED_V551_RUN_IDENTITY_MISMATCH"):
        compiler.compile_v551_run(
            pd.DataFrame([row()]),
            run_id="different-run",
            bridge_path="unused.csv",
        )


def test_uid_metadata_participates_in_artifact_logical_hash_without_changing_legacy_row_hashes() -> None:
    base = pd.DataFrame([{"candidate_id": "c", "value": "1"}])
    with_uid = base.assign(source_family_uid="sf", wave_uid="wv")
    assert compiler._logical_hash(base) != compiler._logical_hash(with_uid)
