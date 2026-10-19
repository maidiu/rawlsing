"""A41 receipt ingestion tests: preimage verification and non-substitutable grades."""
from __future__ import annotations

import copy

import pytest

from a41 import receipt_bank
from a41.gitpreimage import PreimageError


def _first(bank):
    return copy.deepcopy(bank["receipts"][0])


def test_all_declared_receipts_verify_git_preimages(bank, gp, scope):
    result = receipt_bank.ingest_bank(bank, gp, expected_scope=scope)
    assert result["ingested_count"] == 9
    for rec in result["ingested"]:
        assert rec["ingestion_state"] == "VERIFIED_PREIMAGE_ACCEPTED"
        assert rec["verified_artifacts"]
        for art in rec["verified_artifacts"]:
            assert art["blob_sha1"] and art["sha256"] and art["bytes"] > 0


def test_tampered_blob_preimage_is_refused(bank, gp, scope):
    r = _first(bank)
    r["artifacts"][0]["blob_sha1"] = "0" * 40
    with pytest.raises(PreimageError, match="BLOB_PREIMAGE_MISMATCH"):
        receipt_bank.ingest_receipt(r, gp, expected_scope=scope)


def test_missing_artifact_is_refused(bank, gp, scope):
    r = _first(bank)
    r["artifacts"][0]["path"] = "WORKER_RETURNS/DOES-NOT-EXIST/never.md"
    with pytest.raises(PreimageError, match="does not exist|EMPTY_OR_MISSING_PATH|BLOB_PREIMAGE"):
        receipt_bank.ingest_receipt(r, gp, expected_scope=scope)


def test_unknown_occupancy_kind_is_refused(bank, gp, scope):
    r = _first(bank)
    r["occupancy_kind"] = "TOTALLY_REAL_OCCUPANCY"
    with pytest.raises(receipt_bank.ReceiptRefusal, match="UNKNOWN_OCCUPANCY_KIND"):
        receipt_bank.ingest_receipt(r, gp, expected_scope=scope)


def test_sourcefree_promoted_to_original_occupancy_is_refused(bank, gp, scope):
    """A sourcefree receipt cannot be promoted into original measured occupancy."""
    bank2 = copy.deepcopy(bank)
    target = next(r for r in bank2["receipts"] if r["receipt_id"] == "O35B-P1-M1-NATIVE-BINDING")
    target["occupancy_kind"] = "ORIGINAL_MEASURED_OCCUPANCY"
    with pytest.raises(receipt_bank.ReceiptRefusal,
                       match="ORIGINAL_OCCUPANCY_WITHOUT_ISSUED_U_E_PRE"):
        receipt_bank.ingest_bank(bank2, gp, expected_scope=scope)


def test_sourcefree_with_empty_wave_scope_cannot_be_original(bank, gp, scope):
    bank2 = copy.deepcopy(bank)
    target = next(r for r in bank2["receipts"] if r["receipt_id"] == "E04L-SOURCEFREE-READTHROUGH")
    target["occupancy_kind"] = "ORIGINAL_MEASURED_OCCUPANCY"
    target["independent_u_e_pre_authority"] = "SELF_DECLARED"
    with pytest.raises(receipt_bank.ReceiptRefusal,
                       match="ORIGINAL_OCCUPANCY_WITH_EMPTY_WAVE_SCOPE"):
        receipt_bank.ingest_bank(bank2, gp, expected_scope=scope)


def test_false_promotion_with_self_declared_authority_still_refused(bank, gp, scope):
    """Even with a self-declared authority the unissued frozen scope forbids it."""
    bank2 = copy.deepcopy(bank)
    target = next(r for r in bank2["receipts"] if r["receipt_id"] == "O35B-P1-M1-NATIVE-BINDING")
    target["occupancy_kind"] = "ORIGINAL_MEASURED_OCCUPANCY"
    target["independent_u_e_pre_authority"] = "SELF_DECLARED_ISSUER"
    with pytest.raises(receipt_bank.ReceiptRefusal,
                       match="FALSE_PROMOTION_SOURCEFREE_TO_ORIGINAL_OCCUPANCY"):
        receipt_bank.ingest_bank(bank2, gp, expected_scope=scope)


def test_forged_consumer_ref_is_refused(bank, gp, scope):
    r = _first(bank)
    r["downstream_consumer_read_refs"] = ["forged.consumer.not.declared"]
    with pytest.raises(receipt_bank.ReceiptRefusal,
                       match="UNKNOWN_OR_FORGED_CONSUMER_REF"):
        receipt_bank.ingest_receipt(r, gp, expected_scope=scope)


def test_currentness_clock_violation_is_refused(bank, gp, scope):
    r = _first(bank)
    r["currentness"] = {"archive_or_current": "CURRENT", "as_of": "2099-01-01T00:00:00-0400"}
    with pytest.raises(receipt_bank.ReceiptRefusal, match="CURRENTNESS_CLOCK_VIOLATION"):
        receipt_bank.ingest_receipt(r, gp, expected_scope=scope)


def test_unknown_wave_id_is_refused(bank, gp, scope):
    r = _first(bank)
    r["coverage"]["wave_ids"] = ["SRC99"]
    with pytest.raises(receipt_bank.ReceiptRefusal, match="UNKNOWN_WAVE_ID"):
        receipt_bank.ingest_receipt(r, gp, expected_scope=scope)


def test_bank_is_self_admissible_and_has_pending_slots(bank, gp, scope):
    result = receipt_bank.ingest_bank(bank, gp, expected_scope=scope)
    slots = {s["slot_id"] for s in result["pending_slots"]}
    assert slots == {"E41", "W41", "P41"}
    assert all(s["state"].startswith("PENDING_RETURN") for s in result["pending_slots"])
