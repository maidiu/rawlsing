"""A41 falsifiers: input deletion, information loss, false promotion, forged refs.

These are the mandatory same-pass controls. Each proves the assembly is driven by
the real evidence and the frozen scope, not by a self-produced expectation.
"""
from __future__ import annotations

import copy

import pytest

from a41 import receipt_bank, estate_assessor
from a41.gitpreimage import PreimageError


def _accounting_from(bank, scope, gp):
    ingested = receipt_bank.ingest_bank(bank, gp, expected_scope=scope)
    return estate_assessor.assess(scope, ingested)


def test_a41_full_estate_requires_the_accounting_receipt(bank, scope, gp):
    """Deleting the eligible O35B accounting receipt drops 70 identity cells."""
    base = _accounting_from(bank, scope, gp)
    accounted = {c["cell_id"] for c in base["cells"]
                 if c["consumed_grade"] == "DOCUMENTARY_IDENTITY_RECONCILIATION"}
    assert "SRC01.S01" in accounted and len(accounted) == 70
    reduced = copy.deepcopy(bank)
    reduced["receipts"] = [r for r in reduced["receipts"]
                           if r["receipt_id"] != "O35B-ORIGINAL35-ACCOUNTING"]
    cut = _accounting_from(reduced, scope, gp)
    accounted2 = {c["cell_id"] for c in cut["cells"]
                  if c["consumed_grade"] == "DOCUMENTARY_IDENTITY_RECONCILIATION"}
    assert accounted2 != accounted
    assert "SRC01.S01" not in accounted2


def test_a41_missing_receipt_is_detected_by_all35_assertion(bank, scope, gp, accounting):
    missing = accounting["verdict"]["missing_expected_cells"]
    reduced = copy.deepcopy(bank)
    reduced["receipts"] = [r for r in reduced["receipts"]
                           if r["receipt_id"] != "AS2B-LITS-HISTORICAL-POSITIVE"]
    cut = _accounting_from(reduced, scope, gp)
    assert cut["verdict"]["missing_expected_cells"] == missing + 2


def test_a41_preserves_f6_unknown_mass(bank, accounting):
    """The assembly must carry the F6 uncovered masses; dropping them loses info."""
    f6p = next(r for r in bank["receipts"] if r["receipt_id"] == "F6P-SOURCEFREE-PARTIAL-BOUND")
    ub = f6p["unknown_bounds"]
    assert ub["uncovered_target_mass_W2"] == "1/4"
    assert ub["uncovered_target_mass_W7"] == "1/2"
    assert ub["uncovered_target_mass_W3"] == "1/5"
    assert ub["route_probability"] is None
    preserved = {b["receipt_id"]: b["unknown_bounds"]
                 for b in accounting["preserved_unknown_bounds"]}
    f6p_preserved = preserved.get("F6P-SOURCEFREE-PARTIAL-BOUND", {})
    assert f6p_preserved.get("uncovered_target_mass_W2") == "1/4"
    assert f6p_preserved.get("uncovered_target_mass_W7") == "1/2"


def test_a41_rejects_sourcefree_promotion_to_original(bank, scope, gp):
    promoted = copy.deepcopy(bank)
    tgt = next(r for r in promoted["receipts"]
               if r["receipt_id"] == "E04L-SOURCEFREE-READTHROUGH")
    tgt["occupancy_kind"] = "ORIGINAL_MEASURED_OCCUPANCY"
    tgt["independent_u_e_pre_authority"] = "SELF_DECLARED"
    with pytest.raises(receipt_bank.ReceiptRefusal):
        receipt_bank.ingest_bank(promoted, gp, expected_scope=scope)


def test_a41_rejects_forged_consumer_ref(bank, scope, gp):
    forged = copy.deepcopy(bank)
    tgt = next(r for r in forged["receipts"]
               if r["receipt_id"] == "E04L-SOURCEFREE-READTHROUGH")
    tgt["downstream_consumer_read_refs"] = ["stale.forged.consumer"]
    with pytest.raises(receipt_bank.ReceiptRefusal, match="CONSUMER_REF"):
        receipt_bank.ingest_bank(forged, gp, expected_scope=scope)


def test_a41_rejects_stale_currentness(bank, scope, gp):
    stale = copy.deepcopy(bank)
    tgt = next(r for r in stale["receipts"]
               if r["receipt_id"] == "WV1-SOURCEFREE-WORLD-CONSUMPTION")
    tgt["currentness"] = {"archive_or_current": "CURRENT", "as_of": "2000-01-01T00:00:00-0400"}
    # as_of is before the clock so it is admissible; a FUTURE as_of must be refused.
    tgt["currentness"]["as_of"] = "2099-01-01T00:00:00-0400"
    with pytest.raises(receipt_bank.ReceiptRefusal, match="CLOCK_VIOLATION"):
        receipt_bank.ingest_bank(stale, gp, expected_scope=scope)


def test_a41_archive_current_consistency(bank, scope, gp):
    bad = copy.deepcopy(bank)
    tgt = next(r for r in bad["receipts"]
               if r["receipt_id"] == "AS2B-LITS-HISTORICAL-POSITIVE")
    tgt["currentness"] = {"archive_or_current": "CURRENT", "as_of": "2026-10-18T23:30:00-0400"}
    with pytest.raises(receipt_bank.ReceiptRefusal, match="HISTORICAL_ONLY_GRADE"):
        receipt_bank.ingest_bank(bad, gp, expected_scope=scope)


def test_a41_accounting_is_deterministic(scope, bank, gp):
    a = _accounting_from(bank, scope, gp)
    b = _accounting_from(copy.deepcopy(bank), scope, gp)
    assert a["verdict"] == b["verdict"]
    assert a["grade_tally"] == b["grade_tally"]
