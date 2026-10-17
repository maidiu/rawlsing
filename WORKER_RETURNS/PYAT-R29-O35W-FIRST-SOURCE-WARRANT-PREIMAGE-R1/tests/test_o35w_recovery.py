"""O35W sourcefree recovery validation.

No original SAV/DTA is opened.  The tests verify the recovered WGE preimage,
its result-independence, the historical R5 GT2 geometry/terminal, the WGD
retired-key finding, and the 35-wave authority matrix.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import zipfile

import pytest

RET = pathlib.Path(__file__).resolve().parents[1]
E = RET / "evidence"
ZIP = pathlib.Path(
    "/Users/matthewsmith/Downloads/"
    "PYAT_HQ280_WGE_PREOUTCOME_GT2_E2B_POSITIVE_RETURN_R1.zip")
EXPECTED_KEY = "2ee8980a96a73351102c9b814f5d51464c2e7b2d1d625da6f3be8b3dc60e437a"
EXPECTED_TERMINAL = "269573bf9c69fd0ca2c6d0c018d67dde817132bdc2298c85d9e4304161a759d7"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def load(name):
    return json.loads((E / name).read_text())


def test_wge_zip_hash_matches_external_receipt():
    receipt = load("WGE_ZIP_RECEIPT.json")
    assert receipt["zip_sha256"] == \
        "38eed1fcd19d5aaefb3dc84f88a5549ca01f054599b46f35e68662c843a66935"
    assert receipt["zip_bytes"] == 13776082
    if ZIP.exists():
        assert sha(ZIP) == receipt["zip_sha256"]


def test_wge_small_members_match_wge_manifest():
    manifest = load("WGE_06_EVIDENCE_MANIFEST.json")
    by_suffix = {e["path"]: e["sha256"] for e in manifest["entries"]}
    checks = {
        "00_RETURN.md": "WGE_00_RETURN.md",
        "02_PRE_RESULT_EXPECTED_OPERATION_VS_ACTUAL_PRODUCT.json":
            "WGE_02_PRE_RESULT_EXPECTED_OPERATION_VS_ACTUAL_PRODUCT.json",
        "05_ISSUER_SCOPE_AND_ADOPTION_HOLDS.md":
            "WGE_05_ISSUER_SCOPE_AND_ADOPTION_HOLDS.md",
    }
    for suffix, local in checks.items():
        expected = next(v for k, v in by_suffix.items() if k.endswith(suffix))
        assert sha(E / local) == expected, local


def test_recovered_epre_preimage_hashes_to_exact_key():
    d = load("WGE_02_PRE_RESULT_EXPECTED_OPERATION_VS_ACTUAL_PRODUCT.json")
    mat = d["pre_result_expected_operation"]["material"]
    canon = json.dumps(mat, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False).encode()
    assert hashlib.sha256(canon).hexdigest() == EXPECTED_KEY
    assert d["pre_result_expected_operation"]["proposed_expected_operation_key"] == \
        EXPECTED_KEY
    assert d["pre_result_expected_operation"]["material_sha256"] == EXPECTED_KEY


def test_preimage_contains_no_produced_result_identity():
    d = load("WGE_02_PRE_RESULT_EXPECTED_OPERATION_VS_ACTUAL_PRODUCT.json")
    mat = d["pre_result_expected_operation"]["material"]
    text = json.dumps(mat, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)
    for produced in [
        "540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46",
        "3530f08f43e704ad67e0fb74984b03b7ad0f068ea1de4bcf658f3b2d591bd56d",
        "a008553dc94af138de44e73ade8ddbcc1e2bb3a5c40cec575aad694aae104cbb",
        "1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19",
        "2c7fb3f81343179ad75c6441fadcd09201aa47b9dc0e032383071e83cc4e022a",
        "47594be9aaf284122f76e3f2e3d74af29054ae3e1d6228134e4eccfdacfa46d1",
        "205f5049be54eb226a35fad1561554c52f830d858bbf9a642167b3f96c281fda",
        "e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0",
        "bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3",
        "c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f",
        "8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295",
        "ecb7411003a96966d703fc88a28d973b",
    ]:
        assert produced not in text, produced


def test_historical_36_cell_geometry_and_raw_denominator():
    geom = load("WGE_03_GEOMETRY_AND_TERMINAL_SUMMARY.json")
    proof = geom["native_36_cell_geometry_lineage_proof"]
    assert geom["execution_status"] == "EXECUTED"
    assert geom["exit_code"] == 0
    assert proof["cell_count"] == 36
    assert proof["cell_state_counts"] == {
        "OBSERVED_POSITIVE": 13,
        "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET": 23,
    }
    assert proof["raw_numerator_sum"] == 19210
    assert proof["risk_set_member_count"] == 19210
    cells = proof["cells"]
    assert len(cells) == 36
    assert sum(c["raw_numerator_support"] for c in cells) == 19210
    assert sum(c["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
               for c in cells) == 23


def test_historical_terminal_hash_matches_wge_r_receipt():
    geom = load("WGE_03_GEOMETRY_AND_TERMINAL_SUMMARY.json")
    assert geom["terminal_sha256"] == EXPECTED_TERMINAL
    # Recompute from the exact external archive when it is present.
    if ZIP.exists():
        with zipfile.ZipFile(ZIP) as z:
            name = next(n for n in z.namelist()
                        if n.endswith("03_GENUINE_E2B_RUNTIME_EXECUTION.json"))
            full = json.loads(z.read(name))
            term = full["runtime_payload"]["terminal"]
            canon = json.dumps(term, sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False).encode()
            assert hashlib.sha256(canon).hexdigest() == EXPECTED_TERMINAL
    # corroborated by the HQ-received WGE-R receipt: same typed terminal.
    claim = (E / "WGE_R_HQ_RECEIPT.md").read_text()
    assert EXPECTED_TERMINAL in claim
    assert "38eed1fcd19d5aaefb3dc84f88a5549ca01f054599b46f35e68662c843a66935" in claim
    assert "cc346273cf843ed90719ed6608e0dfc684a62741244dddc41d5644f0dbec2391" in claim


def test_wgd_only_issued_key_is_the_retired_result_key():
    wgd = load("WGD_02_ISSUED_EXPECTED_WORK_PREIMAGES_AND_HOLDS.json")
    assert wgd["issued_expected_work_count"] == 1
    assert wgd["issued"][0]["scientifically_issued_expected_work_key"] == \
        "ecb7411003a96966d703fc88a28d973b"
    wge = load("WGE_02_PRE_RESULT_EXPECTED_OPERATION_VS_ACTUAL_PRODUCT.json")
    assert wge["supersedes_wgd_key"]["status"] == \
        "REJECTED_AS_PRE_OUTCOME_EXPECTED_WORK_KEY__RETIRED"


def test_35_wave_matrix_has_no_current_signed_warrant_and_one_recovered_preimage():
    m = json.loads((RET / "01_ORIGINAL_WAVE_SOURCE_ISSUER_AND_U_EPRE_MATRIX.json").read_text())
    assert m["summary"]["total_waves"] == 35
    assert m["summary"]["verified_current_warrants"] == 0
    assert m["global_authority_finding"]["signed_current_warrants_found"] == 0
    assert m["global_authority_finding"]["named_source_data_signer_found"] is False
    recovered = [w["atlas_id"] for w in m["waves"]
                 if w["e_pre_status"].startswith("EXACT_PREIMAGE")]
    assert recovered == ["SRC02"]
    assert m["summary"]["historical_narrow_use"] == ["SRC02", "SRC03", "SRC27"]
    assert all(w["new_original_processing_authorization"] in {
        "UNAUTHORIZED_FOR_NEW_ORIGINAL_PROCESSING", "INAPPLICABLE_FRESH_READ"}
        for w in m["waves"])


def test_unsigned_template_is_not_a_warrant():
    t = json.loads((E / "C4B_07_UNSIGNED_SOURCE_WARRANT_TEMPLATE.json").read_text())
    assert t["signed"] is False
    assert t["authorizes_access"] is False
    assert t["status"] == "NOT_AUTHORIZED_UNTIL_HQ_AND_REQUIRED_USER_RESOURCE_OWNER_APPROVAL"
    assert t["approvals"]["HQ"]["decision"] is None
    assert t["approvals"]["required_user_resource_owner"]["decision"] is None
