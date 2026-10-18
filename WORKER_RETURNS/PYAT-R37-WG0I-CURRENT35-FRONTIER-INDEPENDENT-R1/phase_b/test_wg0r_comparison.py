"""WG0I — independent tests of the WG0R comparison/crosswalk.

WG0R bytes are author evidence.  These tests bind the accounting, wave,
crosswalk, carrier-RED and author-court claims without accepting them as the
full current35 operation frontier.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wg0r_compare as C  # noqa: E402
import wg0i_oracle as O  # noqa: E402


@pytest.fixture(scope="module")
def comp():
    return C.compare()


def test_wg0r_accounting_is_18276_unique_35_waves_9_families(comp):
    a = comp["author_evidence"]
    assert a["accounting_rows"] == 18276
    assert a["unique_implementation_ids"] == 18276
    assert a["unique_identity_hashes"] == 18276
    assert a["waves"] == 35 and a["wave_sum"] == 18276
    assert a["families"] == 9
    assert comp["wg0r_claims"]["implementations"] == 18276
    assert comp["wg0r_claims"]["unique_ids"] == 18276
    assert comp["wg0r_claims"]["duplicate_ids"] == []
    assert comp["wg0r_claims"]["missing_waves"] == []
    assert comp["wg0r_claims"]["unexpected_waves"] == []


def test_crosswalk_arithmetic_is_exact_and_typed(comp):
    c = comp["crosswalk"]
    assert c["o35e_rows"] == 18259
    assert c["o35e_non_none_identity_hashes"] == 18250
    assert c["o35e_none_identity_rows"] == 9
    assert c["common_identity_hashes"] == 18250
    assert c["p2_only_hashes"] == 26
    assert c["net_count_delta"] == 17
    assert c["p2_only_hashes"] - c["o35e_none_identity_rows"] == c["net_count_delta"]
    assert len(c["p2_only_carrier_variables"]) + len(c["p2_only_measurement_candidates"]) == 26
    assert c["classification"].startswith("CROSSWALK_DELTA_REQUIRES_OWNER_TYPING")
    assert {d["atlas_id"] for d in c["wave_deltas"]} == {"SRC01", "SRC24", "SRC26"}
    assert sum(d["delta"] for d in c["wave_deltas"]) == 17


def test_p2_only_measurement_candidates_are_owner_crosswalk_not_silent_drop(comp):
    cands = comp["crosswalk"]["p2_only_measurement_candidates"]
    assert len(cands) == 19
    names = {(x["family"], x["wave"], x["variable"]) for x in cands}
    assert ("Latinobarómetro", "1995", "p46a") in names
    assert ("Latinobarómetro", "2024", "Q45ST") in names
    assert ("Afrobarometer", "R1", "xstronld") in names
    # These are not silently permitted or executed; the oracle keeps PERMITTED=0.
    assert O.ORACLE["operation_census"]["permitted"] == 0


def test_o35e_none_identity_rows_are_typed_blocked_not_omitted(comp):
    rows = comp["crosswalk"]["o35e_none_rows"]
    assert len(rows) == 9
    assert all(r["status"] == "BLOCKED_IDENTITY_OR_AUTHORITY_JOIN" for r in rows)
    # All 9 remain in the oracle item count and status census.
    assert O.ORACLE["item_census"]["status_counts"]["BLOCKED_IDENTITY_OR_AUTHORITY_JOIN"] == 9


def test_wg0r_full_frontier_is_unverified_and_matches_oracle_hold(comp):
    assert comp["wg0r_claims"]["all35_operation_execution"] == \
        "UNVERIFIED__NO_RAW_READS_OR_SOURCE_WARRANT_ISSUED"
    assert comp["wg0r_claims"]["pending_edge"] == \
        "EXACT_ACCEPTED_AUTHORITY_TO_OPERATION_CATALOG_BINDING_AND_FULL_FRONTIER_WITNESS"
    assert comp["full_frontier_claim"] == "UNVERIFIED"
    assert O.ORACLE["six_label_census"]["PERMITTED"]["count"] == 0
    assert O.ORACLE["six_label_census"]["PRODUCER_PENDING"]["count"] == 18259
    states = {x["id"]: x["state"] for x in comp["typed_pending"]}
    assert states["PEND-02"] == "FULL_ORIGINAL_AUTHORITY_TO_OPERATION_BINDING_UNWITNESSED"
    assert states["PEND-03"] == "ALL35_ELIGIBLE_OPERATION_EXECUTION_UNVERIFIED"


def test_wg0r_carrier_red_is_consistent_and_fail_closed(comp):
    c = comp["carrier"]
    assert c["claimed_bytes"] == 18276
    assert c["claimed_sha256"].startswith("64a43ba2")
    assert c["observed_bytes"] == 18387
    assert c["observed_sha256"].startswith("3bee6f0e")
    assert c["reserved_bit_violations"] == 2114
    assert c["state"] == "DISPOSITION_PAYLOAD_MISMATCH"
    assert c["fail_closed"] is True
    assert c["local_archive_copy_sha256"].startswith("c1d5a9a9")


def test_wg0r_bounded_author_court_is_82_and_cold(comp):
    a = comp["author_evidence"]
    assert a["author_court"] == {"tests": 82, "failures": 0, "errors": 0, "skipped": 0}
    assert a["cold_court"] == {"tests": 82, "failures": 0, "errors": 0, "skipped": 0}
    assert a["cold_receipt"]["two_fresh_process_outputs_identical"] is True
    assert a["cold_receipt"]["new_batch_executions_on_resume"] == 0


def test_wg0r_p2_and_lits_claims_match_accepted_hashes(comp):
    assert comp["wg0r_claims"]["p2_sha256"] == \
        "d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6"
    assert comp["p2_skeleton"]["sha256"] == comp["wg0r_claims"]["p2_sha256"]
    assert comp["wg0r_claims"]["p10_accounting_units"] == 65354
    assert comp["wg0r_claims"]["p10_exact_held_states"] == 76
    assert O.ORACLE["accepted_positives"]["lits_i_as2b"]["respondents"] == 29002
    assert O.ORACLE["accepted_positives"]["lits_i_as2b"]["i03_passed"] == 8
