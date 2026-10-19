from __future__ import annotations
import json
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]

def test_b43_delta_is_truthful():
    d = json.loads((RETURN / "b43_a42_source_grade_delta.json").read_text())
    assert d["truthful_original_measured_occupancy"] == 0
    assert d["new_original_measured_cells"] == 0
    assert d["source_grant_present"] is False
    assert d["source_positive_state"] == "SOURCE_EXECUTION_PENDING_OWNER"
    assert d["after_b43"]["original_measured_occupied_cells"] == 0

def test_b43_answer_artifacts_exist_and_are_not_green():
    m = json.loads((RETURN / "b43_a42_v2_estate_acceptance_manifest.json").read_text())
    assert m["verdict"]["n11_state"] == "N11_NOT_READY"
    assert m["verdict"]["original_measured_occupied_cells"] == 0
    f = json.loads((RETURN / "b43_a42_v2_f1_f8_acceptance_matrix.json").read_text())
    assert f["row_count"] == 283
