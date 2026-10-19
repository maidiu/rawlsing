from __future__ import annotations
import json
import sys
from pathlib import Path
import pytest
from s44 import historical, handoff

RETURN = Path(__file__).resolve().parents[1]

def test_as2b_historical_fact_is_exact(hist):
    a = hist["as2b"]
    assert a["source_sha256"] == "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
    assert a["respondent_count"] == 29002 and a["event_count"] == 58004
    assert a["i03_executed"] == 8 and a["i03_supported"] == 1
    assert a["supported_fact"]["empirical_fact_hash"] == \
        "516c1a8b1bfa2f84a39f0423220ecb37f8880e8916e961e61909f5cc933d7cd8"
    assert a["supported_fact"]["raw_numerator_support"] == 5155
    assert a["supported_fact"]["raw_denominator_support"] == 5155

def test_as2b_is_historical_only_not_current_original(hist):
    assert hist["grade"] == "HISTORICAL_SCOPE_POSITIVE"
    assert hist["current_grant"] is False
    assert hist["occupies_original_measured_cells"] is False
    assert hist["grade"] not in ("ORIGINAL_MEASURED_OCCUPANCY",
                                 "SCIENTIFIC_SOURCE_AUTHORIZED_ACCEPTED")

def test_all35_deferred_ledger_no_drop(ho):
    led = ho["deferred_ledger"]
    assert led["wave_count"] == 35
    assert len(led["waves"]) == 35
    assert all(w["native_manifest"] is None for w in led["waves"])
    assert all(w["state"] == "NOT_YET_ISSUED" for w in led["waves"])
    assert led["U_E_pre_count"] is None

def test_single_decision_is_exact_and_issuer_bound(ho):
    d = ho["single_decision"]
    assert d["selected_wave"] == "SRC27"
    assert d["exact_source_identity"]["source_sha256"] == \
        "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
    assert len(d["exact_missing_competent_decisions"]) == 5
    assert d["grant_present"] is False
    assert d["worker_can_self_issue"] is False
    assert "15-section" in d["liTS_c11_prerequisite"]["missing"]

def test_runtime_requires_authenticated_members():
    class Bad:
        host = "H"
        purpose = "P"
    with pytest.raises(handoff.S44RuntimeRefused, match="RUNTIME_INCOMPLETE"):
        handoff.validate_runtime(Bad())

def test_u43_entrypoint_is_real(ho):
    e = ho["u43_entrypoint"]
    assert e["module"] == "rawlsing_next.pre553_issued_workload"
    assert "execute_issued_workload" in e["symbols"]

def test_a42_v4_delta_is_truthful():
    d = json.loads((RETURN / "s44_a42_source_grade_delta.json").read_text())
    assert d["after_s44"]["original_measured"] == 0
    assert d["new_original_measured_cells"] == 0
    assert d["new_historical_cells"] == 2
    assert d["after_s44"]["missing"] == 1777
    assert d["source_positive_state"] == "FIRST_ORIGINAL_CURRENT_B_MEASURED_NOT_YET_EARNED"

def test_a42_v4_is_not_ready():
    m = json.loads((RETURN / "s44_a42_v4_estate_acceptance_manifest.json").read_text())
    assert m["verdict"]["n11_state"] == "N11_NOT_READY"
    assert m["verdict"]["original_measured_occupied_cells"] == 0
    f = json.loads((RETURN / "s44_a42_v4_f1_f8_acceptance_matrix.json").read_text())
    assert f["row_count"] == 283
    assert f["n11_state"] == "N11_NOT_READY"
