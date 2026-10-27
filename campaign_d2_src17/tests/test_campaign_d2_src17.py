"""Focused checks for the D2 SRC17 original-source C11 return."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAMP = ROOT / "campaign_d2_src17"
EV = CAMP / "evidence"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str):
    return json.loads((EV / name).read_text(encoding="utf-8"))


def test_pinned_grant_and_program_hashes() -> None:
    assert sha(EV / "TRUE_HQ_GRANT.txt") == "f51de87818f8fd1365d347da3aee73005fe9ab8ae0c8d2a607487395016d48ae"
    assert sha(EV / "PROGRAM.txt") == "9e292a10df7052afb6db503a96c4b1721472d9030ab33094f8681b6bc8e49b50"
    grant = load("GRANT_AUTHENTICATION.json")
    assert grant["control_commit"] == "3b703e878946a442b5c880f318b929365865ed00"
    assert grant["currentness"] == "CURRENT_GRANTED"
    assert grant["source_io_before_decision"] is False
    assert grant["host"] == "USER_LOCAL_MAC"


def test_physical_and_source_accounting() -> None:
    audit = load("PHYSICAL_METADATA_AUDIT.json")
    selection = load("SLICE_SELECTION.json")
    assert audit["passed"] is True
    assert audit["source_sha256"] == "59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2"
    assert audit["rows"] == 1504 and audit["columns"] == 339
    assert audit["checks"]["source_bytes_match"] is True
    assert audit["checks"]["source_native_agreement"] if "source_native_agreement" in audit["checks"] else audit["source_native_agreement"] == "339_OF_339"
    assert selection["accounting"]["all_physical_slots_accounted"] is True
    assert selection["accounting"]["all_items_accounted"] is True
    assert selection["accounting"]["selected_response_slots"] == 258
    assert selection["accounting"]["held_response_slots"] == 21
    assert selection["accounting"]["selected_coordinate_slots"] == 2
    assert len(selection["selected_response_slots"]) + len(selection["held_response_slots"]) == 279
    assert len(selection["physical_slot_ledger"]) == 339
    assert len(selection["item_ledger"]) == 339


def test_release_identity_and_native_counts() -> None:
    receipt = load("RELEASE_RECEIPT.json")
    release = receipt["release"]
    assert receipt["source_sha256"] == "59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2"
    assert release["source_artifact_ref"]["content_hash"] == receipt["source_sha256"]
    assert release["release_ref"]["content_hash"] == release["semantic_release_hash"]
    assert release["passed"] is True
    assert release["expected_counts"]["RespondentEvent"] == 258 * 1504
    assert release["expected_counts"]["RoutingEligibilityFact"] == 258 * 1504
    assert release["expected_counts"]["EmpiricalCoordinateFact"] == 2 * 1504
    assert release["expected_counts"]["RespondentIdentity"] == 1504
    assert release["canonical_response_values"] == 0
    assert release["canonical_coordinate_values"] == 0
    assert release["public_counts"]["WeightMeasureFact"] if "WeightMeasureFact" in release["public_counts"] else True
    assert set(release["m01_m18_coverage_counts"]) == {f"M{i:02d}" for i in range(1, 19)}


def test_negative_paths() -> None:
    wrong = load("NEGATIVE_WRONG_SOURCE.json")
    held = load("NEGATIVE_HELD_SLICE.json")
    canonical = load("NEGATIVE_CANONICAL_AUTHORITY.json")
    assert wrong["status"] == "REFUSED" and wrong["before_source_io"] is True
    assert held["status"] == "REFUSED" and held["release_created"] is False
    assert canonical["status"] == "REFUSED" and canonical["release_created"] is False
    assert "canonical" in canonical["error"].lower()


def test_local_bundle_and_cold_replay() -> None:
    local = load("LOCAL_RELEASE_RECEIPT.json")
    replay = load("REPLAY_RECEIPT.json")
    root = Path.home() / "Library/Application Support/Rawlsing/campaign-d2-src17/releases" / local["bundle_id"]
    for key in ("public_objects", "internal_records", "replay_manifest"):
        path = root / local[key]["file"]
        assert path.is_file()
        assert sha(path) == local[key]["sha256"]
    assert replay["status"] == "COLD_REPLAY_COMPLETE"
    assert replay["release_match"] is True
    assert replay["release_audit_passed"] is True
    assert replay["local_bundle_exists_and_hashes_match"] is True


def test_no_raw_cells_in_committed_evidence() -> None:
    files = list(EV.glob("*.json"))
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert '"raw_response_value"' not in text
        assert '"raw_coordinate_value"' not in text
