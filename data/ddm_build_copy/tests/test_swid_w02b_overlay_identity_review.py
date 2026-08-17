#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy.ddm_source_wave_identity import ProductionMembershipError
from data.ddm_build_copy.ddm_v550_family_overlay import (
    NOT_CERTIFIED_STATUS,
    REVIEW_ONLY_AUTHORITY_STATUS,
    OverlayAuthorityConflictError,
    enforce_review_only_overlay_frame,
    load_family_overlay,
    load_overlay_manifest,
    resolve_overlay_identity,
)
from data.ddm_build_copy import build_all_survey_overlays as batch
from data.ddm_build_copy import build_wave_overlays as single


def _overlay_csv(path: Path, *, note: str = "same") -> bytes:
    frame = pd.DataFrame([
        {
            "source": "Arab Barometer",
            "wave": "I",
            "canonical_wave": "I",
            "var_name": "Q1",
            "note": note,
            "directionality_authority_status": REVIEW_ONLY_AUTHORITY_STATUS,
            "directional_certification_status": NOT_CERTIFIED_STATUS,
        }
    ])
    data = frame.to_csv(index=False).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def test_alias_equivalent_duplicate_candidates_are_enumerated_and_exact_bytes_are_equivalent(tmp_path):
    root = tmp_path / "reports"
    left = root / "arab_barometer_I_directionality_overlay.csv"
    right = root / "arabbarometer_W1_directionality_overlay.csv"
    expected = _overlay_csv(left)
    right.write_bytes(expected)

    result = load_family_overlay(
        "ArabBarometer",
        "W1",
        "directionality",
        search_roots=[root],
    )

    assert result.status == "FOUND"
    assert result.source_family_uid == "sf_arab_barometer_v1"
    assert result.wave_uid == "wv_arab_barometer_i_v1"
    assert result.row_count == 1
    assert len(result.candidate_paths) == 2
    assert len(result.candidate_sha256) == 1
    assert result.data_frame.iloc[0]["note"] == "same"


def test_conflicting_content_for_one_governed_uid_fails_closed(tmp_path):
    root = tmp_path / "reports"
    _overlay_csv(root / "arab_barometer_I_directionality_overlay.csv", note="left")
    _overlay_csv(root / "arabbarometer_W1_directionality_overlay.csv", note="right")

    result = load_family_overlay(
        "Arab Barometer",
        "1",
        "directionality",
        search_roots=[root],
    )

    assert result.status == "CONFLICTING_AUTHORITY_CANDIDATES"
    assert result.data_frame is None
    assert len(result.candidate_sha256) == 2
    assert "wv_arab_barometer_i_v1" in result.message


def test_candidate_resolution_is_search_order_independent(tmp_path):
    root_a = tmp_path / "a"
    root_b = tmp_path / "b"
    content = _overlay_csv(root_a / "arab_barometer_I_directionality_overlay.csv")
    other = root_b / "arabbarometer_W1_directionality_overlay.csv"
    other.parent.mkdir(parents=True, exist_ok=True)
    other.write_bytes(content)

    forward = load_family_overlay(
        "Arab Barometer", "Wave 1", "directionality", search_roots=[root_a, root_b]
    )
    reverse = load_family_overlay(
        "Arab Barometer", "Wave 1", "directionality", search_roots=[root_b, root_a]
    )

    assert forward.status == reverse.status == "FOUND"
    assert forward.candidate_sha256 == reverse.candidate_sha256
    assert forward.data_frame.to_dict("records") == reverse.data_frame.to_dict("records")
    assert sorted(forward.candidate_paths) == sorted(reverse.candidate_paths)


def test_aliases_resolve_through_governed_uid_not_spelling_equality():
    one = resolve_overlay_identity("Arab Barometer", "I")
    two = resolve_overlay_identity("ArabBarometer", "W1")
    three = resolve_overlay_identity("Arab Barometer", "1")
    assert {one.source_family_uid, two.source_family_uid, three.source_family_uid} == {
        "sf_arab_barometer_v1"
    }
    assert {one.wave_uid, two.wave_uid, three.wave_uid} == {
        "wv_arab_barometer_i_v1"
    }


def test_asian_w6_is_rejected_by_default_and_only_recognized_in_explicit_historical_mode(tmp_path):
    result = load_family_overlay(
        "Asian Barometer",
        "W6",
        "directionality",
        search_roots=[tmp_path],
    )
    assert result.status == "NONPRODUCTION_IDENTITY"

    with pytest.raises(ProductionMembershipError):
        resolve_overlay_identity("Asian Barometer", "Wave 6")

    historical = resolve_overlay_identity(
        "Asian Barometer",
        "Wave 6",
        historical_nonproduction=True,
    )
    assert historical.wave_uid == "wv_asian_barometer_w6_v1"
    assert historical.governance_state == "RECOGNIZED_EXCLUDED"
    assert historical.closed_35_member is False
    assert historical.production_authorized is False


def test_batch_builder_rejects_w6_before_database_access(monkeypatch):
    touched = {"db": False}

    def _forbidden_connect():
        touched["db"] = True
        raise AssertionError("DB must not be touched for ordinary W6 generation")

    monkeypatch.setattr(batch, "connect", _forbidden_connect)
    with pytest.raises(ProductionMembershipError):
        batch.build_for_survey(
            "Asian Barometer",
            "W6",
            "W6",
            "W6",
            "Asian Barometer Wave 6 codebook.csv",
            False,
        )
    assert touched["db"] is False


