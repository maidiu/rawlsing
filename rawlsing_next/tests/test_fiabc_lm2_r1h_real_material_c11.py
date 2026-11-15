from __future__ import annotations

import hashlib
import json
from pathlib import Path

from rawlsing_next.fiabc_lm2_r1e_browser_prep import validate_frozen_response_carrier
from rawlsing_next.fiabc_lm2_r1e_common_c11 import common_c11_receipt

ROOT = Path(__file__).resolve().parents[2]
CARRIER = ROOT / "WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY/LOCAL_OUTPUT/FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER.json"
EXPECTED_SHA256 = "1aea888d8d576fc8606d56dd7a3b1a552411b8f8126ea27a54c36ff6d551dd7e"
EXPECTED_BYTES = 83340882
EXPECTED_ROWS = 97220
EXPECTED_CELLS = 194440
EXPECTED_SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
EXPECTED_STRUCTURAL = "151907b3163959d0eb5ebb020fa5253d33447362420e465600035744112fe5bc"
EXPECTED_PROJECTION_AUTHORITY = "6b0dba629206c563d30bdb86f4f8bb112b24eb0ceaf05e47aec6aa049dbf23c0"
EXPECTED_PROJECTION_IDENTITY = "8d6ee3fac396d7bd0e0afdf2f4fb13bcc8f040e53d63dd4c0d559b65c9ade4df"
QUESTION_ORDER = ("Q291G5", "Q291P5")
ORDINALS = {"Q291G5": 388, "Q291P5": 394}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def test_gate1_exact_persisted_carrier_preflight(capsys):
    assert CARRIER.is_file()
    assert CARRIER.stat().st_size == EXPECTED_BYTES
    assert _sha256_file(CARRIER) == EXPECTED_SHA256

    existing = validate_frozen_response_carrier(CARRIER)
    assert existing["status"] == "PASS__ACCEPTED_FROZEN_RESPONSE_CARRIER_PRESENT"
    assert existing["rows"] == EXPECTED_ROWS
    assert tuple(existing["questions"]) == QUESTION_ORDER

    doc = json.loads(CARRIER.read_text(encoding="ascii"))
    assert doc["schema"] == "FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER@1.0.0"
    assert doc["source_sha256"] == EXPECTED_SOURCE_SHA256
    assert doc["structural_preimage_identity"] == EXPECTED_STRUCTURAL
    assert doc["row_count"] == EXPECTED_ROWS
    assert tuple(doc["question_names"]) == QUESTION_ORDER
    assert doc["candidate_neutral"] is True
    assert doc["contains_candidate_output"] is False
    assert len(doc["rows"]) == EXPECTED_ROWS

    physical_cells = 0
    for expected_row, row in enumerate(doc["rows"], 1):
        assert row["row_ordinal"] == expected_row
        for question in QUESTION_ORDER:
            cell = row[question]
            assert cell["variable_name"] == question
            assert cell["variable_ordinal"] == ORDINALS[question]
            assert "raw_physical_value_witness" in cell
            assert "physical_missing_state" in cell
            assert "source_missing_declaration" in cell
            physical_cells += 1
    assert physical_cells == EXPECTED_CELLS

    receipt = {
        "gate": "GATE_1_CARRIER_PREFLIGHT",
        "status": "PASS",
        "carrier_path": str(CARRIER.relative_to(ROOT)),
        "carrier_sha256": EXPECTED_SHA256,
        "carrier_bytes": EXPECTED_BYTES,
        "row_count": EXPECTED_ROWS,
        "physical_cells": physical_cells,
        "question_names": list(QUESTION_ORDER),
        "source_sha256": doc["source_sha256"],
        "structural_preimage_identity": doc["structural_preimage_identity"],
        "candidate_neutral": doc["candidate_neutral"],
        "contains_candidate_output": doc["contains_candidate_output"],
        "existing_validator": existing,
    }
    with capsys.disabled():
        print("FIABC_LM2_R1H_GATE1=" + json.dumps(receipt, sort_keys=True, separators=(",", ":")))


def test_r15_real_candidate_neutral_common_c11(capsys):
    receipt = common_c11_receipt(CARRIER)

    assert receipt["source_sha256"] == EXPECTED_SOURCE_SHA256
    assert receipt["structural_preimage_identity"] == EXPECTED_STRUCTURAL
    assert receipt["projection_authority_ref"]["authority_content_hash"] == EXPECTED_PROJECTION_AUTHORITY
    assert receipt["projection_identity_ref"]["content_hash"] == EXPECTED_PROJECTION_IDENTITY
    assert receipt["candidate_neutral"] is True
    assert receipt["candidate_outputs_exposed"] == 0
    assert receipt["public_object_count"] > 0
    assert receipt["internal_record_count"] > 0

    with capsys.disabled():
        print("FIABC_LM2_R1H_R15=" + json.dumps(receipt, sort_keys=True, separators=(",", ":")))
