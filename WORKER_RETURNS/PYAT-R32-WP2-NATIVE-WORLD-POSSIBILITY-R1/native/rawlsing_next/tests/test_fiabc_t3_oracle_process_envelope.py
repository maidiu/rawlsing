from __future__ import annotations

import json
from pathlib import Path

import pytest

from rawlsing_next import ee_p2x_candidate_process_envelope as envelope

REPO = Path(__file__).resolve().parents[2]


def _receipt(source_id: str = "CLOSED35_SYNTHETIC", *, derivative: bool = False):
    source_sha = "a" * 64
    source = {
        "source_id": source_id,
        "canonical_source_sha256": source_sha,
        "source_identity_authority_ref": "AUTHORITY71_72_EXACT_SOURCE_ROOT",
        "derivative_identity": None,
        "derivative_to_source_provenance_ref": None,
    }
    if derivative:
        source["derivative_identity"] = {
            "kind": "PRESERVED_TYPED_DERIVATIVE",
            "sha256": "b" * 64,
        }
        source["derivative_to_source_provenance_ref"] = (
            "AUTHORITY71_72_DERIVATIVE_TO_CANONICAL_SOURCE_PROOF"
        )
    return {
        "schema": envelope.FREEZE_RECEIPT_SCHEMA,
        "candidate_neutral": True,
        "frozen_before_candidate_execution": True,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
        "state": "FROZEN_READ_ONLY",
        "source_freezes": {source_id: source},
        "authority_identities": {source_id: {"authority": "frozen"}},
        "workload_identities": {source_id: {"workload": "frozen"}},
        "oracle_identities": {
            source_id: {
                "oracle_identity_sha256": "c" * 64,
                "oracle_freeze_authority_ref": "I05_INDEPENDENT_ORACLE_FREEZE",
            }
        },
        "freeze_order": {
            "source_identity_freeze_sequence": 10,
            "authority_workload_freeze_sequence": 20,
            "oracle_materialize_freeze_sequence": 30,
        },
    }


def _write(tmp_path: Path, doc) -> Path:
    path = tmp_path / "freeze.json"
    path.write_text(json.dumps(doc, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return path


def test_generic_closed35_source_freeze_contract_is_not_lits_wvs_hardcoded(tmp_path):
    doc = _receipt("EVS_WAVE_5", derivative=True)
    loaded, identity = envelope.load_frozen_upstream_receipt(_write(tmp_path, doc))
    assert loaded["source_freezes"]["EVS_WAVE_5"]["source_id"] == "EVS_WAVE_5"
    assert loaded["source_freezes"]["EVS_WAVE_5"]["canonical_source_sha256"] == "a" * 64
    assert loaded["source_freezes"]["EVS_WAVE_5"]["derivative_identity"]["sha256"] == "b" * 64
    assert len(identity) == 64


def test_derivative_identity_requires_derivative_to_source_provenance(tmp_path):
    doc = _receipt()
    doc["source_freezes"]["CLOSED35_SYNTHETIC"]["derivative_identity"] = {"sha256": "b" * 64}
    with pytest.raises(envelope.FrozenUpstreamError):
        envelope.load_frozen_upstream_receipt(_write(tmp_path, doc))


def test_freeze_order_must_precede_candidate_execution(tmp_path):
    doc = _receipt()
    doc["freeze_order"] = {
        "source_identity_freeze_sequence": 30,
        "authority_workload_freeze_sequence": 20,
        "oracle_materialize_freeze_sequence": 10,
    }
    with pytest.raises(envelope.FrozenUpstreamError):
        envelope.load_frozen_upstream_receipt(_write(tmp_path, doc))

    doc = _receipt()
    doc["candidate_outputs_seen"] = 1
    with pytest.raises(envelope.FrozenUpstreamError):
        envelope.load_frozen_upstream_receipt(_write(tmp_path, doc))


def test_live_backend_no_longer_mints_oracle_or_uses_self_replay_as_truth():
    text = (REPO / "rawlsing_next/ee_p2x_darwin_stage_backend.py").read_text(encoding="utf-8")
    s03 = text.split("def _s03(ctx,services,state):", 1)[1].split(
        "def _s04(ctx,services,state):", 1
    )[0]
    assert "_i03(binding)" not in s03
    assert "candidate_self_replay_used_as_expected_truth" in s03
    assert "False" in s03
    assert "PASS__PRE_FROZEN_CANDIDATE_NEUTRAL_ORACLE_BOUND" in s03
    assert "RAWLSING_EE_P2X_CANDIDATE_NEUTRAL_ORACLE@1.0.0" not in s03


def test_driver_requires_frozen_receipt_and_process_isolated_backend_for_execution():
    text = (REPO / "rawlsing_next/ee_p2x_darwin_court_driver.py").read_text(encoding="utf-8")
    assert "--frozen-upstream-receipt" in text
    assert "rawlsing_next.ee_p2x_process_isolated_backend" in text
    assert "direct candidate-backend execution is forbidden" in text


def test_process_envelope_seals_exactly_one_source_candidate_cell():
    text = (REPO / "rawlsing_next/ee_p2x_candidate_process_envelope.py").read_text(
        encoding="utf-8"
    )
    assert 'cell_key = f"{source}/{candidate}"' in text
    assert "active process belongs to" in text
    assert "foreign candidate session survived inside sealed process" in text