def test_review_only_sanitizer_overrides_any_certification_like_candidate_values():
    candidate = pd.DataFrame([
        {
            "semantic_role_authority_status": "CERTIFIED",
            "directionality_authority_status": "CERTIFIED",
            "directional_certification_status": "CERTIFIED",
            "runtime_authority_status": "CERTIFIED",
            "current_directional_atom_eligible": True,
            "manual_review_required": False,
        }
    ])
    out = enforce_review_only_overlay_frame(candidate)
    row = out.iloc[0]
    assert row["semantic_role_authority_status"] == REVIEW_ONLY_AUTHORITY_STATUS
    assert row["directionality_authority_status"] == REVIEW_ONLY_AUTHORITY_STATUS
    assert row["directional_certification_status"] == NOT_CERTIFIED_STATUS
    assert row["runtime_authority_status"] == NOT_CERTIFIED_STATUS
    assert bool(row["current_directional_atom_eligible"]) is False
    assert bool(row["manual_review_required"]) is True


def test_single_wave_builder_uses_uid_scoped_response_context_and_emits_review_only(tmp_path, monkeypatch):
    manifests = tmp_path / "manifests"
    reports = tmp_path / "reports"
    output = tmp_path / "output"
    manifests.mkdir()
    reports.mkdir()

    arab = resolve_overlay_identity("Arab Barometer", "W1")
    asian = resolve_overlay_identity("Asian Barometer", "W1")
    pd.DataFrame([
        {
            "source": "Arab Barometer",
            "wave": "W1",
            "canonical_wave": "I",
            "source_family_uid": arab.source_family_uid,
            "wave_uid": arab.wave_uid,
            "var_name": "Q1",
            "question_text": "Question",
            "semantic_role": "relation_evidence",
            "directionality_policy": "signed_attitude",
        },
        {
            "source": "Asian Barometer",
            "wave": "W1",
            "canonical_wave": "W1",
            "source_family_uid": asian.source_family_uid,
            "wave_uid": asian.wave_uid,
            "var_name": "Q1",
            "question_text": "Other question",
            "semantic_role": "relation_evidence",
            "directionality_policy": "signed_attitude",
        },
    ]).to_csv(manifests / "question_structure_register.csv", index=False)

    # Same var_name exists in two families. Only the Arab UID row may supply
    # response-family context to an Arab overlay.
    pd.DataFrame([
        {
            "source": "Arab Barometer", "wave": "I", "canonical_wave": "I",
            "var_name": "Q1", "response_family": "yes_no",
        },
        {
            "source": "Asian Barometer", "wave": "W1", "canonical_wave": "W1",
            "var_name": "Q1", "response_family": "trust_scale",
        },
    ]).to_csv(reports / "V550_response_option_map.csv", index=False)

    monkeypatch.setattr(single, "MANIFESTS", manifests)
    monkeypatch.setattr(single, "REPORTS", reports)
    monkeypatch.setattr(
        single,
        "infer_semantic_detail",
        lambda _row: {
            "semantic_subrole": "test",
            "semantic_tags": "",
            "directionality_policy": "signed_attitude",
            "semantic_confidence": "low",
            "semantic_note": "test",
        },
    )
    monkeypatch.setattr(single, "infer_semantic_role", lambda _row: "relation_evidence")

    single.build_overlays("ArabBarometer", "W1", "I", output_dir=output)
    directionality = pd.read_csv(output / "arab_barometer_I_directionality_overlay.csv")
    assert len(directionality) == 1
    row = directionality.iloc[0]
    assert row["source_family_uid"] == "sf_arab_barometer_v1"
    assert row["wave_uid"] == "wv_arab_barometer_i_v1"
    assert row["response_family_expectation"] == "yes_no"
    assert row["directionality_authority_status"] == REVIEW_ONLY_AUTHORITY_STATUS
    assert row["directional_certification_status"] == NOT_CERTIFIED_STATUS
    assert bool(row["current_directional_atom_eligible"]) is False
    assert bool(row["manual_review_required"]) is True


def test_uid_equivalent_overlay_manifests_allow_identical_bytes_and_reject_divergence(tmp_path, monkeypatch):
    authority_root = tmp_path / "authority"
    reports = authority_root / "reports"
    reports.mkdir(parents=True)
    payload = {
        "source": "Arab Barometer",
        "source_family_uid": "sf_arab_barometer_v1",
        "status": "HEURISTIC_REVIEW_ONLY",
    }
    data = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
    first = reports / "arab_barometer_overlay_manifest.json"
    second = reports / "arabbarometer_overlay_manifest.json"
    first.write_bytes(data)
    second.write_bytes(data)
    monkeypatch.setenv("DDM_AUTHORITY_ROOT", str(authority_root))

    loaded = load_overlay_manifest(survey_family="ArabBarometer")
    assert loaded["source_family_uid"] == "sf_arab_barometer_v1"
    assert loaded["status"] == "HEURISTIC_REVIEW_ONLY"

    second.write_text(json.dumps({**payload, "status": "DIFFERENT"}) + "\n", encoding="utf-8")
    with pytest.raises(OverlayAuthorityConflictError, match="manifests diverge"):
        load_overlay_manifest(survey_family="Arab Barometer")
